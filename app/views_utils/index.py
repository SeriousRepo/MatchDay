from datetime import datetime
import json
from flask import render_template

from app.connector import Connector


class TeamInMatch:
    def __init__(self, team_in_match, team_info):
        self.team = team_in_match
        self.info = team_info


class Match:
    def __init__(self, match_info, home_team, away_team):
        self.info = match_info
        self.home_team = home_team
        self.away_team = away_team


def get_team_by_id(id, teams):
    proper_team = 0
    for team in teams:
        if str(team['id']) == id:
            proper_team = team
            break
    return proper_team


def get_team_id(team_in_match):
    return team_in_match['team'].split('/')[-2]


def prepare_index_page():
    todays_date = datetime.now().strftime('%d-%m-%Y')
    connector = Connector()
    json_matches = connector.send_get('matches/today/')
    json_teams = connector.send_get('teams/')
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

    return render_template('index.html', date=todays_date, matches=matches_to_display)
