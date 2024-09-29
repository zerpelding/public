"""Machine learning algorithm implementations.

NAME: <your name here>
DATE: Fall 2023
CLASS: CPSC 322

"""

from data_table import *
from data_util import *

import math


#----------------------------------------------------------------------
# HW-6
#----------------------------------------------------------------------

def naive_bayes(table, instance, label_col, continuous_cols, categorical_cols=[]):
    """Returns the labels with the highest probabibility for the instance
    given table of instances using the naive bayes algorithm.

    Args:
       table: A data table of instances to use for estimating most probably labels.
       instance: The instance to classify.
       continuous_cols: The continuous columns to use in the estimation.
       categorical_cols: The categorical columns to use in the estimation. 

    Returns: A pair (labels, prob) consisting of a list of the labels
        with the highest probability and the corresponding highest
        probability.

    """
    labels = []
    prob = 0
    
    tables = partition(table, [label_col])
    probc = []
    probxcs = []
    
    for tab in tables:
        probc.append(tab.row_count() / table.row_count())
        xc = 1
        for att in categorical_cols:
            vtot = 0
            for row in tab:
                if row[att] == instance[att]:
                    vtot += 1
            xc = xc * (vtot/tab.row_count())
        for att in continuous_cols:
            xc = xc * gaussian_density(instance[att], mean(tab, att), std_dev(tab, att))
        probxcs.append(xc)
    
    probcxs = []
    for i in range(len(probc)):
        probcxs.append(probc[i]*probxcs[i])

    max = 0
    for i in range(len(probc)):
        if probcxs[i] > max:
            max = probcxs[i]
    
    i = 0
    for cx in probcxs:
        if cx == max:
            prob = cx
            labels.append(tables[i][0][label_col])
        i += 1
    
    return (labels, prob)

    

def gaussian_density(x, mean, sdev):
    """Return the probability of an x value given the mean and standard
    deviation assuming a normal distribution.

    Args:
        x: The value to estimate the probability of.
        mean: The mean of the distribution.
        sdev: The standard deviation of the distribution.

    """
    return math.exp(-((x-mean)**2)/(2*sdev**2))/(sqrt(2*math.pi)*sdev)


#----------------------------------------------------------------------
# HW-5
#----------------------------------------------------------------------

# TODO: Copy your HW-5 functions here
def knn(table, instance, k, numerical_columns, nominal_columns=[]):
    """Returns the k closest distance values and corresponding table
    instances forming the nearest neighbors of the given instance. 

    Args:
        table: The data table whose instances form the nearest neighbors.
        instance: The instance to find neighbors for in the table.
        k: The number of closest distances to return.
        numerical_columns: The numerical columns to use for comparison.
        nominal_columns: The nominal columns to use for comparison (if any).

    Returns: A dictionary with k key-value pairs, where the keys are
        the distances and the values are the corresponding rows.

    Notes: 
        The numerical and nominal columns must be disjoint. 
        The numerical and nominal columns must be valid for the table.
        The resulting score is a combined distance without the final
        square root applied.

        
    result = {dist1: [...], dist2: [...], ...}
    for row in table:
    ...
        if distance in result:
            result[distance].append(row.values())
        elif len(result) < k:
            result[distance] = [row.values()]
        elif dist < max(result):
            del result[max(result)]
            result[distance] = [row.values()]
            

    """
    # TODO
    result = {}

    for row in table:
        distance = 0
        for col in numerical_columns:
            distance += (instance[col]-row[col])**2
        for col in nominal_columns:
            if instance[col] != row[col]:
                distance += 1
        if distance in result:
            result[distance].append(row)
        elif len(result) < k:
            result[distance] = [row]
        elif distance < max(result):
            del result[max(result)]
            result[distance] = [row]

    return result

    


def majority_vote(instances, scores, labeled_column):
    """Returns the labels in the given instances that occur the most.

    Args:
        instances: A list of instance rows.
        labeled_column: The column holding the class labels.

    Returns: A list of the labels that occur the most in the given
    instances.

    """
    # TODO
    labels = []
    numbers = []
    majority = []

    un_vals = []
    for i in range(len(instances)):
        val = instances[i][labeled_column]
        if val not in un_vals:
            un_vals.append(val)

    if len(instances) != 0:
        i =0
        j = 0
        while i < len(un_vals):
            if instances[j][labeled_column] not in labels:
                labels.append(instances[j][labeled_column])
                i += 1
                total = 0
                for row in instances:
                    if labels[i-1] == row[labeled_column]:
                        total +=1
                numbers.append(total)
            j += 1
    
    max = 0
    for n in numbers:
        if n > max:
            max = n
    
    #majority
    for i in range(len(labels)):
        if max == numbers[i]:
            majority.append(labels[i])

    return majority



def weighted_vote(instances, scores, labeled_column):
    """Returns the labels in the given instances with the largest total
    sum of corresponding scores.

    Args:
        instances: The list of instance rows.
        scores: The corresponding scores for each instance.
        labeled_column: The column with class labels.

    """
    # TODO

    n = len(instances)
    m = {}
    for i in range(len(instances)):
        val = instances[i][labeled_column]
        if val not in m:
            m[val] = 0
    for i in range(n):
        label = instances[i][labeled_column]
        m[label] += scores[i]
    max_score = max(m.values())
    vote = []
    for l in m:
        if m[l] == max_score:
            vote.append(l)
    return vote


            


