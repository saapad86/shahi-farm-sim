import numpy
import pandas
import uuid
import names
import random

class Factory(object):
	def __init__(self,num_codes=1000):
		self.valid_codes = []
		self.redeemed_codes = []

		for i in range(num_codes):
			self.valid_codes.append(uuid.uuid4())

	def redeem(self,code):
		# check if the code has been redeemed
		if code not in self.redeemed_codes:
			# check if the code is valid
			if code in self.valid_codes:
				# append to redeemed codes
				self.redeemed_codes.append(code)
				# return an animal
				return self.createAnimal()
			else:
				print('Invalid code!')
				return None
		else:
			print('This code has already been redeemed!')
			return None

	def discover(self):
		codes = [x for x in self.valid_codes if x not in self.redeemed_codes]
		if len(codes) > 0:
			return codes[0]
		else:
			return None

	def createAnimal(self):
		species = random.randint(0,59)
		return Animal(species)

class Animal(object):
	def __init__(self,species):
		self.id = uuid.uuid4()
		self.species = species
		self.group = round(species*1.0/10)
		self.tier = species % 10

class Player(object):
	def __init__(self,factory,name=None):
		self.name = name if name != None else names.get_full_name()
		self.id = uuid.uuid4()
		self.farm = []
		self.factory = factory
		self.purchases = 0

	def redeemCode(self,code):
		# attempt to redeem the code for an animal
		result = self.factory.redeem(code)
		if result != None:
			# if it is an animal, add it to our farm!
			self.farm.append(result)

	def buy(self):
		self.purchases += 1
		self.redeemCode(self.factory.discover())

	def tally(self):
		row = {
			'id': self.id,
			'name': self.name,
			'num_purchases': self.purchases,
			'num_animals': len(self.farm)
		}
		for g in range(10):
			row['num_group'+str(g)] = len(set([a.tier for a in self.farm if a.group == g]))
		return row
