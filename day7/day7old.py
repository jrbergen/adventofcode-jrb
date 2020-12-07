from pathlib import Path
import re
from typing import List, Optional, Union, Set, Dict


class BagNode:

    def __init__(self, name: str, children: Optional[List['BagNode']] = None,
                 kidamounts: Optional[List[int]] = None):
        self.name = name
        self.children = set()
        self.parents = set()
        self.child_amounts: Dict[str, int] = {}
        self.num_children = len(self.children)
        self.num_parents = len(self.parents)

        if children and kidamounts:
            self.add_children(children, kidamounts)

    def add_children(self, kiddos: List[Union['BagNode', str]], kidamounts: List[int]):
        kiddos = kiddos if type(kiddos) == list else [kiddos]
        for kiddo, kidamount in zip(kiddos, kidamounts):
            if type(kiddo) == str:
                if kiddo in self.child_amounts:
                    continue
                self.child_amounts[kiddo] = kidamount
                kiddo = BagNode(name=kiddo)
            if kiddo not in self.children:
                self._add_child(kiddo)

    def _add_child(self, child: 'BagNode', childamount: int):
        if child == self:
            return
        self.children |= {child}
        self.child_amounts[child.name] = childamount
        child._add_parent(self)
        self.num_children = len(self.children)

    def _add_parent(self, parent: 'BagNode'):
        self.parents |= {parent}
        self.num_parents = len(self.parents)

    def traverse_parents(self, start: str, curparents: Optional[Set] = None) -> Set['BagNode']:
        curparents = curparents or set()
        if not self.parents:
            return {self} if self.name != start else {}
        for parent in self.parents:
            curparents |= parent.traverse_parents(curparents)
        return curparents | self.parents

    def __repr__(self):
        return "".join([f"{self.__class__.__name__}(name={self.name}, num_parents={self.num_parents},",
                        f" num_children={self.num_children})"])


class Graph:
    rule_key_rex = re.compile(r'^(\w+ \w+) bag')
    can_contain_rex = re.compile(r'(\d+) (\w+ \w+)')

    def __init__(self):
        self.nodes: dict = {}
        self.num_nodes: int = 0

    def add_node(self, node: Union[str, BagNode], kiddonames: Optional[List[str]] = None,
                 kiddo_amounts: Optional[List[int]] = None):
        nodename = node.name if hasattr(node, 'name') else node
        if nodename not in self.nodes:
            self.nodes[nodename] = BagNode(name=nodename)

        kiddonames = [] or kiddonames
        for kidname, kidamount in zip(kiddonames, kiddo_amounts):
            if kidname not in self.nodes:
                self.nodes[kidname] = BagNode(name=kidname)
                self.nodes[kidname]._add_parent(self.nodes[nodename])

            if self.nodes[kidname] not in self.nodes[nodename].children:
                self.nodes[nodename]._add_child(self.nodes[kidname], childamount=kidamount)

        self.num_nodes = len(self.nodes)

    def sort_nodes(self, reverse: bool = True):
        self.nodes = {k: self.nodes[k] for k in sorted(self.nodes, reverse=reverse)}

    def find_parents(self, childname: str):
        if childname not in self.nodes:
            raise ValueError(f"Nodename {childname} is not part of this graph")
        return self.nodes[childname].traverse_parents(start=childname)

    @classmethod
    def from_rules(cls, rules: List[str]) -> 'DirectedAcyclicGraph':
        _graph = cls()
        for rule in rules:
            curnode = cls.rule_key_rex.search(rule).groups()[0]
            kiddo_amounts, curnode_kiddos = ([], [],) or zip(*cls.can_contain_rex.findall(rule))
            kiddo_amounts = [int(amount) for amount in kiddo_amounts]
            _graph.add_node(curnode, curnode_kiddos, kiddo_amounts)
        _graph.sort_nodes()
        return _graph

    def __iter__(self):
        yield from self.nodes.items()

    def __getitem__(self, key: str):
        return self.nodes[key]

    def __repr__(self):
        return f'{self.__class__.__name__}(num_nodes={self.num_nodes})'


def read_rules(inpath: Path) -> List[str]:
    return inpath.read_text().split('\n')


if __name__ == '__main__':
    #rulepath = Path(Path(__file__).parent / 'testinput2_day7.txt')
    rulepath = Path(Path(__file__).parent / 'testinput1_day7.txt')
    rules=read_rules(rulepath)
    graph = Graph.from_rules(rules)

    targetbag = 'shiny gold'

    can_contain_targetbag_set = graph.find_parents(targetbag)

    print(f"{len(can_contain_targetbag_set)} bags can hold target bag {targetbag}")

