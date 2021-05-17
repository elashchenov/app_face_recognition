import configs.config as config
__version__ = "1.0.0"
base_address = f"/{__version__}/neural-network"

get_model = f"{base_address}/get-model"
train_model = f"{base_address}/train-model"
face_verify = f"{base_address}/face-verify"
