import subprocess
import os
import openai
from dotenv import load_dotenv, dotenv_values

def get_command(command):
    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error executing command: {e}")
        return None

def complete_chat(chat):    
    res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=chat
    )
    return res["choices"][0]["message"]["content"]

#openai.organization = "YOUR_ORG_ID"
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]
# needed to get git diff git config core.fileMode false

status = get_command('git status')
diff = get_command("git diff")
chat=[
    {"role": "system", "content": """
        You are a bot that generates git commit messages that are succinct and descriptive, only based on git output.
        You should not be exhaustive, and only describe what seems to matter in the diff. Try to guess what the change is mainly doing
        For example if a configuration changes but there is a new feature implemented in the code as well, focus on the feature.
        However if there is only a configuration change in the diff, then you can mention it in the commit message.
    """},
    {"role": "user", "content": f"Here is the output of `git status`: {status}\nAnd here is the output of git diff: ```{diff}```\nCome up with a helpful commit message"}
]

print(complete_chat(chat))