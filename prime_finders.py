# prime_finders.py

"""
A list of functions which get imported to sieve_tests.py
Wraps each function in a time and memory wrapper
no function returns anyting, since the important information is returned by the wrapper
"""

import pandas as pd
import numpy as np
from numba import jit
from sympy import isprime
from primePy import primes

from timer_func import *

@time_and_memory
def human(mini: int, maxi: int):
    """
    basically component division, based around my first impuse on how to find prime numbers
    Loops through whole list of numbers, and divides the candidate by all numbers smaller than it.
    Assumes each number is prime at first
    If there are numbers that divide with no remainder and is not the number itself, flips bool to false.
    Appends numbers for which bool is still true to a separate list of primes

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    primes = []
    for i in raw_numbers:
        prime = True
        for j in raw_numbers[:i]:  # looks at all smaller numbers
            if i % j == 0 and i != j:
                prime = False
                break  # Goes to next number
        if prime == True:
            primes.append(i)  # if prime, then appends to list
    print(f'{human.__name__}: {primes}')


@time_and_memory
def smart_human(mini: int, maxi: int):
    """
    Like human, but smart. Includes filters to component division.
    also adds a level of string procesing which can filter out even numbers and numbers divisible by 5
    cuts down on the component divisor candidates by taking the square root.
    Only divides by primes smaller than the sqrt of the 

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    primes = []
    for candidate in raw_numbers:
        prime = True
        stringified = [int(digit) for digit in str(candidate)]
        if ((stringified[-1] in [2, 4, 5, 6, 8, 0]) or (sum(stringified) % 3 == 0)) and candidate not in [2, 3, 5]:
            prime = False
        if prime:
            candidate == candidate ** 0.5 
            for smaller_prime in primes:  # looks at only smaller primes
                if candidate % smaller_prime == 0 and candidate != smaller_prime:
                    prime = False
                    break  # Goes to next number
        if prime:
            primes.append(candidate)  # if prime, then appends to list
    print(f'{smart_human.__name__}: {primes}')


@time_and_memory
def list_sieve(mini: int, maxi: int):
    """
    Sieve of Erastosthanes with the list as the primary data structure
    For each number in a list of the range, it multiplies them by every other number
    less than the max. Removes multiples as it goes a la sieve.
    if it the multiple exceeds the maximum number, breaks the loop to move on to the next number.

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    for candidate in raw_numbers:
        highest = maxi // candidate
        for multiplier in range(candidate, highest + 1):
            multiple = candidate * multiplier
            if multiple in raw_numbers:
                raw_numbers.remove(multiple)
    print(f'{list_sieve.__name__}: {raw_numbers}')


@time_and_memory
def basic_pandas(mini: int, maxi: int):
    """
    Implements the sieve but with a DataFrame
    Tests the utility of the DataFrame as a memory structure 
    in terms of memory use and time required to access locations in that memory. 

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    raw_df = pd.DataFrame(raw_numbers, columns=['num'])

    for row in raw_df['num']:
        multipliers = list(i * row for i in range(row, maxi))
        for multiple in multipliers:
            if multiple <= maxi:
                raw_df = raw_df.drop(raw_df[raw_df['num'] == multiple].index)
            else:
                break
    prime_numbers = raw_df['num'].tolist()
    print(f'{basic_pandas.__name__}: {prime_numbers}')


@time_and_memory
def basic_numpy(mini: int, maxi: int):
    """
    Uses the seive but with a numpy array
    Tests the utility of the numpy array as a memory structure
    in terms of memory use and time required to access locations in that memory.

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    num_array = np.array(raw_numbers)
    for num in num_array:
        multipliers = list(range(2, maxi + 1))
        for multiple in multipliers:
            remove = multiple * num
            if remove <= maxi:
                num_array = np.delete(num_array, np.where(num_array == remove))
            else:
                break
    print(f'{basic_numpy.__name__}: {num_array}')


@time_and_memory
def sympy(mini: int, maxi: int):
    """
    Uses the imported sympy library
    uses 'filter' to map the function onto a range

    :param mini: minimum number
    :param maxi: maximum number
    """
    found_primes = []

    def sympy_check(n):
        if isprime(n):
            found_primes.append(n)

    list(filter(sympy_check, range(mini, maxi)))
    print(f'{sympy.__name__}: {found_primes}')


@time_and_memory
def primepy(mini: int, maxi: int):
    """
    Uses the imported primePy library
    uses 'filter' to map the function onto a range

    :param mini: minimum number
    :param maxi: maximum number
    """
    found_primes = []
    def primepy_check(n):
        if primes.check(n):
            found_primes.append(n)

    list(filter(primepy_check, range(mini, maxi)))
    print(f'{primepy.__name__}: {found_primes}')


@time_and_memory
def dijkstra(mini: int, maxi: int):
    """
    Uses Dijstra's Prime Number Algorithm to find primes
    keeps in track of the list of lists instead of populating a whole sieve
    Works as a 'sieve as you go', which should be more memory efficient

    :param mini: minimum number
    :param maxi: maximum number
    """
    list_of_lists = [[2, 4]]
    for candidate in range(mini + 1, maxi):
        smaller = False
        seconds = [pair[1] for pair in list_of_lists]
        if candidate < min(seconds):
            smaller = True
        for test_tuple in list_of_lists:
            if candidate == test_tuple[1]:
                test_tuple[1] += test_tuple[0]
        if smaller:
            list_of_lists.append([candidate, 2 * candidate])
    found_primes = [p[0] for p in list_of_lists]
    print(f'{dijkstra.__name__}: {found_primes}')


@time_and_memory
@jit(nopython=True)
def numba_human(mini: int, maxi: int):
    """
    Uses numba's JIT compiler to hopefully optimize the 'human' function.

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    primes = []
    for candidate in raw_numbers:
        prime = True
        for divisor in raw_numbers[:candidate]:
            if candidate % divisor == 0 and candidate != divisor:
                prime = False
                break
        if prime == True:
            primes.append(candidate)
    print(f'numba_human: {primes}')


@time_and_memory
@jit(nopython=True)
def numba_list_sieve(mini: int, maxi: int):
    """
    Uses Numba's JIT compilor to hopefully optimize the 'list_sieve' function

    :param mini: minimum number
    :param maxi: maximum number
    """
    raw_numbers = list(range(mini, maxi))
    for candidate in raw_numbers:
        highest = maxi // candidate
        for divisor in range(candidate, highest + 1):
            multiple = candidate * divisor
            if multiple in raw_numbers:
                raw_numbers.remove(multiple)
    print(f'numba_list_sieve: {raw_numbers}')


@time_and_memory
def numba_smart_human(mini: int, maxi: int):
    """
    Uses Numba's JIT compilor to hopefully optimie the 'smart_human' function
    Numba objects a lot to the string-based processing, 
    so the string and mathmatical functions are factored into subfunctions
    Applies Numba only to the math functions.

    :param mini: minimum number
    :param maxi: maximum number
    """
    def string_check(candidate):
        # stringified = []
        # for digit in str(i):
        #     stringified.append(int(digit))
        prime = True
        stringified = [int(n) for n in str(candidate)]
        if ((stringified[-1] in [2, 4, 5, 6, 8, 0]) or (sum(stringified) % 3 == 0)) and candidate not in [2, 3, 5]:
            prime = False
        return prime
    
    @jit(nopython=True)
    def numba_math(candidate, primes):
        prime = True
        for divisor in primes[1:]:  # looks at only smaller primes, range modified for the fake one
            if candidate % divisor == 0 and candidate != divisor:
                prime = False
                break  # Goes to next number
        if prime:
            primes.append(candidate)  # if prime, then appends to list
        return primes

    raw_numbers = list(range(mini, maxi))
    primes = [100]  # populates one value into the list so numba doesn't get mad
    for candidate in raw_numbers:
        prime = string_check(candidate)
        if not prime:
            pass
        primes = numba_math(candidate, primes)
    primes.pop(0)  # pops the fake number.
        

    print(f'numba_smart_human: {primes}')

