"""Machine learning algorithm implementations.

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""

from data_table import *
from data_util import *
from decision_tree import *

from random import randint
import math


#----------------------------------------------------------------------
# HW-8
#----------------------------------------------------------------------


def random_subset(F, columns):
    """Returns F unique column names from the given list of columns. The
    column names are selected randomly from the given names.

    Args: 
        F: The number of columns to return.
        columns: The columns to select F column names from.

    Notes: If F is greater or equal to the number of names in columns,
       then the columns list is just returned.

    """
    #TODO
    cols = columns.copy()
    if F >= len(cols):
        return cols
    Fcols = []
    while len(Fcols) < F:
        i = randint(0,len(cols)-1)
        Fcols.append(cols[i])
        del cols[i]
    return Fcols




def tdidt_F(table, label_col, F, columns): 
    """Returns an initial decision tree for the table using information
    gain, selecting a random subset of size F of the columns for
    attribute selection. If fewer than F columns remain, all columns
    are used in attribute selection.

    Args:
        table: The table to build the decision tree from. 
        label_col: The column containing class labels. 
        F: The number of columns to randomly subselect
        columns: The categorical columns. 

    Notes: The resulting tree can contain multiple leaf nodes for a
        particular attribute value, may have attributes without all
        possible attribute values, and in general is not pruned.

    """
    #TODO
    # base cases
    # 1. check if table is empty 
    if table.row_count() == 0:
        return None
    # 2. check if table instances are all same class 
    if same_class(table, label_col):
        return [LeafNode(table[0][label_col], table.row_count(), table.row_count())]
    # 3. if no more attributes to partition on (columns is empty)
    if len(columns) == 0:
        return build_leaves(table, label_col)

    cols = random_subset(F, columns)

    # building a new attribute node
    # 4. find enew values for each column
    enew_dict = calc_e_new(table, label_col, cols)
    # 5. find column with smallest enew
    e = min(enew_dict)
    # 6. partition on the column
    partitions = partition(table, [enew_dict[e][0]])
    # 7. create attribute node and fill in value nodes (recursive calls on partition)
    new_columns = [col for col in cols if col != enew_dict[e][0]]
    something = {}
    for tab in partitions:
        thing = tdidt_F(tab, label_col, F, new_columns)
        something[tab[0][enew_dict[e][0]]] = thing
    new_node = AttributeNode(enew_dict[e][0], something)
    return new_node


def euc_dist(row1, row2, columns):
    dist = 0
    for col in columns:
        dist += (row1[col] - row2[col])**2
    return dist

def closest_centroid(centroids, row, columns):
    """Given k centroids and a row, finds the centroid that the row is
    closest to.

    Args:
        centroids: The list of rows serving as cluster centroids.
        row: The row to find closest centroid to.
        columns: The numerical columns to calculate distance from. 
    
    Returns: The index of the centroid the row is closest to. 

    Notes: Uses Euclidean distance (without the sqrt) and assumes
        there is at least one centroid.

    """
    #TODO
    min_dist = 10000
    min_i = 0
    for i in range(len(centroids)):
        dist = euc_dist(centroids[i], row, columns)
        if dist < min_dist:
            min_dist = dist
            min_i = i
    return min_i

def create_centroid(table, columns):
    values = []
    for col in table.columns():
        if col in columns:
            col_tot = 0
            for row in table:
                col_tot += row[col]
            values.append(col_tot/table.row_count())
        else:
            values.append(None)
    return DataRow(table.columns(),values)


def select_k_random_centroids(table, k):
    """Returns a list of k random rows from the table to serve as initial
    centroids.

    Args: 
        table: The table to select rows from.
        k: The number of rows to select values from.
    
    Returns: k unique rows. 

    Notes: k must be less than or equal to the number of rows in the table. 

    """
    #TODO
    if k > table.row_count():
        raise ValueError('k greater than number of rows in tables')
    random_rows = []
    while len(random_rows) < k:
        i = randint(0, table.row_count()-1)
        if table[i] not in random_rows:
            random_rows.append(DataRow(table.columns(), table[i].values()))
    return random_rows


def k_means(table, centroids, columns): 
    """Returns k clusters from the table using the initial centroids for
    the given numerical columns.

    Args:
        table: The data table to build the clusters from.
        centroids: Initial centroids to use, where k is length of centroids.
        columns: The numerical columns for calculating distances.

    Returns: A list of k clusters, where each cluster is represented
        as a data table.

    Notes: Assumes length of given centroids is number of clusters k to find.

    """
    #TODO
    clusters = []
    for center in centroids:
        clusters.append(DataTable(table.columns()))
    for row in table:
        i = closest_centroid(centroids, row, columns)
        clusters[i].append(row.values())
    new_centroids = [create_centroid(clus, columns) for clus in clusters]
    if new_centroids != centroids:
        clusters = k_means(table, new_centroids, columns)
    return clusters


def tss(clusters, columns):
    """Return the total sum of squares (tss) for each cluster using the
    given numerical columns.

    Args:
        clusters: A list of data tables serving as the clusters
        columns: The list of numerical columns for determining distances.
    
    Returns: A list of tss scores for each cluster. 

    """
    #TODO
    scores = []
    for clus in clusters:
        sum = 0
        centroid = create_centroid(clus, columns)
        for row in clus:
            sum += euc_dist(centroid, row, columns)
        scores.append(sum)
    return scores



#----------------------------------------------------------------------
# HW-7
#----------------------------------------------------------------------


#TODO: Copy your hw-7 and prior code here
def same_class(table, label_col):
    """Returns true if all of the instances in the table have the same
    labels and false otherwise.

    Args: 
        table: The table with instances to check. 
        label_col: The column with class labels.

    """
    #TODO
    same = True
    if table.row_count() == 0:
        return True
    label1 = table[0][label_col]
    for row in table:
        if row[label_col] != label1:
            same = False
    return same


def build_leaves(table, label_col):
    """Builds a list of leaves out of the current table instances.
    
    Args: 
        table: The table to build the leaves out of.
        label_col: The column to use as class labels

    Returns: A list of LeafNode objects, one per label value in the
        table.

    """
    #TODO
    labels = list(set([row[label_col] for row in table]))

    leaflist = []
    for label in labels:
        tot = 0
        num = 0
        for row in table:
            tot += 1
            if row[label_col] == label:
                num +=1
        leaflist.append(LeafNode(label, num, tot))

    return leaflist


def entropy(table, label_col):
    labels = list(set([row[label_col] for row in table]))
    entropy = 0
    for label in labels:
        ccount = 0
        for row in table:
            if row[label_col] == label:
                ccount +=1
        entropy += (ccount/table.row_count())*math.log2(ccount/table.row_count())
    entropy = entropy * (-1)
    return entropy


def calc_e_new(table, label_col, columns):
    """Returns entropy values for the given table, label column, and
    feature columns (assumed to be categorical). 

    Args:
        table: The table to compute entropy from
        label_col: The label column.
        columns: The categorical columns to use to compute entropy from.

    Returns: A dictionary, e.g., {e1:['a1', 'a2', ...], ...}, where
        each key is an entropy value and each corresponding key-value
        is a list of attributes having the corresponding entropy value. 

    Notes: This function assumes all columns are categorical.

    """
    #TODO
    entropies = {}
    for col in columns:
        partitions = partition(table, [col])
        enew = 0
        for tab in partitions:
            enew += (tab.row_count()/table.row_count()) * entropy(tab, label_col)
        if enew not in entropies:
            entropies[enew] = [col]
        else:
            entropies[enew].append(col)
    return entropies



def tdidt(table, label_col, columns): 
    """Returns an initial decision tree for the table using information
    gain.

    Args:
        table: The table to build the decision tree from. 
        label_col: The column containing class labels. 
        columns: The categorical columns. 

    Notes: The resulting tree can contain multiple leaf nodes for a
        particular attribute value, may have attributes without all
        possible attribute values, and in general is not pruned.

    """
    #TODO
    # base cases
    # 1. check if table is empty 
    if table.row_count() == 0:
        return None
    # 2. check if table instances are all same class 
    if same_class(table, label_col):
        return [LeafNode(table[0][label_col], table.row_count(), table.row_count())]
    # 3. if no more attributes to partition on (columns is empty)
    if len(columns) == 0:
        return build_leaves(table, label_col)

    # building a new attribute node
    # 4. find enew values for each column
    enew_dict = calc_e_new(table, label_col, columns)
    # 5. find column with smallest enew
    e = min(enew_dict)
    # 6. partition on the column
    partitions = partition(table, [enew_dict[e][0]])
    # 7. create attribute node and fill in value nodes (recursive calls on partition)
    new_columns = [col for col in columns if col != enew_dict[e][0]]
    something = {}
    for tab in partitions:
        thing = tdidt(tab, label_col, new_columns)
        something[tab[0][enew_dict[e][0]]] = thing
    new_node = AttributeNode(enew_dict[e][0], something)
    return new_node


def summarize_instances(dt_root):
    """Return a summary by class label of the leaf nodes within the given
    decision tree.

    Args: 
        dt_root: The subtree root whose (descendant) leaf nodes are summarized. 

    Returns: A dictionary {label1: count, label2: count, ...} of class
        labels and their corresponding number of instances under the
        given subtree root.

    """
    #TODO

    summary = {}
    # if root is leafnode, summarize labels
    if isinstance(dt_root, LeafNode):
        summary[dt_root.label] = summary.get(dt_root.label, 0) + dt_root.count
    elif isinstance(dt_root, AttributeNode):
        for _, subtree in dt_root.values.items():
            if isinstance(subtree, list):
                for node in subtree:
                    result = summarize_instances(node)
                    for label, count in result.items():
                        summary[label] = summary.get(label, 0) + count
            elif isinstance(subtree, AttributeNode):
                result = summarize_instances(subtree)
                for label, count in result.items():
                    summary[label] = summary.get(label, 0) + count
        if not dt_root.values or all(not subtree_summary for subtree_summary in dt_root.values.values()):
            return {}
        
    return summary 





def resolve_leaf_nodes(dt_root):
    """Modifies the given decision tree by combining attribute values with
    multiple leaf nodes into attribute values with a single leaf node
    (selecting the label with the highest overall count).

    Args:
        dt_root: The root of the decision tree to modify.

    Notes: If an attribute value contains two or more leaf nodes with
        the same count, the first leaf node is used.

    """
    #TODO
    # base cases:
    # 1. if dt_root is a leaf node, return a copy of dt_root
    if isinstance(dt_root, LeafNode):
        return LeafNode(dt_root.label, dt_root.count, dt_root.total)
    #2. if dt_root is a list of leaf nodes, return a copy of the list and leaf nodes:
    elif isinstance(dt_root, list):
        return [LeafNode(l.label, l.count, l.total) for l in dt_root]
    # recursive step:
    # 3. create a new decision tree attribute node (same name as dt_root)
    new_dt_root = AttributeNode(dt_root.name, {})
    # 4. recursively navigate the tree:
    for val, child in dt_root.values.items():
        new_dt_root.values[val] = resolve_leaf_nodes(child)
    # backtracking phase: look at each attribute child
    # 5. for each new_dt_root value, combine its leaves if it has multiple
    for value in new_dt_root.values:
        if isinstance(new_dt_root.values[value], list):
            if len(new_dt_root.values[value]) > 1:
                max = new_dt_root.values[value][0]
                for v in new_dt_root.values[value]:
                    if v.count > max.count:
                        max = v
                new_dt_root.values[value] = [max]
    # all done
    # 6. return the new_dt_root
    return new_dt_root
    


def resolve_attribute_values(dt_root, table):
    """Return a modified decision tree by replacing attribute nodes
    having missing attribute values with the corresponding summarized
    descendent leaf nodes.
    
    Args:
        dt_root: The root of the decision tree to modify.
        table: The data table the tree was built from. 

    Notes: The table is only used to obtain the set of unique values
        for attributes represented in the decision tree.

    """
    #TODO
    # base cases:
    # 1. if dt_root is a leaf node, return a copy of dt_root
    if isinstance(dt_root, LeafNode):
        return LeafNode(dt_root.label, dt_root.count, dt_root.total)
    #2. if dt_root is a list of leaf nodes, return a copy of the list and leaf nodes:
    elif isinstance(dt_root, list):
        return [LeafNode(l.label, l.count, l.total) for l in dt_root]
    # recursive step:
    # 3. create a new decision tree attribute node (same name as dt_root)
    new_dt_root = AttributeNode(dt_root.name, {})
    # 4. recursively navigate the tree:
    for val, child in dt_root.values.items():
        new_dt_root.values[val] = resolve_attribute_values(child, table)
        if isinstance(dt_root, AttributeNode):
            all_children = distinct_values(table, dt_root.name)
            if len(all_children) > len(dt_root.values.keys()):
                child_summ = summarize_instances(dt_root)
                return [LeafNode(label, count, sum(child_summ.values())) for label, count in child_summ.items()]
        elif isinstance(child, AttributeNode):
            all_children = distinct_values(table, child.name)
            for val in all_children:
                if val not in child.values.keys():
                    child_summ = summarize_instances(child)
                    new_dt_root.values[val] = [LeafNode(label, count, sum(child_summ.values())) for label, count in child_summ.items()]
    return new_dt_root
    # backtracking phase: look at each attribute child
    # 5. for each new_dt_root value, if there is a missing value, summarize
    # check if there is a missing attribute value
    
    """
    atts = list(set([row[dt_root.name] for row in table]))
    redo = False
    for val in atts:
        if val not in new_dt_root.values:
           redo = True
    if redo:
        summary = summarize_instances(new_dt_root)
        max_count = 0
        max_val = None
        total = 0
        for val in summary:
            total += summary[val]
            if summary[val] > max_count:
                max_count = summary[val]
                max_val = val
        return [LeafNode(max_val, max_count, total)]
    # all done
    # 6. return the new_dt_root
    return new_dt_root
    """

def tdidt_predict(dt_root, instance): 
    """Returns the class for the given instance given the decision tree. 

    Args:
        dt_root: The root node of the decision tree. 
        instance: The instance to classify. 

    Returns: A pair consisting of the predicted label and the
       corresponding percent value of the leaf node.

    """
    #TODO
    if isinstance(dt_root, LeafNode):
        return dt_root.label, dt_root.percent()
    if isinstance(dt_root, list):
        label = None
        perc = 0
        for i in range(len(dt_root)):
            if dt_root[i].percent() > perc:
                perc = dt_root[i].percent()
                label = dt_root[i].label
        return label, perc
    if isinstance(dt_root, AttributeNode):
        attribute_val = instance[dt_root.name]
        if attribute_val in dt_root.values:
            return tdidt_predict(dt_root.values[attribute_val], instance)



#----------------------------------------------------------------------
# HW-6
#----------------------------------------------------------------------

#TODO: Copy your HW-6 data_learn functions here
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

#TODO: Copy your HW-5 data_learn functions here
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


            




