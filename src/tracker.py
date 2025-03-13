class Tracker:
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.start_best = None
        self.best_ever = None
        self.best_fitness_list = []
        self.average_fitness_list = []
        self.best_phenotype_list = []
        self.individuals = []