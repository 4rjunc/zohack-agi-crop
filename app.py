from flask import Flask, render_template, request, jsonify
import os
import requests
from utils import DataPreprocessor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the preprocessor as a global variable
preprocessor = DataPreprocessor()

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global preprocessor  # Ensure we're using the global preprocessor
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Create a new preprocessor instance for each upload
            preprocessor = DataPreprocessor()
            initial_response = preprocessor.load_csv(file_path)
            return jsonify({
                'success': f'File {filename} uploaded successfully',
                'analysis': initial_response
            })
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'})
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/chat', methods=['POST'])
def chat():
    global preprocessor  # Ensure we're using the global preprocessor
    message = request.json.get('message', '')
    
    # First, check if it's a preprocessing command
    if preprocessor.df is not None:
        preprocessing_response = preprocessor.process_command(message)
        if preprocessing_response:
            # Call Eliza API with the preprocessing response
            eliza_response = requests.post(
                'http://localhost:3000/f5b3e476-fd10-01ad-ac62-8adbfefaf224/message',
                json={
                    'text': preprocessing_response + " " + message,
                    'userId': 'user123',
                    'userName': 'User'
                }
            )
            
            if eliza_response.status_code == 200:
                response_data = eliza_response.json()
                return jsonify({'response': response_data[0]['text']})
    
    # If no preprocessing command matched or no CSV is loaded, just use Eliza
    eliza_response = requests.post(
        'http://localhost:3000/f5b3e476-fd10-01ad-ac62-8adbfefaf224/message',
        json={
            'text': message,
            'userId': 'user123',
            'userName': 'User'
        }
    )
    
    if eliza_response.status_code == 200:
        response_data = eliza_response.json()
        response = response_data[0]['text'] if response_data else 'Sorry, I could not process your request.'
    else:
        response = 'Sorry, I am having trouble connecting to the server.'
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 