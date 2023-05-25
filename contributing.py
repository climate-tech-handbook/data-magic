# For scraping
import requests

# Using github api, taking 
def get_contributors(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"
    headers = {"Accept": "application/vnd.github.v3+json"}  # Set the API version

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contributors = response.json()
        contributor_names = [contributor["login"] for contributor in contributors]
        return contributor_names
    else:
        print(f"Failed to fetch contributors. Error: {response.status_code}")
        return []


# Provide the repository owner and name
repository_owner = "Repository Owner Name"
repository_name = "Repository Name"

contributor_names = get_contributors(repository_owner, repository_name)
print("Contributors:")
for name in contributor_names:
    print(name)


def write_contributors_to_readme(contributor_names):
    with open("readme.md", "r+") as readme_file:
        lines = readme_file.readlines()

        # Find the index of the "## Contribute" section
        contribute_index = -1
        for i, line in enumerate(lines):
            if line.startswith("## Contribute"):
                contribute_index = i
                break

        # If "## Contribute" section is found, insert the contributors' list below it
        if contribute_index != -1:
            lines.insert(contribute_index + 1, "\n### Contributors\n\n")
            for name in contributor_names:
                lines.insert(contribute_index + 2, f"- {name}\n")

        # Move the file pointer to the beginning and overwrite the file with updated contents
        readme_file.seek(0)
        readme_file.writelines(lines)


# Assuming you have the contributor_names list already
write_contributors_to_readme(contributor_names)

