import os
from flask import Flask, request, jsonify, render_template
import requests

# Absolute path to the templates and static folders
template_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../frontend/templates')
static_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../frontend/static')

# Create Flask app with the correct template and static folder paths
app = Flask(__name__, 
            template_folder=template_folder_path,  # Absolute path to templates
            static_folder=static_folder_path)  # Absolute path to static files

# Function to fetch YouTube videos based on query using YouTube Data API
def fetch_youtube_videos(query):
    api_key = "AIzaSyBOc-m5ZTxlswmUisY_Avt-OQVxyncQecQ"  # Your provided YouTube API key
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data['items'][:3]:  # Get top 3 videos
                videos.append({
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'thumbnail': item['snippet']['thumbnails']['high']['url']  # Adding thumbnail image
                })
            return videos
        else:
            return []
    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return []

@app.route('/')
def home():
    # This route renders the index page
    return render_template('index.html')  # Flask will now look in the frontend/templates folder

@app.route('/ask', methods=['GET'])
def ask_page():
    # This route renders the ask page
    return render_template('ask.html')  # Flask will now look in the frontend/templates folder

@app.route('/ask', methods=['POST'])
def ask():
    # This route handles the form submission for the YouTube search
    query = request.form.get('query')  # Get query from the form data

    if not query:
        return jsonify({"error": "No query provided!"}), 400

    # Fetch relevant YouTube videos based on the query
    videos = fetch_youtube_videos(query)

    # Return the response with videos
    return jsonify({'videos': videos})

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the request contains a file
    if 'file' in request.files:
        file = request.files['file']
        
        # Ensure the uploads directory exists
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Save the file to the uploads directory
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Return a success message
        return jsonify({"message": f"File '{file.filename}' uploaded successfully!"}), 200
    return jsonify({"error": "No file uploaded!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
