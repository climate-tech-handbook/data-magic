# import sys, os

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from app.api.routes import api_bp
from app.api.routes_fileapi import fileapi_bp
from dotenv import load_dotenv
from utils.utils import get_env_vars, create_generator
from utils.generator_utils import edit_file
from utils.get_file_path import get_file_path

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(fileapi_bp)

yml_files = ["data/prompts/prompts.yml"]
csv_files = ["data/csv/file_info.csv"]
template_mds = ["data/templates/template.md"]
output_dir = "leif_test"

Climate_Tech_Handbook = None  # initialize as None


async def create_file():
    global Climate_Tech_Handbook  # access the global variable
    Climate_Tech_Handbook = create_generator(
        yml_files, csv_files, template_mds, output_dir
    )


# @app.route("/edit_file", methods=["POST"])
# async def edit_file_endpoint():
#     # get the file path and markdown content from the request data
#     data = request.get_json()
#     file_path = data["file_path"]
#     markdown = data["markdown"]
#     start_line = data.get("start_line")
#     end_line = data.get("end_line")

#     # call the edit_file function
#     edit_file(file_path, markdown, start_line, end_line)

#     # generate and write output
#     output = await Climate_Tech_Handbook.create_output(file_path)
#     await Climate_Tech_Handbook.write_output(file_path, output)

#     # return a response indicating success
#     return jsonify({"message": "File edited successfully"})


# @app.route("/add_tags", methods=["POST"])
# def add_tags_endpoint():
#     # get the file path and tags from the request data
#     data = request.get_json()
#     # file_path = data['file_path']
#     tags = data["tags"]

#     # print the file path for debugging purposes
#     # print("file path:", file_path)
#     # import os
#     file_path = os.path.join(
#         os.getcwd(), "app", "output", "solution-abandoned-farmland-restoration.md"
#     )
#     print("file path:", file_path)

#     # call the add_tags method
#     generator = create_generator(yml_files, csv_files, template_mds, output_dir)
#     generator.add_tags(file_path, tags)

#     # return a response indicating success
#     return jsonify({"message": "Tags added successfully"})


# @app.route("/insert_image", methods=["POST"])
# def insert_image_endpoint():
#     # get the file path, image path, caption, and position from the request data
#     data = request.get_json()
#     file_path = data["file_path"]
#     image_path = data["image_path"]
#     caption = data["caption"]
#     position = data["position"]

#     # call the insert_image function
#     global Climate_Tech_Handbook  # access the global variable
#     Climate_Tech_Handbook.insert_image(file_path, image_path, caption, position)

#     # return a response indicating success
#     return jsonify({"message": "Image inserted successfully"})


# @app.route("/add_section", methods=["POST"])
# def add_section_endpoint():
#     # get the file path, header text, and position from the request data
#     data = request.get_json()
#     file_path = data["file_path"]
#     header_text = data["header_text"]
#     position = data["position"]

#     # call the add_section function
#     global Climate_Tech_Handbook  # access the global variable
#     Climate_Tech_Handbook.add_section(file_path, header_text, position)

#     # return a response indicating success
#     return jsonify({"message": "Section added successfully"})


if __name__ == "__main__":
    create_file()
    app.run(debug=True)


# import pdb
# import sys, os
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from flask import Flask
# from app.api.routes import api_bp

# from dotenv import load_dotenv
# from utils.utils import get_env_vars, create_generator

# load_dotenv()

# app = Flask(__name__)
# app.register_blueprint(api_bp)

# yml_files = ["data/prompts/prompts.yml"]
# csv_files = ["data/csv/file_info.csv"]
# template_mds = ["data/templates/template.md"]
# output_dir = "output_test"

# Climate_Tech_Handbook = create_generator(yml_files, csv_files, template_mds, output_dir)


# @app.before_first_request
# async def create_file():
#     # for page in Climate_Tech_Handbook.file_info:
#     page = Climate_Tech_Handbook.file_info[0]
#     print(f"Page: {page}")
#     output = await Climate_Tech_Handbook.create_output(page)
#     print(f"Output: {output}")
#     await Climate_Tech_Handbook.write_output(page, output)


# if __name__ == "__main__":
#     app.run()
