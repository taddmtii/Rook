"""
Serves as the blueprint and construction of our four player objects that
have set attributes such as a number designated to each and thier own
unique hand (or list) of cards.
"""

class Player:
    def __init__(self, pos, hand = []):
        self.pos = pos
        self.hand = hand
        self.bet = 0
    
    def get_pos(self):
        return self.pos
    
    def get_hand(self):
        return self.hand
    
    def get_bet(self):
        return self.bet
    
    def set_bet(self, bet):
        self.bet = bet