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

def main():
    diff = get_command("git diff")
    prompt=[
        {"role": "system", "content": """
                You are a bot that generates git commit messages that are succinct and descriptive, only based on the output git diff.
            """
        },
        {
            "role": "user",
            "content": """
                You will next be given the output of git diff.
                You should not be exhaustive, and only describe what seems to matter in the diff.
                Your message should be context-aware but only focus on what was added or removed.
                The message should be about what the change is primarily doing.
                The message should not focus too much on what is changed but explain the intent behind the change.
                Keep the headline short and don't write on multiple lines.
            """
        },
        {"role": "user", "content": f"""
            Here is the output of git diff: ```{diff}```
            Come up with a helpful commit message and don't mention the file names in the commit message.
            """
        }
    ]
    commit_message = complete_chat(prompt)
    print(diff)
    print("\n-----------------\n")
    print(commit_message)
    log_event({"diff": diff, "message": commit_message})

if __name__ == '__main__':
    config = dotenv_values(".env")
    openai.api_key = config["OPENAI_API_KEY"]
    main()