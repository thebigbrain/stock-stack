FROM python

WORKDIR /app

EXPOSE 5000

RUN pip install pymongo
RUN pip install flask

COPY . ./collection

CMD ["export FLASK_APP=./collection/rest-serv.py; flask run"]