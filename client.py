import json
import re
import requests
import tempfile
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from pathlib import Path
from subprocess import call
from termcolor import colored


def load_configuration():
    with open('{home}/.til/config.json'.format(home=str(Path.home()))) as f:
        configuration = json.load(f)
    return configuration

def get_user_content(configuration):
    """Open text editor of choice and retreive user input"""

    initial_text = """
# Describe what you learned above using markdown for text formatting.
# An empty message will not get published.
# Change the date or add tags below.
#
# Date: {date}
# Tags:""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with tempfile.NamedTemporaryFile(delete=False) as temp_f:
        temp_f.write(bytes(initial_text, 'utf-8'))
        temp_f.flush()
        editor = configuration.get('editor', 'vim')
        call([editor, temp_f.name])
        temp_f.close()
        # must open again because of how vim works
        with open(temp_f.name) as f:
            content = f.read()
    return content

def parse_tags(text):
    """Parse tags from user input"""

    tags_match = re.search(r'\n# Tags:(.+)$', text)
    if tags_match:
        tags = [tag.strip() for tag in tags_match.group(1).split(",")]
        return list(tags)
    return []

def parse_description(text):
    """Parse description from user input"""

    match = re.search(r'[.\s\S]*?(?=# Describe what you learned)', text)
    if match:
        return match.group().strip()
    return ''

def build_request_data(description, date, tags):
    """Build JSON request data from description, date, and tags"""

    request_data = {}
    if description:
        request_data['description'] = description
    if date:
        request_data['date'] = date
    if tags:
        request_data['tags'] = tags

    return request_data

def make_request(configuration, data, for_post):
    """POST or UPDATE content to the server"""

    server_url = configuration.get('server_url', None)
    endpoint = configuration.get('post_path', None)
    full_path = '{base_url}{path}'.format(base_url=server_url,
                                            path=endpoint)
    response = requests.post(full_path, json=data)
    return response


description = """Today I Learned CLI Tool

Set $TIL_EDITOR to change the default text editor.
"""

if __name__ == '__main__':
    parser = ArgumentParser(description=description,
                            formatter_class=RawTextHelpFormatter,
                            add_help=True)

    parser.add_argument(
            '-p',
            '--post',
            help='post a new entry',
            action='store_true',
            dest='post',
            default=False)
    parser.add_argument(
            '-u',
            '--update',
            help='update an existing entry',
            action='store',
            dest='id',
            type=int)

    args = parser.parse_args()

    configuration = load_configuration()
    content = get_user_content(configuration)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_data = build_request_data(parse_description(content),
                                      current_date,
                                      parse_tags(content))
    response = make_request(configuration, request_data, args.post)
    if response.status_code >= 400:
        print('Error - could not publish entry')
    else:
        success_message = '{msg} --> {resource_path}'.format(
                msg=colored('Entry Published!', 'green'),
                resource_path=configuration.get('server_url') + \
                json.loads(response.text)['resource_path'])
        print(success_message)

