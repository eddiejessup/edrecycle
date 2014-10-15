from __future__ import print_function
from flask import Flask, jsonify, request, render_template
from flask.ext.babel import Babel
import couchdb
from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'en_GB')

app = Flask(__name__)
babel = Babel(app)
babel.BABEL_DEFAULT_LOCALE = 'en-gb'

couch = couchdb.Server()
db = couch['locations']


@app.route('/_search_data')
def search_data():
    return jsonify(keys=[r.key for r in db.view('_all_docs').rows])


@app.route('/_lookup')
def lookup():
    date_now = date.today()

    key = request.args.get('loc', 'nan')
    try:
        doc = db[key]
    except couchdb.ResourceNotFound:
        success = False
        results = []
    else:
        success = True
        results = doc
        if doc['blue_dates'] is not None:
            results['blue'] = True
            for collect_date in doc['blue_dates']:
                collect_date_py = date(*[int(n)
                                         for n in collect_date.split('-')])
                if collect_date_py > date_now:
                    results['next_blue_date'] = collect_date_py.strftime('%x')
                    break
        if doc['red_dates'] is not None:
            results['red'] = True
            for collect_date in doc['red_dates']:
                collect_date_py = date(*[int(n)
                                         for n in collect_date.split('-')])
                if collect_date_py > date_now:
                    results['next_red_date'] = collect_date_py.strftime('%x')
                    break
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


if __name__ == '__main__':
    app.run(debug=True)
