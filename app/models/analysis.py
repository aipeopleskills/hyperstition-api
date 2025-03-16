import json
from pathlib import Path

class SyntacticAnalyzer:
    def __init__(self):
        rules_path = Path("app/data/patterns/syntactic_rules.json")
        self.rules = json.loads(rules_path.read_text(encoding="utf-8"))["es"]
        
    def _load_rules(self, category: str) -> dict:
        return self.rules.get(category, {})