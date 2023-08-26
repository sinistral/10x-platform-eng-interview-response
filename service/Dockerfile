
FROM python:3.10.13-bullseye

WORKDIR /var/10x/svc

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD weather.py .
ADD seattle-weather.csv .

CMD ["weather.py"]
ENTRYPOINT ["python"]

EXPOSE 8000
