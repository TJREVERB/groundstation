from functools import wraps

from jsonschema import validate as v

schemas = {
    "received": {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "sat_time": {"type": "string"}
        },
        "required": ["message", "sat_time"]
    }
}


def validate(schema, position=0):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            v(args[position], schemas[schema])
            return function(*args, **kwargs)

        return wrapper

    return decorator
