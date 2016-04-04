import copy
from sys import maxsize
import sys


class AlphaBetaPruning:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        
    def canBePruned(self, node):
        alpha, beta = self.alpha, self.beta
        if isinstance(node, MinNode): #test if node is an instance of MinNode
            self.beta = min(self.beta, node.val)
        else:
            self.alpha = max(self.alpha, node.val)
        if self.alpha >= self.beta:  
            self.alpha, self.beta = alpha, beta
            return True
        return False

    @staticmethod
    def getInstance(pruning):
        if pruning == None:
            return None
        return AlphaBetaPruning(pruning.alpha, pruning.beta)
    
class Node(object):
    def __init__(self, state, player, objectplayer, depth, cutoff, pruning, gameOver = False):
        self.state = copy.deepcopy(state)
        self.player = player
        self.objectplayer = objectplayer
        self.gameOver = gameOver
        self.depth = depth
        self.val = -maxsize - 1
        self.best = None
        self.name = "root"
        self.cutoff = cutoff
        self.pruning = AlphaBetaPruning.getInstance(pruning)

    def __getstr(self, val):
        return {-maxsize - 1 : '-Infinity', maxsize : 'Infinity'}.get(val, str(val))

    def printInfo(self):
        if printlog:
            if task == 3:
                # print str(self.name)+','+str(self.depth)+','+str(self.__getstr(self.val)),
                # print "%s,%d,%s"%(self.name, self.depth, self.__getstr(self.val)),
                file4.write("%s,%d,%s"%(self.name, self.depth, self.__getstr(self.val)))
                if self.pruning != None:
                    # print ','+str(self.__getstr(self.pruning.alpha))+','+str(self.__getstr(self.pruning.beta))
                    # print ",%s,%s"%(self.__getstr(self.pruning.alpha), self.__getstr(self.pruning.beta))
                    file4.write(",%s,%s"%(self.__getstr(self.pruning.alpha), self.__getstr(self.pruning.beta))+'\n')
            else:
                if task == 2:
                    # print "%s,%d,%s"%(self.name, self.depth, self.__getstr(self.val))
                    file3.write("%s,%d,%s"%(self.name, self.depth, self.__getstr(self.val))+'\n')


    def __belongsPlayer(self, i, j, player):
        return i in range(len(self.state)) and j in range(len(self.state)) and self.state[i][j] == ('X','O')[player]

    def __hasNext(self):
        self.gameOver, val = self.__eval()
        return not(self.gameOver) and not(self.isLeaf())

    def __tryBePruned(self):
        return self.pruning != None and self.pruning.canBePruned(self)
    
    def updateBest(self):
        self.printInfo()
        if not(self.__hasNext()):
            return self
        for i in range(5):
            for j in range(5):
                if self.state[i][j] == '*':
                    nextNode = self.__next(i, j).updateBest()
                    self.__tryUpdate(nextNode)
                    canBePruned =  self.__tryBePruned()
                    self.printInfo()
                    if canBePruned:
                        return self
        return self
    
    def canUpdate(self, node):
        return self.val < node.val

    def __tryUpdate(self, node):
        if self.best == None or self.canUpdate(node):
            self.best = node.state
            self.val = node.val

    def nextNodeCopy(self):
        return MinNode(self.state,self.player, self.objectplayer, self.depth + 1, self.cutoff, self.pruning, self.gameOver)
    
    def __next(self, i, j):
        nextNode = self.nextNodeCopy()
        nextNode.name = ('A','B','C','D','E')[j] + str(i + 1)
        nextNode.__nextState(i, j)
        nextNode.gameOver, val = nextNode.__eval()
        nextNode.changeTurn()
        
        if not(nextNode.__hasNext()):
            nextNode.val = val
        return nextNode
        
    def __nextState(self, i, j):
        for n in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if self.__belongsPlayer(n[0], n[1], self.player):
                return self.__raid(i, j)
        self.__sneak(i, j)
        
    def rival(self):
        return 1 - self.player
    
    def changeTurn(self):
        self.player =  self.rival()
                
    def __sneak(self, i, j):
        self.state[i][j] = ('X','O')[self.player]
        
    def __raid(self, i, j):
        self.state[i][j] = ('X','O')[self.player]
        for n in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if self.__belongsPlayer(n[0], n[1], self.rival()):
                    self.state[n[0]][n[1]] = ('X','O')[self.player]
    
    def __eval(self):
        vals = [0, 0, 0]
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                vals[{'X' : 0, 'O': 1, '*' : 2}[self.state[i][j]]] += board[i][j]
        return (vals[2] == 0), vals[self.objectplayer] - vals[1 - self.objectplayer]

    def isLeaf(self):
        return self.depth == self.cutoff

class MinNode(Node):
    def __init__(self, state, player, objectplayer, depth, cutoff, pruning, gameOver):
        Node.__init__(self, state, player, objectplayer, depth, cutoff, pruning, gameOver)
        self.val = maxsize
        
    def canUpdate(self, node):
        return self.val > node.val

    def nextNodeCopy(self):
        return Node(self.state,self.player, self.objectplayer, self.depth + 1, self.cutoff, self.pruning, self.gameOver)
   
def greedy(node):
    return node.updateBest()

file = open(sys.argv[-1], 'r')
file1 = open('next_state.txt','wb')
file2 = open('next_state.txt','wb')

try:
     task, printlog = int(file.readline()), True
     file4 = open('traverse_log.txt', 'wb')
     if task == 3:
         file4.write('Node,Depth,Value,Alpha,Beta\n')
     file3 = open('traverse_log.txt', 'wb')
     if task == 2:
         file3.write('Node,Depth,Value\n')
     if task != 4:
         Player, Cutoff = {'X' : 0, 'O' : 1}[file.readline()[0]], int(file.readline())
     else:
         Player1, task1, Cutoff1 = {'X' : 0, 'O' : 1}[file.readline()[0]], int(file.readline()), int(file.readline())
         Player2, task2, Cutoff2 = {'X' : 0, 'O' : 1}[file.readline()[0]], int(file.readline()), int(file.readline())
         Players, tasks, Cutoffs = (Player1, Player2), (task1, task2), (Cutoff1, Cutoff2)
     # print 'Node,Depth,Value'+'\r'
     board, state = [[int(x) for x in file.readline().split()] for i in range(5)], [list(line.split()[0]) for line in file.readlines()]
     if task != 4:
         # if task == 3:
         #     print 'Node,Depth,Value,Alpha,Beta'+'\r'
         # else:
         #     print 'Node,Depth,Value'+'\r'
         # Pruning = (None, None, AlphaBetaPruning(-maxsize -1, maxsize))[task-1]
         # for r in Node(state, Player, Player, 0, Cutoff, Pruning).updateBest().best:
         #     print ''.join(r)
        if task == 1:
            # file1.write('Node,Depth,Value\n')
            Pruning = (None, None, AlphaBetaPruning(-maxsize -1, maxsize))[task-1]
            for r in Node(state, Player, Player, 0, Cutoff, Pruning).updateBest().best:
                file1.write(''.join(r)+'\n')
        else:
            # file2.write('Node,Depth,Value,Alpha,Beta')
            Pruning = (None, None, AlphaBetaPruning(-maxsize -1, maxsize))[task-1]
            for r in Node(state, Player, Player, 0, Cutoff, Pruning).updateBest().best:
                file2.write(''.join(r)+'\n')
     else:
         file5 = open('trace_state.txt', 'wb')
         Prunings = ((None, None, AlphaBetaPruning(-maxsize -1, maxsize))[tasks[0] - 1], (None, None, AlphaBetaPruning(-maxsize -1, maxsize))[tasks[1] - 1])
         cur, printlog = 0, False
         while True:
             node = Node(state, Players[cur], Players[cur], 0, Cutoffs[cur], Prunings[cur]).updateBest()
             state, cur = node.best, 1 - cur
             if node.gameOver:
                 break
             for r in state:
                 file5.write(''.join(r)+'\n')
         file5.close()
finally:
     file.close()
     file1.close()
     file2.close()
     file3.close()
     file4.close()

     
