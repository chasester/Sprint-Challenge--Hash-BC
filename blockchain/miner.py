import hashlib
import requests
import threading
import sys

from uuid import uuid4

from timeit import default_timer as timer
import json
import random
import time;
next_proof = [-1]
def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """
    
    #548399011 ,4580460
    start = timer()
    #last_proof = 548399011;
    print("Searching for next proof", last_proof)
    proof = 0
    threadsize = 10000;
    #  TODO: Your code here
    
    last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest();
    threads = []
    ind = 0;
    numofthreads = 20;
    next_proof = [-1];
    for i in range(numofthreads):
        threads.append(threading.Thread(target=middle_man, args=(last_hash,i*threadsize, (i+1)*threadsize,next_proof)))
    ind = numofthreads
    for i in threads:
        i.start();
    #time.sleep(0.02); #let everything catch up
    while next_proof[0] == -1:
        for i in threads:
            if(i.is_alive() == False and next_proof[0] == -1):
                #print("Ran indexes",ind*threadsize,"-",(ind+1)*threadsize);
                i.join();
                i._delete();
                i = threading.Thread(target=middle_man, args=(last_hash,ind*threadsize, (ind+1)*threadsize,next_proof));
                i.start();
                ind +=1;
            elif(next_proof[0] != -1):
                print("Proof found: " + str(next_proof[0]) + " in " + str(timer() - start))
                break;        
        if(next_proof[0] != -1):
            break;
        else:
            pass;
            #time.sleep(0.0001); #we dont need to check every ms 
    """ while valid_proof(last_hash, proof) == False:
        proof+= 1; """
    for i in threads:
        i.join();#have to join here cuz of reasons
        i._delete();
    threads = [];
    proof = next_proof;
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof

def middle_man(last_hash,start, end, next_proof):
    for i in range(start, end):
        if(valid_proof(last_hash, i) == True):
            
            print("hash fond", i);
            next_proof[0] = i; #this reaches back to an atomic value that we set here;
            break;
        elif(next_proof[0] != -1):
            break;

def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    # TODO: Your code here!
    guess = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return True or False
    return guess_hash[:6] == last_hash[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    id = "ChaseWenner"
    print("ID is", id)

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
