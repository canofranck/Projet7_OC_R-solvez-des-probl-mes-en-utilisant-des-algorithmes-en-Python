import time
from datetime import timedelta

def Read_Files(load_files):
    # Fonction pour lire les fichiers et extraire les informations sur les actions
    actions = []
    with open(load_files, 'r') as fichier:
        next(fichier)  # Ignorer l'en-tête
        for ligne in fichier:
            action, cout, pourcentage_profit = ligne.strip().split(',')

            cout = float(cout) if float(cout) > 0 else 0
            pourcentage_profit = float(pourcentage_profit) if float(pourcentage_profit) > 0 else 0

            # Calcul du profit réel en utilisant le pourcentage
            profit = (cout * pourcentage_profit) / 100

            actions.append({'action': action, 'cout': cout, 'profit': profit})
    return actions

def format_temps(secondes):
    # Fonction pour formater le temps en minutes, secondes et millisecondes
    temps_delta = timedelta(seconds=secondes)
    millisecondes = temps_delta.microseconds // 1000
    minutes, secondes = divmod(temps_delta.seconds, 60)
    return "{:02}:{:02}.{:03}".format(minutes, secondes, millisecondes)

def dynamic_knapsack(actions, max_cost):
    # Fonction pour résoudre le problème du sac à dos avec la programmation dynamique
    # Filtrer les actions ayant un coût ou un profit nul
    actions = [a for a in actions if a['cout'] > 0 and a['profit'] > 0]

    # Si aucune action n'a de coût ou de profit non nul, retourner une liste vide
    if not actions:
        return [], 0
    # Initialisation d'une table dp pour stocker les résultats intermédiaires
    n = len(actions)
    dp = [[0] * (max_cost + 1) for _ in range(n + 1)]

    # Initialisation de total_cost
    total_cost = 0
    # Boucle pour remplir la table dp avec les résultats optimaux
    for i in range(1, n + 1):
        for j in range(max_cost + 1):
            if actions[i - 1]['cout'] <= j:
                # Choix entre inclure ou exclure l'action actuelle pour maximiser le profit
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - int(actions[i - 1]['cout'])] + actions[i - 1]['cout'] * actions[i - 1]['profit'])

    # Reconstruction de la meilleure combinaison à partir de la table dp
    j = max_cost
    best_combination = []
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            # Vérifier si le coût total ne dépasse pas la limite avant d'ajouter l'action à la meilleure combinaison
            if actions[i - 1]['cout'] <= max_cost - total_cost:
                best_combination.append(actions[i - 1]['action'])
                total_cost += actions[i - 1]['cout']

    return best_combination, dp[n][max_cost]

# Utilisation
load_files = "data/phase1+P7.csv"
actions = Read_Files(load_files)
max_cost = 500

start_time = time.time()
best_combination, best_profit = dynamic_knapsack(actions, max_cost)
end_time = time.time()
execution_time = end_time - start_time

# Affichage des résultats avec des commentaires
print("\nRécapitulatif des actions sélectionnées:")
print("{:<15} {:<10} {:<10}".format("Action", "Cout", "Profit "))
print("="*35)

total_profit = 0  # Ajout d'une variable pour calculer le profit total

for action in best_combination:
    action_info = [a for a in actions if a['action'] == action][0]
    total_profit += action_info['profit']  # Ajout du profit de l'action à la variable total_profit
    print("{:<15} {:<10} {:<10.2f}".format(action_info['action'], action_info['cout'], action_info['profit'] ))

cout_total = sum(action_info['cout'] for action_info in actions if action_info['action'] in best_combination)
print("\nCoût total des actions achetées: {:.2f}".format(cout_total))
print("Profit total: {:.2f}".format(total_profit))  # Utilisation de la variable total_profit
print("Temps d'exécution: {}".format(format_temps(execution_time)))