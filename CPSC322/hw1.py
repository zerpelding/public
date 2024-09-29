"""
HW-1 list functions. 

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""
import random

def list_stats(values):
    """Returns the min, max, average, and sum of the values in the given
    list as a tuple (min, max, avg, sum).
      
    Args:
        values: The list of values to compute statistics over.

    Notes:
        Tuple (None, None, None, None) returned if values is empty.
        Assumes a list of numerical values. 

    Example: 
        >>> list_stats([1, 2, 3])
        (1, 3, 2.0, 6)

    """
    if values == []:
        return (None, None, None, None)
    amt = len(values)
    j = 0
    sum = 0
    min = values[0]
    max = values[0]
    while j < amt:
        if values[j] < min:
            min = values[j]
        if values[j] > max:
            max = values[j]        
        sum += values[j]
        j += 1
    return (min, max, sum / amt, sum)

def convert_numeric(value):
    """Returns corresponding numeric value for given string value.

    Args:
        value: The string value to convert.

    Notes:
        Given value returned if  cannot be converted to int or float.

    Examples:
        >>> convert_numeric('abc')
        'abc'
        >>> convert_numeric('42')
        42
        >>> convert_numeric('3.14')
        3.14

    """
    
    try:        
        int_val = int(value)
        return int_val
    except:
        try:
            flo_val = float(value)
            return flo_val
        except:
            return value


def random_matrix_for(m, n):
    """Return an m x n matrix as a list of lists containing randomly
    generated integer values.
    using for loops

    Args:
        m: The number of rows. 
        n: The number of columns.

    Notes:
        Values are from 0 up to but not including m*n.
    
    Example:
        >>> random_matrix_for(2, 3)
        [[2, 1, 0], [3, 6, 4]]

    """
    matrix = []
    for i in range(m):
        row =[]
        for j in range(n):
            row.append(random.randint(0,(m*n)-1))
        matrix.append(row)
    return(matrix)


def random_matrix_comp(m, n):
    """Return an m x n matrix as a list of lists containing randomly
    generated integer values.
    using list comprehension
    Args:
        m: The number of rows. 
        n: The number of columns.

    Notes:
        Values are from 0 up to but not including m*n.
    
    Example:
        >>> random_matrix_comp(2, 3)
        [[2, 1, 0], [3, 6, 4]]

    """
    new_matrix = [[random.randint(0,(m*n)-1) for i in range(n)]for j in range(m)]
    return new_matrix



def transpose_matrix(list_matrix): 
    """Return the transpose of the given matrix represented as a list of
    lists.

    Args:
        list_matrix: The list version of the matrix to transpose.

    Example: 
        >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]

    """
    m_og = len(list_matrix) 
    if m_og == 0:
        return list_matrix
    n_og = len(list_matrix[0])  
    new_matrix = []
    for k in range(n_og):
        row =[]
        for l in range(m_og):
            row.append(list_matrix[l][k])
        new_matrix.append(row)
    return new_matrix




def reshape_matrix(list_matrix, m, n):
    """Return a new matrix based on the given matrix but scaled to m rows
    and n columns.

    Args:
        list_matrix: The matrix to reshape.
        m: The new number of rows.
        n: The new number of columns.

    Notes:
        New rows or columns are filled with 0 values.

    Example: 
        >>> reshape_matrix([[1, 2, 3], [4, 5, 6]], 3, 2)
        [[1, 2], [4, 5], [0, 0]]
    """

    new_matrix = []
    m_og = len(list_matrix)

    for k in range(m):
        if k < m_og:
            row = []
            n_og = len(list_matrix[0])
            for l in range(n):
                if l < n_og:
                    row.append(list_matrix[k][l])
                else:
                    row.append(0)
            new_matrix.append(row)
        else:
            row = []
            for l in range(n):
                row.append(0)
            new_matrix.append(row)
    return(new_matrix)
