import pokerkit as pk
import itertools

#global variables
chip_count = 0

#determine the next action to take
def take_action(current_bet, community_cards):
    #Go all in
    global chip_count
    raise_amount = chip_count
    chip_count = 0
    return "raise" + raise_amount

#add chips to the player's stack
def add_chips(chips):
    global chip_count
    chip_count += chips

#reset the player's chip count
def reset_chips():
    global chip_count
    chip_count = 0
