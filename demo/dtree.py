import random
# Divider
class DivisionProblem:

    def __init__(self, varlist, dataset):
        # Initialize random assignment
        self.assignment = dict()
        self.partialset = dict()
        for v in varlist:
            self.assignment[v] = int(random.getrandbits(1))
            self.partialset[v] = []
        # Get dataset
        self.dataset = []
        for instance in dataset:
            triple, oddIndex, weight = instance
            if triple[0] in varlist and triple[1] in varlist and triple[2] in varlist:
                self.dataset.append(instance)
                self.partialset[triple[0]].append(instance)
                self.partialset[triple[1]].append(instance)
                self.partialset[triple[2]].append(instance)

    # Update rule
    def updateAssignment(self, triple, oddIndex, weight):
        raise Exception("Update rule need to be overridden.")

    # One iteration
    def iterate(self):
        for instance in self.dataset:
            triple, oddIndex, weight = instance
            self.updateAssignment(triple, oddIndex, weight)

    # Get current reward
    def getReward(self):
        result = 0
        for instance in self.dataset:
            triple, oddIndex, weight = instance
            assignmentTriple = [self.assignment[triple[(oddIndex + i) % 3]] for i in range(3)]
            if assignmentTriple == [0,1,1] or assignmentTriple == [1,0,0]:
                result += weight
            # elif assignmentTriple == [0,0,0] or assignmentTriple == [1,1,1]:
                # result += weight / 2
        return result

    def getPartialReward(self, name):
        result = 0
        for instance in self.partialset[name]:
            triple, oddIndex, weight = instance
            assignmentTriple = [self.assignment[triple[(oddIndex + i) % 3]] for i in range(3)]
            if assignmentTriple == [0,1,1] or assignmentTriple == [1,0,0]:
                result += weight
            # elif assignmentTriple == [0,0,0] or assignmentTriple == [1,1,1]:
                # result += weight / 2
        return result

    # Iterate until convergence or iterate n times
    def solve(self, numIter=None):
        if numIter is not None:
            for _ in range(numIter):
                self.iterate()
        else:
            numNoLearn = 0
            currentReward = 0
            while numNoLearn < 10: # <<<<<<<<< Threshold of no learning
                self.iterate()
                newReward = self.getReward()
                if newReward <= currentReward:
                    numNoLearn += 1
                currentReward = newReward


class SmallUpdateDivision(DivisionProblem):

    def updateAssignment(self, triple, oddIndex, weight):
        assignmentTriple = [self.assignment[triple[(oddIndex + i) % 3]] for i in range(3)]
        indexchange = 0
        # 0,0,0 | 1,1,1
        if assignmentTriple == [0,0,0] or assignmentTriple == [1,1,1]:
            indexchange = oddIndex
        # 1,1,0 | 0,0,1
        elif assignmentTriple == [1,1,0] or assignmentTriple == [0,0,1]:
            indexchange = (oddIndex + 1) % 3
        # 1,0,1 | 0,1,0
        elif assignmentTriple == [1,0,1] or assignmentTriple == [0,1,0]:
            indexchange = (oddIndex + 2) % 3
        else: # 1,0,0 | 0,1,1 :: Pass
            return
        learn = bool(random.getrandbits(1))
        if not learn:
            return
        oldPartialReward = self.getPartialReward(triple[indexchange])
        self.assignment[triple[indexchange]] = 1 - self.assignment[triple[indexchange]]
        if self.getPartialReward(triple[indexchange]) > oldPartialReward:
            return
        self.assignment[triple[indexchange]] = 1 - self.assignment[triple[indexchange]]

# Tree node
class TreeNode:
    def __init__(self):
        self.zero = None
        self.one = None
        self.data = None

# Dichotomous tree solver
class DichotomousTree:
    def __init__(self, varlist, dataset):
        self.Tree = TreeNode()
        self.dataset = dataset
        self.Tree.data = (varlist, dataset)
        self.reward = 0
    def divideNode(self, node):
        varlist, dataset = node.data
        success = False
        while not success:
            sud = SmallUpdateDivision(varlist, dataset)
            sud.solve()
            zeroset = []
            oneset = []
            for v in sud.assignment:
                if sud.assignment[v] == 0:
                    zeroset.append(v)
                else:
                    oneset.append(v)
            success = bool(len(zeroset) > 0 and len(oneset) > 0)
        self.reward += sud.getReward()
        node.zero = TreeNode()
        node.one = TreeNode()
        node.zero.data = (zeroset, sud.dataset)
        node.one.data = (oneset, sud.dataset)
        node.data = None

    def recursivesolve(self, node):
        varlist, dataset = node.data
        if len(varlist) > 2:
            self.divideNode(node)
            self.recursivesolve(node.zero)
            self.recursivesolve(node.one)
        elif len(varlist) == 2:
            node.zero = TreeNode()
            node.zero.data = varlist[0]

            node.one = TreeNode()
            node.one.data = varlist[1]

            node.data = None
        elif len(varlist) == 1:
            node.data = varlist[0]

        else:
            raise Exception("Error: should not reach here")

    def treeSolve(self):
        self.recursivesolve(self.Tree)

    def listform(self):
        def recurse(node):
            zerodata, onedata = None, None
            thisdata = node.data
            if node.zero is not None:
                zerodata = recurse(node.zero)
            if node.one is not None:
                onedata = recurse(node.one)
            return [i for i in [zerodata, thisdata, onedata] if i is not None]
        return recurse(self.Tree)
