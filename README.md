<h1 align="center">Welcome to the EcosystemProject 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://inbarkoursh.com/ecosystemproject/" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" target="_blank">
    <img alt="License: GPL V3" src="https://img.shields.io/badge/License-GPL V3-yellow.svg" />
  </a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fikoursh%2FEcosystemProject?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fikoursh%2FEcosystemProject.svg?type=shield"/></a>
</p>

> Studying natural biological systems using a simulated ecosystem and reinforcement learning.

Project Paper
==================================
If you are interestead in the paper accompanying this project you can find it [here](https://inbarkoursh.com/ecosystemproject/paper.pdf).  
The word version is also available [here](Project%20Paper.docx).

Setup
=====

Initial setup (always required)
-------------------------------
``` bash
git clone https://github.com/ikoursh/EcosystemProject
cd EcosystemProject/proj
pip install -r requirements.txt
```

Setup the GUI (Windows only)
----------------------------
This is useful for people who do not feel comfortable with the command line.
1. Complete the initial setup
2. install the GUI from EcosystemProject/GUI/dist/EcoSystem-Project-GUI Setup 1.0.0.exe
3. Open the program
4. Go to the setting tab and enter the path to proj/auto.py

You are now done!

Spell integration
-----------------

For both GUI and CLI spell is a useful tool. It allows you to run your commands on a server, thus freeing up your computer's resources. You can also choose to run simulations on more powerful systems.

Because of the nature of this project Spell is highly recommended. Click [here](https://web.spell.ml/refer/ikoursh) to create a free account.

Billing costs for Spell are available [here](https://spell.ml/faqs#how-much-does-it-cost-for-developer) but I recommend sticking to the free version.

Use
===
In this section, I will outline 3 ways to use this project.


## Using [auto.py](proj/auto.py)

[auto.py](proj/auto.py) is the recommended way to use envSim.

Typing ```python auto.py --help``` into the command line will get you this hepfull message:
``` 
usage: auto.py [-h] [-s STEPS] [-p POP] [-f FOOD] [-a] [-v] [-dp DP] [--spss] [--no-excel] [--no-plt] [--gui]

Run an ecosystem simulation

optional arguments:
  -h, --help  show this help message and exit
  -s STEPS    Number of steps to run the sim (default: 1000)
  -p POP      Initial population size (default: 500)
  -f FOOD     Ammount of food (default: None)
  -a          enable animation (default: False)
  -v          enable verbose (default: False)
  -dp DP      Maximum number of data points, defaults to excel maximum (1048576) if excel is used. Else, defaults to
              the number of steps (default: 1048576)
  --spss      output data in SPSS data format. Note that this will NOT force data points to max. (default: False)
  --no-excel  Don't output data to excel format. Will be enabled automatically if the number of data points exceed
              1048576 (default: False)
  --no-plt    Don't generate plt preview (default: False)
  --gui       Used to output progress in json format for GUI (in beta) (default: False)

```

## Using the GUI
Simulations can be created using the new simulation tab. 
Simply enter the parameters and the simulation command will be generated for you! Once you are done click "create simulation" and the GUI will run the command for you.

All simulation can be seen in the "My simulations" tab. Once a simulation is completed (as indicated by the progress bar) you can click on it and it will take you directly to the output files.


## Importing it as a library
Please check out the API documentation for instructions to use this project as a library.


API Documentation
================
This project was documented in accordance with the Google API standards and was compiled using SPHINX.

https://inbarkoursh.com/ecosystemproject/

Miscellaneous
=============
## Author

👤 **Inbar Koursh**

* Website: https://inbarkoursh.com
* Github: [@ikoursh](https://github.com/ikoursh)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Inbar Koursh](https://github.com/ikoursh).<br />
The code in this project is [GPL V3](https://www.gnu.org/licenses/gpl-3.0.en.html) licensed. <br />
The accompanying Project paper is licensed under the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

## FOSSA

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fikoursh%2FEcosystemProject.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fikoursh%2FEcosystemProject?ref=badge_large)

***


_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
