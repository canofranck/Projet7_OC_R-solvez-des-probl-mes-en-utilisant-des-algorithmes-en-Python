import time
from datetime import timedelta

def Read_Files(load_files):
    # Fonction pour lire les fichiers et extraire les informations sur les actions
    actions = []
    with open(load_files, 'r', encoding='iso-8859-1') as fichier:
        next(fichier)  # Ignorer l'en-tête
        for ligne in fichier:
           
            action, cout, pourcentage_profit = ligne.strip().split(',')
            if float(cout)>0 and float(pourcentage_profit)>0:
                #l algo marche qu avec des nombre entier 
                cout_int = int(float(cout)*100 ) 
                # Calcul du profit réel en utilisant le pourcentage  et en le metant en entier aussi 
                profit= int(round(float(cout)* float(pourcentage_profit)/100, 2)*100)

                actions.append({'action': action, 'cout': cout_int, 'profit': profit})
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
    dp  = [[0 for x in range(max_cost + 1)] for x in range(n+ 1)]

    # Initialisation de total_cost
    total_cost = 0
    # Boucle pour remplir la table dp avec les résultats optimaux
    for i in range(1, n + 1):
        #on saute la premiere colonne
        for j in range(1,max_cost + 1):
            if actions[i - 1]['cout'] <= j:
                # Choix entre inclure ou exclure l'action actuelle pour maximiser le profit
                """
                dp[i][j] = max(
                    dp[i - 1][j], 
                    dp[i - 1][j - int(actions[i - 1]['cout'])] + actions[i - 1]['cout'] * actions[i - 1]['profit'])
                """
                #  on prend la decision enrre l achat de de la ligne precedente de celui en cours 
                #si meilleire ou peuvent etre combiner
                dp[i][j]= max( 
                        dp[i-1][j],
                        actions[i-1]['profit'] + dp[i-1][j - actions[i-1]['cout']],)
            else:#else manquant 
                # keep result of previous line if highter
                    dp[i][j] = dp[i-1][j]

    # Reconstruction de la meilleure combinaison à partir de la table dp
    j = max_cost
    n = len(actions)
    best_combination = []
    """
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            # Vérifier si le coût total ne dépasse pas la limite avant d'ajouter l'action à la meilleure combinaison
            if actions[i - 1]['cout'] <= max_cost - total_cost:
                best_combination.append(actions[i - 1]['action'])
                total_cost += actions[i - 1]['cout']
    """
    # while there is money in wallet and elements
    while j >= 0 and n >= 0:

        # take the last element in list
        e = actions[n-1]
        # calc the difference between two last line for find selected elements
        if dp[n][j] == dp[n-1][j - e["cout"]] + e["profit"]:
            best_combination.append(e)
            j -= e["cout"]
        n -= 1

    ttcost = 0
    action_format = []
    for i in best_combination:
            # generate cost value
            ttcost += i["cout"] 
            # format action selection value
            action_format.append(i)

    # Format total cost value
    ttcost = ttcost/100
    print(ttcost, (dp[-1][-1])/100, action_format, max_cost/100)

    return ttcost, (dp[-1][-1])/100, action_format, max_cost/100
# Utilisation
load_files = "data/dataset2_Python+P7.csv"
actions = Read_Files(load_files)
#comme le cout a ete multiplier pr mille aussi faudra remtre *100 sur le montant 
max_cost = 500*100

start_time = time.time()
cost , benefit,best_combination,wallet = dynamic_knapsack(actions, max_cost)
end_time = time.time()
execution_time = end_time - start_time
# Affichage des résultats avec des commentaires
print("\nRécapitulatif des actions sélectionnées:")
print("{:<15} {:<10} {:<10}".format("Action", "Cout", "Profit "))
print("="*35)



total_profit = 0  # Ajout d'une variable pour calculer le profit total

for action in best_combination: 
    
    print("{:<15} {:<10} {:<10.2f}".format(action['action'], action['cout']/100, action['profit']/100 ))

print("\nCoût total des actions achetées: {:.2f}".format(cost))
print("Profit total: {:.2f}".format(benefit))  # Utilisation de la variable total_profit
print("Temps d'exécution: {}".format(format_temps(execution_time)))
