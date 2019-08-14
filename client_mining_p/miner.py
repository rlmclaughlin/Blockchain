import hashlib
import requests
import time

import sys


# TODO: Implement functionality to search for a proof 
def proof_of_work(last_proof):

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof

def valid_proof(last_proof, proof):
  
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    while True:
        start = time.time()
        print("Currently seeking a proof solution")
        last_proof = requests.get(url=node + '/last_proof').json().get('proof')
        new_proof = proof_of_work(last_proof)
        elapsed = time.time() - start
        print(f'found a solution in {elapsed} sec, sending to server...')
        proof_data = {'proof': new_proof}
        proof_response = requests.post(url=node + '/mine', json=proof_data).json()

        if proof_response.get('message') == 'New Block Forged':
            print("A coin has successfully been mined!  Count: " + str(coins_mined))
            coins_mined += 1
        else:
            print(proof_response.get('message'))