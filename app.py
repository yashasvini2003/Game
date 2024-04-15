from flask import Flask, render_template, request, redirect, url_for
import random
from database import DatabaseManager

app = Flask(__name__)

db_manager = DatabaseManager()

# Function to generate random numbers based on level
def generate_numbers(level):
    return ''.join(str(random.randint(0, 9)) for _ in range(level))

# Global variable to store the current level
current_level = 1

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    print("instructions called")
    if request.method == 'POST':
        source = request.form.get('source')
        if source == 'index':
            player_name = request.form['playerName']
            print("player_name:", player_name)
            app.config['player_name'] = player_name
            return redirect(url_for('instructions'))
        elif source == 'instructions':
            return redirect(url_for('display_numbers'))
    return render_template('instructions.html')

@app.route('/game')
def display_numbers():
    global current_level
    level = request.args.get('level')
    if level:
        current_level = int(level)
    numbers = generate_numbers(current_level)
    return render_template('game.html', numbers=numbers, level=current_level)

@app.route('/verify_numbers', methods=['POST'])
def verify_numbers():
    global current_level
    displayed_numbers = request.form['displayedNumbers']
    user_input = request.form['userNumbers']
    score = calculate_score(displayed_numbers, user_input)
    return redirect(url_for('display_score', score=score))
    
def calculate_score(displayed_numbers, user_input):
    score = 0
    for i in range(len(displayed_numbers)):
        if i < len(user_input) and user_input[i] == displayed_numbers[i]:
            score += 10
    return score

@app.route('/score/<int:score>')
def display_score(score):
    global current_level
    replay = score < current_level * 10 - 1
    return render_template('score.html', score=score, level=current_level, replay=replay)

@app.route('/next_level')
def next_level():
    global current_level
    current_level += 1
    if current_level > 15:
        return "You have reached the maximum level!"
    else:
        return redirect(url_for('display_numbers'))

@app.route('/end_game')
def end_game():
    global current_level
    player_name = app.config['player_name']
    
    # Calculate the cumulative score from all previous levels
    cumulative_score = sum([(level * 10) for level in range(1, current_level + 1)])
    
    # Insert the cumulative score into the database
    db_manager.insert_score(player_name, cumulative_score)
    
    # Render the end_game template with the current level and cumulative score
    return render_template('end_game.html', level=current_level, cumulative_score=cumulative_score)

@app.route('/start_over')
def start_over():
    global current_level
    current_level = 1
    return redirect(url_for('display_numbers'))

@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = db_manager.fetch_leaderboard_data()
    leaderboard_data_with_rank = [(rank + 1, player_name, score) for rank, (player_name, score) in enumerate(leaderboard_data)]  
    return render_template('leaderboard.html', leaderboard=leaderboard_data_with_rank)
