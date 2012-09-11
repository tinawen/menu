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
from gcalendar import get_menu_desc
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
)

from models import (
    DBSession,
    Menu,
    )

MAIL_SECRETS = '/home/tina/mail_secrets.json'

config_uri = "/home/tina/MenuProject/development.ini"
settings = get_appsettings(config_uri)
engine = engine_from_config(settings, 'sqlalchemy.')
DBSession.configure(bind=engine)

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
meal_filter = 1
if now.hour < 10:
    meal_filter = 1
elif 10 <= now.hour < 14:
    meal_filter = 2
else:
    meal_filter = 3

menu_query = DBSession.query(Menu).filter(Menu.date == today).filter(Menu.time_sort_key == meal_filter)
if len(menu_query.all()) == 1:
    menu = menu_query.one()
    if not menu.sent:
        print "sending email"
        json_data = open(MAIL_SECRETS)
        data = json.load(json_data)
        json_data.close()
    
        msg = MIMEMultipart()

        msg['From'] = data["sender"]
        msg['To'] = data["recipient"]
        msg['Subject'] = get_menu_name(menu)
        msg.attach(MIMEText(get_menu_desc(menu, False)))
        
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(data["sender"], "rianisawesome")
        mailServer.sendmail(data["sender"], [data["recipient"]], msg.as_string())
        mailServer.close()
        menu_query.update({"sent":True}, synchronize_session=False)


    


