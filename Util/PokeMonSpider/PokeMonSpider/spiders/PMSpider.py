import scrapy
from scrapy.selector import Selector
from PokeMonSpider.items import PokemonDataItem, PokemonSkillItem

class PMSpider(scrapy.Spider):
	name = "pokemon_spider"

	def start_requests(self):
		start_page = r'http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VII-present)'
		self.base_url = 'http://bulbapedia.bulbagarden.net'
		yield scrapy.Request(url=start_page, callback=self.parse)

	def parse(self, response):
		pokemons = Selector(text=response.text).xpath('//table[contains(@class,"sortable")]/tr')
		for pokemon in pokemons[0:5]:
			item = PokemonDataItem()
			tds = pokemon.xpath('./td')
			if len(tds) == 11: # find a pokemon row
				item["Id"] = tds[0].xpath('string(.)').extract()[0].strip()

				item["Name"] = tds[2].xpath('string(.)').extract()[0].strip()
				url = self.base_url + tds[2].xpath('.//@href').extract()[0]
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

		# skills learnt by leveling up
		nodes = Selector(text=response.text).xpath('//h4/span')
		for node in nodes:
			if node.xpath('string(.)').extract()[0] == 'By leveling up':
				table = node.xpath('../following-sibling::table[1]//table[contains(@class,"sortable")]')
				trs = table[0].xpath('./tr')

				# find Move name column
				index = 0
				ths = trs[0].xpath('./th')
				for i in range(0,len(ths)):
					if ths[i].xpath('string(.)').extract()[0].strip() == 'Move':
						index = i

				for tr in trs:
					tds = tr.xpath('./td')
					if len(tds) > 6: # a skill row
						value = tds[index].xpath("string(.)").extract()[0].strip()
						skill_set.add(value)

		# skills learnt by TM/HM
		nodes = Selector(text=response.text).xpath('//h4/span')
		for node in nodes:
			if node.xpath('string(.)').extract()[0] == 'By TM/HM':
				table = node.xpath('../following-sibling::table[1]//table[contains(@class,"sortable")]')
				trs = table[0].xpath('./tr')
				for tr in trs:
					tds = tr.xpath('./td')
					if len(tds) > 7: # a skill row
						value = tds[2].xpath("string(.)").extract()[0].strip() # name is always in the 3rd column
						skill_set.add(value)

		item = PokemonSkillItem()
		item["Id"] = response.meta["Id"]
		item["Name"] = response.meta["Name"]
		item["Skills"] = skill_set
		yield item

