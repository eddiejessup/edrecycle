from __future__ import print_function
from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import date
import locale
import json

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())

app = Flask(__name__)

# app.config["APPLICATION_ROOT"] = "/edrecycle"

yes = 'Your {color} bin will next be collected on {date}'
no = 'There is no {color} bin collection at this address'
err = 'There is a {color} bin collection, but its next date is unavailable'


@app.route('/_search_data')
def search_data():
    conn = sqlite3.connect('edrecycle.db')
    c = conn.cursor()
    c.execute('select location from locations')
    keys = [results[0] for results in c.fetchall()]
    conn.close()
    return jsonify(keys=keys)


@app.route('/_lookup')
def lookup():
    conn = sqlite3.connect('edrecycle.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    date_now = date.today()

    key = request.args.get('loc', 'nan')
    c.execute("select * from locations where location=?", (key,))
    row = c.fetchone()
    if row is None:
        success = False
        results = []
    else:
        success = True
        results = {'day': row['day'],
                   'location': row['location'],
                   'pdf': row['pdf'],
                   'filename': row['filename'],
                   }
        if row['blue_dates'] != 'null':
            results['blue_msg'] = err.format(color='blue')
            for collect_date in json.loads(row['blue_dates']):
                collect_date_py = date(*[int(n)
                                         for n in collect_date.split('-')])
                if collect_date_py > date_now:
                    next_blue_date = collect_date_py.strftime('%x')
                    results['blue_msg'] = yes.format(color='blue',
                                                     date=next_blue_date)
                    break
        else:
            results['blue_msg'] = no.format(color='blue')
        if row['red_dates'] != 'null':
            results['red_msg'] = err.format(color='red')
            for collect_date in json.loads(row['red_dates']):
                collect_date_py = date(*[int(n)
                                         for n in collect_date.split('-')])
                if collect_date_py > date_now:
                    next_red_date = collect_date_py.strftime('%x')
                    results['red_msg'] = yes.format(color='red',
                                                    date=next_red_date)
                    break
        else:
            results['red_msg'] = no.format(color='red')
        print(results)
    return jsonify(success=success, results=results)


@app.route('/')
def search():
    return render_template('search.jinja')


@app.route('/help')
def help():
    return render_template('help.jinja')


@app.route('/about')
def about():
    return render_template('about.jinja')


# if __name__ == '__main__':
#     app.run(debug=True)
