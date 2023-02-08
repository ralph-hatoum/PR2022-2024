# implemeting approach for load prediction based on Quan et al. 's paper
import random as rd


L = 3

observations = [rd.randint(1,15) for _ in range(3*L)]

print(observations)


def compute_b(observations):
    num_1 = sum(observations,2*L+1)
    num_2 = sum(observations, L+1)-sum(observations,2*L+1)

    num = num_1-num_2
    
    denom_1 = sum(observations, L+1)-sum(observations, 2*L+1)
    denom_2 = sum(observations)-sum(observations, L+1)

    denom = denom_1-denom_2
    print((num/denom)**(1/L))

    return (num/denom)**(1/L)

def compute_a(observations,b):

    sum1 = sum(observations, L+1)-sum(observations, 2*L+1)
    sum2 = sum(observations)-sum(observations, L+1)
    print((sum1-sum2)*(b-1)/(b*(b**L-1)**2))
    return (sum1-sum2)*(b-1)/(b*(b**L-1)**2)

def compute_K(observations,b,a):
    sum_ = 0
    for i in range(L):
        sum_+=observations[i]
        
    print((1/L)*(sum_ - a*b*(1-b**L)/(1-b)))
    return (1/L)*(sum_ - a*b*(1-b**L)/(1-b))

def compute_prediction(observations,t):
    b = compute_b(observations)
    a = compute_a(observations, b)
    K = compute_K(observations,b,a)

    return K + a*b**t

print(compute_prediction(observations, 3))