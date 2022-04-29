from db_utils import book_insert_or_update
import db_utils
import json
import helper

#reads in JSON files and Inserts to the database
def main():
    #retrieving JSON Data
    f = open('eli.json')
    data = json.load(f)
    ISBN = data[0]['ISBN-13']
    Publisher = data[0]['Publisher']
    PublicationDate = data[0]['PublishlicationDate']
    Series = data[0]['Series']
    EditionDescription = data[0]['Series']
    Pages = data[0]['Pages']
    SalesRank = data[0]['SalesRank']
    ProductDimensions = data[0]['ProductDimensions']
    #seperating width, heighth, and depth from product dimensions
    ProductWidth = helper.getWidth(ProductDimensions)
    ProductHeight = helper.getHeight(ProductDimensions)
    ProductDepth = helper.getDepth(ProductDimensions)
    Price = data[0]['Price']
    #command to Insert to DB
    db_utils.book_insert_or_update(ISBN, Publisher, PublicationDate, Series, EditionDescription, Pages, SalesRank, ProductWidth, ProductHeight, ProductDepth, Price)



if __name__ == "__main__":
    main()