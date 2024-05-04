# AnonCred
CSP Final Project - An Efficient System for Non-transferable Anonymous Credentials with Optional Anonymity Revocation


## Zero-Knowledge Proof
A zero-knowledge proof is a method by which one party (the prover) can prove to another party (the verifier) that a given statement is true, without conveying any information apart from the fact that the statement is indeed true.
In this implementation of the zero-knowledge proof, we use the Schnorr Sigma protocol to prove that one knows $x$, such that $h = g^x$ for a public generator $g$ and some eleemnt $h$. Sigma protocol is a three-step protocol in which communication between prover and verifier goes forwards once, then backwards, then forwards again. In other words, the prover sends the verifier a commitment, the verifier sends a challenge, and the prover sends a response. 

