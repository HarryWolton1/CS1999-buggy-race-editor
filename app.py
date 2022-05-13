from cgitb import reset
from flask import Flask, render_template, request, jsonify
import os
import sqlite3 as sql
import requests
from bs4 import BeautifulSoup

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# the info page
#------------------------------------------------------------
@app.route('/info')
def show_info():
    res = requests.get(
       'https://rhul.buggyrace.net/specs/data?extra=mass'
    )
    soup = BeautifulSoup(res.content, 'html.parser')

    #scrapes power table from https://rhul.buggyrace.net/specs/data?extra=mass
    power_header = soup.find('h3', {'id':'type-power_type'}) 
    power_table = power_header.find_next('table')
    power = power_table

    #scrapes tyre table from https://rhul.buggyrace.net/specs/data?extra=mass
    tyre_header = soup.find('h3', {'id':'type-tyres'})
    tyre_table = tyre_header.find_next('table')
    tyre = tyre_table

    #scrapes armour table from https://rhul.buggyrace.net/specs/data?extra=mass
    armour_header = soup.find('h3', {'id':'type-armour'})
    armour_table = armour_header.find_next('table')
    armour = armour_table

    #scrapes attack table from https://rhul.buggyrace.net/specs/data?extra=mass
    attack_header = soup.find('h3', {'id':'type-attack'})
    attack_table = attack_header.find_next('table')
    attack = attack_table

    #scrapes algo table from https://rhul.buggyrace.net/specs/data?extra=mass
    algo_header = soup.find('h3', {'id':'type-algo'})
    algo_table = algo_header.find_next('table')
    algo = algo_table

    #scrapes flag-pattern table from https://rhul.buggyrace.net/specs/data?extra=mass
    flag_pattern_header = soup.find('h3', {'id':'type-flag_pattern'})
    flag_pattern_table = flag_pattern_header.find_next('table')
    flag_pattern = flag_pattern_table

    #scrapes special table from https://rhul.buggyrace.net/specs/data?extra=mass
    special_header = soup.find('h3', {'id':'type-special'})
    special_table = special_header.find_next('table')
    special = special_table

    #scrapes defaults table from https://rhul.buggyrace.net/specs/data?extra=mass
    defaults_header = soup.find('h2', {'id':'defaults'})
    defaults_table = defaults_header.find_next('table')
    defaults = defaults_table

    return render_template("info.html", power=power, tyre=tyre, armour=armour, attack=attack, algo=algo, flag_pattern=flag_pattern, special=special)


#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        return render_template("buggy-form.html")
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=? WHERE id=?",
                    (qty_wheels, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 
    return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    alloc_port = os.environ['CS1999_PORT']
    app.run(debug=True, host="0.0.0.0", port=alloc_port)
