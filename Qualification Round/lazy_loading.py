from collections import deque

def solve(list_of_boxes):
    list_of_boxes.sort()
    d = deque(list_of_boxes)
    trips = 0
    while d:
        heavy_item = d.pop()
        if heavy_item < 50:
            boxes_needed = 50/heavy_item + (50 % heavy_item != 0) - 1
            for _ in range(boxes_needed):
                try:
                    d.popleft()
                except IndexError:
                    return trips

        trips += 1
    return trips

t = int(raw_input())
for i in range(1, t+1):
    items = []
    num_items = int(raw_input().strip())
    for item in range(num_items):
        items.append(int(raw_input().strip()))
    result = solve(items)
    print "Case #%s: %s" % (i, result)
