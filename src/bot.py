import poker
import tokens
import discord
import asyncio

async def play_game(small_amt, big_amt, start_amt, ch):

    # ASK FOR INPUT
    async def input(prompt):
        await ch.send(prompt)
        return (await client.wait_for('message')).content

    # ONE ROUND OF PLAY
    async def play_rounds(players):
        # INITIALIZED VARIABLES
        small = players[0]
        big = players[1]
        small.bet(small_amt)
        big.bet(big_amt)
        pot = 0
        await ch.send("Small blind: {0}".format(players[0].name))
        await ch.send("Big blind: {0}".format(players[1].name))
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
            if round_over:
                break
            # CHECKING FOR ALL-INS
            if len([p for p in players if p.stack]) > 1 and len([p for p in players if p.still_in]) > 1:
                while True:
                    cp = players[current]

                    if cp.still_in == False:
                        current = (current + 1) % len(players)

                    # ASKING PLAYER ACTION
                    else:
                        if cp.stack > 0:
                            act_valid = False
                            s = f'```  {"Name":<14s}  {"Stack":<5s}  {"Bet":<5s}\n'
                            s += '  '+'-'*26+'\n'
                            for p in players:
                                temp_name = p.name if len(p.name) <= 14 else p.name[:11]+'...'
                                s += '*' if p is cp else ' '
                                s += ' {:<14s}  {:<5s}  {:<5s}\n'.format(temp_name, str(p.stack), str(p.chips_in))
                            s += f'Pot: {str(pot)}\n'
                            s += f'Hand: {cp.hand}\n'
                            s += f'Board: {b}```'
                            await ch.send(s)
                            if cp.chips_in == most_in:
                                act = await input('Options: check, raise... ')
                                while act_valid == False:
                                    if act.lower() not in ['check', 'raise']:
                                        act = await input("Invalid action! Options: check, raise... ")
                                    if act.lower() == 'check':
                                        act_valid = True
                                    elif act.lower() == 'raise':
                                        amount = int(await input('By how much?'))
                                        if amount > cp.stack or amount <= (most_in - cp.chips_in):
                                            act = await input('You cannot bet that amount. Options: check, raise... ')
                                        else:
                                            cp.bet(amount)
                                            most_in = cp.chips_in
                                            last = (current + len(players) - 1) % len(players)
                                            while players[last].still_in == False:
                                                last = (last - 1) % len(players)
                                            act_valid = True
                            else:
                                act = await input('Options: fold, call, raise... ')
                                while act_valid == False:
                                    if act.lower() not in ['fold', 'call', 'raise']:
                                        act = await input("Invalid action! Options: fold, call, raise... ")
                                    if act.lower() == 'fold':
                                        pot += cp.chips_in
                                        cp.chips_in = 0
                                        cp.still_in = False
                                        act_valid = True
                                    elif act.lower() == 'call':
                                        if cp.stack >= (most_in - cp.chips_in):
                                            cp.bet(most_in - cp.chips_in)
                                            act_valid = True
                                        else:
                                            cp.bet(cp.stack)
                                            act_valid = True
                                    elif act.lower() == 'raise':
                                        amount = int(await input('By how much? '))
                                        if amount > cp.stack or amount <= (most_in - cp.chips_in):
                                            act = await input("You cannot bet that amount. Options: fold, call, raise... ")
                                        else:
                                            cp.bet(amount)
                                            most_in = cp.chips_in
                                            last = (current + len(players) - 1) % len(players)
                                            while players[last].still_in == False:
                                                last = (last - 1) % len(players)
                                            act_valid = True
                        # ALL FOLDED CASE
                        if len([p for p in players if p.still_in]) == 1:
                            round_over = True
                            for p in players:
                                if p.still_in:
                                    await ch.send("{0} wins {1}!".format(p.name, str(pot)))
                                    p.stack += pot
                                p.reset()
                            break

                        if current == last:
                            pot += sum([p.chips_in for p in players])
                            most_in = 0
                            for p in players:
                                p.chips_in = 0
                            break
                        current = (current + 1) % len(players)
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
            await ch.send('Board: {0}'.format(b))
            for p in list(players):
                if p.still_in:
                    await ch.send("{0}'s hand: {1}".format(p.name, p.hand))
                p.reset()
                if p.stack == 0:
                    players.remove(p)
            await ch.send("{0} wins {1}!".format(winner.name, str(pot)))

        # GAME OVER CASE
        if len(players) == 1:
            return ch.send(players[0].name, 'wins!')
        # PLAYING MORE ROUNDS CASE
        else:
            players.append(players.pop(0))
            await play_rounds(players)

    # GAME INITIALIZATION
    player_list = []
    for p in range(len(users)):
        player_list.append(Player(users[p], start_amt))
    await play_rounds(player_list)

class Player:
    def __init__(self, user, stack):
        self.still_in = True
        self.chips_in = 0
        self.user = user
        self.name = user.display_name
        self.stack = stack
        self.hand = poker.Hand()
    def bet(self, amount):
        self.stack -= amount
        self.chips_in += amount
    def reset(self):
        self.chips_in = 0
        self.still_in = True
        self.hand.reset()

client = discord.Client()

small_blind = 1
big_blind = 2
starting_chips = 80
users = []

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='with a fish'))
    print('Ready!')

@client.event
async def on_message(message):
    global small_blind, big_blind, starting_chips

    msg = message.content.lower()
    ch = message.channel
    au = message.author

    # ignore own messages
    if au.id == 536822424436473857:
        return

    if msg.startswith('!small '):
        try:
            i = int(msg[7:])
            if i > 0:
                small_blind = i
                await ch.send(f'Small blind set to {i}')
        except: pass
    if msg.startswith('!big '):
        try:
            i = int(msg[5:])
            if i > 0:
                big_blind = i
                await ch.send(f'Big blind set to {i}')
        except: pass
    if msg.startswith('!starting '):
        try:
            i = int(msg[10:])
            if i > 0:
                starting_chips = i
                await ch.send(f'Starting chips set to {i}')
        except: pass

    if msg == '!join':
        if True:#au not in users:
            users.append(au)
            await ch.send(au.display_name + ' has joined')

    if msg == '!start':
        if len(users) >= 2:
            await play_game(small_blind, big_blind, starting_chips, ch)
        else:
            await ch.send('Poker needs at least 2 players!')

client.run(tokens.bot_id)
