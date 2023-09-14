"""Generate exploration problem set (Chat history).
Find a file, write a question, and create a path"""
import os
import sys
import random
import pdb
import re
from typing import List
import json
from termcolor import colored

sys.path.append(os.path.join(os.path.dirname(__file__), '../SPM'))

from gpt_api import get_llm

MODEL_NAME = "gpt-35-turbo"
MAX_COMMAND_STEPS = 100


def _random_file(root: str, suffix: list, ignore_regex: list) -> str:
    # Initialize an empty list to store the filenames that
    # match the suffix criteria
    matching_files = []

    # Traverse through the directory tree starting from the root
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            # Check if the file has one of the defined suffixes
            if any(filename.endswith(s) for s in suffix):
                # The file extension matches one of the suffixes
                fname = os.path.join(dirpath, filename)
                if any(re.search(regex, fname) for regex in ignore_regex):
                    # The file name matches one of the ignore regexes
                    continue
                # Append the full path of the file to the list
                matching_files.append(fname)

    # Randomly select a file from the list of matching files
    return random.choice(matching_files) if matching_files else None


def _random_block(filename: str, n_max_words: int) -> str:
    """
    Given a large file, return a random chunk of text (split by lines) 
    containing up to n_max_words words.
    
    Parameters:
        filename (str): The path to the file from which to read.
        n_max_words (int): The maximum number of words that the random block of 
            text should contain.
        
    Returns:
        str: A string containing the random block of text from the file.
    """
    # Initialize an empty list to store all lines from the file
    all_lines = []

    # Read all lines from the file and store them in the list
    with open(filename, 'r') as f:
        all_lines = f.readlines()

    # If the file is empty or contains no lines, return an empty string
    if not all_lines:
        return ""

    # Randomly choose a starting line index
    start_idx = random.randint(0, len(all_lines) - 1)

    # Initialize variables to keep track of the number of words and the
    # selected lines
    n_words = 0
    selected_lines = []

    # Loop to collect lines until n_max_words is reached or the end of
    # the file is reached
    for line in all_lines[start_idx:]:
        line_words = line.split()
        n_words += len(line_words)

        if n_words > n_max_words:
            break

        selected_lines.append(line)

    return ''.join(selected_lines)


def norm_path(filename):
    # Check if the string contains any non-alphanumeric characters
    if any(not ch.isalnum() and ch not in [".", "_", "-", "/"] for ch in filename):
        return f'"{filename}"'
    return filename


def unnorm_path(filename):
    if filename[0] in ["\'", "\""] and filename[0] == filename[-1]:
        return unnorm_path(filename[1:-1])
    return filename


def commands_to_reach_destination(start: str,
                                  destination: str,
                                  folder_find_acc: float = 0.8) -> List[str]:
    """Use Linux's "ls", "cd", and "cat command to explore the path, 
    from `start` to the `destination`.

    Note that you are unfamiliar with the path, so you may need to "ls" to see
    the content inside a folder.

    It is guaranteed that the start and destination exist. 

    Args:
        start (str): a path
        destination (str): filename, a file which we want to find. 
        folder_find_acc (float, optional): the probability of finding a 
            correct folder. Defaults to 0.8.

    Returns:
        commands (list): a list of commands
    """
    assert os.path.isdir(start)
    assert os.path.isfile(destination)

    # Initialize an empty list to store the commands
    commands = []

    curr = start
    while True:
        commands.append("ls")

        # List the contents in the current directory
        contents = os.listdir(curr)

        # Separate the contents into files and folders
        files = [f for f in contents if os.path.isfile(os.path.join(curr, f))]
        folders = [f for f in contents if os.path.isdir(os.path.join(curr, f))]

        # Roll a dice to find the correct file
        if os.path.realpath(destination) in [
                os.path.realpath(os.path.join(curr, fname)) for fname in files
        ]:
            correct_command = f"cat {norm_path(os.path.basename(destination))}"
        else:
            # If we haven't found the file, we should try folders
            correct_path = os.path.relpath(destination, curr)
            cd_to = correct_path.split('/')[0]
            correct_command = f"cd {norm_path(cd_to)}"

        # List all possible actions
        all_possible_commands = [
            f"cat {norm_path(os.path.basename(fname))}" for fname in files
        ] + [f"cd {norm_path(os.path.basename(folder))}" for folder in folders]
        if curr != start:
            all_possible_commands += ["cd .."]

        if random.random() <= folder_find_acc:
            commands.append(correct_command)
        else:
            commands.append(random.choice(all_possible_commands))

        if commands[-1].startswith("cd "):
            dirname = unnorm_path(commands[-1][3:])
            curr = os.path.join(curr,  dirname)
            curr = os.path.realpath(curr)
        else:
            cat_fname = unnorm_path(commands[-1].split()[-1])
            if os.path.realpath(os.path.join(
                    curr, cat_fname)) == os.path.realpath(destination):
                break

        if len(commands) > MAX_COMMAND_STEPS:
            raise RuntimeError("Too many commands")

    # Remove redundant "ls" command.
    # iterate through the commands, we don't need two adjacent "ls" commands,
    # even if there are some "cat" inside.
    rst = []
    need_ls = True
    for cmd in commands:
        if cmd.startswith("ls"):
            if need_ls:
                rst.append(cmd)
                need_ls = False
        else:
            rst.append(cmd)
            if cmd.startswith("cd"):
                need_ls = True

    print(colored(destination, "green"))
    print(commands)

    return commands


def optimal_path(start: str, destination: str) -> List[str]:
    """Use Linux's "ls", "cd", and "cat command to explore the path, 
    from `start` to the `destination`.

    Note that you are unfamiliar with the path, so you may need to "ls" to see
    the content inside a folder.

    It is guaranteed that the start and destination exist. 

    Args:
        start (str): a path
        destination (str): filename, a file which we want to find. 
        folder_find_acc (float, optional): the probability of finding a 
            correct folder. Defaults to 0.8.

    Returns:
        commands (list): a list of commands
    """
    assert os.path.isdir(start)
    assert os.path.isfile(destination)

    # folders = os.path.relpath(destination, start).split("/")
    # commands = []
    # for dirname in folders[:-1]:
    #     commands += ["ls", f"cd {dirname}"]
    # commands += ["ls", f"cat {folders[-1]}"]

    folders = os.path.relpath(destination, start).split("/")
    commands = [
        cmd for dirname in folders[:-1] for cmd in ["ls", f"cd {norm_path(dirname)}"]
    ] + ["ls", f"cat {norm_path(folders[-1])}"]

    return commands


def _random_question(root: str, filename: str, block: str) -> str:

    api = get_llm()

    prompt = f"""
I found the following content in the file {filename}.

Now, generate reading comprehension questions and answers based on the content.

Use the format:

QUESTION: a question goes here
ANSWER: the answer to the question goes here

--- Here are the content ---
{block}
"""

    ans = api.reply(agent_name="user", msg=prompt, model=MODEL_NAME)

    pairs = re.findall("QUESTION: (.*?)ANSWER: (.*?)\n", ans[0], re.DOTALL)

    return pairs


def gen(root: str, n_files: int = 10, outname: str = "out.json"):
    rst = []
    for i in range(n_files):
        filename = _random_file(
            root=root,
            suffix=['.txt', ".md", ".py"],
            ignore_regex=[".*out.*", ".*\.git.*", ".*test.*"])
        block = _random_block(filename, 3000)
        pairs = _random_question(root, filename, block)

        optimal = optimal_path(root, filename)  # the optimal path

        for question, answer in pairs:
            try:
                commands = commands_to_reach_destination(root,
                                                         filename,
                                                         folder_find_acc=0.8)
            except Exception as e:
                print(e)
                continue

            print(colored(optimal, "red"))

            rst.append({
                "question": question,
                "answer": answer,
                "commands": commands,
                "optimal_path": optimal,
                "filename": os.path.relpath(filename, root)
            })

    # dump `rst` to json
    with open(outname, "w") as f:
        json.dump(rst, f, indent=2)



if __name__ == "__main__":
    random.seed(1)

    # cmds = commands_to_reach_destination('data/', 'data/solver/src/cafe.py')
    # print(cmds)
    gen("data/", n_files=10, outname="file_search_coffee.json")
