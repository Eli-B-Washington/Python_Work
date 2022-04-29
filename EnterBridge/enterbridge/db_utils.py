from ast import excepthandler
import mysql.connector
from mysql.connector import errorcode

db = mysql.connector.connect(host='localhost',database='enterbridge',user='root',password='')

cursor = db.cursor()


#returns book data
def get_book():
    try:
        cursor.execute("SELECT * FROM book")
        myresult = cursor.fetchall()
    except:
        print("Something went wrong with the transaction")
    cursor.close()
    return myresult

#inserts or updates to the book table
def book_insert_or_update(ISBN, Publisher, PublicationDate, Series, EditionDescription, Pages, SalesRank, ProductWidth, ProductHeight, ProductDepth, Price):
    values = (ISBN, Publisher, PublicationDate, Series, EditionDescription,
              Pages, SalesRank, ProductWidth, ProductHeight, ProductDepth, Price)
    print(values)
    sqlStatement = "INSERT INTO book (`ISBN-13`, Publisher, PublicationDate, Series, EditionDescription, Pages, SalesRank, ProductWidth, ProductHeight, ProductDepth, Price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" #ON DUPLICATE KEY UPDATE ISBN = %s, Publisher = %s, PublicationDate = %s, Series = %s, EditionDescription = %s,Pages = %s, SalesRank = %s, ProductWidth = %s, ProductHeight = %s, ProductDepth = %S, Price = %s)"
    try:
        cursor.execute(sqlStatement, values)
        db.commit()
    except:
        print("Something went wrong with the transaction")
        db.rollback()
    cursor.close()    
    return

