import pandas as pd
import os

print("This is a script to analyze gathered data")

print(os.getcwd(), os.listdir(), os.listdir("./../input_files"))

file = 'historic_travels2.csv'
input_file_path = os.path.join("./../input_files", file)

df = pd.read_csv(filepath_or_buffer=input_file_path, sep="|")
df["observation"] = ""

# print(df)

output_file = "processed_file.csv"
output_file_path = os.path.join("./../input_files", output_file)
df.to_csv(output_file_path, sep="|")

# print(df)

import matplotlib.pyplot as plt

for direction in df["direction"].unique().tolist():
    print(" DIRECTION ", direction)
    sub_df = df.loc[df["direction"] == direction].reset_index()
    elapsed_times = sub_df["elapsed_time (mins)"].to_numpy(copy=True)
    plt.scatter(range(len(elapsed_times)), elapsed_times)
    print(sub_df)
    sub_df["elapsed_time (mins)"].plot()
    plt.title("Elapsed travel times measured in minutes")
    # plt.savefig("output_files/times_plot.png")
plt.legend(["Ida", "", "Vuelta", ""])
plt.show()
