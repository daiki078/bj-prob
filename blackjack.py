from enum import Enum, IntEnum

class Suit(Enum):
    SPADE = "♠"
    HEART = "♥"
    DIAMOND = "♦"
    CLUB = "♣"


class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def points(self) -> int:
        """Blackjack-style points (faces count as 10)."""
        if self in (Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING):
            return 10
        return int(self)
    
    @property
    def label(self) -> str:
        return {
            Rank.ACE: "A",
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
        }[self]


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank.label}{self.suit.value}"


class Deck:
    def __init__(self):
        self.deck = []
        for suit in Suit:
            for rank in Rank:
                self.deck.append(Card(suit, rank))

    def __repr__(self):
        cards = " ".join(map(str, self.deck))
        return f"Deck({len(self.deck)} cards): [{cards}]"


class Shoe:
    def __init__(self, num_decks: int = 7):
        self.num_decks = num_decks
        self.shoe = [Deck() for _ in range(self.num_decks)]
        self.cards = []

        for deck in self.shoe:
            self.cards.extend(deck.deck)

    def __repr__(self):
        total_cards = sum(len(deck.deck) for deck in self.shoe)
        return f"Shoe(num_decks={self.num_decks}, total_cards={total_cards})"
    
    


SHOE = Shoe(num_decks = 1)
print(SHOE.cards)
