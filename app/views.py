from flask import Blueprint
import math

from app.views_utils.index import *
from app.views_utils.competition import *
from app.connector import Connector

view = Blueprint('view', __name__)


@view.route('/')
def index():
    return prepare_index_page()


@view.route('/competitions')
def competitions():
    connector = Connector()
    json_competitions = connector.send_get('competitions/')
    competitions = json.loads(json_competitions)
    return render_template('competitions.html', competitions=competitions)


@view.route('/competitions/<int:id>')
def competition(id):
    return prepare_competition_page(id)


def get_id_from_url(url):
    return int(url.split('/')[-2])


def calculate_age(born):
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Player:
    def __init__(self, id, name, position, birth_date, shirt_number, nationality):
        self.id = id
        self.name = name
        self.position = position
        self.age = calculate_age(datetime.strptime(birth_date, '%Y-%m-%d'))
        self.shirt_number = shirt_number
        self.nationality = nationality


@view.route('/teams/<int:id>')
def team(id):
    connector = Connector()
    json_team = connector.send_get('teams/{}/'.format(id))
    team = json.loads(json_team)
    json_people = connector.send_get('people/')
    people = json.loads(json_people)
    proper_players = []
    for player in team['players']:
        for person in people:
            if get_id_from_url(player['person']) == person['id']:
                proper_player = Player(id=person['id'], name=person['name'],
                                       position=player['position'], birth_date=person['birth_date'],
                                       shirt_number=player['shirt_number'], nationality=person['nationality'])
                proper_players.append(proper_player)

    decks_amount = math.ceil(len(proper_players) / 3)

    return render_template('team.html', team=team, players=proper_players, decks_amount=decks_amount)


@view.route('/competitions/<int:id>/matches')
def competition_matches(id):
    connector = Connector()
    json_matches = connector.send_get('competitions/{}/matches/'.format(id))
    json_teams = connector.send_get('competitions/{}/teams/'.format(id))
    matches = json.loads(json_matches)
    teams = json.loads(json_teams)
    matches_to_display = []
    for i in range(0, len(matches)):
        team1 = get_team_by_id(get_team_id(matches[i]['teams'][0]), teams)
        team2 = get_team_by_id(get_team_id(matches[i]['teams'][1]), teams)
        if matches[i]['teams'][0]['is_host']:
            home_team = TeamInMatch(matches[i]['teams'][0], team1)
            away_team = TeamInMatch(matches[i]['teams'][1], team2)
        else:
            home_team = TeamInMatch(matches[i]['teams'][0], team2)
            away_team = TeamInMatch(matches[i]['teams'][1], team1)
        matches_to_display.append(Match(matches[i], home_team, away_team))

    return render_template('matches.html', competition_id=id, matches=matches_to_display)


@view.route('/competitions/<int:competition_id>/matches/<int:match_id>')
def competition_match(competition_id, match_id):
    connector = Connector()
    json_match = connector.send_get('competitions/{}/matches/{}/'.format(competition_id, match_id))
    json_teams = connector.send_get('competitions/{}/teams/'.format(competition_id))
    match = json.loads(json_match)
    teams = json.loads(json_teams)
    team1 = get_team_by_id(get_team_id(match['teams'][0]), teams)
    team2 = get_team_by_id(get_team_id(match['teams'][1]), teams)
    if match['teams'][0]['is_host']:
        home_team = TeamInMatch(match['teams'][0], team1)
        away_team = TeamInMatch(match['teams'][1], team2)
    else:
        home_team = TeamInMatch(match['teams'][0], team2)
        away_team = TeamInMatch(match['teams'][1], team1)
    match_to_display = Match(match, home_team, away_team)

    return render_template('match.html', match=match_to_display, competition_id=competition_id)
