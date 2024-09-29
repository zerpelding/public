"""Machine learning algorithm implementations.

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""

from data_table import DataTable, DataRow


#----------------------------------------------------------------------
# HW-5
#----------------------------------------------------------------------

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

    """
    # TODO
    row_dist = []
    distances = {}
    for row in table:
        distance = 0
        for col in numerical_columns:
            distance = distance + (row[col]-instance[col])**2
        for col in nominal_columns:
            if row[col] != instance[col]:
                distance += 1
        row_dist = row_dist + [[distance, row]]
    # sort row_dist
    n = len(row_dist)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if row_dist[j][0] > row_dist[j+1][0]:
                swapped = True
                row_dist[j], row_dist[j+1] = row_dist[j+1], row_dist[j]
        if not swapped:
            break
    # put the first k distances into the dictionary with lists of rows of that distance
    i = 0
    for pair in row_dist:
        if i < k:
            if pair[0] not in distances:
                distances[pair[0]] = [pair[1]]
                i += 1
            else:    
                distances[pair[0]].append(pair[1])
        else:
            if pair[0] in distances:
                distances[pair[0]].append(pair[1])
    return distances


    



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


            

