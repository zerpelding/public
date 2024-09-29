"""Unit tests for CPSC 322 HW-2. 

Note that these are very basic tests that if passed do not guarantee
correctness of all functions. Instead these tests ensure only a basic
level of functioning.

NAME: S. Bowers
DATE: Fall 2023

"""


import pytest
import os
from data_table import *


#----------------------------------------------------------------------
# Data Row tests
#----------------------------------------------------------------------

def test_init_empty_row():
    r1 = DataRow()
    assert r1.columns() == []
    assert r1.values() == []
    r2 = DataRow([], [])
    assert r1.columns() == []
    assert r1.values() == []

    
def test_init_one_item_row():
    r1 = DataRow(['a'], [42])
    assert r1.columns() == ['a']
    assert r1.values() == [42]

    
def test_init_two_item_row():
    r1 = DataRow(['a', 'b'], [42, 24])
    assert r1.columns() == ['a', 'b']
    assert r1.values() == [42, 24]

    
def test_bad_columns_init_row():
    with pytest.raises(ValueError) as e:
        r1 = DataRow(['a','b','a'], [0, 1, 2])
    with pytest.raises(ValueError) as e:
        r1 = DataRow(['a','b'], [0, 1, 2])        

        
def test_row_get_item():
    r1 = DataRow(['a', 'b'], [10, 20])
    assert r1['a'] == 10
    assert r1['b'] == 20

    
def test_bad_row_get_item():
    r1 = DataRow(['a', 'b'], [10, 20])
    with pytest.raises(IndexError) as e:
        r1['c']

        
def test_row_set_item():
    r1 = DataRow(['a', 'b'], [10, 20])
    r1['a'] = 30
    assert r1['a'] == 30
    assert r1['b'] == 20
    r1['b'] = 10
    assert r1['a'] == 30
    assert r1['b'] == 10

    
def test_bad_row_set_item():
    r1 = DataRow(['a', 'b', 'c'], [10, 20, 30])
    r1['a'] = 50
    with pytest.raises(IndexError) as e:
        r1['d'] = 40
    assert r1.columns() == ['a', 'b', 'c']
    assert r1.values() == [50, 20, 30]

    
def test_row_del_item():
    r1 = DataRow(['a', 'b', 'c'], [10, 20, 30])
    del r1['a']
    assert r1.columns() == ['b', 'c']
    assert r1.values() == [20, 30]
    del r1['c']
    assert r1.columns() == ['b']
    assert r1.values() == [20]
    del r1['b']
    assert r1.columns() == []
    assert r1.values() == []

    
def test_bad_row_del_item():
    r1 = DataRow(['a', 'b'], [10, 20])
    with pytest.raises(IndexError) as e:
        del r1['c']
    del r1['a']
    assert r1.columns() == ['b']
    assert r1.values() == [20]

    
def test_row_add():
    r1 = DataRow()
    r2 = DataRow()
    assert r1 == r1 + r2
    r1 = DataRow(['a'], [1])
    assert r1 == r1 + r2
    r2 = DataRow(['b'], [2])
    assert (r1 + r2).columns() == ['a', 'b']
    assert (r1 + r2).values() == [1, 2]
    r1 = DataRow(['a','c'], [1, 3])
    assert (r2 + r1).columns() == ['b', 'a', 'c']
    assert (r2 + r1).values() == [2, 1, 3]
    assert (r1 + r2).columns() == ['a', 'c', 'b']
    assert (r1 + r2).values() == [1, 3, 2]

    
def test_bad_row_add():
    r1 = DataRow(['a', 'b'], [1, 2])
    with pytest.raises(ValueError) as e:
        r1 + (['c'], 3)
    r2 = DataRow(['c', 'b'], [3, 2])
    with pytest.raises(ValueError) as e:
        r1 + r2

        
def test_row_select():
    r1 = DataRow(['b', 'c', 'a'], [10, 20, 30])
    assert r1 == r1.select()
    assert id(r1) != id(r1.select())
    assert r1.select(['c']).columns() == ['c']
    assert r1.select(['c']).values() == [20]
    assert r1.select(['c', 'b']).columns() == ['c', 'b']
    assert r1.select(['c', 'b']).values() == [20, 10]
    assert r1.select(['a', 'b', 'c']).columns() == ['a', 'b', 'c']
    assert r1.select(['a', 'b', 'c']).values() == [30, 10, 20]
    
    
def test_bad_row_select():
    r1 = DataRow()
    with pytest.raises(ValueError) as e:
        r1.select(['a'])
    r1 = DataRow(['a', 'b'], [10, 20])
    with pytest.raises(ValueError) as e:
        r1.select(['c'])    

        
def test_row_copy():
    r1 = DataRow()
    assert id(r1) != id(r1.copy())
    r1 = DataRow(['a', 'b'], [10, 20])
    r2 = r1.copy()
    assert id(r1) != id(r2)
    assert r2.columns() == ['a', 'b']
    assert r2.values() == [10, 20]

    
#----------------------------------------------------------------------
# Data Table tests
#----------------------------------------------------------------------


def test_empty_init_table():
    t1 = DataTable()
    assert t1.column_count() == 0
    assert t1.row_count() == 0
    assert t1.columns() == []

    
def test_column_only_init_table():
    t1 = DataTable([])
    assert t1.column_count() == 0
    assert t1.columns() == []
    t1 = DataTable(['a'])
    assert t1.column_count() == 1
    assert t1.columns() == ['a']
    t1 = DataTable(['a', 'b'])
    assert t1.column_count() == 2
    assert t1.columns() == ['a', 'b']
    t1 = DataTable(['a', 'c', 'b'])
    assert t1.column_count() == 3
    assert t1.columns() == ['a', 'c', 'b']
    
    
def test_bad_column_only_init_table():
    with pytest.raises(ValueError) as e:
        t1 = DataTable(['a', 'b', 'a'])
    

def test_append_rows_table():
    t1 = DataTable(['a','b'])
    t1.append([10, 20])
    assert t1.row_count() == 1
    assert t1[0] == DataRow(['a','b'], [10, 20])
    t1.append([30, 40])
    assert t1.row_count() == 2
    assert t1[0] == DataRow(['a','b'], [10, 20])
    assert t1[1] == DataRow(['a','b'], [30, 40])    

    
def test_bad_append_rows_table():
    t1 = DataTable(['a','b'])
    with pytest.raises(ValueError) as e:
        t1.append([10])
    with pytest.raises(ValueError) as e:
        t1.append([10, 20, 30])
    t1.append(['1', '2'])
    assert t1[0]['a'] != 1
    assert t1[0]['b'] != 2

    
def test_del_rows_table():
    t1 = DataTable(['a','b'])
    t1.append([10, 20])
    assert t1.row_count() == 1
    del t1[0]
    assert t1.row_count() == 0
    t1 = DataTable(['a','b'])
    t1.append([10, 20])
    t1.append([30, 40])
    assert t1.row_count() == 2
    del t1[1]
    assert t1.row_count() == 1
    assert t1[0] == DataRow(['a','b'], [10, 20])
    t1.append([30, 40])
    del t1[0]
    assert t1.row_count() == 1
    assert t1[0] == DataRow(['a','b'], [30, 40])

    
def test_bad_drop_rows_table():
    t1 = DataTable(['a', 'b', 'c'])
    with pytest.raises(IndexError) as e:
        del t1[0]
    t1.append([10, 20, 30])
    with pytest.raises(IndexError) as e:
        del t1[1]


def test_get_many_rows_table():
    t1 = DataTable(['x', 'y'])
    for i in range(5):
        t1.append([i, i+1])
    t2 = t1.rows([0, 1])
    assert t2.columns() == ['x', 'y']
    assert t2[0].values() == [0, 1]
    assert t2[1].values() == [1, 2]
    t2 = t1.rows([2, 3, 4])
    assert t2.columns() == ['x', 'y']
    assert t2[0].values() == [2, 3]
    assert t2[1].values() == [3, 4]    
    assert t2[2].values() == [4, 5]


def test_bad_get_many_rows_table():
    t1 = DataTable(['x', 'y'])
    with pytest.raises(IndexError) as e:
        t1.rows([0])
    t1.append([0, 1])
    t1.append([1, 2])
    with pytest.raises(IndexError) as e:
        t1.rows([0, 2])
    

def test_update_row_table():
    t1 = DataTable(['x' , 'y', 'z'])
    t1.append([0, 1, 2])
    t1.update(0, 'x', 10)
    t1.update(0, 'y', 20)
    t1.update(0, 'z', 30)
    assert t1[0].values() == [10, 20, 30]
    t1.append([3, 4, 5])
    t1.update(1, 'x', 40)
    t1.update(1, 'y', 50)
    t1.update(1, 'z', 60)
    assert t1[0].values() == [10, 20, 30]
    assert t1[1].values() == [40, 50, 60]    

    
def test_bad_update_row_table():
    t1 = DataTable(['x', 'y'])
    with pytest.raises(IndexError) as e:
        t1.update(0, 'x', 10)
    t1.append([0, 1])
    t1.append([1, 2])
    with pytest.raises(IndexError) as e:
        t1.update(0, 'z', 20)
    with pytest.raises(IndexError) as e:
        t1.update(2, 'y', 20)
    t1.update(0, 'x', '20')
    assert t1[0]['x'] != 20


def test_copy_table():
    t1 = DataTable(['x', 'y'])
    t2 = t1.copy()
    assert id(t1) != id(t2)
    assert t1.columns() == t2.columns()
    assert t1.row_count() == t2.row_count()
    t1.append([10, 20])
    t1.append([30, 40])
    t2 = t1.copy()
    assert id(t1) != id(t2)
    assert t1.columns() == t2.columns()
    assert t1.row_count() == t2.row_count()
    assert t1[0] == t2[0]
    assert t1[1] == t2[1]


def test_load_table():
    with open('tmp.txt', 'w') as f:
        f.write('1, 2, 3.14\n')
        f.write('4,,six\n')
        f.write('a b, c, d e f\n')
        f.write('2.7,a b,\n')
    t1 = DataTable(['x', 'y', 'z'])
    t1.load('tmp.txt')
    assert t1.row_count() == 4
    assert t1[0].values() == [1, 2, 3.14]
    assert t1[1].values() == [4, '', 'six']
    assert t1[2].values() == ['a b', 'c', 'd e f']
    assert t1[3].values() == [2.7, 'a b', '']
    os.remove('tmp.txt')

    
def test_bad_load_table():
    with open('tmp.txt', 'w') as f:
        f.write('1,2\n')
        f.write('1,2,3\n')
    t1 = DataTable(['x', 'y'])
    with pytest.raises(ValueError):
        t1.load('tmp.txt')
    os.remove('tmp.txt')


def test_save_table():
    t1 = DataTable(['x', 'y', 'z'])
    t1.append([1, 3.14, 'six'])
    t1.append([2.7, 'a b', ''])
    t1.save('tmp.txt')
    with open('tmp.txt', 'r') as f:
        assert f.readline() == '1,3.14,"six"\n'
        assert f.readline() == '2.7,"a b",""\n'
    t1 = DataTable(['x', 'y', 'z'])
    t1.load('tmp.txt')
    assert t1.row_count() == 2
    assert t1[0].values() == [1, 3.14, 'six']
    assert t1[1].values() == [2.7, 'a b', '']
    os.remove('tmp.txt')


def test_one_column_combine_table():
    t1 = DataTable(['x', 'y'])
    t1.append([1, 20])
    t1.append([3, 40])
    t1.append([2, 30])
    t2 = DataTable(['y', 'z'])
    t2.append([30, 300])
    t2.append([20, 100])
    t2.append([50, 500])
    t2.append([20, 200])
    t2.append([60, 600])
    # non_matches is false
    t3 = DataTable.combine(t1, t2, ['y'])
    assert t3.columns() == ['x', 'y', 'z']
    assert t3.row_count() == 3
    rows = [t3[i].values() for i in range(t3.row_count())]
    assert [1, 20, 100] in rows
    assert [1, 20, 200] in rows
    assert [2, 30, 300] in rows
    # non_matches is true
    t3 = DataTable.combine(t2, t1, ['y'], True)
    assert t3.columns() == ['y', 'z', 'x']
    assert t3.row_count() == 6
    rows = [t3[i].values() for i in range(t3.row_count())]    
    assert [20, 100, 1] in rows
    assert [20, 200, 1] in rows
    assert [30, 300, 2] in rows
    assert [40, '', 3] in rows
    assert [50, 500, ''] in rows
    assert [60, 600, ''] in rows
    
    
def test_two_column_combine_table():
    t1 = DataTable(['x', 'y', 'z'])
    t1.append([1, 10, 100])
    t1.append([2, 20, 200])
    t1.append([2, 10, 200])
    t1.append([3, 30, 300])
    t2 = DataTable(['z', 'u', 'x'])
    t2.append([200, 60, 2])
    t2.append([100, 60, 1])
    t2.append([400, 60, 2])
    t2.append([100, 60, 1])
    # non_matches is false
    t3 = DataTable.combine(t1, t2, ['x', 'z'])
    assert t3.columns() == ['x', 'y', 'z','u']
    assert t3.row_count() == 4
    rows = [t3[i].values() for i in range(t3.row_count())]
    assert rows.count([1, 10, 100, 60]) == 2
    assert [2, 20, 200, 60] in rows
    assert [2, 10, 200, 60] in rows
    # non_matches is true
    t3 = DataTable.combine(t1, t2, ['x', 'z'], True)
    assert t3.columns() == ['x', 'y', 'z','u']
    assert t3.row_count() == 6
    rows = [t3[i].values() for i in range(t3.row_count())]
    assert rows.count([1, 10, 100, 60]) == 2
    assert [2, 20, 200, 60] in rows
    assert [2, 10, 200, 60] in rows
    assert [3, 30, 300, ''] in rows
    assert [2, '', 400, 60] in rows


def test_bad_combine_table():
    t1 = DataTable(['x','y','z'])
    t2 = DataTable(['y', 'z', 'u'])
    with pytest.raises(IndexError) as e:
        DataTable.combine(t1, t2, ['y', 'z', 'y'])
    with pytest.raises(IndexError) as e:
        DataTable.combine(t1, t2, ['z', 'u'])
    with pytest.raises(IndexError) as e:
        DataTable.combine(t1, t2, ['y', 'x'])


def test_convert_numeric_table():
    v = DataTable.convert_numeric('')
    assert isinstance(v, str)
    v = DataTable.convert_numeric('abc')
    assert isinstance(v, str)
    v = DataTable.convert_numeric('0')
    assert isinstance(v, int)
    assert v == 0
    v = DataTable.convert_numeric('01')
    assert isinstance(v, int)
    assert v == 1
    v = DataTable.convert_numeric('123456789123456789')
    assert isinstance(v, int)
    assert v == 123456789123456789
    v = DataTable.convert_numeric('0.0')
    assert isinstance(v, float)
    assert v == 0.0
    v = DataTable.convert_numeric('3.14')    
    assert isinstance(v, float)
    assert v == 3.14
    v = DataTable.convert_numeric('3.14159')    
    assert isinstance(v, float)
    assert v == 3.14159
    
