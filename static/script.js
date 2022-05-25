
// get_specs collects the specs information from app.py
function get_specs() {
    console.log("get_specs has been initiated") // output that the function has been initiated for debugging
    fetch('/specs') // runs a GET request for specs
        .then(function (response){
            return response.json() ;
        }).then(function (text){
            console.log("response is:") ;
            console.log(text) ; 
        })
}

//------------------------------------------------------------
// info.html
//------------------------------------------------------------

// change_table script changes the table that is displayed on info.html
function change_table(selected) {
    console.log("change_table has been initiated with " + selected) ; //output that the function has been initiated for debugging
    var data_json = get_specs() ;
    if (selected == 'placeholder') { //if statement to check if the placeholder has been selected
        console.log("placeholder is selected");
    } else{
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