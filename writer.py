from gpt_api import get_llm

from termcolor import colored
from collections import defaultdict
import random
import tiktoken
import re
import pdb

#%% Arguments and variables
topic = "How to roasting coffee"
topic_info = """We are the Opti Coffee Roasting Company.

Opti Coffee is a coffee roasting company based in Seattle, Washington.
We are passionate about sourcing, roasting, and serving the finest coffee
from around the world.

Our company was founded in 2010 by two coffee enthusiasts, Jake and Mia, who
met at a barista competition and decided to pursue their dream of creating
their own coffee brand. They started with a small roastery in their garage,
where they experimented with different beans, roasts, and blends.
Soon, they gained a loyal following of local customers who appreciated their
craft and quality.
"""
# base_model = "gpt-35-turbo"
base_model = "gpt-4"

outfile_name = open(f"{topic}.txt", "w")

#%% Global variables
api = get_llm()

ENCODER = tiktoken.encoding_for_model(base_model.replace("35", "3.5"))
max_token_len = 4000 if base_model.find("4") >= 0 else 2000

OUTLINE = "Here is the current outline:\n"
LEVELS = 3    # number of levels in the outline
SYSTEM_MSG = f"""You are an AI assistant that writes documents about `{topic}`.

You should write the document for us:

{topic_info}
"""

DETAILS = defaultdict(str)    # section number -> material
SEC_TITLES = defaultdict(str)    # section number -> title
messages = [("system", SYSTEM_MSG)]

# %% Helper functions
random.seed(1)    # we must set the seed to use cache


def generate_prompt(sec_num: str, sec_title: str) -> str:
    suffix = ""
    if sec_num.split(".") != LEVELS - 1:
        suffix = ("\n\n-------\n\n"
                  "This section is NOT at the lowest level. "
                  "So, you only need to write summaries "
                  "for this whole section, "
                  "and the details of the subsections will be generated "
                  "in the future.")
    suffix += "\n\n------- Write -------\n\n"
    suffix += f"{sec_num} {sec_title}\n\n"
    return (f"Now, write {max_token_len//2} words for the Section "
            f"{sec_num} {sec_title}. ") + suffix


def get_prompt(curr_sec_num: str, curr_sec_title: str) -> (str, list):
    """Return the prompt and the list of previous messages.

    Args:
        curr_sec_num: the current section number, such as "1.2.3"
    """
    global DETAILS, LEVELS, SEC_TITLES

    _history = []
    for sec_num in DETAILS.keys():
        _history += [("user", generate_prompt(sec_num, SEC_TITLES[sec_num])),
                     ("assistant", DETAILS[sec_num])]

    messages = [("system", SYSTEM_MSG + OUTLINE)] + _history

    token_length = sum([len(ENCODER.encode(msg[1])) for msg in messages])

    while token_length > max_token_len:
        # Remove two messages, user and assistant
        messages.pop(1)
        messages.pop(1)
        token_length = sum([len(ENCODER.encode(msg[1])) for msg in messages])

        assert messages[0][0] == "system", ("System message is not in the "
                                            "prompt, which might because the "
                                            "outline is too long.")

    return generate_prompt(curr_sec_num, curr_sec_title), messages


def add_writing_to_details(writing: str) -> None:
    """Add LLM's writing to the details.

    Even if sometimes we only ask GPT to write one small section. Sometimes,
    it will generate a few sections all at once.
    """

    # I gave up using regular expression, as it is getting too complex
    _EOC = "<End of Content>"
    writing += f"\n{_EOC}\n"

    curr_sec_num = None
    curr_content = ""
    for line in writing.split("\n"):
        match = re.findall(r"^((\d+\.)*\d) (.+)", line)
        this_line_is_sec_title = False
        if match:
            match = match[0]
            match = [v.strip().rstrip() for v in match]
            this_line_is_sec_title = SEC_TITLES[match[0]] == match[-1]
        else:
            this_line_is_sec_title = False

        if this_line_is_sec_title or line == _EOC:
            if curr_sec_num and curr_content:
                DETAILS[curr_sec_num] = curr_content
            curr_sec_num = match[0] if match else None
            curr_content = ""
        curr_content += line + "\n"


def deeper_outline(outline: str) -> str:
    """Request LLM to write the outline with one level deeper."""
    raise NotImplementedError


#%% Step 1: Generate the outline for the paper
prompt = f"""Now, generate the outline for the paper.

Use the format with markdown, such as:
```markdown
1 Introduction
1.1 Motivation
1.2 Purpose
...
2 Related Work
2.1 ...
...
10 Conclusion
```

Note that you need to generate {LEVELS} levels of sections,
such as Section {".".join(str(random.randint(1, 5)) for _ in range(LEVELS))}.
"""

reply = api.reply(agent_name="user",
                  msg=prompt,
                  num_response=1,
                  stop=None,
                  model=base_model,
                  prev_msgs=messages,
                  temperature=0,
                  top_p=1)

OUTLINE += re.findall("```markdown\n(.*)```", reply[0], re.DOTALL)[0]

open("outline.txt", "w").write(OUTLINE)

print("The outline is:")
print(OUTLINE)

#%% Step 2: Generate the key points for each section
sections = re.findall(r"^((\d+\.)*\d) (.+)", OUTLINE, re.MULTILINE)



SEC_TITLES = {
    sec_num.rstrip().strip(): sec_title.strip().rstrip()
    for sec_num, _, sec_title in sections
}


print("The sections are:")
print(*SEC_TITLES)
del sections
# input("Press enter if you want to continue:")

for sec_num, sec_title in SEC_TITLES.items():
    if sec_num in DETAILS:
        continue

    prompt, messages = get_prompt(sec_num, sec_title)
    reply = api.reply(agent_name="user",
                      msg=prompt,
                      num_response=1,
                      stop=None,
                      model=base_model,
                      prev_msgs=messages,
                      temperature=0,
                      top_p=1,
                      max_tokens=10000)
    reply = reply[0]
    print(colored(f"Section {sec_num} {sec_title}:", "green"), f"\n{reply}")

    add_writing_to_details(prompt + "\n" + reply)

    outfile_name.write(f"Section {sec_num} {sec_title}\n{reply}")
    outfile_name.flush()
    pdb.set_trace()

# Finally, writing to the disk
f = open(f"{topic}.md", "w")
f.write(f"{topic}\n\nTable of Content:\n\n{OUTLINE}\n\n\n\n")
for sec_num in sorted(DETAILS.keys()):
    f.write(DETAILS[sec_num] + "\n\n")
