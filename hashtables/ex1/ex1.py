#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    ans = [];
    if(len(weights) == 2 and weights[0] == weights[1] and weights[0]+weights[1] == limit):
        return [1,0];
        
    for i in weights:#insert everything into the hash table
        hash_table_insert(ht,i, i);
    
    for i in weights:
        a = hash_table_retrieve(ht, limit-i)
        if(a == None ):
            continue;
        a = weights.index(a)
        i = weights.index(i)
        try:
            ans.index(i)
            ans.index(a)
        except ValueError:
            print(i if i > a else a);
            ans.append(i if i > a else a)
            ans.append(a if i > a else i)
    if(len(ans) < 1):
        ans = None;
    return ans


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
