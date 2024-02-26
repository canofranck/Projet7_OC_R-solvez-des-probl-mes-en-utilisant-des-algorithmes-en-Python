import time
from datetime import timedelta
import sys
def Read_Files(load_files):
    actions = []
    with open(load_files, 'r') as fichier:
        next(fichier)  # Ignorer l'en-tête
        for ligne in fichier:
            action, cout, benefice = ligne.strip().split(',')
            actions.append({'nom': action, 'cout': float(cout), 'benefice': float(benefice) / 100})
    return actions

def format_temps(secondes):
    temps_delta = timedelta(seconds=secondes)
    millisecondes = temps_delta.microseconds // 1000
    minutes, secondes = divmod(temps_delta.seconds, 60)
    return "{:02}:{:02}.{:03}".format(minutes, secondes, millisecondes)


def maximiser_profit_dynamique(actions, max_budget):
    # Nombre total d'actions
    n = len(actions)

    # Création d'une liste bidimensionnelle pour stocker les résultats intermédiaires
    dp = []

    # Initialisation de la liste avec des zéros
    for _ in range(n + 1):
        dp.append([0] * (max_budget + 1))

    # Boucle pour chaque action
    for i in range(1, n + 1):
        # Exclure les actions dont le coût est égal à zéro
        if actions[i - 1]["cout"] == 0:
            continue

        # Boucle pour chaque budget possible
        for budget in range(max_budget + 1):
            # Coût et bénéfice de l'action en cours
            cost = actions[i - 1]["cout"]
            benefit = actions[i - 1]["benefice"]

            # Ne pas inclure l'action i
            exclude_action_i = dp[i - 1][budget]

            # Inclure l'action i si possible
            include_action_i = 0
            if budget >= cost:
                include_action_i = dp[i - 1][int(budget - cost)] + cost * benefit

            # Choix entre inclusion et exclusion
            dp[i][budget] = max(exclude_action_i, include_action_i)

    # Récupérer les actions sélectionnées
    selected_actions = []
    i, budget = n, max_budget
    while i > 0 and budget > 0:
        if dp[i][int(budget)] != dp[i - 1][int(budget)]:
            selected_actions.append(actions[i - 1])
            budget -= actions[i - 1]["cout"]
        i -= 1

    # Retourner le résultat avec les actions sélectionnées et le profit total
    return {"actions_selectionnees": selected_actions, "profit_total": dp[n][max_budget]}



def afficher_resultat(resultat, max_cost, execution_time):
    print("Récapitulatif des actions sélectionnées:")
    print("{:<15} {:<10} {:<10}".format("Action", "Cout", "Benefice"))
    print("=" * 35)

    total_cost = sum(action["cout"] for action in resultat["actions_selectionnees"])
    total_profit = resultat["profit_total"]

    for action in resultat["actions_selectionnees"]:
        nom = action["nom"]
        cout = "{:.2f}".format(action["cout"])
        benefice = "{:.2f}".format(action["benefice"] * action["cout"])

        print("{:<15} {:<10} {:<10}".format(nom, cout, benefice))

    print("=" * 35)
    print("Coût total des actions achetées: {:.2f}".format(total_cost))
    print("Profit total: {:.2f}".format(total_profit))
    print("Temps d'exécution: {}".format(format_temps(execution_time)))


# Utilisation
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python glouton.py <file_path>")
        sys.exit(1)
        
    file_path = "data/" +sys.argv[1]
    max_cost = 500
    actions = Read_Files(file_path)
    start_time = time.time()
    resultat_final = maximiser_profit_dynamique(actions, max_cost)
    end_time = time.time()
    execution_time = end_time - start_time

# Affichage des résultats
afficher_resultat(resultat_final, max_cost, execution_time)


# Big-O :
#     Complexité temporelle : exponentiel
#                             O(2^n)
#                             

#     Complexité spatiale : lineaire
#                           O (n)
#                           

