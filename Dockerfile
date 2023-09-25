FROM python:3.10

WORKDIR /app
RUN pip3 install git+https://github.com/FalkTannhaeuser/python-onvif-zeep ffmpeg-python
COPY src/ /app/