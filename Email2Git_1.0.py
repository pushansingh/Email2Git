import requests
import time
import threading
import logging
from flask import Flask, render_template_string

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

GITHUB_RATE_LIMIT_URL = "https://api.github.com/rate_limit"

# Event to interrupt sleep if Enter is pressed
interrupt_event = threading.Event()

def get_github_api_key():
    return input("Please enter your GitHub API Token: ")

def wait_or_interrupt(seconds):
    def wait_for_enter():
        input("Paused. Press ENTER to retry immediately...\n")
        interrupt_event.set()
    
    # Start thread to listen for Enter
    t = threading.Thread(target=wait_for_enter)
    t.start()

    logger.info(f"Waiting {seconds} seconds or press ENTER to continue early...")
    interrupted = interrupt_event.wait(timeout=seconds)

    if interrupted:
        logger.info("Enter pressed. Resuming early...")
    else:
        logger.info("Timeout reached. Resuming...")

    interrupt_event.clear()

def check_github_user(email, api_key):
    try:
        headers = {
            'Authorization': f'token {api_key}'
        }
        response = requests.get(f'https://api.github.com/search/users?q={email}+in:email', headers=headers)

        if response.status_code == 403:
            logger.error(f"403 Forbidden (Rate Limit likely) while checking {email}")
            wait_or_interrupt(60)
            return check_github_user(email, api_key)

        elif response.status_code == 400:
            logger.error(f"400 Bad Request for {email}. Pausing...")
            wait_or_interrupt(60)
            return check_github_user(email, api_key)

        elif response.status_code == 200:
            data = response.json()
            if data['total_count'] > 0:
                logger.info(f"Email {email} found with GitHub username: {data['items'][0]['login']}")
                return email, data['items'][0]['login']
            else:
                logger.info(f"Email {email} has no associated GitHub account.")
                return email, None

        else:
            logger.error(f"Unexpected error {response.status_code} for {email}. Retrying...")
            wait_or_interrupt(60)
            return check_github_user(email, api_key)

    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception for {email}: {e}")
        wait_or_interrupt(60)
        return check_github_user(email, api_key)

def read_emails(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError as e:
        logger.error(f"Error reading email file: {e}")
        return []

def write_txt_file(usernames):
    try:
        with open("usernames.txt", "w") as file:
            for username in usernames:
                file.write(username + "\n")
        logger.info("Usernames written to usernames.txt")
    except IOError as e:
        logger.error(f"Error writing to file: {e}")

def generate_html_gui(email_results):
    html_template = '''
    <html>
        <head><title>GitHub User Checker</title><style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .email { margin-bottom: 10px; padding: 5px; }
            .valid { background-color: #c8e6c9; }
            .invalid { background-color: #ffcdd2; }
        </style></head>
        <body>
            <h1>GitHub User Checker Results</h1>
            <div>
                {% for email, result in email_results.items() %}
                    <div class="email {% if result %}valid{% else %}invalid{% endif %}">
                        <strong>{{ email }}:</strong>
                        {% if result %}
                            GitHub username: <span style="color: green;">{{ result }}</span>
                        {% else %}
                            <span style="color: red;">No GitHub account</span>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
        </body>
    </html>
    '''
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template_string(html_template, email_results=email_results)

    app.run(debug=True, use_reloader=False)

def main():
    api_key = get_github_api_key()
    email_file = "emails.txt"
    emails = read_emails(email_file)

    email_results = {}
    usernames = []

    for email in emails:
        email = email.strip()
        email, username = check_github_user(email, api_key)
        email_results[email] = username
        if username:
            usernames.append(username)

    write_txt_file(usernames)
    generate_html_gui(email_results)

if __name__ == '__main__':
    main()
