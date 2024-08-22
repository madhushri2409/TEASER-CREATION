import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from teaser_processing import process_video

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'static/processed'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files['video_file']
        title = request.form['title']
        director_name = request.form['director_name']
        
        if video_file:
            video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            video_file.save(video_path)
            
            teaser_path = process_video(video_path, title, director_name, output_dir=PROCESSED_FOLDER)
            
            return redirect(url_for('result', teaser_file=os.path.basename(teaser_path)))
    
    return render_template('index.html')

@app.route('/result')
def result():
    teaser_file = request.args.get('teaser_file')
    return render_template('result.html', teaser_file=teaser_file)

@app.route('/download')
def download_file():
    return send_file(os.path.join(PROCESSED_FOLDER, 'teaser0.mp4'), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
