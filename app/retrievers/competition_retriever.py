from app.retrievers import retriever_interface
from flask import json


competition_types = {
        'Série A': 'league',
        'Championship': 'league',
        'Premier League': 'league',
        'European Championship': 'tournament',
        'UEFA Champions League': 'tournament',
        'Ligue 1': 'league',
        'Bundesliga': 'league',
        'Serie A': 'league',
        'Eredivisie': 'league',
        'Primeira Liga': 'league',
        'Primera Division': 'league',
        'FIFA World Cup': 'tournament'
    }


def construct_proper_competition(competition):
    proper_competition = {
        'name': competition['name'],
        'type': competition_types[competition['name']]
    }
    return proper_competition


class CompetitionRetriever(retriever_interface.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        json_content = json.loads(content)
        competitions = json_content['competitions']
        available_competitions = list()
        for competition in competitions:
            proper_competition = construct_proper_competition(competition)
            available_competitions.append(proper_competition)
            print(proper_competition)

        return available_competitions
