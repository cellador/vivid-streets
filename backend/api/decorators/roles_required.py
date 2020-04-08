import functools
from flask import abort
from flask_jwt_extended import get_jwt_identity


def roles_required(*role_names):
    """Only allow requests that have a JWT in the header containing the roles required."""
    def decorator(original_route):
        @functools.wraps(original_route)
        def decorated_route(*args, **kwargs):
            identity = get_jwt_identity()
            if identity is None:
                abort(401)  # 401 Unauthorized

            missing_roles = [
                role_name
                for role_name in role_names
                if role_name not in identity['roles']
            ]

            if missing_roles:
                abort(401)

            return original_route(*args, **kwargs)

        return decorated_route

    return decorator
