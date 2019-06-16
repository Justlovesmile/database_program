from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return  render_template('index.html')


@app.route('/test/', methods=['GET', 'POST'])
def test():
    a = request.form.get('input')
    print(a)
    return '我是后端'


if __name__ == '__main__':
    app.run(debug=True)