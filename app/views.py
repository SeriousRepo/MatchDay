from app.app import app
from app.connector import connector
from app.retrievers.competition_retriever import CompetitionRetriever


@app.route('/')
def hello():
    content = connector.connect('http://api.football-data.org/v2/competitions?plan=TIER_ONE')
    retriever = CompetitionRetriever()
    comp = retriever.retrieve(content)
    return 'asd'
