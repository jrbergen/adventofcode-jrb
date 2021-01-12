import re
from functools import reduce
from pathlib import Path
from typing import List, Tuple, Dict, NoReturn, Optional


def parse_input(filename: Path) -> Tuple[Dict[str, List[int]],
                                         List[int],
                                         List[List[int]]]:
    numrex = re.compile('\d+')
    with open(filename, 'r') as fhandle:
        fields, yourticket, nearbytickets = fhandle.read().split('\n\n')

    fields = {field.split(':')[0]: [int(lubound)
                                    for lubound in numrex.findall(field.split(':')[1])]
              for field in fields.split('\n')}
    yourticket = [int(x) for x in yourticket.split('\n')[-1].split(',')]
    nearbytickets = [[int(x) for x in nearbyticket.split(',')]
                     for nearbyticket in nearbytickets.replace('nearby tickets:\n', '').split('\n') if nearbyticket]
    return fields, yourticket, nearbytickets


def get_field_index(fields: Dict[str, List[int]], fieldname: str) -> int:
    return list(fields.keys()).index(fieldname)


def count_valid_fields_total(fields: Dict[str, List[int]],
                             tickets: List[List[int]],
                             fieldname: str) -> int:
    fieldidx = get_field_index(fields, fieldname)

    n_valid = 0
    for ticket in tickets:
        lbounds, ubounds = fields[fieldname][::2], fields[fieldname][1::2]
        for lbound, ubound in zip(lbounds, ubounds):
            if lbound <= ticket[fieldidx] <= ubound:
                n_valid += 1
    return n_valid


def checkvalid_single_field(fields: Dict[str, List[int]],
                            fieldname: str,
                            checkval: int) -> bool:
    lbounds, ubounds = fields[fieldname][::2], fields[fieldname][1::2]
    for lbound, ubound in zip(lbounds, ubounds):
        if lbound <= checkval <= ubound:
            return True
    return False


def get_allbounds(fields: Dict[str, List[int]]) -> Tuple[List[int], List[int]]:
    lbounds, ubounds = [], []
    for bounds in fields.values():
        lbounds.extend(bounds[::2])
        ubounds.extend(bounds[1::2])
    return lbounds, ubounds


def get_bounds_per_field(fields: Dict[str, List[int]]) -> Tuple[List[List[int]],
                                                                List[List[int]]]:
    lbounds, ubounds = [], []
    for bounds in fields.values():
        lbounds.append(bounds[::2])
        ubounds.append(bounds[1::2])
    return lbounds, ubounds


def check_any_invalid(fields: Dict[str, List[int]], ticket: List[int]):
    lbounds, ubounds = get_allbounds(fields)
    min_lbound, max_ubound = min(lbounds), max(ubounds)
    for ticketval in ticket:
        if ticketval < min_lbound or ticketval > max(ubounds):
            return True
        elif not any([lb <= ticketval <= ub for lb, ub in zip(lbounds, ubounds)]):
            return True
    return False


def discard_invalid_tickets(fields: Dict[str, List[int]],
                            tickets: List[List[int]]) -> List[List[int]]:
    lbounds, ubounds = get_allbounds(fields)
    min_lbound, max_ubound = min(lbounds), max(ubounds)
    valid_tickets = []
    for ticket in tickets:
        for ticketval in ticket:
            if ticketval < min_lbound or ticketval > max(ubounds):
                break
            elif not any([lb <= ticketval <= ub for lb, ub in zip(lbounds, ubounds)]):
                break
        else:
            valid_tickets.append(ticket)
    return valid_tickets


def get_invalid_values(fields: Dict[str, List[int]], tickets: List[List[int]]) -> List[int]:
    lbounds, ubounds = get_allbounds(fields)
    min_lbound, max_ubound = min(lbounds), max(ubounds)
    invalid_vals = []
    for ticket in tickets:
        for ticketval in ticket:
            if ticketval < min_lbound or ticketval > max(ubounds):
                invalid_vals.append(ticketval)
            elif not any([lb <= ticketval <= ub for lb, ub in zip(lbounds, ubounds)]):
                invalid_vals.append(ticketval)
    return invalid_vals


def get_possible_field_idx_dict(fields: Dict[str, List[int]],
                                tickets: List[List[int]]) -> Dict[str, List[int]]:
    possible_idx = {fieldname: [] for fieldname in fields}
    transposed_tickets = list(zip(*tickets))
    for fieldname in fields:
        possible_idx[fieldname] = find_possible_field_idx(fieldname=fieldname,
                                                          transposed_tickets=transposed_tickets)
    return possible_idx


def find_possible_field_idx(fieldname: str,
                            transposed_tickets: List[Tuple[int, ...]]) -> List[int]:
    possible_field_idx = []
    for col_idx, ticketcol in enumerate(transposed_tickets):
        if all([checkvalid_single_field(fields, fieldname, checkval=ticketval)
                for ticketval in ticketcol]):
            possible_field_idx.append(col_idx)
    return possible_field_idx


def eliminate_field_candidates_recursive(
        fieldidx_dict: Dict[str, List[int]],
        assigned_field_idx_dict: Optional[Dict[str, int]] = None) -> Dict[str, int]:

    assigned_field_idx_dict = assigned_field_idx_dict or {fieldname: None for fieldname in fieldidx_dict}

    entrylens = [len(entry) for entry in fieldidx_dict.values()]
    if not entrylens:
        return assigned_field_idx_dict

    best_candidate_key = [x for _, x in sorted(zip(entrylens, fieldidx_dict.keys()))][0]
    best_candidate_val = fieldidx_dict[best_candidate_key]

    assert len(best_candidate_val) == 1

    best_candidate_val = best_candidate_val[0]

    assigned_field_idx_dict[best_candidate_key] = best_candidate_val

    new_fieldidx_dict = {key: [val for val in values if val != best_candidate_val]
                         for key, values in fieldidx_dict.items()}
    new_fieldidx_dict = {k: v for k, v in new_fieldidx_dict.items() if len(v)}

    assigned_field_idx_dict = eliminate_field_candidates_recursive(fieldidx_dict=new_fieldidx_dict,
                                                                   assigned_field_idx_dict=assigned_field_idx_dict)
    return assigned_field_idx_dict


def multiply_dict_vals_identified_by_keyword(assigned_field_idx_dict: Dict[str, int],
                                             yourticket: List[int],
                                             keyw='departure'):
    return reduce(lambda x, y: x*y,
                  [yourticket[val] for key, val in assigned_field_idx_dict.items() if keyw in key])


def part1(fields: Dict[str, List[int]], nearbytickets: List[List[int]]) -> NoReturn:
    invalid_values = get_invalid_values(fields=fields, tickets=nearbytickets)

    print(f"Part 1: the ticket scanning error rate = {sum(invalid_values)}.")


def part2(fields: Dict[str, List[int]],
          nearbytickets: List[List[int]],
          ownticket: List[int],
          keyw: str = 'departure') -> NoReturn:
    nearbytickets = discard_invalid_tickets(fields=fields, tickets=nearbytickets)
    alltickets = [ownticket] + nearbytickets

    field_idx_dict = get_possible_field_idx_dict(fields=fields, tickets=alltickets)

    field_assignments = eliminate_field_candidates_recursive(fieldidx_dict=field_idx_dict)

    answer = multiply_dict_vals_identified_by_keyword(assigned_field_idx_dict=field_assignments,
                                                      yourticket=ownticket)
    print(f"Part 2: multiplying the fields with the word {keyw} in their keys results in: {answer}")


if __name__ == '__main__':
    infile = Path('input_day16.txt')
    fields, yourticket, nearbytickets = parse_input(infile)

    part1(fields=fields, nearbytickets=nearbytickets)
    part2(fields=fields, ownticket=yourticket, nearbytickets=nearbytickets)
