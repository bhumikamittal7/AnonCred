## ZKP based on Schnorr Sigma protocol to prove that one knows x, such that h = g^x

# Sigma protocol is a three-step protocol in which communication between prover and verifier goes forwards once, then backwards, then forwards again. 
# The prover sends the verifier a commitment, the verifier sends a challenge, and the prover sends a response.


from petlib.bn import Bn
from hashlib import sha256
import random

#takes a list of elements and returns a challenge
def challenge(elements):
    elem = [len(elements)] + elements
    elem_str = map(str, elem)
    #combine length and content of each element
    elem_len = map(lambda x: "%s||%s" % (len(x) , x), elem_str)
    state = "|".join(elem_len)
    H = sha256()
    H.update(state.encode("utf8"))
    return H.digest()

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_group_notprime(p):
    G = []
    for i in range(1, p):
        if gcd(i, p) == 1:
            G.append(i)
    return G

def generate_group(p):
    return [i for i in range(1, p)]

# G = generate_group(7)
# print(G)

def order(G, g):
    for k in range(1, len(G)):
        if pow(g, k, len(G)+1) == 1:
            return k
    return len(G)

# print(order(G, 2))

def generator(G):
    gen = []
    for g in G:
        if order(G, g) == len(G):
            gen.append(g)
    return random.choice(gen)
# print(generator(G)) 

#generates the group G, the generator g, and the order o
def setup():
    p = 101
    G = generate_group(p)
    g = generator(G)
    o = order(G, g)
    return G, g, o

#test the setup function
def test_setup():
    G, g, o = setup()
    print(G)
    print(g)
    print(o)
    assert len(G) == 16
    assert g in G
    assert o == 16

# test_setup()

#proves that one knows x, such that h = g^x 
#params: the group G, the generator g, and the order o
#h: the public key
#g: the generator
#x: the secret key
#m: message
def prove(params, h, x, m=""):
    G, g, o = params   
    assert pow(g, x, len(G)+1) == h
    w = random.randint(1, o)

    #computes W = g^w mod len(G)+1
    W = pow(g, w, len(G)+1)
    #state: the list of elements
    state = ['blah', G, g, h, m, W]

    hash_c = challenge(state)
    c = Bn.from_binary(hash_c) % Bn(o)
    r = (Bn(w) - c * Bn(x)) % Bn(o)

    return (c, r)

#verifies that one knows x
def verify(params, h, proof, m=""):
    G, g, o = params
    c, r = proof
    W = (pow(Bn(g), r, Bn(len(G)+1)) * pow(Bn(h), c, Bn(len(G)+1))) % Bn(len(G)+1)

    state = ['blah', G, g, h, m, W]
    hash_c = challenge(state)
    c2 = Bn.from_binary(hash_c) % Bn(o)
    return c == c2

def test_protocol():
    params = setup()
    G, g, o = params
    x = random.randint(1, o)
    h = pow(g, x, len(G)+1)
    hdash = random.choice(G)

    proof = prove(params, h, x)
    assert verify(params, h, proof)
    assert not verify(params, hdash, proof)

    #to sign a message
    message = "Hello World"
    falsemessage = "Hello World!"
    proof = prove(params, h, x, message)
    assert verify(params, h, proof, message)
    assert not verify(params, h, proof, falsemessage)

test_protocol()
print("All tests pass!")