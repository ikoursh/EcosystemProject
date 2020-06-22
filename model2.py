import numpy as np
import random
import matplotlib.pyplot as plt
import math
import time
import os
import copy

import matplotlib.image as mgimg
from matplotlib import animation

import gc
from nn import neuralNetwork
import configparser


config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('config.ini')


INT_CONST = float(config["VARIABLES"]["INT_CONST"])
ENLB_CONST = float(config["VARIABLES"]["ENLB_CONST"])
ENGB_CONST = float(config["VARIABLES"]["ENGB_CONST"])
ENL_CONST = float(config["VARIABLES"]["ENL_CONST"])
ENG_CONST = float(config["VARIABLES"]["ENG_CONST"])
MAX_LIFE_SPAN = float(config["VARIABLES"]["MAX_LIFE_SPAN"])

AGE_CONST = config["VARIABLES"]["AGE_CONST"]
if (AGE_CONST == "auto"):
	AGE_CONST = ENG_CONST - (100 / MAX_LIFE_SPAN)
else:
	AGE_CONST = float(AGE_CONST)
	
POP_DENCITY = float(config["VARIABLES"]["POP_DENCITY"])
AGING_TIME = float(config["VARIABLES"]["AGING_TIME"])
G_SPEED_FACTOR = float(config["VARIABLES"]["G_SPEED_FACTOR"])
FOOD_CONST = float(config["VARIABLES"]["FOOD_CONST"])
START_MASS_P = float(config["VARIABLES"]["START_MASS_P"])
G_FOOD_COL_CONST = float(config["VARIABLES"]["G_FOOD_COL_CONST"])
G_FIGHT_COL_CONST = float(config["VARIABLES"]["G_FIGHT_COL_CONST"])
MIN_IQ = float(config["VARIABLES"]["MIN_IQ"])
MAX_IQ = float(config["VARIABLES"]["MAX_IQ"])
MIN_EQ = float(config["VARIABLES"]["MIN_EQ"])
MAX_EQ = float(config["VARIABLES"]["MAX_EQ"])
FOOD_FLUCT = float(config["VARIABLES"]["FOOD_FLUCT"])

def isclose(a, b, rel_tol=1e-09, abs_tol=1e-04):
	return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
	
def map_from_to(x, a, b, c, d):
	return (x - a) / (b - a) * (d - c) + c


	
GRAPHS_FOLDER= "/graphs-0.3"
ANIMATION_FOLDER ='/animations-0.1'
if not os.path.isdir('.'+GRAPHS_FOLDER):
	os.mkdir('.'+GRAPHS_FOLDER)
if not os.path.isdir('.'+ANIMATION_FOLDER):
	os.mkdir('.'+ANIMATION_FOLDER)
	
	
	
'''
An agent class

varibles:

	@dynamic x,y

	@fixed iq[int] - number of hidden nerons (1-inf)
	@fixed mass[int] (1-inf)

	@derived brain[neuralNetwork[5, iq, 2]] - the brain of the agent - distance to nearest food, angle to it + same for nearest agent, if agent is stronger than you
	@derived strength - how strong the agent is
	@derived speed - how fast the agent is[~0-1]
	@derived enegy[int] - how much energy the agent has
	@derived health[float] - the amount of health the agent has
'''


class agent:
	def __init__(self,
				 iq,
				 eq,
				 mass,
				 x,
				 id,
				 final_mass,
				 breed_mass_div,
				 breed_chance,
				 size_factor,
				 move_brain=None,
				social_brain=None,
				 parent_id=None):
		self.iq = iq
		self.eq = eq
		if move_brain is not None :
			self.move_brain = move_brain
		else:
			self.move_brain = neuralNetwork([3, iq, iq, 1])

		if social_brain is not None :
			 self.social_brain = social_brain
		else:
			self.social_brain = neuralNetwork([4, eq, eq, 2])

		self.parent_id = parent_id

		self.mass = mass
		self.strength = mass
		self.energy = mass
		self.speed = (1 / mass) * size_factor * G_SPEED_FACTOR
		self.health = mass
		self.final_mass = final_mass

		self.breed_mass_div = breed_mass_div
		self.breed_chance = breed_chance

		self.x = x

		self.id = id
		self.v = 0

		self.size_factor = size_factor

	def age(self):
		if self.mass > self.final_mass * AGING_TIME:
			self.health -= AGE_CONST

	def think(self, d_food, d_agent, s_agent):
		out = self.move_brain.feed_forward(
			[d_food, d_agent,
			 int(s_agent.strength > self.strength)])
		self.v = map_from_to(float(out[0]), 0, 1, -self.speed, self.speed)
		self.energy -= (self.iq+self.eq)/2 * INT_CONST

	def move(self):
		self.x += self.v
		if self.x > 1:  #make the world round
			self.x = 1 - self.x
		if self.x < -1:
			self.x = -self.x- 1

	def breed(self, nid):
		nb = copy.deepcopy(self.move_brain)
		nb.mutate()

		nsb = copy.deepcopy(self.social_brain)
		nsb.mutate()

		nm = 0
		while nm == 0:
			nm = (self.mass + random.randrange(0, 10)) * self.breed_mass_div
		self.health -= nm
		self.mass -= nm
		if self.health < 0:
			return None  #died in childbirth
		return agent(self.iq,self.eq, nm, self.x + random.uniform(0.001, -0.001), nid,
					 nm / self.breed_mass_div,
					 self.breed_mass_div + random.uniform(0.01, -0.01),
					 self.breed_chance + random.uniform(0.01, -0.01),
					 self.size_factor, nb, nsb, self.id)

	def eat(self, food):
		self.energy += food
		self.mass += food
		if self.mass > self.final_mass:
			self.mass = self.final_mass
		self.strength += food

	def __str__(self):
		return str(self.id)


def fight(a1, a2):
	a1.health -= (a2.strength)
	a2.health -= (a1.strength)

	a1.energy += a2.mass
	a2.energy += a1.mass

def interact(a1, a2, s):
	close_family = a1.parent_id == a2.id or a2.parent_id == a1.id
	s1 = a1.social_brain.feed_forward([1 if close_family else 0, a1.energy/a1.mass, a2.energy/a2.mass, 1 if a1.mass>a2.mass else 0])
	s2 = a2.social_brain.feed_forward([1 if close_family else 0, a2.energy/a2.mass, a1.energy/a1.mass, 1 if a1.mass<a2.mass else 0])

	if s1[0]>0.5 or s2[0]>0.5:
		fight(a1, a2)
		s.fight+=1
	if s1[1]>0.5:
		a1.energy-=FOOD_CONST
		a2.energy+=FOOD_CONST
		s.help+=1
	if s2[1]>0.5:
		a1.energy+=FOOD_CONST
		a2.energy-=FOOD_CONST
		s.help+=1
	else:
		s.nothing+=1
		
		
class food:
	def __init__(self, x):
		self.x = x
		
		
def mk_round(d):
	if d>1:
		return d - 2
	if d<-1:
		return -d-1
	else:
		return d

class sim:
	def __init__(
		self,
		agents=500,
		food_count="auto",
	):
		if food_count == "auto":
			food_count = 5 * agents

		if type(food_count) != type(0) or type(agents) != type(0):
			raise TypeError

		self.size_factor = 1 / (agents / POP_DENCITY)
		self.food_col_const = G_FOOD_COL_CONST * self.size_factor
		self.fight_col_const = G_FIGHT_COL_CONST * self.size_factor

		self.food_count = food_count
		self.breed = 0
		self.kill = 0
		self.fight = 0
		self.help = 0
		self.nothing = 0
		self.id = 0
		self.eat = 0
		self.agents = []
		self.food = []
		self.gcsteps = 0
		for i in range(agents):  #create agents
			mass = int(random.randrange(1, 100))
			self.agents.append(
				agent(int(random.randrange(MIN_IQ,
										   MAX_IQ)), int(random.randrange(MIN_EQ, MAX_EQ)), mass * START_MASS_P,
					  random.uniform(-1, 1), self.id, mass, random.random(),
					  random.random(), self.size_factor))
			self.id += 1
#sorting agents now because animation needs sort to happen last in step
		self.agents.sort(
			key=lambda a: a.x
		)  #sort agents by position, allows to quickly determine closest agent with low complexity

		self.i_OT = []

		self.nummber_of_agents_OT = []
		self.mass_OT = []
		self.eat_OT = []

		self.iq_OT = []
		self.eq_OT = []

		self.breed_mass_div_OT = []
		self.breed_chance_OT = []
		
		self.fight_OT = []
		self.help_OT = []
		self.nothing_OT = []

		self.cfood()

		return

	def get_fn(self):
		return '{}-{}-{}'.format(
			len(self.agents), self.gcsteps,
			time.strftime("%d:%M:%Y:%H:%M:%S", time.localtime()))

	def run(self, steps=1000, print_freq=10):
		for i in range(steps):
			self.step()  #update all the agents
			self.update_stats(steps, i, print_freq)

	def update_stats(self, steps, csteps, print_freq):
		self.gcsteps += 1
		if csteps%print_freq==0:
			print(
				"{}% ({} of {}) current population size: {} ammont of food: {}".
				format(round((csteps / steps) * 100, 2), csteps, steps,
					   len(self.agents), len(self.food)))  # print status
		# append statistics:
		self.i_OT.append(self.gcsteps)
		self.nummber_of_agents_OT.append(len(self.agents))
		self.mass_OT.append(np.mean([a.mass for a in self.agents]))
		self.eat_OT.append(self.eat)
		self.eat = 0
		self.iq_OT.append(np.mean([a.iq for a in self.agents]))
		self.eq_OT.append(np.mean([a.eq for a in self.agents]))
		self.breed_mass_div_OT.append(
			np.mean([a.breed_mass_div for a in self.agents]))
		self.breed_chance_OT.append(
			np.mean([a.breed_chance for a in self.agents]))
		
		self.fight_OT.append(np.mean(self.fight))
		self.help_OT.append(np.mean(self.help))
		self.nothing_OT.append(np.mean(self.nothing))


	def cfood(self):
		self.food = []
		for i in range(self.food_count):
			self.food.append(food(random.uniform(-1, 1)))
		

	def step(self):

		if len(self.food) < FOOD_FLUCT * self.food_count:
			self.cfood()

		if len(self.agents) <= 1 or len(self.food) == 0:
			return False
		self.agents.sort(
					key=lambda a: a.x
				)  #sort agents by position, allows to quickly determin closest agent with low complexity
		self.food.sort(key=lambda a: a.x)
		food_index = 0
		for a in range(len(self.agents)):
			if (a >= len(self.agents)
				):  #agents can be removed but the range isn't updated
				return True

			ax = self.agents[a].x
			
			tf=None
			lf = None
			for i in range(food_index, len(self.food)):
				if self.food[i].x > ax:
					food_index = i - 1
					tf = self.food[i]
					break
				else:
					lf = self.food[i]
			
			if tf == None:
				tf = self.food[0]
			if lf==None:
				lf = self.food[-1]
				
			
			dtf = mk_round(tf.x-ax)
			dlf = mk_round(lf.x-ax)
			
			dfood = dtf if dtf<dlf else dlf
		

			if abs(
					dfood
			) < self.food_col_const:  #if the abs distance is smaller than the required collision const
				self.food.pop(food_index - 1 if dtf<dlf else food_index-2)  #remove food
				self.agents[a].eat(FOOD_CONST)  #eat food
				self.eat += 1  #update food statistic
				food_index-=1

			#because agents have been sorted by x values, it is easy to find the closest agent by comparing the agent before and the one after
			if a == 0:
				d1 = abs(ax - self.agents[-1].x)
			else:
				d1 = abs(ax - self.agents[a - 1].x)

			try:
				d2 = abs(ax - self.agents[a + 1].x)
			except:
				d2 = abs(ax - self.agents[0].x)

			if d2 < d1:
				try:
					min_d = ax - self.agents[a + 1].x
				except:
					break
				a_s = a + 1
			else:
				min_d = ax - self.agents[a - 1].x
				a_s = a - 1

			if (abs(ax - self.agents[a_s].x) <
					self.fight_col_const
					):
				interact(self.agents[a], self.agents[a_s], self)

			self.agents[a].think(
				dfood, min_d, self.agents[a_s]
			)  #pass the environment variables to the brain of the agent
			self.agents[a].move()  #updating agent position

			self.agents[a].age()  #applying age effect

			if self.agents[a].energy < ENLB_CONST * self.agents[a].mass:
				self.agents[a].health -= ENL_CONST

			if self.agents[a].energy > ENGB_CONST * self.agents[a].mass:
				self.agents[a].health += ENG_CONST

			if (random.random() < self.agents[a].breed_chance
					and self.agents[a].health > 0
					and self.agents[a].mass == self.agents[a].final_mass):
				nk = self.agents[a].breed(self.id)
				if nk != None :
					self.breed += 1
					self.id += 1
					self.agents.append(nk)

			if ((isclose(self.agents[a].health, 0)
				 or self.agents[a].health < 0)):
				self.kill += 1
				self.agents.remove(self.agents[a])
		return True




	def stats(self):
		return "breed:{} kill:{} eat:{}\n".format(
			self.breed, self.kill, sum(self.eat_OT)
		) + "avg mass: {}\n".format(np.mean([
			a.mass for a in self.agents
		])) + "avg speed: {}\n".format(np.mean([
			a.speed for a in self.agents
		])) + "avg pos: {}\n".format(np.mean(
			[a.x for a in self.agents])) + "avg breed chance: {}\n".format(
				np.mean([a.breed_chance for a in self.agents
						 ])) + "avg breed mass divider: {}\n".format(
							 np.mean([a.breed_mass_div for a in self.agents]))

	def graph(self, save=True, info=None):

		if info is None :
			info = input("Enter aditional information about the sim: ")

		titles = [
		   "Number Of Agents", "Average Agent Mass",
			"Amount of Food Consumed", "Average Agent IQ","Average Agent EQ",
			"Average breeding mass divider", "Average Agent Breed Mass"
		]

		values = [
			self.nummber_of_agents_OT, self.mass_OT, self.eat_OT, self.iq_OT,self.iq_OT,
			self.breed_mass_div_OT, self.breed_chance_OT
		]
		if len(titles) != len(values):
			raise Exception("Error len of titles must match len of vars")

		fig, axs = plt.subplots(len(values), sharex='all', figsize=(10, 20))
		metadata = dict()
		for i in range(len(values)):
			axs[i].plot(self.i_OT, values[i], linewidth=0.25)
			axs[i].axes.set_ylim([0, max(values[i])])
			axs[i].set_ylabel(titles[i])

			metadata["Final" + titles[i]] = values[i][-1]

		axs[0].axes.set_xlim([0, self.gcsteps])
		axs[0].set_title(
			"Simulation with {} initial agents and {} steps\nDate: {}\nNotes: {}\n\nStats:\n{}\n"
			.format(len(self.agents), self.gcsteps, time.strftime("%D"), info,
					self.stats()), )

		axs[-1].set_xlabel("Number Of Steps")

		plt.tight_layout()
		extention = ".png"
		plt.autoscale()

		if (save):
			fn = "graphs-0.3/" + self.get_fn() + extention
			fig.savefig(fn, bbox_inches='tight')  # save graph
			#add metada:
			im = Image.open(fn)
			meta = PngImagePlugin.PngInfo()
			for x in metadata:
				meta.add_text(x, str(metadata[x]))
			im.save(fn, extention, pnginfo=meta)
			self.fileName = fn

		plt.show()  #display graph

	def animate(self, steps, res_mult = 2, fps=10, bitrate=20000, print_freq = 10):
		ims = []
		fig = plt.figure(figsize=(res_mult, res_mult))
		for i in range(steps):
			if not self.step():
				return False
			self.update_stats(steps, i, print_freq)
			acu = self.size_factor / 25
			row = [0 for i in np.arange(0, 1, acu)]
			for f in self.food:
				try:
					row[round(f.x / acu)] = 100
				except:
					if round(f.x / acu) > 1 / acu:
						row[-1] = 100
					else:
						row[0] = 100
			for a in self.agents:
				try:
					row[round(a.x / acu)] = 255
				except:
					if round(a.x / acu) > 1 / acu:
						row[-1] = 255
					else:
						row[0] = 255

			r = len(row)/(2 * math.pi)

			p = np.zeros((math.ceil(2*r)+10, math.ceil(2*r)+10))

			dist_proj = 2*math.pi/len(row)
			angle = 0
			for v in row:
				x=round(r*math.cos(angle)+r)
				y=round(r*math.sin(angle)+r)
				p[y][x] = v
				p[y+1][x] = v
				p[y-1][x] = v
				p[y][x+1] = v
				p[y][x-1] = v
				angle+=dist_proj

			ims.append([
				plt.imshow(p,
						   interpolation='nearest',
						   aspect='auto')
			])
			p=None
			row=None
			gc.collect()

		ani = animation.ArtistAnimation(fig,
										ims,
										interval=100,
										blit=False,
										repeat_delay=1000)

		# Set up formatting for the movie files
		Writer = animation.writers['ffmpeg']
		writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=bitrate)

		ani.save("animations-0.1/" + self.get_fn() + '.mp4', writer=writer)
		#optimize:
		#de-enitialize varibles:
		fig = None
		ims = None
		ani = None
		#call garbage colector:
		gc.collect()
		#return animation file name
		return "animations-0.1/" + self.get_fn() + '.mp4'

		
		
from timeit import default_timer as timer
def model_time():
	y = []
	for i in range (10):
		time_elapsed = []
		for i in range (10, 10000, 100):
			m = sim(i)
			start = timer()
			m.step()
			time_elapsed.append(timer()-start)
			gc.collect()
		print(time_elapsed)
		y.append(time_elapsed)
		
	plt.errorbar([i for i in range(10, 10000, 100)], np.mean(y), np.std(y))

		
