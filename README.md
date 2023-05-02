# Data Magic
Scripts and other fun tricks to enhance the site.

## Instructions for `content-generator`

### Setting up your environment

Navigate to the root folder `data-magic`.

Set up your Python environment variable `python3 -m venv env`.

Create a `.env` file and add your OpenAI API Key and UNSPLASH_ACCESS_KEY = like this:

`OPENAI_API_KEY=your_api_key_here`
`UNSPLASH_ACCESS_KEY=your_api_key_here`

Replace `your_api_key_here` with your actual OpenAI API key, which you create from your OpenAI account dashboard.

_Remember to keep your API key private and secure._

Install requirements: `pip install -r requirements.txt`

### Running the script

Navigate to the sub-directory `content-generator`

`cd content-generator`

Run the script: `python3 generate_markdown.py`

_**Uh oh...**_

The script is currently buggy :(

It does the first part correctly, which is to generate markdown `.md` files based on the parameters listed in `file_info.csv`.

But, it doesn't properly replace {Topic} with the `Topic` from `file_info.csv` and doesn't fill out all the sections of the `template.md` with GPT content that is prompted by `prompts.yml`.

---

### What's supposed to happen

1) Page Title, File Name, and Topic (same as Page Title) are populated from `file_info.csv`

2) GPT Prompts are authored in `prompts.yml`

3) The content is generated into Markdown `.md` files based on the structure provided in `template.md`
