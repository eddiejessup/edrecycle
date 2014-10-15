import icalendar
from icalendar import vText
import string


def recycle_data_to_ical(data):
    cal = icalendar.Calendar()
    cal.add('prodid', '-//Edinburgh Recycling//{}'.format(data['location']))
    cal.add('version', '1.0')
    calendar_name = vText('Edinburgh Recycling - {}'.format(data['location']))
    cal['X-WR-CALNAME'] = calendar_name
    cal['X-WR-CALDESC'] = calendar_name
    cal['X-WR-TIMEZONE'] = vText('Europe/London')

    location_ical = vText('{}, Edinburgh'.format(data['location']))

    for date in data.get('blue_dates', []):
        event = icalendar.Event()
        event.add('Summary', 'Blue bin collection')
        event.add('dtstart', date)
        event['location'] = location_ical
        event['description'] = data['pdf_link']
        cal.add_component(event)
    for date in data.get('red_dates', []):
        event = icalendar.Event()
        event.add('Summary', 'Red bin collection')
        event.add('dtstart', date)
        event['location'] = location_ical
        event['description'] = data['pdf_link']
        cal.add_component(event)
    return cal


def make_all_ical_files():
    for letter in string.uppercase:
        recycle_data = parse.letter_to_recycle_data(letter)
        for location_data in recycle_data:
            cal = recycle_data_to_ical(location_data)
            ical_filename = join(project_path, '/www/icals',
                                 '{}.ical'.format(recycle_data['filename']))
            with open(fname, 'wb') as f:
                f.write(cal.to_ical())
