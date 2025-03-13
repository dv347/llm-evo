from copy import copy
from sys import stdout
from time import time
from typing import List

import numpy as np
from algorithm.parameters import params
from utilities.stats import trackers
from representation.individual import Individual

from tracker import Tracker


"""Algorithm statistics"""
stats = {
    "gen": 0,
    "total_inds": 0,
    "regens": 0,
    "invalids": 0,
    "runtime_error": 0,
    "unique_inds": len(trackers.cache),
    "unused_search": 0,
    "ave_genome_length": 0,
    "max_genome_length": 0,
    "min_genome_length": 0,
    "ave_used_codons": 0,
    "max_used_codons": 0,
    "min_used_codons": 0,
    "ave_tree_depth": 0,
    "max_tree_depth": 0,
    "min_tree_depth": 0,
    "ave_tree_nodes": 0,
    "max_tree_nodes": 0,
    "min_tree_nodes": 0,
    "ave_fitness": 0,
    "best_fitness": 0,
    "time_taken": 0,
    "total_time": 0,
    "time_adjust": 0
}


def get_stats(individuals: List[Individual], tracker: Tracker = Tracker(""), end: bool = False) -> Tracker:
    """
    Generate the statistics for an evolutionary run with a single objesctive.
    Save statistics to utilities.trackers.stats_list. Print statistics. Save
    fitness plot information.

    :param individuals: A population of individuals for which to generate
    statistics.
    :param end: Boolean flag for indicating the end of an evolutionary run.
    """

    # Get best individual.
    best = max(individuals)

    if not tracker.best_ever:
        tracker.start_best = best
        tracker.best_ever = best
    if best > tracker.best_ever:
        tracker.best_ever = best

    tracker.best_fitness_list.append(tracker.best_ever.fitness)
    tracker.best_phenotype_list.append(tracker.best_ever.phenotype)
    fitnesses = [i.fitness for i in individuals]
    average_fitness = np.nanmean(fitnesses, axis=0)
    tracker.average_fitness_list.append(average_fitness)

    # Print simple display output.
    perc = stats['gen'] / (params['GENERATIONS'] + 1) * 100
    stdout.write("Evolution: %d%% complete\r" % perc)
    stdout.flush()

    # Save stats to list.
    # if params['VERBOSE'] or (not params['DEBUG'] and not end):
    #     trackers.stats_list.append(copy(stats))

    return tracker


def update_stats(individuals, end):
    """
    Update all stats in the stats dictionary.

    :param individuals: A population of individuals.
    :param end: Boolean flag for indicating the end of an evolutionary run.
    :return: Nothing.
    """

    if not end:
        # Time Stats
        trackers.time_list.append(time() - stats['time_adjust'])
        stats['time_taken'] = trackers.time_list[-1] - \
                              trackers.time_list[-2]
        stats['total_time'] = trackers.time_list[-1] - \
                              trackers.time_list[0]

    # Population Stats
    stats['total_inds'] = params['POPULATION_SIZE'] * (stats['gen'] + 1)
    stats['runtime_error'] = len(trackers.runtime_error_cache)
    if params['CACHE']:
        stats['unique_inds'] = len(trackers.cache)
        stats['unused_search'] = 100 - stats['unique_inds'] / \
                                 stats['total_inds'] * 100

    # Genome Stats
    genome_lengths = [len(i.genome) for i in individuals]
    stats['max_genome_length'] = np.nanmax(genome_lengths)
    stats['ave_genome_length'] = np.nanmean(genome_lengths)
    stats['min_genome_length'] = np.nanmin(genome_lengths)

    # Used Codon Stats
    codons = [i.used_codons for i in individuals]
    stats['max_used_codons'] = np.nanmax(codons)
    stats['ave_used_codons'] = np.nanmean(codons)
    stats['min_used_codons'] = np.nanmin(codons)

    # Tree Depth Stats
    depths = [i.depth for i in individuals]
    stats['max_tree_depth'] = np.nanmax(depths)
    stats['ave_tree_depth'] = np.nanmean(depths)
    stats['min_tree_depth'] = np.nanmin(depths)

    # Tree Node Stats
    nodes = [i.nodes for i in individuals]
    stats['max_tree_nodes'] = np.nanmax(nodes)
    stats['ave_tree_nodes'] = np.nanmean(nodes)
    stats['min_tree_nodes'] = np.nanmin(nodes)

    # Fitness Stats
    fitnesses = [i.fitness for i in individuals]
    stats['ave_fitness'] = np.nanmean(fitnesses, axis=0)
    stats['best_fitness'] = trackers.best_ever.fitness