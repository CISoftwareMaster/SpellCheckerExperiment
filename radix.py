class SERadixNode:
    def __init__(self):
        self.children = dict()
        self.valid = False


class SERadixOptimisationOperation:
    def __init__(self, startNode=None, lastNode=None, oldKey="", newKey="", parent=None):
        self.startNode = startNode
        self.lastNode = lastNode
        self.oldKey = oldKey
        self.newKey = newKey
        self.parent = parent


class SERadixTree:
    def __init__(self, words=[]):
        self.children = dict()

        # add words (if provided)
        for word in words:
            self.addWord(word)

    def check(self, edge, parent):
        return parent[edge] if edge in parent else None

    def checkAdd(self, edge, parent):
        if edge not in parent:
            parent[edge] = SERadixNode()
        return parent[edge]

    def getEdge(self, word, parent):
        for edge in parent:
            if word.startswith(edge):
                return edge
        return None

    def removeEdgeFromWord(self, edge, word):
        if edge in word:
            word = word[len(edge):len(word)]
        return word

    def addWord(self, word):
        # make sure that we're working with the lowercase variant of our word
        word = word.lower()

        # check if there is something to actually add
        if len(word) > 0:
            # point to that node
            pointer = self.checkAdd(word[0], self.children)
            word = self.removeEdgeFromWord(word[0], word)

            # iteratively add / follow branches
            for char in word:
                pointer = self.checkAdd(char, pointer.children)

            # at the leaf node, mark it as a valid word
            pointer.valid = True

    def checkWord(self, word):
        word = word.lower()

        if len(word) > 0:
            edge = self.getEdge(word, self.children)

            # check if we got a valid edge
            if edge is None: return False

            # point to that node
            pointer = self.children[edge]
            word = self.removeEdgeFromWord(edge, word)

            # follow branches until we reach the word
            while pointer is not None:
                # check if that thing is a word
                if pointer == True:
                    # what the heck are we even doing here?
                    # it's already a word dumbo! (the app, not you [reading this])
                    return True

                # get next edge from word
                edge = self.getEdge(word, pointer.children)

                # check if edge exists
                if edge is None or len(word) == 0: break

                # remove edge from word
                word = self.removeEdgeFromWord(edge, word)
                # print(f"Edge: {edge}, Word: {word}")

                # follow branches until we reach the leaf node
                pointer = self.check(edge, pointer.children)

            # final check
            # print(f"Branches: {[x for x in pointer.children]}, validWord: {pointer.valid}")
            return (len(word) == 0 and pointer is not None and pointer.valid)

    def clear(self):
        self.children = dict()

    def analyseBranch(self, branch, path, previous=None):
        """
        This function can output a tuple of up to three possible values
        value 0: is this node single-branched?
        value 1: combined edges leading to the last node
        value 2: the last single-branched node (or I don't know, the last branch in a single-branched node)
        """
        nBranches = len(branch.children)

        # keep following single branches
        if nBranches == 1:
            # unless, of course, they're already a word
            if branch.valid:
                # because, why in the universe would you compress it?
                return (False, path, branch)

            # follow it
            tokl = list(branch.children.keys())[0] # The Only Key, Literally (tokl, for short) [ignore this]
            return self.analyseBranch(branch.children[tokl], path + tokl, branch)

        # this branches into at least two more nodes (branches, but we've already used that word)
        elif nBranches >= 2:
            # return the path and the last node
            return (False, path, branch)

        # we've reached the last branch! (so, what should we possibly do with it?)
        else:
            # co-llapse, co-llapse, co-llapse! (obviously...)
            return (True, path, branch)

    # this function gets a list of SERadixOptimisationOperation objects from our current tree
    def optimiseHelper(self, branch, edge, parent):
        operations = []

        # analyse the current branch
        branchAnalysis = self.analyseBranch(branch, edge)

        # is this a single-branched node?
        isSingleBranched = branchAnalysis[0]
        # get the new key
        key = branchAnalysis[1]
        # get the last node in this branch
        lastNode = branchAnalysis[2]

        # initialise a new optimisation operation object
        optimisation = SERadixOptimisationOperation(branch, lastNode, edge, key, parent)

        # great, more branches is exactly what our tree needs (not)
        if not isSingleBranched:
            # trim the single branches before this node
            operations.append(optimisation)

            # repeat the whole flipping helper functions on this node's branches as well
            for childEdge in branch.children:
                operations += self.optimiseHelper(branch.children[childEdge], childEdge, branch)
        else:
            # only perform single-branch optimisation if it's not the same edge (obviously)
            if edge != key:
                operations.append(optimisation)

        # finally, return all the operations we've obtained from this branch
        return operations

    def optimise(self, debug=False):
        operations = []

        # get operation objects by starting branch analysis at our base tree nodes
        for edge in self.children:
            operations += self.optimiseHelper(self.children[edge], edge, self)

        # execute operations
        for operation in operations:
            # if debug mode is on, show our collapse operations
            if debug:
                print(f"Collapsed {operation.oldKey} to {operation.newKey}.")

            # perform collapse operations
            operation.parent.children.pop(operation.oldKey)

            # update edge
            operation.parent.children[operation.newKey] = operation.lastNode

    def nodeCount(self, branch):
        count = 1

        # count nodes
        for edge in branch.children:
            count += self.nodeCount(branch.children[edge])

        # return total count
        return count

    def totalNodeCount(self):
        nodeCount = 0
        for edge in self.children:
            nodeCount += self.nodeCount(self.children[edge])
        return nodeCount
