import csv
import os
import requests
import yaml
import openai
import pdb


def save_progress(progress):
    with open("progress.txt", "w") as f:
        f.write(str(progress))


def load_progress():
    try:
        with open("progress.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def list_models():
    models = openai.Model.list()
    print(models.data)


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
    api_key, prompt, engine, temp, max_tokens, n, stop, freq_pen, pres_pen
):
    openai.api_key = api_key

    # Create a chat message with the prompt
    messages = [
        {
            "role": "system",
            "content": "You will be answering multiple prompts set by the stop paramater.",
        },
        {"role": "user", "content": prompt},
    ]

    try:
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=messages,
            max_tokens=max_tokens,
            n=n,
            stop="\n---\n",
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating completion: {e}")
        return None


def validate_and_assign(content_generator, prompts, file_info, templates):
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

    if templates is not None:
        content_generator.templates = templates
    else:
        raise FileNotFoundError(
            f"Could not load template from '{content_generator.template_md}'"
        )


def generate_content(generator, prompt):
    if generator.request_count < generator.max_requests:
        completion = generator.create_completion(prompt)
        generator.request_count += 1
        return completion
    else:
        print(f"Max requests reached. No more content will be generated.")
        return "", "", "", ""


async def generate_output(generator, page):
    separator = "\n---\n"
    combined_prompt = separator.join(
        [
            generator.prompts["Progress Made"]["prompt"].replace(
                "{Topic}", page["Topic"]
            ),
            generator.prompts["Lessons Learned"]["prompt"].replace(
                "{Topic}", page["Topic"]
            ),
            generator.prompts["Challenges Ahead"]["prompt"].replace(
                "{Topic}", page["Topic"]
            ),
            generator.prompts["Best Path Forward"]["prompt"].replace(
                "{Topic}", page["Topic"]
            ),
        ]
    )

    completion = generate_content(generator, combined_prompt)
    print(completion)
    combined_completion = completion.strip()

    (
        progress_made,
        lessons_learned,
        challenges_ahead,
        best_path_forward,
    ) = combined_completion.split(separator)

    template_name = page.get(
        "Template", "template"
    )  # Use default template if not specified
    output = generator.templates[template_name].format(
        topic=page["Topic"],
        progress_made=progress_made.strip(),
        lessons_learned=lessons_learned.strip(),
        challenges_ahead=challenges_ahead.strip(),
        best_path_forward=best_path_forward.strip(),
    )

    return output
