import sys
from queue import PriorityQueue
from queue import Queue
from datetime import datetime

with open(sys.argv[1], 'r') as sfile:
    start = [list(map(int, line.split())) for line in sfile if line.strip() != "End of file"]

with open(sys.argv[2], 'r') as gfile:
    goal = [list(map(int, line.split())) for line in gfile if line.strip() != "End of file"]

dump = False

def tempm(puzzle):
    temp_puzzle=[]
    for i in puzzle:
        temp=[]
        for j in i:
            temp.append(j)
        temp_puzzle.append(temp)
    return  temp_puzzle

def zero_tile(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j]==0:
                return i,j

def any_tile(puzzle, any):
        for i in range(3):
            for j in range(3):
                if puzzle[i][j] == any:
                    return i,j
                
def bfs():
    class Node:
        def __init__(self, state, move, cost, depth, hueristic, parent):
            self.state=state 
            self.move=move 
            self.cost=cost 
            self.depth=depth 
            self.hueristic=hueristic
            self.parent=parent 
            
        def __lt__(self, other):
            return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

        def __repr__(self):
            return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def __str__(self):
            return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)
    
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')

    def man_hueristic(start_matrix, goal_matrix):
        total = 0
        for i in range(3):
            for j in range(3):
                if start_matrix[i][j] != goal_matrix[i][j]:
                    weight = start_matrix[i][j]
                    x,y = any_tile(goal_matrix, weight)
                    total += (abs(i-x) + abs(j-y))*weight
        return(total)

    fringe = Queue()
    closed = []
    nodes_ex = 0
    nodes_ge = 0
    node_pop = 0
    max_fri = 0

    s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
    fringe.put(s_state)

    while fringe:
        if max_fri < fringe.qsize():
            max_fri = fringe.qsize()
        
        crstate = fringe.get()
        node_pop += 1

        if crstate.state == goal:
            sol = []
            g_f = crstate
            while crstate.parent is not None:
                sol.append(crstate.move)
                crstate = crstate.parent
            sol.reverse()

            print("Solution path: ")
            for step in sol:
                print(step)
            print("nodes poped: ", node_pop)
            print("Nodes expanded: ", nodes_ex)
            print("Nodes generated: ", nodes_ge)
            print("Max fringe size: ", max_fri)
            print("solution found at", g_f.depth, "with the cost of", g_f.cost)
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n Goal node is {g_f} \n')
                    f.write(f'nodes poped: {node_pop} \n')
                    f.write(f'Nodes expanded: {nodes_ex} \n')
                    f.write(f'Nodes generated: {nodes_ge} \n')
                    f.write(f'Max fringe size: {max_fri} \n')
            return
            

        elif crstate.state not in closed :
            closed.append(crstate.state)
            nodes_ex += 1
            if dump == True:
                with open(filename, 'a') as f:
                        f.write(f'\n')
                        f.write(f'Generating Successor to < :{crstate} \n')
                        
            x, y = zero_tile(crstate.state)
            fringstr = ""
            count_succ = 0
            p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
            for i in p_pos:
                if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                    temp_m = tempm(crstate.state)
                    n = temp_m[i[0]][i[1]]
                    temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                    if i[0]>x and i[1]==y:
                        _move="up" + str(n)
                        nodes_ge += 1
                    elif i[0]<x and i[1]==y:
                        _move="Down" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]<y:
                        _move="Right" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]>y:
                        _move="left" + str(n)
                        nodes_ge += 1
                    count_succ +=1
                    child_node = Node(temp_m, _move, crstate.cost + n, crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                    fringe.put(child_node)
                    fringstr+=("< " +str(child_node)+" >\n")
            
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'{count_succ} successors generated \n')
                    cc = ''
                    for i in closed :
                        cc += str(i) + " , "
                    f.write(f'Closed: {cc} \n')
                    f.write(f'fringe:')    
                    for v in fringe.queue :
                        f.write(f'{v} \n')

def ucs():
    class Node:
        def __init__(self, state, move, cost, depth, hueristic, parent):
            self.state=state 
            self.move=move 
            self.cost=cost 
            self.depth=depth 
            self.hueristic=hueristic
            self.parent=parent 

        def __lt__(self, other):
            return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

        def __repr__(self):
            return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def __str__(self):
            return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)
    
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')   

    def man_hueristic(start_matrix, goal_matrix):
        total = 0
        for i in range(3):
            for j in range(3):
                if start_matrix[i][j] != goal_matrix[i][j]:
                    weight = start_matrix[i][j]
                    x,y = any_tile(goal_matrix, weight)
                    total += (abs(i-x) + abs(j-y))*weight
        return(total)

    fringe = PriorityQueue(0)
    closed = []
    nodes_ex = 0
    nodes_ge = 1
    node_pop = 0
    max_fri = fringe.qsize()

    s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
    fringe.put((s_state.cost, s_state))

    while fringe:
        if max_fri < fringe.qsize():
            
            max_fri = fringe.qsize()

        crstate = fringe.get()[1]
        node_pop += 1

        if crstate.state == goal:
            sol = []
            g_f = crstate
            while crstate.parent is not None:
                sol.append(crstate.move)
                crstate = crstate.parent
            sol.reverse()

            print("Solution path: ")
            for step in sol:
                print(step)
            print("nodes poped: ", node_pop)
            print("Nodes expanded: ", nodes_ex)
            print("Nodes generated: ", nodes_ge)
            print("Max fringe size: ", max_fri)
            print("solution found at", g_f.depth, "with the cost of", g_f.cost)
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n Goal node is {g_f} \n')
                    f.write(f'nodes poped: {node_pop} \n')
                    f.write(f'Nodes expanded: {nodes_ex} \n')
                    f.write(f'Nodes generated: {nodes_ge} \n')
                    f.write(f'Max fringe size: {max_fri} \n')
            return
            

        elif crstate.state not in closed :
            closed.append(crstate.state)
            nodes_ex += 1
            if dump == True:
                with open(filename, 'a') as f:
                        f.write(f'\n')
                        f.write(f'Generating Successor to < :{crstate} \n')
                        
            x, y = zero_tile(crstate.state)
            fringstr = ""
            count_succ = 0
            p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
            for i in p_pos:
                if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                    temp_m = tempm(crstate.state)
                    n = temp_m[i[0]][i[1]]
                    temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                    if i[0]>x and i[1]==y:
                        _move="up" + str(n)
                        nodes_ge += 1
                    elif i[0]<x and i[1]==y:
                        _move="Down" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]<y:
                        _move="Right" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]>y:
                        _move="left" + str(n)
                        nodes_ge += 1
                    count_succ +=1
                    child_node = Node(temp_m, _move, crstate.cost + n, crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                    fringe.put((child_node.cost, child_node))
                    fringstr+=("< " +str(child_node)+" >\n")
            
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'{count_succ} successors generated \n')
                    cc = ''
                    for i in closed :
                        cc += str(i) + " , "
                    f.write(f'Closed: {cc} \n')
                    f.write(f'fringe:')    
                    for v in fringe.queue :
                        f.write(f'{v[1]} \n')

def dfs():
    class Node:
        def __init__(self, state, move, cost, depth, hueristic, parent):
            self.state=state 
            self.move=move 
            self.cost=cost 
            self.depth=depth 
            self.hueristic=hueristic
            self.parent=parent 
            
        def __lt__(self, other):
            return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

        def __repr__(self):
            return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def __str__(self):
            return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)
    
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')

    def man_hueristic(start_matrix, goal_matrix):
        total = 0
        for i in range(3):
            for j in range(3):
                if start_matrix[i][j] != goal_matrix[i][j]:
                    weight = start_matrix[i][j]
                    x,y = any_tile(goal_matrix, weight)
                    total += (abs(i-x) + abs(j-y))*weight
        return(total)

    fringe = []
    closed = []
    nodes_ex = 0
    nodes_ge = 0
    node_pop = 0
    max_fri = 0

    s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
    fringe.append(s_state)

    while fringe:
        if max_fri < len(fringe):
            max_fri = len(fringe)
        
        crstate = fringe.pop(-1)
        node_pop += 1

        if crstate.state == goal:
            sol = []
            g_f = crstate
            while crstate.parent is not None:
                sol.append(crstate.move)
                crstate = crstate.parent
            sol.reverse()

            print("Solution path: ")
            for step in sol:
                print(step)
            print("nodes poped: ", node_pop)
            print("Nodes expanded: ", nodes_ex)
            print("Nodes generated: ", nodes_ge)
            print("Max fringe size: ", max_fri)
            print("solution found at", g_f.depth, "with the cost of", g_f.cost)
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n Goal node is {g_f} \n')
                    f.write(f'nodes poped: {node_pop} \n')
                    f.write(f'Nodes expanded: {nodes_ex} \n')
                    f.write(f'Nodes generated: {nodes_ge} \n')
                    f.write(f'Max fringe size: {max_fri} \n')
            return
            

        elif crstate.state not in closed :
            closed.append(crstate.state)
            nodes_ex += 1
            if dump == True:
                with open(filename, 'a') as f:
                        f.write(f'\n')
                        f.write(f'Generating Successor to < :{crstate} \n')
                        
            x, y = zero_tile(crstate.state)
            fringstr = ""
            count_succ = 0
            p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
            for i in p_pos:
                if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                    temp_m = tempm(crstate.state)
                    n = temp_m[i[0]][i[1]]
                    temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                    if i[0]>x and i[1]==y:
                        _move="up" + str(n)
                        nodes_ge += 1
                    elif i[0]<x and i[1]==y:
                        _move="Down" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]<y:
                        _move="Right" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]>y:
                        _move="left" + str(n)
                        nodes_ge += 1
                    count_succ +=1
                    child_node = Node(temp_m, _move, crstate.cost + n, crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                    fringe.append(child_node)
            
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'{count_succ} successors generated \n')
                    cc = ''
                    for i in closed :
                        cc += str(i) + " , "
                    f.write(f'Closed: {cc} \n')
                    f.write(f'fringe:')    
                    for v in fringe :
                        f.write(f'{v} \n')
            
            if len(fringe) == 0:
                while crstate.parent is not None:
                    crstate = crstate.parent
                    if crstate.state not in closed:
                        fringe.append(crstate)
                    break
            else:
                while fringe:
                    if crstate.parent is None:
                        break
                    if crstate.parent in fringe:           
                        fringe.remove(crstate)
                        fringe.append(crstate.parent)
                        # crstate = crstate.parent
                    crstate = crstate.parent

def dls():
    inp = input('depth limit : ')
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')
    
    for L in range(1, int(inp)+1):    
        if dump == True:
            with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'For max depth: {L} \n')

        class Node:
            def __init__(self, state, move, cost, depth, hueristic, parent):
                self.state=state 
                self.move=move 
                self.cost=cost 
                self.depth=depth 
                self.hueristic=hueristic
                self.parent=parent 
                
            def __lt__(self, other):
                return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

            def __repr__(self):
                return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

            def __str__(self):
                return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def man_hueristic(start_matrix, goal_matrix):
            total = 0
            for i in range(3):
                for j in range(3):
                    if start_matrix[i][j] != goal_matrix[i][j]:
                        weight = start_matrix[i][j]
                        x,y = any_tile(goal_matrix, weight)
                        total += (abs(i-x) + abs(j-y))*weight
            return(total)

        fringe = []
        closed = []
        nodes_ex = 0
        nodes_ge = 0
        node_pop = 0
        max_fri = 0

        s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
        fringe.append(s_state)

        while fringe:
            if max_fri < len(fringe):
                max_fri = len(fringe)
            
            crstate = fringe.pop(-1)
            node_pop += 1
            n_vis = fringe

            if crstate.state == goal:
                sol = []
                g_f = crstate
                while crstate.parent is not None:
                    sol.append(crstate.move)
                    crstate = crstate.parent
                sol.reverse()

                print("Solution path: ")
                for step in sol:
                    print(step)
                print("nodes poped: ", node_pop)
                print("Nodes expanded: ", nodes_ex)
                print("Nodes generated: ", nodes_ge)
                print("Max fringe size: ", max_fri)
                print("solution found at", g_f.depth, "with the cost of", g_f.cost)
                if dump == True:
                    with open(filename, 'a') as f:
                        f.write(f'\n Goal node is {g_f} \n')
                        f.write(f'nodes poped: {node_pop} \n')
                        f.write(f'Nodes expanded: {nodes_ex} \n')
                        f.write(f'Nodes generated: {nodes_ge} \n')
                        f.write(f'Max fringe size: {max_fri} \n')
                return
                
            elif crstate.depth <= int(L):
                if crstate.state not in closed :
                    closed.append(crstate.state)
                    nodes_ex += 1
                    if dump == True:
                        with open(filename, 'a') as f:
                                f.write(f'\n')
                                f.write(f'Generating Successor to < :{crstate} \n')
                                
                    x, y = zero_tile(crstate.state)
                    fringstr = ""
                    count_succ = 0
                    p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
                    for i in p_pos:
                        if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                            temp_m = tempm(crstate.state)
                            n = temp_m[i[0]][i[1]]
                            temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                            if i[0]>x and i[1]==y:
                                _move="up" + str(n)
                                nodes_ge += 1
                            elif i[0]<x and i[1]==y:
                                _move="Down" + str(n)
                                nodes_ge += 1
                            elif i[0]==x and i[1]<y:
                                _move="Right" + str(n)
                                nodes_ge += 1
                            elif i[0]==x and i[1]>y:
                                _move="left" + str(n)
                                nodes_ge += 1
                            count_succ +=1
                            child_node = Node(temp_m, _move, crstate.cost + n, crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                            fringe.append(child_node)
                            fringstr+=("< " +str(child_node)+" >\n")
                    
                    if dump == True:
                        with open(filename, 'a') as f:
                            f.write(f'\n')
                            f.write(f'{count_succ} successors generated \n')
                            cc = ''
                            for i in closed :
                                cc += str(i) + " , "
                            f.write(f'Closed: {cc} \n')
                            f.write(f'fringe:')    
                            for v in fringe :
                                f.write(f'{v} \n')
                else:
                    while fringe:
                        if crstate.parent is None:
                            break
                        if crstate.parent in n_vis:           
                            fringe.remove(crstate)
                            fringe.append(crstate.parent)
                            # crstate = crstate.parent
                        crstate = crstate.parent
            
def ids():
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')
    
    for L in range(1, 1000000):    
        if dump == True:
            with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'For max depth: {L} \n')

        class Node:
            def __init__(self, state, move, cost, depth, hueristic, parent):
                self.state=state 
                self.move=move 
                self.cost=cost 
                self.depth=depth 
                self.hueristic=hueristic
                self.parent=parent 
                
            def __lt__(self, other):
                return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

            def __repr__(self):
                return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

            def __str__(self):
                return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def man_hueristic(start_matrix, goal_matrix):
            total = 0
            for i in range(3):
                for j in range(3):
                    if start_matrix[i][j] != goal_matrix[i][j]:
                        weight = start_matrix[i][j]
                        x,y = any_tile(goal_matrix, weight)
                        total += (abs(i-x) + abs(j-y))*weight
            return(total)

        fringe = []
        closed = []
        nodes_ex = 0
        nodes_ge = 0
        node_pop = 0
        max_fri = 0

        s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
        fringe.append(s_state)

        while fringe:
            if max_fri < len(fringe):
                max_fri = len(fringe)
            
            crstate = fringe.pop(-1)
            node_pop += 1
            n_vis = fringe

            if crstate.state == goal:
                sol = []
                g_f = crstate
                while crstate.parent is not None:
                    sol.append(crstate.move)
                    crstate = crstate.parent
                sol.reverse()

                print("Solution path: ")
                for step in sol:
                    print(step)
                print("nodes poped: ", node_pop)
                print("Nodes expanded: ", nodes_ex)
                print("Nodes generated: ", nodes_ge)
                print("Max fringe size: ", max_fri)
                print("solution found at", g_f.depth, "with the cost of", g_f.cost)
                if dump == True:
                    with open(filename, 'a') as f:
                        f.write(f'\n Goal node is {g_f} \n')
                        f.write(f'nodes poped: {node_pop} \n')
                        f.write(f'Nodes expanded: {nodes_ex} \n')
                        f.write(f'Nodes generated: {nodes_ge} \n')
                        f.write(f'Max fringe size: {max_fri} \n')
                return
                
            elif crstate.depth <= int(L):
                if crstate.state not in closed :
                    closed.append(crstate.state)
                    nodes_ex += 1
                    if dump == True:
                        with open(filename, 'a') as f:
                                f.write(f'\n')
                                f.write(f'Generating Successor to < :{crstate} \n')
                                
                    x, y = zero_tile(crstate.state)
                    fringstr = ""
                    count_succ = 0
                    p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
                    for i in p_pos:
                        if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                            temp_m = tempm(crstate.state)
                            n = temp_m[i[0]][i[1]]
                            temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                            if i[0]>x and i[1]==y:
                                _move="Up" + str(n)
                                nodes_ge += 1
                            elif i[0]<x and i[1]==y:
                                _move="Down" + str(n)
                                nodes_ge += 1
                            elif i[0]==x and i[1]<y:
                                _move="Right" + str(n)
                                nodes_ge += 1
                            elif i[0]==x and i[1]>y:
                                _move="Left" + str(n)
                                nodes_ge += 1
                            count_succ +=1
                            child_node = Node(temp_m, _move, crstate.cost + n, crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                            fringe.append(child_node)
                            fringstr+=("< " +str(child_node)+" >\n")
                    
                    if dump == True:
                        with open(filename, 'a') as f:
                            f.write(f'\n')
                            f.write(f'{count_succ} successors generated \n')
                            cc = ''
                            for i in closed :
                                cc += str(i) + " , "
                            f.write(f'Closed: {cc} \n')
                            f.write(f'fringe:')    
                            for v in fringe :
                                f.write(f'{v} \n')
                else:
                    while fringe:
                        if crstate.parent is None:
                            break
                        if crstate.parent in n_vis:           
                            fringe.remove(crstate)
                            fringe.append(crstate.parent)
                            # crstate = crstate.parent
                        crstate = crstate.parent
        
def greedy():
    class Node:
        def __init__(self, state, move, cost, depth, hueristic, parent):
            self.state=state 
            self.move=move 
            self.cost=cost 
            self.depth=depth 
            self.hueristic=hueristic
            self.parent=parent 

        def __lt__(self, other):
            return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

        def __repr__(self):
            return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def __str__(self):
            return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)
    
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')

    def man_hueristic(start_matrix, goal_matrix):
        total = 0
        for i in range(3):
            for j in range(3):
                if start_matrix[i][j] != goal_matrix[i][j]:
                    weight = start_matrix[i][j]
                    x,y = any_tile(goal_matrix, weight)
                    total += (abs(i-x) + abs(j-y))*weight
        return(total)

    fringe = PriorityQueue(0)
    closed = []
    nodes_ex = 0
    nodes_ge = 0
    node_pop = 0
    max_fri = 0

    s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
    fringe.put((s_state.cost, s_state))

    while fringe:
        if max_fri < fringe.qsize():
            max_fri = fringe.qsize()
            
        crstate = fringe.get()[1]
        node_pop += 1

        if crstate.state == goal:
            sol = []
            g_f = crstate
            while crstate.parent is not None:
                sol.append(crstate.move)
                crstate = crstate.parent
            sol.reverse()

            print("Solution path: ")
            for step in sol:
                print(step)
            print("nodes poped: ", node_pop)
            print("Nodes expanded: ", nodes_ex)
            print("Nodes generated: ", nodes_ge)
            print("Max fringe size: ", max_fri)
            print("solution found at", g_f.depth, "with the cost of", g_f.cost)
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n Goal node is {g_f} \n')
                    f.write(f'nodes poped: {node_pop} \n')
                    f.write(f'Nodes expanded: {nodes_ex} \n')
                    f.write(f'Nodes generated: {nodes_ge} \n')
                    f.write(f'Max fringe size: {max_fri} \n')
            return

        elif crstate.state not in closed :
            closed.append(crstate.state)
            nodes_ex += 1
            if dump == True:
                with open(filename, 'a') as f:
                        f.write(f'\n')
                        f.write(f'Generating Successor to < :{crstate} \n')
                        
            x, y = zero_tile(crstate.state)
            fringstr = ""
            count_succ = 0
            p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
            for i in p_pos:
                if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                    temp_m = tempm(crstate.state)
                    n = temp_m[i[0]][i[1]]
                    temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                    if i[0]>x and i[1]==y:
                        _move="Up" + str(n)
                        nodes_ge += 1
                    elif i[0]<x and i[1]==y:
                        _move="Down" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]<y:
                        _move="Right" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]>y:
                        _move="Left" + str(n)
                        nodes_ge += 1
                    count_succ +=1
                    child_node = Node(temp_m, _move, man_hueristic(temp_m, goal), crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                    fringe.put((child_node.cost, child_node))
                    fringstr+=("< " +str(child_node)+" >\n")
            
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'{count_succ} successors generated \n')
                    cc = ''
                    for i in closed :
                        cc += str(i) + " , "
                    f.write(f'Closed: {cc} \n')
                    f.write(f'fringe:')    
                    for v in fringe.queue :
                        f.write(f'{v[1]} \n')

def astar():
    class Node:
        def __init__(self, state, move, cost, depth, hueristic, parent):
            self.state=state 
            self.move=move 
            self.cost=cost 
            self.depth=depth 
            self.hueristic=hueristic
            self.parent=parent 

        def __lt__(self, other):
            return (self.state, self.hueristic, self.depth, self.move, self.cost) < (other.state, other.hueristic, other.depth, other.move, other.cost)

        def __repr__(self):
            return "%s %s %s %s %s %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)

        def __str__(self):
            return "state = %s, action = %s, G(n) = %s, d = %s, F(n) = %s, parent = pointer to -> %s" % (self.state, self.move, self.cost, self.depth, self.hueristic, self.parent)
    
    if dump == True:
        filename = 'trace-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.txt'
        with open(filename, 'w') as f:
            f.write(f'Command-Line Arguments :{sys.argv} \n')
            f.write(f'Method :{sys.argv[3]}\n')
            f.write(f'Running :{sys.argv[3]}\n')   

    def man_hueristic(start_matrix, goal_matrix):
        total = 0
        for i in range(3):
            for j in range(3):
                if start_matrix[i][j] != goal_matrix[i][j]:
                    weight = start_matrix[i][j]
                    x,y = any_tile(goal_matrix, weight)
                    total += (abs(i-x) + abs(j-y))*weight
        return(total)

    fringe = PriorityQueue(0)
    closed = []
    nodes_ex = 0
    nodes_ge = 0
    node_pop = 0
    max_fri = fringe.qsize()

    s_state = Node(start, 0, 0, 0, man_hueristic(start, goal), None)
    fringe.put((s_state.hueristic, s_state))

    while fringe:
        if max_fri < fringe.qsize():
            max_fri = fringe.qsize()

        crstate = fringe.get()[1]
        node_pop += 1

        if crstate.state == goal:
            sol = []
            g_f = crstate
            while crstate.parent is not None:
                sol.append(crstate.move)
                crstate = crstate.parent
            sol.reverse()

            print("Solution path: ")
            for step in sol:
                print(step)
            print("nodes poped: ", node_pop)
            print("Nodes expanded: ", nodes_ex)
            print("Nodes generated: ", nodes_ge)
            print("Max fringe size: ", max_fri)
            print("solution found at", g_f.depth, "with the cost of", g_f.cost)
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n Goal node is {g_f} \n')
                    f.write(f'nodes poped: {node_pop} \n')
                    f.write(f'Nodes expanded: {nodes_ex} \n')
                    f.write(f'Nodes generated: {nodes_ge} \n')
                    f.write(f'Max fringe size: {max_fri} \n')
            return
            

        elif crstate.state not in closed:
            closed.append(crstate.state)
            nodes_ex += 1
            if dump == True:
                with open(filename, 'a') as f:
                        f.write(f'\n')
                        f.write(f'Generating Successor to < :{crstate} \n')
                        
            x, y = zero_tile(crstate.state)
            fringstr = ""
            count_succ = 0
            p_pos = [[x+1, y], [x-1, y] ,[x, y-1], [x, y+1]]
            for i in p_pos:
                if i[0] >= 0 and i[1] >= 0 and i[0] <= 2 and i[1] <= 2:
                    temp_m = tempm(crstate.state)
                    n = temp_m[i[0]][i[1]]
                    temp_m[i[0]][i[1]], temp_m[x][y] = temp_m[x][y], temp_m[i[0]][i[1]]
                    if i[0]>x and i[1]==y:
                        _move="Up" + str(n)
                        nodes_ge += 1
                    elif i[0]<x and i[1]==y:
                        _move="Down" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]<y:
                        _move="Right" + str(n)
                        nodes_ge += 1
                    elif i[0]==x and i[1]>y:
                        _move="Left" + str(n)
                        nodes_ge += 1
                    count_succ +=1
                    child_node = Node(temp_m, _move, crstate.cost + n, crstate.depth + 1, man_hueristic(temp_m, goal)+n+crstate.cost, crstate)
                    fringe.put((child_node.hueristic, child_node))
                    fringstr+=("< " +str(child_node)+" >\n")
            
            if dump == True:
                with open(filename, 'a') as f:
                    f.write(f'\n')
                    f.write(f'{count_succ} successors generated \n')
                    cc = ''
                    for i in closed :
                        cc += str(i) + " , "
                    f.write(f'Closed: {cc} \n')
                    f.write(f'fringe:')    
                    for v in fringe.queue :
                        f.write(f'{v[1]} \n')
                    f.write(f'nodes generated : {nodes_ge} ')

if len(sys.argv) == 3:
    astar()

if len(sys.argv) == 4:
    if sys.argv[3] == 'bfs':
        bfs()
    elif sys.argv[3] == 'dfs':
        dfs()
    elif sys.argv[3] == 'ucs':
        ucs()
    elif sys.argv[3] == 'dls':
        dls()
    elif sys.argv[3] == 'ids':
        ids()
    elif sys.argv[3] == 'greedy':
        greedy()
    elif sys.argv[3] == 'a*':
        astar()
    elif sys.argv[3] == 'true':
        dump = True
        astar()
    elif sys.argv[3] == 'false':
        astar()

else:
    0

if len(sys.argv) == 5:
    if sys.argv[3] == 'bfs' and sys.argv[4] == 'true':
        dump = True
        bfs()
    elif sys.argv[3] == 'bfs' and sys.argv[4] != 'true':
        bfs()
    elif sys.argv[3] == 'dfs' and sys.argv[4] == 'true':
        dump = True
        dfs()
    elif sys.argv[3] == 'dfs' and sys.argv[4] != 'true':
        dfs()
    elif sys.argv[3] == 'ucs' and sys.argv[4] == 'true':
        dump = True
        ucs()
    elif sys.argv[3] == 'ucs' and sys.argv[4] != 'true':
        ucs()
    elif sys.argv[3] == 'dls' and sys.argv[4] == 'true':
        dump = True
        dls()
    elif sys.argv[3] == 'dls' and sys.argv[4] != 'true':
        dls()
    elif sys.argv[3] == 'ids' and sys.argv[4] == 'true':
        dump = True
        ids()
    elif sys.argv[3] == 'ids' and sys.argv[4] != 'true':
        ids()
    elif sys.argv[3] == 'greedy' and sys.argv[4] == 'true':
        dump = True
        greedy()
    elif sys.argv[3] == 'greedy' and sys.argv[4] != 'true':
        greedy()
    elif sys.argv[3] == 'a*' and sys.argv[4] == 'true':
        dump = True
        astar()
    elif sys.argv[3] == 'a*' and sys.argv[4] != 'true':
        astar()