from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_creation_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
        # "roles": {
        #     "type": "array",
        #     "minItems": 1,
        #     "items": {
        #         "type": "string",
        #         "enum": ["admin", "member"]
        #     }
        # }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

user_authentication_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_user_registration(data):
    """Validate user using schema supplied above."""
    try:
        validate(data, user_creation_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_authentication(data):
    """Validate user using schema supplied above."""
    try:
        validate(data, user_authentication_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
