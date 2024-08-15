import configparser
from joblib import load
import mlflow

class DeliveryRegion:

    # Construtor
    def __init__(self, env = 'PROD'):
        
        self.env = env
        self.app_config = self.get_app_config(env)
        self.version = self.app_config['version']
    
    # Carrega das configurações da aplicação
    def get_app_config (self, env):

        app_config = configparser.ConfigParser()
        #app_config.read('/app/api/config/app_config.ini')
        app_config.read('config/app_config.ini')
        return app_config[env]
    
    def get_model_uri_by_name_and_alias(self, model_name, alias):
    
        # Initialize MLflow client
        client = mlflow.tracking.MlflowClient()
        
        # Get the model version details by alias
        model_version_details = client.get_model_version_by_alias(name=model_name, alias=alias)
        
        # Construct the model URI
        model_uri = f"models:/{model_name}/{model_version_details.version}"
        
        return model_uri, model_version_details.run_id