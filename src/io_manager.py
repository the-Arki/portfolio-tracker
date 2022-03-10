import json


def read_json(filename):
    with open(filename, "r") as data:
        result = json.load(data)
    return result


def write_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)
