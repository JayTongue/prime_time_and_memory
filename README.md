# Prime Time and Memory

This code was written to solve one issue- I wanted to find a way to torture test a new Raspberry Pi 4B and test its computational power. I figured something math heavy, like finding prime numbers in a variable range, was adequately processor-intensive to help me figure out the benchmarks. I figured that what was more interesting than one prime-finding function, would be to try out a few different ones. While I'm at it, I might as well try a few different libraries, including some optimizations with things like Numba's Just-In-Time compiler. Since all these functions are written, why not keep tabs of time and memory use so I can look at time complexity and big-O notation?

The result is this little side project. 
_________________________________________________________
## A. Files
###  sieve_tests.py
This is the primary file which will run functions from the other files. 

### prime_finders.py
A file with the different functions which find prime numbers in a range.

### timer_func.py
Contains the time and memory function, as well as two optional functions for just time or memory. 

_________________________________________________________

## B. Running the Code 
When run, sieve_tests.py will prompt you for a number. This number will be x for a maximum value of $2^x$. Note that each added order of magnitude adds more and more time to the running of the function. 

On a Raspberry Pi 4B with 2gb RAM:

2<sup>12</sup> = 3 minutes, 31 seconds

2<sup>13</sup> = 10 minutes, 27 Seconds

2<sup>14</sup> = 33 minutes, 58 Seconds

2<sup>15</sup> = 1 Hour, 58 Minutes, 24 Seconds

2<sup>16</sup> = 7 hours, 17 minutes, and 26 seconds.


At this point, I considered my Raspberry Pi sufficiently tortured, and I was beginning to wonder if I was more of sadist for doing this to the pi, or a masochist for doing it to myself. At the last order of magnitude in 2<sup>16</sup>, Both "basic_pandas" and "basic_numpy" took over two hours each. Your computer is probably much more powerful than a Raspberry Pi 4B, in which case you can adjust your expectations.

Taking these data points and calculating an exponential line of best fit, roughly follows the equation: y = 9.9758199E-5 * 3.344873325<sup>x</sup>. 
I can assume that, ceteris paribus:

2<sup>19</sup> would take over a week

2<sup>20</sup> would take over a month

2<sup>22</sup> would take over a year

And just for giggles,

2<sup>26</sup> would take longer than the average US life expectancy

2<sup>41</sup> would be past when the sun runs out of hydrogen

2<sup>271</sup> would be a bit past the heat death of the universe

As an aside, my trusty TI-84 kept throwing errors when asked to calculate 1.7 * 10<sup>106</sup> years, which (according to wikipedia) is the estimation for the heat death of the universe. I ended up having to plug it into WolframAlpha, which churned out the answer with no problem. 
_________________________________________________________
## C. Results

The output created by sieve_tests.py is a 3D graph. If you're in Pycharm, you can interact with this graph by unchecking the "Show plots in tool window" checkmark in the settings since the "scientific view" doens't allow the interactivity. In VSCode, my plot was interactive without any change in settings.

This is a screen cap of the 3D graph at 2<sup>16</sup>
![alt text](https://github.com/JayTongue/prime_time_and_memory/blob/main/exhibit/2%5E16.jpg)

These were the results from the last order of magnitude, 2<sup>16</sup>:

| Function         | Time (Seconds)     | Peak Memory (KiB) |
|--------------|-----------|------------|
| human | 430.16      | 3190.704        |
| smart_human      | 54.24  | 2755.648       |
| list_sieve | 215.38 | 2013.544 |
| basic_numpy | 8628.18 | 8627.016 |
| basic_pandas | 7361.04 | 10604.525 | 
| sympy | 1.29 | 350.132 |
| primepy | 0.43 | 350.136 | 
| dijkstra | 95.80 | 1127.634 | 
| numba_human | 11.00 | 1143.6 | 
| numba_smart_human | 2291.24 | 4570.82 | 
| numba_list_sieve | 4.25 | 559.376 |

One thing I noticed is that, especially at lower orders of magnitude, a lot of time the returned time was 0.0000. I know that this isn't literally true, but it might be a limitation in the way the timer wrapper works, or maybe in the fact that the value is so small the computer must round to 0. Either way, I don't belived this skewed the results. 
_____________________________
## D. Discussion and Analysis
While I did not have any hypotheses in making this project (it would take the utmost charity to say I even really designed it), I did have some expectations. Those are discussed here.

### 1. Constant Time Is No Joke
I had learned about big O/Θ/Ω notation before, but this test impressed on me a brand new appreciation for the power of constant time processing. The function that took the longest was basic_numpy, which took over 143 minutes. The fastest was primePy, which managed the same thing in 0.43 seconds. I would say this is 332x faster, but that might imply that primePy could do 332x the work in that basic_numpy could do in the same time, but this is incorrect because, you know, constant time. Both primePy and sympy were random libraries I found online by searching "how to find prime numbers python" or something similar. Apparently, both have been optimized to run in constant time. 

### 2. Pandas and Numpy Are Very Bad At This
I had heard a lot about how Pandas and Numpy were both very powerful libraries which were largely C-optimized. I thought that this meant that using them as a the pd.DataFrame and np.array would therefore be a fast and expedient way of achieving the task at hand. I was sorely mistaken. They both consistently took longer and used more memory at peak than all other functions, sometimes taking an additional order of magnitude than other functions.
Upon reflection, I have found both Pandas and Numpy to be very fast before, but largely at tasks which can be vectorized, such as multiplying one large array by another large array, or processing all data in a given DataFrame column. Both functions, in their "basic" form, still rely on loops to remove numbers one by one. Not only does this negate any inherent advantage of the library's strengths, it exacterbates its weaknesses by forcing it to retrieve its memory objects repeatedly for each loop. 
Pandas and Numpy are still very powerful and may be the best tool for many things, but for the love of everything good, don't use them as a data structure for running the Sieve of Eratosthenes. 

### 3. Dijkstra Is Very Fast and Efficient
At the beginning of this project, I was only aware of two ways of finding prime numbers- trial division and the Sieve of Eratosthenes. These are reflected in the "human" and "list_sieve" functions. I tried to be inventive as I could, using different data structures and optimizations, but I was only fundamentally aware of these two. I then watched this [video](https://www.youtube.com/watch?time_continue=17&v=fwxjMKBMR7s&embeds_referring_euri=https%3A%2F%2Fduckduckgo.com%2F&feature=emb_title) about how Edsger Dijkstra discovered a third way in 1970. As the video explains, trial division is computationally slow, but memory efficient. Conversely, Eratosthenes is fast, but memory-demanding. Dijkstra's approach is sort of "sieve as you go", which promises to optimize neither memory nor time, and ends up somewhere in between with an overall advantage. However, as I have them written, Dijkstra ended up taking about half to a third of the memory of both trial division and Eratosthenes, and was about two to four times faster. I wonder if this is because of the limited memory and processing in my Raspberry Pi, since the video runs what I assume is a similar trial and found that Dijkstra ended in the middle for memory and time.

### 4. Smart_human Can Be Dumb
Smart_human is probably my favorite function in the whole code. It is a reflection of me if I were to try to be "smart" about finding prime numbers. I would look at the number and if it ended in an even number, know immediately that it was multiple of 2, and if not 2 itself, then not prime. Similarly, numbers which end in 5 would be divisible by 5, and numbers ending in 0 would be divisible by both 2 and 5. I would also only use trial division for prime numbers smaller than the square root + 1 of the candidate number since multiples come in pairs and all numbers are either prime numbers or multiples of prime numbers. See how smart I am? To my credit, straight-up smart_human was much faster and memory efficient than plain human. 
Where smart_human got obliterated was when Numba's JIT compiler got involved. After many efforts, the only way to get Numba to work on smart_human was to isolate the string processing function from the math computation function, with Numba's decorator only being applied to the math function. So while numba_human crushed 2<sup>16</sup> in 11 seconds, numba_smart_human took over 38 minutes, much slower than just smart_human by itself. 

### 5. I Never Want To Do My Own Memory Management
I will not elaborate. I will also not do my own memory management. 
_____________________________
## E. Further Development

1. Try to redeem Pandas and Numpy- I'm sure that if I used something like a Boolean array, it would play to the strengths of these data structures, and could probably improve them a lot.
2. Iterate through line styles to make the graph more readable and inlusive.
3. Python vectorization- This code relied a LOT on loops, and this was largely intentional. However, I would like to explore native and pythonic ways of using vectorization.






