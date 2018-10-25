from app.retrievers import retriever_interface
from flask import json


def construct_proper_team(team):
    proper_team = {
        'name': team['name'],
        'type': team_types[team['name']]
    }
    return proper_team


class TeamRetriever(retriever_interface.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        json_content = json.loads(content)
        teams = json_content['teams']
        available_teams = list()
        for team in teams:
            proper_team = construct_proper_team(team)
            available_teams.append(proper_team)
            print(proper_team)

        return available_teams
