import mysql.connector

# Use Config class to initiate connection

mydb = mysql.connector.connect(
    host ="164.90.137.194:3306",
    user = "diz21",
    password = "InfSci2710_4600049",
    database = "mtc"
)

my_cursor = mydb.cursor()
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
