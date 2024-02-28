# sieve_tests.py

"""
This program loops through different functions for finding prime numbers
Keeps track of time and memory use for each function 
Writes these data points into a dataframe
Creates a graph from that dataframe

NOTE: If run in VSCode, I get a nice, interactive 3d graph, but I've been unable to get Pycharm to do this.
"""

import pandas as pd
import numpy as np
from numba import jit
from sympy import isprime
from primePy import primes
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import datetime

from timer_func import *
from prime_finders import *


def main():
    """
    Main function, loops through all prime finder functions for all orders of magnitude
    creates and populates a DataFrame with a tuple of (order_of_mag, function_time, function_mem)
    transforms that dataframe and sends it to the function for creating a graph
    """
    func_list = [
                 human,
                 smart_human,
                 list_sieve,
                 basic_pandas,
                 basic_numpy,
                 sympy,
                 primepy,
                 dijkstra,
                 numba_human,
                 numba_smart_human,
                 numba_list_sieve
                ]
    results = pd.DataFrame()

    maxi = get_order_of_mag()
    
    for order_of_mag in range(1, maxi):  # this is where you change the range of order of magnitude
        mini = 2
        maxi = 1 + 2 ** order_of_mag
        order_result = []
        for func in func_list: 
            print(f'Runnning: {func}')
            result, function_time, function_mem = func(mini, maxi)
            point = (order_of_mag, function_time, function_mem)
            order_result.append(point)
            print('\n')
        order_result = pd.Series(order_result)
        results[f'{order_of_mag}'] = order_result

    vis_df = results.T
    vis_df.columns = [func_name.__name__ for func_name in func_list]
    print(vis_df)
    make_graph(vis_df)


def get_order_of_mag() -> int:
    """
    Asks for user input to define the maximum exponent to run the function.
    Uses a try/except block to make sure the input is a positive integer greater than 1
    
    :return maxi: The user-defined maximum 
    """
    while True:
        maxi = input('\nEnter the maximum exponent [2^x] \n x = ')
        try:
            maxi = int(maxi)
            if maxi >= 2:
                break
        except ValueError:
            print('Please enter a valid natural number.')
    return(maxi)


def make_graph(vis_df: pd.DataFrame):
    """
    Creates a graph from the given dataframe.
    Loops through each column (prime function), parses the tuple, and creates a datapoint. 
    Each column is a line on the graph.
    displays graph

    :param vis_df: The dataframe of tuples for each function
    """

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.set_xlabel('Magnitude', fontsize=10)
    ax.set_ylabel('Time', fontsize=10)
    ax.set_zlabel('Memory', fontsize=10)

    all_time = 0

    vis_df = vis_df.iloc[1:]  # numba takes a long time to do it's intial JIT processing; this filteres out this outlier
    for column in vis_df:  
        x = []
        y = []
        z = []
        for row in vis_df[column]:
            x.append(row[0])
            y.append(row[1])
            z.append(row[2])
        ax.plot(x, y, z, label=column)  #plots each individual line
        all_time += sum(y)  # adds all time to a total time calculation
    print(f'Total Time: {str(datetime.timedelta(seconds=all_time))}')
    ax.legend(fontsize=8, loc=(-0.35, 0.6))
    plt.show()
    


if __name__ == '__main__':
    main()
    