import sys
import random
from player import Player

class Rook:
    def __init__(self, number = 0, color = ''):
        self.number = number
        self.color = color
        self.player_won = 0
        self.final_bet = 0
        self.players = []
        self.kitty = []
        self.choice = ''
        self.rook_bird_high = False
        self.discardPile = []
        self.trump = ''
        self.team1_points = 0 # P1 and P3
        self.team2_points = 0 # P2 and P4
        self.team1_overall = 0
        self.team2_overall = 0
        self.calc_score_count = 0
        self.discardPoints = 0
        self.point_goal = 0
        self.team1_isSet = False
        self.team2_isSet = False
    
    def __str__(self):
        return f'{self.color}, {self.number}'
    
    def __repr__(self):
        return f'RookCard({self.color}, {self.number})'

    def start(self):
        """
        Handles explanation and beginning information needed to start the game.
        """
        welcome_str = r"""
 __          __  _                            _          _____             _    _ 
 \ \        / / | |                          | |        |  __ \           | |  | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |__) |___   ___ | | _| |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  |  _  // _ \ / _ \| |/ / |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | | \ \ (_) | (_) |   <|_|
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_|  \_\___/ \___/|_|\_(_)
                                                                                                                                                                                                                
"""
        print(welcome_str)
        q = input('Will the Rook Bird be (H)igh or (L)ow?: ')
        if q == 'H' or q == 'h':
            self.rook_bird_high = True
        elif q == 'L' or q == 'l':
            self.rook_bird_high = False
        else:
            print('Try again')
        print('------------------------------------------------------------')
        self.point_goal = input("What would you like the point goal to be? (300 or 500 recommended): ")
        if self.point_goal.isdigit():
            self.point_goal = int(self.point_goal)
        else:
            print('Not a Valid Entry')
        print('------------------------------------------------------------')
        self.restart()


    def create_deck(self):
        """
        Creates a deck of RookCard Objects.
        """
        numbers = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        colors = ['Green', 'Yellow', 'Red', 'Black']
        deck = []
        for number in numbers:
            for color in colors:
                deck.append(Rook(number, color))

        #value of rookbird is either high or low depending on user input.
        if self.rook_bird_high == True:
            rookBird = Rook('High', 'Rook Bird')
        else:
            rookBird = Rook('Low', 'Rook Bird')
        deck.append(rookBird)
        random.shuffle(deck) #shuffle the deck
        self.deal(deck)

    def deal(self, deck):
        """
        Deals all of the cards.
        """
        player1_hand = []
        player2_hand = []
        player3_hand = []
        player4_hand = []

        for card in range(5):
            card = random.choice(deck)
            self.kitty.append(card)
            deck.remove(card)
        
        for card in range(9):
            card = random.choice(deck)
            player1_hand.append(card)
            deck.remove(card)
            card = random.choice(deck)
            player2_hand.append(card)
            deck.remove(card)
            card = random.choice(deck)
            player3_hand.append(card)
            deck.remove(card)
            card = random.choice(deck)
            player4_hand.append(card)
            deck.remove(card)

        #initalize 4 player objects
        player1 = Player(1, player1_hand)
        player2 = Player(2, player2_hand)
        player3 = Player(3, player3_hand)
        player4 = Player(4, player4_hand)
        self.players.append(player1)
        self.players.append(player2)
        self.players.append(player3)
        self.players.append(player4)

        self.betting()
            
    def betting(self):
        """
        Each player gets a turn to bet against each player (even the ones on thier own team).
        """

        faceUpCard = self.kitty[-1]
        print('Lets start the betting phase! Bets must be divisble by 5.')
        print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
        print(f'The kitties face up card is {faceUpCard}')
        print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
        highest = 70 # base bid
        i = 0 #player index
        p_count = 0 # pass count
        while True:
            if i == 4:
                i = 0
            if self.players[i].get_bet() == 'pass':
                i += 1
                continue
            elif p_count == 3:
                break
            new_bet = input(f'Player {i + 1} What would you like to bet? (currently at {highest}, type pass to pass): ')
            if new_bet == '120':
                self.player_won = self.players[i]
                self.final_bet = 120
                break
            if new_bet.isdigit() and int(new_bet) > 120:
                print('--------------------------------------------------------------------------------')
                print('That bid is too high! There are only 120 points in the deck. Please try again.')
                print('--------------------------------------------------------------------------------')
                continue
            if new_bet.isdigit() and int(new_bet) > highest and int(new_bet) % 5 == 0:
                self.players[i].set_bet(int(new_bet))
                highest = int(new_bet)
                self.final_bet = highest
                self.player_won = self.players[i]
            elif new_bet == 'pass':
                self.players[i].set_bet('pass')
                p_count += 1
            else:
                print('Invalid Input / bet is NaN, not higher than the previous or is not divisible by 5.')
                i -= 1
            i += 1
        print('------------------------------------------------------------')
        print(f'Player {i + 1} won the bet with {self.final_bet}!')
        print('------------------------------------------------------------')
        self.deal_kitty(self.player_won.get_pos())
    
    def deal_kitty(self, winner):
        """
        Deals the kitty to the player that won the bid.
        """
        for card in self.kitty:
            self.players[winner - 1].hand.append(card)
        self.trump_color(self.player_won.get_pos())

        self.discard(self.player_won.get_pos())
    
    def enumerate_list(self, player : int):
        """
        Enumerates the list of player cards so that it is more readable to the end user.
        """
        for number, letter in enumerate(self.players[player].get_hand(), 1):
            print(f'Card {number}: {letter}')
        print()

    def discard(self, winner):
        """
        Method to handle the discard of cards gained from the kitty.
        Returns list of discarded cards for use at end of the game.
        """
        # Please discard 5 cards (thinking of showing list and player can just pick index of cards that will be popped out of list)
        count = 0
        while count < 6:
            if count == 5:
                print(f'This is your hand:')
                self.enumerate_list(winner - 1)
                print('-------------------------------------------------------------')
                conf = input(f'Do you wish to start the game? (Y or N): ')
                if conf == 'Y' or conf == 'y':
                    count += 1
                    continue
                elif conf == 'N' or conf == 'n':
                    count = 0
                    cards_to_append = list(self.discardPile)  # copy of discardPile
                    for card in cards_to_append:
                        self.players[winner - 1].get_hand().append(card)
                        self.discardPile.remove(card)
                    print('------------------------------------------------------------')
                    continue

            self.enumerate_list(winner - 1)
            self.cardToDiscard = input((f'Player {winner}, please discard five cards one by one separated by a space. '))
            remove_cards = self.cardToDiscard.split(' ')
            if remove_cards == '' or len(remove_cards) != 5:
                print('Invalid, please try again.')
                continue
            remove_card_values = []
            for value in remove_cards:
                remove_card_values.append(self.players[winner - 1].get_hand()[int(value) - 1])
            
            for card in remove_card_values:
                self.discardPile.append(card)
                self.players[winner - 1].get_hand().remove(card)

            print('------------------------------------------------------------')
            print('Here is the Discard Pile: ')
            for num, let in enumerate(self.discardPile, 1):
                print(f'Card: {num}: {let}')
            print('------------------------------------------------------------')
            count = 5

        print('------------------------------------------------------------')
        #discardPile DOES work correctly. All cards are appended for end of the game.
        self.game_loop(self.player_won.get_pos())


    def trump_color(self, winner):
        """
        Designates the trump color for the game to whatever the winner
        of the bidding so chooses.
        """
        while True:
            print(f'Player {winner}, what color would you like trump to be?: ')
            self.trump = input(f'You can choose between (Green), (Yellow), (Red), (Black):  ')
            if self.trump == 'Green' or self.trump == 'Yellow' or self.trump == 'Red' or self.trump == 'Black':
                break
            else:
                print(f'That is not a valid choice, please ensure that you spelt your decision right.')
                continue
        return self.trump
    
    def discard_add(self, winner):
        """
        Adds discard points to whichever team is awarded them.
        """
        self.discardPoints = 0
        if self.team1_isSet == False:
            for card in self.discardPile:
                if card.number == 5:
                    self.discardPoints += 5
                elif card.number == 10 or card.number == 14:
                    self.discardPoints += 10
                elif card.color == 'Rook Bird':
                    self.discardPoints += 20
        if winner % 2 == 0:
            self.team1_overall += self.discardPoints
        else:
            self.team2_overall += self.discardPoints

    def round_win(self, winner):
        """
        This method should store the scores of each team (player1 & player3, player2 & player4)
        based on how many points each team had depending on factors handled in the calculateScore func.
        """

        if self.player_won.get_pos() == 1 or self.player_won.get_pos() == 3:
            if self.team1_points < self.final_bet:
                self.team1_overall -= self.final_bet
                self.team1_isSet = True
                self.team2_overall += self.team2_points
                self.discard_add(winner)
                print(f'Team 1 got set by {self.final_bet}, thier score is now {self.team1_overall}. ')
            else:
                self.team1_overall += self.team1_points
                self.team2_overall += self.team2_points
                print(f'Team 1 won, their score is now {self.team1_overall}')
        else:
            if self.team2_points < self.final_bet:
                self.team2_overall -= self.final_bet
                self.team2_isSet = True
                self.team1_overall += self.team1_points
                self.discard_add(winner)
                print(f'Team 2 got set by {self.final_bet}, thier score is now {self.team2_overall}')
            else:
                self.team2_overall += self.team2_points
                self.team1_overall += self.team1_points
                print(f'Team 2 won, their score is now {self.team2_overall}')
        
        if self.team1_overall >= self.point_goal:
            print(f'Overall Team 1 Points: {self.team1_overall}')
            print(f'Overall Team 2 Points: {self.team2_overall}')
            print('---------------------------------------------------')
            print(f'Team 1 wins the game with {self.team1_overall}! ')
            print('---------------------------------------------------')
            confirmation = input('Do you wish to start a new game? (Y or N): ')
            if confirmation == 'Y':
                self.start()
                self.team1_overall = 0
                self.team2_overall = 0
            elif confirmation == 'N':
                sys.exit(0)
            else:
                print('Invalid Input')
        elif self.team2_overall >= self.point_goal:
            print(f'Overall Team 1 Points: {self.team1_overall}')
            print(f'Overall Team 2 Points: {self.team2_overall}')
            print('---------------------------------------------------')
            print(f'Team 2 Wins the game with {self.team2_overall}! ')
            print('---------------------------------------------------')
            confirmation = input('Do you wish to start a new game? (Y or N): ')
            if confirmation == 'Y':
                self.start()
                self.team1_overall = 0
                self.team2_overall = 0
            elif confirmation == 'N':
                sys.exit(0)
            else:
                print('Invalid Input')
        else:
            print(f'Overall Team 1 Points: {self.team1_overall}')
            print(f'Overall Team 2 Points: {self.team2_overall}')
            confirmation = input('Do you wish to start the next game? (Y or N): ')
            if confirmation == 'Y':
                self.restart()
            elif confirmation == 'N':
                sys.exit(0)
            else:
                print('Invalid Input')

    def calculate_score(self, winner : int, pile : dict):
        """
        Determines if which ever team won is set or not, if they had enough points to win and how many points the other
        team had so that it can be added to the score_board func.
        """

        points = 0
        for card in pile.values():
            if card.number == 5:
                points += 5
            elif card.number == 10 or card.number == 14:
                points += 10
            elif card.color == 'Rook Bird':
                points += 20

        if winner % 2 == 0:
            self.team1_points += points
        else:
            self.team2_points += points
        self.calc_score_count += 1

        print(f'Team 1 Points: {self.team1_points}')
        print(f'Team 2 Points: {self.team2_points}')
        if self.calc_score_count == 9:
            self.calc_score_count = 0
            self.round_win(winner)

    def check_win(self, pile : dict):
        """
        Checks who won the round.
        """
        # {0 : Card, 1 : Card, 2 : Card}
        
        trumps_played = {}
        rook_bird_player = -1
        winner = -1
        highest = 0
        for player, card in pile.items():
            if card.color == self.trump:
                trumps_played[card.number] = player
                # Red, 8 (Player 1) -> {8 : 0}
            elif card.color == 'Rook Bird':
                rook_bird_player = player
        if rook_bird_player != -1 and (self.rook_bird_high or len(trumps_played) == 0):
            winner = rook_bird_player
        elif len(trumps_played) > 0:
            winningNum = max(trumps_played)
            winner = trumps_played[winningNum]
        else:
            for player, card in pile.items():
                if card.number > highest:
                    highest = card.number
                    winner = player
        self.calculate_score(winner, pile)
        print(f'Player {winner + 1} won the hand.')
        print('----------------------------------------------------------------------------')
        return winner
        
    def game_loop(self, winner):
        """
        Main gameplay loop with turns.
        """
        #Starts game with winner starting.
        currentTurn = winner
        self.enumerate_list(currentTurn - 1)
        pile = {}
        startingCardInput = input(f'Player {currentTurn}, please select a card to start the trick: ')
        if startingCardInput != '' or int(startingCardInput) <= len(self.players[currentTurn - 1].get_hand()):
            startingCard = self.players[currentTurn - 1].get_hand()[int(startingCardInput) - 1]
            print('-------------------------------------------------------------------------')
            print(f'Player {currentTurn} played {startingCard}! ')
            print('-------------------------------------------------------------------------')
            card = self.players[currentTurn - 1].get_hand().pop(int(startingCardInput) - 1)
            pile[currentTurn - 1] = card
            if currentTurn == 4:
                currentTurn = 1
            else:
                currentTurn += 1
            turnCount = 1
        else:
            print('Not a valid card')
        
        #Then goes to next player.
        while True:
            self.enumerate_list(currentTurn - 1)
            card = input(f'Player {currentTurn}, please select a card: ')
            if card == '' or int(card) > len(self.players[currentTurn - 1].get_hand()):
                print('----------------------------------------')
                print('Invalid Input, not a card.')
                print('----------------------------------------')
                continue
            if card != '' or int(card) <= len(self.players[currentTurn - 1].get_hand()) or type(int(card) == int):
                hasStartingCardColor = False
                for playerCard in self.players[currentTurn - 1].get_hand():
                    if playerCard.color == startingCard.color:
                        hasStartingCardColor = True
                        break
                card1 = self.players[currentTurn - 1].get_hand()[int(card) - 1]
                if turnCount == 0:
                    startingCard = card1
                if turnCount != 0 and hasStartingCardColor and (card1.color != startingCard.color) and card1.color != 'Rook Bird':
                    print('Pick a card of the same color.')
                    continue
                print('-------------------------------------------------------------------------')
                print(f'Player {currentTurn} played {card1}! ')
                print('-------------------------------------------------------------------------')
                accCard = self.players[currentTurn - 1].get_hand().pop(int(card) - 1)
                pile[currentTurn - 1] = accCard
                currentTurn += 1
                turnCount += 1

                # Once currentTurn is 5, it resets
                if currentTurn == 5:
                    currentTurn = 1
                
                if turnCount == 4:
                    winner = self.check_win(pile)
                    pile = {}
                    turnCount = 0
                    currentTurn = winner + 1
            else:
                print('Not a valid card')
                continue
            
    def restart(self):
        self.player_won = 0
        self.final_bet = 0
        self.players = []
        self.kitty = []
        self.choice = ''
        self.discardPile = []
        self.trump = ''
        self.team1_points = 0 # P1 and P3
        self.team2_points = 0 # P2 and P4
        self.calc_score_count = 0
        self.discardPoints = 0
        self.create_deck()

if __name__ == '__main__':
    game = Rook()
    game.start()
