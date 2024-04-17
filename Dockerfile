FROM python:3.12.3
ADD . /ppnaforecast
WORKDIR /ppnaforecast
RUN pip install -r requirements.txt