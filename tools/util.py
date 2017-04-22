def tot(n):
    t = 0.0
    for k in range(1,n+1):
        t += 1.0 if gcd(n, k) == 1 else 0.0
    return t

def gcd(a, b):  
    return a if b == 0 else gcd(b, a % b)