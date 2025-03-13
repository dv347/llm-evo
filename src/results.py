import os
import statistics
from typing import List

from matplotlib import pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

from paths import RESULTS_DIR
from tracker import Tracker


def plot_fitness_list(fitness_list: List[float], title: str, path: str) -> None:
    plt.plot(fitness_list, linestyle='-', color='blue')
    plt.xlim(left=0, right=50)
    plt.ylim(bottom=0)
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.savefig(f'{path}.png')
    plt.close()


def plot_times(times: List[float], tasks: List[str], path: str) -> None:
    assert len(times) == len(tasks)
    plt.bar(tasks, times)
    plt.title('Time Taken for Each Task')
    plt.xlabel('Task')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f'{path}.png')
    plt.close()


def plot_multiple_lists(fitness_lists: List[List[float]], labels: List[str], title: str, path: str) -> None:
    plt.figure(figsize=(8, 6))
    colours = ['blue', 'orange']
    linestyles = ['-', ':']
    for i, (fitness_list, label) in enumerate(zip(fitness_lists, labels)):
        color = colours[i % len(colours)]
        linestyle = linestyles[i % len(linestyles)]
        plt.plot(fitness_list, linestyle=linestyle, color=color, label=label, linewidth=3)
    plt.xlim(left=0, right=50)
    plt.ylim(bottom=0)
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig(f'{path}.pdf', bbox_inches='tight')
    plt.close()


class Result:
    def __init__(self, tracker: Tracker, task: str, iteration: int, elapsed_time: float):
        self.experiment_name = tracker.experiment_name
        self.best_fitness_list = tracker.best_fitness_list
        self.average_fitness_list = tracker.average_fitness_list
        self.best_phenotype_list = tracker.best_phenotype_list
        self.best_ever = tracker.best_ever
        self.best_fitness = self.best_ever.fitness
        self.best_phenotype = self.best_ever.phenotype
        self.start_fitness = tracker.start_best.fitness
        self.start_phenotype = tracker.start_best.phenotype
        self.solved = self.best_fitness < 0.005
        self.elapsed_time = elapsed_time
        dir = f"{self.experiment_name}/{task}/Run_{iteration}_[Solved]/" if self.solved else f"{self.experiment_name}/{task}/Run_{iteration}/"
        self.save_dir = os.path.join(RESULTS_DIR, dir)

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)

        with open(f'{self.save_dir}Result.txt', 'w') as file:
            file.write(f'Solved: {self.solved}\n')
            file.write(f'Elapsed Time: {self.elapsed_time}\n\n')
            file.write(f'Best Fitness: {self.best_fitness}\n')
            file.write(f'Best Phenotype: {self.best_phenotype}\n\n')
            file.write(f'Start Fitness: {self.start_fitness}\n')
            file.write(f'Start Phenotype: {self.start_phenotype}')

        with open(f'{self.save_dir}Phenotypes.txt', 'w') as file:
            for i, phenotype in enumerate(self.best_phenotype_list):
                file.write(f'Generation {i}:\n')
                file.write(f'{phenotype}\n')

        plot_fitness_list(self.best_fitness_list, 'Best Fitness', f'{self.save_dir}Best_Fitness')
        plot_fitness_list(self.average_fitness_list, 'Average Fitness', f'{self.save_dir}Average_Fitness')


class Results:
    def __init__(self, results: List[Result], task: str):
        self.no_results = len(results)
        best_fitness_lists = [result.best_fitness_list for result in results]
        average_fitness_lists = [result.average_fitness_list for result in results]
        self.best_fitnesses = [min(values) for values in zip(*best_fitness_lists)]
        final_values = [values[-1] for values in best_fitness_lists]
        std_dev_final_values = statistics.stdev(final_values)
        self.std_dev_final_values = std_dev_final_values
        self.average_best_fitnesses = [sum(values) / len(values) for values in zip(*best_fitness_lists)]
        self.average_fitnesses = [sum(values) / len(values) for values in zip(*average_fitness_lists)]
        best_evers = [result.best_ever for result in results]
        best_ever = min(best_evers, key=lambda x: x.fitness)
        self.best_fitness = best_ever.fitness
        self.best_phenotype = best_ever.phenotype
        self.no_solved = sum(result.solved for result in results)
        self.solved = self.no_solved > 0
        self.experiment_name = results[0].experiment_name
        elapsed_times = [result.elapsed_time for result in results]
        self.total_elapsed_time = sum(elapsed_times)
        self.average_elapsed_time = self.total_elapsed_time / self.no_results
        self.save_dir = os.path.join(RESULTS_DIR, f"{self.experiment_name}/{task}/Results/")
        self.task = task

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)

        with open(f'{self.save_dir}Result.txt', 'w') as file:
            file.write(f'Solved: {self.solved}\n\n')
            file.write(f'Total time elapsed: {self.total_elapsed_time}\n')
            file.write(f'Average time elapsed: {self.average_elapsed_time}\n\n')
            file.write(f'Number solved: {self.no_solved} out of {self.no_results}\n\n')
            file.write(f'Best Fitness: {self.best_fitness}\n')
            file.write(f'Best Phenotype: {self.best_phenotype}')

        plot_fitness_list(self.best_fitnesses, 'Best Fitness', f'{self.save_dir}Best_Fitness')
        plot_fitness_list(self.average_best_fitnesses, 'Average Best Fitness', f'{self.save_dir}Average_Best_Fitness')
        plot_fitness_list(self.average_fitnesses, 'Average Fitness', f'{self.save_dir}Average_Fitness')


class SuiteResults:
    def __init__(self, results: List[Results]):
        self.results = results
        self.no_solved = sum(result.solved for result in results)
        self.tasks = [result.task for result in results]
        self.solved_tasks = [(result.task, result.no_solved, result.no_results) for result in results if result.solved]
        self.elapsed_times = [result.total_elapsed_time for result in results]
        self.total_elapsed_time = sum(self.elapsed_times)
        self.save_dir = os.path.join(RESULTS_DIR, f"{results[0].experiment_name}/")

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        
        with open(f'{self.save_dir}Results.txt', 'w') as file:
            file.write(f'Number of solved tasks: {self.no_solved}\n\n')
            file.write(f'Total time elapsed: {self.total_elapsed_time}\n')
            for task, no_solved, no_results in self.solved_tasks:
                file.write(f'{task}: {no_solved} out of {no_results}\n')
            
        plot_times(self.elapsed_times, self.tasks, f'{self.save_dir}Time_Taken')


class ResultsToCompare:
    def __init__(self, results: List[Results], comparator: str):
        if comparator not in ['grammar']:
            raise ValueError('Invalid comparator')
        self.results = results
        self.comparator = comparator
        assert results[0].save_dir == results[0].save_dir
        self.save_dir = results[0].save_dir
    
    def save(self) -> None:
        if self.comparator == 'grammar':
            labels = ['Base', 'Minimal']
            input = [result.average_best_fitnesses for result in self.results]

            with open(f'{self.save_dir}Comparison_Results.txt', 'w') as file:
                file.write(f'Final best fitnesses: {input[0][-1]} compared to {input[1][-1]}\n')
                file.write(f'Std devs: {self.results[0].std_dev_final_values} compared to {self.results[1].std_dev_final_values}\n')
                                        
            plot_multiple_lists([result.best_fitnesses for result in self.results], labels, self.results[0].task, f'{self.save_dir}Comparison_Best_Fitness')
            plot_multiple_lists(input, labels, self.results[0].task, f'{self.save_dir}Comparison_Average_Best_Fitness')


class SuiteResultsToCompare:
    def __init__(self, suite_results: List[SuiteResults], comparator: str):
        if comparator not in ['grammar']:
            raise ValueError('Invalid comparator')
        self.suite_results = suite_results
        self.comparator = comparator

    def save(self) -> None:
        results_lists = [suite_result.results for suite_result in self.suite_results]
        for results_list in zip(*results_lists):
            results_to_compare = ResultsToCompare(list(results_list), self.comparator)
            results_to_compare.save()