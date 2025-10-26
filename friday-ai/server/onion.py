from functools import wraps
from flask import request, jsonify

def authentication_required(database):
    def route_decorator(route_function):
        @wraps(route_function)
        def decorated_route(*args, **kwargs):
            auth_token = request.get_json()["auth_token"]
            if not auth_token:
                return jsonify({'message': 'Missing authentication token'}), 401
            if not database.validate_token(auth_token):
                return jsonify({'message': 'Invalid authentication token'}), 401
            return route_function(*args, **kwargs)
        return decorated_route
    return route_decorator

