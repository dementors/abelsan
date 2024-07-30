Steps to create your own book list. Here is what mine looks like in the end:
https://abel.mit.edu/#/books

Step 01: Build a Json file. I used amazon data. See the format here:
https://abel.mit.edu/assets/generators/books.json

    {
        "title": "The Biology of Business: Decoding the Natural Laws of Enterprise",
        "author": "John Henry Clippinger",
        "isbn": "078794324X",
        "url": "https://www.amazon.com/dp/078794324X"
    }

Step 02: Getting the book cover images programmatically. Note that the code will break all the time because amazon does not like scraping - they change the html tag selectors all the time. The last 10 I had to do by hand
https://abel.mit.edu/assets/generators/book_covers.js

Step 03: Generating the HTML
https://abel.mit.edu/assets/generators/books.js

Step 04: Sample output
view-source:https://abel.mit.edu/assets/docs/books.html

------------------------------------------------------------------------

Alternatives to Amazon.

-----------
WORLDCAT
-----------
First search by ISBN
https://search.worldcat.org/search?q=bn:078794324X

Then follow first link
https://search.worldcat.org/title/44960660

Then read subjects

---------------
LibraryThing
---------------
Link structure
http://www.librarything.com/isbn/1633697622

peterparker
park1980
peter.parker.data@gmail.com

Token - not needed, use direct link
64232a16460ae09def15bcc18611b4f8
&apikey=64232a16460ae09def15bcc18611b4f8