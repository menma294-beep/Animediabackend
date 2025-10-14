from neo4j import GraphDatabase
from app.config import settings

# Initialize driver using values from settings
driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

def get_driver():
    return driver

def run_query(query: str, parameters: dict = None, single: bool = False):
    with driver.session() as session:
        result = session.run(query, parameters or {})
        records = list(result)  # consume once safely
        return records[0] if single and records else records
