# The following is a skeleton file. Please refer to README.md for more information.


def construct_prompt(description: str):
    pass


def prompt_llm(prompt: str, api_key: str):
    pass


def parse_output(llm_output: str):
    pass


def generate_grammar(description: str, api_key: str, output_file: str, retries: int = 3):
    # Ensure output_file is in BNF format
    prompt = construct_prompt(description)
    llm_output = prompt(prompt, api_key)
    while retries > 0:
        grammar = parse_output(llm_output)
        if grammar:
            break
        retries -= 1

    with open(output_file, 'w') as file:
        file.write(grammar)
