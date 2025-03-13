import os
import json


def create_json(programs_folder, grammars_folder, descriptions_folder, output_file):
    program_files = sorted([f for f in os.listdir(programs_folder) if f.startswith('p_')])
    grammar_files = sorted([f for f in os.listdir(grammars_folder) if f.startswith('G_')])
    description_files = sorted([f for f in os.listdir(descriptions_folder) if f.startswith('d_')])

    assert len(program_files) == len(grammar_files)
    assert len(grammar_files) == len(description_files)

    problems = []
    
    for program_file, grammar_file, description_file in zip(program_files, grammar_files, description_files):
        with open(os.path.join(programs_folder, program_file), 'r') as pf:
            program_content = pf.read()

        with open(os.path.join(grammars_folder, grammar_file), 'r') as gf:
            grammar_content = gf.read()

        with open(os.path.join(descriptions_folder, description_file), 'r') as df:
            description_content = df.read()

        problem_entry = {
            "description": description_content,
            "program": program_content,
            "desired_minimal_grammar": grammar_content
        }
        problems.append(problem_entry)

    json_data = {"problems": problems}

    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"JSON file created successfully: {output_file}")


if __name__ == '__main__':
    create_json('llm_inputs/programs', 'llm_inputs/grammars', 'llm_inputs/descriptions', 'llm_inputs/problems.json')
