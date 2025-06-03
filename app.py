from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Game data with different faction sets
FACTION_SETS = {
    "Advanced Factions": ["Sime", "Utel", "Casi", "Orea", "Visah", "Arti","Capen", "Nica", "Ria", "Cecro", "Jemit", "Saha","Iber", "Ligu", "Carpa"],
    "Basic Factions": ["Lama", "Cypri", "Pomon", "Ana", "Sini"]
}

MATS = [
    "Langstrom", "The Log", "Warré", "Skep", "Poppleton"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_players = int(request.form['players'])
        selected_sets = request.form.getlist('faction_sets')
        
        # Validate input
        if num_players < 1 or num_players > 5:
            return "Invalid number of players (must be 1-5)"
        if not selected_sets:
            return "Please select at least one faction set"
        
        # Generate setup
        setup = generate_setup(num_players, selected_sets)
        return render_template('result.html', setup=setup)
    
    return render_template(
        'index.html',
        faction_sets=FACTION_SETS.keys(),
        FACTION_SETS=FACTION_SETS
    )

def generate_setup(num_players, selected_sets):
    # Combine selected faction sets
    available_factions = []
    for set_name in selected_sets:
        available_factions.extend(FACTION_SETS[set_name])
    
    # Randomly select mats (no duplicates)
    selected_mats = random.sample(MATS, num_players)
    
    # Handle basic set differently (single factions only)
    if selected_sets == ["Basic Factions"]:
        random.shuffle(available_factions)
        factions = available_factions[:num_players]
        return {
            'num_players': num_players,
            'mats': selected_mats,
            'factions': factions,  # Single factions instead of pairs
            'selected_sets': selected_sets,
            'is_basic': True
        }
    else:
        # Normal handling with pairs
        random.shuffle(available_factions)
        faction_pairs = []
        for i in range(num_players):
            if i*2+1 < len(available_factions):
                pair = (available_factions[i*2], available_factions[i*2+1])
            elif i*2 < len(available_factions):
                pair = (available_factions[i*2], None)
            else:
                pair = (None, None)
            faction_pairs.append(pair)
        
        return {
            'num_players': num_players,
            'mats': selected_mats,
            'faction_pairs': faction_pairs,
            'selected_sets': selected_sets,
            'is_basic': False,
            'all_factions': available_factions
        }

if __name__ == '__main__':
    app.run(debug=True)