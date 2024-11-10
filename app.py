from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import logging
from flask_session import Session
import os

app = Flask(__name__)

# Configure Flask session
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
app.config['SESSION_TYPE'] = 'filesystem'  # You can choose other session types as well
Session(app)

with open("apikey.txt") as f:
    API_KEY = f.read().strip()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    messages = session.get('messages', [])
    return render_template('chatbot.html', messages=messages)

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/health')
def health():
    return render_template('health.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    user_message = request.json.get('message')
    logging.debug(f"Received message: {user_message}")
    try:
        response = requests.post(
            'https://api.on-demand.io/chat/v1/sessions',
            headers={'apikey': API_KEY, 'accept': 'application/json', 'content-type': 'application/json'},
            json={'message': user_message, 'externalUserId': 'endUser'}
        )
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()
        logging.debug(f"API response: {response_data}")

        # Extract the id from the response and store it in the session
        session_id = response_data['data']['id']
        session['session_id'] = session_id
        logging.debug(f"Session ID stored in session: {session_id}")

        return jsonify(response_data)
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.route('/api/chatbot/message', methods=['POST'])
def api_chatbot_message():
    user_message = request.json.get('message')
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Session ID not found'}), 400
    logging.debug(f"Using session ID: {session_id} for message: {user_message}")
    try:
        payload = {
            'query': user_message,
            "endpointId": "predefined-openai-gpt4o",
            "responseMode": "sync",
            "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1731164712"]
        }
        headers = {
            'apikey': API_KEY,
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()
        logging.debug(f"API response: {response_data}")
        bot_message = response_data['data']['answer']

        # Store messages in session
        messages = session.get('messages', [])
        messages.append({'sender': 'user', 'message': user_message})
        messages.append({'sender': 'bot', 'message': bot_message})
        session['messages'] = messages

        return jsonify({'answer': bot_message})
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/tasks', methods=['POST'])
def api_chatbot_tasks():
    user_message = request.json.get('message')
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Session ID not found'}), 400
    logging.debug(f"Using session ID: {session_id} for task identification in message: {user_message}")
    try:
        payload = {
            'query': f"Identify tasks in the following message: {user_message}. respond with a comma separated list of tasks. DO NOT include the message itself.",
            "endpointId": "predefined-openai-gpt4o",
            "responseMode": "sync",
            "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1731164712"]
        }
        headers = {
            'apikey': API_KEY,
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()
        logging.debug(f"API response for task identification: {response_data}")
        """example of response_data = {'message': 'Chat query submitted successfully', 'data': {'sessionId': '6730845fe93cb32e4e56c312', 'messageId': '6730b9dd80617dba5611fdf8', 'answer': 'Make my bed, submit problem sheet, send email', 'metrics': {'inputTokens': 226, 'outputTokens': 10, 'totalTokens': 236, 'ragTimeSec': 6.94, 'fulfillmentTimeSec': 0.66, 'totalTimeSec': 7.6}, 'status': 'completed'}}"""
        # extract the answer from the response
        tasks = response_data['data']['answer']
        logging.debug(f"Tasks identified: {tasks}")
        task_list = [task.strip() for task in tasks.split(',') if task.strip()]  # Clean and filter tasks
        session_tasks = session.get('tasks', [])
        session_tasks.extend(task_list)
        session['tasks'] = session_tasks
        logging.debug(f"Tasks added to session: {session['tasks']}")  # Debugging statement
        return jsonify({'tasks': tasks})
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.form.get('new_task')
    if new_task and new_task.strip():  # Check if the task is not empty
        tasks = session.get('tasks', [])
        tasks.append(new_task.strip())  # Strip any leading/trailing whitespace
        session['tasks'] = tasks
    return redirect(url_for('tasks'))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_to_delete = request.form.get('task')
    if task_to_delete:
        tasks = session.get('tasks', [])
        if task_to_delete in tasks:
            tasks.remove(task_to_delete)
            session['tasks'] = tasks
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)