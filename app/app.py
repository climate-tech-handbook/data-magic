import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, current_app,g
from api.routes import api_bp
from api.routes_fileapi import fileapi_bp
from dotenv import load_dotenv
from utils.utils import get_env_vars, create_generator
from utils.generator_utils import edit_file
from utils.get_file_path import get_file_path
from ruamel.yaml import YAML
from io import StringIO
import glob
import logging
load_dotenv()
import json

app = Flask(__name__)
app.register_blueprint(api_bp)

yml_files = ["data/prompts/prompts.yml"]
csv_files = ["data/csv/file_info.csv"]
template_mds = ["data/templates/template.md"]
output_dir = "output_two"


@app.before_first_request
def create_file():
    with app.app_context():
        current_app.Climate_Tech_Handbook= create_generator(yml_files, csv_files, template_mds, output_dir)



@app.route('/edit_file', methods=['POST'])
async def edit_file_endpoint():
    # get the file path and markdown content from the request data
    app.logger.info('/edit_file endpoint called')
    data = request.get_json()
    file_path = data['file_path']
    markdown = data['markdown']
    start_line = data.get('start_line')
    end_line = data.get('end_line')
   
    # call the edit_file function
    edit_file(file_path, markdown, start_line, end_line)
    import pdb; pdb.set_trace()
    with app.app_context():
        output = current_app.Climate_Tech_Handbook.create_output(file_path)
        current_app.Climate_Tech_Handbook.write_output(file_path, output)

    # return a response indicating success
    return jsonify({'message': 'File edited successfully'})




@app.route('/add_tags', methods=['POST'])
def add_tags_endpoint():
    '''
        Adds tags to files in specified directory
        
        Takes in a JSON body the followin paramteres
        {
            file_path: string,
            tags: array of strings
        }
        
        - requires frontmatter already exists
        - does not care if there is a tag property yet
    '''
    # get the directory path and tags from the request data
    app.logger.info('/add_tags endpoint called')
    data = request.get_json()
    directory_path = data['file_path']
    tags = data['tags']

    #formatted_tags = '\n'.join([f"{tag} -" for tag in tags])

    # discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.add_tags(file_path, tags)

    # return a response indicating success
    return jsonify({'message': 'Tags added successfully to all files'})



@app.route('/add_contents', methods=['POST'])
def add_contents_endpoint():
    # Get the file path, YAML front matter, and content from the request data
    app.logger.info('/add_contents endpoint called')
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


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.add_contents(directory_path, yaml_front_matter)

    # Return a response indicating success
    return jsonify({'message': 'Content added successfully to the files'})


@app.route('/add_all_contents', methods=['POST'])
def add_all_contents_endpoint():
    # Get the file path, YAML front matter, and content from the request data
    app.logger.info('/add_all_contents endpoint called')
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


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.add_contents(file_path, yaml_front_matter)
   

    # Return a response indicating success
    return jsonify({'message': 'Content added successfully to the files'})


@app.route('/remove_all_contents', methods=['POST'])
def remove_all_contents_endpoint():
    # Get the directory path from the request data
    app.logger.info('/remove_all_contents endpoint called')
    data = request.get_json()
    directory_path = data['directory_path']

    # Discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.remove_all_contents(file_path)

    # Return a response indicating success
    return jsonify({'message': 'All contents removed successfully from the files'})


@app.route('/insert_image', methods=['POST'])
def insert_image_endpoint():
    # get the file path, image path, caption, and position from the request data
    app.logger.info('/insert_image endpoint called')
    data = request.get_json()
    file_path = data['file_path']
    image_path = data['image_path']
    caption = data['caption']
    position = data['position']


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.insert_image(file_path, image_path, caption, position)

    # return a response indicating success
    return jsonify({'message': 'Image inserted successfully'})


@app.route('/delete_image', methods=['POST'])
def delete_image_endpoint():
    # get the file path, image path, caption, and position from the request data
    app.logger.info('/delete_image endpoint called')
    data = request.get_json()
    file_path = data['file_path']
    image_path = data['image_path']
    caption = data['caption']


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.delete_image(file_path, image_path, caption)


    # return a response indicating success
    return jsonify({'message': 'Image deleted successfully'})




@app.route('/add_section', methods=['POST'])
def add_section_endpoint():
    # get the file path, header text, and position from the request data
    app.logger.info('/add_section endpoint called')
    data = request.get_json()
    file_path = data['file_path']
    header_text = data['header_text']
    position = data['position']


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        generator.add_section(file_path, header_text, position)


    # return a response indicating success
    return jsonify({'message': 'Section added successfully'})

@app.route('/remove_tags', methods=['POST'])
def remove_tags_endpoint():
    # get the directory path and tag_name from the request data
    app.logger.info('/remove_tags endpoint called')
    data = request.get_json()
    directory_path = data['file_path']
    tag_name = data['tag_name']

    # discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))


    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.remove_tags(file_path, tag_name)

    # return a response indicating success
    return jsonify({'message': 'Tags removed successfully from all files'})

@app.route('/update_title', methods=['POST'])
def update_titl_endpoint():
    # Get the file path, YAML front matter, and content from the request data
    app.logger.info('/update_title endpoint called')
    data = request.get_json()
    directory_path = data['directory_path']


    # Call the update_title_position method for each file
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.update_title_position(file_path)

    # Return a response indicating success
    return jsonify({'message': 'Content added successfully to the files'})


@app.route('/update_yaml_front_matter', methods=['POST'])
def update_yaml_front_matter_endpoint(): # update author and tags to correct format
    # Get the directory path from the request data
    app.logger.info('/update_yaml_front_matter endpoint called')
    data = request.get_json()
    directory_path = data['directory_path']

    # Discover all Markdown files in the directory
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    # Loop through the file paths and update the YAML front matter
    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            generator.update_yaml_front_matter(file_path)
  
    # Return a response indicating success
    return jsonify({'message': 'YAML front matter updated successfully for all files.'})


@app.route('/delete_front_matter', methods=['POST'])
def delete_front_matter_endpoint():
    '''
        Clears yaml frontmatter from files in specified directory
        
        Takes in a JSON body the followin paramteres
        {
            file_path: string,
            delete_title: boolean (Optional - True by default)
        }
        When delete_title is set to false, all front matter but the title is deleted
    '''
    # Get the file path from the request data
    app.logger.info('/delete_front_matter endpoint called')
    data = request.get_json()
    directory_path = data['file_path']
    delete_title = True
    if 'delete_title' in data:
        if isinstance(data['delete_title'] , bool):
            delete_title = data['delete_title']
        elif isinstance(data['delete_title'] , str):
            delete_title = json.loads(data['delete_title'].lower())
        else:
            return jsonify({'error': 'delete_title field must be of type bool or string'})
            
        

    # Remove the YAML front matter block from the file
    app.logger.info('delete title set to: ' + str(delete_title))
    
    file_paths = glob.glob(os.path.join(directory_path, '*.md'))

    with app.app_context():
        generator = current_app.Climate_Tech_Handbook
        for file_path in file_paths:
            if delete_title:
                generator.remove_yaml_front_matter(file_path)
            else:
                generator.delete_fields_except_title(file_path)
                


    # Return a response indicating success
    return jsonify({'message': 'YAML front matter removed successfully'})


if __name__ == "__main__":
    app.run(debug=True)