FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY requirements.txt /app/

WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /app/data && chown datapunt /app/data
RUN mkdir -p /static && chown datapunt /static

ENV DJANGO_SETTINGS_MODULE=bbga.settings

USER datapunt

RUN python manage.py collectstatic

CMD uwsgi
