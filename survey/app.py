from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

key = 'reponses'

@app.route('/')
def home():
    """Sets up home page with title of survey, instructions, and button to begin"""
    title = satisfaction_survey.title
    inst = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=inst)

@app.route('/session', methods=["POST"])
def clear_session():
    session[key]=[]
    return redirect('/questions/0')

@app.route('/questions/<int:num>')
def questions(num):
    """Lists questions one at a time and records answer after each form submit"""

    response = session.get(key)

    if response is None:
        """If no questions have been answered redirect to home page"""
        return redirect('/')

    if len(response) == len(satisfaction_survey.questions):
        """If number of answers is the same as length of survey, end the survey and thank the user"""
        response.clear()
        return redirect('/thanks')

    if len(response) != num or num > len(satisfaction_survey.questions)-1:
        """If user tries to change question out of order redirect to current question"""
        flash('Trying to access an invalid question')
        return redirect(f'/questions/{len(response)}')

    q = satisfaction_survey.questions[num]

    return render_template('questions.html', questions=q, num=num)

@app.route('/answer', methods=['POST'])
def answer():
    """Appends answer for each question to response list"""
    reply = request.form['answer']

    response = session[key]
    response.append(reply)
    session[key] = response
    
    if len(response) == len(satisfaction_survey.questions):
        """If number of answers is the same as length of survey, end the survey and thank the user"""
        response.clear()
        return redirect('/thanks')
    else:
        """Else go to next question"""
        return redirect(f'/questions/{len(response)}')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')