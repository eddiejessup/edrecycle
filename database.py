import couchdb
import parse
from couchdb.mapping import TextField, DateField, ListField, Document
import string


class Location(Document):
    _id = TextField()
    location = TextField()
    filename = TextField()
    blue_dates = ListField(DateField())
    red_dates = ListField(DateField())
    pdf = TextField()
    day = TextField()


def put_data():
    for letter in string.uppercase:
        print(letter)
        put_letter_data(letter)


def put_letter_data(letter):
    couch = couchdb.Server()
    db = couch['locations']
    letter_data = parse.uncache_letter_data(letter)
    for data in letter_data:
        location = Location(_id=data.get('location'),
                            location=data.get('location'),
                            filename=data.get('filename'),
                            blue_dates=data.get('blue_dates'),
                            red_dates=data.get('red_dates'),
                            pdf=data.get('pdf_link'),
                            day=data.get('day'))
        if location._id not in db:
            location.store(db)
            print(data['location'])
