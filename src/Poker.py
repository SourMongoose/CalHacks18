def winning_hand(hand1, hand2):
    if hand1.value > hand2.value:
        return hand1.player
    elif hand1.value < hand2.value:
        return hand2.player

hand_values = {'strflush': 900, 'bomb': 800, 'house': 700, 'flush': 600, 'str': 500, 'trip': 400, 'pairs': 300, 'pair': 200, 'high': 100}
card_values = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: '10', 9: '9', 8: '8', 7: '7', 6: '6', 5: '5', 4: '4', 3: '3', 2: '2'}


def pot_winner(playa):
    if not playa:
        print('The pot is split!')
    else:
        print('{0} wins the pot'.format(playa.name))

class Hand:
    '''The Hand class has instance variables VALUE, signifying the total value of the hand, CARDS, a list of 2 Card instances,
    and PLAYER, an instance of the Player Class'''
    def __init__(self, cards, player, board):
        '''Argument board is a list of cards'''
        assert len(cards) == 2, 'Each hand should have 2 cards!'
        self.cards = cards
        self.player = player

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

class Pot:
    def __init__(self, )

def find_strflsh(cards, board):
    entire = cards + board
    for dex in range(len(entire)):
        rest = entire[:dex + 1] + entire[dex + 1:]
