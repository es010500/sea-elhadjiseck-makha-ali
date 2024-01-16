import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Charger le fichier ADECal au format CSV
with open('ADECal.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    data = list(csv_reader)

# Afficher les noms de colonnes pour le débogage
print(data[0].keys())

# Définir la liste des noms de salles de TP
noms_salles_tp = ['RT-Labo Electronique 1', 'RT-Labo Electronique 2', 'RT-Salle Info CAO', 'RT-Labo reseaux 1',
                  'RT-Labo reseaux 2', 'RT-Labo Telecoms 1', 'RT-Labo Telecoms 2', 'RT-Salle Labo Visio',
                  'RT-Labo Informatique 1', 'RT-Labo Informatique 2', 'RT-Labo Informatique 3']

# Filtrer les données pour les salles de TP
filtered_data = [row for row in data if row['LOCATION'] in noms_salles_tp]

# Convertir les colonnes 'DTSTART' et 'DTEND' en datetime et calculer la durée
for row in filtered_data:
    row['DTSTART'] = datetime.strptime(row['DTSTART'], '%Y-%m-%d %H:%M:%S')
    row['DTEND'] = datetime.strptime(row['DTEND'], '%Y-%m-%d %H:%M:%S')
    row['Durée'] = (row['DTEND'] - row['DTSTART']).total_seconds() / 3600

# Calculer le total des heures d'occupation pour chaque salle de TP
heures_par_salle = {}
for row in filtered_data:
    if row['LOCATION'] not in heures_par_salle:
        heures_par_salle[row['LOCATION']] = 0
    heures_par_salle[row['LOCATION']] += row['Durée']

# Afficher le tableau
for location, duration in heures_par_salle.items():
    print(f"{location}: {duration} minutes")

# Enregistrer le tableau au format CSV
with open('resultat_salle_occupation.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['LOCATION', 'Durée'])
    for location, duration in heures_par_salle.items():
        csv_writer.writerow([location, duration])

# Créer et enregistrer l'histogramme
locations = list(heures_par_salle.keys())
durations = list(heures_par_salle.values())

plt.bar(locations, durations)
plt.xlabel('Nom de la salle')
plt.ylabel("Nombre d'heures d'occupation")
plt.title('Occupation des salles de TP')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('histogramme_salle_occupation.png')
plt.show()
