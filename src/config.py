import itertools
import json
import os
import time

from paths import BASE_DIR


def load_task_list(suite_name) -> list:
    tasks_file_path = os.path.join(BASE_DIR, f"tasks/{suite_name}_tasks.json")
    
    if not os.path.exists(tasks_file_path):
        raise FileNotFoundError(f"Tasks file not found for suite: {suite_name}")
    
    with open(tasks_file_path, 'r') as f:
        tasks = json.load(f)
    
    return tasks


def apply_defaults(config: dict):
    defaults = {}

    for key, value in defaults.items():
        config.setdefault(key, value)
    
    return config


def load_config(config_filename: str) -> dict:
    config_path = os.path.join(BASE_DIR, config_filename)
    with open(config_path, 'r') as f:
        config = json.load(f)

    config = apply_defaults(config)
    
    return config


def generate_configs(config: dict) -> list:
    single_params = {k: v for k, v in config.items() if not isinstance(v, list)}
    multi_params = {k: v for k, v in config.items() if isinstance(v, list)}
    
    # Generate all combinations of multi-value parameters
    keys, values = zip(*multi_params.items()) if multi_params else ([], [])
    all_combinations = list(itertools.product(*values)) if values else [()]

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    configs = []
    for index, combination in enumerate(all_combinations):
        combined_config = {**single_params, **dict(zip(keys, combination))}
        prefix = f'{config['experiment_name']}_{timestamp}'
        combined_config["experiment_name"] = f"{prefix}_{index:02d}" if multi_params else prefix
        configs.append(combined_config)
    
    return configs


def make_ge_params(task: str, config: dict) -> list:
    def build_flag(key, value):
        if key in param_names and value is not None:
            if isinstance(value, bool):
                if value:
                    return [f"--{key}"]
            else:
                return [f"--{key}", str(value)]
        return []
            
    param_names = set([
        'crossover',
        'crossover_probability',
        'elite_size',
        'experiment_name',
        'generations',
        'max_init_tree_depth',
        'max_tree_depth',
        'mutation',
        'mutation_events',
        'mutation_probability',
        'no_crossover_invalids',
        'no_mutation_invalids',
        'population_size',
        'random_seed',
        'replacement',
        'selection',
        'selection_proportion',
        'tournament_size'
    ])

    ge_params = []
            
    for key, value in config.items():
        if key in ['benchmark', 'grammar']:
            continue
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                ge_params += build_flag(subkey, subvalue)
        else:
            ge_params += build_flag(key, value)

    suite_name = config['benchmark']['suite_name']
    ge_params += ["--dataset_train", f'{suite_name}/{task}/Train.txt']
    ge_params += ["--dataset_test", f'{suite_name}/{task}/Test.txt']

    match config['grammar']['type']:
        case 'default' | 'ponyge' | 'llm':
            ge_params += ['--grammar_file', f'progsys/{suite_name}_{config['grammar']['type']}/{task}.bnf']
        case 'custom':
            ge_params += ['--grammar_file', config['grammar']['grammar_file']]
        case _:
            raise ValueError('Invalid grammar type')

    ge_params += ['--embed_file', f'progsys/{suite_name}_embed_files/{task}-Embed.txt']
    ge_params += ['--fitness_function', 'progsys']
    ge_params += ['--silent']
    
    return ge_params


def save_to_file(config: dict, save_dir: str) -> None:
    os.makedirs(save_dir, exist_ok=True)
    with open(f'{save_dir}/Config.json', 'w') as f:
        json.dump(config, f, indent=4)