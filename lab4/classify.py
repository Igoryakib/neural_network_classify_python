import numpy as np
from io import StringIO

INPUT_DIM = 4
H_DIM = 10
OUT_DIM = 3

W1 = np.loadtxt("W1.txt", delimiter=",")
b1 = np.loadtxt("b1.txt", delimiter=",").reshape(1, -1)
W2 = np.loadtxt("W2.txt", delimiter=",")
b2 = np.loadtxt("b2.txt", delimiter=",").reshape(1, -1)
    
def relu(t): return np.maximum(t, 0)
    
def softmax(t):
    out = np.exp(t - np.max(t))  # стабілізація
    return out / np.sum(out)

def predict(x):
    t1 = x @ W1 + b1
    h1 = relu(t1)
    t2 = h1 @ W2 + b2
    z = softmax(t2)
    return z