#!/usr/bin/env python

import math

def comb(N, k):
    """
    The number of combinations of N things taken k at a time.
    This is often expressed as "N choose k". Copy from scip.misc.

    Notes
    -----
    - If k > N, N < 0, or k < 0, then 0 is returned.

    """
    N = int(N)
    k = int(k)
    if (k > N) or (N < 0) or (k < 0):
        return 0
    val = 1
    for j in xrange(min(k, N-k)):
        val = (val*(N-j))//(j+1)
    return val

def prob(k, n, K, N):
    """Probility of k successful draws in n tests of a sample with size N and
    a total number K of successes.

    The probability is given by the hypergeometric distribution.
    """
    return comb(K, k) * comb(N-K, n-k) * 1. / comb(N, n)

def probK(k, n, N):
    """Probility of k successful draws in n tests of a sample with size N.
    
    Adds up prob(k, n, K, N) from all K consistent with the given draws.
    The probability is not normalized to unity.
    """
    p = 0
    for K in xrange(k, N-(n-k)+1):
        p += prob(k, n, K, N)
    return p

def probKGivenS(k, n, N, s=0.9):
    """Probility of k successful draws in n tests of a sample with size N,
    whose success rate K/N is larger or equal to s.

    Adds up prob(k, n, K, N) from all K consistent with the given draws and
    the specified success rate K/N >= s. 
    The probability is not normalized to unity.
    """
    S = max(k, int(math.ceil(s*N)))
    p = 0
    for K in xrange(S, N-(n-k)+1):
        p += prob(k, n, K, N)
    return p

def probSGivenK(k, n, N, s=0.9):
    """Probability of the sample success rate >= s, given k sucessful draws 
    in n tests of a sample with size N.

    Uses Bayes Theorem to relate to probKSuccessFrac and probK.
    """
    return probKGivenS(k, n, N, s=s) / probK(k, n, N)

def minSuccessFraction(k, n, N, confidence=0.95, accuracy=0.01):
    """Lower bound on the success fraction in a sample of size N given 
    k successful draws in n tests.

    Searches the largest success fraction s, so that
       probSuccessFracK(k, n, N, s) > confidence

    Args:
       confidence: statistical accuracy of the bound on the success fraction.
          In repeated tests (of length n) of independent samples of size N with
          the same outcome of successful draws k, the number (1 - confidence)
          gives the rate, with which a lower success fraction than the estimated
          lower bound is realized.
       accuracy: precision with which the lower bound on s is found. 
          Note that for finite sample sizes the lower bound estimated here is 
          not a smooth function, so that arbitrarily small accuracy cannot be 
          provided. A reasonable accuracy is of order 1/N.
    """
    # brute-force implementation
    # could be improved by a narrowing down the likely region of s
    # and by only using values of s that lead to changes in probKGivenS.
    s = 1 - accuracy
    pK = probK(k, n, N)
    while s > 0:
        if probKGivenS(k, n, N, s=s) / pK > confidence:
            return s
        s -= accuracy
    return 0

def minTestLength(N, s_limit=0.95, confidence=0.95, accuracy=0.01):
    """Minimum number of tests n to achive a lower limit in the success fraction
    of at least s_limit.

    This test assumes that all test samples are successful, i.e. k=n, and thus
    estimates how many tests are needed to suppress the uncertainty of the 
    whole sample success rate below the threshold 1-s_limit.
    
    Returns -1 if the sample N is not large enough to determine the success rate
    with a certainty of s_limit, before all N samples are tested.
    """
    for n in xrange(1,N):
        if minSuccessFraction(n, n, N, confidence=confidence, accuracy=accuracy) >= s_limit:
            return n
    return -1
        
