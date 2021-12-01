
from typing import List, Tuple

#@njit()
#def cheat() -> Tuple[int, int]:
getallen: List[int] = [18, 8, 0, 5, 4, 1]
waar: List[int] = [1, 2, 3, 4, 5, 6]
waarnu: int = 7
laatste: int = 20
for beurt in range(29999993):
    if laatste in getallen:
        for index, getal in enumerate(getallen):
            if getal == laatste:
                laatste = waarnu - waar[index]
                waar[index] = waarnu
                break
    else:
        getallen.append(laatste)
        waar.append(waarnu)
        laatste = 0
    if beurt == 2012:
        laatste1: int = laatste
    if beurt % 1000 == 0:
        print("beurt:", beurt)
        print("aantal getallen:", len(getallen))
    waarnu += 1
    if beurt > 1e5:
        break
#return laatste1, laatste


#if __name__ == '__main__':
    #laatste1, laatste = cheat()
#print('(1):', laatste1, '(2):', laatste)