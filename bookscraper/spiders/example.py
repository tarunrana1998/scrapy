import mysql.connector
import scrapy
from bookscraper.utils import send_email  # Import the common send_email function

class ExampleSpider(scrapy.Spider):
    name = "example_spider"
    start_urls = ['https://books.toscrape.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_config = {
            'host' : '193.203.184.6',
            'user' : 'u522708214_scrapy',
            'password' : 'Scrapy2024',
            'database' : 'u522708214_scrapy'
        }
        self.conn = self.connect_to_db()
        self.cursor = self.conn.cursor()
        self.create_table()

    def connect_to_db(self):
        """Establish a connection to the MySQL database."""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            self.logger.error(f"Error connecting to MySQL: {err}")
            raise

    def create_table(self):
        """Create the books table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE
        )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def check_if_book_seen(self, name):
        """Check if the book is already in the database."""
        check_query = "SELECT COUNT(*) FROM books WHERE name = %s"
        self.cursor.execute(check_query, (name,))
        return self.cursor.fetchone()[0] > 0

    def add_book_to_db(self, name):
        """Add a new book to the database."""
        try:
            insert_query = "INSERT INTO books (name) VALUES (%s)"
            self.cursor.execute(insert_query, (name,))
            self.conn.commit()
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting data into MySQL: {err}")

    def parse(self, response):
        books = response.css('article.product_pod')
        new_data_flag = False  # Track if new data is found

        for book in books:
            name = book.css('h3 a::text').get()
            price = book.css('div.product_price .price_color::text').get()
            url = response.urljoin(book.css('h3 a').attrib['href'])

            # If the book is new, process it
            if not self.check_if_book_seen(name):
                self.add_book_to_db(name)  # Add to the database
                new_data_flag = True  # Mark new data was found

                # Yield the new book's data
                yield {
                    'name': name,
                    'price': price,
                    'url': url,
                }

        # If new data was found, send an email
        if new_data_flag:
            send_email(
                self.settings,
                subject="New Data Added",
                body="New books have been added to the database.",
                to=["tarunrana1997@gmail.com"]
            )

    def closed(self, reason):
        """Close the database connection when the spider finishes."""
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
