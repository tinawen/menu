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
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = 'Baby assorted lettuces drizzled with mustardy vinaigrette'
        description = 'Roasted baby beets, fire-roasted cippolini onions, \nFava beans and extra virgin croutons'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name='Crispy skin Loche Duart salmon medallions', description='Miso glazed spinach and roasted garlic, wasabi mashed potatoes', menu_id=1) 
        DBSession.add(menuitem) 
        name = 'Baked European eggplant with garlicky yogurt'
        description = 'House-made apricot ham, dill and fig puree'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = 'Beer butt roasted chicken'
        description = 'Pureed celeriac, parsnips and truffles, \nGrilled spring onions, and asparagus'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name=='Amuse bouche', MenuItem.description=='Asian style Ahi tuna tartar with crispy gyoza wrap', MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Barley risotto with wild mushrooms and artichokes'
        description = 'Scallions and cherry confit tomatoes'
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name=='Amuse bouche', MenuItem.description=='Asian style Ahi tuna tartar with crispy gyoza wrap', MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Melon and tarragon soup'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=1) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==1).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
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
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Panko crusted crab cakes'
        description = 'Lime mayonnaise carrot, cabbage slaw, \nLemon aioli'
        menuitem = MenuItem(name=name, description=description, menu_id=2)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        name = 'Black bean, mango, quinoa salad'
        description = 'Assorted baby lettuces, \nMustardy vinaigrette'
        menuitem = MenuItem(name=name, description=description, menu_id=2)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Crispy bareley rissotto and vegetable wedges'
        description = 'Chickpea gravy, \nFire-roasted wild mushroom'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Kori Gassi'
        description = 'Mogolian chicken curry'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Tarka Daal'
        description = 'Yellow lentils'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Aloo Gobi'
        description = 'Potato and cauliflower'
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Basmati steamed rice and garlic naan'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Tamarine and mint chutney'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=2) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==2).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==2).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Shalimar and Gummy Bears', date='2012-7-11', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        menuitem = MenuItem(name='Crispy-skin Magret of duck', description='Ragout of black and white beans, \nSauteed padrons in olive oil', menu_id=3)
        DBSession.add(menuitem) 
        name = 'Porcini dusted Alaskian halibut'
        description = 'Succotash with Laughing bird shrimp, \nGrilled Summer zuchinni'
        menuitem = MenuItem(name=name, description=description, menu_id=3)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==3).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        name = 'Aloo Tikka Chaat'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=3)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==3).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Chole'
        description = 'Indian potato patties served with garbanzo beans, tomato and onion gravy'
        menuitem = MenuItem(name=name, description=description, menu_id=3) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==3).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = 'Spanish chilled tomato soup'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=3) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==3).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Quinoa crusted marinated tofu'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=3) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==3).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = 'Trio plate of white gazpachio, hearts of baby lettuces, roasted jumbo asparagus with tahini dressing'
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=3) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==3).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==3).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name="The Hacker's Diet", date='2012-7-12', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        name = 'Sea salt crusted Loche Duarte Salmon'
        description = 'Extra virgin, Lemony hollandaise, \nSlow baked tomatoes, \nSalad frizze with mimosa dressing'
        menuitem = MenuItem(name=name, description=description, menu_id=4)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==4).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        menuitem = MenuItem(name='Mustard, herb, crusted rack of lamb', description='Virgin cherry tomato vinaigrette, \nRoasted marbled potatoes, \nGrilled asparagus', menu_id=4)
        DBSession.add(menuitem) 
        name = 'Confetti bean hash'
        description = 'Cilantro lime rice, \nAvocado cashew cream, \nPeach cortido'
        menuitem = MenuItem(name=name, description=description, menu_id=4)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==4).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Nuts")
        DBSession.add(allergen)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Salmon 'Desi dill wala'"
        description = 'Mixed vegetable sauted with fenugreek leafs, \nSteamed saffron basmati rice'
        menuitem = MenuItem(name=name, description=description, menu_id=4) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==4).one()
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==4).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Sea salt crusted Loche Duarte Salmon', date='2012-7-13', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        menuitem = MenuItem(name='Jalapeno, tequilla, cilantro roasted whole chicken', description='Sauteed Spring green vegetables, \nMexican potato hash cakes', menu_id=5)
        DBSession.add(menuitem) 
        name = 'Steamed littleneck clams and mussels'
        description = 'in white wine, fennel and onions'
        menuitem = MenuItem(name=name, description=description, menu_id=5)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==5).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Shellfish")
        DBSession.add(allergen)
        menuitem = MenuItem(name='Kolhapuri chicken', description='Maharastra', menu_id=5)
        DBSession.add(menuitem) 
        name = "Rice pilaf with cashews and green peas"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=5) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==5).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Okra Kadahi Bhindi"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=5) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==5).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Potato salad"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=5) 
        DBSession.add(menuitem)    
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==5).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Mint and Tamarind chutney"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=5) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==5).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==5).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Jalapeno, tequila, cilantro roasted whole chicken', date='2012-7-16', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        name = 'Crustacean mac n cheese'
        description = 'Grilled Brentwood corn'
        menuitem = MenuItem(name=name, description=description, menu_id=6)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==6).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = "Italian 'Osso Bucco' with Gremoulata"
        description = 'Creamy polenta, \nOven roasted Roma tomatoes with herbs'
        menuitem = MenuItem(name=name, description=description, menu_id=6)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==6).one()    
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = 'Koorgi pork ribs'
        description = 'Indian garlic potatoes, \nMatar mushroom paneer'
        menuitem = MenuItem(name=name, description=description, menu_id=6)
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==6).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = "Mango lassi"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=6) 
        DBSession.add(menuitem)
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==6).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Mint chutney"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=6) 
        DBSession.add(menuitem)        
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==6).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Chickpea picatta", description='Olive oil mashed potatoes, \nDressed arugula', menu_id=6) 
        DBSession.add(menuitem)       
        name = "Butterleaf lettuce with virgin tomato vinaigrette"
        description = 'Fire roasted squash, \nSnow peas and shaved raddishes'
        menuitem = MenuItem(name=name, description=description, menu_id=6) 
        DBSession.add(menuitem) 
        menu_item = DBSession.query(MenuItem).filter(MenuItem.name==name, MenuItem.description==description, MenuItem.menu_id==6).one()
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==6).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Crustacean mac n cheese', date='2012-7-17', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        name = 'Seared jumbo day-boat scallops'
        description = "Grilled Spanish 'Escalavida' summer vegetables, \nRaspberry vinegar demi drizzle"
        menuitem = MenuItem(name=name, description=description, menu_id=7)
        DBSession.add(menuitem)
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        name = "Chicken breasts 'Cordon Blue' stuffed with Swiss cheese and Black Forrest ham"
        description = "Basil marina tomato sauce, \n'Mama' confit of garlic mashed potatoes"
        menuitem = MenuItem(name=name, description=description, menu_id=7)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = "Tilak's lamb vindaloo"
        description = "aka 'ring of fire'"
        menuitem = MenuItem(name=name, description=description, menu_id=7)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = "Jeera rice"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        DBSession.add(menuitem)
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Paneer, matar, and mushrooms"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        DBSession.add(menuitem)  
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = "Grilled polenta triangles"
        description = 'Lemony cashew cream'
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Fire roasted chefs mixed mushrooms"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Nutmeg sauteed spinach"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        DBSession.add(menuitem)    
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Gigantes broad white beans and roasted corn"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=7) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==7).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Seared jumbo day-boat scallops', date='2012-7-18', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        name = 'Whole salmon and branzino studded and baked in banana leaves'
        description = 'Miso, genger dressing, \nWilted pea tendrils, \nGinger infused steamed brown rice'
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=8) 
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        name = "Classic Italian meat balls in tomato meat sauce"
        description = "'Al dente' fettuccini with extra virgin olive oil, \nParmesan garlic bread"
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Dairy")
        DBSession.add(allergen)
        name = 'West African peanut stew'
        description = 'Sweet potato, okra, cabbage, peanuts, and green bell peppers'
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Nuts")
        DBSession.add(allergen)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Forbidden rice"
        description = ''
        menuitem = MenuItem(name=name, description=description,  menu_id=8) 
        DBSession.add(menuitem)
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Tropical fruit salad with toasted coconut"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=8) 
        DBSession.add(menuitem)   
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Daneli"
        description = 'Mashed potatoes cooked with Dabeli marsala spice'
        menuitem = MenuItem(name=name, description=description,  menu_id=8) 
        DBSession.add(menuitem)  
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Spicy")
        DBSession.add(allergen)
        name = "Mango lassi"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=8) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=8)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Chicken tortilla soup", description='', menu_id=8) 
        DBSession.add(menuitem) 
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==8).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name='Whole salmon and branzino studded and baked in banana leaves', date='2012-7-19', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        name = "English fish 'n chips"
        description = 'Tartar sauce and malt vinegar'
        menuitem = MenuItem(name=name, description=description, menu_id=9)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=9)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Seafood")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Foie-gras sliders", description="Port wine caramelized onions, and baby spinach salad", menu_id=9)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name='China town soy braised chicken', description='The chickens are not actually from Chinatown, because it would be nasty', menu_id=9)
        DBSession.add(menuitem) 
        name = "Mao Ploy teamed vegetables"
        description = 'Veggies that have Chinese names'
        menuitem = MenuItem(name=name, description=description, menu_id=9) 
        DBSession.add(menuitem)
        menuitem = MenuItem(name=name, description=description, menu_id=9)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        name = "Steamed rice"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=9) 
        DBSession.add(menuitem)   
        menuitem = MenuItem(name=name, description=description, menu_id=9)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Chicken and brown rice soup", description='', menu_id=9) 
        DBSession.add(menuitem)        
        name = "Vegetarian vegetable soup"
        description = ''
        menuitem = MenuItem(name=name, description=description, menu_id=9) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=9)
        allergen = Allergen(menu_item_id=menu_item.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Tempeh and white bean cakes", description='If you like beans, you should get it', menu_id=9) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name="Mushroom pate on crostini", description='Yay mushroom!', menu_id=9) 
        DBSession.add(menuitem) 
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==9).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name="English fish 'n chips", date='2012-7-20', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)

        menuitem = MenuItem(name="Smoked salmon and smoked trout blinis", description='Buckwheat pancake tower filled with the above.\n Buckwheat flour, milk, yeast, egg whites, creme fraiche, chives, and lemon',  menu_id=10)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=10)
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Dairy")
        DBSession.add(allergen)
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Seafood")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Lambs lettuce tossed in extra virgin grapeseed oil", description="", menu_id=10)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=10)
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name='24 Hour roasted Heirloom tomato with sea-salt and herbs', description='', menu_id=10)
        DBSession.add(menuitem) 
        menuitem = MenuItem(name=name, description=description, menu_id=10)
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Chicken Katsu", description='If you been to Hawaii you know what we are talking about. Chicken breasts, flour, egg, panko breadcrumbs and rice bran oil', menu_id=10) 
        DBSession.add(menuitem)
        menuitem = MenuItem(name="Hawaiian pineapple slaw", description='Red cabbage, white cabbage, carrots, extra virgin olive oil mayonnaise, pineapple', menu_id=10) 
        DBSession.add(menuitem)      
        menuitem = MenuItem(name=name, description=description, menu_id=10)
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Vegan")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Hawaiian macaroni salad", description='Red vine vinegar, celery, carrots, kewpie mayonnaise', menu_id=10) 
        DBSession.add(menuitem)     
        menuitem = MenuItem(name=name, description=description, menu_id=10)
        allergen = Allergen(menu_item_id=menuitem.id, allergen="Dairy")
        DBSession.add(allergen)
        menuitem = MenuItem(name="Steamed Branzino", description='Why mess with perfection and this application says it all', menu_id=10) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name="Corn, spinach and fire-roasted red bell pepper pancakes", description='Flour, butter, cayenne. eggs, basil', menu_id=10) 
        DBSession.add(menuitem) 
        menuitem = MenuItem(name="Veggie", description='Spaghetti raw zucchinis\n Snuff said\n Herbed mascarpone cream', menu_id=10) 
        DBSession.add(menuitem) 
        menuItems = DBSession.query(MenuItem).filter(MenuItem.menu_id==10).all()
        menuItemIds = ' '.join(str(menuItem.id) for menuItem in menuItems)
        menu = Menu(name="Smoked salmon and smoked trout blinis", date='2012-7-23', time_sort_key=2, menus=menuItemIds)
        DBSession.add(menu)
