FROM python:3.6

WORKDIR /app

#Ver si conviene agregar todo por ahi no
ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "paths:app", "-b", ":5000"]
#CMD gunicorn paths:app
#CMD ["python3.6", "paths.py"]