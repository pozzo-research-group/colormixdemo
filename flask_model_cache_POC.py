from flask import Flask, request
from flask_caching import Cache

config = {
    "DEBUG":True,
    "CACHE_TYPE":"SimpleCache",
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


class test_object():
    def __init__(self, str1):
        self.strings = [str1]

    def update_str(self, new_str):
        self.strings.append(new_str)

    def print_str(self):
        return self.strings

test1 = test_object('this is string 1')

cache.set("object", test1)


class Session():
    def __init__(self):
        pass

session_state = Session()
session_state.test1 = test1

@app.route('/')
def hello_world():
    return "<p>Hello world</p>"

@app.route('/update_str', methods = ['POST'])
def update_str():
    print(request)
    new_str = request.json
    print(new_str)

    test1 = cache.get("object")
    test1.update_str(new_str['new_str'])
    cache.set('object', test1)

    return('\n updated object')


@app.route('/check_object')
def read_obj():
    test1 = cache.get('object')
    return test1.print_str()


@app.route('/reset_object')
def reset():

    test1 = test_object('squeaky clean')
    cache.set('object', test1)
    return 'cleared obj'