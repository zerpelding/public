"""Unit tests for CPSC 322 HW-8. 

Note that these are very basic tests that if passed do not guarantee
correctness of all functions. Instead these tests ensure only a basic
level of functioning.

NAME: S. Bowers
DATE: Fall 2023

"""

import pytest
from data_table import *
from data_learn import *
from data_eval import *
from data_util import *

from math import log


#----------------------------------------------------------------------
# bootstrap and stratified holdout
#----------------------------------------------------------------------

def test_bootstrap():
    table = DataTable(['a', 'b', 'c'])
    train, test = bootstrap(table)
    assert train.column_count() == 3
    assert train.row_count() == 0
    assert test.column_count() == 3
    assert test.row_count() == 0
    table.append([1, 10, 100])
    table.append([2, 20, 200])
    table.append([3, 30, 300])
    table.append([4, 40, 400])
    train, test = bootstrap(table)
    assert train.row_count() == table.row_count()
    for row in train:
        assert row in table
    for row in test:
        assert row in table


def test_stratified_holdout():
    table = DataTable(['a', 'b', 'c'])
    table.append([1, 10, 'y'])
    train, test = stratified_holdout(table, 'c', 0)
    assert train.column_count() == 3
    assert train.row_count() == 1
    assert test.column_count() == 3
    assert test.row_count() == 0
    table.append([2, 20, 'y'])
    train, test = stratified_holdout(table, 'c', 1)
    assert train.row_count() == 1
    assert test.row_count() == 1
    table.append([3, 30, 'n'])
    table.append([4, 40, 'n'])
    train, test = stratified_holdout(table, 'c', 2)
    assert train.row_count() == 2
    assert test.row_count() == 2
    assert set(distinct_values(test, 'c')) == {'y', 'n'}
    table.append([5, 50, 'y'])
    table.append([6, 60, 'y'])
    train, test = stratified_holdout(table, 'c', 3)
    assert train.row_count() == 3
    assert test.row_count() == 3
    assert column_values(test, 'c').count('y') == 2
    assert column_values(test, 'c').count('n') == 1
    table.append([7, 70, 'm'])
    table.append([8, 80, 'm'])
    train, test = stratified_holdout(table, 'c', 4)
    assert train.row_count() == 4
    assert test.row_count() == 4
    assert column_values(test, 'c').count('y') == 2
    assert column_values(test, 'c').count('n') == 1
    assert column_values(test, 'c').count('m') == 1    


#----------------------------------------------------------------------
# random forest
#----------------------------------------------------------------------

def test_random_subset():
    s1 = ['a', 'b', 'c']
    s2 = random_subset(3, s1)
    assert s1 == s2
    s2 = random_subset(2, s1)
    assert len(s2) == 2
    assert s2[0] != s2[1]
    assert s2[0] in s1 and s2[1] in s1
    s2 = random_subset(1, s1)
    assert len(s2) == 1
    assert s2[0] in s1 
    

def test_random_forest():
    table = DataTable(['a', 'b', 'c', 'd'])
    table.append([1, 10, 100, 'y'])
    table.append([1, 20, 100, 'y'])
    table.append([1, 10, 200, 'n'])
    table.append([2, 10, 100, 'y'])
    table.append([2, 20, 200, 'y'])
    table.append([2, 10, 200, 'n'])
    result = random_forest(table, table, 2, 1, 10, 'd', ['a', 'b', 'c'])
    assert len(result) == 1
    result = random_forest(table, table, 2, 2, 10, 'd', ['a', 'b', 'c'])
    assert len(result) == 2
    result = random_forest(table, table, 2, 3, 10, 'd', ['a', 'b', 'c'])
    assert len(result) == 3

#----------------------------------------------------------------------
# k_means
#----------------------------------------------------------------------

def test_closest_centroid():
    table = DataTable(['a', 'b'])
    table.append([1, 1])
    centroids = [table[0]]
    i = closest_centroid(centroids, table[0], ['a', 'b'])
    assert i == 0
    r = DataRow(['a', 'b'], [1, 2])
    i = closest_centroid(centroids, r, ['a', 'b'])
    assert i == 0
    table.append([2, 2])
    centroids = [table[0], table[1]]
    i = closest_centroid(centroids, table[0], ['a', 'b'])
    assert i == 0
    i = closest_centroid(centroids, table[1], ['a', 'b'])    
    assert i == 1
    r = DataRow(['a', 'b'], [3, 3])    
    i = closest_centroid(centroids, r, ['a', 'b'])
    assert i == 1
    r = DataRow(['a', 'b'], [0, 1])    
    i = closest_centroid(centroids, r, ['a', 'b'])
    assert i == 0
    r = DataRow(['a', 'b'], [0, 2])    
    i = closest_centroid(centroids, r, ['a', 'b'])
    assert i == 0

        
def test_select_k_random_centroids():
    table = DataTable(['a', 'b', 'c'])
    centroids = select_k_random_centroids(table, 0)
    assert len(centroids) == 0
    table.append([1, 10, 100])
    table.append([2, 20, 200])
    centroids = select_k_random_centroids(table, 1)
    assert len(centroids) == 1
    assert centroids[0] in table
    centroids = select_k_random_centroids(table, 2)    
    assert len(centroids) == 2
    assert centroids[0] in table
    assert centroids[1] in table
    assert centroids[0] != centroids[1]
    table.append([3, 30, 300])
    centroids = select_k_random_centroids(table, 0)
    assert len(centroids) == 0
    centroids = select_k_random_centroids(table, 1)
    assert len(centroids) == 1
    assert centroids[0] in table
    centroids = select_k_random_centroids(table, 2)
    assert len(centroids) == 2
    assert centroids[0] in table
    assert centroids[1] in table
    assert centroids[0] != centroids[1]
    
    
def test_simple_k_means():
    table = DataTable(['a', 'b'])
    table.append([3, 4])
    table.append([6, 2])
    table.append([2, 1])
    table.append([5, 5])
    centroids = [table[0]]
    clusters = k_means(table, centroids, ['a', 'b'])
    assert len(clusters) == 1
    assert clusters[0].row_count() == 4
    centroids = [table[0], table[1]]
    clusters = k_means(table, centroids, ['a', 'b'])
    assert len(clusters) == 2
    assert clusters[0].row_count() == 3
    assert table[0] in clusters[0]
    assert table[2] in clusters[0]
    assert table[3] in clusters[0]
    assert clusters[1].row_count() == 1
    assert table[1] in clusters[1]
    centroids = [table[1], table[3]]
    clusters = k_means(table, centroids, ['a', 'b'])    
    assert len(clusters) == 2
    assert clusters[0].row_count() == 2
    assert table[1] in clusters[0]
    assert table[2] in clusters[0]
    assert clusters[1].row_count() == 2
    assert table[0] in clusters[1]
    assert table[3] in clusters[1]
    centroids = [table[0], table[1], table[2]]
    clusters = k_means(table, centroids, ['a', 'b'])
    assert len(clusters) == 3
    assert clusters[0].row_count() == 2
    assert table[0] in clusters[0]
    assert table[3] in clusters[0]
    assert clusters[1].row_count() == 1
    assert table[1] in clusters[1]
    assert clusters[2].row_count() == 1
    assert table[2] in clusters[2]

    
def test_two_rounds_k_means():    
    table = DataTable(['a', 'b'])
    table.append([1, 4])
    table.append([1, 5])    
    table.append([2, 2])
    table.append([2, 4])    
    table.append([2, 6])
    table.append([3, 1])    
    table.append([3, 2])
    table.append([4, 2])    
    table.append([4, 4])
    table.append([6, 1])    
    centroids = [table[2], table[6]]
    clusters = k_means(table, centroids, ['a', 'b'])
    assert len(clusters) == 2
    assert clusters[0].row_count() == 4
    assert table[0] in clusters[0]
    assert table[1] in clusters[0]
    assert table[3] in clusters[0]
    assert table[4] in clusters[0]    
    assert clusters[1].row_count() == 6
    assert table[2] in clusters[1]
    assert table[5] in clusters[1]
    assert table[6] in clusters[1]
    assert table[7] in clusters[1]    
    assert table[8] in clusters[1]
    assert table[9] in clusters[1]        
                       

def test_tss():
    result = tss([], [])
    assert len(result) == 0
    c1 = DataTable(['a', 'b', 'c'])
    c1.append([1, 1, 1])
    result = tss([c1], ['a', 'b', 'c'])
    assert len(result) == 1
    assert result == [0]
    c2 = DataTable(['a', 'b', 'c'])
    c2.append([5, 5, 5])
    result = tss([c1, c2], ['a', 'b', 'c'])
    assert len(result) == 2
    assert result == [0, 0]
    c1.append([3, 3, 3])
    result = tss([c1, c2], ['a', 'b', 'c'])
    assert len(result) == 2
    assert result == [6, 0]
    c2.append([5, 7, 5])
    result = tss([c1, c2], ['a', 'b', 'c'])
    assert len(result) == 2
    assert result == [6, 2]
    
