import sys, tempfile, os
import re
import requests
from argparse import ArgumentParser, RawTextHelpFormatter
from subprocess import call
from datetime import datetime


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
            default=False)
    parser.add_argument(
            '-u',
            '--update',
            help='update an existing entry',
            action='store',
            dest='id',
            type=int)

    args = parser.parse_args()



def get_user_content():
    """Open text editor of choice and retreive user input"""

    initial_text = """
# Describe what you learned above using markdown for text formatting.
# An empty message will not get published.
# Change the date or add tags below.
#
# Date: {date}
# Tags:""".format(date=current_date)


    with tempfile.NamedTemporaryFile(delete=False) as temp_f:
        temp_f.write(bytes(initial_text, 'utf-8'))
        temp_f.flush()
        EDITOR = os.environ.get('TIL_EDITOR', 'nvim')
        call([EDITOR, temp_f.name])
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

def make_request(data):
    """POST or UPDATE content to the server"""

    selector_path = '/api/v1/tils'
    server_path = '{base_url}{path}'.format(base_url='http://localhost:4000',
                                            path=selector_path)
    server_fqdn = server_path.strip('/').split('//')[1]

    r = requests.post(server_path, data=data)
    return r.text

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

content = get_user_content()
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

request_data = build_request_data(parse_description(content),
                                  current_date,
                                  parse_tags(content))
response = make_request(request_data)
print(response)
