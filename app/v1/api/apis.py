from app.v1.api import interface
from flask import g


@interface.route('/get_ip', methods=['GET'])
def api() -> str:
    g.log.outside_error('test')
    return g.ip
