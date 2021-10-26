# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

# Creating the scraper class
class ImdbSpider(scrapy.Spider):
    """
    A page crawler for IMDB to extract movies with shared actors
    """
    name = "imdb_spider"

    # Start URL for Pride and Prejudice (2005)
    start_urls = [
        "https://www.imdb.com/title/tt0414387/"
    ]

    def parse(self, response):
        """
        Navigates from movie page to cast & crew 
        page 
        """
        crew_cast_url = response.url + "fullcredits"
        # Navigating to the crew and cast page of the current film
        yield scrapy.Request(crew_cast_url, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        Assumes that we start on the cast and crew 
        page of a given film
        Navigates to the every listed actor's page 
        """
        # Extracting the links to cast pages
        cast = response.css("table.cast_list a")
        # extracts all the links related to cast
        cast_links = [actor.attrib["href"] for actor in cast]
        cast_imgs_links = [link for link in set(cast_links) if link.startswith("/name")]
        # Navigating to the appropriate actor page
        for cast_link in cast_imgs_links:
            url = response.urljoin(cast_link)
            yield scrapy.Request(url, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        Assumes that we start on the actor page
        Yields a dictionary with two key-value pairs: actor_name and movie_or_TV name 
        """
        actor_name = response.css("span.itemprop").get().split("<")[-2].split(">")[-1]
        all_films = response.css("div.filmo-category-section a").getall()

        for film in all_films: 
            movie_or_TV_name = film.split("<")[-2].split(">")[-1]

            yield {
                "actor_name" : actor_name,
                "movie_or_TV_name" : movie_or_TV_name
            }
