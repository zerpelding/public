"""Data utility functions for CPSC 322 HW-3. 

Basic functions for preprocessing and visualization data sets. 

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""


from data_table import DataTable, DataRow
import matplotlib.pyplot as plt



def distinct_values(table, column):
    """Return the unique values in the given column of the table.
    
    Args:
        table: The data table used to get column values from.
        column: The column of the table to get values from.

    Notes:
        Returns a list of unique values
    """
    # TODO
    un_vals = []
    for i in range(table.row_count()):
        val = table[i][column]
        if val not in un_vals:
            un_vals.append(val)
    return un_vals


def remove_missing(table, columns):
    """Return a new data table with rows from the given one without
    missing values.

    Args:
        table: The data table used to create the new table.
        columns: The column names to check for missing values.

    Returns:
        A new data table.

    Notes: 
        Columns must be valid.

    """
    # TODO
    row_index = []
    i = 0
    for row in table:
        missing = False
        for col in columns:
            if row[col] == '':
                missing = True
        if missing == False:
            row_index.append(i)
        i += 1
    return table.rows(row_index)




def duplicate_instances(table):
    """Returns a table containing duplicate instances from original table.
    
    Args:
        table: The original data table to check for duplicate instances.

    """
    # TODO
    row_index = []
    i = 0
    for row in table:
        for n in range(table.row_count()):
            same = True
            if n > i:
                for col in table.columns():
                    if row[col] != table[n][col]:
                        same = False
                if same == True:
                    # check to see if this row is already represented in the table
                    place = True
                    for k in range(len(row_index)):
                        already_there = True
                        if row != table[row_index[k]]:
                            already_there = False
                        if already_there:
                            place = False
                    if place:     
                        row_index.append(i)
        i += 1
    return table.rows(row_index)

                    
def remove_duplicates(table):
    """Remove duplicate instances from the given table.
    
    Args:
        table: The data table to remove duplicate rows from

    """
    # TODO
    dups = duplicate_instances(table)
    new = DataTable(table.columns())
    for dup in dups:
        new.append(dup.values())
    for row in table:
        if row not in dups:
            new.append(row.values())
    return new
    


def partition(table, columns):
    """Partition the given table into a list containing one table per
    corresponding values in the grouping columns.
    
    Args:
        table: the table to partition
        columns: the columns to partition the table on
    """
    # TODO
    final = []
    # create the first datatable and append the first row. move to the next row, 
    # if the columns values of the next row matches the first row of a datatable, 
    # place it in the datatable, if it doesn't, create a new datatable and append the row.
    
    if table.row_count() != 0:
        t1 = DataTable(table.columns())
        final.append(t1)
        t1.append(table[0].values())
    n = 0
    for row in table:
        found = False
        if n > 0:
            for t in final:
                #print(row.values())
                if row.select(columns) == t[0].select(columns):
                    t.append(row.values())
                    found = True
            if found == False:
                t2 = DataTable(table.columns())
                final.append(t2)
                t2.append(row.values())
        n+=1
    return final
    


def summary_stat(table, column, function):
    """Return the result of applying the given function to a list of
    non-empty column values in the given table.

    Args:
        table: the table to compute summary stats over
        column: the column in the table to compute the statistic
        function: the function to compute the summary statistic

    Notes: 
        The given function must take a list of values, return a single
        value, and ignore empty values (denoted by the empty string)

    """
    # TODO
    list = []
    for row in table:
        if row[column] != '':
            list.append(row[column])
    return function(list)


def replace_missing(table, column, partition_columns, function): 
    """Replace missing values in a given table's column using the provided
     function over similar instances, where similar instances are
     those with the same values for the given partition columns.

    Args:
        table: the table to replace missing values for
        column: the coumn whose missing values are to be replaced
        partition_columns: for finding similar values
        function: function that selects value to use for missing value

    Notes: 
        Assumes there is at least one instance with a non-empty value
        in each partition

    """
    # TODO
    new_table = table.copy()
    part = partition(new_table, partition_columns)
    for row in new_table:
        if row[column] == '':
            # which index is this column in the particion tables list?
            for t in part:
                if row in t:
                    # what is the function value of table at column?
                    val = summary_stat(t,column,function)
                    row[column] = val
    return new_table
    

def summary_stat_by_column(table, partition_column, stat_column, function):
    """Returns for each partition column value the result of the statistic
    function over the given statistics column.

    Args:
        table: the table for computing the result
        partition_column: the column used to create groups from
        stat_column: the column to compute the statistic over
        function: the statistic function to apply to the stat column

    Notes:
        Returns a list of the groups and a list of the corresponding
        statistic for that group.

    """
    # TODO
    groups = []
    stat_list = []
    part = partition(table, [partition_column])
    for t in part:
        groups.append(t[0][partition_column])
    for t in part:
        stat_list.append(summary_stat(t, stat_column, function))
    return groups, stat_list



def frequencies(table, partition_column):
    """Returns for each partition column value the number of instances
    having that value.

    Args:
        table: the table for computing the result
        partition_column: the column used to create groups

    Notes:

        Returns a list of the groups and a list of the corresponding
        instance count for that group.

    """
    # TODO
    groups = []
    stat_list = []
    part = partition(table, [partition_column])
    for t in part:
        n = 0
        groups.append(t[0][partition_column])
        for r in t:
            n+=1
        stat_list.append(n)
    return groups, stat_list


def dot_chart(xvalues, xlabel, title, filename=None):
    """Create a dot chart from given values.
    
    Args:
        xvalues: The values to display
        xlabel: The label of the x axis
        title: The title of the chart
        filename: Filename to save chart to (in SVG format)

    Notes:
        If filename is given, chart is saved and not displayed.

    """
    # reset figure
    plt.figure()
    # dummy y values
    yvalues = [1] * len(xvalues)
    # create an x-axis grid
    plt.grid(axis='x', color='0.85', zorder=0)
    # create the dot chart (with pcts)
    plt.plot(xvalues, yvalues, 'b.', alpha=0.2, markersize=16, zorder=3)
    # get rid of the y axis
    plt.gca().get_yaxis().set_visible(False)
    # assign the axis labels and title
    plt.xlabel(xlabel)
    plt.title(title)
    # save as file or just show
    if filename:
        plt.savefig(filename, format='svg')
    else:
        plt.show()
    # close the plot
    plt.close()

    
def pie_chart(values, labels, title, filename=None):
    """Create a pie chart from given values.
    
    Args:
        values: The values to display
        labels: The label to use for each value
        title: The title of the chart
        filename: Filename to save chart to (in SVG format)

    Notes:
        If filename is given, chart is saved and not displayed.

    """
    # TODO
    # reset figure
    plt.figure()
    plt.pie(values, labels = labels)
    plt.title(title)
    if filename:
        plt.savefig(filename, format='svg')
    else:
        plt.show()
    # close the plot
    plt.close()


def bar_chart(bar_values, bar_names, xlabel, ylabel, title, filename=None):
    """Create a bar chart from given values.
    
    Args:
        bar_values: The values used for each bar
        bar_labels: The label for each bar value
        xlabel: The label of the x-axis
        ylabel: The label of the y-axis
        title: The title of the chart
        filename: Filename to save chart to (in SVG format)

    Notes:
        If filename is given, chart is saved and not displayed.

    """
    # TODO
    plt.figure()
    plt.bar(bar_names, bar_values, width = 0.8)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    if filename:
        plt.savefig(filename, format='svg')
    else:
        plt.show()
    # close the plot
    plt.close()

    
def scatter_plot(xvalues, yvalues, xlabel, ylabel, title, filename=None):
    """Create a scatter plot from given values.
    
    Args:
        xvalues: The x values to plot
        yvalues: The y values to plot
        xlabel: The label of the x-axis
        ylabel: The label of the y-axis
        title: The title of the chart
        filename: Filename to save chart to (in SVG format)

    Notes:
        If filename is given, chart is saved and not displayed.

    """
    # TODO
    plt.figure()
    plt.scatter(xvalues, yvalues)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    if filename:
        plt.savefig(filename, format='svg')
    else:
        plt.show()
    # close the plot
    plt.close()


def box_plot(distributions, labels, xlabel, ylabel, title, filename=None):
    """Create a box and whisker plot from given values.
    
    Args:
        distributions: The distribution for each box
        labels: The label of each corresponding box
        xlabel: The label of the x-axis
        ylabel: The label of the y-axis
        title: The title of the chart
        filename: Filename to save chart to (in SVG format)

    Notes:
        If filename is given, chart is saved and not displayed.

    """
    # TODO
    plt.figure()
    plt.boxplot(distributions, zorder = 3)
    ticks = [i+1 for i in range(len(labels))]
    plt.xticks(ticks, labels)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    if filename:
        plt.savefig(filename, format='svg')
    else:
        plt.show()
    # close the plot
    plt.close()
    
