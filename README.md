# Welcome to Rook (v0.5): a trick-taking game made in 1906 by Hasbro.

### NOTE: This program is in an unstable state that lacks error/bounds checking and only utilizes a CLI. Additionaly, the program is not complete as of 1/19/2023.

## Program Comprehension

1s, 2s, 3s, and 4s are taken out of the deck (this iteration of the game does not have them present in the program at all.) Rook Bird Card is added (20 Points), totaling 41 cards. 5, 10, and 14 are worth 5, 10, 10 points respectively. Dealer shuffles, then deals cards one at a time to each player. Each player then has the opprotunity to either "bet" a certain number of points or "pass" their turn, effectively removing thier right to bet again for that betting round. Once final bet is reached, the player who won the bet is then dealt the kitty; which they will then have to discard 5 cards to compensate for the cards being added to match the number of cards of every other player (9). 

Turns are then taken until all four players have played a card, resulting in the program performing extensive logic checking to see who wins that hand. Whomever wins the hand will then start the next hand, and this goes on until each player has no cards in their hand. The program keeps track of the points of each team (Player 1 and Player 3 == Team 1 & Player 2 and Player 4 == Team 2), and whoever has more points wins that game. If the team that won the bet did not fulfill their bet (the amount of points they said they would reach by the end of the game), they are set back that many points on the scoreboard.

## Technologies Used
Python Standard Library

## Install / Run Project
You do not need any external tools or libraries to run Rook.py .

## Known Issues:
When saying no to being ready to play the game in discard(), program does not remove some elements (?)