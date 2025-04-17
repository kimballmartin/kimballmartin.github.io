# return the inverse of a mod n
# or -1 if a is not invertible mod n
def inv(a,n, verb = False):
    a = a % n        # guarantee a < n
    x = [1, 0, n]
    y = [0, 1, a]
    z = [0, 0, 0]
    while y[2] != 0:
        if verb:    print x, y
        q = x[2]/y[2]
        for i in range(3):
            z[i] = x[i] - q*y[i]
            x[i] = y[i]
            y[i] = z[i]
    if verb:   print x, y
    if x[2] == 1:
        return x[1] % n
    else:
        print a, "has no inverse mod", n
        return -1
