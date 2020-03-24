# -*- coding: utf-8 -*-
import os
import scrapy
import urllib
from urllib.parse import quote

output_path = 'tmp'
os.makedirs(output_path, exist_ok=True)

class BfIgaSpider(scrapy.Spider):
    name = "bf"
    start_urls = [
        'https://www.interieur.gouv.fr/Publications/Rapports-de-l-IGA/Bonnes-Feuilles',
    ]

    def parse(self, response):
        print('enter parser')
        for quote in response.css('div h2 a::attr(href)'):
            print(10*"*")
            report_page = quote.get()
            print(report_page)
            if report_page != '/Publications':
                yield response.follow(report_page, callback=self.parse_report)

        #import  pdb; pdb.set_trace()
        next_page = response.css('span.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_report(self, response):

        print("Analyse report page %s"%response.url)
        # import  pdb; pdb.set_trace()
        date = response.css('div.attribute-display_date::text').get(default='')
        author = response.css('div.attribute-author::text').get(default='')
        #abstract = response.css('div.attribute-text *::text').getall()
        title = response.css('div.attribute-header').css('h1::text').get(default='')
        file = response.css('a.file_type_n_size::attr(href)').getall()
        # We choose the file with les bonnes feuilles or BF
        file_to_save = [f for f in file if ('BF' in f) or ('bonnes-feuilles' in f)]
        if len(file_to_save) == 1 :
            local_path = os.path.join(output_path,os.path.basename(file_to_save[0]))
            file_to_download = response.urljoin(quote(file_to_save[0]))#.encode('utf-8')
            if not os.path.isfile(local_path):

                urllib.request.urlretrieve(file_to_download, local_path)

            yield {
                'date' : date.replace(u'\xa0', u' ').replace(
                            '\n','').replace('\t','').strip(),
                 'author' : author.replace(u'\xa0', u' ').replace(
                            '\n','').replace('\t','').strip(),
                 'title' : title.replace(u'\xa0', u' ').replace(
                            '\n','').replace('\t','').strip(),
                 'file': os.path.basename(file_to_save[0])
                }
        else :
            print('!!!! No file !!!!')
            pass
