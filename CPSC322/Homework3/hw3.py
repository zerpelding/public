"""Test data visualization for CPSC 322 HW-3. 

Data visualization tests

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""

import pytest
from data_util import *
from data_table import *


def test_dot_chart():
    xvals = [1,2,3,3,6,5,4,3,5,2,2,4,3]
    xlabel = 'Pairs of Shoes'
    title = 'How many pairs of shoes do you own?'
    dot_chart(xvals, xlabel, title)

def test_pie_chart():
    values = [1,2,3,3,6]
    labels = 'hamster', 'turtle', 'fish', 'cat', 'dog'
    title = 'Popular Pets'
    pie_chart(values, labels, title)

def test_bar_chart():
    bar_names = ['living room', 'kitchen', 'dining room', 'bathroom', 'bedroom']
    bar_values = [4,3,1,1,2]
    xlabel = 'Rooms in the House'
    ylabel = 'Number of Windows'
    title = 'Number of Windows by Room'
    bar_chart(bar_values, bar_names, xlabel, ylabel, title)

def test_scatter_plot():
    xvalues = [4,2,5,3,5,7,2]
    yvalues = [8,4,8,3,5,10,5]
    xlabel = 'Height (in)'
    ylabel = 'Weight (oz)'
    title = 'Apple Weight by Height'
    scatter_plot(xvalues, yvalues, xlabel, ylabel, title)

def test_box_plot():
    distributions = [11, 7, 10, 5, 4, 3, 5, 6,2], [9,7,8,3,5,5,6,3, 6, 9, 3], [5,4,2,2,4,5,2,5, 5, 7, 4]
    labels = ['honey crisp', 'red delicious', 'fuji']
    xlabel = 'Apple Types'
    ylabel = 'Apple Weights (oz)'
    title = 'Apple Weights by Type'
    box_plot(distributions, labels, xlabel, ylabel, title)
