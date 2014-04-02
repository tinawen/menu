from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from datetime import date
import datetime
import time
import threading
import json
import urllib
import calendar
import operator
from gcalendar import get_menu_name
from gcalendar import get_menu_desc
from gcalendar import get_menu_json
from gcalendar import update_menu_on_google_calendar
from gcalendar import THREE_MEALS
from gcalendar import HEALTHY_FACTOR
from datetime import timedelta
from sqlalchemy import distinct
from sqlalchemy import extract
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.url import route_url
import os

from models import (
    DBSession,
    MenuItem,
    Menu,
    Allergen,
    Image,
    )

PRODUCTION_FILE_PATH = '/home/tina/production_mode.txt'
MAIL_SECRETS = '/home/tina/mail_secrets.json'
ALLERGENS = ["Shellfish", "Nuts", "Dairy", "Spicy", "Vegan", "Gluten-free", "Alcohol"]
BREAKFAST_END_HOUR = 9
LUNCH_END_HOUR = 15

#utility function to figure out whether the app is in debug mode
def debug_mode():
    is_debug = not os.path.isfile(PRODUCTION_FILE_PATH)
    return is_debug

#this function converts two integers (month, year) to a displayable string
def convert_to_month_string (month, year):
    return str(calendar.month_name[month]) + ' ' + str(year)

#this function returns a dictionary that maps [month, year] to a string that can be displayed in dropdown
#the dictionary is populated with the current month + all the months that have menus
def build_months_dict():
    month_year_to_string_mapping = {}
    #always add today's month as part of the months dict
    today = datetime.datetime.now()
    today_year = int(today.strftime("%Y"))
    today_month = int(today.strftime("%m"))
    month_year_to_string_mapping[today_month, today_year] = convert_to_month_string(today_month, today_year)

    #now insert all the months that have menus
    distinct_months_years = DBSession.query(extract('month', Menu.date), extract('year', Menu.date)).distinct().all()
    for distinct_month_year in distinct_months_years:
        month = int(distinct_month_year[0])
        year = int(distinct_month_year[1])
        month_year_to_string_mapping[month, year] = convert_to_month_string(month, year)
    return month_year_to_string_mapping

#this function returns a sorted list of dictionaries of all months that should be displayed
#(month, year): month_year_string
def build_months_menu():
    month_year_to_string_mapping = build_months_dict()
    #sort based on the dictionary keys
    sorted_months_years = sorted(month_year_to_string_mapping.items(), key=lambda (x): x[0][0]+(x[0][1]-2012)*12, reverse=True)
    return sorted_months_years

# update menu on google calendar
def update_gcalendar(menu):
    if not debug_mode():
        t = threading.Thread(target=update_menu_on_google_calendar, args=(menu.id, menu.cafe_id))
        t.daemon = True
        t.start()

#send an email about the menu
@view_config(route_name='publish', renderer='string')
def publish(request):
    menuQuery = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    menu = menuQuery.one()
    #only send the email if it hasn't been sent yet
    if not menu.sent:
        mailer = get_mailer(request)
        json_data = open(MAIL_SECRETS)
        data = json.load(json_data)
        json_data.close()

        message = Message(subject=get_menu_name(menu),
                          sender=data["sender"],
                          recipients=[data["recipient"]],
                          body=get_menu_desc(menu, False))
        #print 'sending email to %r' % data["recipient"]
        mailer.send_immediately(message, fail_silently=False)
        menuQuery.update({"sent":True}, synchronize_session=False)
    return json.dumps("Sent")

#returns a dictionary that contains an array of menu items, an array of allergens (each array element corresponds to allergens for the menu item), and the menu, we have to build up the menu_items array to keep the order right
def refresh_menu(menu):
    menu_items = []
    allergens = []
    for menu_item_id in menu.menus and menu.menus.split(' '):
        menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
        allergen_array = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
        menu_items.append(menu_item)
        allergens.append([a.allergen for a in allergen_array])

    return dict(menu_items=menu_items, allergens=allergens, menu=menu, three_meals=THREE_MEALS)

#view all the menus within the month
@view_config(route_name='view_menus_today', renderer='templates/view_menus.jinja2')
@view_config(route_name='view_menus', renderer='templates/view_menus.jinja2')
@view_config(route_name='select_cafe', renderer='templates/view_menus.jinja2')
def view_menus(request):
    if 'cafe_id' in request.matchdict:
        cafe_id = int(request.matchdict['cafe_id'])
    else:
        cafe_id = request.matchdict['cafe_id'] = 1

    #figure out the year and month. If the year and month are in request, use them
    #otherwise use today's year and month
    if 'menu_year' in request.matchdict and 'menu_month' in request.matchdict:
        year = int(request.matchdict['menu_year'])
        month = int(request.matchdict['menu_month'])
    else:
        today = datetime.datetime.now()
        year = int(today.strftime("%Y"))
        month = int(today.strftime("%m"))

    #make an array of weekly menus
    start_date = datetime.datetime(year, month, 1)
    if month == 12:
        end_date = datetime.datetime(year+1, 1, 1)
    else:
        end_date = datetime.datetime(year, month+1, 1)
    week_start_date_list = []
    weekly_menus = []
    week_start_date = end_date
    week_end_date = end_date
    while week_start_date > start_date:
        week_start_date = week_end_date - timedelta(days=week_end_date.isoweekday())
        week_end_date = week_start_date + timedelta(days=7)
        #do the database query, return results in reverse chronilogical order
        menus = DBSession.query(Menu).filter(
            Menu.cafe_id == cafe_id,
            Menu.date >= week_start_date.strftime('%Y-%m-%d'),
            Menu.date < week_end_date.strftime('%Y-%m-%d')).order_by(-Menu.date).order_by(-Menu.time_sort_key).all()
        if len(menus):
            week_start_date_list.append(week_start_date.strftime("%m/%d/%y"))
            weekly_menus.append(menus)
        week_end_date = week_end_date - timedelta(days=7)

    month_menus = build_months_menu()
    month_string = convert_to_month_string(month, year)
    return_params = dict(
        menus=weekly_menus,
        week_start_list = week_start_date_list,
        selected_month_string=month_string,
        month_menus=month_menus,
        menus_monthly_url_prefix=make_link(request, 'view_menus/'),
        menu_url_prefix=make_link(request, 'menu/'),
        three_meals=THREE_MEALS)
    return_params['cafe_id'] = cafe_id
    return return_params

@view_config(route_name='view_menu', renderer='templates/view_menu.jinja2')
def view_menu(request):
    menu = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id']).one()
    return_params = refresh_menu(menu)
    return_params['cafe_id'] = request.matchdict['cafe_id']
    return return_params

def make_link(request, action_name):
    cafe_id = int(request.matchdict['cafe_id'])
    return '/%d/%s' % (cafe_id, action_name)

# view all the menus of the month, in edit view
@view_config(route_name='edit_menus', renderer='templates/edit_menus.jinja2')
@view_config(route_name='edit_menus_today', renderer='templates/edit_menus.jinja2')
def edit_menus(request):
    return_params = view_menus(request)
    return_params['menus_monthly_url_prefix'] = make_link(request, 'edit_menus/')
    return_params['menu_url_prefix'] = make_link(request, 'edit_menu/')
    return_params['create_menu_url'] = make_link(request, 'create_menu')
    return_params['cafe_id'] = request.matchdict['cafe_id']
    return return_params

# editing a specific menu
@view_config(route_name='edit_menu', renderer='templates/edit_menu.jinja2')
def edit_menu(request):
    #get the corresponding menu items and allergens from database
    menu = DBSession.query(Menu).filter(Menu.cafe_id==request.matchdict['cafe_id'], Menu.id==request.matchdict['menu_id']).one()
    return_params = refresh_menu(menu)
    return_params['allergen_list'] = ALLERGENS
    return_params['healthy_factor'] = HEALTHY_FACTOR
    return_params['create_menu_item_url'] = make_link(request, 'create_menu_item/'+ str(menu.id))
    images_id = menu.images_id
    if images_id:
        images_id = images_id.split(' ')
        images = DBSession.query(Image).filter(Image.id.in_(images_id)).all()
        images = [image.thumb_url for image in images]
    else:
        images = []
    return_params['thumbs'] = images
    return_params['cafe_id'] = request.matchdict['cafe_id']
    return return_params

#create a menu
@view_config(route_name='create_menu', renderer='templates/view_menus.jinja2')
def create_menu(request):
    #see if there's already a menu created with the same params
    m = request.matchdict
    menu = DBSession.query(Menu).filter(Menu.cafe_id==request.matchdict['cafe_id'])
    if 'date' in request.params:
        menu = menu.filter(Menu.date==request.params['date'])
    if 'time' in request.params:
        menu = menu.filter(Menu.time_sort_key==int(request.params['time']))
    menu = menu.first()

    #if not, create one
    if menu is None:
        # verify date
        date = request.params['date']
        if date is '0000-00-00':
            return HTTPFound(location= request.route_url('edit_menus_today'))
        menu = Menu(cafe_id=int(m['cafe_id']), name='', date=request.params['date'], time_sort_key=request.params['time'], menus='', sent=False)
        DBSession.add(menu)
        DBSession.flush()
        DBSession.refresh(menu)
    url = request.route_url('edit_menu', cafe_id=int(m['cafe_id']), menu_id=menu.id, allergen_list=ALLERGENS, healthy_factor=HEALTHY_FACTOR)
    update_gcalendar(menu)

    return HTTPFound(location=url)

# create a menu item
@view_config(route_name='create_menu_item', renderer='templates/edit_menu.jinja2')
def create_menu_item(request):
    #create the new menu item entry
    new_menu_item = MenuItem(name=request.params['name'].encode('utf8'), description=request.params['description'].encode('utf8'), menu_id=request.matchdict['menu_id'], healthy=int(request.params['healthy']))
    DBSession.add(new_menu_item)
    DBSession.flush()
    DBSession.refresh(new_menu_item)

    #create corresponding allergens
    for allergen in ALLERGENS:
        if allergen in request.params:
            new_allergen = Allergen(menu_item_id=new_menu_item.id, allergen = allergen)
            DBSession.add(new_allergen)

    #find the corresponding menu
    menuQuery = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    menu = menuQuery.one()
    menu_items = menu.menus

    #update the menu items on the menu
    if len(menu_items) > 0:     #just append
        menu_items = menu_items.split(' ')
        menu_items = map(int, menu_items)
        menu_items.append(int(new_menu_item.id))
    else: #create the first one
        menu_items = [int(new_menu_item.id)]

    menu_items_string = ' '.join(str(menu_item_id) for menu_item_id in menu_items)
    menu.menus = menu_items_string
    menuQuery.update({"menus":menu_items_string}, synchronize_session=False)
    #update menu name if needed
    first_menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_items[0]).one()
    #if we just inserted the first item in the menu, update the menu name with the first item name
    if first_menu_item.id == new_menu_item.id:
        menuQuery.update({"name":first_menu_item.name})
    #update google calendar
    update_gcalendar(menu)

    url = request.route_url('edit_menu', cafe_id=int(request.matchdict['cafe_id']), menu_id=request.matchdict['menu_id'])
    return HTTPFound(location=url)

# set the menus string to be the new order
@view_config(route_name='update_menu_order', renderer='string')
def update_menu_order(request):
    menu_query = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    if "menu_ids" in request.params:
        new_order = request.params['menu_ids'].split(',')
        new_order = ' '.join(str(i) for i in new_order)
        menu_query.update({"menus":new_order})

    update_gcalendar(menu_query.one())

    return "ok"

# updating the menu name
@view_config(route_name='update_menu_name', renderer='json')
def update_menu_name(request):
    menu_query = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    new_name = urllib.unquote(request.json_body)
    menu_query.update({"name":new_name.encode('utf8')})
    update_gcalendar(menu_query.one())

    return json.dumps(menu_query.one().name.decode('utf8'))

@view_config(route_name='delete_picture', renderer='json')
def delete_picture(request):
    menu_query = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    images_id = menu_query.one().images_id
    images_id = images_id.split(' ') if images_id else []

    if "data" in request.params:
        thumb_url = json.loads(request.params["data"])
        image = DBSession.query(Image).filter(Image.thumb_url==thumb_url).filter(Image.id.in_(images_id)).one()
        images_id.remove(str(image.id))
        images_id = ' '.join([str(i) for i in images_id])
        menu_query.update({"images_id": images_id}, synchronize_session=False)
        DBSession.delete(image)
        return thumb_url

@view_config(route_name='attach_pictures', renderer='json')
def attach_pictures(request):
    menu_query = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    images_id = menu_query.one().images_id
    images_id = images_id.split(' ') if images_id else []
    if images_id:
        images = DBSession.query(Image).filter(Image.id.in_(images_id)).all()
    added_thumbs = []
    if "data" in request.params:
        data = json.loads(request.params["data"])
        for image_info in data:
            image, thumb = image_info
            if not image or not thumb:
                continue
            ext = os.path.splitext(image)[-1].lower()
            if ext in (".jpg", ".jpeg", ".png"):
                new_image = Image(image_url=image, thumb_url=thumb)
                added_thumbs.append(thumb)
                DBSession.add(new_image)
                DBSession.flush()
                DBSession.refresh(new_image)
                images_id.append(new_image.id)
        menu_query.update({
                "images_id": ' '.join([str(i) for i in images_id]),
                })
    return json.dumps(added_thumbs)

#deleting a menu item
@view_config(route_name='delete_menu_item', renderer='string')
def delete_menu_item(request):
    menu_item_id = request.matchdict['menu_id']
    menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
    menuQuery = DBSession.query(Menu).filter(Menu.id==menu_item.menu_id)
    menu = menuQuery.one()

    #build the new list of menu ids
    menu_ids = menu.menus.split(' ')
    menu_ids = map(int, menu_ids)
    menu_ids.remove(int(request.matchdict['menu_id']))
    menu_id_string = ' '.join(str(menu_id) for menu_id in menu_ids)
    menu.menus = menu_id_string
    menuQuery.update({"menus":menu_id_string}, synchronize_session=False)

    #delete the menu item
    DBSession.delete(menu_item)

    #update allergens table
    allergens = DBSession.query(Allergen).filter(Allergen.menu_item_id==request.matchdict['menu_id'])
    for allergen in allergens:
        DBSession.delete(allergen)

    update_gcalendar(menu)
    return menu_item_id

#updating the menu item name
@view_config(route_name='update_menu_item_name', renderer='json')
def update_menu_item_name(request):
    menu_item_query = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menu_item_id'])
    menu_item = menu_item_query.one()
    old_name = menu_item.name
    new_name = urllib.unquote(request.json_body)
    menu_item_query.update({"name":new_name.encode('utf8')})
    #update the menu name if the menu item is the first menu item, the menu name is the same as the old menu item name or there's no menu name
    menu_query = DBSession.query(Menu).filter(Menu.id==menu_item.menu_id)
    menu = menu_query.one()

    if int(menu.menus.split(' ')[0]) == menu_item.id:
        if not menu.name or old_name == menu.name:
            menu_query.update({"name":new_name.encode('utf8')})
    update_gcalendar(menu)
    #update the menu title with the new name
    return json.dumps(menu.name.decode('utf8'))

#updating the menu item description
@view_config(route_name='update_menu_item_desc', renderer='string')
def update_menu_item_desc(request):
    menu_item_id = request.matchdict['menu_item_id']
    menuItem = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id)
    new_desc = urllib.unquote(request.json_body).encode('utf8')
    menuItem.update({"description":new_desc})
    menu = DBSession.query(Menu).filter(Menu.id==menuItem.one().menu_id).one()
    update_gcalendar(menu)
    return 'ok'

@view_config(route_name='update_menu_item_allergen', renderer='string')
def update_menu_item_allergen(request):
    menu_item_query = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menu_item_id'])
    allergen_to_add = request.params.get('menu_item_allergen_on', None)
    allergen_to_remove = request.params.get('menu_item_allergen_off', None)
    if allergen_to_add:
        #create a new allergen for the allergen that's turned on
        new_allergen = Allergen(menu_item_id=request.matchdict['menu_item_id'], allergen = allergen_to_add)
        DBSession.add(new_allergen)
    elif allergen_to_remove:
        #delete the allergen that was turned off
        allergen_to_remove = DBSession.query(Allergen).filter(Allergen.menu_item_id==request.matchdict['menu_item_id']).filter(Allergen.allergen==allergen_to_remove).one()
        DBSession.delete(allergen_to_remove)
    menu = DBSession.query(Menu).filter(Menu.id==menu_item_query.one().menu_id).one()
    update_gcalendar(menu)
    return 'ok'

# update menu item healthiness
@view_config(route_name='update_menu_item_healthy', renderer='string')
def update_menu_item_healthy(request):
    menuItem = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menu_item_id'])
    menuItem.update({"healthy":int(request.params['healthy'])})
    return 'ok'

def get_daily_menu(cafe_id):
#find the menu to display
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    # for testing
    # before = now - timedelta(days = 1)
    # yesterday = before.strftime('%Y-%m-%d')
    # today = yesterday
    # today = datetime.date(2012, 11, 3)
    meal_filter = 1
    if now.hour < BREAKFAST_END_HOUR:
        meal_filter = 1
    elif BREAKFAST_END_HOUR <= now.hour < LUNCH_END_HOUR:
        meal_filter = 2
    else:
        meal_filter = 3

    menu = DBSession.query(Menu).filter(Menu.cafe_id == cafe_id, Menu.date >= today, Menu.time_sort_key >= meal_filter).order_by(Menu.date).order_by(Menu.time_sort_key).first()
    # if there isn't a correspondong menu, display the newest one
    if menu is None:
        menu = DBSession.query(Menu).filter(Menu.cafe_id == cafe_id).order_by(-Menu.date).order_by(-Menu.time_sort_key).first()
    if menu is None:
        return None
    return menu

#for displaying the daily menu on big screen with ken burn effect
@view_config(route_name='screen', renderer='templates/kenburn_daily.jinja2')
def screen(request):
    cafe_id = int(request.matchdict['cafe_id'])
    menu = get_daily_menu(cafe_id)
    if menu.images_id:
        images_id = menu.images_id.split(' ')
        images = DBSession.query(Image).filter(Image.id.in_(images_id)).all()
        file_paths = [image.image_url for image in images]
        return dict(images=file_paths)
    return dict()

#for displaying the daily menu
@view_config(route_name='daily_menu', renderer='templates/daily_menu.jinja2')
def daily_menu(request):
    cafe_id = int(request.matchdict['cafe_id'])
    menu = get_daily_menu(cafe_id)
    if menu:
        return refresh_menu(menu)
    else:
        return dict()

# daily menu api
@view_config(route_name='daily_menu_json', renderer="jsonp")
def daily_menu_json(request):
    menu = get_daily_menu()
    if menu:
        return get_menu_json(menu)
    else:
        return ''

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MenuProject_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

