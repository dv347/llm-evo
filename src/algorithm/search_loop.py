from multiprocessing import Pool

from algorithm.parameters import params
from algorithm.step import step
from fitness.evaluation import evaluate_fitness
from operators.initialisation import initialisation
from stats.stats import get_stats, stats
from utilities.algorithm.initialise_run import pool_init

from tracker import Tracker


def search_loop() -> list:
    if params['MULTICORE']:
        params['POOL'] = Pool(processes=params['CORES'], initializer=pool_init,
                              initargs=(params,))  # , maxtasksperchild=1)
    
    tracker = Tracker(params['EXPERIMENT_NAME'])

    individuals = initialisation(params['POPULATION_SIZE'])
    individuals = evaluate_fitness(individuals)

    get_stats(individuals, tracker)

    if params['STEP'].__name__ == 'step':
        params['STEP'] = step

    for generation in range(1, (params['GENERATIONS'] + 1)):
        stats['gen'] = generation

        individuals = params['STEP'](individuals, tracker)

    if params['MULTICORE']:
        params['POOL'].close()

    result = get_stats(individuals, tracker, end=True)
    result.individuals = individuals

    return result