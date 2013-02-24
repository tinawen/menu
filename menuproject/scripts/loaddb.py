import os
import sys
import transaction
import pickle
from sqlalchemy.ext.serializer import loads

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..gcalendar import delete_all
from ..gcalendar import update_menu_on_google_calendar

from ..models import (
    DBSession,
    MenuItem,
    Menu,
    Allergen,
    Base,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
#    delete_all()
    with transaction.manager:
        f = open("./db_backup.txt", 'r');
        serialized_data = pickle.load(f)
        serialized_menu_items = serialized_data["menu_items"]
        menu_items = loads(serialized_menu_items, Base.metadata, DBSession)
        print menu_items
        print "hello"
        for menu_item in menu_items:
            DBSession.merge(menu_item)
            print 'menu_item is %r'%menu_item
        print "hello done"
        serialized_allergens = serialized_data["allergens"]
        allergens = loads(serialized_allergens, Base.metadata, DBSession)
        for allergen in allergens:
            DBSession.merge(allergen)
        serialized_menus = serialized_data["menus"]
        menus = loads(serialized_menus, Base.metadata, DBSession)
        for menu in menus:
            DBSession.merge(menu)
 #           update_menu_on_google_calendar(menu.id)



