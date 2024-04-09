# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GossipingItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
    num_of_comments = scrapy.Field()
    push_score = scrapy.Field()


class MultiboardsItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
    num_of_comments = scrapy.Field()
    push_score = scrapy.Field()
