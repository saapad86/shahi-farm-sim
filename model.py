import numpy as np
import pandas as pd
import uuid
import names
import random
import math

class World(object):
	def __init__(self,num_players=100,num_codes=1000):
		self.num_codes = num_codes
		self.num_players = num_players
		self.time = 0
		self.initCodes()
		self.initPlayers()

	def initCodes(self):
		self.valid_codes = []
		self.redeemed_codes = []
		for i in range(self.num_codes):
			self.valid_codes.append(uuid.uuid4())

	def initPlayers(self):
		self.players = []
		# establish propensity to purchase by drawing from a Gamma distribution
		g_dist = np.random.gamma(2.,1.,self.num_players)
		for i,g in list(zip(range(self.num_players),g_dist)):
			self.players.append(Player(self,id=str(i+1).zfill(6),propensity=g))

	def redeem(self,code):
		# # check if the code has been redeemed
		# if code not in self.redeemed_codes:
		# 	# check if the code is valid
		# 	if code in self.valid_codes:
		# 		# append to redeemed codes
		# 		self.redeemed_codes.append(code)
		# 		# return an animal
		# 		return self.createAnimal()
		# 	else:
		# 		print('Invalid code!')
		# 		return None
		# else:
		# 	print('This code has already been redeemed!')
		# 	return None
		self.redeemed_codes.append(code)
		return self.createAnimal()

	def discover(self):
		if(len(self.valid_codes) > 0):
			return self.valid_codes.pop()
		else:
			return None

	def createAnimal(self):
		species = random.randint(0,59)
		return Animal(species)

	def simulate(self):
		# reset the state of our world
		self.initCodes()
		for p in self.players:
			p.initFarm()

		while(len(self.redeemed_codes) < len(self.valid_codes)):
			# randomly select a buyer to make a purchase
			buyer = random.randint(0,len(self.players)-1)
			self.players[buyer].buy()

		data = []
		for p in self.players:
			data.append(p.tally())
		self.df = pd.DataFrame(data)	

	def report(self):
		cols = [c for c in self.df.columns if c[:9] == 'num_group']
		for c in cols:
			self.df['winner_'+c[4:]] = np.where(self.df[c] >= 10,1,0)
		sum_cols = [c for c in self.df.columns if c[:6] == 'winner']
		df = self.df[sum_cols].agg(np.sum)
		print(df)

class Animal(object):
	def __init__(self,species):
		self.id = uuid.uuid4()
		self.species = species
		self.group = math.floor(species*1.0/10)
		self.tier = species % 10

class Player(object):
	def __init__(self,world,name=None,id=None,propensity=1.0):
		self.name = name if name != None else names.get_full_name()
		self.id = id if id != None else uuid.uuid4()
		self.propensity = propensity
		self.world = world
		self.initFarm()

	def redeemCode(self,code):
		# attempt to redeem the code for an animal
		result = self.world.redeem(code)
		if result != None:
			# if it is an animal, add it to our farm!
			self.farm.append(result)

	def buy(self):
		# generate a random number between 0 and 1
		# apply the purchase propensity modifier (mean of 2) and do a check to see if buyer will make purchase
		r = random.random()*self.propensity
		# on average, this should produce 50% chance of success (higher for those with higher propensity)
		if r >= 1:
			self.purchases += 1
			self.redeemCode(self.world.discover())

	def initFarm(self):
		self.purchases = 0
		self.farm = []

	def tally(self):
		row = {
			'id': self.id,
			'name': self.name,
			'num_purchases': self.purchases,
			'num_animals': len(self.farm),
			'num_species': len(set(a.species for a in self.farm))
		}
		for g in range(6):
			row['num_group'+str(g)] = len(set([a.tier for a in self.farm if a.group == g]))
		return row
