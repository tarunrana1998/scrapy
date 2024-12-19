from scrapy.mail import MailSender
import scrapy
import os
from bookscraper.utils import send_email  # Import the send_email function

class ExampleSpider(scrapy.Spider):
    name = "example_spider"
    start_urls = ['https://books.toscrape.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_file = "seen_books.txt"  # File to store previously seen book names
        self.seen_books = set()  # In-memory set to track seen books
        self.load_seen_books()

    def load_seen_books(self):
        """Load previously seen book names from the file."""
        if os.path.exists(self.seen_file):
            with open(self.seen_file, "r") as file:
                self.seen_books = set(file.read().splitlines())

    def save_seen_books(self):
        """Save the updated list of seen book names to the file."""
        with open(self.seen_file, "w") as file:
            file.write("\n".join(self.seen_books))

    def parse(self, response):
        books = response.css('article.product_pod')
        new_data_flag = False  # Track if new data is found

        for book in books:
            name = book.css('h3 a::text').get()
            price = book.css('div.product_price .price_color::text').get()
            url = response.urljoin(book.css('h3 a').attrib['href'])
            print(name)
            # If the book name is new, process it
            if name not in self.seen_books:
                self.seen_books.add(name)  # Add to the in-memory set
                new_data_flag = True  # Mark that new data was found

                # Log or yield the new data (optional)
                yield {
                    'name': name,
                    'price': price,
                    'url': url,
                }

        # Save the updated list of seen books to the file
        self.save_seen_books()

        # If new data was found, send an email
        if new_data_flag:
            send_email(
                self.settings,
                subject="New Data Added",
                body="New data inserted into the database.",
                to=["tarunrana1997@gmail.com"]
            )