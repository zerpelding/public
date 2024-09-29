"""Unit tests for CPSC 322 HW-4. 

Note that these are very basic tests that if passed do not guarantee
correctness of all functions. Instead these tests ensure only a basic
level of functioning.

NAME: S. Bowers
DATE: Fall 2023

"""

from math import sqrt
import pytest
from data_util import *
from data_table import *


def test_column_values():
    t1 = DataTable(['a', 'b'])    
    assert [] == column_values(t1, 'a')
    assert [] == column_values(t1, 'b')
    t1.append([1, 10])
    assert [1] == column_values(t1, 'a')
    assert [10] == column_values(t1, 'b')
    t1.append([4, 60])
    assert [1,4] == column_values(t1, 'a')
    assert [10,60] == column_values(t1, 'b')
    

def test_mean():
    t1 = DataTable(['a', 'b'])
    t1.append([1, 2])
    assert 1 == mean(t1, 'a')
    assert 2 == mean(t1, 'b')
    t1.append([3, 1])
    assert 2 == mean(t1, 'a')
    assert 1.5 == mean(t1, 'b')
    t1.append([1, 1])
    assert 5/3 == mean(t1, 'a')
    assert 4/3 == mean(t1, 'b')

    
def test_variance():
    t1 = DataTable(['a', 'b'])
    t1.append([1, 2])
    assert 0 == variance(t1, 'a')
    assert 0 == variance(t1, 'b')
    t1.append([2, 3])
    assert 0.25 == variance(t1, 'a')
    assert 0.25 == variance(t1, 'b')
    t1.append([3, 4])
    assert 2/3 == variance(t1, 'a')
    assert 2/3 == variance(t1, 'b')


def test_std_dev():
    t1 = DataTable(['a', 'b'])
    t1.append([1, 2])
    assert 0 == std_dev(t1, 'a')
    assert 0 == std_dev(t1, 'b')
    t1.append([2, 3])
    assert sqrt(0.25) == std_dev(t1, 'a')
    assert sqrt(0.25) == std_dev(t1, 'b')
    t1.append([3, 4])
    assert sqrt(2/3) == std_dev(t1, 'a')
    assert sqrt(2/3) == std_dev(t1, 'b')

    
def test_covariance():
    t1 = DataTable(['a', 'b'])
    t1.append([1, 2])
    assert 0 == covariance(t1, 'a', 'b')
    t1.append([2, 3])
    assert 0.25 == covariance(t1, 'a', 'b')
    t1.append([3, 4])
    assert 2/3 == covariance(t1, 'a', 'b')

    
def test_linear_regression():
    t1 = DataTable(['a', 'b', 'c', 'd'])
    t1.append([1, 1, 2, 7])
    t1.append([2, 2, 4, 4])
    t1.append([3, 3, 6, 1])
    m, b = linear_regression(t1, 'a', 'b')
    assert 1 == m and 0 == b
    m, b = linear_regression(t1, 'a', 'c')
    assert 2 == m and b == 0
    m, b = linear_regression(t1, 'b', 'd')    
    assert -3 == m and b == 10
    t1 = DataTable(['a', 'b'])
    t1.append([1, 1])
    t1.append([2, 2])
    t1.append([3, 3])
    t1.append([1, 3])
    t1.append([2, 4])
    t1.append([3, 5])
    m, b = linear_regression(t1, 'a', 'b')
    assert m == 1 and b == 1

    
def test_correlation_coefficient():
    t1 = DataTable(['a', 'b'])
    t1.append([1, 1])
    t1.append([2, 2])
    t1.append([3, 3])
    r = correlation_coefficient(t1, 'a', 'b')
    assert r == 1
    t1 = DataTable(['a', 'b'])
    t1.append([1, 3])
    t1.append([2, 2])
    t1.append([3, 1])
    r = correlation_coefficient(t1, 'a', 'b')    
    assert r == -1
    t1 = DataTable(['a', 'b'])
    t1.append([1, 1])
    t1.append([2, 2])
    t1.append([3, 3])
    t1.append([1, 3])
    t1.append([2, 4])
    t1.append([3, 5])
    r = correlation_coefficient(t1, 'a', 'b')
    assert round(2 / (3 * sqrt(10/9)), 2) == round(r, 2)

    
def test_frequency_of_range():
    t1 = DataTable(['a', 'b', 'c'])
    assert 0 == frequency_of_range(t1, 'a', 0, 10)
    t1.append([1, 10, 100])
    assert 1 == frequency_of_range(t1, 'a', 1, 2)
    assert 1 == frequency_of_range(t1, 'a', 0, 2)
    assert 0 == frequency_of_range(t1, 'a', 0, 1)
    t1.append([1, 12, 200])
    assert 2 == frequency_of_range(t1, 'a', 0, 2)
    assert 1 == frequency_of_range(t1, 'b', 11, 15)
    assert 0 == frequency_of_range(t1, 'c', 0, 100)
    t1.append([5, 15, 300])
    assert 3 == frequency_of_range(t1, 'a', 0, 10)
    assert 2 == frequency_of_range(t1, 'b', 11, 16)
    assert 1 == frequency_of_range(t1, 'c', 100, 200)



