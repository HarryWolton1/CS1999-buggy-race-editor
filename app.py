from cgitb import reset
from tkinter import *
from typing import final
from urllib import response
from flask import Flask, render_template, request, jsonify
import os
import sqlite3 as sql
from urllib.request import urlopen 
import json
import requests
from bs4 import BeautifulSoup
from flask import Markup

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
    power = Markup(power_table)
    

    #scrapes tyre table from https://rhul.buggyrace.net/specs/data?extra=mass
    tyre_header = soup.find('h3', {'id':'type-tyres'})
    tyre_table = tyre_header.find_next('table')
    tyre = Markup(tyre_table)

    #scrapes armour table from https://rhul.buggyrace.net/specs/data?extra=mass
    armour_header = soup.find('h3', {'id':'type-armour'})
    armour_table = armour_header.find_next('table')
    armour = Markup(armour_table)

    #scrapes attack table from https://rhul.buggyrace.net/specs/data?extra=mass
    attack_header = soup.find('h3', {'id':'type-attack'})
    attack_table = attack_header.find_next('table')
    attack = Markup(attack_table)

    #scrapes algo table from https://rhul.buggyrace.net/specs/data?extra=mass
    algo_header = soup.find('h3', {'id':'type-algo'})
    algo_table = algo_header.find_next('table')
    algo = Markup(algo_table)

    #scrapes flag-pattern table from https://rhul.buggyrace.net/specs/data?extra=mass
    flag_pattern_header = soup.find('h3', {'id':'type-flag_pattern'})
    flag_pattern_table = flag_pattern_header.find_next('table')
    flag_pattern = Markup(flag_pattern_table)

    #scrapes special table from https://rhul.buggyrace.net/specs/data?extra=mass
    special_header = soup.find('h3', {'id':'type-special'})
    special_table = special_header.find_next('table')
    special = Markup(special_table)

    #scrapes defaults table from https://rhul.buggyrace.net/specs/data?extra=mass
    defaults_header = soup.find('h2', {'id':'defaults'})
    defaults_table = defaults_header.find_next('table')
    defaults = Markup(defaults_table)

    return render_template("info.html", power=power, tyre=tyre, armour=armour, attack=attack, algo=algo, flag_pattern=flag_pattern, special=special, defaults=defaults)

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
        url='https://rhul.buggyrace.net/specs/data/defaults.json' #url of the default buggy specs to pre fill in the form
        json_url = urlopen(url) #opens the url
        response = json.loads(json_url.read()) # puts the json response from the web page as a variable
        return render_template("buggy-form.html", buggy=response)


    elif request.method == 'POST':
        msg=""
        max_price = 100 #sets the max price (currently set to 100 as i cannot find the proper value)

        #assigns variables with the data of the form
        buggyID = request.form['id']
        buggyID = buggyID.strip()
        #wheel attibutes
        qty_wheels = request.form['qty_wheels']
        qty_wheels = qty_wheels.strip()
        tyre = request.form['tyre']
        tyre = tyre.strip()

        #flag attributes
        flag_color = request.form['flag_color']
        flag_color = flag_color.strip()
        flag_color_secondary = request.form['flag_color_secondary']
        flag_color_secondary = flag_color_secondary.strip()
        flag_pattern = request.form['flag_pattern']
        flag_pattern = flag_pattern.strip()


        #checks if qty_wheels is a number
        if not qty_wheels.isdigit():
            msg = "wheel quantity should be a number"
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            record = cur.fetchone()
            return render_template("buggy-form.html", msg = msg, buggy = record)
        else:
            qty_wheels = int(qty_wheels)


        #checks number of wheels is even number
        if (qty_wheels % 2) != 0 :
            msg = "wheel quantity must be even"
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            records = cur.fetchall()
            return render_template("buggy-form.html", msg = msg, buggies = records)            



        
        #checks the price is below the max.
        url = 'https://rhul.buggyrace.net/specs/data/types.json' #sets the url as the page where the json output of the specs can be found
        json_url = urlopen(url) #opens the url
        specs = json.loads(json_url.read()) # puts the json response from the web page as a variable
        price = 0 # sets the intitial price to 0
        price_per_tyre = specs['tyres'][tyre]['cost'] #calculates price per tyre by looking for the tyre cost in the json object
        tyre_cost = price_per_tyre * qty_wheels #calculates the cost of the tyres by multiplying the tyre price
        price = tyre_cost + price # adds the tyre_cost to the total cost.



        #checks that the price is lower than the max price.
        if price > max_price:
            msg = "this excedes the max price of the buggy"
            return render_template("updated.html", msg = msg)

        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                if buggyID:
                    cur.execute(
                        "UPDATE buggies set qty_wheels=?, tyres=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, price=? WHERE id=?" ,
                        (qty_wheels, tyre, flag_color, flag_color_secondary, flag_pattern, price, buggyID)
                    )
                else:
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels, tyres, flag_color, flag_color_secondary, flag_pattern, price) VALUES (?,?,?,?,?,?)" ,
                        (qty_wheels, tyre, flag_color, flag_color_secondary, flag_pattern, price)
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
# a page for deleting buggies.
#------------------------------------------------------------
@app.route('/delete/<buggy_id>') 
def delete_buggies(buggy_id):
    print("delete_buggies initiated ")
    print("initiated with delete")
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM buggies WHERE id=?", 
                (buggy_id)
            )
            con.commit()
            msg = "Record succesfully deleted"
    except:
        con.rollback()
        msg = "error in update operation"
    finally:
        con.close() 

    return render_template("delete.html", msg=msg)




#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchall(); 
    return render_template("buggy.html", buggies = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
    record = cur.fetchone(); 
    return render_template("buggy-form.html", buggy = record)

@app.route('/updated')
def update_buggy():
    return render_template("updated.html")

#------------------------------------------------------------
# links to the poster.html page
#------------------------------------------------------------
@app.route('/poster')
def display_poster():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 
    return render_template("poster.html", buggy = record)


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


