n = 64
l_n = 16
# Gamma = (-2**l_gamma, 2**l_gamma)
# Delta = (-2**l_delta, 2**l_delta)
# Lambda = (-2**l_lambda, 2**(l_lambda+l_sigma))
epsilion = 0.5
l_gamma = 32
l_lambda = 64
l_sigma = 8
l_delta = epsilion * (l_lambda + l_n) + 1
print(l_delta)
assert(l_lambda > l_sigma + l_delta + 4)