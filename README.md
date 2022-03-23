# Phase2Checkpoint

Technologies/Libraries Used:
1. Python
2. Flask
3. SQLlite
4. Pandas

createTables(): Opens a connenction and Creates all the respective tables

load_data(): Opens all the CSV files and inserts the data into the proper tables

checkCredentials(email, passwordUser): Takes in parameters and checks if the username and password exist and match in DB

checkPasswords(userPassword, dbPassword): Checks if the password of User matches password in DB

index(): 
  When a GET call occurred --> template was automatically rendered
  When a POST call occured -->  a string val was assigned with success or failure message, which led to the template being rendered and the string value being referenced in the html template code(Jinja)
