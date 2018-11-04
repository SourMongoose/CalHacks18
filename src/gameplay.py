import poker
import calc_hand

def play_round(small_amt, big_amt, small, big):
    '''Players is a list of Player instances'''
    board = []
    small.raise(small_amt)
    big.raise(big_amt)
    pot = small_amt + big_amt
    while True:
        s = input("What will {0} do?".format(small.name))
        if s == 'fold' or s == 'call':
            

    input("What will {0} do?".format(big.name))
