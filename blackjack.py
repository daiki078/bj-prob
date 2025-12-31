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

        self.bust = best > 21
        return best, soft

    
    def hit(self, card: str = "", shoe: Shoe | None = None) -> bool:
        self.hand.append(card)
        best, _ = self.total_val()

        if self.bust == True:
            raise ValueError("Player is bust")
        elif self.total_val()[0] >= 21:
            raise ValueError("Player has 21")
        
        if shoe is not None:
            shoe.remove_cards(card)

        can_continue = not self.bust or best == 21
        return can_continue

        
    def __repr__(self):
        return repr(f"Hand: {self.hand}, Bust: {self.bust}")

# class Player(Human):
#     pass

# class Dealer(Human):
#     def __init__(self, hand=None):
#         super().__init__(hand)

#     def is_stand():
#         best, soft = self.total_val()
#         if best > 17:
#             # stand
#             pass
#         elif not soft and best == 17:
#             # stand
#             pass
#         else:
#             # hit
#             pass

class Game:
    def __init__(self, num_decks = 7):
        self.shoe  = Shoe(num_decks = num_decks)
        self.hand_count = 1
        self.player = Human()
        self.dealer = Human()
        self.game_over = False

    def reset_shoe(self, num_decks = 7):
        self.shoe = Shoe(num_decks = num_decks)
        self.hand_count = 0
        print(f"Game Reset with num_decks: {num_decks}")
    
    # play one round of the game
    def play_round(self):
        while True:
            try:
                dealer_total = self.dealer.total_val()
                player_total = self.player.total_val()
                d1 = input(f"------\nHand Number {self.hand_count}\nDealer: ?, Total: {dealer_total}\nPlayer: ??, Total: {player_total}\n -------\nEnter dealer card: ")
                
                self.dealer.hit(d1)
            except Exception as e:
                print(e)

            try:
                dealer_total = self.dealer.total_val()
                player_total = self.player.total_val()
                p1 = input(f"-------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {dealer_total}\nPlayer: ??, Total: {self.player.hand}\n-----\nEnter Player upcard 1: ")
                self.player.hit(p1)
            except Exception as e:
                print(e)

            try:
                dealer_total = self.dealer.total_val()
                player_total = self.player.total_val()
                p2 = input(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {dealer_total}\nPlayer: {self.player.hand}, Total: {player_total}\n------\nEnter Player upcard 2: ")
                self.player.hit(p2)
                player_total = self.player.total_val()
                print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {dealer_total}\nPlayer: {self.player.hand}, Total: {player_total}\n------")
                self.hand_count += 1
            except Exception as e:
                print(e)

            self.player_hitting = True
            while self.player_hitting:
                try:
                    action = input(f"Enter action (stand, hit): ")
                    if action == "stand":
                        self.player_hitting = False
                    elif action == "hit":
                        hit_card = input("Enter new player card: ")
                        can_continue = self.player.hit(hit_card)
                        if not can_continue:
                            self.player_hitting = False

                        player_total = self.player.total_val()
                        print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {dealer_total}\nPlayer: {self.player.hand}, Total: {player_total}\n------")
                except Exception as e:
                    print(e)
            
            self.dealer_hitting = True
            while self.dealer_hitting:
                dealer_card = input("Enter new dealer card: ")
                try:
                    self.dealer.hit(dealer_card)
                    dealer_total = self.dealer.total_val()
                    self.dealer_hitting = dealer_total[0] <= 17 or dealer_total[1] == True
                    print(f"------\nHand Number {self.hand_count}\nDealer: {self.dealer.hand}, Total: {dealer_total}\nPlayer: {self.player.hand}, Total: {player_total}\n------")
                except Exception as e:
                    print(e)

            return
    
    # def run():
    #     while not self.game_over:
    #         self.play_round()
    #         game_over = input("play another hand? [Y/n]")
    #         self.game_over = game_over

game = Game(num_decks = 7)
game.reset_shoe(num_decks = 7)
game.play_round()