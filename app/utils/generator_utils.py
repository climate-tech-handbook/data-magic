from loader import requests, csv, yaml, os, openai


# save the current progress in the "progress.txt" file and continue from the last saved progress
# when run the script again,
def save_progress(progress):
    with open("progress.txt", "w") as f:
        f.write(str(progress))


def load_progress():
    try:
        with open("progress.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def stage_content(
    yml_file,
    csv_file,
    template_md,
    output_dir,
):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except FileExistsError:
        return 0
    try:
        with open(yml_file) as f:
            prompts = yaml.safe_load(f)
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
        file_info = [row for row in reader]
        with open(template_md) as f:
            template = f.read()
        return prompts, file_info, template
    except FileNotFoundError:
        return 0


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
