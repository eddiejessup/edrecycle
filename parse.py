from __future__ import print_function
from BeautifulSoup import BeautifulSoup
import datetime
import urllib2
from urlparse import urljoin
import string
import pickle
from os.path import join

project_path = '/Users/ejm/Projects/recyfans'

domain_name = 'http://www.edinburgh.gov.uk/'
base_index_path = 'directory/143/a_to_z/'
index_base = urljoin(domain_name, base_index_path)
field_names = {
    'blue_dates': 'Blue Box Dates',
    'red_dates': 'Red Box Dates',
    'day': 'Collection Day',
    'link': 'Download Calendar',
    'properties_served': 'Properties Served',
}


def parse_dates(dates_raw):
    dates_string = dates_raw.string.strip().split(', ')
    dates = []
    for date_string in dates_string:
        date_string = date_string.strip(',')
        day, month, year = [int(n) for n in date_string.split('/')]
        # When python 3 is supported, add this argument to datetime:
        # tzinfo=pytz.timezone('Europe/London')
        date = datetime.date(year=year, month=month, day=day)
        dates.append(date)
    return dates


def parse_collection_day(raw):
    return raw.string.strip()


def parse_link(raw):
    return raw.find('a').string


def parse_location(soup):
    return soup.find("meta", {"name": "description"})['content']


def location_link_to_recycle_data(url):
    page = urllib2.urlopen(url).read()
    return location_page_to_recycle_data(page)


def location_page_to_recycle_data(page):
    s = BeautifulSoup(page)
    data = {}

    data['location'] = parse_location(s)
    data['filename'] = data['location'].replace(' ', '_').lower()

    table = s.find('table')
    rows = table.findAll('tr')

    for row in rows:
        field = row.find('th').string.strip()
        value = row.find('td')
        if field == field_names['blue_dates']:
            data['blue_dates'] = parse_dates(value)
        elif field == field_names['red_dates']:
            data['red_dates'] = parse_dates(value)
        elif field == field_names['day']:
            data['day'] = parse_collection_day(value)
        elif field == field_names['link']:
            data['pdf_link'] = parse_link(value)
        elif field == field_names['properties_served']:
            data['places_served'] = value.string
        else:
            raise Exception(field, value, data, page.title)
    return data


def index_page_to_location_links(page):
    soup = BeautifulSoup(page)
    links_list = soup.find("ul", {"class": "item-list"})
    if links_list is None:
        return []
    links_raw = links_list.findAll('a')
    links = []
    for link_raw in links_raw:
        link = urljoin(domain_name, link_raw['href'])
        links.append(link)
    return links


def location_links_to_recycle_data(location_links):
    recycle_datas = []
    for location_link in location_links:
        recycle_data = location_link_to_recycle_data(location_link)
        recycle_datas.append(recycle_data)
    return recycle_datas


def letter_to_recycle_data(letter):
    index_link = urljoin(index_base, letter)
    index_page = urllib2.urlopen(index_link).read()
    location_links = index_page_to_location_links(index_page)
    recycle_data = location_links_to_recycle_data(location_links)
    return recycle_data


def pickle_dump(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def pickle_load(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def pickle_dump_letter(letter, filename, minimal=False):
    recycle_data = letter_to_recycle_data(letter)
    if minimal:
        for data in recycle_data:
            for key in data.keys():
                if key not in ['location', 'filename']:
                    data.pop(key)
    pickle_dump(recycle_data, filename)


def letter_to_cache_filename(letter, minimal):
    dir_name = 'recycle_data_min' if minimal else 'recycle_data'
    return join(project_path, dir_name, '{}.pkl'.format(letter))


def cache_all_data(minimal=False):
    for letter in string.uppercase[5:]:
        print(letter)
        cache_letter_data(letter, minimal)


def cache_letter_data(letter, minimal=False):
    cache_filename = letter_to_cache_filename(letter, minimal)
    pickle_dump_letter(letter, cache_filename, minimal)


def uncache_letter_data(letter, minimal=False):
    return pickle_load(letter_to_cache_filename(letter, minimal))
