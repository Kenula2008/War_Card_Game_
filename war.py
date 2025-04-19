import sys
import random
from datetime import datetime
from module import create_deck, deal, play_rounds

def main():

#deciding the game count with user input in console    
    try:
        count = int(sys.argv[1])
        count = count if 1 <= count <= 5 else 1
    except (IndexError, ValueError):
        count = 1#default output coming if any error happens 

#datetime capturing process
    now = datetime.now()
    logs = [f"Date : {now.date()} \nTime : {now.strftime('%H:%M:%S')}", ""]

#deck manage
    deck = create_deck()
    human, computer = deal(deck)

#use to play till one player deck get over
    for game in range(1, count + 1):
        game_log, human, computer = play_rounds(human, computer, game)
        logs.extend(game_log)
        if not human or not computer:
            break

#making file names 
    filename = f"[{now.strftime('%y-%m-%d')}]_[{now.strftime('%H-%M')}]_{random.randint(1000,9999)}"
    with open(f"{filename}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    with open(f"{filename}.html", "w", encoding="utf-8") as f:
        f.write("<html><body><pre>" + "\n".join(logs) + "</pre></body></html>")

#output in console
    print(f"Logs saved to {filename}.txt and {filename}.html")

if __name__ == "__main__":
    main()
