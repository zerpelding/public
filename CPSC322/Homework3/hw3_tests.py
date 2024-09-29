"""Unit tests for CPSC 322 HW-3. 

Note that these are very basic tests that if passed do not guarantee
correctness of all functions. Instead these tests ensure only a basic
level of functioning.

NAME: S. Bowers
DATE: Fall 2023

"""


import pytest
from data_util import *
from data_table import *


def test_drop_columns():
    t1 = DataTable(['a', 'b', 'c'])
    t1.drop(['b'])
    assert t1.columns() == ['a', 'c']
    t1 = DataTable(['a', 'b', 'c'])
    t1.drop(['a', 'c'])
    assert t1.columns() == ['b']
    t1 = DataTable(['a', 'b', 'c'])
    t1.append([1, 2, 3])
    t1.append([4, 5, 6])
    t1.drop(['c'])
    assert t1.columns() == ['a', 'b']
    assert t1[0].values() == [1, 2]
    assert t1[1].values() == [4, 5]
    t1 = DataTable(['a', 'b', 'c'])
    t1.append([1, 2, 3])
    t1.append([4, 5, 6])
    t1.drop(['a', 'b'])
    assert t1.columns() == ['c']
    assert t1[0].values() == [3]
    assert t1[1].values() == [6]
    t1 = DataTable(['a', 'b', 'c'])
    t1.append([1, 2, 3])
    t1.append([4, 5, 6])
    t1.drop(['a', 'b', 'c'])
    assert t1.columns() == []
    assert t1[0].values() == []
    assert t1[1].values() == []

    
    
def test_distinct_values():
    t1 = DataTable(['a', 'b'])
    v1 = distinct_values(t1, 'a')
    assert v1 == []
    t1.append([1, 2])
    v1 = distinct_values(t1, 'a')
    assert v1 == [1]
    v1 = distinct_values(t1, 'b')
    assert v1 == [2]
    t1.append([1, 3])
    v1 = distinct_values(t1, 'a')
    assert v1 == [1]
    v1 = distinct_values(t1, 'b')
    assert v1 == [2, 3]
    t1.append([2, 4])
    v1 = distinct_values(t1, 'a')
    assert v1 == [1, 2]
    v1 = distinct_values(t1, 'b')
    assert v1 == [2, 3, 4]

    
    
def test_remove_missing():
    t1 = DataTable(['a', 'b', 'c', 'd'])
    assert t1.row_count() == 0
    t2 = remove_missing(t1, ['b'])
    assert t2.row_count() == 0
    t1.append(['1', '2', 3.14, True])
    t1.append(['' , 1, 2, '4'])
    t1.append([0, '', 2, '4'])
    t1.append([0, 1, '', '4'])
    assert t1.row_count() == 4
    t2 = remove_missing(t1, ['a'])
    assert t2.row_count() == 3
    rows = [row.values() for row in t2]
    assert ['1', '2', 3.14, True] in rows
    assert [0, '', 2, '4'] in rows
    assert [0, 1, '', '4'] in rows
    t2 = remove_missing(t2, ['b'])
    assert t2.row_count() == 2
    rows = [row.values() for row in t2]    
    assert ['1', '2', 3.14, True] in rows
    assert [0, 1, '', '4'] in rows
    t2 = remove_missing(t2, ['c'])
    assert t2.row_count() == 1
    rows = [row.values() for row in t2]    
    assert ['1', '2', 3.14, True] in rows


    
def test_duplicate_instances():
    t1 = DataTable(['a','b','c'])
    t2 = duplicate_instances(t1)
    assert t2.row_count() == 0
    t1.append([1, 2, 3])
    t2 = duplicate_instances(t1)
    assert t2.row_count() == 0
    t1.append([1, 2, 3])
    t2 = duplicate_instances(t1)
    assert t2.row_count() == 1
    assert t2[0].values() == [1, 2, 3]
    t1.append([4, 5, 6])
    t2 = duplicate_instances(t1)
    assert t2.row_count() == 1
    assert t2[0].values() == [1, 2, 3]
    t1.append([1, 2, 3])
    t2 = duplicate_instances(t1)
    assert t2.row_count() == 1
    assert t2[0].values() == [1, 2, 3]
    t1.append([4, 5, 6])
    t2 = duplicate_instances(t1)
    assert t2.row_count() == 2
    r1 = t2[0].values()
    r2 = t2[1].values()
    assert r1 == [1,2,3] and r2 == [4,5,6] or r1 == [4,5,6] and r2 == [1,2,3]
    

    
def test_remove_duplicates():
    t1 = DataTable(['a', 'b', 'c'])
    t2 = remove_duplicates(t1)
    assert t1.row_count() == t2.row_count()
    t1.append([1, 2, 3])
    t1.append([4, 5, 6])
    t2 = remove_duplicates(t1)
    assert t1.row_count() == t2.row_count()
    t1.append([1, 2, 3])
    t2 = remove_duplicates(t1)
    assert t1.row_count() == (t2.row_count() + 1)
    t1.append([4, 5, 6])
    t2 = remove_duplicates(t1)    
    assert t1.row_count() == (t2.row_count() + 2)


    
def test_partition():
    t1 = DataTable(['a', 'b', 'c'])
    p = partition(t1, ['a'])
    assert len(p) == 0
    t1.append([1, 2, 3])
    p = partition(t1, ['a'])
    assert len(p) == 1 and p[0].row_count() == 1
    t1.append([1, 4, 5])
    p = partition(t1, ['a'])
    assert len(p) == 1 and p[0].row_count() == 2
    t1.append([2, 2, 3])
    p = partition(t1, ['b', 'c'])
    c1, c2 = p[0].row_count(), p[1].row_count()
    assert len(p) == 2 and (c1 == 1 and c2 == 2) or (c1 == 2 and c2 == 1)


    
def test_summary_stat():
    avg = lambda xs : None if not len(xs) else sum(xs) / len(xs)
    t1 = DataTable(['a', 'b'])
    r1 = summary_stat(t1, 'a', avg)
    assert r1 is None
    t1.append([1, 2])
    r1 = summary_stat(t1, 'a', avg)
    assert r1 == 1
    t1.append([3, 4])
    r1 = summary_stat(t1, 'a', avg)    
    assert r1 == 2
    r2 = summary_stat(t1, 'b', avg)
    assert r2 == 3
    

    
def test_replace_missing():
    avg = lambda xs : None if not len(xs) else sum(xs) / len(xs)
    t1 = DataTable(['a', 'b', 'c'])
    t1.append([1, 1, 1])
    t1.append([1, '', 1])
    t1.append([1, 3, 2])
    t1.append([1, '', 2])
    t1.append([2, 4, 2])
    t2 = replace_missing(t1, 'b', ['a'], avg)
    assert id(t1) != id(t2)
    assert t2.row_count() == t1.row_count()
    assert t2[1]['b'] == 2
    assert t2[3]['b'] == 2
    t2 = replace_missing(t1, 'b', ['a', 'c'], avg)
    assert id(t1) != id(t2)
    assert t2.row_count() == t1.row_count()
    assert t2[1]['b'] == 1
    assert t2[3]['b'] == 3


    
def test_summary_stat_by_column():
    t1 = DataTable(['a', 'b', 'c'])
    g1, s1 = summary_stat_by_column(t1, 'b', 'a', max)
    assert g1 == [] and s1 == []
    t1.append([10, 2, 30])
    g1, s1 = summary_stat_by_column(t1, 'b', 'a', max)
    assert g1 == [2] and s1 == [10]
    t1.append([20, 2, 40])
    t1.append([30, 3, 30])
    g1, s1 = summary_stat_by_column(t1, 'b', 'a', max)    
    assert g1 == [2, 3] and s1 == [20, 30] or g1 == [3, 2] and s1 == [30, 20]
    g1, s1 = summary_stat_by_column(t1, 'c', 'b', min)        
    assert (g1 == [30, 40] or g1 == [40, 30]) and s1 == [2, 2]


    
def test_frequencies():
    t1 = DataTable(['a', 'b', 'c'])
    g1, s1 = frequencies(t1, 'b')
    assert g1 == [] and s1 == []
    t1.append([10, 2, 30])
    g1, s1 = frequencies(t1, 'b')
    assert g1 == [2] and s1 == [1]
    t1.append([20, 2, 30])
    g1, s1 = frequencies(t1, 'b')
    assert g1 == [2] and s1 == [2]
    t1.append([20, 3, 30])
    g1, s1 = frequencies(t1, 'b')
    assert g1 == [2, 3] and s1 == [2, 1] or g1 == [3, 2] and s1 == [1, 2]
    g1, s1 = frequencies(t1, 'c')    
    assert g1 == [30] and s1 == [3]
    g1, s1 = frequencies(t1, 'a')    
    assert g1 == [10, 20] and s1 == [1, 2] or g1 == [20, 10] and s1 == [2, 1]
    
