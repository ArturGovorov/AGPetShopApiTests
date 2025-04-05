STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "status": {
            "type": "string",
            "enum": ["placed", "approved"]
        },
        "complete": {
            "type": "boolean"
        },
    },
    "required": ["id", "petId", "quantity", "status", "complete"],
    "additionalProperties": False
}
