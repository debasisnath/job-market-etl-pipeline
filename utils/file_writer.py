import json

def save_json(data, output):

    with open(output, "w") as f:
        json.dump(data, f, indent=2)


