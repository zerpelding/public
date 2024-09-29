"""Unit tests for CPSC 322 HW-7. 

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
# same_class 
#----------------------------------------------------------------------

def test_same_class():
    table = DataTable(['a', 'b', 'c'])
    table.append([1, 1, 'y'])
    assert same_class(table, 'c')
    table.append([1, 2, 'y'])
    assert same_class(table, 'c')    
    table.append([1, 2, 'n'])
    assert not same_class(table, 'c')        
    assert same_class(table, 'a')

#----------------------------------------------------------------------
# build_leaves
#----------------------------------------------------------------------

def test_build_leaves():
    table = DataTable(['a', 'b'])
    result = build_leaves(table, 'b')
    assert result == []
    table.append([1, 10])
    result = build_leaves(table, 'b')
    assert len(result) == 1
    assert result[0] == LeafNode(10, 1, 1)
    table.append([2, 10])
    result = build_leaves(table, 'b')
    assert len(result) == 1
    assert result[0] == LeafNode(10, 2, 2)
    table.append([3, 20])
    result = build_leaves(table, 'b')
    assert len(result) == 2
    assert LeafNode(10, 2, 3) in result
    assert LeafNode(20, 1, 3) in result
    table.append([4, 30])
    table.append([5, 20])
    result = build_leaves(table, 'b')
    assert len(result) == 3
    assert LeafNode(10, 2, 5) in result
    assert LeafNode(20, 2, 5) in result
    assert LeafNode(30, 1, 5) in result

    
#----------------------------------------------------------------------
# calc_e_new
#----------------------------------------------------------------------

def test_two_col_calc_e_new():
    table = DataTable(['a', 'b', 'c'])
    e_new = calc_e_new(table, 'c', ['a', 'b'])
    assert len(e_new) == 1
    assert 'a' in e_new[0.0]
    assert 'b' in e_new[0.0]
    table.append([1, 10, 'y'])
    table.append([2, 10, 'n'])
    e_new = calc_e_new(table, 'c', ['a', 'b'])
    assert e_new[0.0] == ['a']
    assert e_new[1.0] == ['b']
    table.append([1, 20, 'n'])
    e_new = calc_e_new(table, 'c', ['a', 'b'])
    assert len(e_new) == 1
    assert 'a' in e_new[2/3]
    assert 'b' in e_new[2/3]
    table.append([2, 20, 'y'])
    e_new = calc_e_new(table, 'c', ['a', 'b'])    
    assert len(e_new) == 1
    assert 'a' in e_new[1.0]
    assert 'b' in e_new[1.0]
    table.append([1, 30, 'y'])
    e_new = calc_e_new(table, 'c', ['a', 'b'])
    assert len(e_new) == 2
    e_new_a = (3/5)*-((2/3)*log(2/3,2) + (1/3)*log(1/3,2)) + (2/5)
    e_new_b = (2/5) + (2/5)
    assert e_new[e_new_a] == ['a']
    assert e_new[e_new_b] == ['b']
    table.append([1, 30, 'n'])
    e_new = calc_e_new(table, 'c', ['a', 'b'])
    assert 'a' in e_new[1.0]
    assert 'b' in e_new[1.0]

    
def test_three_col_calc_e_new():
    table = DataTable(['a', 'b', 'c', 'd'])
    e_new = calc_e_new(table, 'd', ['a', 'b', 'c'])
    assert len(e_new) == 1
    assert 'a' in e_new[0.0]
    assert 'b' in e_new[0.0]
    assert 'c' in e_new[0.0]
    table.append([1, 10, 100, 'y'])
    table.append([1, 20, 200, 'n'])
    table.append([2, 10, 200, 'y'])
    table.append([2, 20, 100, 'n'])
    e_new = calc_e_new(table, 'd', ['a', 'b', 'c'])
    assert len(e_new) == 2
    assert 'b' in e_new[0.0]
    assert 'a' in e_new[1.0]
    assert 'c' in e_new[1.0]

def test_three_labels_calc_e_new():
    table = DataTable(['a', 'b', 'c'])
    table.append([1, 10, 'y'])
    table.append([1, 20, 'm'])
    table.append([1, 10, 'n'])
    table.append([2, 10, 'm'])
    table.append([2, 20, 'y'])
    table.append([2, 10, 'n'])    
    e_new = calc_e_new(table, 'c', ['a', 'b'])
    print(e_new)
    e_new_a = -((1/3)*log(1/3,2) + (1/3)*log(1/3,2) + (1/3)*log(1/3,2))
    assert 'a' in e_new[e_new_a]
    assert 'b' in e_new[4/3]

#----------------------------------------------------------------------
# tdidt
#----------------------------------------------------------------------

def test_zero_column_tdidt():
    table = DataTable(['a'])
    tree = tdidt(table, 'a', [])
    assert tree == None
    table.append(['y'])
    tree = tdidt(table, 'a', [])
    assert tree == [LeafNode('y', 1, 1)]
    table.append(['n'])
    tree = tdidt(table, 'a', [])    
    assert LeafNode('y', 1, 2) in tree
    assert LeafNode('n', 1, 2) in tree

def test_one_column_tdidt():
    table = DataTable(['a', 'b'])
    tree = tdidt(table, 'b', ['a'])
    assert tree == None
    table.append([1, 'y'])
    tree = tdidt(table, 'b', ['a'])
    assert tree == [LeafNode('y', 1, 1)]
    table.append([1, 'y'])
    tree = tdidt(table, 'b', ['a'])
    assert tree == [LeafNode('y', 2, 2)]
    table.append([2, 'n'])
    tree = tdidt(table, 'b', ['a'])
    print(tree)
    assert tree.name == 'a'
    assert tree.values[1] == [LeafNode('y', 2, 2)]
    assert tree.values[2] == [LeafNode('n', 1, 1)]

def test_two_column_tdidt():
    table = DataTable(['a', 'b', 'c'])
    tree = tdidt(table, 'c', ['a','b'])
    assert tree == None
    table.append([1, 1, 'y'])
    tree = tdidt(table, 'c', ['a','b'])
    assert tree == [LeafNode('y', 1, 1)]
    table.append([1, 2, 'n'])
    tree = tdidt(table, 'c', ['a','b'])
    assert type(tree) == AttributeNode
    assert tree.name == 'b'
    assert tree.values[1] == [LeafNode('y', 1, 1)]
    assert tree.values[2] == [LeafNode('n', 1, 1)]
    table.append([2, 1, 'y'])
    tree = tdidt(table, 'c', ['a','b'])
    assert type(tree) == AttributeNode
    assert tree.name == 'b'
    assert tree.values[1] == [LeafNode('y', 2, 2)]
    assert tree.values[2] == [LeafNode('n', 1, 1)]
    table.append([2, 2, 'n'])
    tree = tdidt(table, 'c', ['a','b'])
    assert type(tree) == AttributeNode
    assert tree.name == 'b'
    assert tree.values[1] == [LeafNode('y', 2, 2)]
    assert tree.values[2] == [LeafNode('n', 2, 2)]
    table.append([1, 1, 'n'])
    tree = tdidt(table, 'c', ['a','b'])
    assert type(tree) == AttributeNode
    assert tree.name == 'b'
    assert tree.values[2] == [LeafNode('n', 2, 2)]
    assert type(tree.values[1]) == AttributeNode
    assert tree.values[1].name == 'a'
    assert LeafNode('y', 1, 2) in tree.values[1].values[1]
    assert LeafNode('n', 1, 2) in tree.values[1].values[1]
    assert tree.values[1].values[2] == [LeafNode('y', 1, 1)]

    
#----------------------------------------------------------------------
# summarize instances
#----------------------------------------------------------------------

def test_summarize_instances():
    root = LeafNode('y', 1, 1)
    result = summarize_instances(root)
    assert result == {'y': 1}
    root = LeafNode('y', 1, 2)
    result = summarize_instances(root)
    assert result == {'y': 1}
    root = AttributeNode('a', values={1: [LeafNode('y', 1, 1)]})
    result = summarize_instances(root)
    assert result == {'y': 1}
    root.values[2] = [LeafNode('y', 1, 1)]
    result = summarize_instances(root)
    assert result == {'y': 2}    
    root = AttributeNode('b', values={10: root, 20: [LeafNode('n', 1, 1)]})
    result = summarize_instances(root)
    assert result['y'] == 2
    assert result['n'] == 1
    root.values[20][0].total = 3
    root.values[20].append(LeafNode('y', 2, 3))
    result = summarize_instances(root)
    assert result['y'] == 4
    assert result['n'] == 1

    
#----------------------------------------------------------------------
# resolve nodes
#----------------------------------------------------------------------

def test_resolve_leaf_nodes():
    # case where no attribute nodes (no resolution needed)
    root = LeafNode('y', 1, 1)
    new_root = resolve_leaf_nodes(root)
    assert root == LeafNode('y', 1, 1)
    # simple case with two leaf nodes
    root = AttributeNode('a', {1: [LeafNode('y', 2, 3), LeafNode('n', 1, 3)]})
    new_root = resolve_leaf_nodes(root)
    assert new_root == AttributeNode('a', {1: [LeafNode('y', 2, 3)]})
    assert new_root != root
    # nested tree with two leaf nodes
    subtree = AttributeNode('a', {1: [LeafNode('y', 2, 3), LeafNode('n', 1, 3)]})
    root = AttributeNode('b', {10: subtree, 20: [LeafNode('n', 1, 1)]})
    new_root = resolve_leaf_nodes(root)
    assert new_root.name == 'b'
    assert new_root.values[10] == AttributeNode('a', {1: [LeafNode('y', 2, 3)]})
    assert new_root.values[20] == [LeafNode('n', 1, 1)]
    assert new_root != root
    # two leaf nodes with same counts
    root = AttributeNode('a', {1: [LeafNode('n', 1, 2), LeafNode('y', 1, 2)]})
    new_root = resolve_leaf_nodes(root)
    assert new_root.name == 'a'
    assert new_root.values[1] == [LeafNode('n', 1, 2)]
    assert new_root != root
    # two cases, one case with three leaf nodes 
    subtree1 = [LeafNode('y', 2, 4), LeafNode('n', 1, 4), LeafNode('m', 1, 4)]
    subtree2 = [LeafNode('m', 1, 3), LeafNode('n', 2, 3)]
    root = AttributeNode('a', {1: AttributeNode('b', {10: subtree1, 20: subtree2})})
    new_root = resolve_leaf_nodes(root)
    assert new_root.name == 'a'
    assert new_root.values[1].name == 'b'
    assert new_root.values[1].values[10] == [LeafNode('y', 2, 4)]
    assert new_root.values[1].values[20] == [LeafNode('n', 2, 3)]
    assert new_root != root

    
def test_resolve_attribute_values():
    # single leaf node (no resolution needed)
    root = LeafNode('y', 1, 1)
    table = DataTable(['a', 'b', 'c'])
    new_root = resolve_attribute_values(root, table)
    assert new_root == root
    # single attribute with missing value
    root = AttributeNode('a', {1: [LeafNode('y', 1, 1)]})
    table = DataTable(['a', 'b', 'c'])
    table.append([1, 10, 'y'])
    table.append([2, 10, 'y'])
    new_root = resolve_attribute_values(root, table)
    assert new_root == [LeafNode('y', 1, 1)]
    assert new_root != root
    # nested attribute with missing value
    root = AttributeNode('b', {10: root})
    new_root = resolve_attribute_values(root, table)
    assert new_root == AttributeNode('b', {10: [LeafNode('y', 1, 1)]})
    assert new_root != root
    # fix two missing values
    subtree = AttributeNode('b', {10: [LeafNode('y', 1, 1)]})
    root = AttributeNode('a', {1: subtree})
    table.append([1, 20, 'n'])
    new_root = resolve_attribute_values(root, table)
    assert new_root == [LeafNode('y', 1, 1)]
    assert new_root != root
    # fix nested one of three attributes missing
    subtree = AttributeNode('b', {10: [LeafNode('y', 2, 2)],
                                  20: [LeafNode('n', 3, 3)]})
    root = AttributeNode('a', {1: subtree})
    table = DataTable(['a', 'b', 'c'])
    table.append([1, 10, 'y'])
    table.append([1, 20, 'y'])
    table.append([1, 30, 'n'])
    new_root = resolve_attribute_values(root, table)
    assert new_root.name == 'a'
    assert len(new_root.values[1]) == 2
    assert LeafNode('y', 2, 5) in new_root.values[1]
    assert LeafNode('n', 3, 5) in new_root.values[1]    
    # fix nested two separate values missing
    subtree1 = AttributeNode('b', {10: [LeafNode('y', 1, 1)]})
    subtree2 = AttributeNode('b', {10: [LeafNode('n', 1, 1)]})
    root = AttributeNode('a', {1: subtree1, 2: subtree2})
    table.append([2, 10, 'y'])
    new_root = resolve_attribute_values(root, table)
    assert new_root.name == 'a'
    assert new_root.values[1] == [LeafNode('y', 1, 1)]
    assert new_root.values[2] == [LeafNode('n', 1, 1)]

#----------------------------------------------------------------------
# tdidt_predict
#----------------------------------------------------------------------

def test_tdidt_predict():
    # always predict y
    root = LeafNode('y', 1, 1)
    label = tdidt_predict(root, DataRow(['a', 'b'], [1, 1]))
    assert label == ('y', 100)
    # if a=1 then n
    root = AttributeNode('a', {1: LeafNode('n', 1, 1)})
    label = tdidt_predict(root, DataRow(['a', 'b'], [1, 2]))
    assert label == ('n', 100)
    # if a=1 and b=10 then y, if a=1 and b=20 then n
    l1 = [LeafNode('y', 1, 1)]
    l2 = [LeafNode('n', 1, 1)]
    root = AttributeNode('a', {1: AttributeNode('b', {10: l1, 20: l2})})
    label = tdidt_predict(root, DataRow(['a', 'b'], [1, 10]))
    assert label == ('y', 100)    
    label = tdidt_predict(root, DataRow(['a', 'b'], [1, 20]))
    assert label == ('n', 100)    
    # if a=1, b=10 then y, if a=2 and b=20 then n
    s1 = AttributeNode('b', {10: [LeafNode('y', 2, 3)]})
    s2 = AttributeNode('b', {20: [LeafNode('n', 3, 4)]})
    root = AttributeNode('a', {1: s1, 2: s2})
    label = tdidt_predict(root, DataRow(['a', 'b'], [1, 10]))
    assert label == ('y', (2/3)*100)
    label = tdidt_predict(root, DataRow(['a', 'b'], [2, 20]))
    assert label == ('n', (3/4)*100)
    # if a=1, b=10, c=100 then y
    s1 = AttributeNode('c', {100: [LeafNode('y', 1, 2)]})
    root = AttributeNode('a', {1: AttributeNode('b', {10: s1})})
    label = tdidt_predict(root, DataRow(['a', 'b', 'c'], [1, 10, 100]))
    assert label == ('y', (1/2)*100)
