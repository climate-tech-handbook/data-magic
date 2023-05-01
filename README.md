# Data Magic
Scripts and other fun tricks to enhance the site.

## Instructions for `content-generator`

### Setting up your environment

Navigate to the root folder `data-magic`.

Set up your Python environment variable `python3 -m venv env`.

Create a `.env` file and add your OpenAI API Key like this:

`OPENAI_API_KEY=your_api_key_here`

Replace `your_api_key_here` with your actual OpenAI API key, which you create from your OpenAI account dashboard.

_Remember to keep your API key private and secure._

Install requirements: `pip install -r requirements.txt`

### Running the script

Navigate to the sub-directory `content-generator`

`cd content-generator`

Run the script: `python3 generate_markdown.py`
