import scrapy
from collections import Counter


class MultiboardsSpider(scrapy.Spider):
    name = "multiboards"
    allowed_domains = ["www.ptt.cc"]
    start_urls = [
        "https://www.ptt.cc/bbs/Gossiping/index.html",
        "https://www.ptt.cc/bbs/Stock/index.html",
        "https://www.ptt.cc/bbs/Beauty/index.html",
    ]
    page_counts = {url.split("/")[4]: 0 for url in start_urls}
    page_limit = 5

    def parse(self, response):

        # handle the ptt over18 notice redirect
        if response.css("div.over18-notice").get():
            print("=== over18-notice ===")
            yield scrapy.FormRequest.from_response(
                response,
                formdata={"yes": "yes"},
                callback=self.parse,
            )
            return

        # early return if we have already scraped {max_page} pages
        board = response.url.split("/")[4]
        self.page_counts[board] += 1
        if self.page_counts[board] > self.page_limit:
            return
        print(f"\n=== Crawling page: {self.page_counts[board]} ===\n")

        for href in response.css("div.r-ent > div.title a::attr(href)"):
            yield response.follow(href, self.parse_post)

        # locate the previous page using the fixed index of button group
        prev_page = response.css("div.btn-group-paging a::attr(href)").getall()[1]
        if not prev_page:
            return
        yield response.follow(prev_page, self.parse)

    def parse_post(self, response):
        """
        Extract below information from a post:
        - author
        - category
        - title
        - datetime
        - content
        - num_of_comments
        - push_score
        """
        info_group = response.css("span.article-meta-value::text").getall()
        if not info_group:
            return
        author, category, title, datetime = info_group

        # {"推": int, "噓": int, "→": int}
        push_scores = Counter(
            map(str.strip, response.css("span.push-tag::text").getall())
        )

        yield {
            "author": author,
            "category": category,
            "title": title,
            "datetime": datetime,
            "content": response.css("#main-content::text").get(),
            "num_of_comments": len(response.css("div.push").getall()),
            "push_score": push_scores["推"],
        }
