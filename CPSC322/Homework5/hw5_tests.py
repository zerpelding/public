"""Unit tests for CPSC 322 HW-5. 

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


#----------------------------------------------------------------------
# knn tests
#----------------------------------------------------------------------

def test_one_row_one_col_knn():
    table = DataTable(['a'])    
    table.append([1])
    # exact match
    instance = DataRow(['a'], [1])
    result = knn(table, instance, 1, ['a'])
    assert len(result) == 1
    assert result[0] == [table[0]]
    # one off
    instance = DataRow(['a'], [2])
    result = knn(table, instance, 1, ['a'])
    assert len(result) == 1
    assert result[1] == [table[0]]
    # one off (other direction)
    instance = DataRow(['a'], [0])
    result = knn(table, instance, 1, ['a'])
    assert len(result) == 1
    assert result[1] == [table[0]]
    # k = 2 still returns one row
    instance = DataRow(['a'], [1])
    result = knn(table, instance, 2, ['a'])
    assert len(result) == 1
    assert result[0] == [table[0]]

    
def test_two_rows_one_col_knn():
    table = DataTable(['a'])
    table.append([1])
    table.append([2])
    # one instance for k=1
    instance = DataRow(['a'], [1])
    result = knn(table, instance, 1, ['a'])
    assert len(result) == 1
    assert result[0] == [table[0]]
    # two instances for k=1
    instance = DataRow(['a'], [1.5])
    result = knn(table, instance, 1, ['a'])
    assert len(result) == 1
    assert len(result[0.25]) == 2
    assert table[0] in result[0.25] and table[1] in result[0.25]
    # two instances for k=2
    instance = DataRow(['a'], [1])
    result = knn(table, instance, 2, ['a'])
    assert len(result) == 2
    assert result[0] == [table[0]]
    assert result[1] == [table[1]]
    
    
def test_two_rows_two_col_knn():
    table = DataTable(['a', 'b'])
    table.append([1, 2])
    table.append([2, 1])
    # one instance for k=1
    instance = DataRow(['a', 'b'], [2, 1])
    result = knn(table, instance, 1, ['a', 'b'])
    assert len(result) == 1
    assert result[0] == [table[1]]
    # two instances for k=1
    instance = DataRow(['a', 'b'], [1.5, 1.5])
    result = knn(table, instance, 1, ['a', 'b'])
    assert len(result) == 1
    assert len(result[0.5]) == 2
    assert table[0] in result[0.5] and table[1] in result[0.5]
    # two instances for k=2
    instance = DataRow(['a', 'b'], [2, 1])
    result = knn(table, instance, 2, ['a', 'b'])    
    assert len(result) == 2
    assert result[0] == [table[1]]
    assert result[2] == [table[0]]
    # one instance for k=2
    instance = DataRow(['a', 'b'], [1, 1])
    result = knn(table, instance, 2, ['a', 'b'])    
    assert len(result) == 1
    assert len(result[1]) == 2
    assert table[0] in result[1] and table[1] in result[1]

    
def test_mult_rows_mult_col_knn():
    table = DataTable(['a', 'b', 'c', 'd'])
    table.append([1, 2, 3, 4])
    table.append([2, 4, 6, 8])
    table.append([1, 3, 5, 7])
    table.append([4, 3, 2, 1])
    table.append([3, 1, 4, 2])
    instance = DataRow(['a', 'b', 'c', 'd'], [1, 3, 3, 4])
    # k = 1
    result = knn(table, instance, 1, table.columns())
    assert len(result) == 1
    assert result[1] == [table[0]]
    # k = 2
    result = knn(table, instance, 2, table.columns())
    assert len(result) == 2
    assert result[1] == [table[0]]
    assert table[2] in result[13] and table[4] in result[13]
    # k = 3
    result = knn(table, instance, 3, table.columns())
    assert len(result) == 3
    print(result.keys())
    assert result[1] == [table[0]]
    assert table[2] in result[13] and table[4] in result[13]
    assert result[19] == [table[3]]
    

def test_nominal_col_knn():
    table = DataTable(['a', 'b'])
    table.append([1, 2])
    table.append([2, 1])
    # one instance for k=1
    instance = DataRow(['a', 'b'], [3, 1])
    result = knn(table, instance, 1, [], ['b'])
    assert len(result) == 1
    assert result[0] == [table[1]]
    # two instances for k=2
    result = knn(table, instance, 2, [], ['b'])
    assert len(result) == 2
    assert result[0] == [table[1]]
    assert result[1] == [table[0]]
    # two instances, one result for k=1
    instance = DataRow(['a', 'b'], [2, 2])
    result = knn(table, instance, 1, [], ['a', 'b'])
    assert len(result) == 1
    assert result[1] == [table[0], table[1]]
    # two instances, two results for k=2
    instance = DataRow(['a', 'b'], [3, 1])
    result = knn(table, instance, 2, [], ['a', 'b'])
    assert len(result) == 2
    assert result[1] == [table[1]]
    assert result[2] == [table[0]]
    

def test_numerical_nominal_knn():
    table = DataTable(['a', 'b', 'c'])
    table.append([1, 2, 'y'])
    table.append([2, 4, 'y'])
    table.append([1, 3, 'n'])
    table.append([4, 3, 'n'])
    table.append([3, 1, 'y'])
    instance = DataRow(['a', 'b', 'c'], [2, 2, 'n'])
    # k = 1
    result = knn(table, instance, 1, ['a', 'b'], ['c'])
    assert len(result) == 1
    assert table[0] in result[2] and table[2] in result[2]
    # k = 2
    result = knn(table, instance, 2, ['a', 'b'], ['c'])
    assert len(result) == 2
    assert table[0] in result[2] and table[2] in result[2]
    assert result[3] == [table[4]]
    # k = 3
    result = knn(table, instance, 3, ['a', 'b'], ['c'])
    assert len(result) == 3
    assert table[0] in result[2] and table[2] in result[2]
    assert result[3] == [table[4]]
    print(result[5])
    assert table[1] in result[5] and table[3] in result[5]

    
#----------------------------------------------------------------------
# majority and weighted vote tests
#----------------------------------------------------------------------
    
def test_majority_vote():
    instances = [DataRow(['a', 'b'], [1, 'x'])]
    assert majority_vote(instances, [], 'b') == ['x']
    instances.append(DataRow(['a', 'b'], [2, 'y']))
    assert set(majority_vote(instances, [], 'b')) == set(['x', 'y'])
    instances.append(DataRow(['a', 'b'], [3, 'z']))
    assert set(majority_vote(instances, [], 'b')) == set(['x', 'y', 'z'])    
    instances.append(DataRow(['a', 'b'], [4, 'x']))
    assert majority_vote(instances, [], 'b') == ['x']    
    instances.append(DataRow(['a', 'b'], [5, 'y']))
    assert set(majority_vote(instances, [], 'b')) == set(['x', 'y'])    

    
def test_weighted_vote():
    instances = [DataRow(['a', 'b'], [1, 'x'])]
    scores = [1]
    assert weighted_vote(instances, scores, 'b') == ['x']
    instances.append(DataRow(['a', 'b'], [2, 'y']))
    scores.append(1)
    assert set(weighted_vote(instances, scores, 'b')) == set(['x', 'y'])
    instances.append(DataRow(['a', 'b'], [3, 'z']))
    scores.append(2)
    assert weighted_vote(instances, scores, 'b') == ['z']
    instances.append(DataRow(['a', 'b'], [1, 'x']))
    scores.append(1)
    assert set(weighted_vote(instances, scores, 'b')) == set(['x', 'z'])
    instances.append(DataRow(['a', 'b'], [2, 'y']))
    scores.append(2)
    assert weighted_vote(instances, scores, 'b') == ['y']

    
#----------------------------------------------------------------------
# holdout tests
#----------------------------------------------------------------------
    
def test_holdout():
    table = DataTable(['a', 'b', 'c'])
    n = 10
    for i in range(n):
        table.append([i, i*10, i*100])
    train, test = holdout(table, 0)
    assert table.row_count() == n
    assert train.row_count() == n
    assert test.row_count() == 0
    train, test = holdout(table, 3)
    assert table.row_count() == n
    assert train.row_count() == n - 3
    assert test.row_count() == 3
    assert duplicate_instances(test).row_count() == 0
    assert duplicate_instances(train).row_count() == 0
    train, test = holdout(table, 7)
    assert table.row_count() == n
    assert train.row_count() == n - 7
    assert test.row_count() == 7
    assert duplicate_instances(test).row_count() == 0
    assert duplicate_instances(train).row_count() == 0
    train, test = holdout(table, n)
    assert table.row_count() == n
    assert train.row_count() == 0
    assert test.row_count() == n
    assert duplicate_instances(test).row_count() == 0
    assert duplicate_instances(train).row_count() == 0

    
#----------------------------------------------------------------------
# accuracy, precision, and recall tests
#----------------------------------------------------------------------

def test_accuracy():
    # two labels
    matrix = DataTable(['actual', 1, 2])
    matrix.append([1, 10, 2])
    matrix.append([2, 4, 12])
    assert accuracy(matrix, 1) == ((10 + 12) / 28)
    assert accuracy(matrix, 2) == ((12 + 10) / 28)
    # three labels
    matrix = DataTable(['actual', 1, 2, 3])
    matrix.append([1, 10,  2, 1])
    matrix.append([2,  4, 12, 3])
    matrix.append([3,  0,  3, 9])
    assert accuracy(matrix, 1) == ((10 + (12 + 3 + 3 + 9)) / 44)
    assert accuracy(matrix, 2) == ((12 + (10 + 1 + 0 + 9)) / 44)    
    assert accuracy(matrix, 3) == ((9 + (10 + 2 + 4 + 12)) / 44)    

    
def test_precision():
    # two labels
    matrix = DataTable(['actual', 1, 2])
    matrix.append([1, 10, 2])
    matrix.append([2, 4, 12])
    assert precision(matrix, 1) == (10 / (10 + 4))
    assert precision(matrix, 2) == (12 / (2 + 12))
    # three labels
    matrix = DataTable(['actual', 1, 2, 3])
    matrix.append([1, 10,  2, 1])
    matrix.append([2,  4, 12, 3])
    matrix.append([3,  0,  3, 9])
    assert precision(matrix, 1) == (10 / (10 + 4 + 0))
    assert precision(matrix, 2) == (12 / (2 + 12 + 3))
    assert precision(matrix, 3) == (9 / (1 + 3 + 9))


def test_recall():
    # two labels
    matrix = DataTable(['actual', 1, 2])
    matrix.append([1, 10, 2])
    matrix.append([2, 4, 12])
    assert recall(matrix, 1) == (10 / (10 + 2))
    assert recall(matrix, 2) == (12 / (4 + 12))
    # three labels
    matrix = DataTable(['actual', 1, 2, 3])
    matrix.append([1, 10,  2, 1])
    matrix.append([2,  4, 12, 3])
    matrix.append([3,  0,  3, 9])
    assert recall(matrix, 1) == (10 / (10 + 2 + 1))
    assert recall(matrix, 2) == (12 / (4 + 12 + 3))
    assert recall(matrix, 3) == (9 / (0 + 3 + 9))

    
#----------------------------------------------------------------------
# normalize and discretize tests
#----------------------------------------------------------------------

def test_normalize():
    table = DataTable(['a', 'b'])
    for i in range(11):
        table.append([1, i])
    normalize(table, 'b')
    for i in range(11):
        assert table[i]['a'] == 1
        assert table[i]['b'] == i / 10

        
def test_discretize():
    table1 = DataTable(['a', 'b'])
    for i in range(10):
        table1.append([1, i])
    # 2 bins
    table2 = table1.copy()
    discretize(table2, 'b', [5])
    for i in range(10):
        assert table2[i]['a'] == 1
        if i < 5:
            assert table2[i]['b'] == 1
        else:
            assert table2[i]['b'] == 2
    # 3 bins
    table2 = table1.copy()
    discretize(table2, 'b', [4, 8])
    for i in range(10):
        assert table2[i]['a'] == 1
        if i < 4:
            assert table2[i]['b'] == 1
        elif i < 8:
            assert table2[i]['b'] == 2
        else:
            assert table2[i]['b'] == 3

    # 4 bins
    table2 = table1.copy()
    discretize(table2, 'b', [2, 5, 7])
    for i in range(10):
        assert table2[i]['a'] == 1
        if i < 2:
            assert table2[i]['b'] == 1
        elif i < 5:
            assert table2[i]['b'] == 2
        elif i < 7:
            assert table2[i]['b'] == 3
        else:
            assert table2[i]['b'] == 4
