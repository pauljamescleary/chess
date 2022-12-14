from . import create_app

if __name__ == '__main__':
    print("*** IN APP.PY ***")
    create_app().run(debug=True, host='0.0.0.0')
