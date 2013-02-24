#!/usr/bin/env python

import httplib2
import sys
import urllib2
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from sqlalchemy import engine_from_config

from models import (
    DBSession,
    MenuItem,
    Menu,
    Allergen,
    )

from pyramid.paster import (
    get_appsettings,
)


CALENDAR_ID = '/home/tina/client_secrets.json'
CLIENT_SECRETS = '/home/tina/credentials.dat'

health_icon = ['\xe2\x97\x95\xe2\x80\xbf\xe2\x97\x95', '\xe2\x8a\x99\xef\xb9\x8f\xe2\x8a\x99', '\xe0\xb2\xa0_\xe0\xb2\xa0']
THREE_MEALS = ['Breakfast', 'Lunch', 'Dinner']
HEALTHY_FACTOR = ["Healthy", "Moderate", "Unhealthy"]
#three entries correspond to breskfast, lunch, dinner
#first number is the start time, second number is the end time
CALENDAR_MEAL_TIMES = [['09', '11'], ['13', '15'], ['19', '21']]

config_uri = "/home/tina/MenuProject/development.ini"
settings = get_appsettings(config_uri)
engine = engine_from_config(settings, 'sqlalchemy.')
DBSession.configure(bind=engine)

def get_menu_name(menu):
    meal = THREE_MEALS[int(menu.time_sort_key-1)]
    menu_name = str(menu.date) + ' ' + meal
    if menu.name:
        menu_name = menu_name + ': ' + menu.name
    return menu_name

def get_menu_desc(menu, for_calendar):
    desc = ''
    json_result = []
    if len(menu.menus) < 1:
        return ''
    for menu_item_id in menu.menus.split(' '):
        menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
        allergens = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
        allergen_string = ', '.join([a.allergen for a in allergens])
        desc = '\n' + desc
        menu_item_name = menu_item.name.decode('utf8')
        desc = desc + menu_item_name
        if  menu_item.healthy:
            if for_calendar:
                desc = desc + '\n' + health_icon[menu_item.healthy-1].decode('utf8') + ' ' + HEALTHY_FACTOR[menu_item.healthy-1] + ' '
            else:
                desc = desc + '\n' + '(' + HEALTHY_FACTOR[menu_item.healthy-1] + ') '

        desc = desc + '\n'
        if len(menu_item.description.decode('utf8')):
            menu_item_desc = menu_item.description.decode('utf8')
            desc = desc + menu_item_desc + '\n'
        if len(allergen_string):
            desc = desc + '(' + allergen_string + ')\n\n'
        json_result.append((menu_item_name, menu_item_desc))
    return desc.strip('\n')

def get_menu_json(menu):
    json_result = []
    if len(menu.menus) < 1:
        return ''
    for menu_item_id in menu.menus.split(' '):
        menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
        allergens = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
        allergen_string = ', '.join([a.allergen for a in allergens])
        menu_item_name = menu_item.name.decode('utf8')
        if len(menu_item.description.decode('utf8')):
            menu_item_desc = menu_item.description.decode('utf8')
        json_result.append((menu_item_name, menu_item_desc))
        return json.dumps(json_result)

def update_menu_on_google_calendar(menu_id):
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
        #validate input
        menu_query = DBSession.query(Menu).filter(Menu.id==int(menu_id))
        if menu_query.count() != 1:
            return
        menu = menu_query.one()
        time = int(menu.time_sort_key)
        meal = THREE_MEALS[time-1]
        start_time = CALENDAR_MEAL_TIMES[time-1][0]
        end_time = CALENDAR_MEAL_TIMES[time-1][1]

        json_data = open(CALENDAR_ID)
        data = json.load(json_data)
        json_data.close()
        #find the event
        events = service.events().list(calendarId=data["tuckshop_calendar_id"], timeMin=str(menu.date) + 'T' + start_time + ':00:00.000-07:00', timeMax=str(menu.date) + 'T' + end_time + ':00:00.000-07:00').execute()

        if 'items' in events and events['items'] and len(events['items']) == 1:
            event = events['items'][0]
            desc = get_menu_desc(menu, True)
            event['summary'] = get_menu_name(menu)
            event['description'] = desc
            updated_event = service.events().update(calendarId=data["tuckshop_calendar_id"], eventId=event['id'], body=event).execute()
        else:
            menu_description = u"%s", get_menu_desc(menu, True)
            event = {
            'summary': get_menu_name(menu),
            'location': 'Tuckshop',
            'start': {
                'dateTime': str(menu.date) + 'T' + start_time + ':00:00.000-07:00'
                },
            'end': {
                    'dateTime': str(menu.date) + 'T' + end_time + ':00:00.000-07:00'
                },
            'description': menu_description,
            }

            created_event = service.events().insert(calendarId=data["tuckshop_calendar_id"], body=event).execute()
    except AccessTokenRefreshError:
        #just added
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
        credentials.refresh(httplib2.Http())
        print ('The credentials have been revoked or expired, please re-run'
               'the application to re-authorize')

if __name__ == '__main__':
    update_menu_on_google_calendar(sys.argv[1])
