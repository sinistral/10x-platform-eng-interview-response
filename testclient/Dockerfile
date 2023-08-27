
FROM python:3.10.13-bullseye

WORKDIR /var/10x/app

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD testclient.py .

CMD ["testclient.py"]
ENTRYPOINT ["python"]
