import pdb
from utils.generator_utils import (
    stage_content,
    save_progress,
    load_progress,
    generate_completion,
    validate_and_assign,
    generate_output,
    list_models,
    edit_file,
    add_tags,
    insert_image,
    add_section,
    extract_keys_from_template,
)


class ContentGenerator:
    def __init__(
        self,
        api_key,
        mode="markdown",
        yml_files=["prompts.yml"],
        csv_files=["file_info.csv"],
        template_mds=["template.md"],
        output_dir="output",
        completion_params=None,
        max_requests=1000,
    ):
        self.api_key = api_key
        self.mode = mode
        self.yml_files = yml_files
        self.csv_files = csv_files
        self.template_mds = template_mds
        self.output_dir = output_dir
        self.request_count = 0
        self.max_requests = max_requests
        self.progress = self.handle_progress("load")

        if self.mode == "markdown":
            self._initialize()
        elif self.mode == "completion" and completion_params:
            self.create_completion(**completion_params)

    def _initialize(self):
        prompts, file_info, templates = stage_content(
            self.yml_files,
            self.csv_files,
            self.template_mds,
            self.output_dir,
        )

        validate_and_assign(self, prompts, file_info, templates)

    def handle_progress(self, save_or_load, progress=None):
        if save_or_load == "load":
            return load_progress()
        else:
            save_progress(progress)

    def create_completion(
        self,
        prompt,
        engine="text-davinci-002",
        temp=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        freq_pen=0,
        pres_pen=0,
    ):
        completion = generate_completion(
            self.api_key, prompt, engine, temp, max_tokens, n, stop, freq_pen, pres_pen
        )
        return completion

    async def create_output(self, page):
        output = await generate_output(self, page,self.template_mds[0])
        return output

    async def write_output(self, page, output):
        file_name = f"{self.output_dir}/{page['File Name']}"
        with open(file_name, "w") as f:
            f.write(output)

    def extract_prompt_keys(self, template_name="template"):
        template_path = f"{template_name}"
        return extract_keys_from_template(template_path)

    def prompt_user_for_model_list(self):
        choice = input(
            "Would you like to see a list of available models? (y/n): "
        ).lower()

        if choice == "y":
            list_models()
        elif choice == "n":
            print("Fine then I won't list the models....")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    def edit_file(self, file_path, markdown, start_line=None, end_line=None):
        edit_file(file_path, markdown, start_line, end_line)

    def add_tags(self, file_path, tags):
        add_tags(file_path, tags)

    def insert_image(self, file_path, image_path, caption, position):
        insert_image(file_path, image_path, caption, position)

    def add_section(self, file_path, header_text, position):
        add_section(file_path, header_text, position)
