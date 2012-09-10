import httplib2
import sys
import urllib2
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from .models import (
    DBSession,
    MenuItem,
    Menu,
    Allergen,
    )

CALENDAR_ID = '/home/tina/client_secrets.json'
CLIENT_SECRETS = '/home/tina/credentials.dat'

health_color = ['\033[92m', '\033[93m', '\033[91m']
 
def color(text, color):
    return u"%s%s%s" % (color, text, '\033[0m')

def get_menu_name(menu):
    time = int(menu.time_sort_key)
    if time == 1:
        meal = 'Breakfast'
    elif time == 2:
        meal = 'Lunch'
    else:
        meal = 'Dinner'

    menu_name = str(menu.date) + ' ' + meal 
    if len(menu.name):
        menu_name = menu_name + ': ' + menu.name
    return menu_name

def get_menu_desc(menu):
    desc = '' 
    if len(menu.menus) < 1:
        return ''
    for menu_item_id in menu.menus.split(' '):
        menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
        allergens = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
        allergen_string = ', '.join([a.allergen for a in allergens])
        desc = '\n' + desc
        if menu_item.healthy:
            color_icon = color(u'\u2764', health_color[menu_item.healthy-1])
            desc = desc + color_icon + ' ' 
        
        desc = desc + menu_item.name;
        
        desc = desc + '\n'
        if len(menu_item.description):
            desc = desc + menu_item.description + '\n'
        if len(allergen_string):
            desc = desc + '(' + allergen_string + ')\n' 
    return desc.strip('\n')

def update_menu_on_google_calendar(menu):
    try:
        with open(CLIENT_SECRETS) as f: pass
    except IOError as e:
        print 'no client secret stored'
        return;
            
    storage = Storage(CLIENT_SECRETS)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        print "we are in trouble. credential invalid!!!"
        credentials.refresh(httplib2.Http())

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('calendar', 'v3', http=http)

    try:
        print 'time sort key is %d', menu.time_sort_key
        time = int(menu.time_sort_key)
        if time == 1:
            start_time = '08'
            end_time = '10'
            meal = 'Breakfast'
        elif time == 2:
            start_time = '12'
            end_time = '14'
            meal = 'Lunch'
        else:
            start_time = '18'
            end_time = '20'
            meal = 'Dinner'

        json_data = open(CALENDAR_ID)
        data = json.load(json_data)
        json_data.close()
        #find the event
        events = service.events().list(calendarId=data["tuckshop_calendar_id"], timeMin=str(menu.date) + 'T' + start_time + ':00:00.000-07:00', timeMax=str(menu.date) + 'T' + end_time + ':00:00.000-07:00').execute()

        if 'items' in events and events['items'] and len(events['items']) == 1:
            event = events['items'][0]
            desc = get_menu_desc(menu)
            event['summary'] = get_menu_name(menu)
            event['description'] = desc
            updated_event = service.events().update(calendarId=data["tuckshop_calendar_id"], eventId=event['id'], body=event).execute()
            print updated_event['updated']
       
        else:
            print 'creating new event'
            event = {
            'summary': get_menu_name(menu),
            'location': 'Tuckshop',
            'start': {
                'dateTime': str(menu.date) + 'T' + start_time + ':00:00.000-07:00'
                },
            'end': {
                    'dateTime': str(menu.date) + 'T' + end_time + ':00:00.000-07:00'
                },
            'description': get_menu_desc(menu),
            }

            created_event = service.events().insert(calendarId=data["tuckshop_calendar_id"], body=event).execute()
    except AccessTokenRefreshError:
        #just added
        print 'refreshing'
        credentials.refresh(httplib2.Http())
        print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')

def delete_all():
    try:
        with open(CLIENT_SECRETS) as f: pass
    except IOError as e:
        print 'no client secret stored'
        return;

    storage = Storage(CLIENT_SECRETS)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        print "we are in trouble. invalid credential!!!"
        credentials.refresh(httplib2.Http())

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)

    try:
        json_data = open(CALENDAR_ID)
        data = json.load(json_data)
        json_data.close()
        #find the event
        events = service.events().list(calendarId=data["tuckshop_calendar_id"]).execute()

        if 'items' in events and events['items'] and len(events['items']) >= 1:
            for event in events['items']:
                print 'deleting event with id %r' % event['id']
                service.events().delete(calendarId=data["tuckshop_calendar_id"], eventId=event['id']).execute()
        else:
            print 'nothing to delete'

    except AccessTokenRefreshError:
        #just added
        print 'refreshing'
        credentials.refresh(httplib2.Http())
        print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')
