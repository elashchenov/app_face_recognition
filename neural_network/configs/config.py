import os

host = "localhost"
port = "5000"
host_api_db = "http://localhost"
port_api_db = "5050"

work_path = r"/Users/lashchenov/university/ТРКПО Маслаков/app_access_with_Face_Recognition/neural_network"

path_to_images = os.path.join(work_path, "images")
path_to_models = os.path.join(work_path, "models")

api_set_percent = f'{host_api_db}:{port_api_db}/database/1.0.0/set-percent/'
