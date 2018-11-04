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
    def __init__(self, deck, size=2):
        self.cards = [deck.pop() for _ in range(size)]
    
    def best_hand(self, board):
        
        

class Player:
    '''The Player class has instance variables NAME, the name of the player, and STACK, the amount of chips the player has'''
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
    '''def raise(self, amount):

    def fold(self):

    def call(self, amount):'''

class Card:
    '''The Card class has instance variables SUIT and VALUE'''
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

def find_strflsh(cards, board):
    entire = cards + board
    for dex in range(len(entire)):
        rest = entire[:dex + 1] + entire[dex + 1:]
