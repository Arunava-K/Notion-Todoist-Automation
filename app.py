from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Your Todoist API token
todoist_api_token = "YOUR_TODOIST_API_TOKEN"

# Your Notion API token
notion_api_token = "secret_l3R5ILPoUZqSu84YbT7eoEYJ39Ff6yWw8sTt33WSUjZ"

# Notion database ID
database_id = "c899e06bd5714edca4229801c7182fa2"

# Notion API endpoint for creating a new page in the database
notion_create_page_url = f"https://api.notion.com/v1/pages"

# Map Todoist task fields to Notion properties
property_mapping = {
    "Task": "content",
    "Due Date": "due_date",
    "Due Time": "due_time"
}

# Function to create a new page in Notion database
def create_notion_page(task):
    headers = {
        "Authorization": f"Bearer {notion_api_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }

    properties = {
        property_mapping[key]: {"title": [{"text": {"content": task[key]}}]} for key in property_mapping.keys() if key in task
    }

    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(notion_create_page_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return True
    else:
        return False

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = {
            "Task": request.form['task'],
            "Due Date": request.form['due_date'],
            "Due Time": request.form['due_time']
        }
        create_success = create_notion_page(task)
        if create_success:
            return "Task added successfully to Notion!"
        else:
            return "Failed to add task to Notion."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
