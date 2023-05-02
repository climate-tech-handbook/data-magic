from loader import requests, unsplash_access_key


# Fetch an image from Unsplash based on the topic
def fetch_unsplash_image(topic):
    response = requests.get(
        f"https://api.unsplash.com/search/photos?query={topic}&client_id={unsplash_access_key}"
    )
    data = response.json()
    if data["results"]:
        return (
            data["results"][0]["urls"]["regular"],
            data["results"][0]["user"]["links"]["html"],
        )
    else:
        return None, None
