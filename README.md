# Data Magic (OpenAI Utility API)

This project provides an API for generating content using OpenAI's completion models. It includes a `ContentGenerator` class, utility functions, and a simple Flask app to generate content based on prompts, templates, and other configurations.

## Current Goals

### 1. API Development

- Expand the API to handle HTTP requests, allowing users to interact with the content generation features using tools like Postman, Thunder Client, etc.
- Implement various API endpoints for different content generation operations, such as creating, updating, and deleting content.

### 2. CLI Commands

- Develop CLI commands to create content locally while the Flask app is running, providing a more convenient way to interact with the content generation features.

### 3. Error Handling

- Implement robust error handling throughout the application to provide helpful feedback to users and ensure the stability of the system.

### 4. Advanced File Editing

- Add advanced file editing capabilities, such as inserting, replacing, and removing content from existing files and directories.

### 5. Improved Prompts

- Design better prompts for content generation to enhance the quality and relevance of the generated content.

### 6. Enhanced Templates

- Create more sophisticated templates for various content types and use cases, providing users with greater flexibility in customizing their generated content.

### 7. Unsplash Integration

- Integrate Unsplash functionality into the templates, allowing users to include relevant images in their generated content.

## Future Plans

### 1. Integration of Additional OpenAI Services

- Integrate more of OpenAI's services into the tool, such as DALL-E, Whisper, Fine-Tuning, etc., to create even more advanced tooling and markdown content.

### 2. RSS Bridge for Climate Data Fine-Tuning

- Develop a unique RSS bridge to collect and process climate data, which will be used for fine-tuning the AI model and enhancing the quality and relevance of the generated content.

### 3. Climate Tech Chatbot

- Use the resource database and RSS bridge, along with fine-tuning, to create the "Climate Tech Chatbot," a tool designed to provide users with valuable insights and information on climate technologies and trends.

## Installation

1. Clone this repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required packages using `pip install -r requirements.txt`.

## Setting and Using the OpenAI API Key

To use the generator, you will need an OpenAI API key. Follow these steps to set and use the `OPENAI_SECRET_KEY`:

1. Obtain your OpenAI API key from the [OpenAI Dashboard](https://beta.openai.com/signup/).
2. Create a `.env` file in the root directory of your project (if it doesn't already exist).
3. Add your OpenAI API key to the `.env` file in the following format:

`OPENAI_SECRET_KEY=your_api_key_here`

Replace `your_api_key_here` with the actual key you obtained from OpenAI.

**For Unsplash photos**

Add this to your .env as well:

`UNSPLASH_ACCESS_KEY=your_api_key_here`


4. In your Python code, you can use the `dotenv` library to load the API key from the `.env` file:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_SECRET_KEY")
```

### Running the Flask App

1. Run the Flask app by executing `flask run` or try `python app.py` if struggling, but you should make sure flask is installed.
2. The app will create a file for a specific topic using the prompts, templates, and configurations provided in the `data` folder.
   - At this moment in the app it's being forced with a `@before_request` decorator, this will be improved upon in the future.
3. The generated file will be saved in the `output_test` folder.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

If you are lost on how to start contributing or don't understand how a certain class or file works, try checking the wiki first!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

This README provides an overview of the project, installation instructions, usage examples, and contribution guidelines. You can customize the content as needed to better suit your project.

## Acknowledgments

This project is in active development and is currently in an MVP stage, stay tuned to see how it grows!

<!-- Insert additional acks -->
