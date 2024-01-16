import sys
import csv
from icalendar import Calendar

def ics_to_csv(input_file, output_file):
    with open(input_file, 'rb') as f:
        cal = Calendar.from_ical(f.read())

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Écriture de la première ligne de descripteur
        csv_writer.writerow(['SUMMARY', 'DESCRIPTION', 'DTSTART', 'DTEND', 'LOCATION'])

        for event in cal.walk('VEVENT'):
            # Récupération des informations nécessaires
            summary = event.get('SUMMARY', '')
            description = event.get('DESCRIPTION', '')
            start_time = event.get('DTSTART').dt.strftime('%Y-%m-%d %H:%M:%S')
            end_time = event.get('DTEND').dt.strftime('%Y-%m-%d %H:%M:%S')
            location = event.get('LOCATION', '')

            # Écriture des informations dans le fichier CSV
            csv_writer.writerow([summary, description, start_time, end_time, location])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py ADECal.ics ADECal.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    ics_to_csv(input_file, output_file)
    print(f"Conversion terminée. Résultats enregistrés dans {output_file}")
