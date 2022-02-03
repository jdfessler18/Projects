"""Runs a working, console-based 6-deck Blackjack card game utilizing functions and a class.  The game can be played as many times as the user would like before quitting."""

import random
done_playing = False;
userTotal = 0;
dealerTotal = 0;
cardsdrawn = []
user_card_list = []
dealer_card_list = []
drawphase = True

class Cards:
    #creates a class to store the name, suite,visibility and value of each card
    def __init__(self, number, suite, value, name, visible):  
        #doing modulo 52 to find the position within the deck and then 13 to find the position within the suite
        value = (number % 52) % 13
        if value == 0:
            value = 10
            name = "King"
        elif value == 1:
            value = 11
            name = "Ace"
        elif value == 11:
            value = 10
            name = "Jack"
        elif value == 12:
            value = 10
            name = "Queen"
        else:
            name = str(value)
        #Finds the card's position in its respective deck, which determines suite
        if (number % 52) / 13 <= 1:
            suite = "Clubs"
        elif (number % 52) / 13 > 1 and (number % 52) / 13 <= 2:
            suite = "Diamonds"
        elif (number % 52) / 13 > 2 and (number % 52) / 13 <= 3:
            suite = "Hearts"
        elif (number % 52) / 13 > 3 and (number % 52) / 13 <= 4:
            suite = "Spades"
        #sets the attributes of this card object
        self.suite = suite
        self.value = value
        self.name = name
        self.visible = visible

#randomCard finds a random number between 1 and 312 to represent 6 decks of cards and makes sure the card has not already been drawn
def randomCard():
    drawn = True
    num: int = 0
    #checks to make sure the card has not been previously drawn in this game
    while(drawn):
        i: int = 0
        num = random.randrange(1, 312, 1)
        if len(cardsdrawn) == 0:
            break
        else:
            while i < len(cardsdrawn):
                if cardsdrawn[i] == num:
                    break
                else:
                    if i == len(cardsdrawn) - 1:
                        drawn = False
                    i += 1
    #adds this number to the cards drawn list for future duplicate checks
    cardsdrawn.append(num)            
    return num

#totalPoints loops through a cardlist adding up card values and recording acecount, whose values are factored in after
def totalPoints(cardlist):
    i = 0
    total = 0
    ace_count = 0
    while i < len(cardlist):
        #hidden cards are not counted in point totals
        if cardlist[i].visible == False:
            i+=1
            continue
        else:
            if cardlist[i].name == "Ace":
                ace_count += 1
            else:
                total += cardlist[i].value
            i += 1
    i = 0
    #if the aces can counted as 11 without busting, they are
    while i < ace_count:
        if (total + 11) <= 21:
            total += 11
        else:
            total += 1
        i += 1
    return total
#printCards prints out the cards each user has and each users point totals
def printCards(drawphase):
    i = 0
    print("User cards:", end = ' ')
    #loops through user_card_list printing each card
    while i < len(user_card_list):
        print(user_card_list[i].name + " of " + user_card_list[i].suite, end = '')
        i+=1
        if i < len(user_card_list):
            print(" and", end = ' ')
    i = 0
    #if in the drawphase, prints Hidden for the first dealer card and then prints the rest of the dealer cards normally
    if drawphase == True:
        i = 1
        print("\nDealer cards: Hidden and", end = ' ')
        while i < len(dealer_card_list):
            print(dealer_card_list[i].name + " of " + dealer_card_list[i].suite)
            i+=1
            if i < len(dealer_card_list):
                print(" and", end = ' ')
    #if not in the drawphase, sets the first dealer card to visible and prints every card
    else:    
        print("\nDealer cards:", end = ' ')
        dealer_card_list[0].visible = True
        while i < len(dealer_card_list):
            print(dealer_card_list[i].name + " of " + dealer_card_list[i].suite, end = '')
            i+=1
            if i < len(dealer_card_list):
                print(" and", end = ' ')
            else:
                print(" ")
    print("User total points: " + str(totalPoints(user_card_list)) + "\nDealer total points: " + str(totalPoints(dealer_card_list)))

print("Welcome to Jacob's Blackjack!")
#this loop allows the game to go on while the user wants to play
while done_playing == False:
    print("New game:\nDealing Cards...")
    x = 0
    #adds first 2 user cards and dealer cards to their card lists
    while x < 2:
        user_card_list.append(Cards(randomCard(), " ", 0, " ", True))
        if x == 0:
            dealer_card_list.append(Cards(randomCard(), " ", 0, " ", False))
        else:
            dealer_card_list.append(Cards(randomCard(), " ", 0, " ", True)) 
        x+=1
    #This loop either concludes the game based off of point totals or gives the user the option to hit or stand
    while drawphase == True:
        if totalPoints(user_card_list) > 21:
            drawphase = False
            printCards(drawphase)
            print("You bust, dealer wins!")
        elif totalPoints(user_card_list) == 21:
            dealer_card_list[0].visible = True
            printCards(drawphase)
            if totalPoints(dealer_card_list) == 21:
                print("Wow, you both got 21! Push!")
            else:
                if len(user_card_list) == 2:
                    print("Blackjack! You win!")
                else:
                    print("You win!")
            drawphase = False
        else:
            printCards(drawphase)
            hs = input("Would you like to hit or stand? (Hit/Stand) ")
            if hs == "Hit":
                user_card_list.append(Cards(randomCard(), " ", 0, " ", True))
            elif hs == "Stand":
                dealer_card_list[0].visible = True
                dealerTotal = totalPoints(dealer_card_list)
                #if the dealers point total is less than 17, the dealer draws a card
                while drawphase == True:     
                    if totalPoints(dealer_card_list) < 17:
                        dealer_card_list.append(Cards(randomCard(), " ", 0, " ", True))
                    else:
                        drawphase = False
                printCards(drawphase)
                dealerTotal = totalPoints(dealer_card_list)
                userTotal = totalPoints(user_card_list)
                #user and dealer win conditions
                if userTotal > dealerTotal:
                    print("You win!")
                elif userTotal == dealerTotal:
                    print("Push!")
                elif dealerTotal > 21:
                    print("You win!")
                else:
                    print("Dealer wins!")
    #Gets input from the user if they want to play the game again
    yn = input("Would you like to play again? (Y/N) ")
    #if they say "N", ends the code
    if yn == "N":
        done_playing = True
    #if they say "Y", resets card lists, totals, cards drawn and draw phase
    elif yn == "Y":
        userTotal = 0;
        dealerTotal = 0;
        cardsdrawn = []
        user_card_list = []
        dealer_card_list = []
        drawphase = True


    
