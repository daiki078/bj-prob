"""
TODO
- handling input errors (ex. 1-10 valid)
- starts next round when bust
- dealer should stop when above 17 

"""

def numerical_val(rank: str) -> int:
    if rank == "A":
        return 1
    if rank == "T":
        return 10
    return int(rank)

class Shoe:
    def __init__(self, num_decks: int = 7):
        self.num_decks = num_decks
        self.per_rank = 4 * num_decks  

        self.shoe = {
            "A": self.per_rank, "2": self.per_rank, "3": self.per_rank, "4": self.per_rank,
            "5": self.per_rank, "6": self.per_rank, "7": self.per_rank, "8": self.per_rank,
            "9": self.per_rank,
            "T": 4 * self.per_rank,
        }
    
    def total_cards(self):
        return sum(self.shoe.values())
    
    def remove_cards(self, cards = None):
        if cards is None:
            cards = []
        for c in cards:
            if c not in self.shoe:
                raise KeyError(f"Invalid card: {c}")
            if self.shoe[c] == 0:
                raise KeyError(f"No cards left: {c}")
            self.shoe[c] -= 1
    
    def __repr__(self):
        return repr(self.shoe)

class Human:
    def __init__(self, hand = None):
        if hand is None:
            self.hand = []
        else:
            self.hand = list(hand)
        self.bust = False

    def total_val(self) -> tuple[int, bool]:
        total = 0
        aces = 0

        for c in self.hand:
            total += numerical_val(c)
            if c == "A":
                aces += 1

        best = total
        soft = False

        while aces > 0 and best + 10 <= 21:
            best += 10
            aces -= 1
            soft = True

        return best, soft
    
    def is_bust(self) -> bool:
        best, _=  self.total_val()
        return best > 21
    
    def has_bj(self) -> bool:
        hand = self.hand
        bj = False

        if (hand[0] == "A" and numerical_val(hand[1]) == 10) or (hand[1] == "A" and numerical_val(hand[0]) == 10):
            bj = True

        return bj

    
    def hit(self, card: str = "", shoe: Shoe | None = None) -> bool:
        self.hand.append(card)
        best, _ = self.total_val()

        if shoe is not None:
            shoe.remove_cards(card)

    def __repr__(self):
        return repr(f"Hand: {self.hand}, Bust: {self.bust}")

class Dealer(Human):
    def __init__(self, hand = None):
        super().__init__(hand)

    def should_hit(self) -> bool:
        best, soft = self.total_val()

        if best > 17:
            return False
        elif best == 17 and not soft:
            return False
        else:
            return True


class Game:
    def __init__(self, num_decks = 7):
        self.shoe  = Shoe(num_decks = num_decks)
        self.hand_count = 1
        self.player = Human()
        self.dealer = Dealer()
        self.game_over = False

    def reset_shoe(self, num_decks = 7):
        self.shoe = Shoe(num_decks = num_decks)
        self.hand_count = 1
        print(f"Game Reset with num_decks: {num_decks}")

    def play_round(self):
        #This part sets up the initial hands (one card for dealer and two for player)
        d1 = input(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------\nEnter dealer card: ")
        self.dealer.hit(d1, self.shoe)
        p1 = input(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------\nEnter player card 1: ")
        self.player.hit(p1, self.shoe)
        p2 = input(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------\nEnter player card 2: ")
        self.player.hit(p2, self.shoe)
        print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------")

        #This part handles the blackjack logic
        if self.player.has_bj() and d1 != "A" and d1 != "T":
            print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------\nPlayer has blackjack (win)")
            return
        elif self.player.has_bj() and (d1 == "A" or d1 == "T"):
            d2 = input("Enter dealer card 2: ")
            self.dealer.hit(d2, self.shoe)
            if (d1 == "A" and d2 == "T") or (d1 == "T" and d2 == "A"):
                print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------\nDealer also has blackjack (push)")
                return
            else:
                print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------\nPlayer has blackjack (win)")
                return
            
        #At this point we know the dealer and player doesn't have blackjack, so we continue with the game
        player_card_count = 3
        dealer_card_count = 2
        while not self.player.is_bust() and self.player.total_val()[0] != 21:
            action = input("Enter action (hit, stand): ")
            if action == "stand":
                break
            elif action == "hit":
                p3 = input(f"Enter player card {player_card_count}: ")
                self.player.hit(p3, self.shoe)
                print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------")
                player_card_count += 1
            
        #The while loop above ended so either: player stood or they busted; here we check if they busted or got 21
        if self.player.is_bust():
            print("Player is bust (loss)")
            return
        
        #If the code gets here that means the player didn't bust and are done hitting, so the dealer logic is handled here
        while not self.dealer.is_bust() and self.dealer.should_hit():
            d3 = input(f"Enter dealer card {dealer_card_count}: ")
            self.dealer.hit(d3, self.shoe)
            print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------")
            dealer_card_count += 1

        #At this point either: the dealer busted or is between the range [17,21]; we check who won
        player_total , _ = self.player.total_val()
        dealer_total , _ = self.dealer.total_val()

        if player_total > dealer_total:
            print("Player beats dealer (win)")
        elif player_total < dealer_total:
            print("Player loses to dealer (lose)")
        else:
            print("Push")

        




    

game = Game(num_decks = 7)
game.reset_shoe(num_decks = 7)
game.play_round()