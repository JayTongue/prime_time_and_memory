# prime_time_and_memory

This code was written to solve one issue- I wanted to find a way to torture test a new Raspberry Pi 4B. I figured something math heavy, like finding prime numbers in a variable range, was adequately processor-intensive to help me figure out the benchmarks. I figured that what was more interesting than one prime-finding function, would be to try out a few different ones. While I'm at it, I might as well try a few different libraries, including some optimizations with things like Numba's Just-In-Time compiler. Since all these functions are written, why not keep tabs of time and memory use so I can look at time complexity and big-O notation?

The result is this little side project. 
_________________________________________________________
##  sieve_tests.py
This is the primary file which will run functions from the other files. 

## prime_finders.py
A file with the different functions which find prime numbers in a range.

## timer_func.py
Contains the time and memory function, as well as two optional functions for just time or memory. 

_________________________________________________________

## instructions
When run, sieve_tests.py will prompt you for a number. This number will be x for a maximum value of 2^x. Note that each added order of magnitude adds more and more time to the running of the function. 

On a Raspberry Pi 4B with 2gb RAM:
2 ^ 14  
2 ^ 15 
2 ^ 16 
2 ^ 17

_________________________________________________________
## Output

The output created by sieve_tests.py is a 3D graph. If you're in Pycharm, you can interact with this graph by unchecking the "Show plots in tool window" checkmark in the settings. In VSCode, my plot was interactive wtihout any change in settings. 
