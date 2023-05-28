import subprocess
import os
import openai
from dotenv import load_dotenv, dotenv_values

def run_git_command(command):
    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error executing command: {e}")
        return None
    

#openai.organization = "YOUR_ORG_ID"
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]
# needed to get git diff git config core.fileMode false
res = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
print(res["choices"][0]["message"]["content"])
status = run_git_command('git status')
diff = run_git_command("git diff")
print(diff)