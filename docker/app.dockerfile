FROM python:3.6.5

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn app.main:app --bind ${BIND_HOST}:${BIND_PORT} --worker-class aiohttp.GunicornWebWorker -w ${WORKERS_NUMBER}