from flask import Flask, render_template, request, redirect, url_for, send_file
from teaser_processing import process_video
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files['video_file']
        title = request.form['title']
        director_name = request.form['director_name']
        
        if video_file:
            video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            video_file.save(video_path)
            
            process_video(video_path, title, director_name)
            
            return redirect(url_for('result'))
    
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/download')
def download_file():
    return send_file("teaser0.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
