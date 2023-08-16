import tiktoken
import os
import shutil
import pandas as pd

encoder = tiktoken.encoding_for_model("gpt-4")
token_length = 0

data = {}

# Iterate all files in "data" folder recursively
for root, dirs, files in os.walk("data"):
    for name in files:
        # Get the file path
        file_path = os.path.join(root, name)

        suffix = name.split(".")[-1]
        if suffix not in ["py", "md", "txt", "csv"]:
            print("Skip: " + file_path)
            continue

        # Read the file as a string
        with open(file_path, "r") as file:
            text = file.read()
            length = len(encoder.encode(text))
            data[file_path] = length
            token_length += length


print("Total token length:", token_length)
df = pd.DataFrame(data.items(), columns=["file", "tokens"])
df["suffix"] = df["file"].apply(lambda x: x.split(".")[-1])
df.to_csv("token_length.csv", index=False)