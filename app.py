from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the poll data file
POLL_DATA_FILE = os.path.join('data', 'poll_data.json')


def load_poll_data():
    if os.path.exists(POLL_DATA_FILE):
        with open(POLL_DATA_FILE, 'r') as f:
            return json.load(f)
    return {"question": "", "choices": {}, "votes": {}}


def save_poll_data(data):
    with open(POLL_DATA_FILE, 'w') as f:
        json.dump(data, f)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        question = request.form['question']
        choices = {choice: 0 for choice in request.form.getlist('choices')}

        poll_data = {
            "question": question,
            "choices": choices,
            "votes": {choice: 0 for choice in choices}
        }
        save_poll_data(poll_data)
        return "Poll created successfully!"
    return render_template('admin.html')


@app.route('/poll', methods=['GET'])
def poll():
    poll_data = load_poll_data()
    return render_template('poll.html', poll_data=poll_data)


@app.route('/vote', methods=['POST'])
def vote():
    poll_data = load_poll_data()
    selected_choice = request.json.get('choice')
    if selected_choice in poll_data['votes']:
        poll_data['votes'][selected_choice] += 1
        save_poll_data(poll_data)
    return jsonify({"status": "success", "votes": poll_data['votes']})

@app.route('/display', methods=['GET'])
def display():
    """Display the current poll results for separate viewing."""
    poll_data = load_poll_data()
    return render_template('display.html', poll_data=poll_data)



@app.route('/results', methods=['GET'])
def results():
    poll_data = load_poll_data()
    return jsonify(poll_data)


if __name__ == '__main__':
    app.run(debug=True)
