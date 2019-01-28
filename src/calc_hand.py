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
        vals = [h[4].value]+[c.value for c in h][:4] if h[4].value == 14 else [c.value for c in h]
    
    return strength * 15**5 + sum([vals[i] * 15**i for i in range(5)])

card_text = {
    2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A'
}

def score_to_str(s):
    strength = s // (15**5)
    s %= 15**5
    vals = []
    for _ in range(5):
        vals.append(s % 15)
        s //= 15
    if strength == 0:
        return card_text[vals[4]] + ' high'
    if strength == 1:
        return f'pair of {card_text[vals[4]]}s'
    if strength == 2:
        return f'two pair, {card_text[vals[4]]}s and {card_text[vals[2]]}s'
    if strength == 3:
        return f'three of a kind, {card_text[vals[4]]}s'
    if strength == 4:
        return f'straight, {card_text[vals[4]]} high'
    if strength == 5:
        return f'flush, {card_text[vals[4]]} high'
    if strength == 6:
        return f'full house, {card_text[vals[4]]}s full of {card_text[vals[1]]}s'
    if strength == 7:
        return f'four of a kind, {card_text[vals[4]]}s'
    if strength == 8:
        return f'straight flush, {card_text[vals[5]]} high'

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
