from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from chalice import Chalice

app = Chalice(app_name='webscraper-project')
BUCKET_NAME = 'arc-webscraper-project'

# Crypto is the currency to return data for
@app.route('/{crypto}')
def index(crypto):



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#


# TODO: Using chalice, have a webpage that allows you to input which crypto you want to see
# TODO: This will trigger a post request app.route, which scrapes masternodes.online and returns
# TODO: daily, weekly, monthly, and yearly income, price, required coins, and mn worth

# website has input box -> "ULT" -> if it exists call the application -> return results



def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if response_correct(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error("Error during requests to {0} : {1}".format(url, str(e)))
        return None


def response_correct(resp):
    # Get the content-type in <head></head>
    content_type = resp.headers['Content-Type'].lower()
    # return true if an HTTP response of 200 (means successful)
    # and there is not, nothing there
    # and the string html is found
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    # Write errors to log named log.txt
    with open('log.txt', 'w') as f:
        f.writelines(e)


def get_items():
    url = 'https://masternodes.online/'
    response = simple_get(url)
    # If there is a response, parse the html, and for each <option> element, add it's content to an array
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        items = set()
        for option in html.select('option'):
            items.add(option.text)
        return sorted(list(items))


if __name__ == '__main__':
    print('Starting script...')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    # print(get_breeds())
    for x in get_items():
        print(x)
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print('Done')