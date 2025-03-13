# Overview

This is the replication package for a paper currently under peer review. The repository contains the implementation and experimental framework for exploring program synthesis using specialized grammars predicted by large language models (LLMs).

# PonyGE2

This software uses [PonyGE2](https://github.com/PonyGE/PonyGE2) as the backbone for performing grammatical evolution. Numerous features have been added and modifications made to the original source code. Changes include:
- A revamped experimental harness for more detailed results. New metrics include average best and overall best fitnesses over several runs, and the standard deviations thereof.
- The ability to compare the performance of different grammars, including superimposed fitness graphs.
- The ability to run an entire program synthesis benchmark suite and aggregate results.
- A list of phenotypes across generations to track changes.
- Fixed bug where loop breaks were not being parsed correctly.
- Added a loop break constant of 200 to all grammars. This should be enough for all training examples in the datasets provided, while not high enough to significantly impact performance.

# Installation

```bash
pip install -r requirements.txt
```

# Running Experiments

The desired experimental parameters must be specified in a configuration file. An example configuration file is provided in `configs/example.json`. Details of how to create a configuration file are provided in the next section.

To run the experiment:
```bash
cd src
python experiment.py --config <path-to-config>
```
For example, to use the example configuration file, you would run:
```bash
python experiment.py --config configs/example.json
```

Results are saved in the `results` folder.

# Configuration

The configuration parameters are designed to mirror the PonyGE2 parameters, as set out in the [wiki](https://github.com/PonyGE/PonyGE2/wiki/Evolutionary-Parameters).

In addition to the PonyGE2 parameters, we add some of our own for running multiple experiments using default and LLM-predicted grammars. These are described in the table below.

| Parameter                 | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `benchmark.type`          | Specifies the benchmark type. Can be either `"single"` (individual problem) or `"suite"` (collection of problems). |
| `benchmark.suite_name`    | The name of the benchmark suite. Currently only supports `"psb1"`.         |
| `benchmark.problem_name`  | The name of the specific problem in the suite. Example: `"Number IO"`. Use `null` if running the whole suite. |
| `comparison`              | Specifies whether to run the experiment using different grammars. Can be either `"grammar"` or `null`. If comparing grammars, the grammars must be specified as a list in the `grammar` parameter. |
| `grammar.type`            | Defines the grammar type. Can be either `"ponyge"` for the out-of-the-box grammars provided by PonyGE, `"default"` for repaired versions of those grammars, `"llm"` for LLM-predicted grammars or `"custom"`.             |
| `grammar.grammar_file`    | Path to a custom grammar file for when `"custom"` is used in `grammar.type`.             |
| `grammar.embed_file`      | Optional path to the embed file, which includes the fitness function. By default, PonyGE's embed files are used. The embed file for the String Differences problem is currently not supported.           |

The PSB1 tasks are listed in `tasks/psb1_tasks.json`. If you wish to run the experiment on a subset of PSB1 tasks, simply modify the file.

# LLM-Predicted Grammars

In-context examples for conditioning the LLM are provided in the `llm_inputs` folder. This contains all example problems in `problems.json`. The dataset provided is of size K=10, in line with the recommendation of [Brown et al](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf) for few-shot learning due to LLM context window sizes. However, should you wish to modify or add more examples, you may do so using the following steps:
1. Add the natural language description as a text file to the `descriptions` folder.
2. Add the desired program as a Python file to the `programs` folder.
3. Add the desired minimal grammar as a BNF file to the `grammars` folder.
4. Run `create_json.py` to regenerate the `problems.json` file with the added or modified examples.

We have provided the LLM-predicted grammars used in the experiments in the `grammars/progsys/psb1_llm` folder. The process for obtaining them is described in Section 3.3 in the paper, and the grammars were generated using the in-context examples in `problems.json` for conditioning the LLM. The prompt template is provided in Figure 2.

To generate new LLM-predicted grammars yourself, you will need to implement the functions in `generate_grammar.py`. In particular, you will need to supply your own API key for your LLM of choice, or run the LLM on your machine.