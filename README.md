# Email2Git

**Email2Git** is a Python tool that converts email addresses into their associated GitHub profiles. By leveraging the GitHub API, Email2Git scans a list of emails, identifies corresponding GitHub usernames (when available), and displays the results via a command-line and a Flask-powered web interface.

## Features

- **Email-to-GitHub Conversion:** Converts emails into GitHub profiles if they exist.
- **Command-Line & Web Interface:** Run from the command line and view results in a sortable, color-coded HTML table.
- **Color-Coded Logging:** Real-time logging with clear, color-coded messages using the `colorama` library.
- **Graceful Shutdown:** Supports clean exit on Ctrl+C.
- **Rate Limit Handling:** Automatically handles GitHub API rate limits by pausing and retrying as needed.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourUserName/Email2Git.git
   cd Email2Git 
2.Create a Virtual Environment and install Dependencies
```bash
  python3 -m venv venv
  source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
  pip install requests Flask colorama
```
**Usage**
1. Run the Tool:
   ```bash
   python email2git.py
2. Enter Your GitHub API Token: When prompted, provide your GitHub API token to authenticate your requests.
3. Review the Results:
A usernames.txt file is generated containing the matched GitHub usernames.
A web interface is launched at http://127.0.0.1:5000 where the results are displayed in a sortable table.**
