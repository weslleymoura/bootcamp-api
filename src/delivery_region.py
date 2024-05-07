import configparser
from joblib import load

class DeliveryRegion:

    # Construtor
    def __init__(self, env = 'PROD'):
        
        self.env = env
        self.app_config = self.get_app_config(env)
        self.version = self.app_config['version']
        self.n_clusters = int(self.app_config['n_clusters'])
        self.covered_region_in_km = int(self.app_config['covered_region_in_km'])
        self.model = self.get_model(self.app_config['model_location'])
        self.sample_points_location = self.app_config['sample_points_location']
    
    # Carrega das configurações da aplicação
    def get_app_config (self, env):

        app_config = configparser.ConfigParser()
        app_config.read('config/app_config.ini')
        return app_config[env]
    
    # Carrega o modelo
    def get_model (self, model_location):

        return load(model_location) 
    
    # Retorna os centróides de cada cluster
    def get_cluster_centroids (self, model):

        centers = []
        for i, center in enumerate(model.cluster_centers_):
            c = dict()
            c['lat'] = center[0]
            c['lng'] = center[1]
            c['cluster'] = i + 1
            centers.append(c)
            
        return centers