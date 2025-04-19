import random

#creating decks 
def create_deck():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    cards = [(rank, suit, i + 2) for i, rank in enumerate(ranks) for suit in suits]
    cards += [("Joker", "1", 15), ("Joker", "2", 15)]
    return cards

def format_card(card):
    return f"{card[0]}{card[1]}"

#shuffling players deck before start to play
def deal(deck):
    random.shuffle(deck)
    return deck[:27], deck[27:]

def total_cards(active, won):
    return len(active) + len(won)

#war handling
def war(human, pile1, computer, pile2, pot, log, round_num, war_depth):
    war_depth += 1
    log.append(f"{round_num:02d} WAR begins")

#decide whether war can continue or not     
    while True:
        if len(human) < 4:
            log.append("    Human can't continue war. Computer gets everything")
            pile2 += pot + human
            human.clear()
            return "Computer", war_depth, True
        if len(computer) < 4:
            log.append("    Computer can't continue war. Human gets everything")
            pile1 += pot + computer
            computer.clear()
            return "Human", war_depth, True

#continueing the war
        p1_down = [human.pop(0) for _ in range(3)]
        p2_down = [computer.pop(0) for _ in range(3)]
        pot += p1_down + p2_down
        log.append("    Both sides place 3 cards face down")

        p1_card = human.pop(0)
        p2_card = computer.pop(0)
        pot += [p1_card, p2_card]

        log.append(f"    Reveal : {format_card(p1_card)} vs {format_card(p2_card)}")

#decide who wins the war or its going to a tie
        if p1_card[2] > p2_card[2]:
            pile1 += pot
            pot.clear()
            log.append("    Human wins the war")
            return "Human", war_depth, False
        elif p2_card[2] > p1_card[2]:
            pile2 += pot
            pot.clear()
            log.append("    Computer wins the war")
            return "Computer", war_depth, False
        else:
            log.append("    Another tie War continues ")

#normal game playing
def play_rounds(active1, active2, game_num):
    log = [f" = = =  Game  {game_num}  = = =  \n##.Human vs Computer \n"]
    won1, won2 = [], []
    war_count = 0
    round_num = 0

    while active1 and active2:
        round_num += 1
        c1, c2 = active1.pop(0), active2.pop(0)
        pot = [c1, c2]
        log.append(f"{round_num:02d}. {format_card(c1)} vs {format_card(c2)}")

#decide who wins the flip or its going to be a war
        if c1[2] > c2[2]:
            won1 += pot
            log.append("    Human wins the round")
        elif c2[2] > c1[2]:
            won2 += pot
            log.append("    Computer wins the round")
        else:
            log.append("    Tie - war ")
            _, war_count, ended = war(active1, won1, active2, won2, pot, log, round_num, war_count)
            if ended:
                break

        log.append(f"    Decks : Human = {len(active1)}, Computer = {len(active2)}")

#overall game information
    log.append(f"\nGame over in {round_num} rounds")
    p1_total = total_cards(active1, won1)
    p2_total = total_cards(active2, won2)
    log.append(f"Human total cards : {p1_total}")
    log.append(f"Computer total cards : {p2_total}")
    log.append(f"War count : {war_count}")

#decide who wins the game
    if p1_total > p2_total:
        log.append("Human wins the game \n\n")
    elif p2_total > p1_total:
        log.append("Computer wins the game \n\n")
    else:
        log.append("Game is a tie \n\n")

#new decks creating for next rounds
    new_p1 = active1 + won1
    new_p2 = active2 + won2
    random.shuffle(new_p1)
    random.shuffle(new_p2)

    return log, new_p1, new_p2
