n = 5

# Initial Belief [x1, x2, x3, x4, x5]
# Probabilty vectors list, p, with uniform probabilty for all the n spots
p = [(1.0/n)] * n # uniform prior distribution
# p = [0, 1, 0, 0, 0]

world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
motions = [1, 1] # 1 - right, 0 - left

# Localization: sense -> move -> sense ...

pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

# Probability after sense (turns the proir into prosterior)
# returns the normalized probabilty vector
def sense(p, Z):
    global world, pHit, pMiss
    q = []
    for i in range(len(p)):
        hit = (world[i] == Z)
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    # Normalize the results
    s= sum(q)
    for i in range(len(p)):
        q[i] = q[i]/s
    return q

# Returns the shifted distrubtion by U units to the right.
# If U=0, q will be the same as p
# Note: a cyclic world
def exact_move(p, U):
    q = []
    U = U % len(p)
    q = p[-U:] + p[:-U]
    # alternate solution:
    # for i in range(U):
    #    end = q.pop()
    #    q.insert(0, end)
    print q


def inexact_move(p, U):
    q = []
    for i in range(len(p)):
        s = p[(i-U)%len(p)] * pExact
        s += p[(i-U-1)%len(p)] * pUndershoot
        s += p[(i-U+1)%len(p)] * pOvershoot
        q.append(s)
    return q

def sense_multiple_measurements():
    result = p
    for i in measurements:
        result = sense(result, i)
    print result

def move_multiple(n=2):
    # Move n amount of times
    result = p
    for i in range(n):
        result = inexact_move(result, 1)
    return result

# infinite moves makes the distribution uniform or stationary
# move_multiple(1000)

def localization():
    # sense and move
    # 1. sense the world
    # 2. move
    global p
    for i in range(len(measurements)):
        p = sense(p, measurements[i])
        p = inexact_move(p, motions[i])
    print p

localization()
