from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from datetime import date
import datetime
import time
import json
import urllib
import calendar
import operator
from gcalendar import get_menu_name
from gcalendar import get_menu_desc
from gcalendar import update_menu_on_google_calendar
from datetime import timedelta
from sqlalchemy import distinct
from sqlalchemy import extract
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from models import (
    DBSession,
    MenuItem,
    Menu,
    Allergen,
    )

MAIL_SECRETS = '/home/tina/mail_secrets.json'

def refresh_menu(menu_id):
    menu = DBSession.query(Menu).filter(Menu.id==menu_id).one()
    menu_items = DBSession.query(MenuItem).filter(MenuItem.menu_id==menu.id).all()
    allergens = []
    for menu_item in menu_items:
        allergen_array = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
        allergens.append([a.allergen for a in allergen_array])
    return dict(menu_items=menu_items, allergens=allergens, menu=menu)

@view_config(route_name='publish', renderer='string')
def publish(request):
    menuQuery = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    menu = menuQuery.one()
    if not menu.sent:
        mailer = get_mailer(request)
        json_data = open(MAIL_SECRETS)
        data = json.load(json_data)
        json_data.close()

        message = Message(subject=get_menu_name(menu),
                          sender=data["sender"],
                          recipients=[data["recipient"]],
                          body=get_menu_desc(menu, False))
        print 'trying to send email to %r' % data["recipient"]
        mailer.send_immediately(message, fail_silently=False)
        menuQuery.update({"sent":True}, synchronize_session=False)
    return json.dumps("Sent")    

def migrate(request):
    menu_items = DBSession.query(MenuItem).all()
    for menu_item in menu_items:
        if len(menu_item.restriction):
            allergens = menu_item.restriction.strip().split(' ') 
        else:
            allergens = []
        for allergen in allergens:
            if allergen != 'Seafood':
                allergen_item = Allergen(menu_item_id=menu_item.id, allergen = allergen.strip())
                DBSession.add(allergen_item)
    return {'content':'migration done'}

@view_config(route_name='view_menus_init', renderer='templates/view_menus.jinja2')
def view_menus_init(request):
    return view_menus(request)

def convert_to_month_string (month, year):
    return str(calendar.month_name[month]) + ' ' + str(year)
   
def build_months_dict():
    today = datetime.datetime.now()
    new_year = int(today.strftime("%Y"))
    
    new_month = int(today.strftime("%m"))
    months_dict = {}
    distinct_months = DBSession.query(extract('month', Menu.date), extract('year', Menu.date)).distinct().all()
    months_dict[int(new_month), int(new_year)] = convert_to_month_string(new_month, new_year)
    for distinct_month in distinct_months:
        months_dict[int(distinct_month[0]), int(distinct_month[1])] = convert_to_month_string(int(distinct_month[0]), int(distinct_month[1]))
    return months_dict

def build_months_menu():
    months_dict = build_months_dict()
    sorted_months = sorted(months_dict.iteritems(), key=operator.itemgetter(0))
    sorted_months = [y for x, y in sorted_months]
    return sorted_months

@view_config(route_name='view_menus', renderer='templates/view_menus.jinja2')
def view_menus(request):
    today = datetime.datetime.now()
    year = today.strftime("%Y")
    
    new_month = int(today.strftime("%m"))
    new_year = year
    sorted_months = build_months_menu()
    print 'sorted month is: ', sorted_months
    if 'menu_month' in request.matchdict:
        print 'index is ', int(request.matchdict['menu_month'])
        month_string = sorted_months[int(request.matchdict['menu_month'])]
        months_dict = build_months_dict()
        for key, value in months_dict.iteritems():
            if value == month_string:
                new_month = key[0]
                new_year = key[1]

    print 'new_month is %r'%new_month
    print 'new_year is %r'%new_year
    start_date = datetime.datetime(int(new_year), int(new_month), 1)
    end_date = datetime.datetime(int(new_year), int(new_month)+1, 1)
    week_starts = []
    weekly_menus = []
    week_end = end_date
    while True:
        week_start = week_end-timedelta(days=week_end.isoweekday())
        week_end = week_end-timedelta(days=week_end.isoweekday()-7)
        if week_start < start_date:
            week_start = start_date
        if week_end > end_date:
            week_end = end_date
        menus = DBSession.query(Menu).filter(Menu.date >= week_start.strftime('%Y-%m-%d')).filter(Menu.date < week_end.strftime('%Y-%m-%d')).order_by(-Menu.date).order_by(-Menu.time_sort_key).all()
        if len(menus):
            week_starts.append(week_start.strftime("%m/%d/%y"))
            weekly_menus.append(menus)
        week_end = week_end-timedelta(days=7)
        if week_start <= start_date:
            break

        month_string = convert_to_month_string(int(new_month), int(new_year))
        print 'new month is ', month_string

        month = sorted_months.index(month_string)
        print 'month is ', month
    return dict(menus=weekly_menus, week_starts = week_starts, selected_month=month_string, months=sorted_months)

@view_config(route_name='edit_menu', renderer='templates/edit_menu.jinja2')
def edit_menu(request):
    menu = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id']).one()
    menu_items = []
    allergens = []
    if len(menu.menus):
        for menu_item_id in menu.menus.split(' '):
            menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
            allergen_array = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
            menu_items.append(menu_item)
            allergens.append([a.allergen for a in allergen_array])
    return dict(menu_items=menu_items, allergens=allergens, menu=menu)

@view_config(route_name='edit_menus', renderer='templates/edit_menus.jinja2')
def edit_menus(request):
    return view_menus(request)

@view_config(route_name='edit_menus_init', renderer='templates/edit_menus.jinja2')
def edit_menus_init(request):
    return edit_menus(request)

@view_config(route_name='create_menu_item', renderer='templates/edit_menu.jinja2')
def create_menu_item(request):
    new_menu_item = MenuItem(name=request.params['name'].encode('utf8'), description=request.params['description'].encode('utf8'), menu_id=request.matchdict['menu_id'], healthy=int(request.params['healthy']))
    DBSession.add(new_menu_item)
    print 'adding menu_item, desc is %r' % request.params['description'].encode('utf8')
    menu_item = DBSession.query(MenuItem).filter(MenuItem.name==request.params['name'].encode('utf8')).filter(MenuItem.description==request.params['description'].encode('utf8')).filter(MenuItem.menu_id==request.matchdict['menu_id']).filter(MenuItem.healthy==request.params['healthy']).one()
    allergens = ["Shellfish", "Nuts", "Dairy", "Spicy", "Vegan", "Gluten-free", "Alcohol"]
    for allergen in allergens:
        if allergen in request.params:
            new_allergen = Allergen(menu_item_id=menu_item.id, allergen = allergen)
            DBSession.add(new_allergen)

    menuQuery = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    menu = menuQuery.one()
    new_menuids = menu.menus

    if len(new_menuids) > 0:
        new_menuids = new_menuids.split(' ')
        new_menuids = map(int, new_menuids)
        new_menuids.append(int(new_menu_item.id))
    else:
        new_menuids = [int(new_menu_item.id)]
    
    menuidstring = ' '.join(str(new_menuid) for new_menuid in new_menuids)
    menu.menus = menuidstring
    menuQuery.update({"menus":menuidstring}, synchronize_session=False)
    first_menu_item = DBSession.query(MenuItem).filter(MenuItem.id==new_menuids[0]).one()
    if first_menu_item.id == menu_item.id:
        menuQuery.update({"name":first_menu_item.name})
    
    update_menu_on_google_calendar(menu)
    url = request.route_url('edit_menu', menu_id=request.matchdict['menu_id'])
    return HTTPFound(location=url)

@view_config(route_name='delete_menu_item', renderer='templates/edit_menu.jinja2')
def delete_menu_item(request):
    menu_item = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menu_id']).one()
    menuQuery = DBSession.query(Menu).filter(Menu.id==menu_item.menu_id)
    menu = menuQuery.one()

    new_menuids = menu.menus.split(' ')
    new_menuids = map(int, new_menuids)
    new_menuids.remove(int(request.matchdict['menu_id']))
    
    menuidstring = ' '.join(str(new_menuid) for new_menuid in new_menuids)
    menu.menus = menuidstring
    menuQuery.update({"menus":menuidstring}, synchronize_session=False)
    DBSession.delete(menu_item)

    allergens = DBSession.query(Allergen).filter(Allergen.menu_item_id==request.matchdict['menu_id'])
    for allergen in allergens:
        DBSession.delete(allergen)
    url = request.route_url('edit_menu', menu_id=menu.id)
    update_menu_on_google_calendar(menu)
    return HTTPFound(location=url)

@view_config(route_name='update_menu_item_name', renderer='json')
def update_menu_item_name(request):
    print 'updating menu item name'
    menuItem = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menuItem_id'])
    old_name = menuItem.one().name
    new_name = urllib.unquote(request.json_body)
    menuItem.update({"name":new_name.encode('utf8')})
    menuQuery = DBSession.query(Menu).filter(Menu.id==menuItem.one().menu_id)
    menu = menuQuery.one()
    if int(menu.menus.split(' ')[0]) == menuItem.one().id:
        if len(menu.name) == 0 or old_name == menu.name:
            menuQuery.update({"name":new_name.encode('utf8')})
            old_name = new_name.encode('utf8')
    update_menu_on_google_calendar(menu)
    return json.dumps(old_name.decode('utf8'))

@view_config(route_name='update_menu_item_desc', renderer='templates/edit_menu.jinja2')
def update_menu_item_desc(request):
    print 'updating menu item desc'
    menu_item_id = request.matchdict['menuItem_id']
    menuItem = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id)
    new_desc = urllib.unquote(request.json_body).encode('utf8') 
    print 'new_desc is %r' % new_desc
    menuItem.update({"description":new_desc})
    menu = DBSession.query(Menu).filter(Menu.id==menuItem.one().menu_id).one()
    update_menu_on_google_calendar(menu)
    return refresh_menu(menuItem.one().menu_id)

@view_config(route_name='update_menu_item_allergen', renderer='templates/edit_menu.jinja2')
def update_menu_item_allergen(request):
    print 'updating menu item allergen'
    menuItem = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menuItem_id'])
    if "menuItemAllergenOn" in request.params:
        allergen = str(request.params['menuItemAllergenOn'])
        print 'allergen turning on is %r' % allergen
        new_allergen = Allergen(menu_item_id=request.matchdict['menuItem_id'], allergen = allergen)
        DBSession.add(new_allergen)
    elif "menuItemAllergenOff" in request.params:
        allergen = str(request.params['menuItemAllergenOff'])
        print 'allergen turning off is %r' % allergen
        allergens_to_remove = DBSession.query(Allergen).filter(Allergen.menu_item_id==request.matchdict['menuItem_id']).filter(Allergen.allergen==allergen)
        for allergen_to_remove in allergens_to_remove:
            DBSession.delete(allergen_to_remove)

    menu = DBSession.query(Menu).filter(Menu.id==menuItem.one().menu_id).one()     
    menu_items = DBSession.query(MenuItem).filter(MenuItem.menu_id==menu.id).all()
    allergens = []
    for menu_item in menu_items:
        allergen_array = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
        allergens.append([a.allergen for a in allergen_array])
    update_menu_on_google_calendar(menu)
    return dict(menu_items=menu_items, allergens=allergens, menu=menu)


@view_config(route_name='update_menu_item_healthy', renderer='json')
def update_menu_item_healthy(request):
    menuItem = DBSession.query(MenuItem).filter(MenuItem.id==request.matchdict['menuItem_id'])
    menuItem.update({"healthy":int(request.params['healthy'])})
    return dict()

@view_config(route_name='update_menus', renderer='templates/edit_menu.jinja2')
def update_menus(request):
    menu = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    if "menuIds" in request.params:
        new_order = request.params['menuIds'].split(',')
        new_order = ' '.join(str(i) for i in new_order)
        menu.update({"menus":new_order})
    update_menu_on_google_calendar(menu.one())
    return edit_menu(request)

@view_config(route_name='update_menus_name', renderer='templates/edit_menu.jinja2')
def update_menus_name(request):
    print 'update menu name is called'
    menu = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id'])
    new_name = urllib.unquote(request.json_body)
    menu.update({"name":new_name.encode('utf8')})
    update_menu_on_google_calendar(menu.one())
    return edit_menu(request)

@view_config(route_name='create_menu', renderer='templates/view_menus.jinja2')
def create_menu(request):
    menu = DBSession.query(Menu).filter(Menu.date==request.params['date']).filter(Menu.time_sort_key==int(request.params['time'])).first()
    if menu is None:
        menu = Menu(name='', date=request.params['date'], time_sort_key=request.params['time'], menus='', sent=False)
        DBSession.add(menu)
        menu = DBSession.query(Menu).filter(Menu.name=='').filter(Menu.date==request.params['date']).filter(Menu.time_sort_key==request.params['time']).one()
    url = request.route_url('edit_menu', menu_id=menu.id)
    update_menu_on_google_calendar(menu)

    return HTTPFound(location=url)

@view_config(route_name='daily_menu', renderer='templates/daily_menu.jinja2')
def daily_menu(request):
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
   # before = now - timedelta(days = 1)
  #  yesterday = before.strftime('%Y-%m-%d')
 #   today = yesterday
    meal_filter = 1
    if now.hour < 9:
        meal_filter = 1
    elif 9 <= now.hour < 15:
        meal_filter = 2
    else:
        meal_filter = 3
    menu = DBSession.query(Menu).filter(Menu.date >= today).filter(Menu.time_sort_key >= meal_filter).order_by(Menu.date).order_by(Menu.time_sort_key).first()
    if menu is None:
        menu = DBSession.query(Menu).order_by(-Menu.date).order_by(-Menu.time_sort_key).first()
    if menu is None:
        return dict()
    menu_items = []
    allergens = []
    if len(menu.menus):
        for menu_item_id in menu.menus.split(' '):
            menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
            allergen_array = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
            menu_items.append(menu_item)
            allergens.append([a.allergen for a in allergen_array])
    return dict(menu_items=menu_items, allergens=allergens, menu=menu)

@view_config(route_name='view_menu', renderer='templates/view_menu.jinja2')
def view_menu(request):
    menu = DBSession.query(Menu).filter(Menu.id==request.matchdict['menu_id']).one()
    menu_items = []
    allergens = []
    if len(menu.menus):
        for menu_item_id in menu.menus.split(' '):
            menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
            allergen_array = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
            menu_items.append(menu_item)
            allergens.append([a.allergen for a in allergen_array])
    print 'allergens are %r' % allergens
    return dict(menu_items=menu_items, allergens=allergens, menu=menu)


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

