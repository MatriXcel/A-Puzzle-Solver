import math
import copy

class Node:
    data = []
    parent = None
    relationToParent = "None"
    goalNode = None

    def __init__(self, data, parent, goalNode):
        self.data = data
        self.parent = parent
        self.goalNode = goalNode


    def getFCost(self):   
        if self.goalNode == None:
            return self.getGCost()

        return manhattanDistanceNode(self, self.goalNode) + self.getGCost()

    def getGCost(self):
        numLevels = 0
        currNode = self

        if currNode.parent != None:
            currNode = currNode.parent
            numLevels += 1
        
        return numLevels

    def equals(self, node2):
        for i in range(3):
            for j in range(4):
                if(self.data[i][j] != node2.data[i][j]):
                    return False

        return True    

    def relationTo(self, referenceNode):
        row1, col1 = find(self.data, 0)
        row2, col2 = find(referenceNode.data, 0)

        if(col1 - col2 == 1 and row1 == row2):
            return "R"
        elif(col1 - col2 == -1 and row1 == row2):
            return "L"
        elif(row1 - row2 == 1 and col1 == col2):
            return "D"
        elif(row1 - row2 == -1 and col1 == col2):
            return "U"
        
        return "No relation"



    def getShiftedNeighbor(self, row, col, sOffsetRow, sOffsetCol):
        dataShifted = copy.deepcopy(self.data)
        dataShifted[row][col] = dataShifted[row + sOffsetRow][col + sOffsetCol] 
        dataShifted[row + sOffsetRow][col + sOffsetCol] = 0

        neighbor = Node(data=dataShifted, parent=self, goalNode=self.goalNode)

        return neighbor

    def getNeighbors(self):
        neighbors = []

        row, col = find(self.data, 0)

        if(col < 3):
            dataRightShifted = self.getShiftedNeighbor(row, col, 0, 1)
            neighbors.append(dataRightShifted)
        
        if(col > 0):
            dataLeftShifted = self.getShiftedNeighbor(row, col, 0, -1)
            neighbors.append(dataLeftShifted)
        
        if(row < 2):
            dataDownShifted = self.getShiftedNeighbor(row, col, 1, 0)
            neighbors.append(dataDownShifted)
        
        if(row > 0):
            dataUpShifted = self.getShiftedNeighbor(row, col, -1, 0)
            neighbors.append(dataUpShifted)
        
        return neighbors
            



def find(l, elem):
    for row, i in enumerate(l):
        try:
            column = i.index(elem)
        except ValueError:
            continue
        return row, column
    return -1


def manhattanDistanceNode(node1, node2):
    totalManhattan = 0

    for i in range(3):
        for j in range(4):
            element = node1.data[i][j]
            node2Position = list(find(node2.data, element))

            totalManhattan += manhattanDistancePoint([i,j], node2Position)

    return totalManhattan


def manhattanDistancePoint(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1] - point2[1])




def outputToFile(filename, initialNode, goalNode, D, N, moves, fcosts):
    file = open(filename, "w")

    for row in initialNode.data:
        lineStr = ' '.join(map(str, row))
        file.write(lineStr + "\n")
    
    file.write("\n")

    for row in goalNode.data:
        lineStr = ' '.join(map(str, row))
        file.write(lineStr + "\n")

    file.write("\n")

    file.write(str(D) + "\n")
    file.write(str(N) + "\n") 
    file.write(" ".join(moves) + "\n")
    file.write(' '.join(map(str, fcosts)) + "\n")

    file.close()



def solvePuzzle(inputFileName, outputFileName):
    file = open(inputFileName, "r")

    goalNode = Node(data=[], parent=None, goalNode=None)
    initialNode = Node(data=[], parent=None, goalNode=goalNode)

    lines = file.read().split('\n')
    file.close()

    for line in lines[0:3]:
        nodeRow = []
        for num in line.split():
            nodeRow.append(int(num))
        initialNode.data.append(nodeRow)


    for line in lines[4:7]:
        nodeRow = []
        for num in line.split():
            nodeRow.append(int(num))
        goalNode.data.append(nodeRow)


    openList = []
    closedList = []

    openList.append(initialNode)
    
    currentNode = None

    while(True):
        lowestCost = 1000000
        

        for node in openList:
            if (node.getFCost() < lowestCost):
                lowestCost = node.getFCost()
                currentNode = node


        openList.remove(currentNode)
        closedList.append(currentNode)

        if currentNode.equals(goalNode):
            break

        for neighbor in currentNode.getNeighbors():

            isInClosed = False

            for node in closedList:
                if node.equals(neighbor):
                    isInClosed = True
            
            if isInClosed: 
                continue
                
            isInOpen = False
            for node in openList:
                if node.equals(neighbor):
                    isInOpen = True
                    neighbor = node
            
            oldParent = neighbor.parent
            neighbor.parent = currentNode
            newPathLength = neighbor.getGCost()
            neighbor.parent = oldParent

            if newPathLength  < neighbor.getGCost() or not isInOpen:
                neighbor.parent = currentNode

                if not isInOpen:
                    openList.append(neighbor)

    moves = []
    fcosts = []

    while currentNode != None:
        if(currentNode.parent != None):
            moves.append(currentNode.relationTo(currentNode.parent))
        
        fcosts.append(currentNode.getFCost())
        currentNode = currentNode.parent


    moves.reverse()
    fcosts.reverse()


    N = len(openList) + len(closedList)
    D = len(moves)

    outputToFile(outputFileName, initialNode, goalNode, D, N, moves, fcosts)

def main():
    solvePuzzle("Sample_Input.txt", "Sample_Input_Output.txt")
    solvePuzzle("Input2.txt", "Input2Output.txt")
    solvePuzzle("Input3.txt", "Input3Output.txt")

main()
