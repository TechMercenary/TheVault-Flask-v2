from flask import Blueprint, jsonify
from flask.views import MethodView
from config import get_app_settings
import os


api_bp = Blueprint(
        name='api',
        import_name=__name__,
        url_prefix='/api'
    )


class AppSettings(MethodView):
    def get(self):
        # app_settings = get_app_settings()
        response = {
            'FERNET_KEY': os.environ.get('FERNET_KEY'),
            # 'DEFAULT_COUNTRY': app_settings['DEFAULT_COUNTRY'],
            # 'DEFAULT_CURRENCY': app_settings['DEFAULT_CURRENCY'],
            # 'UI_TIMEZONE': app_settings['UI_TIMEZONE'],
        } 
        return jsonify(response)


api_bp.add_url_rule(rule='/app_settings', view_func=AppSettings.as_view('app_settings'))
