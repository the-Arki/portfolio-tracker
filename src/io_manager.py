import json
import matplotlib.pyplot as plt
import pandas as pd


def read_json(filename):
    with open(filename, "r") as data:
        result = json.load(data)
    return result


def write_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)


def save_plot(name, df):
    df.plot(kind='line')
    plt.savefig('./files/images/' + name + '_graph.png')
    plt.close()
