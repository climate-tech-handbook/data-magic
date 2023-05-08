# from loader import requests
import os
from models.content_generator import ContentGenerator

# Fetch an image from Unsplash based on the topic
# def fetch_unsplash_image(topic):
#     response = requests.get(
#         f"https://api.unsplash.com/search/photos?query={topic}&client_id={unsplash_access_key}"
#     )
#     data = response.json()
#     if data["results"]:
#         return (
#             data["results"][0]["urls"]["regular"],
#             data["results"][0]["user"]["links"]["html"],
#         )
#     else:
#         return None, None


def get_env_vars(*keys, exit_on_missing=True):
    env_vars = []
    missing_vars = []
    for key in keys:
        value = os.getenv(key)
        if value is None:
            if key == "OPENAI_SECRET_KEY":
                print(
                    "Error: OPENAI_SECRET_KEY environment variable is not set. OpenAI key is needed to run this class."
                )
                exit(1)
            else:
                print(
                    f"Note: {key} unset. If you plan to interact with any necessary services related to this key, you will be unable."
                )
                missing_vars.append(key)
        env_vars = value

    if missing_vars and exit_on_missing:
        print("Exiting due to missing environment variables.")
        exit(1)

    return env_vars


def create_generator(yml_files, csv_files, template_mds, output_dir):
    api_key = get_env_vars("OPENAI_SECRET_KEY")

    content_generator = ContentGenerator(
        api_key,
        yml_files=yml_files,
        csv_files=csv_files,
        template_mds=template_mds,
        output_dir=output_dir,
    )
    return content_generator
