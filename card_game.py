import random
SUITS = ["Hearts", "Diamonds", "Spades", "Clubs", ]
VALUES = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
          "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

class Card:
    def __init__(self, suite, name, value):
        self.suite = suite
        self.value = value
        self.name = name
        
    def printMe(self):
        return f"{self.name} of {self.suite}"


class Deck:
    def __init__(self):
        self.deck = []
        self.reset()

    def printDeck(self):
        for i in range(0, 52):
            print(f"{self.deck[i].name} of {self.deck[i].suite}")

    def deal(self):
        ran = random.randint(0, (len(self.deck)-1))
        return self.deck.pop(ran)

    def shuffle(self):
        for i in range(0, 10000):
            for j in range(0, len(self.deck)):
                randomI = random.randint(0, (len(self.deck)-1))
                temp = self.deck[j]
                self.deck[j] = self.deck[randomI]
                self.deck[randomI] = temp

    def reset(self):
        self.deck = []
        for i in range(0, 4):
            for j in range(0, 13):
                if VALUES[j] == "Ten" or VALUES[j] == "Jack" or VALUES[j] == "Queen" or VALUES[j] == "King":
                    self.deck.append(Card(SUITS[i], VALUES[j], 10))
                elif VALUES[j] == "Ace":
                    self.deck.append(Card(SUITS[i], VALUES[j], 11))
                else:
                    self.deck.append(Card(SUITS[i], VALUES[j], j + 1))                
        self.shuffle()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.greet()

    def calculateHand(self):
        handValue = 0
        for card in self.hand:
            handValue += card.value
            print("This is the card value", card.value)
        print("Players hand value", handValue)
        return handValue

    def greet(self):
        print(f"Welcome {self.name}! Try not to cry when you lose.")

    def takeCard(self, deck):
        card = deck.deal()
        self.hand.append(card)
        print("You recieved a card.", card.printMe())

    # def discard(self, val):
        # if val <= 5 and val >= 0:
            # return self.hand.remove(val)

    def printHand(self):
        for i in range(0, len(self.hand)):
            print(f"{self.hand[i].name} of {self.hand[i].suite}")

class Dealer:
    def __init__(self):
        self.hand = []
        self.taunt()
        self.deck = Deck()

    def calculateHand(self):
        handValue = 0
        for card in self.hand:
            handValue += card.value
            print("Dealers card value:", card.value)
        print("Dealers hand value:", handValue)
        return handValue

    def taunt(self):
        print(f"Bring it.")

    def dealToSelf(self):
        card = self.deck.deal()
        self.hand.append(card)
        print("The dealer recieved one card", card.printMe())
    
    def printHand(self):
        for i in range(0, len(self.hand)):
            print(f"{self.hand[i].name} of {self.hand[i].suite}")

    def dealToPlayer(self, player):
        player.takeCard(self.deck)
        
    def newRound(self):
        self.deck.reset()

class Game:

    def __init__(self):
        self.isPlaying = False
        self.player = Player(input("Type your name:"))
        self.dealer = Dealer()

    def startRound(self):
        self.dealer.newRound()
        self.dealer.hand = []
        self.player.hand = []
        self.dealer.dealToPlayer(self.player)
        self.dealer.dealToSelf()
        self.dealer.dealToPlayer(self.player)
        self.dealer.dealToSelf()
        if not self.compareBothHands():
            self.endRound()
            return
        self.playerChoice()

# start round, give 2 cards and 2 cards to player
    def compareBothHands(self):
        handValuePlayer = self.player.calculateHand()
        handValueDealer = self.dealer.calculateHand()

        if handValuePlayer == 21 and handValueDealer == 21:
            print("Draw")
            return False
        if handValueDealer == 21:
            print("Dealer wins. Suckaaaaaaaaaaaa")
            return False
        if handValuePlayer == 21:
            print("Well played.... -_-")
            return False
        return True

    def playerChoice(self):
        value = input("Would you like to hit or stay?")
        count = 0
        while value.lower() != "hit" and value.lower() != "stay" and count != 5:
            count += 1
            value = input("You suck at spelling. Please re-take the 1st grade and try again. You must choose to HIT or STAY!")

        if value.lower() == "hit":
            self.dealer.dealToPlayer(self.player)
            playerScore = self.player.calculateHand()
            print(f"Your score is {playerScore}")
            if playerScore > 21:
                print("You suck and you lose")
                self.endRound()
            if playerScore == 21:
                print("You win.") 
            if playerScore < 21:
                self.dealerChoice()           
        if value.lower() == "stay":
            self.dealerChoice()

    def dealerChoice(self):

        self.dealer.dealToSelf()
        dealerScore = self.dealer.calculateHand()
        playerScore = self.player.calculateHand()
        print(f"Your score is {dealerScore}")
        choiceList = ["hit", "stay"]
        choiceGenerator = print(random.choice(choiceList))
        if choiceGenerator == "hit":
            self.dealer.dealToSelf()
        else:
            if dealerScore > 21:
                print("You have bested me, but It wont be so easy next time!")
                self.endRound()
            if dealerScore == 21:
                print("Dealer wins.")
                self.endRound() 
            if dealerScore < 21:
                if dealerScore > playerScore:
                    print("You have been crushed!")
                    self.endRound()
                elif dealerScore < playerScore:
                    print("Player wins. But you still suck.")
                    self.endRound()
                elif dealerScore == playerScore:
                    print("Draw. You don't lose, but you also don't win.")
                    self.endRound()

    def endRound(self):
        count = 0
        playAgain = input("Would you like to play again? Yes or No.")
        while playAgain.lower() != "yes" and playAgain.lower() != "no" and count != 2:
            count += 1
            playAgain = input("Pleeeeeease learn how to spell. And then try again.")
        if playAgain.lower() == "yes":
            self.startRound()
        if playAgain.lower() == "no":
            print("You coward. Lol.")

        # round ends if both player and dealer have chosen to stay, if one of them busts, or if one of them gets 21

game = Game()
game.startRound()

