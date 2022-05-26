from cgitb import reset
from tkinter import W
from flask import Flask, render_template, request, jsonify
import os
import sqlite3 as sql
from urllib.request import urlopen 
import json


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
    return render_template("info.html")

#------------------------------------------------------------
# getting the specifications from the buggy race server
#------------------------------------------------------------
@app.route('/specs', methods = ['GET'])
def show_specs():
    print("show_specs has been initiated") # prints that the api has been ititiated for debugging
    if request.method == 'GET' :
        print("GET initiated") #prints that the GET part has been initiated for debugging 
        url = 'https://rhul.buggyrace.net/specs/data/types.json' #sets the url as the page where the json output of the specs can be found
        json_url = urlopen(url) #opens the url
        specs = json.loads(json_url.read()) # puts the json response from the web page as a variable
        return specs #returns the json object
    else:
        return "This method only accepts GET" # returns that only GET is accepted for debugging


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
        
        #assigns variables with the data of the form
        #wheel attibutes
        qty_wheels = request.form['qty_wheels']
        qty_wheels = qty_wheels.strip()
        wheel_type = request.form['wheel_type']
        wheel_type = wheel_type.strip()
        #flag attributes
        flag_color = request.form['flag_color']
        flag_color = flag_color.strip()
        flag_color_secondary = request.form['flag_color_secondary']
        flag_color_secondary = flag_color_secondary.strip()
        flag_pattern = request.form['flag_pattern']
        flag_pattern = flag_pattern.strip()
        
        #checks if qty_wheels is a number
        if qty_wheels.isdigit() == False:
            msg = "wheel quantity should be a number"
            return msg


        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=? WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, DEFAULT_BUGGY_ID)
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


