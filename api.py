import click
from flask import Flask, render_template, Response, request
from card_manager import CardManager


app = Flask(__name__)


# --------------------------- Helper Methods -------------------------------



# --------------------------- Commands -------------------------------------------------

@click.command()
@click.option('--host', default = "127.0.0.1", help = "Host IP address.")
@click.option('--port', default = 9999, help = "Host\'s Port")
@click.option('--database', default = "filesystem://metadata_cards", help = "Database type and location")
def run_api_server(host, port, database):
    global driver, card_manager                             # I am not sure this is the best way, but it is simple so i will take it
    card_manager = CardManager(database, "images")
    driver = card_manager.driver        # I just don't want to write card_manager.driver everytime
    app.run(host=host,port=port)


@app.route("/creators")
def get_creators():
    return render_template("creators.html", creators = list(driver.getCreators()))


# I will upload the picture on this command too (only f the option is a card), I see no reason to split this two commands
@app.route("/creators/<creator>/cards/<option>")     
def get_creator_card(creator, option):
    if option == "solved":
        return render_template("creator_cards.html", cards = [str(card) for card in driver.getCreatorCards(creator) if card.solution != None], header = f"{creator}\'s solved cards")
    elif option == "unsolved":
        print(card_manager.driver.getCreatorCards(creator))
        return render_template("creator_cards.html", cards = [str(card) for card in driver.getCreatorCards(creator) if card.solution == None], header = f"{creator}\'s unsolved cards")
    
    card_name = option           # much more informative
    creator_cards = driver.getCreatorCards(creator)
    for card in creator_cards:
        if card.name == card_name: 
            return render_template("creator_card.html", card = card, impath = card_manager.get_card_impath(card))
    return Response(
        "Invalid command: card does not exist",
        status=400,
    )


@app.route("/cards/find")
def find_card():
    name = request.args.get("name", "")
    creator = request.args.get("creator", "")
    riddle = request.args.get("riddle", "") 

    cards = driver.getCards()
    cards = [card for card in cards if (name in card.name and creator in card.creator and riddle in card.riddle)]
    return render_template("find_cards.html", cards = cards, name = name, creator = creator, riddle = riddle)


@app.post("/cards/<card_id>/solve")
def check_solution(card_id: str):
    creator, name = card_id.split("_")
    creator_cards = driver.getCreatorCards(creator)
    for card in creator_cards:
        if card.name == name:
            if request.json["solution"] == card.solution:           #card.solution = None always
                impath = CardManager.get_card_impath(card)
                print()
            else:
                print()
    return Response(
        "Invalid command: card does not exist",
        status=400,
    )



if __name__ == "__main__":
    run_api_server()