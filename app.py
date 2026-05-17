from flask import Flask, render_template, request
from utils.resume_parser import extract_text
from utils.skill_extractor import extract_skills
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

job_skills = [
    "python",
    "react",
    "mongodb",
    "java"
]

candidate_results = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    total = len(candidate_results)

    selected = len([
        c for c in candidate_results
        if c['status'] == 'Selected'
    ])

    rejected = len([
        c for c in candidate_results
        if c['status'] == 'Rejected'
    ])

    return render_template(
        'dashboard.html',
        total=total,
        selected=selected,
        rejected=rejected
    )

@app.route('/uploadpage')
def uploadpage():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():

    file = request.files['resume']

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    resume_text = extract_text(filepath)

    skills = extract_skills(resume_text)

    matched_skills = list(
        set(job_skills) & set(skills)
    )

    score = (
        len(matched_skills) /
        len(job_skills)
    ) * 100

    if score >= 70:
        status = 'Selected'
    else:
        status = 'Rejected'

    candidate = {
        'name': file.filename,
        'skills': skills,
        'score': score,
        'status': status
    }

    candidate_results.append(candidate)

    return render_template(
        'result.html',
        skills=skills,
        matched_skills=matched_skills,
        score=score,
        status=status
    )

@app.route('/ranking')
def ranking():

    sorted_candidates = sorted(
        candidate_results,
        key=lambda x: x['score'],
        reverse=True
    )

    return render_template(
        'ranking.html',
        candidates=sorted_candidates
    )

if __name__ == '__main__':
    app.run(debug=True)