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
def meilleur_combinaison(actions, max_cost):
    meilleur_combination = []
    meilleur_profit = 0
    

    # Générer toutes les combinaisons possibles de actions
    for i in range(1 << len(actions)):
        combinaison= []
        for j in range(len(actions)):
            if (i & (1 << j)) > 0:
                combinaison.append(actions[j])
         # Calculer le coût total de la combinaison
        cout_total = 0
        for action in combinaison:
            cout_total += action['cout']
        profit_total = sum(action['cout'] * action['benefice'] for action in combinaison)

        # Vérifier si la combinaison respecte la limite de coût et a un meilleur profit
        if cout_total <= max_cost and profit_total > meilleur_profit:
            meilleur_combination = combinaison
            meilleur_profit = profit_total

    return meilleur_combination, meilleur_profit

def afficher_resultats(meilleur_combinaison, meilleur_profit, temps_execution):
    print("\nAction          Cout       Profit (%)")
    print("=" * 40)

    for action in meilleur_combinaison:
        print("{:<15} {:<10.1f} {:<10.2f}".format(action['action'], action['cout'], action["benefice"] * action["cout"]))

    cout_total = sum(action['cout'] for action in meilleur_combinaison)
    print("\nCoût total des actions achetées: {:.2f}".format(cout_total))
    print("Profit total: {:.2f}".format(meilleur_profit))
    print("Temps d'exécution: {}".format(format_temps(temps_execution)))
    
# Exemple d'utilisation avec des actions fictives

limite_achat = 500

load_files = "data/phase1+P7.csv"
actions = Read_Files(load_files)
start_time = time.time()  
resultat_combinaison, resultat_profit = meilleur_combinaison(actions, limite_achat)
end_time = time.time()  
execution_time = end_time - start_time
afficher_resultats(resultat_combinaison, resultat_profit, execution_time)