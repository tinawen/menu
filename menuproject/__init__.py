from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.renderers import JSONP
from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('daily_menu', '/daily')
    config.add_route('daily_menu_json', '/api/daily')
    config.add_route('view_menus', '/view_menus/{menu_year}/{menu_month}')
    config.add_route('view_menu', '/menu/{menu_id}')
    config.add_route('view_menus_today', '/')
    config.add_route('edit_menus_today', '/edit')
    config.add_route('edit_menus', '/edit_menus/{menu_year}/{menu_month}')
    config.add_route('create_menu_item', '/create_menu_item/{menu_id}')
    config.add_route('create_menu', '/create_menu')
    config.add_route('edit_menu', '/edit_menu/{menu_id}')
    config.add_route('delete_menu_item', '/delete_menu_item/{menu_id}')
    config.add_route('update_menu_item_allergen', '/update_menu_item_allergen/{menu_item_id}')
    config.add_route('update_menu_item_healthy', '/update_menu_item_healthy/{menu_item_id}')
    config.add_route('update_menu_item_name', '/update_menu_item_name/{menu_item_id}')
    config.add_route('update_menu_item_desc', '/update_menu_item_desc/{menu_item_id}')
    config.add_route('update_menu_name', '/update_menu_name/{menu_id}')
    config.add_route('update_menu_order', '/update_menu_order/{menu_id}')
    config.add_route('update_menu_month', '/edit/{meny_year}/{menu_month}')
    config.add_route('publish', '/publish/{menu_id}')
    config.add_route('screen', '/screen')
    config.add_route('attach_pictures', '/attach_pictures/{menu_id}')
    config.add_route('delete_picture', '/delete_picture/{menu_id}')
    config.include('pyramid_jinja2')
    config.include('pyramid_mailer')
    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.scan()
    return config.make_wsgi_app()

