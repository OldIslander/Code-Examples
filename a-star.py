import heapq
import sys, random
import copy

class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)



    
nodeid = 0
class node():
    def __init__(self, val, aState):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.thisState = aState
        self.val = val
        self.previousNode = None
    #Expands in four directions. Value calculated from given heuristic is input and added to current val plus 1.
    def expandUp(self, heuristic):
        self.upNode = node((self.val + heuristic + 1), self.thisState.up())
        self.upNode.previousNode = self
    def expandDown(self, heuristic):
        self.downNode = node((self.val + heuristic + 1), self.thisState.down())
        self.downNode.previousNode = self
    def expandLeft(self, heuristic):
        self.leftNode = node((self.val + heuristic + 1), self.thisState.left())
        self.leftNode.previousNode = self
    def expandRight(self, heuristic):
        self.rightNode = node((self.val + heuristic + 1), self.thisState.right())
        self.rightNode.previousNode = self
        
    def __str__(self):
        return 'Node: id=%d val=%d'%(self.id,self.val)
    


class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet


class state():
    def __init__(self, x, y, newTiles):
        self.xpos = x
        self.ypos = y
        self.tiles = newTiles
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s

    
    
    
def h0(head):
    frontier = PriorityQueue()
    closedList = Set()
    frontier.push(head)
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    currentNode = head
    v = 0 #For counting iterations
    n = 0 #Max number of nodes stored in memory(frontier + closedList)
    d = 0 #Depth of the solution
    b = 0 #Branching factor N ** (1/d)
    while not (frontier.isEmpty() or currentNode.thisState.tiles == goal):
        currentNode = frontier.pop()
        #print(closedList.isMember(currentNode.thisState))
        if not(closedList.isMember(currentNode.thisState)):
            if not (currentNode.thisState.xpos == 0):
                newState = currentNode.thisState.up()
                currentNode.expandUp(0)
                frontier.push(currentNode.upNode)
            if not (currentNode.thisState.xpos == 2):
                newState = currentNode.thisState.down()
                currentNode.expandDown(0)
                frontier.push(currentNode.downNode)
            if not (currentNode.thisState.ypos == 0):
                newState = currentNode.thisState.left()
                currentNode.expandLeft(0)
                frontier.push(currentNode.leftNode)
            if not (currentNode.thisState.ypos == 2):
                newState = currentNode.thisState.right()
                currentNode.expandRight(0)
                frontier.push(currentNode.rightNode)
            closedList.add(currentNode.thisState)
            v = v + 1
            if ((frontier.length() + closedList.length()) > n):
                n = (frontier.length() + closedList.length())
    temp = currentNode
    while not (temp.previousNode == None):
        d+=1
        temp = temp.previousNode
    
    print("V=", v)
    f= open("theVs1.txt" , "a")
    f.write(str(v)+ "\n")
    f.close()
    print("N=", n)
    f= open("theNs1.txt" , "a")
    f.write(str(n)+ "\n")
    f.close()
    print("d=", d)
    f= open("theDs1.txt" , "a")
    f.write(str(d)+ "\n")
    f.close()
    b = n ** (1/d)
    print("b=", (n ** (1/d)))
    f= open("theBs1.txt" , "a")
    f.write(str(b)+ "\n")
    f.close()
    print(currentNode.thisState)
    while not (currentNode.previousNode == None):
        print(currentNode.previousNode.thisState)
        d += 1
        currentNode = currentNode.previousNode
#I'm just gonna not write a calc function for h0 because that's always 0.
#The one where it returns the number of displaced tiles
#I'm calling it a "board" here to distinguish it from the state class
#Basically each run with a heuristic will be done with a function that calls a "calc" function that
#gets the actual value of the heuristic
def h1(head): #Hey Dr. Phillips, tell me if there's a better way to do this than to write four nearly identical functions
    frontier = PriorityQueue()
    closedList = Set()
    frontier.push(head)
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    currentNode = head
    v = 0 #Total number of nodes visited
    n = 0 #Max number of nodes stored in memory(frontier + closedList)
    d = 0 #Depth of the solution
    b = 0 #Branching factor N ** (1/d)
    while not (frontier.isEmpty() or currentNode.thisState.tiles == goal):
        currentNode = frontier.pop()
        #print(closedList.isMember(currentNode.thisState))
        if not(closedList.isMember(currentNode.thisState)):
            if not (currentNode.thisState.xpos == 0):
                newState = currentNode.thisState.up()
                currentNode.expandUp(h1Calc(newState.tiles) - h1Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.upNode)
            if not (currentNode.thisState.xpos == 2):
                newState = currentNode.thisState.down()
                currentNode.expandDown(h1Calc(newState.tiles) - h1Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.downNode)
            if not (currentNode.thisState.ypos == 0):
                newState = currentNode.thisState.left()
                currentNode.expandLeft(h1Calc(newState.tiles) - h1Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.leftNode)
            if not (currentNode.thisState.ypos == 2):
                newState = currentNode.thisState.right()
                currentNode.expandRight(h1Calc(newState.tiles) - h1Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.rightNode)
            closedList.add(currentNode.thisState)
            v = v + 1
            if ((frontier.length() + closedList.length()) > n):
                n = (frontier.length() + closedList.length())
    temp = currentNode
    while not (temp.previousNode == None):
        d+=1
        temp = temp.previousNode
    
    print("V=", v)
    f= open("theVs2.txt" , "a")
    f.write(str(v)+ "\n")
    f.close()
    print("N=", n)
    f= open("theNs2.txt" , "a")
    f.write(str(n)+ "\n")
    f.close()
    print("d=", d)
    f= open("theDs2.txt" , "a")
    f.write(str(d)+ "\n")
    f.close()
    b = n ** (1/d)
    print("b=", (n ** (1/d)))
    f= open("theBs2.txt" , "a")
    f.write(str(b)+ "\n")
    f.close()
    print(currentNode.thisState)
    while not (currentNode.previousNode == None):
        print(currentNode.previousNode.thisState)
        d += 1
        currentNode = currentNode.previousNode
    

def h1Calc(aBoard):
    num = 0 #Number of displaced tiles
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    for x in range(3):
        for y in range(3):
            if not (aBoard[x][y] == goal[x][y]):
                num += 1
    return num

def h2(head):
    frontier = PriorityQueue()
    closedList = Set()
    frontier.push(head)
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    currentNode = head
    v = 0 #For counting iterations
    n = 0 #Max number of nodes stored in memory(frontier + closedList)
    d = 0 #Depth of the solution
    b = 0 #Branching factor N ** (1/d)
    while not (frontier.isEmpty() or currentNode.thisState.tiles == goal):
        currentNode = frontier.pop()
        #print(closedList.isMember(currentNode.thisState))
        if not(closedList.isMember(currentNode.thisState)):
            if not (currentNode.thisState.xpos == 0):
                newState = currentNode.thisState.up()
                currentNode.expandUp(h2Calc(newState.tiles) - h2Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.upNode)
            if not (currentNode.thisState.xpos == 2):
                newState = currentNode.thisState.down()
                currentNode.expandDown(h2Calc(newState.tiles) - h2Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.downNode)
            if not (currentNode.thisState.ypos == 0):
                newState = currentNode.thisState.left()
                currentNode.expandLeft(h2Calc(newState.tiles) - h2Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.leftNode)
            if not (currentNode.thisState.ypos == 2):
                newState = currentNode.thisState.right()
                currentNode.expandRight(h2Calc(newState.tiles) - h2Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.rightNode)
            closedList.add(currentNode.thisState)
            v = v + 1
            if ((frontier.length() + closedList.length()) > n):
                n = (frontier.length() + closedList.length())
    temp = currentNode
    while not (temp.previousNode == None):
        d+=1
        temp = temp.previousNode
    
    print("V=", v)
    f= open("theVs3.txt" , "a")
    f.write(str(v)+ "\n")
    f.close()
    print("N=", n)
    f= open("theNs3.txt" , "a")
    f.write(str(n)+ "\n")
    f.close()
    print("d=", d)
    f= open("theDs3.txt" , "a")
    f.write(str(d)+ "\n")
    f.close()
    b = n ** (1/d)
    print("b=", (n ** (1/d)))
    f= open("theBs3.txt" , "a")
    f.write(str(b)+ "\n")
    f.close()
    print(currentNode.thisState)
    while not (currentNode.previousNode == None):
        print(currentNode.previousNode.thisState)
        currentNode = currentNode.previousNode

def h2Calc(aBoard): #The manhatten distance
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]] 
    total = 0
    for x in range(3):
        for y in range(3):
            if not (aBoard[x][y] == goal[x][y]):
                for k in range(3):
                    for j in range(3):
                        if(aBoard[j][k] == goal[x][y]):
                            total += (abs(x - k) + abs(y - j))
    return total

def h3(head):
    frontier = PriorityQueue()
    closedList = Set()
    frontier.push(head)
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    currentNode = head
    v = 0 #For counting iterations
    n = 0 #Max number of nodes stored in memory(frontier + closedList)
    d = 0 #Depth of the solution
    b = 0 #Branching factor N ** (1/d)
    while not (frontier.isEmpty() or currentNode.thisState.tiles == goal):
        currentNode = frontier.pop()
        #print(closedList.isMember(currentNode.thisState))
        if not(closedList.isMember(currentNode.thisState)):
            if not (currentNode.thisState.xpos == 0):
                newState = currentNode.thisState.up()
                currentNode.expandUp(h3Calc(newState.tiles) - h3Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.upNode)
            if not (currentNode.thisState.xpos == 2):
                newState = currentNode.thisState.down()
                currentNode.expandDown(h3Calc(newState.tiles) - h3Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.downNode)
            if not (currentNode.thisState.ypos == 0):
                newState = currentNode.thisState.left()
                currentNode.expandLeft(h3Calc(newState.tiles) - h3Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.leftNode)
            if not (currentNode.thisState.ypos == 2):
                newState = currentNode.thisState.right()
                currentNode.expandRight(h3Calc(newState.tiles) - h3Calc(currentNode.thisState.tiles))
                frontier.push(currentNode.rightNode)
            closedList.add(currentNode.thisState)
            v = v + 1
            if ((frontier.length() + closedList.length()) > n):
                n = (frontier.length() + closedList.length())
    temp = currentNode
    while not (temp.previousNode == None):
        d+=1
        temp = temp.previousNode
    print("V=", v)
    print("N=", n)
    print("d=", d)
    b =(n ** (1/d))
    print("b=", (n ** (1/d)))
    print(currentNode.thisState)
    while not (currentNode.previousNode == None):
        print(currentNode.previousNode.thisState)
        d += 1
        currentNode = currentNode.previousNode
    

def h3Calc(aBoard): #Manhatten distance plus number of displaced tiles surrounding given tile
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]] 
    total = 0
    for m in range(3):
        for n in range(3):
            if (aBoard[m][n] == 0):
                xpos = m
                ypos = n
    for x in range(3):
        for y in range(3):
            if not (aBoard[x][y] == goal[x][y]):
                for k in range(3):
                    for j in range(3):
                        if(aBoard[j][k] == goal[x][y]):
                            total += (abs(x - k) + abs(y - j))
                            if not (j == 0):
                                if not (aBoard[j-1][k] == goal[j-1][k] ):
                                    total += 1
                            if not (j == 2): 
                                   if not(aBoard[j+1][k] == goal[j+1][k]):
                                        total += 1
                            if not (k == 0): 
                                if not (aBoard[j][k-1] == goal[j][k-1]):
                                    total += 1
                            if not (k == 2): 
                                if not (aBoard[j][k+1] == goal[j][k+1]):
                                    total += 1
    return total
    
    
    
    

    
    
def main():
    board = [[],[],[]]
    j = 0 #Used for iterating through lines of list
    fromGen = sys.stdin #Random Board Generator should be piped in at this point.
    temp = []
    for num in fromGen:
         temp.append(list(map(int, num.split()))) #Basically just turns the input into one big list
    
    #This whole thing's a result of me incrementally re-learning python
    #It works for putting the numbers into a 2d list, albeit...inefficiently.
    #This shouldn't slow down the program significantly, so fuck it
    for x in range(3):
        for y in range(3): #I'll probably look back on this and wince
            board[x].append(temp[0][j])
            if (board[x][y] == 0):
                xpos = x;
                ypos = y
            j = j + 1
    
        
    #I made the state class a member of the node class for health's sake
    iniState = state(xpos, ypos, board)
    head = node(0, iniState)
    h0(head)
    
    head = node(0, iniState)
    h1(head)
    
    head = node(0, iniState) #I'm doing this because I'm scared
    h2(head)
    
    head = node(0, iniState)
    h3(head)
    
    
    
main()