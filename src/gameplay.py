import poker

def play_game(small_amt, big_amt, start_amt):

    # ONE ROUND OF PLAY
    def play_rounds(players):
        # INITIALIZED VARIABLES
        small = players[0]
        big = players[1]
        small.bet(small_amt)
        big.bet(big_amt)
        pot = small_amt + big_amt
        print("Small blind: {0}".format(players[0].name))
        print("Big blind: {0}".format(players[1].name))
        most_in = big.chips_in
        last = 1
        current = (last + 1) % len(players)
        d = poker.Deck()
        b = poker.Board()
        for p in players:
            d.deal(p.hand)
        round_over = False

        # BETTING ROUNDS
        for i in range(4):
            # CHECKING FOR ALL-INS
            if len([p for p in players if p.stack]) > 1 and len([p for p in players if p.still_in]) > 1:
                while True:
                    # ALL FOLDED CASE
                    if len([p for p in players if p.still_in]) == 1:
                        round_over = True
                        for p in players:
                            if p.still_in:
                                print("{0} wins {1}!".format(p.name, str(pot)))
                                p.stack += pot
                            p.reset()
                        break
                    cp = players[current]

                    if cp.still_in == False:
                        current = (current + 1) % len(players)

                    # ASKING PLAYER ACTION
                    else:
                        if cp.stack > 0:
                            act_valid = False
                            print(f"It is {cp.name}'s turn")
                            print(f'Stack: {cp.stack}')
                            print('Pot:', str(pot))
                            print(f'Hand: {cp.hand}')
                            print(f'Board: {b}')
                            if cp.chips_in == most_in:
                                act = input('Options: check, raise... ')
                                while act_valid == False:
                                    if act.lower() not in ['check', 'raise']:
                                        act = input("Invalid action! Options: check, raise... ")
                                    if act.lower() == 'check':
                                        act_valid = True
                                    elif act.lower() == 'raise':
                                        amount = int(input('By how much? '))
                                        if amount > cp.stack or amount <= (most_in - cp.chips_in):
                                            act = input("You cannot bet that amount. Options: check, raise... ")
                                        else:
                                            cp.bet(amount)
                                            pot += amount
                                            most_in = cp.chips_in
                                            last = (current + len(players) - 1) % len(players)
                                            while players[last].still_in == False:
                                                last = (last - 1) % len(players)
                                            act_valid = True
                            else:
                                act = input('Options: fold, call, raise... ')
                                while act_valid == False:
                                    if act.lower() not in ['fold', 'call', 'raise']:
                                        act = input("Invalid action! Options: fold, call, raise... ")
                                    if act.lower() == 'fold':
                                        cp.chips_in = 0
                                        cp.still_in = False
                                        act_valid = True
                                    elif act.lower() == 'call':
                                        if cp.stack >= (most_in - cp.chips_in):
                                            pot += (most_in - cp.chips_in)
                                            cp.bet(most_in - cp.chips_in)
                                            act_valid = True
                                        else:
                                            cp.bet(cp.stack)
                                            pot += cp.stack
                                            act_valid = True
                                    elif act.lower() == 'raise':
                                        amount = int(input('By how much? '))
                                        if amount > cp.stack or amount <= (most_in - cp.chips_in):
                                            act = input("You cannot bet that amount. Options: fold, call, raise... ")
                                        else:
                                            cp.bet(amount)
                                            pot += amount
                                            most_in = cp.chips_in
                                            last = (current + len(players) - 1) % len(players)
                                            while players[last].still_in == False:
                                                last = (last - 1) % len(players)
                                            act_valid = True
                        if current == last:
                                break
                        current = (current + 1) % len(players)
            if round_over:
                break
            if i < 3:
                d.deal(b)

            current = 0
            last = len(players) - 1
            while players[last].still_in == False:
                last = (last - 1) % len(players)

        # CARDS SHOWN CASE
        if not round_over:
            winner = max([p for p in players if p.still_in], key=lambda x: x.hand.score(b))
            winner.stack += pot
            print('Board: {0}'.format(b))
            for p in list(players):
                if p.still_in:
                    print("{0}'s hand: {1}".format(p.name, p.hand))
                p.reset()
                if p.stack == 0:
                    players.remove(p)
            print("{0} wins {1}!".format(winner.name, str(pot)))

        # GAME OVER CASE
        if len(players) == 1:
            return print(players[0].name, 'wins!')
        # PLAYING MORE ROUNDS CASE
        else:
            players.append(players.pop(0))
            play_rounds(players)

    # GAME INITIALIZATION
    player_list = []
    num = 0
    while num < 2:
        try:
            num = int(input('How many players? '))
            if num < 2:
                print('Poker needs at least 2 players!')
        except ValueError:
            print("That's not a whole number!")

    for p in range(num):
        player_list.append(Player(input("Player {0} name? ".format(str(p + 1))), start_amt))
    play_rounds(player_list)

class Player:
    def __init__(self, name, stack):
        self.still_in = True
        self.chips_in = 0
        self.name = name
        self.stack = stack
        self.hand = poker.Hand()
    def bet(self, amount):
        self.stack -= amount
        self.chips_in += amount
    def reset(self):
        self.chips_in = 0
        self.still_in = True
        self.hand.reset()

play_game(1, 2, 160)
