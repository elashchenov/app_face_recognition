import os
import threading
import pytest
import mock
from mock import patch
import base64
import requests
import time
import json

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import main
import train
from waitress import serve
import configs.config as config

def run_flask_app():
    app = main.app
    main.serve(app, host=config.host, port=config.port)


t = threading.Thread(target=run_flask_app)
t.start()
user_id = '12345'

absolute_path = '/Users/lashchenov/university/ТРКПО Маслаков/app_access_with_Face_Recognition/neural_network'

class TestNeural:

    @patch('train.CustomCallback.on_epoch_end')
    def test_train_model(self, mock_callback):
        """Проверка обучения модели и создание весов модели"""

        list_binary_images_train = []
        # print(os.listdir('.'))
        for test_img in os.listdir(f'{absolute_path}/tests/images/train'):
            with open(os.path.join(f'{absolute_path}/tests/images/train', test_img), 'rb') as img_bytes:
                list_binary_images_train.append(
                    base64.b64encode(bytes(str(img_bytes.read()), "utf-8")).decode('ascii')
                )

        list_binary_images_test = []
        for test_img in os.listdir(f'{absolute_path}/tests/images/test'):
            with open(os.path.join(f'{absolute_path}/tests/images/test', test_img), 'rb') as img_bytes:
                list_binary_images_test.append(
                    base64.b64encode(bytes(str(img_bytes.read()), "utf-8")).decode('ascii')
                )

        print('here')

        response = requests.get("http://localhost:5000/1.0.0/neural-network/train-model",
                     json=[user_id, list_binary_images_train, list_binary_images_test])
        assert response.content == b'success'
        time.sleep(120)

        assert os.path.isfile(f'{absolute_path}/models/{user_id}/model_face.h5')
        test_images = os.listdir(f'{absolute_path}/images/{user_id}/test/{user_id}')
        train_images = os.listdir(f'{absolute_path}/images/{user_id}/train/{user_id}')
        assert len(test_images) == 40 and len(train_images) == 160

    def test_get_model(self):
        """Проверка возвращения весов модели"""
        response = requests.get("http://localhost:5000/1.0.0/neural-network/get-model",
                                json={"id_user": user_id})
        response_data = json.loads(response.content)
        assert len(response_data)



@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def exit():
        os._exit(0)
    request.addfinalizer(exit)