from flask import Flask, request, g, make_response
from app.common import logger
from app.common.logger import Logger
from app.config.settings import LoggerConfig
import json
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(LoggerConfig)

    app.template_folder = os.path.join(app.root_path, 'html')

    @app.before_request
    def before_request_init():
        if request.method == 'OPTIONS':
            response = {'code': 0, 'msg': '', 'data': 'ok'}
            response = json.dumps(response, default=str)
            response = make_response(response)
            response.headers["Access-Control-Allow-Origin"] = '*'
            response.headers["Access-Control-Allow-Headers"] = '*'
            response.headers["Access-Control-Allow-Method"] = '*'
            return response
        g.config = app.config
        g.ip = request.remote_addr
        g.log = Logger(info_log=g.config.get("INFO_LOG"),
                       error_log=g.config.get("ERROR_LOG"),
                       slow_action=g.config.get("SLOW_ACTION"),
                       level_no=g.config.get("LEVEL_INFO"), client_identification=g.ip)
        print(g.config.get("INFO_LOG"))

    # api路由
    from app.v1 import interface as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1/api')

    # 显示前端页面路由
    from app.v1 import template as view_blueprint
    app.register_blueprint(view_blueprint, url_prefix='/v1/html')

    print(app.url_map)
    return app
