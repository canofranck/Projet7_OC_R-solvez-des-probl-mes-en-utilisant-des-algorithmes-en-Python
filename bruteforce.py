import itertools
import time
from datetime import timedelta

def Read_Files(load_files):
    actions = []
    with open(load_files, 'r') as fichier:
        next(fichier)  # Ignorer l'en-tête
        for ligne in fichier:
            action, cout, benefice = ligne.strip().split(',')
            actions.append({'action': action, 'cout': float(cout), 'benefice': float(benefice) / 100})
    return actions


def format_temps(secondes):
    temps_delta = timedelta(seconds=secondes)
    millisecondes = temps_delta.microseconds // 1000
    minutes, secondes = divmod(temps_delta.seconds, 60)
    return "{:02}:{:02}.{:03}".format(minutes, secondes, millisecondes)


def generate_combinaisons(actions):
    all_combinations = []
    
    for r in range(1, len(actions) + 1):
        for combinaison in itertools.combinations(actions, r):
            cout_total = sum(action['cout'] for action in combinaison)
            if cout_total <= 500:
                all_combinations.append(list(combinaison))
    return all_combinations


def calculate_profit(combinaison):
    cout_total = sum(action['cout'] for action in combinaison)
    if cout_total > 500:
        return 0
    return sum(action['cout'] * action['benefice'] for action in combinaison)


def find_best_combinaison(actions):
    best_combinations = []
    best_profits = 0

    all_combinations = generate_combinaisons(actions)

    for combinaison in all_combinations:
        profit = calculate_profit(combinaison)
        if profit > best_profits:
            best_combinations = [combinaison]
            best_profits = profit
            # print(" best combinaisons : ", combinaison)
            # print(" Best profit: ",profit)
            
        elif profit == best_profits:
            best_combinations.append(combinaison)

    return best_combinations, best_profits

# utilisation

load_files = "data/phase1+P7.csv"
actions = Read_Files(load_files)
start_time = time.time()  
best_combinations, best_profits = find_best_combinaison(actions)
end_time = time.time()  
execution_time = end_time - start_time

print("{:<15} {:<10} {:<10}".format("Action", "Cout", "Profit (%)"))
print("="*35)

for combinaison in best_combinations:
    for action in combinaison:
        action_info = [a for a in actions if a['action'] == action['action']][0]
        print("{:<15} {:<10} {:<10.2f}".format(action_info['action'], action_info['cout'], action_info['benefice'] * 100))

cout_total = sum(action_info['cout'] for action_info in actions if action_info['action'] in [a['action'] for a in best_combinations[0]])
print("\nCoût total des actions achetées: {:.2f}".format(cout_total))
print("Profit total: {:.2f}".format(best_profits))
print("Temps d'exécution: {}".format(format_temps(execution_time)))
