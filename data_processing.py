NB_OF_MEAS = 15
import statistics
import numpy as np
import matplotlib.pyplot as plt
import datetime


def data_processing():
    with open("measure_output.txt","r") as f:
        raw_data = f.readlines()


    data = []

    k = 0
    j=0

    while k<len(raw_data):
        data.append([])
        for _ in range(NB_OF_MEAS):
            data[j].append(float(raw_data[k][:-1]))
            k+=1
        j+=1

    data_wout_outliers = []
    cleaned_data = []
    stddev = []

    def remove_outliers_zscore(data, threshold=1.5):
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        print("zscores :", z_scores)
        cleaned_data = data[z_scores < threshold]
        return cleaned_data

    for series in data:
        series = np.array(series)
        # print(series)
        temp=remove_outliers_zscore(series)
        # print(temp)
        data_wout_outliers.append(temp)

    for values in data_wout_outliers:
        cleaned_data.append(statistics.mean(values))
        stddev.append(statistics.stdev(values))
        
    print(cleaned_data)

    x = np.arange(1,len(cleaned_data)+1)
    y = np.array(cleaned_data)

    fig, ax = plt.subplots()
    ax.errorbar(x, y, yerr=stddev, fmt="o", capsize=3)

    ax.set_xlabel('Number of copies on IPFS network')
    ax.set_ylabel('Time to retrieve data in seconds')
    ax.set_title('Values with Standard Deviation')

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    plt.savefig(f"graphs/{formatted_datetime}.png")
    print(f"Figure saved to graphs/{formatted_datetime}.png")

data_processing()