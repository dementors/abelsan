// ----------------------------------------
// code breaks all the time because 
// amazon does not like scraping
// e.g. the selectors change all the time
// ----------------------------------------

const fs = require('fs');
const axios = require('axios');
const cheerio = require('cheerio');

// brief list for debugging - see books.json for full list
var books = [
    {
        title : 'The Coming Wave',
        author : 'Mustafa Suleyman',
        isbn : '',
        url : 'https://www.amazon.com/dp/0593728173'
    },
    {
        title : 'Competing in the Age of AI',
        author : 'Marco Iansiti ',
        isbn : '',
        url : 'https://www.amazon.com/dp/1633697622'
    }
]    

async function scrapeBook(url) {
    try {
        // alternative to fetch
        // const { data } = await axios.get(url);
        // const $ = cheerio.load(data);

        // switched to fetch - to avoid amazon blocking
        const response = await fetch(url);
        const body = await response.text();
        const $ = cheerio.load(body);

        // Selector for the book cover image - this will vary based on the website
        const selector = 'img#landingImage';

        // Extracting the 'src' attribute of the book cover image
        const cover = $(selector).attr('src');

        // Selector for the ISBN 10 number
        const selectorISBN = '#rpi-attribute-book_details-isbn10 .rpi-attribute-value span';
        const isbn = $(selectorISBN).text();        

        return { cover, isbn };
    } catch (error) {
        console.error('Error fetching book cover:', error);
    }
    
}

async function downloadImage(book) {
    try {
        const response = await axios({
            method: 'GET',
            url: book.cover,
            responseType: 'stream'
        });

        const writer = fs.createWriteStream('covers/' + book.isbn + '.jpg');

        response.data.pipe(writer);

        return new Promise((resolve, reject) => {
            writer.on('finish', resolve);
            writer.on('error', reject);
        });
    } catch (error) {
        console.error('Error occurred while downloading the image:', error);
    }
}

// Function to create a delay with a random amount of time
function delay() {
    const time = Math.floor(Math.random() * 10000); // Random delay between 0 and 3 secs
    return new Promise(resolve => setTimeout(resolve, time));
}

async function process(books) {
    for (const book of books) {
        console.log('Scrape Book:', book.title);
        var data = await scrapeBook(book.url);        
        if (data.cover) {
            downloadImage(data);
            book.isbn = data.isbn;
        } else {
            console.log('Book cover not found.');
        }
        await delay(); // Wait for the random delay
    }

    // write the books array to a file
    console.log('Writing books to file...'); 
    fs.writeFileSync('working_list.json', JSON.stringify(books));    
}

process(books);
