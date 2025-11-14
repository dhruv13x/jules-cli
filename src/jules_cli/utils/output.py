import json

def print_json(data, pretty=False):
    """Prints a dictionary as a JSON string."""
    if pretty:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))
