import poker
import calc_hand
import tokens
import discord
import asyncio

MSG = "too many hands"

async def play_game(small_amt, big_amt, start_amt, ch):
    global started
    started = True
    ended = False

    # ONE ROUND OF PLAY
    async def play_rounds(players, pot=0):

        async def check_action(cp):

            # ASK FOR INPUT
            async def input(prompt):
                nonlocal ended
                if prompt: await ch.send(prompt)
                #await asyncio.sleep(0.5)
                msg = await client.wait_for('message', check=lambda msg: msg.author == cp.user or msg.content == '!endgame')
                if msg.content == '!endgame':
                    ended = True
                return msg.content

            nonlocal last, most_in
            act_valid = False
            if cp.chips_in == most_in:
                act = await input('Options: check, raise... ')
                while act_valid == False:
                    if act == '!endgame':
                        return
                    if act.lower()[:5] not in ['check', 'raise']:
                        act = await input('')
                    if act.lower() == 'check':
                        act_valid = True
                    elif act.lower() == 'raise' or act.lower().startswith('raise'):
                        try:
                            if act.lower() == 'raise':
                                amount = int(await input('By how much?'))
                            elif act.lower().startswith('raise to '):
                                amount = int(act.lower()[9:]) - cp.chips_in
                            elif act.lower().startswith('raise '):
                                amount = int(act.lower()[6:])
                            else:
                                raise
                        except:
                            act = await input('Invalid input. Options: check, raise... ')
                            continue
                        if (amount > cp.stack or amount < big_amt) and amount != cp.stack:
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
                    if act == '!endgame':
                        return
                    if act.lower()[:5] not in ['fold', 'call', 'raise']:
                        act = await input('')
                    if act.lower() == 'fold':
                        cp.still_in = False
                        act_valid = True
                    elif act.lower() == 'call':
                        if cp.stack >= (most_in - cp.chips_in):
                            cp.bet(most_in - cp.chips_in)
                            act_valid = True
                        else:
                            cp.bet(cp.stack)
                            act_valid = True
                    elif act.lower() == 'raise' or act.lower().startswith('raise'):
                        try:
                            if act.lower() == 'raise':
                                amount = int(await input('By how much?'))
                            elif act.lower().startswith('raise to '):
                                amount = int(act.lower()[9:]) - cp.chips_in
                            elif act.lower().startswith('raise '):
                                amount = int(act.lower()[6:])
                            else:
                                raise
                        except:
                            act = await input('Invalid input. Options: fold, call, raise... ')
                            continue
                        if (amount > cp.stack or amount < most_in * 2 - cp.chips_in or amount < big_amt) and amount != cp.stack:
                            act = await input('You cannot bet that amount. Options: fold, call, raise... ')
                        else:
                            cp.bet(amount)
                            most_in = cp.chips_in
                            last = (current + len(players) - 1) % len(players)
                            while players[last].still_in == False:
                                last = (last - 1) % len(players)
                            act_valid = True

        async def round_winner(plist):
            nonlocal pot, winners
            highest = max([p.hand.score(b) for p in plist if p.still_in])
            winners = [p for p in plist if p.hand.score(b) == highest and p.still_in]
            min_chips = min([w.side_potential for w in winners])

            # SIDEPOTS CASE
            if any(p.side_potential > min_chips for p in plist):
                sidepot = sum([p.side_potential for p in plist if p.side_potential <= min_chips])
                for p in plist:
                    if p.side_potential > min_chips:
                        p.side_potential -= min_chips
                    else:
                        p.side_potential = 0
                sidepot += min_chips * len([p for p in plist if p.side_potential])
                pot -= sidepot
                for w in winners:
                    w.stack += sidepot // len(winners)
                for w in winners:
                    await ch.send("{0} wins sidepot of {1} with {2}!".format(
                        w.name, str(sidepot // len(winners)), calc_hand.score_to_str(highest)))
                pot += sidepot % len(winners)
                await round_winner([p for p in plist if p.side_potential])


            # REGULAR WIN CASE
            else:
                for w in winners:
                    w.stack += pot // len(winners)
                for w in winners:
                    await ch.send("{0} wins {1} with {2}!".format(
                        w.name, str(pot // len(winners)), calc_hand.score_to_str(highest)))

        # INITIALIZED VARIABLES
        if ended:
            await ch.send('Game ended')
            return
        small = players[0]
        big = players[1]
        if small.stack < small_amt:
            small.bet(small.stack)
        else:
            small.bet(small_amt)
        if big.stack < big_amt:
            big.bet(big.stack)
        else:
            big.bet(big_amt)
        #await ch.send("Small blind: {0}".format(players[0].name))
        #await ch.send("Big blind: {0}".format(players[1].name))
        most_in = max([p.chips_in for p in players])
        last = 1
        current = (last + 1) % len(players)
        d = poker.Deck()
        b = poker.Board()
        for p in players:
            d.deal(p.hand)
            await p.user.send(f'Your hand:\n{p.hand}')
        round_over = False

        # BETTING ROUNDS
        for i in range(4):
            if round_over:
                break
            # CHECKING FOR ALL-INS
            if len([p for p in players if p.stack and p.still_in]) > 1:
                while True:
                    cp = players[current]

                    if cp.still_in == False:
                        current = (current + 1) % len(players)

                    # ASKING PLAYER ACTION
                    else:
                        if cp.stack > 0:
                            s = f'```  {"Name":<14s}  {"Stack":<5s}  {"Bet":<5s}\n'
                            s += '  '+'-'*26+'\n'
                            for u in range(len(users)):
                                for p in players:
                                    if p.place == u:
                                        temp_name = p.name if len(p.name) <= 14 else p.name[:11]+'...'
                                        s += '*' if p is cp else ' '
                                        s += ' {:<14s}  {:<5s}  {:<5s}  {}\n'.format(temp_name, str(p.stack), str(p.chips_in), 'SB' if p==players[0] else 'BB' if p==players[1] else '')
                            s += f'```\nPot: {str(pot)}\n'
                            #s += f'Hand: {cp.hand}\n'
                            s += f'Board: {b}\n\n'
                            s += f'{cp.user.mention}\'s turn'
                            await ch.send(s)
                            await check_action(cp)
                            if ended:
                                await ch.send('Game has been reset.')
                                started = False
                                return
                        # ALL FOLDED CASE
                        if len([p for p in players if p.still_in]) == 1:
                            round_over = True
                            pot += sum([p.chips_in for p in players])
                            for p in players:
                                if p.still_in:
                                    winners = [p]
                                    await ch.send("{0} wins {1}!".format(p.name, str(pot)))
                                    p.stack += pot
                                p.reset()
                            break

                        if current == last:
                            pot += sum([p.chips_in for p in players])
                            most_in = 0
                            for p in players:
                                p.side_potential += p.chips_in
                                p.chips_in = 0
                            break
                        current = (current + 1) % len(players)

            if i < 3:
                d.deal(b)

            current = 0
            last = len(players) - 1
            if len(users) == 2:
                current, last = 1, 0
            while players[last].still_in == False:
                last = (last - 1) % len(players)

        # CARDS SHOWN CASE
        if not round_over:
            await ch.send('Board: {0}'.format(b))
            for p in players:
                if p.still_in:
                    await ch.send("{0}'s hand: {1}".format(p.name, p.hand))
            await round_winner(players)
            for p in list(players):
                p.reset()
                if p.stack == 0:
                    players.remove(p)



        # GAME OVER CASE
        if len(players) == 1:
            await ch.send(players[0].name+' wins!')
            return
        # PLAYING MORE ROUNDS CASE
        else:
            players.append(players.pop(0))
            await play_rounds(players, pot % len(winners))

    # GAME INITIALIZATION
    player_list = []
    for p in range(len(users)):
        player_list.append(Player(users[p], start_amt, p))
    await play_rounds(player_list)

    started = False
    users.clear()

class Player:
    def __init__(self, user, stack, place=0):
        self.still_in = True
        self.chips_in = 0
        self.side_potential = 0
        self.user = user
        self.name = user.display_name
        self.place = place
        self.stack = stack
        self.hand = poker.Hand()
    def bet(self, amount):
        self.stack -= amount
        self.chips_in += amount
    def reset(self):
        self.chips_in = 0
        self.side_potential = 0
        self.still_in = True
        self.hand.reset()

client = discord.Client()

small_blind = 1
big_blind = 2
starting_chips = 80
users = []
started = False

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=MSG))
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

    if msg.startswith('!msg '):
        await client.change_presence(activity=discord.Game(name=msg[5:]))

    if not started:
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
                await ch.send(au.display_name + ' has joined\nCurrent players: ' + ', '.join(p.display_name for p in users))
        if msg == '!leave':
            if au in users:
                users.remove(au)
                await ch.send(au.display_name + ' has left\nCurrent players: ' + ', '.join(p.display_name for p in users))

        if msg == '!start':
            if len(users) >= 2:
                await play_game(small_blind, big_blind, starting_chips, ch)
            else:
                await ch.send('Poker needs at least 2 players!')

client.run(tokens.bot_id)
