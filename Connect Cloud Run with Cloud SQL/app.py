# Import Python libraries
import mysql.connector
from flask import Flask, render_template, request, send_file
import csv

# Establish Connetion
cnx = mysql.connector.connect(user='root'
    , password='Password1234'
    , host='34.88.19.185'
    , database='offdig22')

cursor = cnx.cursor()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

ORG = [
    "Andet",
    "2021.ai",
    "7N A/S",
    "A-2 A/S",
    "Aety ApS",
    "Albertslund Kommune - Kombit Monopolbrud(EAN)"
]

# Create mysql table
query = ("CREATE TABLE IF NOT EXISTS customers (navn VARCHAR(255), email VARCHAR(255), telefonnummer VARCHAR(255), titel VARCHAR(255), organisation VARCHAR(255), emne VARCHAR(255), ønsker VARCHAR(255), talt VARCHAR(255), partner VARCHAR(255), point VARCHAR(255))")
cursor.execute(query)

@app.route("/", methods=["GET", "POST"])
def index():

    # Retrieve data from form
    if request.method == "POST":

        navn = request.form.get("navn")
        email = request.form.get("email")
        telefonnummer = request.form.get("telefonnummer")
        titel = request.form.get("titel")
        organisation = request.form.get("organisation")
        emne = request.form.get("emne")
        ønsker = request.form.get("ønsker")
        talt = request.form.get("talt")
        partner = request.form.get("partner")
        point = request.form.get("point")

        # Add info to customers table (remember that '%s' is a placeholder)
        cursor.execute("INSERT INTO customers (navn, email, telefonnummer, titel, organisation, emne, ønsker, talt, partner, point) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (navn, email, telefonnummer, titel, organisation, emne, ønsker, talt, partner, point))
        cnx.commit()

        # Store datatable in registrants variable
        cursor.execute("SELECT * FROM customers ORDER BY navn")
        registrants = cursor.fetchall()

        return render_template("done.html", registrants=registrants)

    else:
        # Count the number of rows
        cursor.execute("SELECT COUNT(navn) FROM customers")
        count = cursor.fetchone() #return a tuple

        return render_template("index.html", org=ORG, count=count[0])

@app.route("/download")
# create function to download database as csv file
def download():
    # Store datatable in registrants variable
    cursor.execute("SELECT * FROM customers ORDER BY navn")
    registrants = cursor.fetchall()

    # Create a csv file
    with open("registrants.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Navn", "Email", "Telefonnummer", "Titel", "Organisation", "Emne", "Ønsker", "Talt", "Partner", "Point"])
        for registrant in registrants:
            writer.writerow(registrant)

    # Download the csv file
    return send_file("registrants.csv", as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)