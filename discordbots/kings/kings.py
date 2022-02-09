import random
import yaml
import discord
import numpy as np

class Kings():
    def __init__(self, names):
        self.new_deck()
        self.card_images = {card: discord.File(f'card_images/{card}.png') for card in self.cards}
        
        self.names = names
        self.name_ids = {name: 0 for name in names}
        self.current_player = names[0]
        
        self.kings = 0
        self.kings_left = ['H', 'D', 'S', 'C']
        self.queens = 0
        self.queens_left = ['H', 'D', 'S', 'C']

        self.questionnaire = 'Nobody'

        with open('rules.yml', 'r+') as file:
            self.rules = yaml.safe_load(file)

    def next_player(self):
        self.current_player = self.names[0]

        self.names = self.names[1:]
        self.names.append(self.current_player)

    def still_need_names(self):
        return 0 in self.name_ids.values()

    def check_correct_player(self, player_id):
        return player_id == self.name_ids[self.current_player]

    def next_card(self):
        self.current_card = self.cards.pop()

    def new_deck(self):
        suits = ['H', 'S', 'C', 'D']
        suits_52 = np.repeat(suits, 13).tolist()
        values = list(range(1,14))*4

        self.cards = [f"{suit}{value}" for suit, value in list(zip(values,suits_52))]

        random.shuffle(self.cards)