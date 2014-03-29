import json

from flask import Flask
from flask import request
from flask_cors import cross_origin
app = Flask(__name__)

candidates_list = {
    "John Boener": {
        "Tech": 3,
        "Guns": 5,
        "Lobby": 2,
        "Pharma": 5,
        "Union": 1
    },
    "Eric Cantor": {
        "Tech": 1,
        "Guns": 1,
        "Lobby": 5,
        "Pharma": 1,
        "Union": 5
    }
}

@app.route('/')
@cross_origin()
def hello():
    return 'politindr init!\n'

@app.route('/choice', methods=['POST'])
@cross_origin()
def create_choice():
    """Route to create a new choice when seleting through industries
    """
    data = json.loads(request.data)
    candidate_votes = calculate_politicians(data)

    return json.dumps(candidate_votes)

def calculate_politicians(vote_dicts):
    """Calculate all the politician rating based off the industry voting data
    sent in.

    Arguments
    vote_dicts -- list, The vote information sent from frontend, a list of 
    dicts with industry and vote from user.

    Returns
    list A list of dicts with the candidate name and puirty.
    [
      {
        name: {string}
        purity: {int -1|0|1}
      }
    ]
    """
    to_return = []
    for politician in candidates_list:
        politician_industries = candidates_list[politician]
        tally = 0
        politician_dict = {}
        for vote in vote_dicts:
            rating = politician_industries[vote['industry_group_name']]
            vote_choice = vote['choice']
            tally += rank_politician(rating, vote_choice)

        politician_dict['name'] = politician
        politician_dict['purity'] = calculate_purity(tally)
        
        to_return.append(politician_dict)

    return to_return

def rank_politician(rating, choice):
    """Ranks the politician by applying a calcuation to the rating, which is a
    summerized number based on contribution money amount, and choice, which is
    a int between -1 and 1 based on what the user voted.

    Arguments
    rating -- int, The rating of the candidate to industry
    choice -- int, The choice of the user between -1 and 1

    Returns
    int, Based on multiplying choice by rating

    """
    calc = choice * rating
    return calc
        
def calculate_purity(rating):
    """Ranks the puirty number between -1 to 1, which will correctly label the
    politician.

    Arguments
    rating -- int, The rating for the candidate to apply the purity rating to.
    """
    if rating >= 1:
        return 1
    elif rating <= -1:
        return -1
    else:
        return 0

if __name__ == "__main__":
    app.run(port=8080, debug=True)
