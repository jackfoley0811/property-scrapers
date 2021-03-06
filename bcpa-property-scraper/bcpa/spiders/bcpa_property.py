import scrapy
import urllib
import json
from bcpa.items import BcpaItem
import datetime
import time
import pdb

class Bcpa_Property(scrapy.Spider):
    name = "bcpa_prop"

    def start_requests(self):
      folios = [
            "4941 10 38 0430",
            "4942 35 04 0720",
            "5040 02 19 0250",
            "4942 06 29 0260",
            "4841 23 09 0120",
            "4843 30 AE 0810",
            "4843 30 AF 1430",
            "4841 10 01 3640",
            "504119110540",
            "494117310091",
      ]
      for folio in folios:
            url = 'http://www.bcpa.net/RecInfo.asp?URL_Folio={}'
            yield scrapy.Request(url.format(folio), callback=self.parse_detail, method="GET", meta={'url': url.format(folio)})


    def parse_detail(self, response):

      item = BcpaItem()
      item['url'] = response.meta['url']
      if response.status != 200:
            yield item
      elif response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[1]/td[2]/span/a/b/text()').get() == None:
            yield item
      else:       
            item['website'] = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[1]/td[2]/span/a/b/text()').get()
            # 7260 NW 8 STREET,MARGATE FL 33063-4027

            item['website'] = item['website'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace('  ', ' ').strip()
            item['street'] = item['website'].split(',')[0].strip()
            sep1 = item['website'].split(',')[1].strip().split(' ')
            print(sep1)
            item['zipcode'] = sep1[len(sep1) - 1].strip()
            item['state'] = sep1[len(sep1) - 3].strip()
            item['city'] = item['website'].split(',')[1].replace(item['zipcode'], '').replace(item['state'], '').replace('  ', '').strip()
            # item['website'].split(' ')[len(item['website'].split(' ')) - 1]
            property_owners = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[2]/td[2]/span/text()').getall()		

            item['property_owner'] = ' '.join(property_owners)
            item['property_owner'] = item['property_owner'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace('  ', '').strip()

            item['mail'] = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[3]/td[2]/span/text()').get()
            item['mail'] = item['mail'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace('  ', '').strip()

            item['sid'] = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[3]/table/tr/td[2]/span/text()').get()
            item['sid'] = item['sid'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace('  ', '').strip()

            item['Saled_Date'] = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[9]/tr/td[1]/table/tr[3]/td[1]/span/text()').get()
            item['Saled_Date'] = item['Saled_Date'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace(' ', '').strip()

            item['Saled_Type'] = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[9]/tr/td[1]/table/tr[3]/td[2]/span/text()').get()
            item['Saled_Type'] = item['Saled_Type'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace(' ', '').strip()
            item['Saled_Price'] = response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[9]/tr/td[1]/table/tr[3]/td[3]/span/text()').get()
            item['Saled_Price'] = item['Saled_Price'].replace('\n', '').replace('\r', ' ').replace('\t', '').replace('\xa0', ' ').replace(' ', '').strip()

            # print(response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[1]/td[2]/span/a/b/text()').get());
            # print(response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[2]/td[2]/span/text()').getall());
            # print(response.xpath('//html/body/table[2]/tr/td/table/tr[1]/td[1]/table[1]/tr/td[1]/table/tr[3]/td[2]/span/text()').get());
            yield item
            # print(response.css('table')[4].get())
            # print(response.xpath('//table[1]//table[1]//table[1]').getall()[1].xpath('tr').getall())

