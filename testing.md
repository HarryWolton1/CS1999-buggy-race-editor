# testing



## Testing 'show info'
1. To test the 'show info' button I went onto the `index.html` page.
2. Then I checked the terminal in VScode which had the output of `127.0.0.1 - - [14/Jun/2022 16:20:31] "GET /info HTTP/1.1" 200 -` This shows that the route in `app.py` which renders `info.html` has been initiated
3. When I then checked the browser to check what had appeared on the screen.
4. When I did this the `/info` page had fully loaded. I know the web scraping of the tables has worked as the tables show fully on the screen.
5. **This shows that this test has been successfully as the show info page performs as expected**

## Testing 'make buggy'

### Normal test
1. To do this test I will enter data into the form which is correct so the expected result is for this data to be accepted and written into the database.
2. The test data I used for this is
    * number of wheels = `6`
    * type of wheel = `slick`
    * Primary flag color = `purple`
    * Secondary flag color = `red`
    * flag pattern = `spot`
3. When I entered this data and pressed submit I got a message saying `Record successfully saved`
4. To confirm that the buggy has been added to the database I went onto the show buggy page.
5. When I do this I see the buggy that I entered has been added to the database.
6. **This mean that this test has been a success.**

### Odd number of wheels test
1. To do this test I will enter all valid data other than the number of wheels being odd.
2. The expected output of this test is the user will be given the message saying the wheel number is invalid.
3. The test data I used for this is
    * number of wheels = `7`
    * type of wheel = `slick`
    * Primary flag color = `purple`
    * Secondary flag color = `red`
    * flag pattern = `spot`
4. When I ran this test I got a message saying buggy is undefined. 
5. To fix this issue I changed the api to return the data that has been in the form (buggy) to the form
6. This means when I pressed submit again I got a message saying `wheel quantity must be even ` **hence making the test succesfull**

### Wheels is not a number
1. To do this test I will enter all valid data other than the number of wheels being an even number.
2. the expected output of this test is a message telling the user that they have entered an ivalid input
3. The test data I used for this is
    * number of wheels = `number`
    * type of wheel = `slick`
    * Primary flag color = `purple`
    * Secondary flag color = `red`
    * flag pattern = `spot`
4. When I pressed submit I got a message saying `wheel quantity should be a number`
5. **This means that this test has been successfull**

### Testing max price
1. To do this test I will enter a combination of wheels that will make the buggy exceed the max cost
2. The test data I used for this is
    * number of wheels = `20`
    * type of wheel = `slick`
    * Primary flag color = `purple`
    * Secondary flag color = `red`
    * flag pattern = `spot`
3. The expected outcome from this test is a message telling the user that the cost of the buggy exceeds the max cost
4. When I completed this test it opened a page which contained a message ` this excedes the max price of the buggy `
5. **this means the test has been succesfull** however in future development this could be improved to display this message in the buggy form instead of opening this in a new window

## Testing `show buggy`
1. First to do this test I made sure there was enough buggies in the database to test displaying multiple buggies.
2. Then I pressed the `show buggy` button on index.html.
3. This caused the buggy.html page to be opened.
4. the tables where displayed correctly **however** the canvas which was meant to display the flag did not work as intended
5. This means that fixing this is a task that would be required in future development of this project

## Testing editing buggies
1. First I pressed on the edit link on the first buggy in the table
2. This took me to the buggy form however the form was pre-loaded with the data about that specific buggy (as expected)
3. I then changed the wheel type to knobbly and pressed submit
4. This caused a message which said ` Record successfully saved ` to be displayed
5. To check that this change has happened I went to the `show buggy` page again where the tyre type and cost of the buggy had been changed.
6. **this means that this test has been successful**

## Testing deleting buggies 
1. First I went onto the `show buggy` page. 
2. Next I pressed the delete button under the buggy with the id of `2`
3. This caused a message to be displayed to say the buggy has been deleted
4. to check that this has been the case I went back to the `show buggy` page where there was no longer a buggy with the id of `2`
5. **this means that this test has been successfull**