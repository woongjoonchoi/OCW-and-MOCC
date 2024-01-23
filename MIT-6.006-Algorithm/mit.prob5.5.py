# ----------------------------------- #
# REWRITE SOLVE IMPLEMENTING PART (e) #
# ----------------------------------- #
MAX_CONFIG = 3674160
def solve(config):
    # Return a sequence of moves to solve config, or None if not possible
    # Fully explore graph using BFS
    parent, frontier ,sol_frontier,sol_parent= {config: None}, [config] ,[SOLVED] ,{SOLVED: None}
    start_parent_set = set()
    sol_parent_set = set()
    # print(f'config type :{type(config[0])} ,  ')
    intersection = set()
    unions = set()
    while len(frontier) != 0 and len(sol_frontier) != 0  and len(intersection) == 0 and len(unions) < MAX_CONFIG:
        frontier = explore_frontier(frontier, parent, True)
        
        
        sol_frontier = explore_frontier(sol_frontier,sol_parent,True)
        for k in frontier : start_parent_set.add(k) 
        for t in sol_frontier : sol_parent_set.add(t)
        intersection = start_parent_set & sol_parent_set
        unions |= start_parent_set | sol_parent_set
        
    print(f'intersecion : {intersection}')
    print('Searched %s reachable configurations' % (len(parent) + len(sol_parent)))
    # Check whether solved state visited and reconstruct path
    intersection = list(intersection)
    if intersection[0] in parent:
        path = path_to_config(intersection[0], parent)
        path_sol = path_to_config(intersection[0],sol_parent)
        # print(f'path : {path}')
        # print(f'path_sol : {path_sol}')
        # print(f'moves_from_path : {moves_from_path(path)}')
        # print(f'moves_from_path_sol : {moves_from_path(path_sol)}')
        
        path = path + path_sol[::-1][1:]
        return moves_from_path(path)
    return None
# --------------------------------------- #
# READ, BUT DO NOT MODIFY CODE BELOW HERE #
# --------------------------------------- #
# Pocket Cube configurations are represented by length 24 strings
# Each character repesents the color of a small cube face
# Faces are layed out in reading order of a Latin cross unfolding of the cube
SOLVED = '000011223344112233445555'
def config_str(config):
# Return config string representation as a Latin cross unfolding
    return """
    %s%s
    %s%s
    %s%s%s%s%s%s%s%s
    %s%s%s%s%s%s%s%s
    %s%s
    %s%s
    """ % tuple(config)
def shift(A, d, ps):
# Circularly shift values at indices ps in list A by d positions
    values = [A[p] for p in ps]
    k = len(ps)
    for i in range(k):
        A[ps[i]] = values[(i - d) % k]
def rotate(config, face, sgn):
# Returns new config by rotating input face of input config
# Rotation is clockwise if sgn == 1, counterclockwise if sgn == -1
    assert face in (0, 1, 2)
    assert sgn in (-1, 1)
    if face is None: return config
    new_config = list(config)
    if face == 0:
        shift(new_config, 1*sgn, [0,1,3,2])
        shift(new_config, 2*sgn, [11,10,9,8,7,6,5,4])
    elif face == 1:
        shift(new_config, 1*sgn, [4,5,13,12])
        shift(new_config, 2*sgn, [0,2,6,14,20,22,19,11])
    elif face == 2:
        shift(new_config, 1*sgn, [6,7,15,14])
        shift(new_config, 2*sgn, [2,3,8,16,21,20,13,5])
    return ''.join(new_config)
def neighbors(config):
# Return neighbors of config
    ns = []
    for face in (0, 1, 2):
        for sgn in (-1, 1):
            ns.append(rotate(config, face, sgn))
    return ns
def explore_frontier(frontier, parent, verbose = False):
# Explore frontier, adding new configs to parent and new_frontier
# Prints size of frontier if verbose is True
    if verbose:
        print('Exploring next frontier containing # configs: %s' % len(frontier))
    new_frontier = []
    for f in frontier:
        for config in neighbors(f):
            if config not in parent:
                parent[config] = f
                new_frontier.append(config)
    return new_frontier
def path_to_config(config, parent):
# Return path of configurations from root of parent tree to config
    path = [config]
    while path[-1] is not None:
        path.append(parent[path[-1]])
    path.pop()
    path.reverse()
    return path
def moves_from_path(path):
# Given path of configurations, return list of moves relating them
# Returns None if any adjacent configs on path are not related by a move
    moves = []
    for i in range(1, len(path)):
        move = None
        for face in (0, 1, 2):
            for sgn in (-1, 1):
                if rotate(path[i - 1], face, sgn) == path[i]:
                    move = (face, sgn)
                    moves.append(move)
        if move is None:
            return None
    return moves

def path_from_moves(config, moves):
    # Return the path of configurations from input config applying input moves
    path = [config]
    for move in moves:
        face, sgn = move
        config = rotate(config, face, sgn)
        path.append(config)
    return path
def scramble(config, n):
# Returns new configuration by appling n random moves to config
    from random import randint
    for _ in range(n):
        ns = neighbors(config)
        i = randint(0, 2)
        config = ns[i]
    return config
def check(config, moves, verbose = False):
# Checks whether applying moves to config results in the solved config
    if verbose:
        print('Making %s moves from starting configuration:' % len(moves))
    path = path_from_moves(config, moves)
    if verbose:
        print(config_str(config))
    for i in range(1, len(path)):
        face, sgn = moves[i - 1]
        direction = 'clockwise'
        if sgn == -1:
            direction = 'counterclockwise'
        if verbose:
            print('Rotating face %s %s:' % (face, direction))
            print(config_str(path[i]))
    return path[-1] == SOLVED
def test(config):
    print('Solving configuration:')
    print(config_str(config))
    moves = solve(config)
    if moves is None:
        print('Path to solved state not found... :(')
        return
    print('Path to solved state found!')
    if check(config, moves):
        print('Move sequence terminated at solved state!')
    else:
        print('Move sequence did not terminate at solved state... :(')
if __name__ == '__main__':
    config = scramble(SOLVED, 100)
    test(config)

