"""
Program Name: A Random RPG
Purpose: To be a game I work on when waiting for random bull crap.
Author: Isaiah Wegwitz
Last Modified: 12/03/2025
"""
import random

class Items:

    def getName(self):
        return self.name
    
    def getCategory(self):
        return self.category

    def setStats(self, stats):
        #Change this to make it all a dictionary with optional stat values based on a JSON format.
        #i.e. if category == 'weapon':
        #stats.get('damage', 0)
        #Meanwhile, the input would look like:
        #{ "name": "Sword", "category": "weapon", "stats": {"traits":["sharp", "metal"],"damage": 10, etc...}}
        #This makes it easy to read from and write to a JSON format file for the items, and I can do the same for NPCs, Monsters, and Rooms.
        category = self.category
        for i in stats.get('traits',[]):
            self.specialTraits.append(i)
        self.weight = stats.get('weight',0)
        self.price = stats.get('price',0)
        if category == 'weapon':
            self.damage = stats.get('damage',1)
            self.range = stats.get('range','melee')
        if category == 'equipable':
            print("stuff for equipable")
        if category == 'consumable':
            print("Stuff for consumable")
    
    def getStatsWeapon(self):
        return [self.damage,self.range,self.weight,self.price]
    
    def getStatsEquip(self):
        return "Equpable Stats"
    
    def getStatsConsume(self):
        return "Consumable Stats"
    
    def getStats(self):
        if self.category == 'weapon':
            return self.getStatsWeapon()
        elif self.category == 'equipable':
            return self.getStatsEquipt()
        elif self.category == 'consumable':
            return self.getStatsConsume()

    def __init__(self, itemInfo):
        self.name = itemInfo.get('name')
        self.category = itemInfo.get('category')
        self.setStats(itemInfo)
        
class Npc:
    "More temporary code"

sword = Items({'name':'Sword','category':'weapon','damage':10,'weight':2,'price':8,'traits':['metal','highSkill','oneHand'],'range':'melee'})
print(sword.getStats())