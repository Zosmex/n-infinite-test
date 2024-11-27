
def word_mesh(words: list[str]) -> str:
    # Write your code here.
    result = ""

    for i in range(len(words)-1):
        word_1 = words[i]
        word_2 = words[i+1]
        overlap = ""

        for j in range(1, min(len(word_1), len(word_2)) + 1):
            if word_1[-j:] == word_2[:j]:
                overlap = word_1[-j:]
        
        if overlap:
            result += overlap
        else:
            return "failed to mesh"

    return result

# Run this file for test
assert word_mesh(["beacon", "condominium", "umbilical", "california"]) == "conumcal"
assert word_mesh(["allow", "lowering", "ringmaster", "terror"]) == "lowringter"
assert word_mesh(["abandon", "donation", "onion", "ongoing"]) == "dononon"
assert word_mesh(["jamestown", "ownership", "hippocampus", "pushcart", "cartographer", "pheromone"]) == "ownhippuscartpher"
assert word_mesh(["kingdom", "dominator", "notorious", "usual", "allegory"] ) == "failed to mesh"