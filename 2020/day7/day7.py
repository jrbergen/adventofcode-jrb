import re
from functools import reduce
from pathlib import Path
from typing import List, Optional, Union, Dict, NoReturn, Set


class NodeConnection:
    source: "BagNode"
    target: "BagNode"
    name: str
    weight: int

    def __init__(self, source: "BagNode", target: "BagNode", weight: int = 0):
        self.source = source
        self.target = target
        self.name = f'{self.source.name}->{self.target.name}'
        self.weight = weight

    def __repr__(self):
        return f'({self.source} -> {self.target}) * {self.weight}'


class BagNode:
    name: str
    cons: List[NodeConnection]
    con_in: List[NodeConnection]
    con_out: List[NodeConnection]
    visited: bool
    has_unvisited_kiddos: bool

    def __init__(self, name: str):
        self.name = name
        self.cons = []
        self.con_in = []
        self.con_out = []
        self.con_in_names, self.con_out_names = [], []
        self.num_incoming, self.num_outgoing = 0, 0
        self.visited = False
        self.has_unvisited_kiddos = False

    def traverse_nodes_upstream(self, startname: Optional[str] = None,
                                found: Set['BagNode'] = None) -> Set['BagNode']:
        startname = startname or self.name
        found = found or set()

        if not self.con_in:
            return {self} if self.name != startname else set()

        for conn in self.con_in:
            found |= conn.source.traverse_nodes_upstream(startname, found)
        return found | {con.source for con in self.con_in}

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'


class DirectedAcyclicGraph:
    rule_key_rex = re.compile(r'^(\w+ \w+) bag')
    can_contain_rex = re.compile(r'(\d+) (\w+ \w+)')

    def __init__(self, default_startnode: str):
        self.startnode = default_startnode
        self.nodes: Dict[str, BagNode] = {}
        self.connections = {}

        self.paths = []

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
        src.has_unvisited_kiddos = True

        tgt.num_incoming += 1
        tgt.con_in_names.append(source_node)
        tgt.con_in.append(connection)

        self.connections[connection.name] = connection

    def add_node(self, node: Union[str, BagNode]) -> NoReturn:
        nodename = node.name if hasattr(node, 'name') else node

        if nodename not in self.nodes:
            self.nodes[nodename] = BagNode(node)
        self.num_nodes = len(self.nodes)

    def dfs(self, path: Optional[List[BagNode]] = None, paths: Optional[list] = None):
        path = path or [self.startnode if type(self.startnode) == BagNode else self[self.startnode]]
        if type(path) == BagNode:
            path = [path]
        paths = paths or []
        lastnode: BagNode = path[-1]
        if lastnode in self and lastnode.con_out:
            for subnode in [conn.target for conn in self[lastnode.name].con_out]:
                new_path = path + [subnode]
                paths = self.dfs(new_path, paths)
        else:
            paths += [path]
        return paths

    @classmethod
    def from_rules(cls, rules: List[str], default_startnode: Optional[BagNode]) -> 'DirectedAcyclicGraph':
        _graph = cls(default_startnode)
        for rule in rules:
            if not rule:
                continue
            curnode = cls.rule_key_rex.search(rule).groups()[0]
            _graph.add_node(curnode)
            for tgt_weight, tgt_name in cls.can_contain_rex.findall(rule):
                tgt_weight = int(tgt_weight)
                _graph.connect(curnode, tgt_name, tgt_weight)
        return _graph

    def __iter__(self):
        yield from self.nodes.values()

    def __getitem__(self, key: str):
        return self.nodes[key]

    def __repr__(self):
        if hasattr(self, 'nodes'):
            return f"{self.__class__.__name__}(nodes: {', '.join(self.nodes.keys())})"
        else:
            return f"{self.__class__.__name__}()"

    def calc_nobags(self):
        cumsum = 0
        for path in self.paths:
            weights = [graph.connections[f'{curnode.name}->{nextnode.name}'].weight for
                       curnode, nextnode in zip(path[:-1], path[1:])]
            while len(weights) > 1:
                cumsum += reduce(lambda x, y: x * y, weights[1:]) + weights[0]
                weights = weights[1:]
        paths = self.paths
        #   weights = weights[:-1]
        [print(path) for path in self.paths]

        return cumsum


def read_rules(inpath: Path) -> List[str]:
    return inpath.read_text().split('\n')


if __name__ == '__main__':
    rulepath = Path(Path(__file__).parent / 'testinput2_day7.txt')
    rules = read_rules(rulepath)

    targetbag = 'shiny gold'

    graph = DirectedAcyclicGraph.from_rules(rules, default_startnode=targetbag)

    can_contain_targetbag_set = graph[targetbag].traverse_nodes_upstream()
    print(f"Solution 1: {len(can_contain_targetbag_set)} bags can hold target bag {targetbag}")

    graph.paths = graph.dfs()
    nbags = graph.calc_nobags()
    print(f"Solution 2: {targetbag} will have to contain {nbags} to pass airport security")
