import openai
import os
from dotenv import load_dotenv
import csv
import yaml

load_dotenv()

# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Authenticate with OpenAI API key
openai.api_key = api_key

if not os.path.exists('output'):
    os.makedirs('output')

# Load prompts
with open('prompts.yml') as f:
    prompts = yaml.safe_load(f)

# Load file info
with open('file_info.csv', newline='') as f:
    reader = csv.DictReader(f)
    file_info = [row for row in reader]

# Load template
with open('template.md') as f:
    template = f.read()

# Generate content for a given prompt
def generate_content(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        n = 1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text

# Loop over pages and generate output
for page in file_info:
    # Generate output for current page
    progress_made = generate_content(prompts['Progress Made']['prompt'].replace('{topic}', page['Topic']))
    lessons_learned = generate_content(prompts['Lessons Learned']['prompt'].replace('{topic}', page['Topic']))
    challenges_ahead = generate_content(prompts['Challenges Ahead']['prompt'].replace('{topic}', page['Topic']))
    best_path_forward = generate_content(prompts['Best Path Forward']['prompt'].replace('{topic}', page['Topic']))

    output = template.format(
        topic=page['Topic'],
        progress_made=progress_made,
        lessons_learned=lessons_learned,
        challenges_ahead=challenges_ahead,
        best_path_forward=best_path_forward
    )

    # Write output to file
    with open(f"output/{page['File Name']}", 'w') as f:
        f.write(output)
