import random


class Deck:

    
    deck = []
    index = 0
    
    def making_deck(self):
        
        suits = ["H", "C", "D", "S"]
        figures = ["J", "Q", "K", "A"]
        option = 0
        while option < 6:
            for x in suits:
                for i in range(2,11):
                    self.deck.append(str(i) + x)
                for i in figures:
                    self.deck.append(i + x)
            option += 1

    def shuffle(self):
        return random.shuffle(self.deck)

    def next_card(self):
        self.index += 1
        return self.index

shoe = Deck()
shoe.making_deck()
shoe.shuffle()
shoe.deck[0] = "Q"
shoe.deck[1] = "A"
shoe.deck[2] = "Q"
shoe.deck[3] = "K"


class Hand:


    cards = {}
    
    def draw_card(self):
        
        if shoe.deck[shoe.index][0] in "1JQK":
            self.cards[shoe.deck[shoe.index]] = 10
        elif shoe.deck[shoe.index][0] == "A":
            if sum(self.cards.values()) < 11:
                self.cards[shoe.deck[shoe.index]] = 11
            else:
                self.cards[shoe.deck[shoe.index]] = 1
        else:
            self.cards[shoe.deck[shoe.index]] = int(shoe.deck[shoe.index][0])
        if sum(self.cards.values()) > 21:
            for k, v in self.cards.items():
                if v == 11:
                    self.cards[k] = 1
        shoe.next_card()

              
class Dealer(Hand):


    cards = {}
    
    def turn(self):
        
        while sum(self.cards.values()) < 17:
            self.draw_card()
        print(list(self.cards))


class Player(Hand):


    wallet = 0
    cards = {}
    bet = 0.0
    decision = ""
    scores = []
    
    def ante(self):
        
        while True:
            try:
                self.bet = int(input("Place your bet: "))
                if 10 <= self.bet <= 300:
                    self.wallet -= self.bet
                    break
                print("Ante must be between 10-300")
            except ValueError:
                print("Invalid number")
        

    def turn(self):
        
        while True:
            if sum(self.cards.values()) < 21:
                print('''Options:
Hit - Pass - Surrender - Double - Split''')
                self.decision = input()
                if self.decision.upper() == "HIT":
                    self.draw_card()
                    print(list(self.cards))
                elif self.decision.upper() == "SURRENDER":
                    if len(self.cards) == 2 and len(self.scores) < 1:
                        self.wallet += self.bet * 0.5
                        break
                    else:
                        print("You cant surrender")
                        continue
                elif self.decision.upper() == "DOUBLE":
                    if len(self.cards) == 2:
                        self.wallet -= self.bet
                        self.draw_card()
                        print(list(self.cards))
                        break
                    else:
                        print("You cant double")
                        continue
                elif self.decision.upper() == "PASS":
                    break
                elif self.decision.upper() == "SPLIT":
                    if self.cards[list(self.cards.keys())[0]] == self.cards[list(self.cards.keys())[1]]:
                        split = Player()
                        self.wallet -= self.bet
                        split.cards = self.cards.copy()
                        del self.cards[list(self.cards.keys())[1]]
                        del split.cards[list(split.cards.keys())[0]]
                        print (list(self.cards), "\n", list(split.cards))
                        self.draw_card()
                        print(list(self.cards))
                        self.turn()
                        split.draw_card()
                        print(list(split.cards))
                        split.turn()
                        self.scores.append(sum(split.cards.values()))
                        break
                        
                    else:
                        print("You cant split")
                        continue
                else:
                    print("Incorrect choice, try again\n")
                    continue
            elif 11 in self.cards.values():
                if self.decision.upper() == "HIT":
                    self.draw_card()
                    print(list(self.cards))
                else:
                    break
            else:
                break
            
def result(box1, dealer, score, choice):
    #payout and prints result
        if score > 21:
            print ("Lose")
        else:
            dealer.turn()
            if sum(dealer.cards.values()) > 21:
                print("Win")
                box1.wallet += box1.bet * 2
                if box1.decision.upper() == "DOUBLE":
                    box1.wallet += box1.bet * 2
            elif score == sum(dealer.cards.values()):
                print("Push")
                box1.wallet += box1.bet
                if box1.decision.upper() == "DOUBLE":
                    box1.wallet += box1.bet
            elif sum(dealer.cards.values()) > score:
                print ("Lose")
            elif sum(dealer.cards.values()) < score:
                print ("Win")
                box1.wallet += box1.bet * 2
                if box1.decision.upper() == "DOUBLE":
                    box1.wallet += box1.bet * 2
        if choice:
            print("Insurance lost")

def blackjack(box1, dealer):

    if sum(box1.cards.values()) == 21 and sum(dealer.cards.values()) < 10:
        print( "BlackJack!")
        box1.wallet += box1.bet * 2.5
        return True
    elif sum(box1.cards.values()) == 21 and sum(dealer.cards.values()) == 10:
        dealer.draw_card()
        print(list(dealer.cards))
        if sum(dealer.cards.values()) == 21:
            print("Push")
            box1.wallet += box1.bet
        else:
            print("BlackJack!")
            box1.wallet += box1.bet * 2.5
        return True
    elif sum(box1.cards.values()) == 21 and sum(dealer.cards.values()) == 11:
        print("Even money?[y/n]")
        while True:
            even = input().upper()
            if even == "Y":
                box1.wallet += box1.bet * 2
                break
            elif even == "N":
                dealer.draw_card()
                print(list(dealer.cards))
                if sum(dealer.cards.values()) == 21:
                    print("Push")
                    box1.wallet += box1.bet
                    break
                else:
                    print("BlackJack!")
                    box1.wallet += box1.bet * 2.5
                    break
            else:
                print("Incorrect choice")
        return True

def insurance():
    pass

dealer = Dealer()
box1 = Player()
choice = 0
while True:
    print("Wallet: ", box1.wallet)
    box1.ante()
    box1.cards.clear()
    dealer.cards.clear()
    box1.scores.clear()
    box1.draw_card()
    dealer.draw_card()
    box1.draw_card()
    print(list(dealer.cards.keys()), "\n", list(box1.cards.keys()))
    #evaluate result of dealer and player and makes their turn
    bj = blackjack(box1, dealer)
    if bj:
        continue
    if sum(dealer.cards.values()) == 11 and not bj:
        print("Insurance?")
        while True:
            insurance = input().upper()
            if insurance == "Y":
                while True:
                    try:
                        print("How much you want to bet?")
                        choice = int(input())
                        if (box1.bet/2) <= box1.bet <= 10:
                            box1.wallet -= choice
                            break
                        elif choice <= (box1.bet/2) and choice >= 10:
                            box1.wallet -= choice
                            break
                        print("Insurance must be between 10 and half of bet")
                    except ValueError:
                        print("Invalid number")
                break
            elif insurance == "N":
                break
            else:
                print("Incorrect choice")
        
    box1.turn()
    box1.scores.append(sum(box1.cards.values()))
    if box1.decision.upper() == "SURRENDER":
        continue
    else:
        dealer.draw_card()
        if sum(dealer.cards.values()) == 21:
            print(list(dealer.cards))
            print("BlackJack... Lose")
            if choice:
                print("Insurance wins")
                box1.wallet += choice * 3
        else:
            for i in box1.scores:
                result(box1, dealer, i, choice)
        
