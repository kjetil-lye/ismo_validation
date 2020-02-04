FROM tensorflow/tensorflow:2.1.0-py3

COPY requirements.txt /requirements.txt
RUN apt update && apt install --yes git
RUN pip install -r requirements.txt
