import itertools
import time
import argparse
import csv

def build_coin_wff(coin_names, coin_value, coin_quant):
    num_clauses = 1

    for i in range(len(coin_quant)):
        num_clauses *= (coin_quant[i] + 1)
   
    possible_wffs = []
    # Create ranges for each type of coin
    ranges = [range(quant + 1) for quant in coin_quant]
    
    # Generate the cartesian product of all ranges
    for combination in itertools.product(*ranges):
        yield combination

    return possible_wffs

def test_wffs(wffs, coin_values, desired_max):
    satisfiable = []
    num_wffs = 0
    for wff in wffs:
        num_wffs += 1
        total = 0
        for i, coin in enumerate(wff):
            total += coin * coin_values[i]
            if total > desired_max:
                continue
        if total == desired_max:
            satisfiable.append(wff)
    return satisfiable, num_wffs

def run_tests(coin_names, voin_value, coin_quant):
    
    user_input = ""
    user_input = input("What's the name of your first coin? (enter done if no more) ")
    while True:
        coin_names.append(user_input)
        coin_value.append(int(input("What is its value? ")))
        coin_quant.append(int(input("How many do you have? ")))
        user_input = input("What's the name of your next coin? (enter to finish) ")
        user_input.strip()
        if user_input == '':
            break
        desired_max = int(input("What is your desired value in cents? "))

    satisfied, num_wffs = test_wffs(wffs, coin_value, cents)
    if (len(satisfied)) == 0:
        print("No possible solutions")
    else:    

        print("working combinations: ", len(satisfied))

        print_vals = input("Would you like to see all combinations? (y/n) ")

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

    # Add arguments
    parser.add_argument("-f", "--file", type=str, help="Input argument", default="user")  # Optional argument with a default value

    args = parser.parse_args()
    if args.file != "user":
        data = []
        desired_max = 34
        coin_names = ["3 Cent", "6 Cent", "7 Cent", "11 Cent"]
        coin_value = [3, 6, 7, 11]
       # with open('output.csv', 'w', newline='') as file:
        #    writer = csv.writer(file)
        with open('output_tests_godmark.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                start_time = time.time()
                coin_quant = []
                for i in range(2, len(row)):
                    coin_quant.append(int(row[i]))
                wffs = build_coin_wff(coin_names, coin_value, coin_quant)
                satisfied, num_wffs = test_wffs(wffs, coin_value, int(row[1]))
                end_time = time.time()
                num_coins = 0
                for val in coin_quant:
                    num_coins += val
                data.append([row[0], num_coins, (end_time-start_time) * 1000])
        with open('output_godmark.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            file.close()
        
        file.close()
    else:
        run_tests(coin_names, coin_value, coin_quant)
