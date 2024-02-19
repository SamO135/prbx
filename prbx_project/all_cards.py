from prbx_project.card import Card
from prbx_project.settings import Token

with open("prbx_project/splendor_cards.csv", "r") as file:
    all_cards = [[], [], []]
    line = file.readline()
    line  = file.readline()
    while line:
        card_data = line.split(",")
        for i in range(len(card_data)):
            try:
                card_data[i] = int(card_data[i])
            except:
                match card_data[i]:
                    case "Red":
                        card_data[i] = Token.RED
                    case "Green":
                        card_data[i] = Token.GREEN
                    case "Blue":
                        card_data[i] = Token.BLUE
                    case "White":
                        card_data[i] = Token.WHITE
                    case "Black":
                        card_data[i] = Token.BLACK
        card = Card(
            id=0,
            points=card_data[2],
            bonus=card_data[1],
            price={
                Token.RED: card_data[6],
                Token.GREEN: card_data[5],
                Token.BLUE: card_data[4],
                Token.WHITE: card_data[7],
                Token.BLACK: card_data[3],
                Token.YELLOW: 0
                },
            tier=card_data[0],
            )
        all_cards[card.tier-1].append(card)
        line = file.readline()     
