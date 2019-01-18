import poker

def play_game(small_amt, big_amt, start_amt):

    def play_rounds(players):
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


        for i in range(4):
            while True:
                cp = players[current]
                if cp.still_in == False:
                    current = (current + 1) % len(players)
                else:
                    print("{0}'s stack: {1}".format(cp.name, str(cp.stack)))
                    print('Pot:', str(pot))
                    print("{0}'s hand: {1}".format(cp.name, cp.hand))
                    print('Board: {0}'.format(b))

                    if cp.stack > 0:
                        act_valid = False
                        act = input("{0}'s action? ".format(cp.name))
                        while act_valid == False:
                            if act.lower() not in ['fold', 'check', 'call', 'raise']:
                                act = input("Invalid action! {0}'s action? ".format(cp.name))
                            if act.lower() == 'check':
                                if cp.chips_in < most_in:
                                    act = input("You cannot check here. {0}'s action? ".format(cp.name))
                                else:
                                    act_valid = True
                            elif act.lower() == 'fold':
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
                                    act = input("You cannot bet that amount. {0}'s action? ".format(cp.name))
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
            if i < 3:
                d.deal(b)
            if len([p for p in players if p.still_in]) == 1:
                round_over = True
                for p in players:
                    p.hand.reset()
                    if p.still_in:
                        print("{0} wins {1}!".format(p.name, str(pot)))
                        p.stack += pot
                        p.chips_in = 0
                break
            current = 0
            last = len(players) - 1
            while players[last].still_in == False:
                last = (last - 1) % len(players)

        if not round_over:
            winner = max([p for p in players if p.still_in], key=lambda x: x.hand.score(b))
            print('Board: {0}'.format(b))
            for p in list(players):
                if p.still_in:
                    print("{0}'s hand: {1}".format(p.name, p.hand))
                p.still_in = True
                p.chips_in = 0
                p.hand.reset()
                if p.stack == 0:
                    players.remove(p)
            print("{0} wins {1}!".format(winner.name, str(pot)))
            winner.stack += pot

        if len(players) == 1:
            return print(players[0].name, ' wins!')
        else:
            players.append(players.pop(0))
            play_rounds(players)


    player_list = []
    num = 0
    while num < 2:
        try:
            num = int(input('How many players? '))
        except ValueError:
            print('Poker needs at least 2 players!')

    for p in range(num):
        player_list.append(Player(input("Player {0} name? ".format(str(p + 1))), start_amt))
    play_rounds(player_list)

class Player:
    still_in = True
    chips_in = 0
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hand = poker.Hand()
    def bet(self, amount):
        self.stack -= amount
        self.chips_in += amount

play_game(1, 2, 160)
