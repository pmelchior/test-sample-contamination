test-sample-contamination
=========================

The python code allows to estimate the contamination of a sample from a limited set of tests. As a simple extension, you can also find out the minimum number of tests to be performed to determine (with any given confidence) that the actual sample contamination rate is below a desired threshold.

These functions should be useful in the context of quality control tests, specifically with small sample sizes. For details, please see the [documentation](doc/test_sample_contamination.pdf). I do not claim (nor do I believe) that the derivation is at all novel, but I haven't found this functionality anywhere. Feel free to use and share.

### Example usage

Image you have a batch of N=100 eggs (of unknown origin) and you want to estimate how many of them are spoiled. So you start testing a certain number of them, say n=10. Of these k=8 are OK. What is the upper bound of the fraction of spoiled eggs in the batch? To make sure the estimate is halfways trustworthy, let's ask for a 95% confidence in the upper bound.

```python
from test_sample_contamination import *

N, n, k = 100, 10, 8
print 1 - minSuccessFraction(k, n, N, confidence=0.95)
```

We've asked for the lower bound on the success fraction, i.e. the fraction of eggs that are OK. Then, `1 - minSuccessFraction` gives the upper bound on the contamination fraction. The outcome is a worrisome upper limit of 46%. That's substantially larger than the naive estimate of 1 - k/n = 20%. The discrepancy stems from the uncertainty of having tested only 10 eggs, which leaves 90 untested, and our requirement of a 95% confidence level. Still, I wouldn't use these eggs... 

Let's say from the n=10 tests you've done, all are OK, i.e. n=k=10. Then, the maximum contamination is below 22% at 95% confidence. Somewhat better. How many eggs would you need to test (as OK) so that this limit is below, say, 5%?

```python
s_min = 1 - 0.05
print minTestLength(N, s_min=s_min, confidence=0.95)
```

The answer is 38. 
