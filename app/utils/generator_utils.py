from loader import requests, csv, yaml, os, openai


def save_progress(progress):
    with open("progress.txt", "w") as f:
        f.write(str(progress))


def load_progress():
    try:
        with open("progress.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def stage_content(yml_files, csv_files, template_files, output_dir):
    if not isinstance(yml_files, list):
        yml_files = [yml_files]
    if not isinstance(csv_files, list):
        csv_files = [csv_files]
    if not isinstance(template_files, list):
        template_files = [template_files]

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except FileExistsError:
        return 0

    prompts = {}
    file_info = []
    templates = {}

    for yml_file in yml_files:
        with open(yml_file) as f:
            prompts.update(yaml.safe_load(f))

    for csv_file in csv_files:
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            file_info.extend([row for row in reader])

    for template_file in template_files:
        template_name = os.path.splitext(os.path.basename(template_file))[0]
        with open(template_file) as f:
            templates[template_name] = f.read()

    return prompts, file_info, templates


def generate_completion(
    api_key,
    prompt,
    engine,
    temp,
    max_tokens,
    n,
    stop,
    freq_pen,
    pres_pen,
):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
    )
    completion = response.choices[0].text.strip()
    return completion


def validate_and_assign(content_generator, prompts, file_info, template):
    if prompts is not None:
        content_generator.prompts = prompts
    else:
        raise FileNotFoundError(
            f"Could not load prompts from '{content_generator.yml_file}'"
        )

    if file_info is not None:
        content_generator.file_info = file_info
    else:
        raise FileNotFoundError(
            f"Could not load file info from '{content_generator.csv_file}'"
        )

    if template is not None:
        content_generator.template = template
    else:
        raise FileNotFoundError(
            f"Could not load template from '{content_generator.template_md}'"
        )


def create_output(self, page):
    progress_made = self.generate_content(
        self.prompts["Progress Made"]["prompt"].replace("{Topic}", page["Topic"])
    )
    lessons_learned = self.generate_content(
        self.prompts["Lessons Learned"]["prompt"].replace("{Topic}", page["Topic"])
    )
    challenges_ahead = self.generate_content(
        self.prompts["Challenges Ahead"]["prompt"].replace("{Topic}", page["Topic"])
    )
    best_path_forward = self.generate_content(
        self.prompts["Best Path Forward"]["prompt"].replace("{Topic}", page["Topic"])
    )

    template_name = page.get(
        "Template", "template"
    )  # Use default template if not specified
    output = self.templates[template_name].format(
        topic=page["Topic"],
        progress_made=progress_made,
        lessons_learned=lessons_learned,
        challenges_ahead=challenges_ahead,
        best_path_forward=best_path_forward,
    )

    return output
