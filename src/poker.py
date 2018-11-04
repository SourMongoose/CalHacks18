import calc_hand

class Card:
    values = {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A'
    }
    for i in range(2,11): values[i] = str(i)
    suits = {
        'diamonds': '♦',
        'clubs': '♣',
        'hearts': '♥',
        'spades': '♠'
    }
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __str__(self):
        return Card.values[self.value] + Card.suits[self.suit]

class Hand:
    def __init__(self, size=2):
        self.reset()
        self.size = size
    
    def reset(self):
        self.cards = []
    
    def score(self, board):
        assert len(self.cards) == self.size
        assert len(board.cards) == board.flop + board.turn + board.river
        
        all_cards = self.cards + board.cards
        total = len(all_cards)
        
        max_score = 0
        
        # try omitting cards i and j
        for i in range(total):
            for j in range(i+1, total):
                max_score = max(max_score, calc_hand.score(all_cards[:i]+all_cards[i+1:j]+all_cards[j+1:]))
        
        return max_score
    
    def __str__(self):
        return ' '.join(str(c) for c in self.cards)

class Board:
    flop = 3
    turn = 1
    river = 1
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.cards = []
        self.burn = []
    
    def __str__(self):
        return ' '.join(str(c) for c in self.cards)

from random import shuffle

class Deck:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.cards = []
        for v in Card.values:
            for s in Card.suits:
                self.cards.append(Card(v, s))
        shuffle(self.cards)
    
    def pop(self):
        return self.cards.pop()
    
    def deal(self, obj):
        if isinstance(obj, Hand):
            for _ in range(obj.size):
                obj.cards.append(self.pop())
        elif isinstance(obj, Board):
            if len(obj.cards) == 0:
                obj.burn.append(self.pop())
                for _ in range(obj.flop): obj.cards.append(self.pop())
            elif len(obj.cards) == obj.flop:
                for _ in range(obj.turn): obj.cards.append(self.pop())
            elif len(obj.cards) == obj.flop + obj.turn:
                for _ in range(obj.river): obj.cards.append(self.pop())
    
