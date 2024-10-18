import itertools
import time
import argparse
import csv

# Function to build all possible combinations of coins (weighted formulas, or wffs)
def build_coin_wff(coin_names, coin_value, coin_quant):
    num_clauses = 1

    # Calculate the total number of possible combinations (clauses)
    for i in range(len(coin_quant)):
        num_clauses *= (coin_quant[i] + 1)
   
    possible_wffs = []
    # Create ranges for each type of coin
    ranges = [range(quant + 1) for quant in coin_quant]
    
    # Generate the cartesian product of all ranges
    for combination in itertools.product(*ranges):
        yield combination

    return possible_wffs

# Function to test all combinations (wffs) and find those that match the desired total value
def test_wffs(wffs, coin_values, desired_max):
    satisfiable = []  # To store valid combinations
    num_wffs = 0  # Counter for the number of wffs tested
    # Iterate through each wff (combination of coins)
    for wff in wffs:
        num_wffs += 1
        total = 0
        # Calculate the total value of coins in the current combination
        for i, coin in enumerate(wff):
            total += coin * coin_values[i]
            # If the total exceeds the desired max, skip the current combination
            if total > desired_max:
                continue
        # If the total matches the desired max, save the valid combination
        if total == desired_max:
            satisfiable.append(wff)
    return satisfiable, num_wffs

# Function to run tests with either user input or preset coin values
def run_tests(coin_names, voin_value, coin_quant):
    
    user_input = ""
    # Loop to get user input for coin types, values, and quantities
    user_input = input("What's the name of your first coin? (enter done if no more) ")
    while True:
        coin_names.append(user_input)                                    # Append coin name
        coin_value.append(int(input("What is its value? ")))             # Append coin value    
        coin_quant.append(int(input("How many do you have? ")))          # Append coin quantity
         # Get input for the next coin or break the loop
        user_input = input("What's the name of your next coin? (enter to finish) ")
        user_input.strip()
        if user_input == '':
            break
        desired_max = int(input("What is your desired value in cents? "))
    
    satisfied, num_wffs = test_wffs(wffs, coin_value, cents)
    # If no solutions are found
    if (len(satisfied)) == 0:
        print("No possible solutions")
    else:    

        print("working combinations: ", len(satisfied))
        # Ask if the user wants to print all valid combinations
        print_vals = input("Would you like to see all combinations? (y/n) ")
        # Print each solution and the corresponding coin quantities
        if (print_vals == 'y' or print_vals == 'Y'):
            # customize to coins
            for j, wff in enumerate(satisfied):
                print(f"Solution {j}:")
                for i in range(len(coin_names)):
                    print(coin_names[i], ": ", wff[i])
                print()
    


if True:
    coin_names = []
    coin_value = []
    coin_quant = []

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Process user inputs to determine whether to use test scripts or user determined values.")

    # Add an argument for file input, with "user" as the default
    parser.add_argument("-f", "--file", type=str, help="Input argument", default="user")  # Optional argument with a default value

    args = parser.parse_args()
    # If the user provides a file
    if args.file != "user":
        data = []
        desired_max = 34
        # Example coin data
        coin_names = ["3 Cent", "6 Cent", "7 Cent", "11 Cent"]
        coin_value = [3, 6, 7, 11]
        
        # Loop through each row in the CSV
        with open('output_tests_godmark.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                start_time = time.time()    # Record the start time for performance measurement
                coin_quant = []

                # Parse the quantities of each coin from the CSV
                for i in range(2, len(row)):
                    coin_quant.append(int(row[i]))

                # Build all possible wffs (combinations) and test them
                wffs = build_coin_wff(coin_names, coin_value, coin_quant)
                satisfied, num_wffs = test_wffs(wffs, coin_value, int(row[1]))
                end_time = time.time()
                
                # Count the total number of coins used in the row
                num_coins = 0
                for val in coin_quant:
                    num_coins += val
                    
                # Append the results (row, number of coins, execution time in milliseconds) to the data list
                data.append([row[0], num_coins, (end_time-start_time) * 1000])
                
        # Write the results to an output CSV file
        with open('output_godmark.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            file.close()
        
        file.close()
    else:
        # If no file is provided, run the user-input test
        run_tests(coin_names, coin_value, coin_quant)
