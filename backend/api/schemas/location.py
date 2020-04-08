from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

location_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "longitude": {
            "type": "number",
        },
        "latitude": {
            "type": "number",
        },
        "user_id": {
            "type": "string",
        },
        "label": {
            "type": "string",
        }
    },
    "required": ["longitude", "latitude", "user_id"],
    "additionalProperties": False
}


def validate_location(data):
    """Validate location using schema supplied above."""
    try:
        validate(data, location_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
