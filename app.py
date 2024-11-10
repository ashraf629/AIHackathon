from flask import Flask, render_template, request, jsonify, session
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
    return render_template('chatbot.html')

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
        payload = {'query': user_message,
                   "endpointId": "predefined-openai-gpt4o",
                    "responseMode": "sync",
                    "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1731164712"]}
        headers = {'apikey': API_KEY,
                 'accept': 'application/json',
                 'content-type': 'application/json'}
        url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        response = requests.post(url,headers=headers,json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()
        logging.debug(f"API response: {response_data}")

        # Extract the answer from the response
        answer = response_data['data']['answer']
        return jsonify({'answer': answer})
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

    """

    Generic
    The SMART framework is a goal-setting tool used to create clear and achievable objectives. It stands for:

Specific: Goals should be clear and specific, answering the questions of what, why, and how.
Measurable: Goals should have criteria that allow progress and completion to be tracked.
Achievable: Goals should be realistic and attainable, taking into account available resources and constraints.
Relevant: Goals should be aligned with broader objectives and be worthwhile.
Time-bound: Goals should have a defined timeline, with a start and end date, to provide a sense of urgency and deadline.
This framework is widely used in personal development, business, and project management to ensure goals are well-structured and attainable.

The SMART system, often discussed in the context of decision-making and cognitive processes, involves two distinct systems known as System 1 and System 2.

System 1: This is the intuitive, automatic, and fast-thinking part of the brain. It operates subconsciously and is responsible for quick judgments and decisions based on heuristics and past experiences. It is efficient and effective for routine decisions and situations that require immediate responses.

System 2: This is the analytical, deliberate, and slow-thinking part of the brain. It requires conscious effort and is used for complex decision-making and problem-solving. System 2 is responsible for logical reasoning, critical thinking, and the evaluation of information, often overriding the initial impulses of System 1 when necessary.

Together, these systems help individuals navigate various situations by balancing speed and accuracy in decision-making processes.



AGent

The SMART framework is a goal-setting tool that helps individuals and organizations create clear, actionable, and achievable objectives. SMART is an acronym that stands for:

Specific: Goals should be clear and specific, answering the questions of who, what, where, when, and why.

Measurable: Goals should have criteria for measuring progress and success, allowing you to track progress and stay motivated.

Achievable: Goals should be realistic and attainable, considering available resources and constraints.

Relevant: Goals should align with broader objectives and be important to the individual or organization.

Time-bound: Goals should have a defined timeline, including a start and finish date, to provide a sense of urgency and focus.

This framework is widely used in various fields, including business, education, and personal development, to enhance productivity and ensure effective planning and execution.

System 1 and System 2 refer to a concept introduced by psychologist Daniel Kahneman in his book "Thinking, Fast and Slow." These two systems describe different modes of thinking used by the human brain:

System 1: This is the fast, automatic, and intuitive way of thinking. It operates quickly and with little effort, relying on heuristics and instincts. System 1 is responsible for quick judgments and decisions, often without conscious awareness. It is useful for routine tasks and situations requiring immediate responses.

System 2: This is the slow, deliberate, and analytical mode of thinking. It requires more effort and is used for complex problem-solving and decision-making. System 2 is responsible for critical thinking and reasoning, allowing individuals to evaluate information carefully and make more informed decisions.

Both systems work together to help humans navigate the world, with System 1 handling routine and familiar tasks efficiently and System 2 stepping in when more thoughtful analysis is needed.



"""




"""
To manage your tasks effectively given your essay deadline and other commitments, here's a structured approach:

Prioritize the Essay: Since the essay has a firm deadline, allocate dedicated time slots for writing and research. Consider breaking down the task into smaller parts (research, outlining, writing, editing) and schedule these parts over the next few days.

Vitamins and Medication: Taking vitamins every alternate day can be challenging to remember. Consider associating this task with a routine activity you do daily, like brushing your teeth or having your morning coffee, to create a habit.

Gym Schedule: Plan your gym sessions around your essay work. If the essay is due on Sunday, aim to complete most of your writing before the weekend, allowing you to attend the gym without feeling stressed. You could go to the gym on days when you need a mental break from writing.

Social Event: Decide if attending the social event today is necessary or beneficial for you. If it’s important, you might use it as a reward after completing a significant portion of your essay. If not, consider skipping it or attending briefly to focus on your essay.

Use Reminders and To-Do Lists: Utilize digital tools or apps for reminders about your vitamins, gym sessions, and essay deadlines. Keeping a to-do list can help you track your progress and prioritize tasks.

By organizing your schedule and setting clear priorities, you can balance all your commitments effectively.




To effectively manage your schedule, consider the following plan:

Prioritize Your Essay: Since your essay is due today, focus on completing it first. Allocate specific blocks of time to ensure you have enough to write, revise, and finalize it. Aim to complete it early in the day if possible.

Plan Your Vitamins: As you need to take vitamins every alternate day, ensure that you keep track of the days you need to take them. If today is a vitamin day, make sure to take them at a convenient time.

Gym Schedule: Since you need to go to the gym four times a week, you might need to adjust your schedule based on your availability and the time left in the week. If you haven't met your gym goal yet, plan your gym sessions for the upcoming days.

Social Event: After handling your primary responsibilities (like the essay), decide if you can attend the social event. It can be a good way to relax after completing your tasks. However, if attending will prevent you from finishing important work, you might consider skipping it or attending for a shorter duration.

By prioritizing your tasks and managing your time efficiently, you can meet all your responsibilities while still having time for social activities.
"""