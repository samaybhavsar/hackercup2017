from math import atan2, degrees

def is_black(percent, x, y):
    x = x - 50
    y = y - 50
    if percent == 0:
        return False
    if not in_circle(x,y):
        return False
    canonical_degree = (degrees(atan2(y,x)) + 360) % 360
    degree_from_top_clockwise = (90 - canonical_degree) % 360
    return degree_from_top_clockwise <= percent * 360/float(100)

def in_circle(x,y):
    radius = (x)**2 + (y)**2
    if radius > 2500:
        return False
    else:
        return True

t = int(raw_input())  # read a line with a single integer
for i in xrange(1, t + 1):
    percent, x, y = map(int, raw_input().strip().split())
    result = "black" if is_black(percent, x, y) else "white"
    print "Case #%s: %s" % (i, result)
