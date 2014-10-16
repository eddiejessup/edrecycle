import sqlite3
import parse
import string
import json


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def put_data():
    for letter in string.uppercase:
        print(letter)
        put_letter_data(letter)


def put_letter_data(letter):
    conn = sqlite3.connect('recyfans.db')
    c = conn.cursor()

    letter_data = parse.uncache_letter_data(letter)
    for data in letter_data:
        location = data.get('location')
        filename = data.get('filename')
        blue_dates_py = data.get('blue_dates')
        blue_dates = json.dumps(blue_dates_py, default=date_handler)
        red_dates_py = data.get('red_dates')
        red_dates = json.dumps(red_dates_py, default=date_handler)
        pdf = data.get('pdf_link')
        day = data.get('day')
        c.execute("insert into locations values(?, ?, ?, ?, ?, ?)",
                  (location, filename, blue_dates, red_dates, pdf, day))

        print(location)
    conn.commit()
    conn.close()


def make_db():
    conn = sqlite3.connect('recyfans.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE locations
              (location text, filename text, blue_dates text, red_dates text,
              pdf text, day text)''')
