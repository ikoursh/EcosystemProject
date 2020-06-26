import configparser
import copy
import gc
import math
import os
import random
import time
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from nn import NeuralNetwork

from PIL import Image  # work with metadata via pillow
from PIL import PngImagePlugin

import openpyxl  # work with excell

config = configparser.ConfigParser(inline_comment_prefixes="#")
# config.read('config.ini')
config.read('C:\\Users\\Student\\Documents\\EcoSystemProject\\proj\\config.ini');

INT_CONST = float(config["VARIABLES"]["INT_CONST"])
MOV_CONST = float(config["VARIABLES"]["MOV_CONST"])
ENLB_CONST = float(config["VARIABLES"]["ENLB_CONST"])
ENGB_CONST = float(config["VARIABLES"]["ENGB_CONST"])
ENL_CONST = float(config["VARIABLES"]["ENL_CONST"])
ENG_CONST = float(config["VARIABLES"]["ENG_CONST"])
MAX_LIFE_SPAN = float(config["VARIABLES"]["MAX_LIFE_SPAN"])

AGE_CONST = config["VARIABLES"]["AGE_CONST"]
if AGE_CONST == "auto":
    AGE_CONST = ENG_CONST - (100 / MAX_LIFE_SPAN)
else:
    AGE_CONST = float(AGE_CONST)

POP_DENCITY = float(config["VARIABLES"]["POP_DENCITY"])
AGING_TIME = float(config["VARIABLES"]["AGING_TIME"])
G_SPEED_FACTOR = float(config["VARIABLES"]["G_SPEED_FACTOR"])
FOOD_CONST = float(config["VARIABLES"]["FOOD_CONST"])
START_MASS_P = float(config["VARIABLES"]["START_MASS_P"])
G_COL_CONST = float(config["VARIABLES"]["G_COL_CONST"])
MIN_IQ = float(config["VARIABLES"]["MIN_IQ"])
MAX_IQ = float(config["VARIABLES"]["MAX_IQ"])
MIN_EQ = float(config["VARIABLES"]["MIN_EQ"])
MAX_EQ = float(config["VARIABLES"]["MAX_EQ"])
FOOD_FLUCT = float(config["VARIABLES"]["FOOD_FLUCT"])


def map_from_to(x, a, b, c, d):
    """
    Map a value to a new range

    Used in :meth:`model2.Agent.think` to map inputs and outputs to and from ranges that the neural network requires

    Args:
        x(float): Value
        a(float): Initial range start
        b(float): Initial range end
        c(float): Final range start
        d(float): Final range end


    Returns:
        float: Mapped value
    """
    return (x - a) / (b - a) * (d - c) + c


GRAPHS_FOLDER = "/graphs-0.3"
ANIMATION_FOLDER = '/animations-0.1'
if not os.path.isdir('.' + GRAPHS_FOLDER):
    os.mkdir('.' + GRAPHS_FOLDER)
if not os.path.isdir('.' + ANIMATION_FOLDER):
    os.mkdir('.' + ANIMATION_FOLDER)


class Agent:
    """
    An class that models the behavior of wild creatures.


    Args:
        x (float): The agents initial position. See :attr:`model2.Agent.x`
        id(int): An id used by the simulation class to keep track of agents. See :attr:`model2.Agent.id`

        iq (int): The amount of neurons in every hidden layer of the agent's neural network that is responsible for movement. See :attr:`model2.Agent.iq`

        eq (int): The amount of neurons in every hidden layer of the agent's neural network that is responsible for agent to agent interactions. See :attr:`model2.Agent.eq`

        mass(int): The mass of the agent represents it's size. See :attr:`model2.Agent.mass`
        final_mass(int): The final mass of the agent. See :attr:`model2.Agent.final_mass`

        breed_mass_div(float): The initial mass to final mass ratio of the agents children. See :attr:`model2.Agent.breed_mass_div`
        breed_chance(float): The chance for the agent to breed at every step. See :attr:`model2.Agent.breed_chance`

        size_factor(float): A variable used by the sim's movement and collision engines to control the size of the simulation. See :attr:`model2.Sim.size_factor`

        move_brain(NeuralNetwork): The neural network the agent will use to decide where to move. This is either provided by the creature's parent (via a mutated brain) or is generated from scratch (for the initial population) See :attr:`model2.Agent.move_brain`.
        social_brain(NeuralNetwork): The neural network the agent will use to interact with other agents. This is either provided by the creature's parent (via a mutated brain) or is generated from scratch (for the initial population) See :attr:`model2.Agent.social_brain`.

        parent_id(int): This variable is used to detect close family by the simulation. It is then used as a variable in agent interactions. See :attr:`model2.Agent.parent_id`

    Attributes:
        energy(float): Tracks the amount energy an agent has. energy is acquired by eating, and lost by moving or thinking. Energy allows agents to grow and regenerate health. If an agent has low energy, he will take damage. See :meth:`model2.Agent.think`, :meth:`model2.Agent.move`, :meth:`model2.interact`

        speed(float): The maximum velocity at which the creature can move. Inversely related to mass (1/mass)
        health(float): How much damage can a creature sustain. When it reaches 0, the creature dies.

        x (float): The agents position. See :meth:`model2.Agent.move`.

        id(int): An id used by the simulation class to keep track of agents. See :attr:`model2.Agent.parent_id` for use case.

        iq (int): The amount of neurons in every hidden layer of the agent's neural network that is responsible for movement. See :attr:`model2.Agent.move_brain` for use case.

        eq (int): The amount of neurons in every hidden layer of the agent's neural network that is responsible for agent to agent interactions. See :attr:`model2.Agent.social_brain` for use case

        mass(int): The mass of the agent, represents it's size.
        final_mass(int): The final mass of the agent.

        breed_mass_div(float): The initial mass to final mass ratio of the agents children. See :meth:`model2.Agent.breed`.
        breed_chance(float): The chance for the agent to breed at every step. See :meth:`model2.Agent.breed`

        size_factor(float): A variable used by the sim's movement and collision engines to control the size of the simulation. See :attr:`model2.Sim.size_factor`

        move_brain(NeuralNetwork): The neural network the agent will use to decide where to move. Structure: [3, iq, iq, 1] See :meth:`model2.Agent.think` and :attr:`model2.Agent.iq`.
        social_brain(NeuralNetwork): The neural network the agent will use to interact with other agents.  Structure [4, eq, eq, 2] See :meth:`model2.interact` and :attr:`model2.Agent.eq`.

        parent_id(int): This variable is used to detect close family by the simulation. It is then used as a variable in agent interactions See :attr:`model2.Agent.id`.


    """

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
        if move_brain is not None:
            self.move_brain = move_brain
        else:
            self.move_brain = NeuralNetwork([3, iq, iq, 1])

        if social_brain is not None:
            self.social_brain = social_brain
        else:
            self.social_brain = NeuralNetwork([4, eq, eq, 2])

        self.parent_id = parent_id

        self.mass = mass
        self.energy = mass
        self.speed = (1 / mass) * size_factor * G_SPEED_FACTOR
        self.health = mass
        self.final_mass = final_mass

        self.breed_mass_div = breed_mass_div
        self.breed_chance = breed_chance

        self.x = x

        self.id = id

        self.size_factor = size_factor

    def age(self):
        """
        Make the agent experience aging

        See Also:
             :attr:`model2.Agent.health`
        """
        if self.mass > self.final_mass * AGING_TIME:
            self.health -= AGE_CONST

    def think(self, d_food: float, d_agent: float, s_agent: 'Agent') -> float:
        """
        Trigger the agent's :attr:`model2.Agent.move_brain` and make it decide where to go.
        Energy is subtracted for thinking using :attr:`model2.Agent.iq`.

        See Also:
            :attr:`model2.Agent.move`

        Args:
            d_food(float): The distance to the nearest food item
            d_agent(float): The distance to the nearest agent
            s_agent(Agent): The strength of the nearest agent

        Returns:
            float: DX, fed into :meth:`model2.Agent.move`

        """
        out = self.move_brain.feed_forward(
            [map_from_to(d_food, -1, 1, 0, 1), map_from_to(d_agent, -1, 1, 0, 1),
             int(s_agent.mass > self.mass)])
        self.energy -= self.iq * INT_CONST
        return map_from_to(float(out[0]), 0, 1, -self.speed, self.speed)

    def move(self, dx: float) -> None:
        """
        Apply the velocity calculated in the think function to the agent's position
        Energy is subtracted for moving. See :attr:`model2.Agent.energy`

        Args:
            dx: Distance to travel

        See Also:
            :attr:`model2.Agent.think`

        """
        self.x += dx
        if self.x > 1:  # make the world round
            self.x = 1 - self.x
        if self.x < -1:
            self.x = -self.x - 1
        self.energy -= MOV_CONST * dx

    def breed(self, nid: int):
        """
        Make the agent have a child.
        Note that the child's mass is removed from the agent's mass on childbirth


        See Also:
            :attr:`model2.Agent.breed_chance`
            :attr:`model2.Agent.breed_mass_div`

        Args:
            nid(int): The id of the new child

        Returns:
            Agent: A child that is a mutated version of the agent
        """
        nb = copy.deepcopy(self.move_brain)
        nb.mutate()

        nsb = copy.deepcopy(self.social_brain)
        nsb.mutate()

        nm = math.ceil((self.mass + random.randrange(-10, 10)) * self.breed_mass_div)
        self.health -= nm
        self.mass -= nm
        if self.health <= 0 or self.mass < 1 or nm < 1:
            self.health = -1
            return None  # died in childbirth
        return Agent(self.iq, self.eq, nm, self.x + random.uniform(0.001, -0.001), nid,
                     math.ceil(nm / self.breed_mass_div),
                     self.breed_mass_div + random.uniform(0.01, -0.01), self.breed_chance + random.uniform(0.01, -0.01),
                     self.size_factor, nb, nsb, self.id)

    def eat(self, food: int) -> None:
        """
        Make the agent eat, increases agent energy (:attr:`model2.Agent.energy`) and mass (:attr:`model2.Agent.mass`) if the agent has not reached it's final mass and has energy to spare

        Args:
            food(int): The amount of food the agent should eat
        """
        if self.mass < self.final_mass and self.energy / self.mass > ENGB_CONST:
            self.mass += food
        else:
            self.energy += food

    def __str__(self):
        return str(self.id)


def fight(a1: Agent, a2: Agent) -> None:
    """
    Makes the given agents fight
    Health is lost according to the other agent's mass, but the same amount of energy is gained (note: this expects one agent to die so the other can eat him)

    See Also:
        :attr:`model2.Agent.energy`
        :attr:`model2.Agent.mass`
        :attr:`model2.Agent.health`

    Args:
        a1(Agent): Agent 1
        a2(Agent): Agent 2
    """
    a1.health -= a2.mass
    a2.health -= a1.mass

    a1.energy += a2.mass
    a2.energy += a1.mass


def interact(a1: Agent, a2: Agent, s) -> None:
    """
    Makes the given agents interact
    Energy is subtracted according to :attr:`model2.Agent.eq`. See :attr:`model2.Agent.energy`

    Args:
        a1(Agent): Agent 1
        a2(Agent): Agent 2
        s(Sim): The simulation that is requesting the interaction (used to update statistics)
    """
    a1.energy -= a1.eq * INT_CONST
    a2.energy -= a2.eq * INT_CONST
    close_family = a1.parent_id == a2.id or a2.parent_id == a1.id
    s1 = a1.social_brain.feed_forward(
        [1 if close_family else 0, a1.energy / a1.mass, a2.energy / a2.mass, 1 if a1.mass > a2.mass else 0])
    s2 = a2.social_brain.feed_forward(
        [1 if close_family else 0, a2.energy / a2.mass, a1.energy / a1.mass, 1 if a1.mass < a2.mass else 0])

    if s1[0] > 0.5 or s2[0] > 0.5:
        fight(a1, a2)
        s.fight += 1
    if s1[1] > 0.5:
        a1.energy -= FOOD_CONST
        a2.energy += FOOD_CONST
        s.help += 1
    if s2[1] > 0.5:
        a1.energy += FOOD_CONST
        a2.energy -= FOOD_CONST
        s.help += 1
    else:
        s.nothing += 1


class Food:
    """ Food class

    Args:
        x(float): Food position

    Attributes:
        x(float): Food position
    """

    def __init__(self, x: float) -> None:
        self.x = x


def mk_round(d: float) -> float:
    """
    Gets the smallest distance between 2 objects on a circle with flattened coordinates from -1 to 1

    Args:
        d(float): The distance to process


    Returns:
        float: The processed distance
    """
    if d > 1:
        return d - 2
    if d < -1:
        return -d - 1
    else:
        return d


class Sim:
    """A class used to model a simulated population


    Args:
        agents: The number of agents the simulation should start with. See :class:`model2.Agent`
        food_count: The amount of food that should be provided. See :class:`model2.Food`

    Attributes:

        agents(list[Agent]): A list of all the agents that are alive in the simulation.
        size_factor(float): A constant that scales the simulation. calculated via  1 / (agents / POP_DENCITY)
        col_const(float): The minimum distance at which 2 objects are considered to be colliding.
        food_count(int): The amount of food that should be provided.

        breed(int): The number of times agents breed in total
        kill(int): The number of times agents kill one another in total
        fight(int): The number of times agents fight one another in total
        help(int): The number of times agents help one another in total
        nothing(int): The number of times agents ignore one another in total

        id(int): A variable used to keep tracked of the issued id's to agents. See :attr:`model2.Agent.id`

        eat(int): The number of times agents ate in the last step

        food(list[Food]): A list of all the food items
        gcsteps(int): The number of total steps taken (if run/animate is used more than once)

        i_OT(list[int]): The x array for the model's graphs

        number_of_agents_OT(list[int]): A list of the number of agents over time
        mass_OT(list[float]): A list of the average agent mass over time. See :attr:`model2.Agent.mass`
        eat_OT(list[int]): A list of the rate of eating over time. See :meth:`model2.Agent.eat`

        iq_OT(list[float]): A list of the average iq over time. See :attr:`model2.Agent.iq`
        eq_OT(list[float]): A list of the average eq over time. See :attr:`model2.Agent.eq`

        breed_mass_div_OT(list[float]): A list of the average mass to final mass ratio of newborns over time. See :attr:`model2.Agent.breed_mass_div`
        breed_chance_OT(list[float]): A list of the average breeding chase of agents over time. See :attr:`model2.Agent.breed_chance`

        fight_OT(list[int]): A list of the amount of fighting over time. See :meth:`model2.fight`, :meth:`model2.interact`
        help_OT(list[int]): A list of the amount of creatures helping one another over time. See :meth:`model2.interact`
        nothing_OT(list[int]): A list of the amount of creatures ignoring one another over time. See :meth:`model2.interact`

    Raises:
        TypeError: If agents or food_count aren't integers

    """

    def __init__(
            self,
            agents: int = 500,
            food_count: int = None,
    ) -> None:
        if food_count is None:
            food_count = 5 * agents

        if (not isinstance(food_count, int)) or (not isinstance(agents, int)):
            raise TypeError

        self.size_factor = 1 / (agents / POP_DENCITY)
        self.col_const = G_COL_CONST * self.size_factor

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
        for i in range(agents):  # create agents
            mass = math.ceil(random.randrange(1, 100))
            self.agents.append(
                Agent(int(random.randrange(MIN_IQ,
                                           MAX_IQ)), int(random.randrange(MIN_EQ, MAX_EQ)),
                      math.ceil(mass * START_MASS_P),
                      random.uniform(-1, 1), self.id, mass, random.random(), random.random(), self.size_factor))
            self.id += 1

        self.i_OT = []

        self.number_of_agents_OT = []
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

    def get_fn(self) -> str:
        """
        A helper function that generates a file name for the graph/animation

        Returns:
            str: A unique file name

        See Also:
            :meth:`model2.Sim.graph`
            :meth:`model2.Sim.animate`
        """
        return '{}-{}-{}'.format(
            len(self.agents), self.gcsteps,
            time.strftime("%d%M%Y%H%M%S", time.localtime()))

    def run(self, steps: int = 1000, print_freq: int = None, max_attempts=1) -> Tuple[bool, int]:
        """
        Runs the mode

        Args:
            max_attempts: The maximum amount of attempts the simulation should try before quiting, -1 is effectively infinity
            steps(int): The amount of steps to run the model
            print_freq(int): The frequency to print progress updates

        See also:
            :meth:`model2.Sim.step`
            :meth:`model2.Sim.update_stats`

        Returns:
            (tuple): tuple containing:
                (bool: If the simulation was successful
                (int): Amount of times the simulation failed
        """
        if max_attempts == -1:
            max_attempts = 2 ** 32
        sim_copy = copy.deepcopy(self)
        if print_freq is None:
            print_freq = steps / 100
        for a in range(max_attempts):
            failed = False
            for i in range(steps):
                if not self.step():
                    self.__dict__.update(copy.deepcopy(sim_copy).__dict__)  # resetting the sim to its original state
                    failed = True
                    break
                self.update_stats(steps, i, print_freq)
            if not failed:
                return True, a
        return False, max_attempts

    def update_stats(self, steps: int, csteps: int, print_freq: int) -> None:
        """
        Update model statistics and print progress updates if necessary

        Args:
            steps(int): How many steps are their in total
            csteps(int): The current step number
            print_freq(int): How often to print progress updates
        """
        self.gcsteps += 1
        if csteps % print_freq == 0:
            print(
                "{}% ({} of {}) current population size: {} amount of food: {}".
                    format(round((csteps / steps) * 100, 2), csteps, steps,
                           len(self.agents), len(self.food)))  # print status
        # append statistics:
        self.i_OT.append(self.gcsteps)
        self.number_of_agents_OT.append(len(self.agents))
        self.mass_OT.append(np.mean([a.mass for a in self.agents]))
        self.eat_OT.append(self.eat)
        self.eat = 0
        self.iq_OT.append(np.mean([a.iq for a in self.agents]))
        self.eq_OT.append(np.mean([a.eq for a in self.agents]))
        self.breed_mass_div_OT.append(
            np.mean([a.breed_mass_div for a in self.agents]))
        self.breed_chance_OT.append(
            np.mean([a.breed_chance for a in self.agents]))

        self.fight_OT.append(self.fight / len(self.agents))
        self.help_OT.append(self.help / len(self.agents))
        self.nothing_OT.append(self.nothing / len(self.agents))

        self.help = 0
        self.fight = 0
        self.nothing = 0

    def cfood(self):
        """
        Create food
        """
        self.food = []
        for i in range(int((1 - FOOD_FLUCT) * self.food_count)):
            self.food.append(Food(random.uniform(-1, 1)))

    def step(self) -> bool:
        """
        Update the model

        Returns:
            bool: If all the agents in the model are dead
        """
        if len(self.food) < FOOD_FLUCT * self.food_count:
            self.cfood()

        if len(self.agents) <= 1:
            print("ALERT: the model has died")
            return False
        self.agents.sort(
            key=lambda ag: ag.x
        )  # sort agents by position, allows to quickly determine closest agent with low complexity
        self.food.sort(key=lambda ag: ag.x)
        food_index = 0
        debug = []
        for a in range(len(self.agents)):
            if a >= len(self.agents):  # agents can be removed but the range isn't updated
                return True

            ax = self.agents[a].x

            tf = None
            lf = None
            tmp_fi = food_index
            debug_line = "food length: " + str(len(self.food)) + " start search index: " + str(food_index)
            for i in range(food_index, len(self.food)):
                try:
                    if self.food[i].x > ax:
                        food_index = i - 1
                        tf = self.food[i]
                        debug_line += " found food index " + str(i) + " new food index set to " + str(i - 1)
                        break
                    else:
                        lf = self.food[i]
                except:
                    print("there was an unexpected crash")
                    print("Agent number " + str(a) + " out of " + str(len(self.agents)))
                    print("Food index at crash was " + str(i))
                    print("Length of food list is " + str(len(self.food)))
                    print("The food index at the start of the search was " + str(tmp_fi))
                    print("\n\n debug: ")
                    for p in debug:
                        print(p)
                    exit(-1)

            if tf is None:
                tf = self.food[0]
            if lf is None:
                lf = self.food[-1]

            dtf = mk_round(tf.x - ax)
            dlf = mk_round(lf.x - ax)

            dfood = dtf if dtf < dlf else dlf

            if abs(
                    dfood
            ) < self.col_const:  # if the abs distance is smaller than the required collision const
                # self.food.pop(food_index-1 if dtf < dlf else food_index-2)
                self.food.remove(tf if dtf < dlf else lf)  # remove food
                self.agents[a].eat(FOOD_CONST)  # eat food
                self.eat += 1  # update food statistic
                food_index -= 1
                debug_line += " food was consumed, new food index is now " + str(food_index)

            debug.append(debug_line)

            # because agents have been sorted by x values, it is easy to find the closest agent by comparing the agent before and the one after
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
                    self.col_const
            ):
                interact(self.agents[a], self.agents[a_s], self)

            self.agents[a].move(
                self.agents[a].think(
                    dfood, min_d, self.agents[a_s]
                )  # pass the environment variables to the brain of the agent
            )  # updating agent position

            self.agents[a].age()  # applying age effect

            if self.agents[a].energy < ENLB_CONST * self.agents[a].mass:
                self.agents[a].health -= ENL_CONST

            if self.agents[a].energy > ENGB_CONST * self.agents[a].mass:
                self.agents[a].health += ENG_CONST

            if (random.random() < self.agents[a].breed_chance
                    and self.agents[a].health > 0
                    and self.agents[a].mass >= self.agents[a].final_mass):
                nk = self.agents[a].breed(self.id)
                if not nk is None:
                    self.breed += 1
                    self.id += 1
                    self.agents.append(nk)

            if self.agents[a].health < -1e-5:
                self.kill += 1
                self.agents.remove(self.agents[a])
        return True

    def stats(self) -> str:
        """
        Get basic statistics

        Returns:
            str: A string containing basic statistics

        """
        return "breed:{} kill:{} eat:{}\n".format(
            self.breed, self.kill, sum(self.eat_OT)
        ) + "avg mass: {}\n".format(np.mean([
            a.mass for a in self.agents
        ])) + "avg speed: {}\n".format(np.mean([
            a.speed for a in self.agents
        ])) + "avg breed chance: {}\n".format(
            np.mean([a.breed_chance for a in self.agents
                     ])) + "avg breed mass divider: {}\n".format(
            np.mean([a.breed_mass_div for a in self.agents]))

    def graph(self, save: bool = True, info: str = None) -> str:
        """
        Graph the recorded statistics in a plt plot, as well as in an excel spreadsheet (if save is true)

        Args:
            save(bool): Save the graph + excel files
            info(str): Additional notes. If None is passed the function will ask via input so if you don't want info, pass an empty string.

        Returns:
            str: file name without extention
        """
        if info is None:
            info = input("Enter additional information about the sim: ")

        titles = [
            "Number Of Agents", "Average Agent Mass",
            "Amount of Food Consumed", "Average Agent IQ", "Average Agent EQ",
            "Average breeding mass divider", "Average Agent Breed Chance", "Fight count relative to population size",
            "Help count relative to population size", "Ignore count relative to population size"
        ]

        values = [
            self.number_of_agents_OT, self.mass_OT, self.eat_OT, self.iq_OT, self.iq_OT,
            self.breed_mass_div_OT, self.breed_chance_OT, self.fight_OT, self.help_OT, self.nothing_OT
        ]
        if len(titles) != len(values):
            raise Exception("Error len of titles must match len of vars")

        fig, axs = plt.subplots(len(values), sharex='all', figsize=(20, 60))
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
        extention = "png"
        plt.autoscale()

        if (save):
            fn = "graphs-0.3/" + self.get_fn()

            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet["A1"] = 'Amount of steps:'
            sheet["B1"] = self.gcsteps

            sheet.append([])

            sheet.append(["X:"])
            sheet.append(self.i_OT)

            xvalues = openpyxl.chart.Reference(sheet, min_col=1, min_row=4, max_col=self.gcsteps)

            for i in range(len(values)):
                sheet.append([titles[i]])
                sheet.append(values[i])

                chart = openpyxl.chart.ScatterChart()
                chart.title = titles[i] + " V.S number of steps"
                chart.style = 13
                chart.x_axis.title = 'Number of steps'
                chart.y_axis.title = titles[i]

                yvalues = openpyxl.chart.Reference(sheet, min_col=1, min_row=sheet._current_row, max_col=len(values[i]))
                series = openpyxl.chart.Series(yvalues, xvalues)
                chart.series.append(series)

                sheet.add_chart(chart)

            wb.save(fn + ".xlsx")
            pltfn = fn + "." + extention
            fig.savefig(pltfn, bbox_inches='tight')  # save graph
            # add metadata:
            im = Image.open(pltfn)
            meta = PngImagePlugin.PngInfo()
            for x in metadata:
                meta.add_text(x, str(metadata[x]))
            im.save(pltfn, extention, pnginfo=meta)
            return fn

        plt.show()  # display graph

    def animate(self, steps, res_mult=5, fps=10, bitrate=20000, print_freq=10):
        """
        Creates an animated model of the simulation

        Args:
            steps(int): The number of steps to animate
            res_mult: The size of each frame (plt figure size)
            fps(int): The animation's FPS (frames per second)
            bitrate(int): The animation's bitrate (higher -> less compression)
            print_freq(int): How frequently to print progress updates

        Returns:
            str: The filename of the animation

        Danger:
            This is highly Ram Intensive. If you plan on doing more than the simplest animation you will need either extremely high ram capacity, or the animation will crash/use the windows page file
        """
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

            r = len(row) / (2 * math.pi)

            p = np.zeros((math.ceil(2 * r) + 10, math.ceil(2 * r) + 10))

            dist_proj = 2 * math.pi / len(row)
            angle = 0
            for v in row:
                x = round(r * math.cos(angle) + r)
                y = round(r * math.sin(angle) + r)
                p[y][x] = v
                p[y + 1][x] = v
                p[y - 1][x] = v
                p[y][x + 1] = v
                p[y][x - 1] = v
                angle += dist_proj

            ims.append([
                plt.imshow(p,
                           interpolation='nearest',
                           aspect='auto')
            ])
            p = None
            row = None
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
        # optimize:
        # de-enitialize varibles:
        fig = None
        ims = None
        ani = None
        # call garbage colector:
        gc.collect()
        # return animation file name
        return "animations-0.1/" + self.get_fn() + '.mp4'
