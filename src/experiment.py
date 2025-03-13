import argparse
import copy
import os
import time
from typing import List

from algorithm.parameters import params, set_params
from stats.stats import stats
from utilities.stats import trackers

from config import generate_configs, load_task_list, load_config, make_ge_params, save_to_file
from algorithm.search_loop import search_loop
from paths import RESULTS_DIR
from results import Result, Results, ResultsToCompare, SuiteResults, SuiteResultsToCompare


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the configuration file"
    )
    args = parser.parse_args()
    return args


def get_config() -> dict:
    args = parse_arguments()
    config_path = args.config
    config = load_config(config_path)
    return config


def get_tasks(config) -> List[str]:
    match config['benchmark']['type']:
        case 'single':
            return [config['benchmark']['problem_name']]
        case 'suite':
            match config['benchmark']['suite_name']:
                case 'psb1':
                    return load_task_list('psb1')
                case 'psb2':
                    return load_task_list('psb2')
                case _:
                    raise ValueError('Invalid suite name')
        case _:
            raise ValueError('Invalid benchmark')
        

def reset_trackers():
    trackers.cache = {}
    trackers.runtime_error_cache = []
    trackers.best_fitness_list = []
    trackers.first_pareto_list = []
    trackers.time_list = []
    trackers.stats_list = []
    trackers.best_ever = None


def reset_dict(defaults: dict, dictionary: dict) -> None:
    for key, value in defaults.items():
        dictionary[key] = value


def run_ge(task: str, config: dict, iteration: int) -> Result:
    start_time = time.time()
    start_params = copy.deepcopy(params)
    start_stats = copy.deepcopy(stats)
    ge_params = make_ge_params(task, config)
    set_params(ge_params)
    tracker = search_loop()
    reset_trackers()
    reset_dict(start_params, params)
    reset_dict(start_stats, stats)
    end_time = time.time()
    return Result(tracker, task, iteration, end_time - start_time)


def run_experiment(experiment_config: dict, tasks: List[str]) -> None:
    save_dir = os.path.join(RESULTS_DIR, f'{experiment_config['experiment_name']}')
    save_to_file(experiment_config, save_dir)
    num_runs = experiment_config['num_runs']
    results_list = []
    for task in tasks:
        if task == 'String Differences':
            continue
        task_results = []
        print(f'Running {task}')
        for iteration in range(num_runs):
            print(f'\t Iteration {iteration + 1}')
            result = run_ge(task, experiment_config, iteration)
            result.save()
            task_results.append(result)
        if num_runs > 1:
            results = Results(task_results, task)
            results.save()
            results_list.append(results)
    if len(tasks) > 1 and num_runs > 1:
        suite_results = SuiteResults(results_list)
        suite_results.save()
        return suite_results
    elif len(tasks) == 1 and num_runs > 1:
        return results


if __name__ == "__main__":
    config = get_config()
    comparator = config.pop('comparator', None)
    experiment_configs = generate_configs(config)
    tasks = get_tasks(config)

    experiment_results = []
    for experiment_config in experiment_configs:
        experiment_result = run_experiment(experiment_config, tasks)
        experiment_results.append(experiment_result)

    if comparator is not None:
        if type(experiment_results[0]) == Results:
            ResultsToCompare(experiment_results, comparator).save()
        elif type(experiment_results[0]) == SuiteResults:
            SuiteResultsToCompare(experiment_results, comparator).save()