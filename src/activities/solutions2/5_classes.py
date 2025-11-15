from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Medal:
    type: str
    design: str
    date_designed: date


class athletle:
    def __init__(self, name: str, team: str, disability_class: str, medals: List[Medal]):
        self.name = name
        self.team = team
        self.disability_class = disability_class
        self.medals = medals

    def __str__(self):
        return (
            f"Athlete: {self.name}\n"
            f"Team: {self.team}\n"
            f"Classification: {self.disability_class}\n"
            f"Medals: {', '.join([medal.type for medal in self.medals]) if self.medals else 'None'}"
        )
medal1 = Medal("gold", "Paris 2024 design", date(2023, 7, 1))
medal2 = Medal("silver", "Tokyo 2020 design", date(2019, 8, 25))

a = athletle("Sungjoon Jung", "KOR", "BC1", [medal1, medal2])
print(a)