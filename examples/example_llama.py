from llama_index import RssReader
from flask import Flask, request, render_template
import json 

# Load template
with open('app/template.md') as f:
    template = f.read()

# Get rss content 
def get_rss_content(websites:list) -> list:
    reader = RssReader()
    results = []
        
    for web in range(len(websites)):
        documents = reader.load_data([websites[web]])
        for doc in documents: 
            text = str(doc.get_text())
            results.append(text)

    return results
 
app = Flask(__name__)
@app.route('/rss', methods=['POST'])
def endpiont_generate_rss():

    feed_requests = ["insert rss feed url"]
    markdown_string = get_rss_content(feed_requests)

    #Format the Markdown string using mdformat
    concate_markdown_string = ""
    for string in markdown_string:
        concate_markdown_string = concate_markdown_string + string
    columun = list(range(len(markdown_string)))

    format_dict = {}
    for num in range(len(columun)): 
        format_dict[f"key number {columun[num]}"] = markdown_string[num]
    #Populate the template with the generated content and image URL
    output = template.format(topic="topic", overview=concate_markdown_string)

    # # Write output to file
    with open(f"", 'w') as f:
        f.write(output)

    format_json_dict =  json.dumps(format_dict, indent = 4)
    return format_json_dict

if __name__ == '__main__':
    app.run()