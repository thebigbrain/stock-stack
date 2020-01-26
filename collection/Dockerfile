FROM python

WORKDIR /app

EXPOSE 5000

RUN pip install pymongo
RUN pip install flask
RUN pip install uwsgi

COPY . ./collection

#CMD sh -c "uwsgi --http 0.0.0.0:5000 --module collection.rest-serv:app"