
// get_specs collects the specs information from app.py
function get_specs() {
    console.log("get_specs has been initiated") // output that the function has been initiated for debugging
    var data_json = 1 ; 
    fetch('/specs') // runs a GET request for specs
            .then(function (response){
                return response.json() ;
         }).then(function (text){
             console.log("get_specs json object" + text) ; //prints the json object
             data_json = text ; 
        })
    return data_json
}

//------------------------------------------------------------
// info.html
//------------------------------------------------------------

// this code is now not used as it will not work correctly
// change_table script changes the table that is displayed on info.html
function change_table(selected) {
    console.log("change_table has been initiated with " + selected) ; //output that the function has been initiated for debugging
    var data_json = get_specs() ; // creates a json object that contains the specs of the buggy
    console.log("recieved data " + data_json) ; //prints the json object that has been returned for debugging 
    if (selected == 'placeholder') { //if statement to check if the placeholder has been selected
        console.log("placeholder is selected");
    } else{
        console.log[data_json]
        table_data = data_json[selected] ; //creates a new object with only the data that is required for the table
        var text = "<table>" ;
        for (column in table_data) {
            text += "<tr>"
            for (row in column) {
                text += "<td>" + table_data[column][row].name + "</td>" ;

            }
            text += "</tr>" ;
        }
        text =+ "</table>" ;
        document.getElementById("specs_table").innerHTML = text ;
    }

}

//------------------------------------------------------------
// buggy_form.html
//------------------------------------------------------------

//function to autofill the table with standard values
function autofill() {
    console.log("autofill has been initiated with ") ; // output that the function has been initiated for debugging.
    var wheel_quantity = 4 ; 
    var tyre = "knobbly" ;
    var flag_color = "white" ; 
    var flag_color_secondary = "black" ; 
    var flag_pattern = "plain" ; 

    if (document.getElementsByName("qty_wheels") = "") { // checks if the value of wheel quantity in the form is empty
        document.getElementsByName("qty_wheels").value = wheel_quantity ; // sets the value of wheel quantity to the default value
    }
    if (document.getElementsByName("tyre") = "") { // checks if the value of tyre in the form is empty
        document.getElementsByName("tyre").value = tyre ; // sets the value of tyre quantity to the default value
    }
    if (document.getElementsByName("flag_color") = "") { // checks if the value of flag color in the form is empty
        document.getElementsByName("flag_color").value = flag_color ; // sets the value of flag color to the default value
    }
    if (document.getElementsByName("flag_color_secondary") = "") { // checks if the value of flag color secondary in the form is empty
        document.getElementsByName("flag_color_secondary").value = flag_color_secondary ; // sets the value of flag color secondary to the default value
    }
    if (document.getElementsByName("flag_pattern") = "") { // checks if the value of flag pattern in the form is empty
        document.getElementsByName("flag_pattern").value = flag_pattern ; // sets the value of flag pattern to the default value
    }
}


// function to add the dropdown menu of buggy id
function buggy_list(buggy) {
    var index = buggy[id] ; // sets index to be the id column of the buggies column
    var text = "<select id='buggy_select'>" ; // creates the variable text which contains the html for the dropdown menu

    for (i in index) { //increments through all the id's in the buggy table
        text =+ "<option value='" + i + "'>" + i + "</option>" ; // adds the row to the dropdown
    }

    text =+ "</select>"
    document.getElementById("buggy_select").innerHTML = text ; // adds the text into the html page
}