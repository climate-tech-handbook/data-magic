import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, current_app,g
from api.routes import api_bp
from api.routes_fileapi import fileapi_bp
from dotenv import load_dotenv
from utils.utils import get_env_vars, create_generator
from utils.generator_utils import edit_file
from utils.get_file_path import get_file_path
import pdb,logging
from ruamel.yaml import YAML
from io import StringIO
import glob
load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_bp)

yml_files = ["data/prompts/prompts.yml"]
csv_files = ["data/csv/file_info.csv"]
template_mds = ["data/templates/template.md"]
output_dir = "output_two"

# Climate_Tech_Handbook = None  # initialize as None



@app.before_first_request
def create_file():
    with app.app_context():
        current_app.Climate_Tech_Handbook= create_generator(yml_files, csv_files, template_mds, output_dir)



@app.route('/edit_file', methods=['POST'])
async def edit_file_endpoint():
    # get the file path and markdown content from the request data
    data = request.get_json()
    file_path = data['file_path']
    markdown = data['markdown']
    start_line = data.get('start_line')
    end_line = data.get('end_line')

    # call the edit_file function
    edit_file(file_path, markdown, start_line, end_line)

    # generate and write output
    # output = await Climate_Tech_Handbook.create_output(file_path)
    # await Climate_Tech_Handbook.write_output(file_path, output)
    with app.app_context():
        output = current_app.Climate_Tech_Handbook.create_output(file_path)
        current_app.Climate_Tech_Handbook.write_output(file_path, output)

    # return a response indicating success
    return jsonify({'message': 'File edited successfully'})




@app.route('/add_tags', methods=['POST'])
def add_tags_endpoint():
    # get the directory path and tags from the request data
    data = request.get_json()
    directory_path = data['file_path']
    tags = data['notes_we_will_be_covering']

    formatted_tags = '\n'.join([f"{tag} -" for tag in tags])

    # discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    # # call the add_tags method for each file
    # generator = create_generator(yml_files, csv_files, template_mds, output_dir)
    # for file_path in file_paths:
    #     generator.add_tags(file_path, formatted_tags)
    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.add_tags(file_path, formatted_tags)

    # return a response indicating success
    return jsonify({'message': 'Tags added successfully to all files'})



@app.route('/add_contents', methods=['POST'])
def add_contents_endpoint():
    # Get the file path, YAML front matter, and content from the request data
    data = request.get_json()
    directory_path = data['file_path']
    yaml_front_matter = data['yaml_front_matter']

    # Convert the front matter data to a YAML string
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(sequence=4, offset=2)
    yaml_string = StringIO()
    yaml.dump(yaml_front_matter, yaml_string)
    yaml_front_matter = yaml_string.getvalue()


    # # Call the add_content_to_files method for the specified directory
    # global Climate_Tech_Handbook  # access the global variable
    # # Loop through the file paths and add contents to each file
    # Climate_Tech_Handbook.add_contents(directory_path, yaml_front_matter)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.add_contents(directory_path, yaml_front_matter)

    # Return a response indicating success
    return jsonify({'message': 'Content added successfully to the files'})


@app.route('/add_all_contents', methods=['POST'])
def add_all_contents_endpoint():
    # Get the file path, YAML front matter, and content from the request data
    data = request.get_json()
    directory_path = data['file_path']
    yaml_front_matter = data['yaml_front_matter']

    # Convert the front matter data to a YAML string
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(sequence=4, offset=2)
    yaml_string = StringIO()
    yaml.dump(yaml_front_matter, yaml_string)
    yaml_front_matter = yaml_string.getvalue()

    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    # Call the add_content_to_files method for the specified directory
    # global Climate_Tech_Handbook  # access the global variable
    # # Loop through the file paths and add contents to each file
    # for file_path in file_paths:
    #      Climate_Tech_Handbook.add_contents(file_path, yaml_front_matter)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.add_contents(file_path, yaml_front_matter)
   

    # Return a response indicating success
    return jsonify({'message': 'Content added successfully to the files'})


@app.route('/remove_all_contents', methods=['POST'])
def remove_all_contents_endpoint():
    # Get the directory path from the request data
    data = request.get_json()
    directory_path = data['directory_path']

    # Discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    # global Climate_Tech_Handbook  # access the global variable

    # # Call the remove_all_contents method for each file
    # for file_path in file_paths:
    #      Climate_Tech_Handbook.remove_all_contents(file_path)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.remove_all_contents(file_path)

    # Return a response indicating success
    return jsonify({'message': 'All contents removed successfully from the files'})


@app.route('/insert_image', methods=['POST'])
def insert_image_endpoint():
    # get the file path, image path, caption, and position from the request data
    data = request.get_json()
    file_path = data['file_path']
    image_path = data['image_path']
    caption = data['caption']
    position = data['position']

    # call the insert_image function
    # global Climate_Tech_Handbook  # access the global variable
    # Climate_Tech_Handbook.insert_image(file_path, image_path, caption, position)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.insert_image(file_path, image_path, caption, position)

    # return a response indicating success
    return jsonify({'message': 'Image inserted successfully'})


@app.route('/delete_image', methods=['POST'])
def delete_image_endpoint():
    # get the file path, image path, caption, and position from the request data
    data = request.get_json()
    file_path = data['file_path']
    image_path = data['image_path']
    caption = data['caption']

    # call the delete_image method
    # global Climate_Tech_Handbook  # access the global variable
    # Climate_Tech_Handbook.delete_image(file_path, image_path, caption)


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.delete_image(file_path, image_path, caption)


    # return a response indicating success
    return jsonify({'message': 'Image deleted successfully'})




@app.route('/add_section', methods=['POST'])
def add_section_endpoint():
    # get the file path, header text, and position from the request data
    data = request.get_json()
    file_path = data['file_path']
    header_text = data['header_text']
    position = data['position']

    # call the add_section function
    # global Climate_Tech_Handbook  # access the global variable
    # Climate_Tech_Handbook.add_section(file_path, header_text, position)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.add_section(file_path, header_text, position)


    # return a response indicating success
    return jsonify({'message': 'Section added successfully'})

@app.route('/remove_tags', methods=['POST'])
def remove_tags_endpoint():
    # get the directory path and tag_name from the request data
    data = request.get_json()
    directory_path = data['file_path']
    tag_name = data['tag_name']

    # discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    # call the remove_tags method for each file
    # generator = create_generator(yml_files, csv_files, template_mds, output_dir)
    # for file_path in file_paths:
    #     generator.remove_tags(file_path, tag_name)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.remove_tags(file_path, tag_name)

    # return a response indicating success
    return jsonify({'message': 'Tags removed successfully from all files'})

@app.route('/update_title', methods=['POST'])
def update_titl_endpoint():
    # Get the file path, YAML front matter, and content from the request data
    data = request.get_json()
    directory_path = data['directory_path']


    # Call the update_title_position method for each file
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    # global Climate_Tech_Handbook  # access the global variable
    # for file_path in file_paths:
    #     Climate_Tech_Handbook.update_title_position(file_path)

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.update_title_position(file_path)

    # Return a response indicating success
    return jsonify({'message': 'Content added successfully to the files'})




if __name__ == "__main__":
    app.run(debug=True)