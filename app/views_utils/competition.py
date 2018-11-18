import json
from flask import render_template

from app.connector import Connector


class Team:
    played_matches = 0
    points = 0
    scored = 0
    conceded = 0
    won = 0
    drawn = 0
    lost = 0

    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_team_id_from_match(match, team_index):
    return int(match['teams'][team_index]['team'].split('/')[-2])


def prepare_competition_page(id):
    connector = Connector()
    json_matches = connector.send_get('competitions/{}/matches/'.format(id))
    matches = json.loads(json_matches)
    json_teams = connector.send_get('competitions/{}/teams/'.format(id))
    teams = json.loads(json_teams)
    proper_teams = []
    [proper_teams.append(Team(team['id'], team['name'])) for team in teams]
    for match in matches:
        if match['status'] in ['scheduled', 'in_play']:
            continue
        team_indexes = []
        for i, team in enumerate(proper_teams):
            if team.id == get_team_id_from_match(match, 0):
                team_indexes.append(i)
        for i, team in enumerate(proper_teams):
            if team.id == get_team_id_from_match(match, 1):
                team_indexes.append(i)
        for i, index in enumerate(team_indexes):
            proper_teams[index].played_matches += 1
            proper_teams[team_indexes[i]].scored += match['teams'][i]['goals']
            proper_teams[team_indexes[i]].conceded += match['teams'][(i + 1) % 2]['goals']

        if match['teams'][0]['goals'] > match['teams'][1]['goals']:
            proper_teams[team_indexes[0]].points += 3
            proper_teams[team_indexes[0]].won += 1
            proper_teams[team_indexes[1]].lost += 1
        elif match['teams'][0]['goals'] == match['teams'][1]['goals']:
            for index in team_indexes:
                proper_teams[index].points += 1
                proper_teams[index].drawn += 1
        else:
            proper_teams[team_indexes[1]].points += 3
            proper_teams[team_indexes[1]].won += 1
            proper_teams[team_indexes[0]].lost += 1

    proper_teams.sort(key=lambda x: x.points, reverse=True)

    return render_template('competition.html', competition_id=id, matches=matches, teams=proper_teams)
