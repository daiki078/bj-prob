from copy import deepcopy

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
    
    #Returns the total number of cards in Shoe
    def total_cards(self):
        return sum(self.shoe.values())

    #Remove cards from Shoe 
    def remove_cards(self, cards = None):
        if cards is None:
            cards = []
        if isinstance(cards, str):
            cards = [cards]
        for c in cards:
            if c not in self.shoe:
                raise KeyError(f"Invalid card: {c}")
            if self.shoe[c] == 0:
                raise KeyError(f"No cards left: {c}")
            self.shoe[c] -= 1
    
    #Returns the probability of drawing a certain card from Shoe
    def card_p(self, card: str = "") -> float:
        return self.shoe[card] / self.total_cards()
    
    def __repr__(self):
        return repr(self.shoe)

class Human:
    def __init__(self, hand = None):
        if hand is None:
            self.hand = []
        else:
            self.hand = list(hand)
        self.bust = False

    #Resets a human hand
    def reset_hand(self):
        self.hand = []

    #Returns the game value of a hand, and indicates if the hand is soft
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
    
    #Returns True if hand is bust
    def is_bust(self) -> bool:
        best, _=  self.total_val()
        return best > 21
    
    #Returns True if hand is a (two-card) blackjack 
    def has_bj(self) -> bool:
        hand = self.hand
        bj = False

        if (hand[0] == "A" and numerical_val(hand[1]) == 10) or (hand[1] == "A" and numerical_val(hand[0]) == 10):
            bj = True

        return bj

    #Appends a card to hand and also removes from Shoe
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

    #Returns true if dealer should take a card (hits on soft 17)
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

    #Resets game shoe
    def reset_shoe(self, num_decks = 7):
        self.shoe = Shoe(num_decks = num_decks)
        self.hand_count = 1
        print(f"Game Reset with num_decks: {num_decks}")

    #Starts a round of blackjack
    def play_round(self):
        self.dealer.reset_hand()
        self.player.reset_hand()

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
            print("Player is bust (lose)")
            return
        
        #If the code gets here that means the player didn't bust and are done hitting, so the dealer logic is handled here
        while not self.dealer.is_bust() and self.dealer.should_hit():
            d3 = input(f"Enter dealer card {dealer_card_count}: ")
            self.dealer.hit(d3, self.shoe)
            print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {self.dealer.total_val()}\nPlayer: {self.player.hand}, Total: {self.player.total_val()}\n-------")
            dealer_card_count += 1

        if self.dealer.is_bust():
            print("Dealer busts (win)")
            return

        #At this point the dealer is in the range [17,21]; we check who won
        player_total, _ = self.player.total_val()
        dealer_total, _ = self.dealer.total_val()

        if player_total > dealer_total:
            print("Player beats dealer (win)")
        elif player_total < dealer_total:
            print("Player loses to dealer (lose)")
        else:
            print("Push")

    #Runs game multiple times    
    def run(self):
        self.play_round()

        while not self.game_over:
            again = input("Play another hand? [Y/n]: ").strip().lower()
            if again in ("n", "no"):
                self.game_over = True
                break

            self.hand_count += 1
            self.play_round()
    
class EV(Game):
    def __init__(self, num_decks = 7):
        super().__init__(num_decks)

    def dealer_outcome_p(self, dealer: Dealer, shoe: Shoe) -> dict:
        if dealer.is_bust():
            return {"bust": 1}
        if not dealer.should_hit():
            total, _ = dealer.total_val()
            return {total: 1}
        
        outcomes = {}

        for card, count in shoe.shoe.items():
            if count == 0:
                continue
            draw_p = shoe.card_p(card)

            next_dealer = deepcopy(dealer)
            next_shoe = deepcopy(shoe)
            next_dealer.hit(card, next_shoe)

            for outcome, prob in self.dealer_outcome_p(next_dealer, next_shoe).items():
                outcomes[outcome] = outcomes.get(outcome, 0) + draw_p * prob
        return outcomes
    

    def stand_EV(self) -> float:
        player_total, _ = self.player.total_val()
        dealer_summand = 17
        outcomes = self.dealer_outcome_p(self.dealer, self.shoe)
        win_p = outcomes.get("bust", 0)
        tie_p = outcomes.get(player_total, 0)
        
        while dealer_summand < player_total:
            win_p += outcomes.get(dealer_summand, 0)
            dealer_summand += 1
        
        return 2 * win_p + tie_p - 1


game = EV(num_decks = 1)
game.reset_shoe(num_decks = 1)
game.dealer.hit("6")
game.player.hit("T")
game.player.hit("7")

print(game.dealer_outcome_p(game.dealer, game.shoe))
print(game.stand_EV())