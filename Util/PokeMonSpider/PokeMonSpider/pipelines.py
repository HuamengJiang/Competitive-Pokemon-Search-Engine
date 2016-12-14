# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from items import PokemonDataItem, PokemonSkillItem

class PokemonspiderPipeline(object):

	def __init__(self):
		self.writer = csv.writer(file('pokemon.csv', 'w'))
		# self.fieldnames = ["Id","Name","Attack","Defense","Sp_attack","Sp_defense","Speed","Total"]
		# self.writer = csv.DictWriter(file('pokemon.csv'), fieldnames=self.fieldnames)
		self.skill_writer = csv.writer(file('skills.csv', 'w'))

	def process_item(self, item, spider):
		if isinstance(item, PokemonDataItem):
			self.writer.writerow([item["Id"],item["Name"],item["HP"],item["Attack"],item["Defense"], \
				item["Sp_attack"],item["Sp_defense"],item["Speed"],item["Total"]])
		# self.writer.writerow([item["Id"], item["Name"],item["Attack"],item["Defense"]])
		elif isinstance(item, PokemonSkillItem):
			l = [item["Id"],item["Name"]]
			skills = list(item["Skills"])
			skills.sort()
			l.extend(skills)
			self.skill_writer.writerow(l)
			# self.skill_writer.writerow(list(item["Skills"]))
		return item