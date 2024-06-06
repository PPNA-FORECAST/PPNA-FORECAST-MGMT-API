user_register_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 3
        },
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
        "geometry": {
            "type": "array",
            "items": {"type": "array", "items": {"type": "number"}},
            "minItems": 3
        }
    },
    "required": ["username","email", "password", "geometry"]
}

user_login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
}