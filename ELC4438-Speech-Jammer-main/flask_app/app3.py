from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

counter = 0       # Button counter
volume = 50       # Initial volume (midpoint)

@app.route('/')
def index():
    return render_template('index.html', count=counter, volume=volume)

@app.route('/increment', methods=['POST'])
def increment():
    global counter
    counter += 1
    print("current counter number =", counter)
    return redirect(url_for('index'))

@app.route('/decrement', methods=['POST'])
def decrement():
    global counter
    counter -= 1
    print("current counter number =", counter)
    return redirect(url_for('index'))

@app.route('/set_volume', methods=['POST'])
def set_volume():
    global volume
    try:
        volume = int(request.form.get('volume', 50))
    except ValueError:
        volume = 50  # fallback
    print("current volume number =", volume)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
