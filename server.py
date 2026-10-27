import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Données du serveur ULC 27
donnees_serveur = {
    "palmares_ballon_dor": [
        {
            "annee": "2026",
            "date": "Octobre 2026",
            "prenom": "Harry",
            "nom": "Kane",
            "club": "Bayern Munich",
        },
        {
            "annee": "2025",
            "date": "Décembre 2025",
            "prenom": "Lionel",
            "nom": "Messi",
            "club": "Inter Miami",
        },
    ],
    "classement": [
        {"position": 1, "equipe": "Real Madrid low-poly", "points": 42},
        {"position": 2, "equipe": "PSG All-Stars", "points": 39},
    ],
}

database_joueurs_packs = [
    {
        "nom": "Kylian Mbappé",
        "note": 91,
        "type": "Rare Or",
        "equipe": "France / Real",
    },
    {
        "nom": "Lionel Messi",
        "note": 90,
        "type": "Rare Or",
        "equipe": "Argentine",
    },
    {
        "nom": "Harry Kane",
        "note": 92,
        "type": "Ballon d'Or 2026",
        "equipe": "Angleterre",
    },
]


@app.route("/api/donnees", methods=["GET"])
def get_donnees():
  return jsonify(donnees_serveur)


@app.route("/api/ouvrir_pack", methods=["POST"])
def ouvrir_pack():
  joueur_obtenu = random.choice(database_joueurs_packs)
  return jsonify({"succes": True, "joueur_affiche": joueur_obtenu})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)