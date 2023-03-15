import pandas as pd
import os

print("This is a script to analyze gathered data")

print(os.getcwd(), os.listdir(), os.listdir("./../input_files"))

file = 'historic_travels2.csv'
input_file_path = os.path.join("./../input_files", file)

df = pd.read_csv(filepath_or_buffer=input_file_path, sep="|")
df["observation"] = ""

print(df)

output_file = "processed_file.csv"
output_file_path = os.path.join("./../input_files", output_file)
df.to_csv(output_file_path, sep="|")

print(df)

import matplotlib.pyplot as plt

elapsed_times = df["elapsed_time (mins)"].to_numpy(copy=True)
plt.scatter(range(len(elapsed_times)), elapsed_times)
df["elapsed_time (mins)"].plot()
plt.title("Elapsed travel times measured in minutes")
plt.show()



# plt.show()