import matplotlib.pyplot as plt
import csv

times = []
num_wffs = []


with open('output.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        times.append(row[2])
        num_wffs.append(row[1])

    file.close()

# Create the plot
plt.plot(num_wffs, times)

# Add labels and a title
plt.xlabel("Number of WFFs Tested")
plt.ylabel("Time to Find All Possible Solutions")
plt.title("Coin Problem")

# Display the graph
plt.savefig('coin_problem_plot.png')
