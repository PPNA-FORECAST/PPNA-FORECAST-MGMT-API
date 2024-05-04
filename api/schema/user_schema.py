user_register_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email", 
            "pattern": "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$" 
        },
        "password": {
            "type": "string",
            "minLength": 8, # Password must be at least 8 characters
            "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$"  # Password must have Upper case, Lower case and numbers
        },
        "datapoints": {
            "type": "array",
            #"items": {"type": "number"},
            "minItems": 3  # There must be at least 3 datapoints
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