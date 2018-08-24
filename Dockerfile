FROM python:3.7-alpine

ADD . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "init-db"]
CMD ["flask", "run", "--host=0.0.0.0"]