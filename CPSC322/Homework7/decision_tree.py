"""Classes and functions for representing and drawing basic decision
trees.

NAME: S. Bowers
DATE: Fall 2023
CLASS: CPSC 322

NOTE: To use the drawing function below you must install the graphviz
module, which can be done via the conda command:

    conda install python-graphviz

"""

from __future__ import annotations
from dataclasses import dataclass
from graphviz import Digraph



@dataclass
class LeafNode:
    """Represents a leaf node of a decision tree."""
    label: any
    count: int
    total: int

    def percent(self):
        """Return the percentage of occurrences of the leaf"""
        return (self.count / self.total) * 100


    
@dataclass
class AttributeNode:
    """Represents an attribute node of a decision tree."""
    name: str
    values: dict[str, AttributeNode | [LeafNode]]


    
def draw_tree(root, fname, display=False, att_clr='white',
              val_clr='white', leaf_clr='white'):
    """Draws a decision tree using graphviz. 

    Args:
        root: The root AttributeNode of a decision tree to draw.
        fname: The filename to save the graphviz and pdf file. 
        display: If true, displays the resulting PDF file. 
        att_clr: The color name of attribute nodes (default is no color).
        val_clr: The color name of value nodes (default is no color). 
        leaf_clr: The color name of leaf nodes (default is no color). 

    Notes: The given filename creates two files in the current
        directory. One with the Graphviz dot commands and the other a
        PDF file of the generated graph. For a list of color names supported by
        GraphViz see: https://graphviz.org/doc/info/colors.html

    """
    # helper function to draw the nodes and edges
    def draw(dot, dt_root):
        dt_root_id = str(id(dt_root))
        if type(dt_root) == AttributeNode:
            dot.node(dt_root_id, f'Attribute: {dt_root.name}', shape='rectangle',
                     style='filled', fillcolor=att_clr)
            for val in dt_root.values:
                val_id = f'"{dt_root_id}_{val}"'
                dot.node(val_id, f'Value: {val}', shape='oval',
                         style='filled', fillcolor=val_clr)
                dot.edge(dt_root_id, val_id)
                subtree_root = dt_root.values[val]
                if type(subtree_root) == AttributeNode: 
                    child_id = str(id(subtree_root))
                    dot.edge(val_id, child_id)
                    draw(dot, subtree_root)
                else:
                    for leaf in subtree_root:
                        child_id = str(id(leaf))
                        dot.edge(val_id, child_id)
                        draw(dot, leaf)
        elif type(dt_root) == LeafNode:
            p = round(dt_root.percent(), 2)
            stats = f'{dt_root.label} ({dt_root.count}, {dt_root.total}, {p}%)' 
            dot.node(dt_root_id, stats, shape='oval',
                     style='filled', fillcolor=leaf_clr)

    # create the graph
    dot = Digraph()
    dot.graph_attr['rankdir'] = 'TB'    
    if not root: 
        raise ValueError('expecting attribute node')
    if type(root) == list:
        for leaf in root: 
            draw(dot, leaf)
    else: 
        draw(dot, root)
    dot.render(fname, view=display)
    return dot

