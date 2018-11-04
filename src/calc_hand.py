def score(h):
    assert len(h) == 5
    
    h.sort()
    
    strength = 0
    if pair(h): strength = 1
    elif two_pair(h): strength = 2
    elif triple(h): strength = 3
    elif straight(h): strength = 4
    elif flush(h): strength = 5
    elif full_house(h): strength = 6
    elif four_of_a_kind(h): strength = 7
    if straight_flush(h): strength = 8
    
    # high card to low card
    if flush(h) or high_card(h):
        vals = [c.value for c in h]
    # identical cards take precedent
    elif four_of_a_kind(h) or full_house(h) or triple(h) or two_pair(h) or pair(h):
        h = sorted(h, key=lambda c: c.value + h.count(c)*1000)
        vals = [c.value for c in h]
    # straight
    elif straight(h):
        vals = [h[4]]+[c.value for c in h][:4] if h[4].value == 14 else [c.value for c in h]
    
    return strength * 15**5 + sum([vals[i] * 15**i for i in range(5)])

def straight_flush(h):
    return straight(h) and flush(h)

def four_of_a_kind(h):
    return h[0] == h[1] == h[2] == h[3] \
        or h[1] == h[2] == h[3] == h[4]

def full_house(h):
    return h[0] == h[1] == h[2] != h[3] == h[4] \
        or h[0] == h[1] != h[2] == h[3] == h[4]

def flush(h):
    return h[0].suit == h[1].suit == h[2].suit == h[3].suit == h[4].suit

def straight(h):
    a, b, c, d, e = h[0].value, h[1].value, h[2].value, h[3].value, h[4].value
    return a == b-1 == c-2 == d-3 == e-4 \
        or (e == 14 and a == b-1 == c-2 == d-3 == 2)

def triple(h):
    return h[0] == h[1] == h[2] != h[3] != h[4] \
        or h[0] != h[1] == h[2] == h[3] != h[4] \
        or h[0] != h[1] != h[2] == h[3] == h[4]

def two_pair(h):
    return h[0] == h[1] != h[2] == h[3] != h[4] \
        or h[0] == h[1] != h[2] != h[3] == h[4] \
        or h[0] != h[1] == h[2] != h[3] == h[4]

def pair(h):
    return h[0] == h[1] != h[2] != h[3] != h[4] \
        or h[0] != h[1] == h[2] != h[3] != h[4] \
        or h[0] != h[1] != h[2] == h[3] != h[4] \
        or h[0] != h[1] != h[2] != h[3] == h[4]

def high_card(h):
    return h[0] != h[1] != h[2] != h[3] != h[4] and not straight(h) and not flush(h)
    