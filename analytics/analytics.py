import numpy as np
import pandas as pd
import os

print("This is a script to analyze gathered data")


file = 'historic_travels4.csv'
input_file_path = os.path.join("./../input_files", file)

df = pd.read_csv(filepath_or_buffer=input_file_path, sep="|")
df["observation"] = ""


output_file = "processed_file.csv"
output_file_path = os.path.join("./../input_files", output_file)
df.to_csv(output_file_path, sep="|")



import matplotlib.pyplot as plt

q = 12
df = df.loc[df["means_of_transport"] != "Coche", :]

for direction in df["direction"].unique().tolist():
    print(" DIRECTION ", direction)
    sub_df = df.loc[df["direction"] == direction].reset_index()
    elapsed_times = sub_df["elapsed_time (mins)"].to_numpy(copy=True)
    mean_time = np.mean(elapsed_times)
    plt.plot(range(len(elapsed_times)), elapsed_times, marker="o")
    plt.plot(range(len(elapsed_times)), [mean_time for i in range(len(elapsed_times))])
    plt.text(q, 75, direction + "_" + str(mean_time)[:2], rotation=40, verticalalignment='center')
    q += 12
    plt.title("Elapsed travel times measured in minutes")
    plt.legend([direction, "Media_" + direction])
    plt.savefig("output_files/times_plot" + direction + ".png")

plt.legend(["Ida", "tiempo_medio_ida", "vuelta", "tiempo_medio_vuelta"])
plt.savefig("output_files/times_plot" + direction + ".png")
plt.show()


df["elapsed_time (mins)"].plot()
plt.show()
