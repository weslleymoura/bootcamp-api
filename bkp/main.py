from fastapi import FastAPI, HTTPException
from src.delivery_region import DeliveryRegion
import brazilcep
from geopy.geocoders import Nominatim
import geopy.distance
from joblib import load
from pathlib import Path
import sys 
path = Path().joinpath().joinpath('..')
sys.path.append(str(path))

from src.database import SessionLocal, engine
from src import models, schemas
from sqlalchemy.orm import Session
from fastapi import Query, Depends

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

app = FastAPI()



delivery_region = DeliveryRegion()

@app.get("/", summary="Bootcamp root parh")
async def bootcamp():
    return {"message": "Bem-vindo ao bootcamp!"}

@app.get("/get-delivery-region/{lat}/{lng}", summary="Valida região de entrega")
def get_delivery_region(lat, lng, db: Session = Depends(get_db)):

    # Prepara as coordenadas do CEP
    coords_cep = (lat, lng)

    # Lista centróides dos clusters
    centers = delivery_region.get_cluster_centroids(delivery_region.model)

    # Verifica a distância (em km) entre o CEP a cada cluster
    res = dict()
    for c in centers:
        coords_cluster = (c['lat'], c['lng'])
        res[c['cluster']] = geopy.distance.geodesic(coords_cep, coords_cluster).km

    # Cria uma lista com as chaves (keys) ordenadas pelos seus valores (values)
    res_sorted_keys = sorted(res, key=res.get, reverse=False)

    # Prepara o resultado do endpoint
    result = {
        'is_region_covered': round(res[res_sorted_keys[0]], 2) <= delivery_region.covered_region_in_km,
        'closest_center': {
            'id': res_sorted_keys[0],
            'distance_in_km': round(res[res_sorted_keys[0]], 2),
            'lat': centers[res_sorted_keys[0]]['lat'],
            'lng': centers[res_sorted_keys[0]]['lng']
        }
    }

    # Registra a chamada da API no banco de dados
    new_api_call = models.ApiCall(
        lat=lat, 
        lng=lng,
        res_is_region_covered = result['is_region_covered'],
        res_closest_center_id = result['closest_center']['id'],
        res_closest_center_distance_in_km = result['closest_center']['distance_in_km'],
        res_closest_center_lat = result['closest_center']['lat'],
        res_closest_center_lng = result['closest_center']['lng'])

    # Add the user to the session
    db.add(new_api_call)

    # Commit the session to persist the changes
    db.commit()

    # Close the session
    db.close()

    return result

@app.get("/get-model-version", summary="Retorna a versão da API")
def get_model_version():

    result = {
        'version': delivery_region.version
    }

    return result

@app.get("/get-clusters", summary="Retorna os centróides de cada cluster")
def get_cluster():

    return delivery_region.get_cluster_centroids(delivery_region.model)

@app.get("/get-sample-points", summary="Retorna alguns pontos (lat, lng) de exemplo para teste da aplicação")
def get_sample_points():

    return load(delivery_region.sample_points_location)