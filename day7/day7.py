import re
from pathlib import Path
from typing import List, Optional, Union, Dict, NoReturn, Set, Tuple


class NodeConnection:
    source: "BagNode"
    target: "BagNode"
    weight: int

    def __init__(self, source: "BagNode", target: "BagNode", weight: int = 0):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return f'({self.source} -> {self.target}) * {self.weight}'


class BagNode:
    name: str
    cons: List[NodeConnection]
    con_in: List[NodeConnection]
    con_out: List[NodeConnection]

    def __init__(self, name: str):
        self.name = name
        self.cons = []
        self.con_in = []
        self.con_out = []
        self.con_in_names, self.con_out_names = [], []
        self.num_incoming, self.num_outgoing = 0, 0

    def traverse_nodes_upstream(self, startname: Optional[str] = None,
                                found: Set['BagNode'] = None) -> Set['BagNode']:
        startname = startname or self.name
        found = found or set()

        if not self.con_in:
            return {self} if self.name != startname else set()

        for conn in self.con_in:
            found |= conn.source.traverse_nodes_upstream(startname, found)
        return found | {con.source for con in self.con_in}


    def traverse_paths_downstream(self, startnode: Optional['BagNode'] = None,
                                  lastnode: Optional['BagNode'] = None) -> Set['BagNode']:

        startnode = startnode or self
        lastnode = lastnode or startnode
        for conn in curnode.con_out:

            path = curnode.traverse_paths_downstream(lastnode)


        paths_traversed = False
        curnode = startnode
        cumsum = 0
        while not paths_traversed:
            visited = []
            nextcons = []
            for conn in curnode.con_out:
                cumsum += conn.weight
                visited.append(conn)
                nextcons.extend(conn.target.con_out if conn.target.con_out not in visited)




        curname = startname or curname
        found = found or set()

        if not self.con_out:
            return {self} if self.name != startname else set()

        for conn in self.con_in:
            found |= conn.source.traverse_nodes_upstream(curname, found)
    #     return found | {con.source for con in self.con_in}
    #
    # def traverse_edges_downstream(self, startname: Optional[str] = None,
    #                               connections: Set[NodeConnection] = None) -> Set[NodeConnection]:
    #     startname = startname or self.name
    #     connections = connections or set()
    #
    #     if not self.con_out:
    #         return connections
    #     connections |= set(self.con_out)
    #
    #     for conn in self.con_out:
    #         connections |= conn.target.traverse_edges_downstream(startname, connections)
    #
    #     return connections

    def __repr__(self):
        return self.name

class DirectedAcyclicGraph:
    rule_key_rex = re.compile(r'^(\w+ \w+) bag')
    can_contain_rex = re.compile(r'(\d+) (\w+ \w+)')

    def __init__(self):
        self.nodes: Dict[str, BagNode] = {}
        self.cons: List[NodeConnection] = []
        self.srcnodes: List[str] = []
        self.tgtnodes: List[str] = []

        self.num_nodes: int = 0

    def connect(self, source_node: str, target_node: str, weight: int):
        for node in (source_node, target_node,):
            if node not in self.nodes:
                self.add_node(node)

        src, tgt = self.nodes[source_node], self.nodes[target_node]
        if src == tgt:
            raise ValueError("Acyclic graph does not support self-referencing nodes.")

        connection = NodeConnection(src, tgt, weight)

        src.num_outgoing += 1
        src.con_out_names.append(target_node)
        src.con_out.append(connection)

        tgt.num_incoming += 1
        tgt.con_in_names.append(source_node)
        tgt.con_in.append(connection)

        self.cons.append(connection)
        self.srcnodes = [node.name for node in self.nodes.values() if node.con_out]
        self.tgtnodes = [node.name for node in self.nodes.values() if node.con_in]

    def add_node(self, node: Union[str, BagNode]) -> NoReturn:
        nodename = node.name if hasattr(node, 'name') else node

        if nodename not in self.nodes:
            self.nodes[nodename] = BagNode(node)
        self.num_nodes = len(self.nodes)


    def traverse_connections(self, startnode: str, curnodes: Optional[str] = None, cumsum: int = 0):

        curnodes = [startnode] or curnodes

        while curnodes:
            cumsum += sum(con.weight for con in self.cons if con.source.name == curnode)
        for connection in self.cons:
            if connection.source.name == curnode:

                curnode =

                #!BOEKENLEGGER


    @classmethod
    def from_rules(cls, rules: List[str]) -> 'DirectedAcyclicGraph':
        _graph = cls()
        for rule in rules:
            curnode = cls.rule_key_rex.search(rule).groups()[0]
            _graph.add_node(curnode)
            for tgt_weight, tgt_name in cls.can_contain_rex.findall(rule):
                tgt_weight = int(tgt_weight)
                _graph.connect(curnode, tgt_name, tgt_weight)
        return _graph

    def __iter__(self):
        yield from self.nodes.items()

    def __getitem__(self, key: str):
        return self.nodes[key]

    def __repr__(self):
        if hasattr(self, 'nodes'):
            return f"{self.__class__.__name__}(nodes: {', '.join(self.nodes.keys())})"
        else:
            return f"{self.__class__.__name__}()"


def read_rules(inpath: Path) -> List[str]:
    return inpath.read_text().split('\n')


if __name__ == '__main__':
    rulepath = Path(Path(__file__).parent / 'input_day7.txt')
    rules = read_rules(rulepath)
    graph = DirectedAcyclicGraph.from_rules(rules)

    targetbag = 'shiny gold'
    can_contain_targetbag_set = graph[targetbag].traverse_nodes_upstream()
    downstream_connections = graph.traverse_edges_downstream(targetbag)
    #downstream_connections = graph[targetbag].traverse_edges_downstream()
    #nbags = sum(conn.weight for conn in downstream_connections)
    ##nbags =

    print(f"Solution 1: {len(can_contain_targetbag_set)} bags can hold target bag {targetbag}")
    print(f"Solution 2: {targetbag} will have to contain {nbags} to pass airport security")
