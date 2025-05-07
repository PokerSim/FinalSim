import pokerkit as pk
import itertools

#global variables
chip_count = 0
#Hand is a list of tuples, where each tuple is a card in the format (rank, suit)
# Example: hand = [('A', 'H'), ('K', 'D')] represents Ace of Hearts and King of Diamonds
hand = []
hand_type_stengths= {
    "high_card": 0,
    "one_pair": 1,
    "two_pair": 2,
    "three_of_a_kind": 3,
    "straight": 4,
    "flush": 5,
    "full_house": 6,
    "four_of_a_kind": 7,
    "straight_flush": 8,
    "royal_flush": 9
}
oddsLine = 0.3

#determine the next action to take
# vars needed: current_bet, community_cards, hand, chip_count, num_players, position
def take_action(current_bet, community_cards):
    result = ""
    if result == "R": return "raise"
    elif result == "C": return "call"
    elif result == "F": return "fold"
    else: return "fold"

#determine what to do postflop
def postflop_action(numPlayers, playerIndex, current_bet, community_cards, pot_size):
    global hand, chip_count
    
    # Get current hand
    current_hand_strength, current_hand_cards = get_current_best_hand(hand, community_cards)
    if current_hand_strength >= 7:   # If the hand is quads or better, all in
        return "R"

    # get the number of outs for each hand type
    outs = get_outs(hand, community_cards)

    # Calculate total number of outs that can improve the hand
    outs_total = 0
    for out_type, count in outs.items():
        if hand_type_stengths[out_type] > current_hand_strength:
            outs_total += count

    outs_odds = 0
    if (community_cards.count() == 3): # On the flop
        outs_odds = outs_total / 47
    elif (community_cards.count() == 4): # On the turn
        outs_odds = outs_total / 46
    
    # Strategy
    if current_bet == 0: # If there is no cost to call, always call or raise
        if current_hand_strength >= 4:
            return "R"
        elif current_hand_strength >= 2:
            return "R"
        else:
            return "C"
    if current_hand_strength >= 4: # If the current hand is a straight or better
        return "C"
    elif current_hand_strength >= 2: # If the current hand is a two pair or better
        if outs_odds >= oddsLine:
            return "C"
        else:
            return "F"
    elif current_hand_strength >= 0: # If the current hand is a one pair or high card
        for out_type, count in outs.items():
            if hand_type_stengths[out_type] >= 4:
                if outs_odds >= oddsLine and count > 0:
                    return "C"
                else:
                    return "F"
    else:
        return "F"
    
#determine what to do preflop
def preflop_action(numPlayers, playerIndex, been_raised, are_limpers):
    column = determine_position(numPlayers, playerIndex)
    if been_raised(): column += 6
    if are_limpers(): column += 3

    rows = {"AAo": 0, "KKo": 0, "QQo": 0, 
            "JJo": 1,
            "TTo": 2,
            "99o": 3, "88o": 3, "77o": 3,
            "66o": 4, "55o": 4, "44o": 4, "33o": 4, "22o": 4,
            "AKo": 5, "AKs": 5,
            "AQo": 6, "AQs": 6,
            "AJo": 7, "AJs": 7, "ATs": 7, "KQo": 7, "KJo": 7, "KQs": 7, "KJs": 7, "QJs": 7, "JTs": 7,
            "ATo": 8, "KTs": 8,
            "A9s": 9, "A8s": 9, "KTo": 9, "K9s": 9, "QJo": 9, "QTo": 9, "QTs": 9, "J9s": 9, "T9s": 9, "98s": 9,
            "A9o": 10, "A8o": 10, "A7s": 10, "A6s": 10, "A5s": 10, "A4s": 10, "A3s": 10, "A2s": 10, "K9o": 10, "Q9s": 10, "JTo": 10, "J8s": 10, "T9o": 10, "T8s": 10, "98o": 10, "97s": 10, "87s": 10, "86s": 10, "76s": 10, "65s": 10,
            "A7o": 11, "A6o": 11, "A5o": 11, "A4o": 11, "A3o": 11, "A2o": 11, "K8s": 11, "Q9o": 11, "Q8s": 11, "J9o": 11, "J8o": 11, "J7s": 11, "T8o": 11, "T7s": 11, "T6s": 11, "97o": 11, "96s": 11, "87o": 11, "75s": 11, "54s": 12}

    if hand[0][1] == hand[1][1]:
        hand_str = hand[0][0] + hand[1][0] + "s"
    else:
        hand_str = hand[0][0] + hand[1][0] + "o"
    row = rows.get(hand_str, None)
    if row is None:
        return "fold"

    solutions = [
        ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'C', 'C', 'R'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'C', 'C', 'C'],
        ['R', 'R', 'R', 'C', 'R', 'R', 'C', 'C', 'C'],
        ['R', 'R', 'R', 'C', 'C', 'C', 'C', 'C', 'C'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'C', 'R', 'R'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'C', 'C', 'R'],
        ['F', 'R', 'R', 'R', 'R', 'R', 'F', 'C', 'C'],
        ['F', 'R', 'R', 'R', 'R', 'R', 'F', 'F', 'C'],
        ['F', 'F', 'R', 'F', 'R', 'R', 'F', 'F', 'F'],
        ['F', 'F', 'R', 'F', 'F', 'F', 'F', 'F', 'F']]

    return solutions[row][column]

# determine position
# 0 == early, 1 == mid, 2 == late, -1 == invalid
def determine_position(numPlayers, playerIndex):
    if (playerIndex == 0 & numPlayers != 2):
        return 2
    #switch case for numPlayers
    match numPlayers:
        case 2:
            return 2
        case 3:
            if playerIndex == 1: return 2
            elif playerIndex == 2: return 1
            else: return -1
        case 4:
            if playerIndex == 1: return 1
            elif playerIndex == 2 | playerIndex == 3: return 0
            else: return -1
        case 5:
            if playerIndex >= 1 & playerIndex <= 3: return 0
            elif playerIndex == 4: return 1
            else: return -1
        case 6:
            if playerIndex >= 1 & playerIndex <= 3: return 0
            elif playerIndex == 4: return 1
            elif playerIndex == 5: return 2
            else: return -1
        case 7:
            if playerIndex >= 1 & playerIndex <= 3: return 0
            elif playerIndex == 4 | playerIndex == 5: return 1
            elif playerIndex == 6: return 2
            else: return -1
        case 8:
            if playerIndex >= 1 & playerIndex <= 4: return 0
            elif playerIndex == 5 | playerIndex == 6: return 1
            elif playerIndex == 7: return 2
            else: return -1
        case 9:
            if playerIndex >= 1 & playerIndex <= 4: return 0
            elif playerIndex == 5 | playerIndex == 6: return 1
            elif playerIndex == 7 | playerIndex == 8: return 2
            else: return -1
        case 10:
            if playerIndex >= 1 & playerIndex <= 5: return 0
            elif playerIndex == 6 | playerIndex == 7: return 1
            elif playerIndex == 8 | playerIndex == 9: return 2
            else: return -1
        case _:
            return "invalid"
        
#determine the current best hand
def get_current_best_hand(hand, community_cards):
    all_cards = hand + community_cards
    # order all_cards by rank
    all_cards = sorted(all_cards, key=lambda x: x[0])

    # get all possible hands
    possible_hands = list(itertools.combinations(all_cards, 5))

    # get the best hand from all possible hands
    for five_cards in possible_hands:
        best_hand, high_card_values  = get_best_hand(five_cards)
    return best_hand, high_card_values

#Evaluate the best 5-card hand from a given set of cards (hole + community).
#Returns a tuple (hand_rank, high_card_values) where:
#    - hand_rank: Integer representing the hand type (e.g., 9 = royal flush, 8 = straight flush, etc.).
#    - high_card_values: List of card values for tie-breaking.
def get_best_hand(cards):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    ranks = sorted([values[card[:-1]] for card in cards], reverse=True)
    suits = [card[-1] for card in cards]

    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    suit_counts = {suit: suits.count(suit) for suit in set(suits)}

    # Helper functions
    def is_flush():
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
        if flush_suit:
            flush_cards = [card for card in cards if card[-1] == flush_suit]
            return True, sorted([values[card[:-1]] for card in flush_cards], reverse=True)
        return False, None

    def is_straight():
        sorted_ranks = sorted(set(ranks), reverse=True)
        if sorted_ranks == [14, 5, 4, 3, 2]:    # Special case for Ace-low straight
            return True, sorted_ranks
        if len(sorted_ranks) == 5 and sorted_ranks[0] - sorted_ranks[-1] == 4:
            return True, sorted_ranks
        return False, None

    # Check for poker hands
    flush, flush_cards = is_flush()
    straight, high_straight_cards = is_straight()

    if flush and straight:
        # Check if it's a Royal Flush
        if set([14, 13, 12, 11, 10]).issubset(flush_cards):
            return 9, [14]  # Royal Flush (highest card is Ace)
        return 8, high_straight_cards  # Straight Flush
    if flush:
        return 5, flush_cards[:5]  # Flush (highest 5 cards)
    if straight:
        return 4, high_straight_cards  # Straight

    rank_count_list = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))
    most_common = rank_count_list[0]

    if most_common[1] == 4:
        return 7, [most_common[0]] + [rank for rank in ranks if rank != most_common[0]]  # Four of a kind
    if most_common[1] == 3:
        second_common = rank_count_list[1]
        if second_common[1] >= 2:
            return 6, [most_common[0], second_common[0]]  # Full house
        return 3, [most_common[0]] + [rank for rank in ranks if rank != most_common[0]]  # Three of a kind
    if most_common[1] == 2:
        second_pair = rank_count_list[1]
        if second_pair[1] == 2:
            return 2, [most_common[0], second_pair[0]] + [rank for rank in ranks if rank not in (most_common[0], second_pair[0])]  # Two pair
        return 1, [most_common[0]] + [rank for rank in ranks if rank != most_common[0]]  # One pair

    return 0, ranks[:5]  # High card (highest 5 cards)

def get_outs(hand, community_cards):
    all_cards = hand + community_cards
    # order all_cards by rank
    all_cards = sorted(all_cards, key=lambda x: x[0])

    # get all four card combinations
    # This is a brute force approach, but it will work for now.
    four_card_combinations = list(itertools.combinations(all_cards, 4))

    # get the number of outs for each hand type
    outs = {
        "royal_flush": 0,
        "straight_flush": 0,
        "four_of_a_kind": 0,
        "full_house": 0,
        "flush": 0,
        "straight": 0,
        "three_of_a_kind": 0,
        "two_pair": 0,
        "one_pair": 0,
    }

    # set to keep track of already checked hands
    # This is to avoid double counting hands that are already checked
    already_checked = {
        "royal_flush": set(),
        "straight_flush": set(),
        "four_of_a_kind": set(),
        "full_house": set(),
        "flush": set(),
        "straight": set(),
        "three_of_a_kind": set(),
        "two_pair": set(),
        "one_pair": set(),
    }

    for four_cards in four_card_combinations:
        update_outs(outs, already_checked, four_cards)

    return outs

# Outs is a dictionary of sets, where each key is a hand type and the value is a set of ranks
def update_outs(outs, already_checked, cards):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    ranks = sorted([values[card[:-1]] for card in cards], reverse=True)
    suits = [card[-1] for card in cards]

    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    suit_counts = {suit: suits.count(suit) for suit in set(suits)}

    # Helper functions
    def is_suited(cards):
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 4:
                return True
        return False
    
    def open_ended_straight(ranks):
        sorted_ranks = sorted(set(ranks), reverse=True)
        # special case for possible end straights (low end handeled by calculations)
        if sorted_ranks == [14, 13, 12, 11]:
            return False, None
        elif len(sorted_ranks) == 4 and sorted_ranks[0] - sorted_ranks[-1] == 3:
            return True
        return False
    
    def gutshot_straight(ranks):
        sorted_ranks = sorted(set(ranks), reverse=True)
        # special case for possible end straights
        if sorted_ranks == [14, 13, 12, 11] or sorted_ranks == [14, 5, 4, 3] or sorted_ranks == [14, 5, 4, 2] or sorted_ranks == [14, 5, 3, 2]  or sorted_ranks == [14, 4, 3, 2]:
            return True
        elif len(sorted_ranks) == 4 and sorted_ranks[0] - sorted_ranks[-1] == 4:
            return True
        return False
    
    # Possibly a royal flush or straight flush
    if is_suited(cards) and gutshot_straight(ranks):
        if ranks not in already_checked["straight_flush"]:
            outs["straight_flush"] += 1
            already_checked["straight_flush"].add(tuple(ranks))
        if (ranks == [14, 13, 12, 11] or ranks == [14, 13, 12, 10] or ranks == [14, 13, 11, 10] or ranks == [14, 12, 11, 10]) and ranks not in already_checked["royal_flush"]:
            outs["royal_flush"] += 1
            already_checked["royal_flush"].add(tuple(ranks))
    if is_suited(cards) and open_ended_straight(ranks):
        if ranks not in already_checked["straight_flush"]:
            outs["straight_flush"] += 2
            already_checked["straight_flush"].add(tuple(ranks))
        if ranks == [13, 12, 11, 10] and ranks not in already_checked["royal_flush"]:
            outs["royal_flush"] += 1
            already_checked["royal_flush"].add(tuple(ranks))
    # Possibly four of a kind 
    for rank, count in rank_counts.items():
        if count == 3:
            three_of_a_kind = (rank, rank, rank)
            if three_of_a_kind not in already_checked["four_of_a_kind"]:
                outs["four_of_a_kind"] += 1
                already_checked["four_of_a_kind"].add(three_of_a_kind)
    # Possibly a full house (already have 3 of a kind)
    if 3 in rank_counts.values() and ranks not in already_checked["full_house"]:
        outs["full_house"] += 3
        already_checked["full_house"].add(tuple(ranks))
    #possibly a full house(already have 2 pair)
    if list(rank_counts.values()).count(2) == 2 and ranks not in already_checked["full_house"]:
        outs["full_house"] += 4
        already_checked["full_house"].add(tuple(ranks))
    # Possibly a flush
    if is_suited(cards) and ranks not in already_checked["flush"]:
        outs["flush"] += 9
        already_checked["flush"].add(tuple(ranks))
    # Possibly a straight
    if open_ended_straight(ranks) and ranks not in already_checked["straight"]:
        outs["straight"] += 8
        already_checked["straight"].add(tuple(ranks))
    if gutshot_straight(ranks) and ranks not in already_checked["straight"]:
        outs["straight"] += 4
        already_checked["straight"].add(tuple(ranks))
    # Possibly three of a kind or two pair
    for rank, count in rank_counts.items():
        if count == 2:
            two_pair = (rank, rank)
            if two_pair not in already_checked["three_of_a_kind"]:
                outs["three_of_a_kind"] += 2
                already_checked["three_of_a_kind"].add(two_pair)
            for other_rank in ranks:
                if other_rank != rank and (rank, rank, other_rank) not in already_checked["two_pair"]:
                    outs["two_pair"] += 3
                    already_checked["two_pair"].add((rank, rank, other_rank))
    # Possibly a pair
    # if rank_counts.values()  only has 1s, then there are no pairs
    if len(rank_counts.values()) == 4:
        for rank in ranks:
            if rank not in already_checked["one_pair"]:
                outs["one_pair"] += 3
                already_checked["one_pair"].add(rank)

    return

#recieve card 
def recieve_card(card):
    hand.append(card)

#add chips to the player's stack
def add_chips(chips):
    global chip_count
    chip_count += chips

#reset the player's chip count
def reset_chips():
    global chip_count
    chip_count = 0
