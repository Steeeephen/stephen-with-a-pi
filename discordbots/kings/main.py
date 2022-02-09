import os
import discord

from dotenv import load_dotenv
from kings import Kings

global kings_class
kings_class = None

def main():
  load_dotenv()
  TOKEN = os.getenv('DISCORD_TOKEN')

  client = discord.Client()

  @client.event
  async def on_ready():
      print(f'{client.user} has connected to Discord!')

  @client.event
  async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$kings '):
        players = message.content.split(' ')[1:]

        global kings_class
        kings_class = Kings(names=players)

        newline = '\n'
        await message.channel.send(
            '---\n**New Game**\n---\n'
            f'Players playing:\n{newline.join(players)}\n\n' 
            'Claim your name with `$name <name>`\n'
            f'e.g. `$name {players[0]}`')

    if message.content.startswith('$name'):
        if kings_class is None:
            return

        still_needed_names = kings_class.still_need_names()

        name = message.content.split(' ')[1]
        kings_class.name_ids[name] = message.author.id

        await message.channel.send(f"{message.author} is {name}")

        no_more_names_needed = not kings_class.still_need_names()

        if no_more_names_needed and still_needed_names:
            await message.channel.send(
                f'Next Player: {kings_class.names[0]}\nType `$card` to pick a card')

    if message.content.startswith('$card'):
        kings_class.next_card()

        if kings_class is None:
            return

        if kings_class.still_need_names():
            unclaimed_names = [key for key, value in kings_class.name_ids.items() if value == 0]

            await message.channel.send(
                f"Still need some players to claim their names: {', '.join(unclaimed_names)}")

            return

        if not kings_class.check_correct_player(message.author.id):
            await message.channel.send('Please wait your turn')

            return

        if kings_class.current_card is None:
            await message.channel.send('No Cards Left!')
            
            return

        card_num = int(kings_class.current_card[:-1])
        card_suit = kings_class.current_card[-1]


        if card_num == 12 and card_suit in kings_class.queens_left:
            kings_class.queens_left.remove(card_suit)

            if kings_class.questionnaire == kings_class.current_player:
                kings_class.queens += 1
            else:
                kings_class.queens = 1

            kings_class.questionnaire = kings_class.current_player
        
        await message.channel.send(
            f"---\n{card_num}: **{kings_class.rules[card_num]['name']}**\n"
            f"{kings_class.rules[card_num]['rule']}\n---\n",
            file=kings_class.card_images[kings_class.current_card]
        )

        if card_num == 13 and card_suit in kings_class.kings_left:
            kings_class.kings += 1
            kings_class.kings_left.remove(card_suit)

            if kings_class.kings < 4:
                await message.channel.send(f'{4-kings_class.kings} remaining')
            else:
                await message.channel.send(f"Winner: {kings_class.current_player}")

                kings_class = None

        kings_class.next_player()

        await message.channel.send(f"Next Player: {kings_class.current_player}",)

    if message.content.startswith('$queens'):
        if kings_class is None:
            return

        await message.channel.send(f'{kings_class.questionnaire} is the Questionnaire (x{kings_class.queens})')

    if message.content.startswith('$count'):
        if kings_class is None:
            return

        await message.channel.send(f'{4-kings_class.kings} Kings remaining out of {len(kings_class.cards)+1} cards')

    if message.content.startswith('$deck'):
        if kings_class is None:
            return

        deck_left = """``` 
             |---+---+---+---+---+---+---+---+---+----+---+---+---+
             | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | J | Q | K |
            -|---+---+---+---+---+---+---+---+---+----+---+---+---+
            ♥|{H}
            -|---+---+---+---+---+---+---+---+---+----+---+---+---+
            ♦|{D}
            -|---+---+---+---+---+---+---+---+---+----+---+---+---+
            ♣|{C}
            -|---+---+---+---+---+---+---+---+---+----+---+---+---+
            ♠|{S}
            -|---+---+---+---+---+---+---+---+---+----+---+---+---+```
        """

        suits = {suit: "" for suit in ['H', 'D', 'C', 'S']}

        for suit in suits.keys():
            suit_cards = [int(card[:-1]) for card in kings_class.cards if card.endswith(suit)]

            suit_string = ""

            for i in range(1, 14):
                num_chars = 3 + (i==10)

                suit_string += f"{' ' * num_chars if i in suit_cards else ' x' + ' ' * (num_chars-2)}|"

            suits[suit] = suit_string

        deck_left = deck_left.format(**suits)

        await message.channel.send(deck_left)
        
  client.run(TOKEN)

if __name__ == '__main__':
    main()