Welcome to Ecosystem Project's documentation!
=============================================
| Author: Inbar Koursh
| Instructor: Shlomo Rozenfeld
| This project is submitted to Moach at Hemda institute.

To see the source code you can go to the GitHub repository here: https://github.com/ikoursh/EcosystemProject

.. Note:: Because the project is still in alpha, the repository is not publicly available.


Quick Setup
===========
Hi, this will be a quick tutorial for how to setup the simulation

Downloading and installing the simulation
-----------------------------------------

.. code-block:: bash

	git clone https://github.com/ikoursh/EcoSystemProject
	cd EcoSystemProject/proj
	pip -r requirements.txt

If you want to add support for animation you will need an installation of ffmpeg. To do so you can go `here <https://ffmpeg.org/download.html>`_ (don't forget to add it to PATH, `this <https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/>`_ is a great explanation)
 Note that pip install ffmpeg does not seem to work, however, linux users may use apt.

Done!
You can now import the module from python

.. Hint:: It's always a good idea to setup a virtual environment

A simple example
----------------

.. code-block:: python

	from model2 import Sim
	my_sim = Sim()
	my_sim.run(max_attempts=3)

.. SeeAlso:: :meth:`model2.Sim.run` :class:`model2.Sim`



More advanced users
-------------------

For users who desire more control, see the :ref:`Global Paramaters` section.
Aditionaly, it is possible to manualy call the :meth:`model2.Sim.step` function directley for more persice control.
See the source code for more information.


The Simulation
==============

Global Paramaters
-----------------

.. _Global Paramaters:

The simulation makes use of a config.ini file that keeps track of the global parameters.
These are the global constants that define the simulation

*	**INT_CONST** = 1 - Energy cost for intelligence (IQ, EQ average)
*	**ENLB_CONST** = 0.5 - energy to mass ratio used to determine if an agent is sick if so the agent starts to lose health
*	**ENGB_CONST** = 0.5 – energy to mass ratio used to determine if an agent is healthy, used to gain health and to gain mass if the agent is still growing
*	**ENL_CONST** = 1 - the amount of health lost if an agent’s energy is under the threshold.
*	**ENG_CONST** = 4 - the amount of energy gained if an agent is above the energy threshold
*	**MAX_LIFE_SPAN** = 200 - the maximum amount of steps an agent with mass 100 can survive after reaching maturity
*	**AGE_CONST** = ENG_CONST - (100 / MAX_LIFE_SPAN) - Age suffered every step, derived from the maximum life span and the amount of health an agent can gain per turn.
*	**POP_DENCITY** = 1 - controls how concentrated is the populus (map scaled size)
*	**AGING_TIME** = 0.99 - the mass percentage required before maturity (age starts)
*	**G_SPEED_FACTOR** = 1 - controls universal speed, provides a way to control gravity and friction
*	**FOOD_CONST** = 25 - how much energy a food item contains
*	**START_MASS_P** = 0.95 – The mass to final mass ratio for the initial population
*	**G_FOOD_COL_CONST** = 0.1 - the global accuracy for food collisionss (actual is scaled)
*	**G_FIGHT_COL_CONST** = 0.1 - the global accuracy for fight collisionss (actual is scaled)
*	**MIN_IQ** = 1 - the minimum number of hidden neurons (per layer).
*	**MAX_IQ** = 10 – the maximum number of hidden neurons (per layer)
*	**MIN_EQ** = 1– the minimum number of hidden neurons (per layer)
*	**MAX_EQ** = 10 - the maximum number of hidden neurons (per layer)
*	**FOOD_FLUCT** = 1 - 0.3 – the percentage food is allowed to dip before it is reproduced.
*	**GROUP_FACTOR** = 100 - A factor applied to the collision constant to define the minimum distance between 2 agents that are in the same group

.. Note:: these values may not be always up to date with the current config. Check `here <https://github.com/ikoursh/EcosystemProject/blob/master/proj/config.ini>`_ for the most up to date values, or your own config.ini(located at proj/config.ini) for your specific values.


.. module:: model2



The Simulation class
--------------------

.. autoclass:: Sim
   :members:

The Agent class
---------------

.. autoclass:: Agent
   :members:

The Food class
--------------
.. autoclass:: Food


Helper Functions
----------------

.. autofunction:: isZero

.. autofunction:: map_from_to

.. autofunction:: fight

.. autofunction:: interact

.. autofunction:: mk_round



The Neural Network
==================

.. module:: nn


The NeuralNetwork class
-----------------------

.. autoclass:: NeuralNetwork
   :members:


The Neural Network Layer class
------------------------------

.. autoclass:: NNLayer
   :members:



Helper Functions
----------------

.. autofunction:: s

.. autofunction:: m


