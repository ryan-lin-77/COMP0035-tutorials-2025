# Base class
class Athlete:
    def __init__(self, first_name, last_name, team_code, disability_class):
        self.first_name = first_name
        self.last_name = last_name
        self.team_code = team_code
        self.disability_class = disability_class

    def introduce(self):
        print(f"{self.first_name} {self.last_name} represents {self.team_code} in class {self.disability_class}.")


# Subclass
class Runner(Athlete):
    def __init__(self, first_name, last_name, team_code, disability_class, distance):
        super().__init__(first_name, last_name, team_code, disability_class)
        self.distance = distance  # e.g., 100m, 400m

    def race_info(self):
        print(f"{self.first_name} is running the {self.distance} race.")


# Example usage
runner1 = Runner("Li", "Na", "CHN", "T12", "100m")
runner1.introduce()  # Inherited method
runner1.race_info()  # Subclass-specific methodzzzzzzzzzzz