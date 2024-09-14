import random
from termcolor import colored

CARD_SYMBOLS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_TYPES = ["♣", "♦", "♥", "♠"]

ace_of_spades = """
.------.
|A     |
|  ♠   |
|     A|
'------'
"""

class Player():
    def __init__(self):
        self.balance = 100 # Let's start with 100 bucks
        self.max_hand = 21
        self.hand = []
        self.hand_value = 0
        self.name = ""

    def deposit_cash(self, player, amount):
        player.balance += int(amount)
        print(colored("New balance: " + str(player.balance), "green"))
        pass

    def place_bet(self):
        try:
            bet = int(input("Place your bet: "))
            print("Bet: " + str(bet))
        except ValueError:
            print("Please enter an integer!")
        return bet

    def double_bet(self, bet):
        bet += bet # Doing addition for better performance? Not sure if *= would be better...
        print("Current bet: " + str(bet))
        return bet

class Dealer():
    def __init__(self):
        self.min_hand = 16
        self.max_hand = 21
        self.hand = []
        self.hand_value = 0
        self.hand_value_visible = 0
        self.winnings = 0
        self.balance = 100 # 100 to have same initial balance as player, just for later statistics maybe

    def generate_deck(self):
        deck = []
        # Create deck with each card symbol and type
        for card in range (len(CARD_SYMBOLS)):
            deck.append(CARD_SYMBOLS[card] + CARD_TYPES[0])
            deck.append(CARD_SYMBOLS[card] + CARD_TYPES[1])
            deck.append(CARD_SYMBOLS[card] + CARD_TYPES[2])
            deck.append(CARD_SYMBOLS[card] + CARD_TYPES[3])
        return deck

    def calculate_hand_value(self, hand):
        hand_value = 0
        num_aces = 0  # Count the number of Aces in the hand
        for card in hand:
            # If image card value is 10
            if ("J" in card or "Q" in card or "K" in card or "10" in card):
                card_value = 10
                hand_value += card_value
            elif ("A" in card[0]):
                num_aces += 1
                card_value = 11
                hand_value += card_value
            else:
                card_value = int(card[0])
                hand_value += card_value

        # Adjust for Aces if necessary
        while hand_value > 21 and num_aces > 0:
            hand_value -= 10  # Change Ace value from 11 to 1
            num_aces -= 1  # Decrement the count of Aces

        return hand_value
        

    # Draw a random card from the deck
    def draw_card(self, deck):
        random_card = random.choice(deck)
        deck.remove(random_card) # Remove the card from the deck population
        return random_card

    def check_split(self, hand):
        split_possible = False
        ace_split = False # If Ace split, player is only allowed to hit once
        if (hand[0][0] == hand[1][0]):
            split_possible = True
        if (hand[0][0] == "A" and hand[1][0] == "A"):
            ace_split = True
        return split_possible, ace_split

    def split_hand(self, hand):
        # TODO
        pass

    def check_for_blackjack(self, player_hand_value):
        blackjack = False
        if (player_hand_value == 21):
            blackjack = True
            #print("BLACKJACK! You Win! 1/1.5")
            # TODO Payouts.... Deal new cards
        return blackjack

    def check_bust(self, hand_value):
        bust = False
        if (hand_value > 21):
            bust = True
        return bust

    def compare_hands(self, dealer_hand_value, player_hand_value):
        winner = ""
        if (dealer_hand_value > player_hand_value and dealer_hand_value <= 21):
            print(colored("Dealer wins! Dealer " + str(dealer_hand_value) + " : " + str(player_hand_value) + " Player", "red"))
            winner = "dealer"
            return winner
        elif (dealer_hand_value == player_hand_value):
            print(colored("Pushy pushsy! Dealer " + str(dealer_hand_value) + " : " + str(player_hand_value) + " Player", "blue"))
            winner = "draw"
            return winner
        elif (player_hand_value > 21):
            print(colored("Dealer wins! Dealer " + str(dealer_hand_value) + " : " + str(player_hand_value) + " Player", "red"))
            winner = "dealer"
            return winner
        elif (dealer_hand_value < player_hand_value and player_hand_value <= 21):
            print(colored("Player wins! Dealer " + str(dealer_hand_value) + " : " + str(player_hand_value) + " Player", "green"))
            winner = "player"
            return winner

    def draw_till_17(self, dealer, deck, dealer_hand_value):
        print("Draw till 17...")
        while (dealer_hand_value < 17): # While hand value is smaller than 17
            dealer.hand.append(dealer.draw_card(deck)) # Draw a card and append it to the dealer object attribute
            dealer_hand_value = dealer.calculate_hand_value(dealer.hand) # Calculate the new dealer hand value 
            print(dealer.hand) 
            print(dealer_hand_value)
        print("Dealer hand value: " + str(dealer_hand_value))
        return dealer.hand, dealer_hand_value

    def calculate_win(self):
        pass

    def payout_wins(self, bet, player, dealer):
        player.balance += bet * 2
        dealer.balance -= bet * 2
        return player.balance, dealer.balance

    def payout_blackjack(self, bet, player, dealer):
        player.balance += bet * 1.5
        dealer.balance -= bet * 1.5
        return player.balance, dealer.balance

    def collect_bets(self, bet, player, dealer):
        player.balance -= bet
        dealer.balance += bet
        return player.balance, dealer.balance

    def print_balances(self, player, dealer):
        print("Player balance: " + str(player.balance))
        print("Dealer balance: " + str(dealer.balance))
        return 0

# Main function
def main():
    print(colored("---- Welcome to the Blackjack table! ----", "cyan"))
    print("-----------------------------------------" + ace_of_spades + "-----------------------------------------")
    dealer = Dealer()
    player = Player()
    print("Initial balance: " + str(player.balance))

    # Was struggling a bit with this constellation and calculating the hand value with it... 
    #dealer.hand_value = dealer.calculate_hand_value(['4♣', 'A♦', '7♣'])

    """
    Add a dictionary with dealer, player, draw as keys and a list for each key with 


    """

    while True:
        # Generate a fresh deck
        deck = dealer.generate_deck()

        # Let player place bet
        #bet = player.place_bet()
        bet = 10
        # Check player balance
        while (player.balance <= 0):
            print(colored("Out of money... Please deposit new cash or leave the table!", "red"))
            cash = input(colored("Enter cash amount or 'q' for quitting: ", "red"))
            if (cash.isdigit()):
                player.deposit_cash(player, cash)
                print(colored("Welcome back!", "green"))
                break
            elif (cash == "q"):
                print(colored("Leaving Table... See you next time!", "blue"))
                quit()
            else:
                print(colored("No money seen... Please try again", "red"))


        # Draw first dealer card (hidden)
        dealer.hand.append(dealer.draw_card(deck))

        # Draw 2 cards for the player
        player.hand.append(dealer.draw_card(deck))
        player.hand.append(dealer.draw_card(deck))
        player.hand_value = dealer.calculate_hand_value(player.hand)
        print("Player hand: " + str(player.hand[0]) + " " + str(player.hand[1]) + " ---- " + str(player.hand_value) + " ---- ")

        # Draw second dealer card (face up)
        dealer.hand.append(dealer.draw_card(deck))
        dealer.hand_value_visible = dealer.calculate_hand_value([dealer.hand[1]]) # Handover the card a list, so the calculation workds
        dealer.hand_value = dealer.calculate_hand_value(dealer.hand)
        print("Dealer hand: XX " + str(dealer.hand[1]) + " ---- " + str(dealer.hand_value_visible) + " ---- ")    
        
        # TODO: Check if player want insurance if dealer has an ace

        double = True # Allow doubling if no hit has happened yet
        split_possible = dealer.check_split(player.hand)[0]
        
        while True:
            if (len(player.hand) == 2): # Check for Blackjack only if 2 cards on players hands
                blackjack = dealer.check_for_blackjack(player.hand_value)
                #blackjack = dealer.check_for_blackjack(21)
            if (blackjack == True):
                print("Blackjack! You win!")
                print(colored("Player wins! Dealer " + str(dealer.hand_value) + " : " + str(player.hand_value) + " Player", "green"))
                dealer.payout_blackjack(bet, player, dealer)
                dealer.print_balances(player, dealer)
                break
            # Ask the player what he wants to do...
            action = input("Hit [h], Split [s], Double [d], Stand [x] or Quit [q]?: ")
            if action not in {"h", "s", "d", "x", "q"}:
                print(colored("Please try again", "red"))
            elif (action == "q"):
                print(colored("Leaving Table... See you next time!", "blue"))
                quit()
            # Hit
            elif (action == "h"):
                double = False # Diasallow doubling the bets
                print("Hit!")
                player.hand.append(dealer.draw_card(deck))
                print(player.hand)
                player.hand_value = dealer.calculate_hand_value(player.hand)
                print("Player hand value: ------------" + str(player.hand_value) + " ------------")
                if (dealer.check_bust(dealer.calculate_hand_value(player.hand))):
                    print("Player busted")
                    print(colored("Dealer wins! Dealer " + str(dealer.hand_value) + " : " + str(player.hand_value) + " Player", "red"))
                    dealer.collect_bets(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                    break

            # Split
            elif (action == "s" and split_possible == False):
                print(colored("Splitting not possible with this hand! Try again...", "red"))

            elif (action == "s" and split_possible == True):
                print(" Do the splitting here....")
                # TODO
            
            # Double
            elif (action == "d" and double == True):
                double = True
                print("Doubling the bets...")
                bet = player.double_bet(bet)
                player.hand.append(dealer.draw_card(deck)) # Only 1 card when doubling bets
                print("Player hand: " + str(player.hand))
                player.hand_value = dealer.calculate_hand_value(player.hand) 
                print("Player hand value: " + str(player.hand_value))
                # Check player bust
                if (dealer.check_bust(player.hand_value) == True):
                    print("Player busted")
                    print(colored("Dealer wins! Dealer " + str(dealer.hand_value) + " : " + str(player.hand_value) + " Player", "red"))
                    dealer.collect_bets(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                    break
                
                # Let dealer draw till 17
                dealer.hand, dealer.hand_value = dealer.draw_till_17(dealer, deck, dealer.hand_value)
                dealer_bust = dealer.check_bust(dealer.hand_value)
                if (dealer_bust == True):
                    print("Dealer busted")
                    print(colored("Player wins! Dealer " + str(dealer.hand_value) + " : " + str(player.hand_value) + " Player", "green"))
                    dealer.payout_wins(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                print("Dealer hand: " + str(dealer.hand))
                winner = dealer.compare_hands(dealer.hand_value, player.hand_value)
                if (winner == "player"):
                    dealer.payout_wins(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                elif (winner == "dealer"):
                    dealer.collect_bets(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                break
            
            elif (action == "x"):
                dealer.hand, dealer.hand_value = dealer.draw_till_17(dealer, deck, dealer.hand_value)
                dealer_bust = dealer.check_bust(dealer.hand_value)
                if (dealer_bust == True):
                    print("Dealer busted")
                    print(colored("Player wins! Dealer " + str(dealer.hand_value) + " : " + str(player.hand_value) + " Player", "green"))
                    dealer.payout_wins(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                print("Dealer hand: " + str(dealer.hand))
                winner = dealer.compare_hands(dealer.hand_value, player.hand_value)
                if (winner == "player"):
                    dealer.payout_wins(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                elif (winner == "dealer"):
                    dealer.collect_bets(bet, player, dealer)
                    dealer.print_balances(player, dealer)
                elif (winner == "draw"):
                    dealer.print_balances(player, dealer)
                break

        dealer.hand = []
        player.hand = []
        winner = ""

        print("--------------------------------------------------------------------------------------------------------")
            



if __name__ == "__main__":
    main()

    '''
    ace_of_spades = """
    .------.
    |A     |
    |  ♠   |
    |     A|
    '------'
    """

    print(ace_of_spades)

    # Define the ranks, suits, and their corresponding symbols
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']
    
    # Generate ASCII art for each card
    cards = []
    for rank in ranks:
        for suit in suits:
            card = f"""
            .------.
            |{rank.ljust(2)}    |
            |  {suit}   |
            |    {rank.rjust(2)}|
            '------'
            """
            cards.append(card)

    # Print each card
    for card in cards:
        print(card)
    '''
