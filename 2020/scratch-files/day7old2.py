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

    def traverse_nodepath(self, startname: Optional[str] = None, found: Set['BagNode'] = None, count: int = 0,
                          direction: str = 'upstream') -> Tuple[int, Set['BagNode']]:
        startname = startname or self.name
        found = found or set()
        if direction == 'upstream':
            cons = self.con_in
            src_or_tgt = 'source'
        elif direction == 'downstream':
            cons = self.con_out
            src_or_tgt = 'target'
        else:
            raise ValueError(f"Invalid direction {direction}. Valid directions: 'upstream', 'downstream'.")

        if not cons:
            return (count, {self},) if self.name != startname else (count, set(),)

        for conn in cons:
            countfound = conn.__getattribute__(src_or_tgt).traverse_nodepath(startname, found, count, direction)
            count += conn.weight + countfound[0]
            found |= countfound[1]
        found |= {con.__getattribute__(src_or_tgt) for con in cons}
        return count, found

    def __repr__(self):
        return self.name


class AcyclicGraph:
    rule_key_rex = re.compile(r'^(\w+ \w+) bag')
    can_contain_rex = re.compile(r'(\d+) (\w+ \w+)')

    def __init__(self):
        self.nodes: Dict[str, BagNode] = {}
        self.cons = []
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

    def add_node(self, node: Union[str, BagNode]) -> NoReturn:
        nodename = node.name if hasattr(node, 'name') else node

        if nodename not in self.nodes:
            self.nodes[nodename] = BagNode(node)
        self.num_nodes = len(self.nodes)

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
    # rulepath = Path(Path(__file__).parent / 'testinput2_day7.txt')
    rulepath = Path(Path(__file__).parent / 'testinput2_day7.txt')
    rules = read_rules(rulepath)
    graph = AcyclicGraph.from_rules(rules)

    targetbag = 'shiny gold'

    can_contain_targetbag_set = graph[targetbag].traverse_nodepath(direction='downstream')

    print(f"{len(can_contain_targetbag_set)} bags can hold target bag {targetbag}")
