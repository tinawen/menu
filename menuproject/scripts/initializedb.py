import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

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
    with transaction.manager:
        name = 'Amuse bouche'
        description = 'Asian style Ahi tuna tartar with crispy gyoza wrap'
        menuitem = MenuItem(name=name, description=description, menu_id=1)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Eggplant 'caviar'", description='', menu_id=1)
        DBSession.add(menuitem) 
        name = 'Melo-melo of red and white gazpacho soup'
        description = 'with confetti of bell peppers and cucumbers'
        menuitem = MenuItem(name=name, description=description, menu_id=1)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Dairy")
        DBSession.add(allergen)
        name = 'Baby assorted lettuces drizzled with mustardy vinaigrette'
        description = 'Roasted baby beets, fire-roasted cippolini onions, \nFava beans and extra virgin croutons'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name='Crispy skin Loche Duart salmon medallions', description='Miso glazed spinach and roasted garlic, wasabi mashed potatoes', menu_id=1) 
        DBSession.add(menuitem) 
        name = 'Baked European eggplant with garlicky yogurt'
        description = 'House-made apricot ham, dill and fig puree'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Dairy")
        DBSession.add(allergen)
        name = 'Beer butt roasted chicken'
        description = 'Pureed celeriac, parsnips and truffles, \nGrilled spring onions, and asparagus'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name=='Amuse bouche', MenuItem.description=='Asian style Ahi tuna tartar with crispy gyoza wrap', MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Barley risotto with wild mushrooms and artichokes'
        description = 'Scallions and cherry confit tomatoes'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name=='Amuse bouche', MenuItem.description=='Asian style Ahi tuna tartar with crispy gyoza wrap', MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Melon and tarragon soup'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==1).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Pizza and Cactus Cooler', date='2012-7-10', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        name = 'Roasted studded garlic pork loin'
        description = 'glazed with garlic confit and Heirloom tomatoes, \nbuttermilk mashed potatoes, \nsteamed summer vegetables'
        menuitem = MenuItem(name=name, description=description, menu_id=2)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Panko crusted crab cakes'
        description = 'Lime mayonnaise carrot, cabbage slaw, \nLemon aioli'
        menuitem = MenuItem(name=name, description=description, menu_id=2)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Seafood")
        DBSession.add(allergen)
        name = 'Black bean, mango, quinoa salad'
        description = 'Assorted baby lettuces, \nMustardy vinaigrette'
        menuitem = MenuItem(name=name, description=description, menu_id=2)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Crispy bareley rissotto and vegetable wedges'
        description = 'Chickpea gravy, \nFire-roasted wild mushroom'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Kori Gassi'
        description = 'Mogolian chicken curry'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Tarka Daal'
        description = 'Yellow lentils'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Aloo Gobi'
        description = 'Potato and cauliflower'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Basmati steamed rice and garlic naan'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Tamarine and mint chutney'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==2).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Shalimar and Gummy Bears', date='2012-7-11', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

