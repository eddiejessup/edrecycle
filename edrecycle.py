from __future__ import print_function
from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import date
import locale
import json

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())

app = Flask(__name__)

# app.config["APPLICATION_ROOT"] = "/edrecycle"


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
        results = dict(row)
        if row['blue_dates'] != 'null':
            results['blue'] = True
            for collect_date in json.loads(row['blue_dates']):
                collect_date_py = date(*[int(n)
                                         for n in collect_date.split('-')])
                if collect_date_py > date_now:
                    results['next_blue_date'] = collect_date_py.strftime('%x')
                    break
        else:
            results['blue'] = False
        if row['red_dates'] != 'null':
            results['red'] = True
            for collect_date in json.loads(row['red_dates']):
                collect_date_py = date(*[int(n)
                                         for n in collect_date.split('-')])
                if collect_date_py > date_now:
                    results['next_red_date'] = collect_date_py.strftime('%x')
                    break
        else:
            results['red'] = False
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
