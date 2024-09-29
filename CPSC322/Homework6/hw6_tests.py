"""Unit tests for CPSC 322 HW-6. 

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
# naive bayes tests
#----------------------------------------------------------------------

def test_simple_categorical_one_col_cases_naive_bayes():
    table = DataTable(['a', 'b'])
    # one row tests
    table.append([1, 'y'])
    pred = naive_bayes(table, DataRow(['a'], [1]), 'b', [], ['a'])
    assert pred == (['y'], 1.0)
    pred = naive_bayes(table, DataRow(['a'], [2]), 'b', [], ['a'])
    assert pred == (['y'], 0.0)
    # two row tests
    table.append([2, 'n'])
    pred = naive_bayes(table, DataRow(['a'], [1]), 'b', [], ['a'])
    assert pred == (['y'], 0.5)
    pred = naive_bayes(table, DataRow(['a'], [2]), 'b', [], ['a'])
    assert pred == (['n'], 0.5)
    # three row tests
    table.append([1, 'y'])
    pred = naive_bayes(table, DataRow(['a'], [1]), 'b', [], ['a'])
    assert pred == (['y'], 2/3)
    pred = naive_bayes(table, DataRow(['a'], [2]), 'b', [], ['a'])    
    assert pred == (['n'], 1/3)
    # four row tests
    table.append([2, 'y'])
    pred = naive_bayes(table, DataRow(['a'], [1]), 'b', [], ['a'])
    assert pred == (['y'], 0.5)
    pred = naive_bayes(table, DataRow(['a'], [2]), 'b', [], ['a'])
    assert set(pred[0]) == {'y','n'} and pred[1] == 0.25


def test_simple_categorical_two_col_cases_naive_bayes():
    table = DataTable(['a','b','c'])
    # one row tests
    table.append([1, 1, 'y'])
    pred = naive_bayes(table, DataRow(['a', 'b'], [1, 1]), 'c', [], ['a', 'b'])
    assert pred == (['y'], 1.0)
    pred = naive_bayes(table, DataRow(['a', 'b'], [1, 2]), 'c', [], ['a', 'b'])
    assert pred == (['y'], 0.0)    
    pred = naive_bayes(table, DataRow(['a', 'b'], [2, 1]), 'c', [], ['a', 'b'])
    assert pred == (['y'], 0.0)    
    # two row tests
    table.append([2, 2, 'n'])    
    pred = naive_bayes(table, DataRow(['a', 'b'], [1, 1]), 'c', [], ['a', 'b'])
    assert pred == (['y'], 0.5)
    pred = naive_bayes(table, DataRow(['a', 'b'], [2, 2]), 'c', [], ['a', 'b'])
    assert pred == (['n'], 0.5)    
    pred = naive_bayes(table, DataRow(['a', 'b'], [1, 2]), 'c', [], ['a', 'b'])    
    assert set(pred[0]) == {'y','n'} and pred[1] == 0.0
    # three row tests
    table.append([1, 2, 'y'])
    pred = naive_bayes(table, DataRow(['a', 'b'], [1, 1]), 'c', [], ['a', 'b'])
    assert pred == (['y'], 1/3)
    pred = naive_bayes(table, DataRow(['a', 'b'], [2, 2]), 'c', [], ['a', 'b'])
    assert pred == (['n'], 1/3)
    pred = naive_bayes(table, DataRow(['a', 'b'], [2, 1]), 'c', [], ['a', 'b'])    
    assert set(pred[0]) == {'y','n'} and pred[1] == 0.0
    # four row tests
    table.append([2, 1, 'y'])    
    pred = naive_bayes(table, DataRow(['a', 'b'], [1, 1]), 'c', [], ['a', 'b'])
    assert pred == (['y'], 1/3)    
    pred = naive_bayes(table, DataRow(['a', 'b'], [2, 2]), 'c', [], ['a', 'b'])    
    assert pred == (['n'], 1/4)
    pred = naive_bayes(table, DataRow(['a', 'b'], [2, 1]), 'c', [], ['a', 'b'])        
    assert pred == (['y'], 1/6)        
    # five row tests
    table.append([3, 3, 'm'])
    pred = naive_bayes(table, DataRow(['a', 'b'], [3, 3]), 'c', [], ['a', 'b'])            
    assert pred == (['m'], (1/5))


def test_gaussian_density():
    stp = math.sqrt(2 * math.pi)
    assert gaussian_density(1, 1, 1) == 1 / stp
    assert gaussian_density(2, 1, 1) == (1 / stp) * (math.e ** -0.5)
    assert gaussian_density(2, 2, 2) == 1 / (2 * stp)
    assert gaussian_density(2, 3, 2) == (1 / (2 * stp)) * (math.e ** -(1/8))
    
    
def test_simple_continuous_naive_bayes():
    table = DataTable(['a', 'b'])
    table.append([1, 'y'])
    table.append([2, 'y'])
    table.append([3, 'y'])
    pred = naive_bayes(table, DataRow(['a'], [2]), 'b', ['a'], [])
    std = std_dev(table, 'a')
    assert pred[0] == ['y'] and pred[1] == gaussian_density(2, 2, std)
    table.append([10, 'n'])
    table.append([14, 'n'])
    pred = naive_bayes(table, DataRow(['a'], [12.5]), 'b', ['a'], [])
    print(pred)
    assert pred[0] == ['n'] and pred[1] == (gaussian_density(12.5, 12.0, 2.0) * (2/5))

    
#----------------------------------------------------------------------
# stratified cross validation tests
#----------------------------------------------------------------------

def test_simple_stratify():
    table = DataTable(['a', 'b', 'c'])
    # one row, one fold
    table.append([1, 1, 1])
    result = stratify(table, 'b', 1)
    assert len(result) == 1
    assert result[0].row_count() == 1
    assert result[0][0].values() == [1, 1, 1]
    # one row, two folds
    result = stratify(table, 'b', 2)
    assert len(result) == 2
    assert result[0].row_count() == 1
    assert result[1].row_count() == 0
    assert result[0][0].values() == [1, 1, 1]    
    # two rows, one fold
    table.append([2, 1, 2])
    result = stratify(table, 'b', 1)
    assert len(result) == 1
    assert result[0].row_count() == 2
    assert result[0][0].values() == [1, 1, 1]
    assert result[0][1].values() == [2, 1, 2]
    # two rows, two folds
    result = stratify(table, 'b', 2)
    assert len(result) == 2
    assert result[0].row_count() == 1
    assert result[1].row_count() == 1
    assert result[0][0].values() == [1, 1, 1]
    assert result[1][0].values() == [2, 1, 2]    
    # three rows, two folds
    table.append([3, 2, 3])
    result = stratify(table, 'b', 2)
    assert len(result) == 2
    assert result[0].row_count() == 2
    assert result[1].row_count() == 1
    assert result[0][0].values() == [1, 1, 1]
    assert result[1][0].values() == [2, 1, 2]
    assert result[0][1].values() == [3, 2, 3]
    # three rows, three folds
    result = stratify(table, 'b', 3)
    assert len(result) == 3
    assert result[0].row_count() == 2
    assert result[1].row_count() == 1
    assert result[2].row_count() == 0
    assert result[0][0].values() == [1, 1, 1]
    assert result[1][0].values() == [2, 1, 2]
    assert result[0][1].values() == [3, 2, 3]

    
def test_more_involved_stratify():
    table = DataTable(['a', 'b', 'c'])
    for i in range(17):
        table.append([0, (i % 3) + 1, 0])
    print(table)
    result = stratify(table, 'b', 2)
    assert len(result) == 2
    assert result[0].row_count() == 9
    assert result[1].row_count() == 8
    assert sum(1 if r['b']==1 else 0 for r in result[0]) == 3
    assert sum(1 if r['b']==2 else 0 for r in result[0]) == 3
    assert sum(1 if r['b']==3 else 0 for r in result[0]) == 3
    assert sum(1 if r['b']==1 else 0 for r in result[1]) == 3
    assert sum(1 if r['b']==2 else 0 for r in result[1]) == 3
    assert sum(1 if r['b']==3 else 0 for r in result[1]) == 2
    result = stratify(table, 'b', 3)
    assert len(result) == 3
    assert result[0].row_count() == 6
    assert result[1].row_count() == 6
    assert result[2].row_count() == 5
    assert sum(1 if r['b']==1 else 0 for r in result[0]) == 2
    assert sum(1 if r['b']==2 else 0 for r in result[0]) == 2
    assert sum(1 if r['b']==3 else 0 for r in result[0]) == 2
    assert sum(1 if r['b']==1 else 0 for r in result[1]) == 2
    assert sum(1 if r['b']==2 else 0 for r in result[1]) == 2
    assert sum(1 if r['b']==3 else 0 for r in result[1]) == 2
    assert sum(1 if r['b']==1 else 0 for r in result[2]) == 2
    assert sum(1 if r['b']==2 else 0 for r in result[2]) == 2
    assert sum(1 if r['b']==3 else 0 for r in result[2]) == 1
    result = stratify(table, 'b', 4)
    assert len(result) == 4
    assert result[0].row_count() == 6
    assert result[1].row_count() == 5
    assert result[2].row_count() == 3
    assert result[3].row_count() == 3    
    assert sum(1 if r['b']==1 else 0 for r in result[0]) == 2
    assert sum(1 if r['b']==2 else 0 for r in result[0]) == 2
    assert sum(1 if r['b']==3 else 0 for r in result[0]) == 2
    assert sum(1 if r['b']==1 else 0 for r in result[1]) == 2
    assert sum(1 if r['b']==2 else 0 for r in result[1]) == 2
    assert sum(1 if r['b']==3 else 0 for r in result[1]) == 1
    assert sum(1 if r['b']==1 else 0 for r in result[2]) == 1
    assert sum(1 if r['b']==2 else 0 for r in result[2]) == 1
    assert sum(1 if r['b']==3 else 0 for r in result[2]) == 1
    assert sum(1 if r['b']==1 else 0 for r in result[3]) == 1
    assert sum(1 if r['b']==2 else 0 for r in result[3]) == 1
    assert sum(1 if r['b']==3 else 0 for r in result[3]) == 1


def test_union_all():
    table1 = DataTable(['a', 'b', 'c'])
    table2 = DataTable(['a', 'b', 'c'])
    table3 = DataTable(['a', 'b', 'c'])
    result = union_all([table1, table2, table3])
    assert result.columns() == ['a', 'b', 'c']
    assert result.row_count() == 0
    table1.append([1, 1, 1])
    table2.append([2, 2, 2])
    table3.append([3, 3, 3])
    result = union_all([table1, table2, table3])
    assert result.columns() == ['a', 'b', 'c']
    assert result.row_count() == 3
    assert result[0].values() == [1, 1, 1]
    assert result[1].values() == [2, 2, 2]    
    assert result[2].values() == [3, 3, 3]
    table2.append([1, 1, 1])
    table3.append([1, 1, 1])
    result = union_all([table1, table2, table3])
    assert result.columns() == ['a', 'b', 'c']
    assert result.row_count() == 5
    assert result[0].values() == [1, 1, 1]
    assert result[1].values() == [2, 2, 2]    
    assert result[2].values() == [1, 1, 1]
    assert result[3].values() == [3, 3, 3]
    assert result[2].values() == [1, 1, 1]    
    result = union_all([table1])
    assert result.columns() == ['a', 'b', 'c']
    assert result.row_count() == 1
    assert result[0].values() == [1, 1, 1]

    
def test_bad_union_all():
    # no tables to union
    with pytest.raises(ValueError) as e:
        result = union_all([])
    # mismatched column names
    table1 = DataTable(['a', 'b', 'c'])
    table2 = DataTable(['b', 'a', 'c'])
    with pytest.raises(ValueError) as e:
        result = union_all([table1, table2])
    # mismatched number of columns
    table2 = DataTable(['a', 'b'])
    with pytest.raises(ValueError) as e:
        result = union_all([table1, table2])