FROM python:3

WORKDIR /solution

COPY [".", "/solution"]

RUN pip install --no-cache-dir -r /solution/requirements.txt

EXPOSE 80

CMD gunicorn --workers=16 --access-logfile - --error-logfile - -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker api.main:app