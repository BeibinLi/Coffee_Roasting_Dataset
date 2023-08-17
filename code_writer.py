import sys
sys.path.append("../SPM/")
from gpt_api import get_llm
from termcolor import colored
from collections import defaultdict
import random
import tiktoken
import re
import pdb
import os

#%% Arguments and variables

# base_model = "gpt-35-turbo"
base_model = "gpt-4-32k"
langauges = [
              # ("c++", ".cpp"),
              ("C#", ".cs"), 
              ("Java", ".java")]

input_folder = "data"
max_tokens = 32000
max_memory_tokens = 20000
max_generation_tokens = 10000

#%% Global variables
api = get_llm()
n_calls = 0

encoder = tiktoken.encoding_for_model(base_model.replace("35", "3.5").replace("-32k", ""))
max_token_len = 4000 if base_model.find("4") >= 0 else 2000

files_written = []

# %%
def rewrite(filename:str, language:str, ext_name:str, memory: list):
    global n_calls
    code = open(filename, "r", encoding="utf-8").read()
    origin_ext = "." + filename.split(".")[-1]
    # out_filename = os.path.basename(filename).replace(origin_ext, ext_name)
    # out_filename = os.path.join(os.path.dirname(filename), ext_name, out_filename)
    # os.makedirs(os.path.dirname(out_filename), exist_ok=True)

    prompt = f"""
Please rewrite the following code ({filename}) into {language}
```
{code}
```
"""
    response = api.reply("user", prompt,
                      num_response=1,
                      stop=None,
                      model=base_model,
                      prev_msgs=memory,
                      temperature=0,
                      top_p=1, max_tokens=max_generation_tokens)
    n_calls += 1
    print("Number of calls:", n_calls)
    r0 = response[0]
    memory.append(("user", prompt))
    memory.append(("assistant", r0))

    match = re.findall(r"OUTPUT_FILENAME:(.+?)\n```(\w*)\n(.*?)\n```", r0, flags=re.DOTALL)
    
    if len(match) == 0 and code.strip().rstrip() != "":
        # maybe, the result is too long.
        pdb.set_trace()

    for out_filename, new_lan, new_code in match:
        out_filename = out_filename.strip().rstrip()
        out_filename = re.findall(f"(\w+\.\w+)", out_filename)[0]

        # Special handling of the folder. 
        # TODO: LLM should give the correct path.
        out_filename = os.path.join(os.path.dirname(filename).replace("/test/", "/"),
                                     ext_name[1:], out_filename)
        files_written.append(out_filename)
        print(colored("Writing: " + out_filename, "green"))
        try:
            os.makedirs(os.path.dirname(out_filename), exist_ok=True)
        except Exception as e:
            print(e)
        open(out_filename, "w", encoding="utf-8").write(new_code)

def pop_memory(memory):
    token_length = 0
    for i, (agent, msg) in enumerate(memory):
        token_length += len(encoder.encode(msg))

        # Remove messages from memory if the token length is too long
        if token_length > max_memory_tokens:
            memory = memory[:i]
            break

#%% Main loop
for language, ext in langauges:
    memory = [("system", f"""You are writing {language} code.
               
For the output, please use the format
OUTPUT_FILENAME: new_filename_goes_here
```language
new code goes here
with detailed comments
```

It is ok to write multiple files (e.g., header, source files, etc). 
You can writer whatever you want, and just give me the results all at once~!
"""), ]

    # Iterate all files in "data" folder recursively
    for root, dirs, files in os.walk(input_folder):
        for name in files:
            # Get the file path
            file_path = os.path.join(root, name)

            suffix = name.split(".")[-1]
            if suffix not in ["py"]:
                print("Skip: " + file_path)
                continue

        # Get the language
            rewrite(file_path, language, ext, memory)
            pop_memory(memory)