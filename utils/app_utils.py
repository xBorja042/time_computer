import pandas as pd
import datetime
from datetime import date
import time
import os
import json


def read_codes(primary_key: str, second_key: str = False):
    """The purpose of this function is to read the input dataframe that contains the codes for the application."""
    with open(os.path.dirname(__file__) + '/../input_files/codes.json') as f:
        if not second_key:
            code = json.loads(f.read())[primary_key]
        else:
            code = json.loads(f.read())[primary_key][second_key]
    return code


def get_times(current: bool = True):
    """Returns day and time of today or the data for previous day."""
    if current:
        remember = input("Do you remember departure time (y/n)? ")
        assert remember == "y" or remember == "n", "Answer needs to be either (y) or (n)!!!"
        if remember == "y":
            hour = input("OK. Then input your departure time in (hh:mm): ")
        else:
            hour = time.strftime('%X %x %Z')[:5]
        day = datetime.datetime.today().strftime("%d/%m/%Y")
    else:
        day = datetime.datetime.today() - datetime.timedelta(days=1)
        day = day.strftime("%d/%m/%Y")
        remember = input("Do you remember departure time (y/n)? ")
        if remember == "y":
            hour = input("OK. Then input your departure time in (hh:mm): ")
        else:
            hour = "19:00"
    return day, hour


def get_sense(current_time: str):
    """This function computes the direction of the travel depending on the time of the day."""
    comparing_time = current_time
    midday = "12:00"
    if comparing_time < midday:
        direction = "1"
    else:
        direction = "2"
    return direction


def get_travel_df(current_day: str, current_time: str) -> pd.DataFrame:
    """This function fulfills all the information related to travel history."""
    items = [item for item in enumerate(read_codes("means").values())]
    print(f"These are the available ways to come here {items}")
    m = input("Enter how you came: ")
    assert str(m) in read_codes("means").keys(), "The way you came needs to be a valid way!!"
    elapsed_time = int(input("Enter your total time measured in minutes: "))
    observation = input_obs()
    test_elapsed_time(elapsed_time)
    day_name = compute_day_name(current_day=current_day)
    direction = read_codes("senses", get_sense(current_time))
    data = pd.DataFrame({"date": current_day, "data_collection_time": current_time, "direction": direction,
                         "means_of_transport": read_codes("means", m), "elapsed_time (mins)": elapsed_time,
                         "observation": observation, "week_day": day_name}, index=[0])
    return data


def input_obs() -> str:
    any_obs = input("Do you have any observation? (y/n): ")
    assert any_obs == "y" or any_obs == "n", "Answer needs to be either (y) or (n)!!!"
    if any_obs == "y":
        obs = input("Enter a short observation: ")
    else:
        obs = ""
    return obs


def write_output_file(df: pd.DataFrame):
    """This function writes the resulting file with all the information from travels"""
    input_output = os.path.dirname(__file__) + '/../input_files'
    files = os.listdir(input_output)
    csv = [file for file in files if '.csv' in file]
    file_name = "/historic_travels4.csv"
    if not csv:
        df.to_csv(input_output + file_name, sep="|", index=False, header=True)
    else:
        historic = pd.read_csv(input_output + file_name, sep="|")
        df = pd.concat([historic, df], ignore_index=True)
        df.to_csv(input_output + file_name, sep="|", index=False, header=True)


def initial_times():
    """This function limits travel times"""
    input_output = os.path.dirname(__file__) + '/../input_files'
    files = os.listdir(input_output)
    csv = [file for file in files if '.csv' in file]
    day, hour = "", ""
    if not csv:
        day, hour = get_times()
    else:
        historic = pd.read_csv(input_output + "/historic_travels4.csv", sep="|").sort_values(by="date")
        last_2_days = pd.to_datetime(historic["date"].values, format='%d/%m/%Y').sort_values().values[-2:]
        if last_2_days[0] != last_2_days[1]:
            y = input("Hello, did you fulfill last day return journey (y/n)? ")
            assert y == "y" or y == "n", "Answer needs to be either (y) or (n)!!!"
            if y == "y":
                day, hour = get_times()
            elif y == "n":
                day = datetime.datetime.today().strftime("%d/%m/%Y")
                last_travel = pd.to_datetime(last_2_days[1]).strftime("%d/%m/%Y")
                if day == last_travel:
                    _, hour = get_times()
                else:
                    day, hour = get_times(current=False)
        else:
            day, hour = get_times()
    return day, hour


def test_elapsed_time(elapsed_time: int):
    assert isinstance(elapsed_time, int), "We need a number to measure time!!"
    assert 10 < elapsed_time < 300, "Elapsed time needs to be in correct range!!"


def compute_day_name(current_day: str) -> str:
    return datetime.datetime.strptime(current_day, '%d/%m/%Y').strftime("%A")
