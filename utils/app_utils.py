import pandas as pd
import datetime
import time
import os
import json


def read_codes(primary_key:str, second_key: str = False):
    with open(os.path.dirname(__file__) + '/../input_files/codes.json') as f:
        if not second_key:
            code = json.loads(f.read())[primary_key]
        else:
            code = json.loads(f.read())[primary_key][second_key]
    return code


def get_times():
    today = datetime.date.today().strftime("%d/%m/%Y")
    hour = time.strftime('%X %x %Z')[:5]
    return today, hour


def get_sense():
    now = datetime.datetime.now()
    if now < now.replace(hour=12, minute=0, second=0, microsecond=0):
        direction = "1"
    else:
        direction = "2"
    return direction


def get_travel_df() -> pd.DataFrame:
    current_day, current_time = get_times()
    items = [item for item in enumerate(read_codes("means").values())]
    print(f"These are the available ways to come here {items}")
    m = input("Input how you came: ")
    elapsed_time = int(input("Input your total time measured in minutes: "))
    assert isinstance(elapsed_time, int), "We need a number to measure time!!"
    direction = read_codes("senses", get_sense())
    data = pd.DataFrame({"date": current_day, "data_collection_time": current_time, "direction": direction,
                         "means_of_transport": read_codes("means", m), "elapsed_time (mins)": elapsed_time}, index=[0])
    return data


def get_input_file(df: pd.DataFrame):
    input_output = os.path.dirname(__file__) + '/../input_files'
    files = os.listdir(input_output)
    csv = [file for file in files if '.csv' in file]
    # print(files, csv)
    if not csv:
        df.to_csv(input_output + "/historic_travels.csv", sep="|", index=False, header=True)
        # print("No input DF, creating it")
    else:
        historic = pd.read_csv(input_output + "/historic_travels.csv", sep="|")
        df = pd.concat([historic, df], ignore_index=True)
        df.to_csv(input_output + "/historic_travels.csv", sep="|", index=False, header=True)
