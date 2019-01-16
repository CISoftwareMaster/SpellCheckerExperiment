from radix import SERadixTree

# create a radix tree
tree = SERadixTree("deck detour did dog dogs deer door doorknob doe does".split(" "))

# get size of object in bytes
trieNodeCount = tree.totalNodeCount()
print(f"Trie Node count: {trieNodeCount}")

# optimise our tree (turning our Trie into a Radix tree)
tree.optimise(True)

radixNodeCount = tree.totalNodeCount()
print(f"Radix Trie Node count: {radixNodeCount}\n")

# calculate difference
print(f"Delta: {trieNodeCount - radixNodeCount}, reduction: {100 - ((radixNodeCount/trieNodeCount) * 100):.2f} %\n")

# check words
for word in ["Deck", "Didd", "Doe", "Dogs", "Dogggs", "Doorknob"]:
    print(f"Does {word} exist in tree? ==> {tree.checkWord(word)}")
