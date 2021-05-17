FROM centos/python-38-centos7:latest

USER root

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install --upgrade --force --no-dependencies \
    https://github.com/apple/tensorflow_macos/releases/download/v0.1alpha3/tensorflow_macos-0.1a3-cp38-cp38-macosx_11_0_arm64.whl \
    https://github.com/apple/tensorflow_macos/releases/download/v0.1alpha3/tensorflow_addons_macos-0.1a3-cp38-cp38-macosx_11_0_arm64.whl

CMD ["python3", "main.py"]