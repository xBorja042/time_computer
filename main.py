from utils.app_utils import *


def main():
    current_day, current_time = initial_times()
    data_travel = get_travel_df(current_day, current_time)
    write_output_file(data_travel)


if __name__ == '__main__':
    main()
