import json
from urllib import request


def process_file(absolute_filename, save_prefix):
    prompt_workflow = json.load(open('workflow_api.json'))

    # give some easy-to-remember names to the nodes
    load_image_node = prompt_workflow["56"]
    save_image_node = prompt_workflow["53"]

    load_image_node["inputs"]["image"] = absolute_filename
    save_image_node["inputs"]["filename_prefix"] = save_prefix

    # everything set, add entire workflow to queue.
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://localhost:8189/prompt", data=data)
    request.urlopen(req)

