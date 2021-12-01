from typing import List
from functools import reduce
from math import gcd

# Redundant stuff from when I thought there had to be some optimal approach using prime numbers day 13 pt2.

def prime_factors_foreach_in_list(l: List[int]):
    "Return a tuple containing the prime factor for all values in a list"
    return tuple(a for b in [prime_factors(x) for x in l] for a in b)


def reduce_mul_zero_skip(l):
    """Multiply values in a list skipping zeros"""
    l = tuple(l for l in l if l != 0)
    return reduce(lambda x, y: x * y, l)


def reduce_greatest_common_divisor(l):
    """Recursively apply greatest common divisor on the first two entries on a list until a single value remains"""
    l = tuple(l for l in l if l != 0)
    return reduce(lambda x, y: gcd(x, y), l)


def phi(primes: List[int]):
    primes_mul = reduce_mul_zero_skip(primes)
    return reduce_mul_zero_skip(p - 1 for p in primes_mul)


def euler(l):
    l = tuple(l for l in l if l != 0)
    return reduce(lambda x, y: prime_factors(y))


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def largest_prime_factor(n):
    """Find largest prime factor"""
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
    return n


def prime_factors(n: int):
    """Return all prime factors for an integer"""
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def prime_factors_intersect(a: List[int], b: List[int], mode: str):
    """
    Return the intersection of a the prime factors of two lists of integers if it contains a single value,
     otherwise throw exception
     """
    intersection_of_prime_factors = set(prime_factors_foreach_in_list(a)).intersection(
        set(prime_factors_foreach_in_list(b)))
    if mode == 'min':
        return min(intersection_of_prime_factors)
    elif mode == 'max':
        return max(intersection_of_prime_factors)
    else:
        raise ValueError(f"Invalid mode {mode}. Valid: 'min', 'max'.")