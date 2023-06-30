# Content Generation Pipeline
###### assisting static site generation by engineering prompts to LLMs, assisted with external data for accuracy and solution-specific information.

### Installation and Use

Clone the parent repo:
```
git clone git@github.com:climate-tech-handbook/data-magic.git
```

Move into the repo directory and checkout the appropriate branch:
```
cd data-magic/
git checkout content-pipeline-research
cd pipeline/
```

Create a new .env file to store API keys:
```
OPENAI_API_KEY = your_key_here
```

Create a new virtual environment and install required dependencies:
```
python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

You should now be able to successfully start and run the jupyter notebook:
```
jupyter notebook
```
