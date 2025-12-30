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
    
    def remove_cards(self, cards: tuple[str] = []):
        for c in cards:
            if c not in self.shoe:
                raise KeyError(f"Invalid card: {c}")
            if self.shoe[c] == 0:
                raise KeyError(f"No cards left: {c}")
            self.shoe[c] -= 1
    
    def __repr__(self):
        return repr(self.shoe)

class Player:
    def __init__(self, hand=None):
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


    
    def hit(self, card: str = ""):
        if self.bust == True:
            return "Player is bust"



    def __repr__(self):
        return repr(f"Hand: {self.hand}, Bust: {self.bust}")



bob = Player(hand = ["8", "T", "3"])

print(bob.total_val())