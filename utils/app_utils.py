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


def get_times(current=True):
    """Returns day and time of today or the data for previous day."""
    if current:
        day = datetime.datetime.today().strftime("%d/%m/%Y")
        hour = time.strftime('%X %x %Z')[:5]
    else:
        day = datetime.datetime.today() - datetime.timedelta(days=1)
        day = day.strftime("%d/%m/%Y")
        hour = "19:00"
    return day, hour


def get_sense(current_day, current_time):
    complete_time = current_day + " " + current_time
    complete_time = datetime.datetime.strptime(complete_time, '%d/%m/%Y %H:%M')
    now = datetime.datetime.now()
    if complete_time < now.replace(hour=12, minute=0, second=0, microsecond=0):
        direction = "1"
    else:
        direction = "2"
    return direction


def get_travel_df(current_day, current_time) -> pd.DataFrame:
    # current_day, current_time = get_times()
    items = [item for item in enumerate(read_codes("means").values())]
    print(f"These are the available ways to come here {items}")
    m = input("Enter how you came: ")
    assert str(m) in read_codes("means").keys(), "The way you came needs to be a valid way!!"
    elapsed_time = int(input("Enter your total time measured in minutes: "))
    assert isinstance(elapsed_time, int), "We need a number to measure time!!"
    direction = read_codes("senses", get_sense(current_day, current_time))
    data = pd.DataFrame({"date": current_day, "data_collection_time": current_time, "direction": direction,
                         "means_of_transport": read_codes("means", m), "elapsed_time (mins)": elapsed_time}, index=[0])
    return data


def write_output_file(df: pd.DataFrame):
    input_output = os.path.dirname(__file__) + '/../input_files'
    files = os.listdir(input_output)
    csv = [file for file in files if '.csv' in file]
    if not csv:
        df.to_csv(input_output + "/historic_travels.csv", sep="|", index=False, header=True)
    else:
        historic = pd.read_csv(input_output + "/historic_travels.csv", sep="|")
        df = pd.concat([historic, df], ignore_index=True)
        df.to_csv(input_output + "/historic_travels.csv", sep="|", index=False, header=True)


def initial_times():
    input_output = os.path.dirname(__file__) + '/../input_files'
    files = os.listdir(input_output)
    csv = [file for file in files if '.csv' in file]
    if not csv:
        # df = pd.DataFrame()
        # df.to_csv(input_output + "/historic_travels.csv", sep="|", index=False, header=True)
        day, hour = get_times()
    else:
        historic = pd.read_csv(input_output + "/historic_travels.csv", sep="|").sort_values(by="date")
        last_2_days = pd.to_datetime(historic["date"].values, format='%d/%m/%Y').sort_values().values[-2:]
        print("Last 2 days: ", last_2_days)
        if last_2_days[0] != last_2_days[1]:
            y = input("Hello, did you fullfilled last day travels (y/n)? ")
            assert y == "y" or y == "n", "Answer needs to be either (y) or (n)!!!"
            if y == "y":
                day, hour = get_times()
            elif y == "n":
                day, hour = get_times(False)
        else:
            day, hour = get_times()
    return day, hour



        # df.to_csv(input_output + "/historic_travels.csv", sep="|", index=False, header=True)