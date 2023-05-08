import pdb
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from app.api.routes import api_bp

from dotenv import load_dotenv
from utils.utils import get_env_vars, create_generator

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_bp)

yml_files = ["data/prompts/prompts.yml"]
csv_files = ["data/csv/file_info.csv"]
template_mds = ["data/templates/template.md"]
output_dir = "output_test"

Climate_Tech_Handbook = create_generator(yml_files, csv_files, template_mds, output_dir)


@app.before_first_request
async def create_file():
    # for page in Climate_Tech_Handbook.file_info:
    page = Climate_Tech_Handbook.file_info[3]
    print(f"Page: {page}")
    output = await Climate_Tech_Handbook.create_output(page)
    print(f"Output: {output}")
    await Climate_Tech_Handbook.write_output(page, output)


if __name__ == "__main__":
    app.run()
