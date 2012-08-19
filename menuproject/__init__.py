from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('daily_menu', '/daily')
    config.add_route('view_menus_init', '/')
    config.add_route('view_menus', '/view_menus/{menu_month}')
    config.add_route('view_menu', '/menu/{menu_id}')
    config.add_route('edit_menus_init', '/edit')
    config.add_route('edit_menus', '/edit_menus/{menu_month}')
    config.add_route('create_menu_item', '/create_menu_item/{menu_id}')
    config.add_route('create_menu', '/create_menu')
    config.add_route('edit_menu', '/edit_menu/{menu_id}')
    config.add_route('delete_menu_item', '/delete_menu/{menu_id}')
    config.add_route('update_menu_item_allergen', '/update_menu_item_allergen/{menuItem_id}')
    config.add_route('update_menu_item_name', '/update_menu_item_name/{menuItem_id}')
    config.add_route('update_menu_item_desc', '/update_menu_item_desc/{menuItem_id}')
    config.add_route('update_menus_name', '/update_menus_name/{menu_id}')
    config.add_route('update_menus', '/update_menus/{menu_id}')
    config.add_route('update_menu_month', '/edit/{menu_month}')
    config.include('pyramid_jinja2')
    config.scan()
    return config.make_wsgi_app()

