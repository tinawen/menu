#!/usr/bin/env python

import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from datetime import date
import datetime
import json
import smtplib
from gcalendar import get_menu_name
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
)

from models import (
    DBSession,
    Menu,
    MenuItem,
    Allergen,
    Cafe,
    )

MAIL_SECRETS = '/home/tina/mail_secrets.json'
HEALTH_COLORS = ['green', 'orange', 'red']
BREAKFAST_LUNCH_CUTOFF_HOUR = 10
LUNCH_DINNER_CUTOFF_HOUR = 14

if __name__ == '__main__':
    config_uri = "/home/tina/MenuProject/production.ini"
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d') 

#figure out which meal this is for
meal_filter = 1
if now.hour < BREAKFAST_LUNCH_CUTOFF_HOUR:
    meal_filter = 1
elif BREAKFAST_LUNCH_CUTOFF_HOUR <= now.hour < LUNCH_DINNER_CUTOFF_HOUR:
    meal_filter = 2
else:
    meal_filter = 3

menu_query = DBSession.query(Menu).filter(Menu.date==today).filter(Menu.time_sort_key==meal_filter)
if len(menu_query.all()) > 0:
    desc = "<div>"
    for menu in menu_query.all():
        if not menu.sent:
            cafe_name = DBSession.query(Cafe).filter(Cafe.id==menu.cafe_id).one().name
            desc = desc + "<div style='display:block; text-align:center; font-size:17px;font-weight:bold;'>"+cafe_name.decode('utf8') + '</div>'
            if len(menu.menus) >= 1:
                for menu_item_id in menu.menus.split(' '):
                    menu_item = DBSession.query(MenuItem).filter(MenuItem.id==menu_item_id).one()
                    allergens = DBSession.query(Allergen).filter(Allergen.menu_item_id==menu_item.id).all()
                    allergen_string = ', '.join([a.allergen for a in allergens])
                    if menu_item.healthy:
                        desc = desc + "<div style='display: block; text-align:center; font-size:15px; font-weight:bold; color:" + HEALTH_COLORS[menu_item.healthy-1] + "'>" + "&hearts; " + "<font color=black>" + menu_item.name.decode('utf8') + '</font></div>'
                    else:
                        desc = desc + "<div style='display: block; text-align:center; font-size:15px; font-weight:bold;'>" + menu_item.name.decode('utf8') + '</div>'

                    if len(menu_item.description.decode('utf8')):
                        desc = desc + "<div style='display: block; font-size:13px; text-align:center'>"
                        desc = desc + menu_item.description.decode('utf8')
                        desc = desc + '</div>'
                    if len(allergen_string):
                        desc = desc + "<div style='display: block; font-size:11px; text-align:center'>"
                        desc = desc + '(' + allergen_string + ')'
                        desc = desc + '</div>'
                    desc = desc + '</div><br>\n'
        desc = desc + '<br>\n'

    json_data = open(MAIL_SECRETS)
    data = json.load(json_data)
    json_data.close()
    msg = MIMEMultipart()

    msg['From'] = data["sender"]
    msg['To'] = data["recipient"]
    msg['Subject'] = get_menu_name(menu).decode('utf8')
    html_part1 = """
<html>
  <head></head>
  <body>
  <style>
  * {font-family: Opensans, helvetica, sans-serif;
       font-size: 15px;
  }
</style>
<div style="display:block; font-size:17;text-align:center">
    Today Tuckshop is serving:
</div><br>
     """
    html_part2 ="""
<div style="display:block; font-size:15; text-align:center">
View the menu on <a href="http://food.corp.dropbox.com/
"""
    html_part3 = """
">food</a>
</div>
  </body>
</html>
"""
    html = html_part1 + desc.encode('utf8') + html_part2 + str(menu.cafe_id) + """/menu/""" + str(menu.id) + html_part3
    print "sending email:"
    print html
    msg_part  = MIMEText(html, 'html')
    msg.attach(msg_part)

    s = smtplib.SMTP()
    s.connect()
    s.sendmail(data["sender"], data["recipient"], msg.as_string())
    s.close()
    menu_query.update({"sent":True}, synchronize_session=False)






