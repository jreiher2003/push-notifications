from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_sse import sse
import redis
import datetime

app = Flask(__name__)
# app.config["REDIS_URL"] = "redis://localhost"
# app.register_blueprint(sse, url_prefix='/stream')
app.secret_key = 'asdf'
red = redis.StrictRedis()

# @app.route('/')
# def index():
#     return render_template("index.html")

def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat')
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect('/')
    return '<form action="" method="post">user: <input name="user">'

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index2.html', session['user']) 

@app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    user = session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return "print message"


@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")


# @app.route('/new')
# def new():
#     return render_template("message.html")

# @app.route('/send', methods=['POST'])
# def send():
#     data = {"message": request.form.get('message')}
#     sse.publish(type="testevent", data=data, channel='test')
#     return redirect(url_for('new'))

# @app.route('/hello')
# def publish_hello():
#     data = {"message": "Hello!"}
#     sse.publish(data=data, type='greeting', channel='test2')
#     return "Message sent!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020, debug=True, threaded=True)