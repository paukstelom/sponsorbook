from flask import Flask, render_template

flask = Flask(__name__)


@flask.route('/login')
def hello_world():
    return render_template('login_page.html')


if __name__ == '__main__f':
    flask.run(debug=True)