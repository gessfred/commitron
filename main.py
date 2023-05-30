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

def filter_git_diff(output):
    filtered_output = []
    for line in output.splitlines():
        if not line.startswith(('diff', 'old mode', 'new mode')):
            filtered_output.append(line)
    return '\n'.join(filtered_output)

def main():
    diff = get_command("git diff")
    diff = filter_git_diff(diff)
    #py_file = get_command("cat main.py")
    prompt=[
        {"role": "system", "content": """
                You are a bot that automates the generation of helpful git commit messages that are succinct and descriptive
            """
        },
        {
            "role": "user",
            "content": """
                I want you to act as a commit message generator. I will provide you with information about the task and the prefix for the task code, and I would like you to generate an appropriate commit message using the conventional commit format. Do not write any explanations or other words, just reply with the commit message.
            """
        },
        {
            "role": "user",
            "content": f"""
                Output of git diff: {diff}
            """
        }
    ]
    commit_message = complete_chat(prompt)
    print(commit_message)
    log_event({"diff": diff, "message": commit_message})

if __name__ == '__main__':
    config = dotenv_values(".env")
    openai.api_key = config["OPENAI_API_KEY"]
    main()