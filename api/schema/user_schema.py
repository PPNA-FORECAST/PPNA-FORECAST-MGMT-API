user_register_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "datapoints": {
            "type": "array",
            "items": {"type": "number"}
        }
    },
    "required": ["email", "password", "datapoints"]
}

user_login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
}