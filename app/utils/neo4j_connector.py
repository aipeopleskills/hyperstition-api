from neo4j import GraphDatabase
import os

class Neo4jConnector:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "hyperstition")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
    
    def get_db(self):
        return self.driver