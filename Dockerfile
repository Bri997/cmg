FROM python:3.8

ADD app/main.py .
RUN mkdir -p /upload

ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "./main.py"]