"""Machine learning algorithm evaluation functions. 

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""

from data_table import *
from data_learn import *
from data_util import *
from random import randint



def holdout(table, test_set_size):
    """Partitions the table into a training and test set using the holdout method. 

    Args:
        table: The table to partition.
        test_set_size: The number of rows to include in the test set.

    Returns: The pair (training_set, test_set)

    """
    # TODO
    train = table.copy()
    test = DataTable(table.columns())
    for i in range(test_set_size):
        x = randint(0,table.row_count()-i-1)
        test.append(train[x].values())
        del train[x]
    return train, test


def knn_eval(train, test, vote_fun, k, label_col, numeric_cols, nominal_cols=[]):
    """Returns a confusion matrix resulting from running knn over the
    given test set. 

    Args:
        train: The training set.
        test: The test set.
        vote_fun: The function to use for selecting labels.
        k: The k nearest neighbors for knn.
        label_col: The column to use for predictions. 
        numeric_cols: The columns compared using Euclidean distance.
        nominal_cols: The nominal columns for knn (match or no match).

    Returns: A data table with n rows (one per label), n+1 columns (an
        'actual' column plus n label columns), and corresponding
        prediction vs actual label counts.

    Notes: If the given voting function returns multiple labels, the
        first such label is selected.

        have a loop
        1. row by row through the test set
        2. call knn(train, row, k, numerical, nominal)
        3. prep results of knn: create an instance list and a scores list (score = 0 - d)
        4. call the vote_fun(instances, scores, label_col)
        5. prediction is first labeled returned
        6. compare the prediction to the ground truth of the row
        update_matrix(matrix, label1, label2) where label1 is the col and label2 is the row
        if actual column is equal to label2
    """
    # TODO
    #knn(table, instance, k, numerical_columns, nominal_columns=[])

    #create an empty confusion matrix
    labels = set(row[label_col] for row in train)
    labels = list(labels)
    matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        matrix.append([r] + zeros)
    
    # for the voting function
    instances = []
    scores = []
    majority = []

    #print(matrix)
    for instance in test:
        # predicting the label
        dist_dict = knn(train, instance, k, numeric_cols, nominal_cols)
        for key in dist_dict:
            #print(key)
            for r in dist_dict[key]:
                instances.append(r)
                scores.append(0-key)
        majority = vote_fun(instances, scores, label_col)
        
        #compare the prediction to the ground truth
        for row in matrix: 
            if row['actual'] == instance[label_col]:
                row[majority[0]] +=1
    
    return matrix

        


def accuracy(confusion_matrix, label):
    """Returns the accuracy for the given label from the confusion matrix.
    
    Args:
        confusion_matrix: The confusion matrix.
        label: The class label to measure the accuracy of.

    """
    # TODO
    # TP + TN / P + N  
    # true aa + all non a things / all things
    #for row in confusion_matrix:
    num = 0
    den = 0
    for row in confusion_matrix:
        if row['actual'] == label:
            num += row[label]
        else:
            for col in confusion_matrix.columns():
                if col != label and col != 'actual':
                    num += row[col]
        for col in confusion_matrix.columns():
            if col != 'actual':
                den += row[col]
    return num/den
    
    
    






def precision(confusion_matrix, label):
    """Returns the precision for the given label from the confusion
    matrix.

    Args:
        confusion_matrix: The confusion matrix.
        label: The class label to measure the precision of.

    """
    # TODO
    # TP / Ppred
    den = 0
    num = 0
    for row in confusion_matrix:
        if row['actual'] == label:
            num += row[label]
        den += row[label]
    if den != 0:
        return num/den
    else:
        return 0

    
    
    



def recall(confusion_matrix, label): 
    """Returns the recall for the given label from the confusion matrix.

    Args:
        confusion_matrix: The confusion matrix.
        label: The class label to measure the recall of.

    """
    # TODO
    # TP / Pact
    den = 0
    num = 0
    for row in confusion_matrix:
        if row['actual'] == label:
            num += row[label]
            for col in confusion_matrix.columns():
                if col != 'actual':
                    den += row[col]
    if den != 0:
        return num/den
    else:
        return 0

