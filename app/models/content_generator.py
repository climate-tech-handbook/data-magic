from utils import stage_content, save_progress, load_progress, generate_completion


class ContentGenerator:
    def __init__(
        self,
        api_key,
        yml_file="prompts.yml",
        csv_file="file_info.csv",
        template_md="template.md",
        output_dir="output",
    ):
        self.api_key = api_key
        self.yml_file = yml_file
        self.csv_file = csv_file
        self.template_md = template_md
        self.output_dir = output_dir
        self._initialize()

    def _initialize(self):
        stage_content(
            self.api_key,
            self.yml_file,
            self.csv_file,
            self.template_md,
            self.output_dir,
        )

    def handle_progress(save_or_load, progress=None):
        if save_or_load == "load":
            return load_progress()
        else:
            save_progress(progress)

    def generate_completion(
        self,
        prompt,
        temp=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        freq_pen=0,
        pres_pen=0,
    ):
        return generate_completion(
            self.api_key, prompt, temp, max_tokens, n, stop, freq_pen, pres_pen
        )
