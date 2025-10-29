"""
This module contains a class for creating sortable digraphs from our versatile digraph objects

Outlines a method for applying topological sort to the graph
"""
from collections import deque

class VersatileDigraph:
    """
    A class for making directed graphs made of nodes and edges

    Created versatile digraph objects that contain a dictionary for nodes and a dictionary for
    edges, while allowing the graph to be examined and modified using functions

    Attributes:
        nodes (dict): a dictionary with the key as node_id and the value as another dictionary with
        key 'value' and value as the node_value
        edges (dict): a dictionary with the key as start_node_id and the value as another
        dictionary with key edge_name and value as an additional dictionary with keys
        'end_node_id' and 'edge_weight' and values end_node_id and edge_weight
    """
    def __init__(self):
        """
        A function for initializing the versatile digraph objects

        Attributes:
            self: the object
        """
        self.nodes = {} # nodes will be a dict of dicts
        self.edges = {} # edges will be a dict of dict of dicts

    def add_edge(self, start_node_id, end_node_id, **kwargs):
        """
        A function for adding an edge to the digraph

        Attributes:
            self: the object
            start_node_id: starting node of the edge
            end_node_id: ending node of the edge
            end_node_value: value of the end node
            edge_name: identifier for the edge
            edge_weight: weight affiliated with the edge
        """
        # extract values from kwargs with defaults
        start_node_value = kwargs.get('start_node_value', None)
        end_node_value = kwargs.get('end_node_value', None)
        edge_name = kwargs.get('edge_name', None)
        edge_weight = kwargs.get('edge_weight', None)

        # checks for valid inputs
        check1 = isinstance(start_node_id, str)
        check2 = isinstance(end_node_id, str)
        if not (check1 and check2):
            raise TypeError("start_node_id and end_node_id must be strings.")

        if edge_name is not None and not isinstance(edge_name, str):
            raise TypeError("edge_name must be a string.")
        if edge_weight is not None:
            if not isinstance(edge_weight, (int, float)):
                raise TypeError("edge_weight must be a number.")
            if edge_weight <= 0:
                raise ValueError("edge_weight must be positive")
        if start_node_value is not None and not isinstance(start_node_value, (int, float)):
            raise TypeError("start_node_value must be a number.")
        if end_node_value is not None:
            check6 = isinstance(end_node_value, (int, float))
            if not check6:
                raise TypeError("end_node_value must be a number.")
        # ensure node exists
        if start_node_id not in self.nodes:
            self.add_node(start_node_id, start_node_value)
        if end_node_id not in self.nodes:
            self.add_node(end_node_id, end_node_value)
        # ensure start_node_id is in self.edges
        if start_node_id not in self.edges:
            self.edges[start_node_id] = {}
        # ensure edge_name is unique
        if edge_name is not None and edge_name in self.edges[start_node_id]:
            raise ValueError(f"Edge with name '{edge_name}' already exists from node \
            '{start_node_id}'")
        self.edges[start_node_id][edge_name] = {'end_node_id': end_node_id, \
                                                'edge_weight': edge_weight}

    def add_node(self, node_id, node_value=0):
        """
        A function for adding a node to the digraph

        Attributes:
            self: the object
            node_id: node being added
            node_value: value of the node being added
        """
        check1 = isinstance(node_id, str)
        if check1:
            pass
        else:
            node_id = str(node_id)
        if node_id in self.nodes:
            raise ValueError("node already exists in graph")
        if node_value is not None:
            check4 = isinstance(node_value, (int, float))
            if check4:
                pass
            else:
                raise TypeError("node_value must be a number.")
        if node_id not in self.nodes:
            self.nodes[node_id] = {"value": node_value}

    def get_nodes(self):
        """
        A function for returning a list of nodes

        Attributes:
            self: the object
        """
        node_list = list(self.nodes.keys())
        return node_list

    def get_edge_weight(self, start_node, end_node):
        """
        A function for getting the edge weight between two nodes

        Attributes:
            start_node: starting node of the edge
            end_node: ending node of the edge
        """
        check1 = isinstance(start_node, str)
        check2 = isinstance(end_node, str)
        if check1 and check2:
            pass
        else:
            raise TypeError("start_node_id and end_node_id must be strings.")
        if start_node not in self.edges:
            raise KeyError("start node not in map")
        for edge_name in self.edges[start_node]:
            if self.edges[start_node][edge_name]['end_node_id'] == end_node:
                return self.edges[start_node][edge_name]['edge_weight']
        raise KeyError("Path not found")

    def get_node_value(self, node_id):
        """
        A function for getting the value of a node

        Attributes:
            self: the object
            node_id: node of interest
        """
        if node_id not in self.nodes:
            raise KeyError("node not in map")
        return self.nodes[node_id]['value']

    def print_graph(self):
        """
        A function for printing out the versatile digraph

        Attributes:
            self: the object
        """
        for node_id, node_data in self.nodes.items():
            node_value = node_data['value']
            print(f"Node {node_id} with value {node_value}")
        for start_node_id, outgoing_edges in self.edges.items():
            for edge_name, edge_details in outgoing_edges.items():
                end_node_id = edge_details['end_node_id']
                edge_weight = edge_details['edge_weight']
                print(
                    f"Edge from {start_node_id} to {end_node_id} with weight {edge_weight} "
                    f"and name {edge_name}"
                )

    def predecessors(self, node_id):
        """
        A function for getting the nodes with edges that lead to the input node

        Attributes:
            self: the object
            node_id: starting node of the edge
        """
        check1 = isinstance(node_id, str)
        if check1:
            pass
        else:
            raise TypeError("node_id must be a string.")

        if node_id not in self.nodes:
            raise KeyError("node_id not in graph")
        return [start_node_id for start_node_id, edges in self.edges.items() \
                for edge_names, edge_info in edges.items() \
                if edge_info['end_node_id'] == node_id]

    def successors(self, node_id):
        """
        A function for getting the nodes that come after a given node

        Attributes:
            self: the object
            node_id: id of the imnput node
        """
        check1 = isinstance(node_id, str)
        if check1:
            pass
        else:
            raise TypeError("node_id must be a string.")
        if node_id not in self.nodes:
            raise KeyError("node_id not in graph")
        if node_id not in self.edges:
            return []
        return [self.edges[node_id][edge_name]['end_node_id'] for edge_name \
                in self.edges[node_id]]

    def successor_on_edge(self, node_id, edge_name):
        """
        A function for accessing the end node from a given start node and edge name

        Attributes:
            self: the object
            node_id: starting node of the edge
            edge_name: identifier for the edge
        """
        check1 = isinstance(node_id, str)
        check2 = isinstance(edge_name, str)
        if check1 and check2:
            pass
        else:
            raise TypeError("node_id and edge_name must be strings.")
        if node_id not in self.edges:
            raise KeyError("node_id not in graph")
        if edge_name not in self.edges[node_id]:
            raise KeyError("edge not found in graph")
        return self.edges[node_id][edge_name]['end_node_id']

    def in_degree(self, node_id):
        """
        A function counting the number of edges leading to a node

        Attributes:
            self: the object
            node_id: id for the input node
        """
        check1 = isinstance(node_id, str)
        if check1:
            pass
        else:
            raise TypeError("node_id must be a string.")
        if node_id not in self.nodes:
            raise KeyError("node_id not in graph")
        return sum(1 for start_node_id, edges in self.edges.items() \
                   for edge_name, edge_info in edges.items() \
                   if edge_info['end_node_id'] == node_id)

    def out_degree(self, node_id):
        """
        A function for counting the number of edges from a node

        Attributes:
            self: the object
            node_id: id of the input node
        """
        check1 = isinstance(node_id, str)
        if check1:
            pass
        else:
            raise TypeError("node_id must be a string.")
        if node_id not in self.nodes:
            raise KeyError("node_id not in graph")
        return sum(1 for edge_name in self.edges[node_id])

    def plot_graph(self):
        """
        A function for plotting the graph using graphviz

        Attributes:
            self: the object
        """
        try:
            import graphviz  # pylint: disable=import-outside-toplevel
        except ImportError as ex:
            raise ImportError(
                "The 'plot_graph' function requires the 'graphviz' library. "
                "Please install it by running: pip install graphviz"
            ) from ex
        grapher = graphviz.Digraph()
        for node_id, node_data in self.nodes.items():
            grapher.node(node_id, label = str(node_data['value']))
        for start_node_id, outgoing_edges in self.edges.items():
            sni = start_node_id
            for edge_name, edge_details in outgoing_edges.items():
                edge_weight_str = str(edge_details['edge_weight']) if \
                edge_details['edge_weight'] is not None else "None"
                edge_data = f"edge name: {edge_name}, edge weight: {edge_weight_str}"
                grapher.edge(sni, edge_details['end_node_id'], label = edge_data)
        grapher.render('321_digraph_visualization', view=True, format='png')

    def plot_edge_weights(self):
        """
        A function for plotting the edge weights using Bokeh

        Attributes:
            self: the object
        """
        try:
            from bokeh.plotting import figure, show  # pylint: disable=import-outside-toplevel
        except ImportError as ex:
            raise ImportError(
                "The 'plot_edge_weights' function requires the 'bokeh' library."
                "Please install it by running: pip install bokeh"
            ) from ex
        weights = []
        names = []
        for start_node_id, outgoing_edges in self.edges.items():
            start_node_id = str(start_node_id) # pylint
            for edge_name, edge_details in outgoing_edges.items():
                names.append(edge_name)
                if edge_details['edge_weight'] is not None:
                    weights.append(edge_details['edge_weight'])
        grapher = figure(title = "Edge Weights", x_axis_label = "edges", \
                          y_axis_label = "weight")
        grapher.vbar(x = names, top = weights, width = 0.9)
        show(grapher)

class SortableDigraph(VersatileDigraph):
    """
    A child class for making sortable graphs made of nodes and edges

    Created sortable digraph objects that contain a can use topological sort on a DAG
    """
    def top_sort(self):
        """
        A function for topological sorting

        Attributes:
            self: the object
        """
        count = {}
        for node in self.get_nodes():
            count[node] = self.in_degree(node)
        que = [node for node, deg in count.items() if deg == 0]
        es = []
        while que:
            mynode = que.pop(0)
            es.append(mynode)
            for v in self.successors(mynode):
                count[v] -= 1
                if count[v] == 0:
                    que.append(v)
        return es

class TraversableDigraph(SortableDigraph):
    """
    A child class for making transversible graphs made of nodes and edges

    Creates transversable digraph objects that can be navigated through BFS or DFS
    """
    def dfs(self, start_node):
        """
        A function for breadth first transversal

        Attributes:
            self: the object
            start_node: node to begin transversal
        """
        visited = set()
        stack = [start_node]
        while stack:
            current_node = stack.pop()
            if current_node not in visited:
                visited.add(current_node)
                yield current_node
                neighbors = self.successors(current_node)
                stack.extend(reversed(neighbors))

    def bfs(self, start_node):
        """
        A function for depth first transversal

        Attributes:
            self: the object
            start_node: node to begin transversal
        """
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        first_node = True
        while queue:
            current_node = queue.popleft()
            if first_node:
                first_node = False
            else:
                yield current_node
            for v in sorted(self.successors(current_node)):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

class DAG(TraversableDigraph):
    """
    A child class for making DAGs made of nodes and edges

    Creates directed acyclical graphs that redefine the add_edge method
    """
    def add_edge(self, start_node_id, end_node_id, **kwargs):
        """
        Overrides the function for adding an edge to DAGs

        Attributes:
            self: the object
            start_node_id: starting node of the edge
            end_node_id: ending node of the edge
            end_node_value: value of the end node
            edge_name: identifier for the edge
            edge_weight: weight affiliated with the edge
        """
        # extract values from kwargs with defaults
        start_node_value = kwargs.get('start_node_value', None)
        end_node_value = kwargs.get('end_node_value', None)
        edge_name = kwargs.get('edge_name', None)
        edge_weight = kwargs.get('edge_weight', None)

        # checks for valid inputs
        if not all(isinstance(n, str) for n in (start_node_id, end_node_id)):
            raise TypeError("start_node_id and end_node_id must be strings.")

        if edge_name is not None and not isinstance(edge_name, str):
            raise TypeError("edge_name must be a string.")

        if edge_weight is not None:
            if not isinstance(edge_weight, (int, float)) or edge_weight <= 0:
                raise ValueError("edge_weight must be a positive number.")

        for name, value in (("start_node_value", start_node_value),
                    ("end_node_value", end_node_value)):
            if value is not None and not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a number.")
        # ensure node exists
        for node_id, node_value in ((start_node_id, start_node_value),
                            (end_node_id, end_node_value)):
            if node_id not in self.nodes:
                self.add_node(node_id, node_value)
        # ensure start_node_id is in self.edges
        if start_node_id not in self.edges:
            self.edges[start_node_id] = {}
        # ensure edge_name is unique
        if edge_name is not None and edge_name in self.edges[start_node_id]:
            raise ValueError(f"Edge with name '{edge_name}' already exists from node \
            '{start_node_id}'")
        # check for cycles
        if end_node_id in self.nodes:
            for node in self.dfs(end_node_id):
                if node == start_node_id:
                    raise ValueError("Cannot add a cycle to the DAG")
        # add edge
        self.edges[start_node_id][edge_name] = {'end_node_id': end_node_id, \
                                                'edge_weight': edge_weight}
