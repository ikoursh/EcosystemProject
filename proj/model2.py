#!/usr/bin/env python3

# Ecosystem project - studying natural biological systems using a simulated ecosystem and reinforcement learning.
# Copyright (C) 2020 Inbar Koursh
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import copy
import gc
import os
import random
import time
from typing import Tuple

import matplotlib

import matplotlib.pyplot as plt

import numpy as np
from matplotlib import animation
from nn import NeuralNetwork

from PIL import Image  # work with metadata via pillow
from PIL import PngImagePlugin

import openpyxl  # work with excel
import savReaderWriter  # work with spss

import pickle  # support serialization

import json  # work with gui

matplotlib.get_backend()

import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 4:
    raise Exception(
        "Python 3.4 or higher is required. Download the latest version here https://www.python.org/downloads/ ")

if sys.version_info[0] > 3:
    print("WARNING this program was write to support python 3. Use any future versions at your discretion")

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read(os.path.join(dir_path, 'config.ini'))

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
GROUP_FACTOR = float(config["VARIABLES"]["GROUP_FACTOR"])


def map_from_to(x: float, a: float, b: float, c: float, d: float) -> float:
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


# create folders for model outputs
GRAPHS_FOLDER = "/graphs-0.3"
ANIMATION_FOLDER = '/animations-0.1'
if not os.path.isdir('.' + GRAPHS_FOLDER):
    os.mkdir('.' + GRAPHS_FOLDER)
if not os.path.isdir('.' + ANIMATION_FOLDER):
    os.mkdir('.' + ANIMATION_FOLDER)

if not os.path.isdir("./saved"):
    os.mkdir("./saved")


class Agent:
    """
    A class that models the behavior of wild creatures.


    Args:
        x (float): The agents initial position. See :attr:`model2.Agent.x`
        id(int): An id used by the simulation class to keep track of agents. See :attr:`model2.Agent.id`

        iq (int): The number of neurons in every hidden layer of the agent's neural network that is responsible for movement. See :attr:`model2.Agent.iq`

        eq (int): The number of neurons in every hidden layer of the agent's neural network that is responsible for agent to agent interactions. See :attr:`model2.Agent.eq`

        mass(int): The mass of the agent represents its size. See :attr:`model2.Agent.mass`
        final_mass(int): The final mass of the agent. See :attr:`model2.Agent.final_mass`

        breed_mass_div(float): The initial mass to final mass ratio of the agents children. See :attr:`model2.Agent.breed_mass_div`
        breed_chance(float): The chance for the agent to breed at every step. See :attr:`model2.Agent.breed_chance`

        size_factor(float): A variable used by the sim's movement and collision engines to control the size of the simulation. See :attr:`model2.Sim.size_factor`

        move_brain(NeuralNetwork): The neural network the agent will use to decide where to move. This is either provided by the creature's parent (via a mutated brain) or is generated from scratch (for the initial population) See :attr:`model2.Agent.move_brain`.
        social_brain(NeuralNetwork): The neural network the agent will use to interact with other agents. This is either provided by the creature's parent (via a mutated brain) or is generated from scratch (for the initial population) See :attr:`model2.Agent.social_brain`.

        parent_id(int): This variable is used to detect close family by the simulation. It is then used as a variable in agent interactions. See :attr:`model2.Agent.parent_id`

    Attributes:
        energy(float): Tracks the amount of energy an agent has. energy is acquired by eating and lost by moving or thinking. Energy allows agents to grow and regenerate health. If an agent has low energy, he will take damage. See :meth:`model2.Agent.think`, :meth:`model2.Agent.move`, :meth:`model2.interact`

        speed(float): The maximum velocity at which the creature can move. Inversely related to mass (1/mass)
        health(float): How much damage can a creature sustain. When it reaches 0, the creature dies.

        x (float): The agents position. See :meth:`model2.Agent.move`.

        id(int): An id used by the simulation class to keep track of agents. See :attr:`model2.Agent.parent_id` for use case.

        iq (int): The number of neurons in every hidden layer of the agent's neural network that is responsible for movement. See :attr:`model2.Agent.move_brain` for use case.

        eq (int): The number of neurons in every hidden layer of the agent's neural network that is responsible for agent to agent interactions. See :attr:`model2.Agent.social_brain` for use case

        mass(int): The mass of the agent, represents its size.
        final_mass(int): The final mass of the agent.

        breed_mass_div(float): The initial mass to final mass ratio of the agent's children. See :meth:`model2.Agent.breed`.
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
            if iq == 1:  # if the size of the hidden layers is 1, the amount of hidden layers doesn't matter
                self.move_brain = NeuralNetwork([3, 1])
            else:
                self.move_brain = NeuralNetwork([3, iq, iq, 1])

        if social_brain is not None:
            self.social_brain = social_brain
        else:
            if eq == 1:  # if the size of the hidden layers is 1, the amount of hidden layers doesn't matter
                self.social_brain = NeuralNetwork([4, eq, 2])
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

    def age(self) -> None:
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

    def breed(self, nid: int) -> 'Agent':
        """
        Make the agent have a child.
        Note that the child's mass is removed from the agent's mass on childbirth


        See Also:
            :attr:`model2.Agent.breed_chance`
            :attr:`model2.Agent.breed_mass_div`

        Args:
            nid(int): The id of the new child

        Returns:
            Agent: A child that is a mutated version of the agent, None if the agent died in childbirth
        """
        nb = copy.deepcopy(self.move_brain)
        nb.mutate()

        nsb = copy.deepcopy(self.social_brain)
        nsb.mutate()

        nm = np.ceil((self.mass + random.randrange(-10, 10)) * self.breed_mass_div)
        self.health -= nm
        self.mass -= nm
        if self.health <= 0 or self.mass < 1 or nm < 1:
            self.health = -1
            return None  # died in childbirth
        return Agent(self.iq, self.eq, nm, self.x + random.uniform(0.001, -0.001), nid,
                     np.ceil(nm / self.breed_mass_div),
                     self.breed_mass_div + random.uniform(0.01, -0.01), self.breed_chance + random.uniform(0.01, -0.01),
                     self.size_factor, nb, nsb, self.id)

    def eat(self, food: int) -> None:
        """
        Make the agent eat, increases agent energy (:attr:`model2.Agent.energy`) and mass (:attr:`model2.Agent.mass`) if the agent has not reached its final mass and has energy to spare

        Args:
            food(int): The amount of food the agent should eat
        """
        if self.mass < self.final_mass and self.energy / self.mass > ENGB_CONST:
            self.mass += food  # update mass and speed
            self.speed = (1 / self.mass) * self.size_factor * G_SPEED_FACTOR
        else:
            self.energy += food

    def __str__(self) -> str:
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
    a1.energy -= a1.eq * INT_CONST  # subtract energy used for interaction thought
    a2.energy -= a2.eq * INT_CONST
    close_family = a1.parent_id == a2.id or a2.parent_id == a1.id
    s1 = a1.social_brain.feed_forward(
        [1 if close_family else 0, a1.energy / a1.mass, a2.energy / a2.mass, 1 if a1.mass > a2.mass else 0])
    s2 = a2.social_brain.feed_forward(
        [1 if close_family else 0, a2.energy / a2.mass, a1.energy / a1.mass, 1 if a1.mass < a2.mass else 0])

    if s1[0] > 0.5 or s2[0] > 0.5:  # if either agent wants to fight
        fight(a1, a2)
        s.fight += 1
    if s1[1] > 0.5:  # if an agent wants to help
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
    if d > 1:  # if the distance between them is greater than 1, then the other distance must be smaller Ex. 1.2 -> -0.8
        return d - 2
    if d < -1:  # if the distance between them is smaller than -1, then the other distance must be smaller Ex. -1.2 -> 0.8
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

        id(int): A variable used to keep track of the issued id's to agents. See :attr:`model2.Agent.id`

        eat(int): The number of times agents ate in the last step

        food(list[Food]): A list of all the food items
        gcsteps(int): The number of total steps taken (if run/animate is used more than once)
        dataPoints(int): The nummber of datapoints recorded

        i_OT(list[int]): The x array for the model's graphs - composed of datapoints over time

        number_of_agents_OT(list[int]): A list of the number of agents over time
        mass_OT(list[float]): A list of the average agent mass over time. See :attr:`model2.Agent.mass`
        eat_OT(list[int]): A list of the rate of eating over time. See :meth:`model2.Agent.eat`

        iq_OT(list[float]): A list of the average iq over time. See :attr:`model2.Agent.iq`
        eq_OT(list[float]): A list of the average eq over time. See :attr:`model2.Agent.eq`

        breed_mass_div_OT(list[float]): A list of the average mass to final mass ratio of newborns over time. See :attr:`model2.Agent.breed_mass_div`
        breed_chance_OT(list[float]): A list of the average breeding chase of agents over time. See :attr:`model2.Agent.breed_chance`

        fight_OT(list[int]): A list of the amount of fighting over time. See :meth:`model2.fight`, :meth:`model2.interact`
        help_OT(list[int]): A list of the number of creatures helping one another over time. See :meth:`model2.interact`
        nothing_OT(list[int]): A list of the number of creatures ignoring one another over time. See :meth:`model2.interact`

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
        self.dataPoints = 0
        self.interactions = 0
        for i in range(agents):  # create initial population
            mass = np.ceil(random.randrange(1, 100))
            self.agents.append(
                Agent(int(random.randrange(MIN_IQ,
                                           MAX_IQ)), int(random.randrange(MIN_EQ, MAX_EQ)),
                      np.ceil(mass * START_MASS_P),
                      random.uniform(-1, 1), self.id, mass, random.random(), random.random(), self.size_factor))
            self.id += 1

        # create statistic helpers
        self.group()
        self.i_OT = []

        self.number_of_agents_OT = []
        self.mass_OT = []
        self.eat_OT = []

        self.iq_OT = []
        self.eq_OT = []

        self.breed_mass_div_OT = []
        self.breed_chance_OT = []

        self.interactions_OT = []

        self.fight_OT = []
        self.help_OT = []
        self.nothing_OT = []

        self.relative_groups_OT = []
        self.close_family_in_group_OT = []
        self.cfood()

        return

    def get_fn(self) -> str:
        """
        A helper function that generates a file name for the graph/animation

        Returns:
            str: A unique filename

        See Also:
            :meth:`model2.Sim.graph`
            :meth:`model2.Sim.animate`
        """
        return '{}-{}-{}'.format(
            len(self.agents), self.gcsteps,
            time.strftime("%d%M%Y%H%M%S", time.localtime()))

    def save(self, file: str = None) -> None:
        """
        Save the simulation state to a file.

        Args:
            file: The path to save the state to.

        Throws:
            ValueError: if the filename does not end with .envs
        """
        if file is not None and file.endswith(".envs"):
            raise ValueError("File must end with .envs")
        pickle.dump(self, open(file if file is not None else "save/" + self.get_fn() + ".envs", "w"), 4)

    @classmethod
    def load(cls, filename: str) -> "Sim":
        """
        Load a simulation from a file
        Args:
            filename: the path to the file

        Returns:
            the loaded sim
        """
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def run(self, steps: int = 1000, print_freq: int = None, max_attempts: int = 1, data_point_freq: int = 10,
            gui: bool = False) -> Tuple[bool, int]:
        """
        Runs the mode

        Args:
            max_attempts: The maximum amount of attempts the simulation should try before quitting, -1 is effectively infinity
            steps(int): The number of steps to run the model
            print_freq(int): The frequency to print progress updates
            data_point_freq: The frequency to update data points. Note: the maximum number of data points for excel is 16,383.

        See also:
            :meth:`model2.Sim.step`
            :meth:`model2.Sim.update_stats`

        Returns:
            (tuple): tuple containing:
                (bool: If the simulation was successful
                (int): Amount of times the simulation failed
        """
        if max_attempts == -1:  # if maximum attempts is -1, make it effectively infinite
            max_attempts = 2 ** 32

        sim_copy = copy.deepcopy(self)  # create a copy of the sim to use as a restore point

        if print_freq is None:  # if print frequency is not specified, set it so that the model prints every 1% of steps
            print_freq = steps / 100
        for a in range(max_attempts):
            failed = False
            for i in range(steps):
                if not self.step():  # call step, if it failed, stop this attempt
                    self.__dict__.update(copy.deepcopy(sim_copy).__dict__)  # resetting the sim to its original state
                    failed = True
                    break
                if i % print_freq == 0:
                    self.progress(steps, i, gui)
                if i % data_point_freq == 0:
                    self.update_stats()  # update statistics
            if not failed:
                self.progress(steps, steps, gui)
                return True, a
        return False, max_attempts

    def group(self) -> int:
        """
        Group agents via position
        Returns:
            number of groups
        """
        prev_a = self.agents[0]
        prev_a.group = 0
        for a in self.agents:
            a.group = prev_a.group + (0 if abs(a.x - prev_a.x) < self.col_const * GROUP_FACTOR else 1)
            prev_a = a
        return prev_a.group

    def progress(self, steps: int, csteps: int, gui: bool) -> None:
        """
        Print model progress
         Args:
            steps(int): How many steps are there in total
            csteps(int): The current step number
        """
        if gui:
            print(json.dumps({
                "steps": csteps,
                "food": len(self.food),
                "agents": len(self.agents)
            }))
            sys.stdout.flush()
        else:
            print(
                "{}% ({} of {}) current population size: {} amount of food: {}"
                    .format(round((csteps / steps) * 100, 2),
                            csteps, steps,
                            len(self.agents),
                            len(self.food)))  # print status

    def update_stats(self) -> None:
        """
        Update model statistics
        """
        agent_count = len(self.agents)  # save time
        self.gcsteps += 1
        self.dataPoints += 1

        # append statistics:
        self.i_OT.append(self.gcsteps)
        self.number_of_agents_OT.append(agent_count)
        self.interactions_OT.append(self.interactions)
        self.interactions = 0

        # group based statistics:
        self.relative_groups_OT.append(self.group())

        # in order to reduce compute time all for data collection will occur once

        helper_mass = np.ndarray([agent_count])
        helper_iq = np.ndarray([agent_count])
        helper_eq = np.ndarray([agent_count])
        helper_bmd = np.ndarray([agent_count])
        helper_bch = np.ndarray([agent_count])
        helper_group_i = -1
        helper_group_size = []
        helper_close_family_group = []

        for i in range(agent_count):
            a = self.agents[i]
            helper_mass[i] = a.mass
            helper_iq[i] = a.iq
            helper_eq[i] = a.eq
            helper_bmd[i] = a.breed_mass_div
            helper_bch[i] = a.breed_chance
            if a.group != helper_group_i:
                a.group = helper_group_i
                helper_close_family_group.append([])
                helper_group_size.append(0)
                helper_group_i += 1

            helper_close_family_group[helper_group_i].extend([a.id, a.parent_id])
            helper_group_size[helper_group_i] += 1

        self.close_family_in_group_OT.append(np.mean(
            [(len(helper_close_family_group[i]) - len(set(helper_close_family_group[i]))) / helper_group_size[i] for i
             in
             range(helper_group_i)]))  # the average amount of duplicates is the amount of close family
        self.mass_OT.append(np.mean(helper_mass))
        self.eat_OT.append(self.eat)
        self.eat = 0
        self.iq_OT.append(np.mean(helper_iq))
        self.eq_OT.append(np.mean(helper_eq))
        self.breed_mass_div_OT.append(np.mean(helper_bmd))
        self.breed_chance_OT.append(np.mean(helper_bch))

        self.fight_OT.append(self.fight / agent_count)
        self.help_OT.append(self.help / agent_count)
        self.nothing_OT.append(self.nothing / agent_count)

        self.help = 0
        self.fight = 0
        self.nothing = 0

    def cfood(self) -> None:
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
        self.gcsteps += 1
        if len(self.food) < FOOD_FLUCT * self.food_count:
            self.cfood()

        agent_count = len(self.agents)

        if agent_count <= 1:
            print("ALERT: the model has died")
            return False
        self.agents.sort(
            key=lambda ag: ag.x
        )  # sort agents by position, allows to quickly determine the closest agent with low complexity
        self.food.sort(key=lambda ag: ag.x)
        food_index = 0  # used to find closest food item with low complexity

        for a in range(agent_count):
            agent_count = len(self.agents)

            if a >= agent_count:  # agents can be removed but the range isn't updated
                return True

            ax = self.agents[a].x

            tf = None
            lf = None
            for i in range(food_index, len(self.food)):
                if self.food[i].x > ax:
                    food_index = i - 1
                    tf = self.food[i]
                    break
                else:
                    lf = self.food[i]

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
                self.food.remove(tf if dtf < dlf else lf)  # remove food
                self.agents[a].eat(FOOD_CONST)  # eat food
                self.eat += 1  # update food statistic
                food_index -= 1

            # because agents have been sorted by x values, it is easy to find the closest agent by comparing the agent before and the one after

            ta = self.agents[a + 1 if a != agent_count - 1 else 0]
            la = self.agents[(a - 1) if a != 1 else agent_count - 1]

            dta = mk_round(ta.x - ax)
            dla = mk_round(la.x - ax)

            if dta < dla:
                dagent = dta
                a_s = ta
            else:
                dagent = dla
                a_s = la

            if abs(dagent) < self.col_const:
                self.interactions += 1
                interact(self.agents[a], a_s, self)

            self.agents[a].move(
                self.agents[a].think(
                    dfood, dagent, a_s
                )  # pass the environment variables to the brain of the agent
            )  # updating agent position

            self.agents[a].age()  # applying age effect

            if self.agents[a].energy < ENLB_CONST * self.agents[a].mass:  # if the agent is sick, lose health
                self.agents[a].health -= ENL_CONST

            if self.agents[a].energy > ENGB_CONST * self.agents[a].mass:  # if the agent is healthy, gain health
                self.agents[a].health += ENG_CONST

            if (random.random() < self.agents[a].breed_chance
                    and self.agents[a].health > 0
                    and self.agents[a].mass >= self.agents[a].final_mass):  # determine if an agent will breed
                nk = self.agents[a].breed(self.id)
                if nk is not None:  # if the agent did not die in childbirth, append the newborn to the sim
                    self.breed += 1
                    self.id += 1
                    self.agents.append(nk)

            if self.agents[a].health < -1e-5:  # if the agent's health is <=0, kill it
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

    def graph(self, info: str = None, output=("plt", "excel")) -> str:
        """
        Graph the recorded statistics in a plt plot, in an excel spreadsheet or in an ssps compatible file.

        Args:
            output (Tuple[str]): the output formats to use.
            info(str): Additional notes for the plt plot. If None is passed the function will ask via input so if you don't want info, pass an empty string.

        Returns:
            str: folder name for output
        """
        compatible_out = ["plt", "excel", "spss"]
        e = False
        for ro in output:
            if ro not in compatible_out:
                e = True
                print("WARNING, output format {} is not supported, it will be skipped".format(ro))
        if e:
            print("We currently support " + str(compatible_out))

        if info is None:
            info = input("Enter additional information about the sim: ")

        titles = [
            "Number Of Agents", "Average Agent Mass",
            "Amount of Food Consumed", "Average Agent IQ", "Average Agent EQ",
            "Average breeding mass divider", "Average Agent Breed Chance", "Fight count relative to population size",
            "Help count relative to population size", "Ignore count relative to population size",
            "Number of groups", "Close family ration in group"
        ]

        values = [
            self.number_of_agents_OT, self.mass_OT, self.eat_OT, self.iq_OT, self.iq_OT,
            self.breed_mass_div_OT, self.breed_chance_OT, self.fight_OT, self.help_OT, self.nothing_OT,
            self.relative_groups_OT, self.close_family_in_group_OT
        ]
        extention = "png"
        fn = "graphs-0.3/" + self.get_fn()
        os.mkdir(fn)

        try:
            if "plt" in output:
                if len(titles) != len(values):
                    raise Exception("Error len of titles must match len of vars")

                fig, axs = plt.subplots(len(values), sharex='all', figsize=(20, 60))
                metadata = dict()
                for i in range(len(values)):
                    axs[i].plot(self.i_OT, values[i], linewidth=0.25)
                    axs[i].axes.set_ylim([0, max(values[i])])
                    axs[i].set_ylabel(titles[i])

                    metadata["Final" + titles[i]] = values[i][-1]

                axs[0].axes.set_xlim([0, self.dataPoints])
                axs[0].set_title(
                    "Simulation with {} initial agents and {} steps\nDate: {}\nNotes: {}\n\nStats:\n{}\n"
                        .format(len(self.agents), self.gcsteps, time.strftime("%D"), info,
                                self.stats()), )

                axs[-1].set_xlabel("Number Of Data Points")

                plt.tight_layout()
                plt.autoscale()

                pltfn = fn + "/plt." + extention
                fig.savefig(pltfn, bbox_inches='tight')  # save graph
                # add metadata:
                im = Image.open(pltfn)
                meta = PngImagePlugin.PngInfo()
                for x in metadata:
                    meta.add_text(x, str(metadata[x]))
                im.save(pltfn, extention, pnginfo=meta)
        except:
            print("error in generating plt file")
        transposed_data = []
        for i in range(self.dataPoints):
            transposed_data.append([j[i] for j in values])
        try:
            if "excel" in output:
                if len(values[0]) > 1048576:
                    print("to manny data points, skipping excel")
                else:
                    wb = openpyxl.Workbook(write_only=True)
                    sheet = wb.create_sheet()
                    sheet.append(titles)
                    for i in transposed_data:
                        sheet.append(i)
                    wb.save(fn + "/excel.xlsx")
        except:
            print("error in generating excel file")

        if "spss" in output:
            savFileName = fn + '/spss.sav'
            varNames = [i.replace(" ", "_") for i in titles]
            varTypes = dict()
            for t in varNames:
                varTypes[t] = 0
            with savReaderWriter.SavWriter(savFileName, varNames, varTypes) as writer:
                for i in range(self.dataPoints):
                    writer.writerow(transposed_data[i])

        return os.getcwd() + "\\" + fn.replace("/", "\\");

    def animate(self, steps, res_mult=5, fps=10, bitrate=20000, print_freq=10, data_point_freq: int = 10,
                gui: bool = False) -> str:
        """
        Creates an animated model of the simulation

        Args:
            steps(int): The number of steps to animate
            res_mult: The size of each frame (plt figure size)
            fps(int): The animation's FPS (frames per second)
            bitrate(int): The animation's bitrate (higher -> less compression)
            print_freq(int): How frequently to print progress updates
            data_point_freq: The frequency to update data points. Note: the maximum number of data points for excel is 16,383.

        Returns:
            str: The filename of the animation

        Danger:
            As of now this function has a memory leak. Until it is resolved you will need extremely high ram capacity
        """
        # TODO: fix memory leak
        ims = []
        fig = plt.figure(figsize=(res_mult, res_mult))
        for i in range(steps):
            if not self.step():
                return
            if i % data_point_freq == 0:
                self.update_stats()
            if i % print_freq == 0:
                self.progress(steps, i, gui)
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

            r = len(row) / (2 * np.pi)

            p = np.zeros((np.ceil(2 * r) + 10, np.ceil(2 * r) + 10))

            dist_proj = 2 * np.pi / len(row)
            angle = 0
            for v in row:
                x = round(r * np.cos(angle) + r)
                y = round(r * np.sin(angle) + r)
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
            acu = None
            r = None
            dist_proj = None
            p = None
            row = None
            angle = None
            gc.collect()
        self.progress(steps, steps, gui)

        ani = animation.ArtistAnimation(fig,
                                        ims,
                                        interval=100,
                                        blit=False,
                                        repeat_delay=1000)

        # Set up formatting for the movie files
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=bitrate)

        fn = "animations-0.1/" + self.get_fn() + '.mp4'
        ani.save(fn, writer=writer)

        # optimize:
        # de-initialize variables:
        fig = None
        ims = None
        ani = None
        writer = None
        Writer = None
        # call garbage collector:
        gc.collect()
        # return animation file name
        return fn
