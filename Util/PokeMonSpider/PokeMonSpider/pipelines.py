# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from items import PokemonDataItem, PokemonSkillItem

class PokemonspiderPipeline(object):

	def __init__(self):
		self.pokemon_writer = csv.writer(file('outputs/pokemon.csv', 'w'))
		self.skill_writer = csv.writer(file('outputs/skills.csv', 'w'))

	def process_item(self, item, spider):
		if isinstance(item, PokemonDataItem):
			self.pokemon_writer.writerow([item["Id"],item["Name"],item["HP"],item["Attack"],item["Defense"], \
				item["Sp_attack"],item["Sp_defense"],item["Speed"],item["Total"]])
		elif isinstance(item, PokemonSkillItem):
			row = [item["Id"],item["Name"]]
			skills = list(item["Skills"])
			skills.sort()
			row.extend(skills)
			self.skill_writer.writerow(row)
		return item