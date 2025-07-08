from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load symptom data
with open('medical_permutation.json') as f:
    data = json.load(f)

# Get primary symptom list
primary_symptoms = list(data.keys())

@app.route("/", methods=["GET", "POST"])
def index():
    selected_primary = None
    selected_secondary = None
    secondary_symptoms = []
    diagnosis = None

    if request.method == "POST":
        selected_primary = request.form.get("primary")
        selected_secondary = request.form.get("secondary")

        # Update secondary symptom list if primary is selected
        if selected_primary in data:
            secondary_symptoms = list(data[selected_primary].keys())

        # Handle full diagnosis request
        if selected_primary and selected_secondary:
            symptom_info = data[selected_primary].get(selected_secondary)
            if symptom_info:
                diagnosis = {
                    "combo": f"{selected_primary} + {selected_secondary}",
                    "disease": symptom_info.get("Disease", "Unknown"),
                    "treatment": symptom_info.get("Treatment", []),
                    "notes": symptom_info.get("Notes", ""),
                    "common": symptom_info.get("Common Disease", ""),
                    "healing": symptom_info.get("Expected Healing Time", "")
                }

    return render_template("index.html",
                           primary_symptoms=primary_symptoms,
                           selected_primary=selected_primary,
                           secondary_symptoms=secondary_symptoms,
                           selected_secondary=selected_secondary,
                           diagnosis=diagnosis)

if __name__ == "__main__":
    app.run(debug=True)
