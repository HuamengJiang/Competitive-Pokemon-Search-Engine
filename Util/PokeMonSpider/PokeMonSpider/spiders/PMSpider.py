import scrapy
from scrapy.selector import Selector
from PokeMonSpider.items import PokemonDataItem, PokemonSkillItem

class PMSpider(scrapy.Spider):
	name = "pokemon_spider"

	def start_requests(self):
		site = r'http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VII-present)'
		self.base_url = 'http://bulbapedia.bulbagarden.net'
		yield scrapy.Request(url=site, callback=self.parse)

	def parse(self, response):
		pokemons = Selector(text=response.text).xpath('//table[contains(@class,"sortable")]/tr')
		for pokemon in pokemons:
			item = PokemonDataItem()
			tds = pokemon.xpath('./td')
			if len(tds) == 11:
				item["Id"] = tds[0].xpath('string(.)').extract()[0].strip()

				item["Name"] = tds[2].xpath('string(.)').extract()[0].strip()
				url = self.base_url + tds[2].xpath('.//@href').extract()[0]
				print url
				yield scrapy.Request(url=url, callback=self.parse_skills, meta={"Id":item["Id"], "Name":item["Name"]})

				item["HP"] = tds[3].xpath('string(.)').extract()[0].strip()
				item["Attack"] = tds[4].xpath('string(.)').extract()[0].strip()
				item["Defense"] = tds[5].xpath('string(.)').extract()[0].strip()
				item["Sp_attack"] = tds[6].xpath('string(.)').extract()[0].strip()
				item["Sp_defense"] = tds[7].xpath('string(.)').extract()[0].strip()
				item["Speed"] = tds[8].xpath('string(.)').extract()[0].strip()
				item["Total"] = tds[9].xpath('string(.)').extract()[0].strip()
				yield item

	def parse_skills(self, response):
		skill_set = set()

		nodes = Selector(text=response.text).xpath('//h4/span/a')
		for node in nodes:
			if node.xpath('text()').extract()[0] == 'leveling up':
				table = node.xpath('../../following-sibling::table[1]//table[contains(@class,"sortable")]')
				trs = table[0].xpath('./tr')
				print len(trs)
				index = 1
				ths = trs[0].xpath('./th')
				print len(ths)
				for i in range(0,len(ths)):
					if ths[i].xpath('string(.)').extract()[0].strip() == 'Move':
						index = i
					# 	print "----------find---------------------"
					# 	break
					# else:
					# 	print ths[i].xpath('string(.)').extract()[0]

				print "----------look---------------------"
				for tr in trs:
					tds = tr.xpath('./td')
					if len(tds) > 6:
						value = tds[index].xpath("string(.)").extract()[0].strip()
						skill_set.add(value)

		nodes = Selector(text=response.text).xpath('//h4/span')
		for node in nodes:
			if node.xpath('string(.)').extract()[0] == 'By TM/HM':
				table = node.xpath('../following-sibling::table[1]//table[contains(@class,"sortable")]')
				trs = table[0].xpath('./tr')
				for tr in trs:
					tds = tr.xpath('./td')
					if len(tds) > 7:
						value = tds[2].xpath("string(.)").extract()[0].strip()
						skill_set.add(value)

		item = PokemonSkillItem()
		item["Id"] = response.meta["Id"]
		item["Name"] = response.meta["Name"]
		item["Skills"] = skill_set
		yield item

