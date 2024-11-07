import pandas as pd
import json
import logging

# Configure logging pour débogage
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Charger les fichiers CSV
criteres_df = pd.read_csv("D:/Ensim/5_A/ipsastre/criteres.csv", encoding='ISO-8859-1')
reponses_df = pd.read_csv("D:/Ensim/5_A/ipsastre/qui_est_tu.csv", encoding='ISO-8859-1')

# Fonction pour calculer le score de chaque étudiant en fonction des critères
def calculer_score_etudiant(row, criteres_df):
    score = 0
    total_ponderation = 0
    criteres_trouves = 0
    
    for _, critere_row in criteres_df.iterrows():
        critere = critere_row['critere']
        ponderation = critere_row['ponderation']
        importance = critere_row['degre_d_importance']
        
        for col in row.index:
            if pd.notnull(row[col]) and critere.lower() in str(row[col]).lower():
                score += ponderation * importance
                total_ponderation += ponderation
                criteres_trouves += 1
                break
    

    ponderation_moyenne = total_ponderation / len(criteres_df) if len(criteres_df) > 0 else 0
    return score, ponderation_moyenne

# Calculer le score et la pondération moyenne pour chaque étudiant
reponses_df[['score', 'ponderation_moyenne']] = reponses_df.apply(
    lambda row: pd.Series(calculer_score_etudiant(row, criteres_df)), axis=1
)

# Remplacer toutes les valeurs NaN par des valeurs par défaut
reponses_df['score'] = reponses_df['score'].apply(lambda x: 0 if isinstance(x, str) and x == "100% ASTRE" else x)
reponses_df = reponses_df.fillna(0)

# Préparer les données pour Highcharts
student_column_name = 'Numero etudiant '
highcharts_data = [
    [
        row[student_column_name],
        row['score'],
        row['ponderation_moyenne'],
        "ASTRE" if row['score'] == 0 else "IPS"
    ]
    for _, row in reponses_df.iterrows()
]

# Sauvegarder les données en JSON
with open("data.json", "w") as f:
    json.dump(highcharts_data, f)
