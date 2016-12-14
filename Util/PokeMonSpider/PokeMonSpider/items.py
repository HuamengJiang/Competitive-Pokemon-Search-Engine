# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item

class PokemonDataItem(Item):
    # define the fields for your item here like:
    Id = Field() 
    Name = Field()
    HP = Field()
    Attack = Field()
    Defense = Field()
    Sp_attack = Field()
    Sp_defense = Field()
    Speed = Field()
    Total = Field()

class PokemonSkillItem(Item):
    # define the fields for your item here like:
    Id = Field() 
    Name = Field()
    Skills = Field()
