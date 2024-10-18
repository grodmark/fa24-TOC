import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Load the CSV file
# Assuming the CSV file is in the format: size,num_coins,time
df = pd.read_csv('output_godmark.csv')

# Set color mapping based on size
color_map = {
    'Small': 'blue',
    'Medium': 'orange',
    'Large': 'green'
}

# Map sizes to corresponding colors
colors = df['size'].map(color_map)

# Create the plot
fig, ax = plt.subplots()
plt.scatter(df['num_wffs'], df['time'], label='Data Points')

# Scatter plot: num_coins on x-axis, time on y-axis, color-coded by size
scatter = ax.scatter(df['num_wffs'], df['time'], c=colors, label=df['size'])

# Add a legend to describe the colors
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[size], markersize=10, label=size)
           for size in color_map]
#ax.legend(handles=handles, title="Size")

# Extract the 'num_coins' and 'time' columns
x = df['num_wffs']
y = df['time']

# Define the exponential function for curve fitting
def exponential_func(x, a, b):
    return a * np.exp(b * x)

# Fit the data to the exponential function
popt, pcov = curve_fit(exponential_func, x, y, p0=(1, 0.01))  # Initial guess for a and b

# Extract the parameters a and b from popt
a, b = popt

# Create a scatter plot
plt.scatter(x, y, label='Data Points')

# Plot the exponential curve
x_fit = np.linspace(min(x), max(x), 100)  # Generate x values for the fitted curve
y_fit = exponential_func(x_fit, *popt)  # Calculate the corresponding y values using the fitted parameters
plt.plot(x_fit, y_fit, color='red', label=f'Best fit: y = {a:.2f}e^({b:.2f}x)')

# Display the equation on the plot
plt.text(0.1, 0.9, f'Line of Best Fit \ny = {a:.2f}e^({b:.2f}x)', fontsize=12, transform=plt.gca().transAxes)

# Set x-axis ticks to increment by 5
ax.set_xticks(np.arange(0, df['num_wffs'].max() + 1, 15))
# Set axis labels
ax.set_xlabel('Number of Coins')
ax.set_ylabel('Time to Process (ms)')

# Set title
ax.set_title('Time to Process Number of Coins')
#plt.legend()
# Show the plot
plt.show()
