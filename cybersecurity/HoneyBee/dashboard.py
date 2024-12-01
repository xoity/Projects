from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import dash
import plotly.express as px
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import json
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username
    
    @staticmethod
    def check_password(password):
        return check_password_hash(Config.ADMIN_PASSWORD_HASH, password)

@login_manager.user_loader
def load_user(username):
    if username == Config.ADMIN_USERNAME:
        return User(username)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == Config.ADMIN_USERNAME and User.check_password(password):
            user = User(username)
            login_user(user)
            session['username'] = username
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        # Save the new user to the database
        flash('User registered successfully')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/attacks')
@login_required
def get_attacks():
    with open('SSH_honeypot.log', 'r') as log_file:
        logs = [json.loads(line) for line in log_file]
    return jsonify(logs)

@app.route('/credentials')
def credentials():
    return jsonify({
        'username': Config.ADMIN_USERNAME,
        'password': 'The password is stored as a hash and cannot be retrieved directly.'
    })

def create_dash_app(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')
    dash_app.layout = dash.html.Div([
        dash.html.H1('Attack Data Visualization'),
        dash.dcc.Graph(id='attack-graph')
    ])

    @dash_app.callback(
        dash.Output('attack-graph', 'figure'),
        [dash.Input('interval-component', 'n_intervals')]
    )
    def update_graph(n):
        with open('SSH_honeypot.log', 'r') as log_file:
            logs = [json.loads(line) for line in log_file]
        df = pd.DataFrame(logs)
        fig = px.histogram(df, x='timestamp', title='Attack Frequency Over Time')
        return fig

    return dash_app

if __name__ == "__main__":
    create_dash_app(app)
    app.run(debug=True)