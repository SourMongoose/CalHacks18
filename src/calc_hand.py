def scores(h):
    assert len(h) == 5
    
    h.sort()
    
    # high card to low card
    if flush(h) or high_card(h):
        return [c.value for c in h][::-1]
    # identical cards take precedent
    if four_of_a_kind(h) or full_house(h) or triple(h) or two_pair(h) or pair(h):
        h = sorted(h, key=lambda c: c.value + h.count(c)*1000)
        return [c.value for c in h][::-1]
    # straight
    if straight(h):
        return [c.value for c in h][:4:-1]+[h[4]] if h[4].value == 14 else [c.value for c in h][::-1]

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
    