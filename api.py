import click
from flask import Flask, jsonify, render_template, Response
from card_manager import CardManager


app = Flask(__name__)


# --------------------------- Helper Methods -------------------------------



# --------------------------- Commands -------------------------------------------------

@click.command()
@click.option('--host', default = "127.0.0.1", help = "Host IP address.")
@click.option('--port', default = 9999, help = "Host\'s Port")
@click.option('--database', default = "filesystem://metadata_cards", help = "Database type and location")
def run_api_server(host, port, database):
    global driver                               # I am not sure this is the best way, but it is simple so i will take it
    driver = CardManager.get_driver(database)
    app.run(host=host,port=port)


@app.route("/creators")
def get_creators():
    return render_template("creators.html", creators = list(driver.getCreators()))


@app.route("/creators/<creator>/cards/<is_solved>")
def get_creator_cards(creator, is_solved):
    if is_solved == "solved": 
        return render_template("creator_cards.html", cards = [str(card) for card in  driver.getCreatorCards(creator) if card.solution != None], header = f"{creator}\'s solved cards")
    elif is_solved == "unsolved":
        return render_template("creator_cards.html", cards = [str(card) for card in  driver.getCreatorCards(creator) if card.solution == None], header = f"{creator}\'s unsolved cards")
    else:
        return Response(
            "Invalid option: use 'solved' or 'unsolved'",
            status=400,
        )



if __name__ == "__main__":
    run_api_server()