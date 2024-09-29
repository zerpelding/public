"""Machine learning algorithm evaluation functions. 

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""

from data_table import *
from data_util import *
from data_learn import *
from random import randint



#----------------------------------------------------------------------
# HW-8
#----------------------------------------------------------------------

def bootstrap(table): 
    """Creates a training and testing set using the bootstrap method.

    Args: 
        table: The table to create the train and test sets from.

    Returns: The pair (training_set, testing_set)

    """
    # TODO
    include = [randint(0, table.row_count()-1) for row in table]
    train = DataTable(table.columns())
    test = DataTable(table.columns())
    for i in include:
        train.append(table[i].values())
    for i in range(table.row_count()):
        if i not in include:
            test.append(table[i].values())
    return (train, test)




def stratified_holdout(table, label_col, test_set_size):
    """Partitions the table into a training and test set using the holdout
    method such that the test set has a similar distribution as the
    table.

    Args:
        table: The table to partition.
        label_col: The column with the class labels. 
        test_set_size: The number of rows to include in the test set.

    Returns: The pair (training_set, test_set)

    """
    #TODO
    ptabs = partition(table, [label_col])
    test = DataTable(table[0].columns())
    train = DataTable(table[0].columns())
    for p in ptabs:
        num_rows = (p.row_count()/table.row_count()) * test_set_size
        i = 0
        while i < num_rows:
            j = randint(0,p.row_count()-1)
            test.append(p[j].values())
            del p[j]
            i += 1
        while p.row_count() > 0:
            train.append(p[0].values())
            del p[0]
    return (train, test)

    


def tdidt_eval_with_tree(dt_root, test, label_col, columns):
    """Evaluates the given test set using tdidt over the training
    set, returning a corresponding confusion matrix.

    Args:
       td_root: The decision tree to use.
       test: The testing data set.
       label_col: The column being predicted.
       columns: The categorical columns

    Returns: A data table with n rows (one per label), n+1 columns (an
        'actual' column plus n label columns), and corresponding
        prediction vs actual label counts.

    Notes: If the naive bayes returns multiple labels for a given test
        instance, the first such label is selected.

    """
    #TODO
    #summary = summarize_instances(dt_root)
    #labels = [key for key in summary.keys()]
    labels = columns
    matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        matrix.append([r] + zeros)
    
    for instance in test:
        pre_label, perc = tdidt_predict(dt_root, instance)
        for row in matrix: 
            if row['actual'] == instance[label_col]:
               row[pre_label] +=1
    
    return matrix



def random_forest(table, remainder, F, M, N, label_col, columns):
    """Returns a random forest build from the given table. 
    
    Args:
        table: The original table for cleaning up the decision tree.
        remainder: The table to use to build the random forest.
        F: The subset of columns to use for each classifier.
        M: The number of unique accuracy values to return.
        N: The total number of decision trees to build initially.
        label_col: The column with the class labels.
        columns: The categorical columns used for building the forest.

    Returns: A list of (at most) M pairs (tree, accuracy) consisting
        of the "best" decision trees and their corresponding accuracy
        values. The exact number of trees (pairs) returned depends on
        the other parameters (F, M, N, and so on).

    """
    #TODO
    pairs = []
    for i in range(N):
        train, test = bootstrap(remainder)
        while not test.row_count():
            train, test = bootstrap(remainder)
        
        tree = tdidt_F(train, label_col, F, columns)
        tree = resolve_attribute_values(tree, table)
        tree = resolve_leaf_nodes(tree)
        matrix = tdidt_eval_with_tree(tree, test, label_col, distinct_values(table, label_col))
        acc_sum = 0
        for lab in matrix.columns():
            if lab != 'actual':
                acc_sum += accuracy(matrix, lab)
            
        acc_i = acc_sum/(len(matrix.columns())-1)
        
        acc_list = [pair[1] for pair in pairs]
        
        if len(pairs) < M:
            pairs.append((tree, acc_i))
        elif acc_i > min(acc_list):
            for i in range(len(acc_list)):
                if acc_list[i] == min(acc_list):
                    del pairs[i]
                    break
            pairs.append((tree, acc_i))
    
    return pairs
    
        



def random_forest_eval(table, train, test, F, M, N, label_col, columns):
    """Builds a random forest and evaluate's it given a training and
    testing set.

    Args: 
        table: The initial table.
        train: The training set from the initial table.
        test: The testing set from the initial table.
        F: Number of features (columns) to select.
        M: Number of trees to include in random forest.
        N: Number of trees to initially generate.
        label_col: The column with class labels. 
        columns: The categorical columns to use for classification.

    Returns: A confusion matrix containing the results. 

    Notes: Assumes weighted voting (based on each tree's accuracy) is
        used to select predicted label for each test row.

    """
    #TODO
    pairs = random_forest(table, train, F, M, N, label_col, columns)
    # matrix
    labels = distinct_values(table, label_col)
    matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        matrix.append([r] + zeros)

    # determining and building
    for row in test:
        # predict
        val_dict = {}
        for pair in pairs:
            prediction, perc = tdidt_predict(pair[0], row)
            if prediction in val_dict:
                val_dict[prediction] += pair[1]
            else:
                val_dict[prediction] = pair[1]
        # find the prediction with the highest accuracy
        max_acc = 0
        max_val = None
        for val in val_dict:
            if val_dict[val] > max_acc:
                max_acc = val_dict[val]
                max_val = val
        
        # add to confusion matrix
        for mrow in matrix: 
            if mrow['actual'] == row[label_col]:
               mrow[max_val] +=1
    
    return matrix


            


    

#----------------------------------------------------------------------
# HW-7
#----------------------------------------------------------------------


# TODO: Copy your HW-7 and prior data_eval functions below

def tdidt_eval(train, test, label_col, columns):
    """Evaluates the given test set using tdidt over the training
    set, returning a corresponding confusion matrix.

    Args:
       train: The training data set.
       test: The testing data set.
       label_col: The column being predicted.
       columns: The categorical columns

    Returns: A data table with n rows (one per label), n+1 columns (an
        'actual' column plus n label columns), and corresponding
        prediction vs actual label counts.

    Notes: If the naive bayes returns multiple labels for a given test
        instance, the first such label is selected.

    """
    #TODO
    #create an empty confusion matrix
    labels = distinct_values(train, label_col)
    matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        matrix.append([r] + zeros)
    tree = tdidt(train, label_col, columns)
    tree = resolve_attribute_values(tree, train)
    tree = resolve_leaf_nodes(tree)

    for instance in test:
        pre_label, percent = tdidt_predict(tree, instance)
        for row in matrix: 
            if row['actual'] == instance[label_col]:
               row[pre_label] +=1
    
    return matrix


def tdidt_stratified(table, k_folds, label_col, columns):
    """Evaluates tdidt prediction approach over the table using stratified
    k-fold cross validation, returning a single confusion matrix of
    the results.

    Args:
        table: The data table.
        k_folds: The number of stratified folds to use.
        label_col: The column with labels to predict. 
        columns: The categorical columns for tdidt. 

    Notes: Each fold created is used as the test set whose results are
        added to a combined confusion matrix from evaluating each
        fold.

    """
    #TODO
    labels = distinct_values(table, label_col)
    final_matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        final_matrix.append([r] + zeros)
    
    folds = stratify(table, label_col, k_folds)
    for test in folds:
        tables = []
        for t in folds:
            if t != test:
                tables.append(t)
        train = union_all(tables)
        matrix = tdidt_eval(train, test, label_col, columns)
        r = 0
        for row in final_matrix:
            for col in final_matrix.columns():
                if col != 'actual':
                    row[col] = row[col] + matrix[r][col]
            r += 1
    return final_matrix


#----------------------------------------------------------------------
# HW-6
#----------------------------------------------------------------------

#TODO: Copy your data_eval HW-6 functions here
def stratify(table, label_column, k):
    """Returns a list of k stratified folds as data tables from the given
    data table based on the label column.

    Args:
        table: The data table to partition.
        label_column: The column to use for the label. 
        k: The number of folds to return. 

    Note: Does not randomly select instances for the folds, and
        instead produces folds in order of the instances given in the
        table.

    """
    ptabs = partition(table, [label_column])
    final = []
    for i in range(k):
        final.append(DataTable(ptabs[0].columns()))
    for part in ptabs:
        while part.row_count() != 0:
            for tab in final:
                if part.row_count() != 0:
                    tab.append(part[0].values())
                    del part[0]
    return final
        



def union_all(tables):
    """Returns a table containing all instances in the given list of data
    tables.

    Args:
        tables: A list of data tables. 

    Notes: Returns a new data table that contains all the instances of
       the first table in tables, followed by all the instances in the
       second table in tables, and so on. The tables must have the
       exact same columns, and the list of tables must be non-empty.

    """
    if len(tables) == 0:
        raise ValueError('there are no tables in the list')
    table = DataTable(tables[0].columns())
    for tab in tables:
        if tab.columns() != tables[0].columns():
            raise ValueError('columns do not match')
        for row in tab:
            table.append(row.values())
    return table


def naive_bayes_eval(train, test, label_col, continuous_cols, categorical_cols=[]):
    """Evaluates the given test set using naive bayes over the training
    set, returning a corresponding confusion matrix.

    Args:
       train: The training data set.
       test: The testing data set.
       label_col: The column being predicted.
       continuous_cols: The continuous columns (estimated via PDF)
       categorical_cols: The categorical columns

    Returns: A data table with n rows (one per label), n+1 columns (an
        'actual' column plus n label columns), and corresponding
        prediction vs actual label counts.

    Notes: If the naive bayes returns multiple labels for a given test
        instance, the first such label is selected.

    """
    #create an empty confusion matrix
    labels = set(row[label_col] for row in train)
    labels = list(labels)
    matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        matrix.append([r] + zeros)
    
    labelsprob = (0,0)

    for instance in test:
        # predicting the label
        labelsprob = naive_bayes(train, instance, label_col, continuous_cols, categorical_cols)
        
        #compare the prediction to the ground truth
        for row in matrix: 
            if row['actual'] == instance[label_col]:
                row[labelsprob[0][0]] +=1
    
    return matrix



def naive_bayes_stratified(table, k_folds, label_col, cont_cols, cat_cols=[]):
    """Evaluates naive bayes over the table using stratified k-fold cross
    validation, returning a single confusion matrix of the results.

    Args:
        table: The data table.
        k_folds: The number of stratified folds to use.
        label_col: The column with labels to predict. 
        cont_cols: The continuous columns for naive bayes. 
        cat_cols: The categorical columns for naive bayes. 

    Notes: Each fold created is used as the test set whose results are
        added to a combined confusion matrix from evaluating each
        fold.

    """
    labels = set(row[label_col] for row in table)
    labels = list(labels)
    final_matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        final_matrix.append([r] + zeros)
    folds = stratify(table, label_col, k_folds)
    for test in folds:
        tables = []
        for t in folds:
            if t != test:
                tables.append(t)
        train = union_all(tables)
        matrix = naive_bayes_eval(train, test, label_col, cont_cols, cat_cols)
        r = 0
        for row in final_matrix:
            for col in final_matrix.columns():
                if col != 'actual':
                    row[col] = row[col] + matrix[r][col]
            r += 1
    return final_matrix



def knn_stratified(table, k_folds, label_col, vote_fun, k, num_cols, nom_cols=[]):
    """Evaluates knn over the table using stratified k-fold cross
    validation, returning a single confusion matrix of the results.

    Args:
        table: The data table.
        k_folds: The number of stratified folds to use.
        label_col: The column with labels to predict. 
        vote_fun: The voting function to use with knn.
        num_cols: The numeric columns for knn.
        nom_cols: The nominal columns for knn.

    Notes: Each fold created is used as the test set whose results are
        added to a combined confusion matrix from evaluating each
        fold.

    """
    labels = set(row[label_col] for row in table)
    labels = list(labels)
    final_matrix = DataTable(['actual'] + labels)
    zeros = [0 for l in labels]
    for r in labels:
        final_matrix.append([r] + zeros)
    folds = stratify(table, label_col, k_folds)
    for test in folds:
        tables = []
        for t in folds:
            if t != test:
                tables.append(t)
        train = union_all(tables)
        matrix = knn_eval(train, test, vote_fun, k, label_col, num_cols, nom_cols)
        r = 0
        for row in final_matrix:
            for col in final_matrix.columns():
                if col != 'actual':
                    row[col] = row[col] + matrix[r][col]
            r += 1
    return final_matrix


#----------------------------------------------------------------------
# HW-5
#----------------------------------------------------------------------

# TODO: Copy your HW-5 functions here
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








