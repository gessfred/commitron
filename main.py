import subprocess
import openai
import json
from dotenv import dotenv_values

def get_command(command):
    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error executing command: {e}")
        return None

def log_event(event):
    with open("log.jsonl", "a") as fd:
        fd.write(json.dumps(event) + ",\n")

def complete_chat(chat):    
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat
    )
    return res["choices"][0]["message"]["content"]


#openai.organization = "YOUR_ORG_ID"
def main():
    config = dotenv_values(".env")
    openai.api_key = config["OPENAI_API_KEY"]

    status = get_command('git status')

    diff = get_command("git diff")
    log = get_command("git log --oneline")
    codebase = get_command("cat main.py")
    prompt=[
        {"role": "user", "content": """
            You are a bot that generates git commit messages that are succinct and descriptive, only based on git output.
            You should not be exhaustive, and only describe what seems to matter in the diff. 
            Try to guess what the change is primarily doing.
            For example if the diff contains a configuration change but also a new feature, focus on the feature.
            However if there is only a configuration change, then you can mention it in the commit message.
            Also don't just say what is changed but try to understand why.
            Don't mention the file names in the commit message.
            Try to keep the headline short. You can generate a multiline commit message if (and only if) needed.
        """},
        {"role": "user", "content": f"""
            First, here is the full content of file(s) that were updated {codebase}
            Here is the output of git diff: ```{diff}```
            Here is the current git log: {log}
            Come up with a helpful commit message and don't mention the file name"""}
    ]
    commit_message = complete_chat(prompt)
    print(commit_message)
    log_event({"diff": diff, "message": commit_message})

if __name__ == '__main__':
    main()