import poker

def play_game(small_amt, big_amt, start_amt):

    def play_rounds(players):
        small = players[0]
        big = players[1]
        small.bet(small_amt)
        big.bet(big_amt)
        pot = small_amt + big_amt
        most_in = big.chips_in
        active_players = list(players)
        order_play = active_players[2:] + active_players[:2]

        while len(active_players) > 1:

            while not all([p.chips_in == most_in for p in active_players]):
                for p in list(order_play):
                    print("{0}'s stack: {1}".format(p.name, str(p.stack)))
                    print('Pot:', str(pot))
                    if p.stack > 0:
                        act_valid = False
                        act = input("{0}'s action? ".format(p.name))
                        while act_valid == False:
                            if act.lower() not in ['fold', 'check', 'call', 'raise']:
                                act = input("Invalid action! {0}'s action? ".format(p.name))
                            if act.lower() == 'check':
                                if p.chips_in < most_in:
                                    act = input("You cannot check here. {0}'s action? ".format(p.name))
                                else:
                                    act_valid = True
                            elif act.lower() == 'fold':
                                p.chips_in = 0
                                order_play.remove(p)
                                active_players.remove(p)
                                act_valid = True
                            elif act.lower() == 'call':
                                if p.stack >= (most_in - p.chips_in):
                                    pot += (most_in - p.chips_in)
                                    p.bet(most_in - p.chips_in)
                                    act_valid = True
                                else:
                                    p.bet(p.stack)
                                    pot += p.stack
                                    act_valid = True
                            elif act.lower() == 'raise':
                                amount = int(input('By how much? '))
                                if amount > p.stack or amount <= (most_in - p.chips_in):
                                    act = input("You cannot bet that amount. {0}'s action? ".format(p.name))
                                else:
                                    p.bet(amount)
                                    pot += amount
                                    most_in = p.chips_in
                                    order_play = order_play[:order_play.index(p)]
                                    act_valid = True


            print('first bets done')
            return


        for p in list(players):
            if p.stack == 0:
                players.remove(p)
        if len(players) == 1:
            return print(players[0].name, ' wins!')
        else:
            play_rounds(players.append(players.pop(0)))


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
    folded = False
    chips_in = 0
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
    def bet(self, amount):
        self.stack -= amount
        self.chips_in += amount

play_game(1, 2, 160)
