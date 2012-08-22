import os
import sys
import transaction
import pickle

from sqlalchemy import engine_from_config

from sqlalchemy.ext.serializer import dumps

from pyramid.paster import (
    get_appsettings,
    )

from ..models import (
    DBSession,
    MenuItem,
    Menu,
    Allergen,
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
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    menu_items = DBSession.query(MenuItem)
    serialized_menu_items = dumps(menu_items.all())
    menus = DBSession.query(Menu)
    serialized_menus = dumps(menus.all()) 
    allergens = DBSession.query(Allergen)
    serialized_allergens = dumps(allergens.all())
    serialized_data = {"menus" : serialized_menus,
                       "menu_items" : serialized_menu_items,
                       "allergens" : serialized_allergens}
    file = open('./db_backup.txt', 'w+')
    pickle.dump(serialized_data, file)




