from fastapi import FastAPI, HTTPException
from src.delivery_region import DeliveryRegion
import brazilcep
from geopy.geocoders import Nominatim
import geopy.distance
from joblib import load
from pathlib import Path
import sys 

app = FastAPI()

path = Path().joinpath().joinpath('..')
sys.path.append(str(path))

delivery_region = DeliveryRegion()

@app.get("/", summary="Bootcamp root parh")
async def bootcamp():
    return {"message": "Bem-vindo ao bootcamp!"}

@app.get("/get-lat-lng-cep/{cep}", summary="Retorna latitude e longitude de um CEP")
def get_delivery_region_info(cep):

    # Busca os dados de um CEP
    address = brazilcep.get_address_from_cep(cep)

    # Usa um geo localizador de endereços para buscar a lat, lng
    geolocator = Nominatim(user_agent="test_app")
    location = geolocator.geocode(address['street'] + ", " + address['city'] + " - " + address['district'])

    # Prepara o resultado do endpoint
    result = {
        'lat': location.latitude,
        'lng': location.longitude
    }

    return result

@app.get("/get-delivery-region/{lat}/{lng}", summary="Valida região de entrega")
def get_delivery_region(lat, lng):

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