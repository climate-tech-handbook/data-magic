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

# Loop over pages and generate output
for page in file_info:
    # Generate output for current page
    output = template.format(
        topic=page['Topic'],
        progress_made=prompts['Progress Made']['text'].replace('{topic}', page['Topic']),
        lessons_learned=prompts['Lessons Learned']['text'].replace('{topic}', page['Topic']),
        challenges_ahead=prompts['Challenges Ahead']['text'].replace('{topic}', page['Topic']),
        best_path_forward=prompts['Best Path Forward']['text'].replace('{topic}', page['Topic'])
    )

    # Write output to file
    with open(f"output/{page['File Name']}", 'w') as f:
        f.write(output)
