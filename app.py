from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__, static_folder='Static')
# Set a secret key for session management
app.secret_key = os.urandom(24)

def initialize_inventory():
    """Initialize the user's inventory if not already set"""
    if 'inventory' not in session:
        session['inventory'] = []

def add_to_inventory(item):
    """Add an item to the user's inventory"""
    initialize_inventory()
    if item not in session['inventory']:
        session['inventory'].append(item)
        session.modified = True

def get_inventory():
    """Get the user's current inventory"""
    initialize_inventory()
    return session.get('inventory', [])
 
# Define the secret codes here
SECRET_CODES = {
    "10/24/25": "secret.html",
    "MaTh": "secret2.html",
    "python": "secret3.html",
    "PYTHON": "secret3.html",
    "BREAD": "secret_bread.html",
    "abandoned": "dungeon.html",
    "piano": "piano_room.html",
    "03/15/25": "you_are_not_alone.html",
    # Sector access codes
    "5E-1102-GAMMA": "sector/5",
    "3L-7721-OMEGA": "sector/3",
    "9F-3381-THETA": "sector/9",
    "2D-5566-ALPHA": "sector/2",
    "7X-9942-DELTA": "sector/7",
    "1C-0013-UNKNOWN": "sector/1",
    "8A-0029-TEACHER": "sector/8"
}

# Sector access codes mapping
SECTOR_CODES = {
    1: "1C-0013-UNKNOWN",  # C13 - UNKNOWN
    2: "2D-5566-ALPHA",  # D14 - DECEASED
    3: "3L-7721-OMEGA",  # L14 - DECEASED
    5: "5E-1102-GAMMA",  # E13 - ALIVE
    7: "7X-9942-DELTA",  # S14 - DECEASED
    8: "8A-0029-TEACHER",  # A29 - THE TEACHER
    9: "9F-3381-THETA"   # F13 - DECEASED
}

def get_code_template(code):
    """Check if code matches (case-insensitive) and return template name"""
    code_lower = code.lower().strip()
    for key, value in SECRET_CODES.items():
        if key.lower() == code_lower:
            return value
    return None


@app.route('/')
def inicio():
    if check_backrooms():
        return redirect(url_for('backrooms'))

    # Check if there's a death message to display
    death_message = session.pop('death_message', None)  # Pop to only show once
    return render_template('web.html', inventory=get_inventory(), death_message=death_message)


@app.route('/newpage')
def new_page():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('newpage.html', inventory=get_inventory())


@app.route('/dream-world')
def dream_world():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('dream_world.html', inventory=get_inventory())


@app.route('/three-buttons')
def three_buttons():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('web.html', inventory=get_inventory())


@app.route('/secret2', methods=['GET', 'POST'])
def secret2_page():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    
    if request.method == 'POST':
        math_answer = request.form.get('math_answer', '').strip()
        # Correct answers for x²-10x+16=0 are x = 2 and x = 8
        # Accept various formats for either solution or ordered pairs
        correct_single_answers = ['2', '8']
        correct_ordered_pairs = ['2,8', '8,2', '(2,8)', '(8,2)', '2, 8', '8, 2']

        if math_answer in correct_single_answers:
            result = "correct"
        elif math_answer in correct_ordered_pairs:
            result = "correct_ordered"
        else:
            result = "incorrect"

        return render_template('secret2.html', result=result, submitted_answer=math_answer, inventory=get_inventory())

    return render_template('secret2.html', inventory=get_inventory())


@app.route('/secret', methods=['GET', 'POST'])
def secret_page():
    if check_backrooms():
        return redirect(url_for('backrooms'))

    if request.method == 'POST':
        entered_code = request.form.get('code')
        template_name = get_code_template(entered_code)
        if template_name:
            # Special handling for pages with dedicated routes
            if template_name == "secret2.html":
                return redirect(url_for('secret2_page'))
            elif template_name == "secret3.html":
                return redirect(url_for('secret3_page'))
            return render_template(template_name, inventory=get_inventory())
        else:
            # Return the same page with an error message
            return render_template('newpage.html', error="Incorrect code. Please try again.", inventory=get_inventory())

    # If GET request, show the Hall Of Memes directly
    return render_template('secret.html', inventory=get_inventory())


@app.route('/secret-content')
def secret_content():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('secret.html', inventory=get_inventory())


@app.route('/secret3')
def secret3_page():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('secret3.html', inventory=get_inventory())


@app.route('/sliding-puzzle')
def sliding_puzzle():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sliding_puzzle.html', inventory=get_inventory())


@app.route('/leo-graveyard')
def leo_graveyard():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('leo_graveyard.html', inventory=get_inventory())


@app.route('/piano-room')
def piano_room():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('piano_room.html', inventory=get_inventory())


@app.route('/basement')
def basement():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('basement.html', inventory=get_inventory())


@app.route('/bread-sanctuary')
def bread_sanctuary():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('secret_bread.html', inventory=get_inventory())


@app.route('/you-are-not-alone')
def you_are_not_alone():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    
    # Unlock sector 1 when visiting this page (since it's CLASSIFIED but discoverable)
    if 'unlocked_sectors' not in session:
        session['unlocked_sectors'] = []
    if 1 not in session['unlocked_sectors']:
        session['unlocked_sectors'].append(1)
        session.modified = True
    
    return render_template('you_are_not_alone.html', inventory=get_inventory())


@app.route('/did-not-listen')
def did_not_listen():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('did_not_listen.html', inventory=get_inventory())


@app.route('/harder-math', methods=['GET', 'POST'])
def harder_math():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    
    if request.method == 'POST':
        # Get the answers from the form
        answer1 = request.form.get('answer1', '').strip()
        answer2 = request.form.get('answer2', '').strip()
        answer3 = request.form.get('answer3', '').strip()
        answer4 = request.form.get('answer4', '').strip()

        # Check answers (these are the correct answers)
        # Problem 1: 2x² - 7x + 3 = 0 -> x = 3, x = 0.5
        # Problem 2: 3x + 2y = 12, x - y = 1 -> x = 2.8, y = 1.8 (or simplified as x=2, y=1 doesn't work, actually x=2.8, y=1.8)
        # Actually solving: x-y=1 => x=1+y, substitute: 3(1+y)+2y=12 => 3+3y+2y=12 => 5y=9 => y=1.8, x=2.8
        # Problem 3: 2^(x+1) = 16 -> 2^(x+1) = 2^4 -> x+1=4 -> x=3
        # Problem 4: x² - 5x - 14 -> (x-7)(x+2)

        correct_answers = {
            'answer1': ['3, 0.5', '0.5, 3', '3 and 0.5', '0.5 and 3', 'x=3, x=0.5', 'x=0.5, x=3'],
            'answer2': ['x=2.8, y=1.8', '2.8, 1.8', '(2.8, 1.8)', 'x = 2.8 and y = 1.8'],
            'answer3': ['3', 'x=3'],
            'answer4': ['(x-7)(x+2)', '(x+2)(x-7)', 'x-7)(x+2)', 'x²-5x-14=(x-7)(x+2)']
        }

        # Check each answer
        results = {}
        results['answer1'] = answer1.lower() in [ans.lower() for ans in correct_answers['answer1']]
        results['answer2'] = answer2.lower() in [ans.lower() for ans in correct_answers['answer2']]
        results['answer3'] = answer3.lower() in [ans.lower() for ans in correct_answers['answer3']]
        results['answer4'] = answer4.lower() in [ans.lower() for ans in correct_answers['answer4']]

        # Check if all answers are correct
        all_correct = all(results.values())

        return render_template('harder_math.html', results=results, user_answers={
            'answer1': answer1,
            'answer2': answer2,
            'answer3': answer3,
            'answer4': answer4
        }, all_correct=all_correct, inventory=get_inventory())

    return render_template('harder_math.html', inventory=get_inventory())


@app.route('/dungeon')
def dungeon():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('dungeon.html', inventory=get_inventory())


@app.route('/sector/<int:sector_number>')
def sector(sector_number):
    if check_backrooms():
        return redirect(url_for('backrooms'))

    if sector_number < 1 or sector_number > 9:
        return redirect(url_for('inicio'))

    # Check if user has unlocked this sector via access code
    unlocked_sectors = session.get('unlocked_sectors', [])

    # Sector 1 is accessible if user reached you_are_not_alone (has A29 classified)
    # Other sectors require their specific code to be entered
    if sector_number not in unlocked_sectors:
        return redirect(url_for('you_are_not_alone'))

    return render_template('sector.html', sector_number=sector_number, inventory=get_inventory())


@app.route('/sector-2')
def sector_2():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_2.html', inventory=get_inventory())


@app.route('/sector-1')
def sector_1():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_1.html', inventory=get_inventory())


@app.route('/sector-8')
def sector_8():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_8.html', inventory=get_inventory())


@app.route('/sector-3')
def sector_3():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_3.html', inventory=get_inventory())


@app.route('/l14-trial')
def l14_trial():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('l14_trial.html', inventory=get_inventory())


@app.route('/e13-trial')
def e13_trial():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('e13_trial.html', inventory=get_inventory())


@app.route('/sector-5')
def sector_5():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_5.html', inventory=get_inventory())


@app.route('/sector-7')
def sector_7():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_7.html', inventory=get_inventory())


@app.route('/sector-9')
def sector_9():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sector_9.html', inventory=get_inventory())


@app.route('/unlock-sector/<int:sector_number>', methods=['POST'])
def unlock_sector(sector_number):
    """Unlock a sector by entering its access code"""
    if sector_number < 1 or sector_number > 9:
        return redirect(url_for('inicio'))

    entered_code = request.form.get('code', '').strip()
    expected_code = SECTOR_CODES.get(sector_number)

    if expected_code and entered_code.upper() == expected_code:
        if 'unlocked_sectors' not in session:
            session['unlocked_sectors'] = []
        if sector_number not in session['unlocked_sectors']:
            session['unlocked_sectors'].append(sector_number)
            session.modified = True
        
        # Redirect to the correct sector route
        sector_routes = {
            1: 'sector_1',
            2: 'sector_2',
            3: 'sector_3',
            5: 'sector_5',
            7: 'sector_7',
            8: 'sector_8',
            9: 'sector_9'
        }
        
        if sector_number in sector_routes:
            return redirect(url_for(sector_routes[sector_number]))
        else:
            return redirect(url_for('you_are_not_alone'))
    else:
        return redirect(url_for('you_are_not_alone'))


@app.route('/add_item', methods=['POST'])
def add_item():
    import json
    item = request.json.get('item')
    if item:
        add_to_inventory(item)
    return {'success': True, 'inventory': get_inventory()}


@app.route('/get_inventory', methods=['GET'])
def get_inventory_route():
    """Get the user's current inventory"""
    return {'success': True, 'inventory': get_inventory()}


@app.route('/backrooms')
def backrooms():
    import random
    # Initialize backrooms attempts counter
    if 'backrooms_attempts' not in session:
        session['backrooms_attempts'] = 0
    
    # Generate a random room number
    room_number = random.randint(1, 1000)
    attempts = session['backrooms_attempts']
    return render_template('backrooms.html', inventory=get_inventory(), room_number=room_number, attempts=attempts)


@app.route('/random-backrooms')
def random_backrooms():
    import random
    # Get current attempts
    attempts = session.get('backrooms_attempts', 0)
    
    # Increment attempts on each visit to this route (whether escape succeeds or fails)
    attempts += 1
    session['backrooms_attempts'] = attempts
    
    if attempts >= 5:
        # Reset inventory and send to home page with death message (lose all progress)
        session['inventory'] = []
        session['backrooms_attempts'] = 0  # Reset attempts
        # Pass a death message to the home page
        session['death_message'] = "You died in the backrooms after 5 failed escape attempts!"
        return redirect(url_for('inicio'))
    
    # 5% chance to escape, 95% chance to go deeper
    if random.random() < 0.05:
        session['backrooms_attempts'] = 0  # Reset attempts on successful escape
        return redirect(url_for('inicio'))
    else:
        # Generate a random room number
        room_number = random.randint(1, 1000)
        return render_template('backrooms.html', inventory=get_inventory(), room_number=room_number, attempts=attempts)


def check_backrooms():
    """Function to check if user should be transported to backrooms (0.5% chance)"""
    import random
    return random.random() < 0.01  # 1% chance


# API routes for the buttons in web.html
@app.route('/api/button1')
def api_button1():
    import datetime
    return {
        "result": "Button 1 was clicked!",
        "message": "This is the response from the backend for button 1.",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "inventory": get_inventory()
    }


@app.route('/api/button2')
def api_button2():
    import datetime
    return {
        "result": "Button 2 was clicked!",
        "message": "This is the response from the backend for button 2.",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "inventory": get_inventory()
    }


@app.route('/api/button3')
def api_button3():
    import datetime
    return {
        "result": "Button 3 was clicked!",
        "message": "This is the response from the backend for button 3.",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "inventory": get_inventory()
    }


@app.route('/authentication')
def authentication():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('authentication.html', inventory=get_inventory())


@app.route('/admin-panel')
def admin_panel():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('admin_panel.html', inventory=get_inventory())


@app.route('/sd--_dasd+!')
def broken_page():
    if check_backrooms():
        return redirect(url_for('backrooms'))
    return render_template('sd--_dasd+!.html', inventory=get_inventory())


if __name__  == '__main__':
    app.run(debug=True, port=5001)