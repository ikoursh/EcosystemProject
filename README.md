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

http://ecosystem.inbarkoursh.com/

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

# 3rd-Party Software for [EcosystemProject]()

The following 3rd-party software packages may be used by or distributed with **EcosystemProject**.  This document was automatically generated by [FOSSA](https://fossa.com) on 11/15/20; any information relevant to third-party vendors listed below are collected using common, reasonable means.






## Direct Dependencies


Package|Licenses
-------|--------
**[argparse (0.9.1.win32)](#argparse-0-9-1-win32)**|
**[configparser (5.0.1)](#configparser-5-0-1)**|MIT
**[electron-store (6.0.1)](#electron-store-6-0-1)**|MIT
**[matplotlib (1.4.3.win-amd64)](#matplotlib-1-4-3-win-amd64)**|MIT, **Multi-license:** BSD-3-Clause *OR* MIT, **Multi-license:** BSD-3-Clause *OR* Python-2.0, BSD-3-Clause, Apache-2.0
**[numpy (1.19.4)](#numpy-1-19-4)**|
**[openpyxl (3.0.5)](#openpyxl-3-0-5)**|MIT
**[Pillow (8.0.1)](#Pillow-8-0-1)**|BSD-3-Clause
**[savReaderWriter (3.4.2)](#savReaderWriter-3-4-2)**|MIT
**[yarn (1.22.10)](#yarn-1-22-10)**|BSD-2-Clause



### Details


#### **argparse (0.9.1.win32)**


* Declared License(s)



* Discovered License(s)
    * Apache-2.0
    * **Multi-license:** GPL-3.0-only *OR* MIT






---
---

#### **configparser (5.0.1)**


* Declared License(s)
    * MIT
        * Attribution:
        Copyright Jason R. Coombs
		
		Permission is hereby granted, free of charge, to any person obtaining a copy
		of this software and associated documentation files (the "Software"), to
		deal in the Software without restriction, including without limitation the
		rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
		sell copies of the Software, and to permit persons to whom the Software is
		furnished to do so, subject to the following conditions:
		
		The above copyright notice and this permission notice shall be included in
		all copies or substantial portions of the Software.
		
		THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
		IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
		FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
		AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
		LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
		FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
		IN THE SOFTWARE.
		



* Discovered License(s)






---
---

#### **electron-store (6.0.1)**


* Declared License(s)
    * MIT
        * Attribution:
        Copyright (c) Sindre Sorhus 
		Permission is hereby granted, free of charge, to any person obtaining a copy
		of this software and associated documentation files (the "Software"), to deal
		in the Software without restriction, including without limitation the rights
		to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
		copies of the Software, and to permit persons to whom the Software is
		furnished to do so, subject to the following conditions:
		
		The above copyright notice and this permission notice shall be included in all
		copies or substantial portions of the Software.
		
		THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
		IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
		FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
		AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
		LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
		OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
		SOFTWARE.



* Discovered License(s)






---
---

#### **matplotlib (1.4.3.win-amd64)**


* Declared License(s)
    * MIT
        * Attribution:
        TERMS AND CONDITIONS
		
		   1. Permission is hereby granted, free of charge, to any person 
		obtaining a copy of the STIX Fonts-TM set accompanying this license 
		(collectively, the "Fonts") and the associated documentation files 
		(collectively with the Fonts, the "Font Software"), to reproduce and 
		distribute the Font Software, including the rights to use, copy, merge 
		and publish copies of the Font Software, and to permit persons to whom 
		the Font Software is furnished to do so same, subject to the following 
		terms and conditions (the "License").
		
		   2. The following copyright and trademark notice and these Terms and 
		Conditions shall be included in all copies of one or more of the Font 
		typefaces and any derivative work created as permitted under this 
		License:
		
			Copyright (c) 2001-2005 by the STI Pub Companies, consisting of 
		the American Institute of Physics, the American Chemical Society, the 
		American Mathematical Society, the American Physical Society, Elsevier, 
		Inc., and The Institute of Electrical and Electronic Engineers, Inc. 
		Portions copyright (c) 1998-2003 by MicroPress, Inc. Portions copyright 
		(c) 1990 by Elsevier, Inc. All rights reserved. STIX Fonts-TM is a 
		trademark of The Institute of Electrical and Electronics Engineers, Inc.
		
		   3. You may (a) convert the Fonts from one format to another (e.g., 
		from TrueType to PostScript), in which case the normal and reasonable 
		distortion that occurs during such conversion shall be permitted and (b) 
		embed or include a subset of the Fonts in a document for the purposes of 
		allowing users to read text in the document that utilizes the Fonts. In 
		each case, you may use the STIX Fonts-TM mark to designate the resulting 
		Fonts or subset of the Fonts.
		
		   4. You may also (a) add glyphs or characters to the Fonts, or modify 
		the shape of existing glyphs, so long as the base set of glyphs is not 
		removed and (b) delete glyphs or characters from the Fonts, provided 
		that the resulting font set is distributed with the following 
		disclaimer: "This [name] font does not include all the Unicode points 
		covered in the STIX Fonts-TM set but may include others." In each case, 
		the name used to denote the resulting font set shall not include the 
		term "STIX" or any similar term.
		
		   5. You may charge a fee in connection with the distribution of the 
		Font Software, provided that no copy of one or more of the individual 
		Font typefaces that form the STIX Fonts-TM set may be sold by itself.
		
		   6. THE FONT SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY 
		KIND, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTIES 
		OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT 
		OF COPYRIGHT, PATENT, TRADEMARK OR OTHER RIGHT. IN NO EVENT SHALL 
		MICROPRESS OR ANY OF THE STI PUB COMPANIES BE LIABLE FOR ANY CLAIM, 
		DAMAGES OR OTHER LIABILITY, INCLUDING, BUT NOT LIMITED TO, ANY GENERAL, 
		SPECIAL, INDIRECT, INCIDENTAL OR CONSEQUENTIAL DAMAGES, WHETHER IN AN 
		ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM OR OUT OF THE USE OR 
		INABILITY TO USE THE FONT SOFTWARE OR FROM OTHER DEALINGS IN THE FONT 
		SOFTWARE.
		
		   7. Except as contained in the notice set forth in Section 2, the 
		names MicroPress Inc. and STI Pub Companies, as well as the names of the 
		companies/organizations that compose the STI Pub Companies, shall not be 
		used in advertising or otherwise to promote the sale, use or other 
		dealings in the Font Software without the prior written consent of the 
		respective company or organization.
		
		   8. This License shall become null and void in the event of any 
		material breach of the Terms and Conditions herein by licensee.
		
		   9. A substantial portion of the STIX Fonts set was developed by 
		MicroPress Inc. for the STI Pub Companies. To obtain additional 
		mathematical fonts, please contact MicroPress, Inc., 68-30 Harrow 
		Street, Forest Hills, NY 11375, USA - Phone: (718) 575-1816.
		
		
    * **Multi-license:** BSD-3-Clause
        * Attribution:
        BSD-style license for gist/yorick colormaps.
		
		Copyright:
		
		  Copyright (c) 1996.  The Regents of the University of California.
					 All rights reserved.
		
		Permission to use, copy, modify, and distribute this software for any
		purpose without fee is hereby granted, provided that this entire
		notice is included in all copies of any software which is or includes
		a copy or modification of this software and in all copies of the
		supporting documentation for such software.
		
		This work was produced at the University of California, Lawrence
		Livermore National Laboratory under contract no. W-7405-ENG-48 between
		the U.S. Department of Energy and The Regents of the University of
		California for the operation of UC LLNL.
		
		
					      DISCLAIMER
		
		This software was prepared as an account of work sponsored by an
		agency of the United States Government.  Neither the United States
		Government nor the University of California nor any of their
		employees, makes any warranty, express or implied, or assumes any
		liability or responsibility for the accuracy, completeness, or
		usefulness of any information, apparatus, product, or process
		disclosed, or represents that its use would not infringe
		privately-owned rights.  Reference herein to any specific commercial
		products, process, or service by trade name, trademark, manufacturer,
		or otherwise, does not necessarily constitute or imply its
		endorsement, recommendation, or favoring by the United States
		Government or the University of California.  The views and opinions of
		authors expressed herein do not necessarily state or reflect those of
		the United States Government or the University of California, and
		shall not be used for advertising or product endorsement purposes.
		
		
						AUTHOR
		
		David H. Munro wrote Yorick and Gist.  Berkeley Yacc (byacc) generated
		the Yorick parser.  The routines in Math are from LAPACK and FFTPACK;
		MathC contains C translations by David H. Munro.  The algorithms for
		Yorick's random number generator and several special functions in
		Yorick/include were taken from Numerical Recipes by Press, et. al.,
		although the Yorick implementations are unrelated to those in
		Numerical Recipes.  A small amount of code in Gist was adapted from
		the X11R4 release, copyright M.I.T. -- the complete copyright notice
		may be found in the (unused) file Gist/host.c.
		 *OR* MIT
        * Attribution:
        TERMS AND CONDITIONS
		
		   1. Permission is hereby granted, free of charge, to any person 
		obtaining a copy of the STIX Fonts-TM set accompanying this license 
		(collectively, the "Fonts") and the associated documentation files 
		(collectively with the Fonts, the "Font Software"), to reproduce and 
		distribute the Font Software, including the rights to use, copy, merge 
		and publish copies of the Font Software, and to permit persons to whom 
		the Font Software is furnished to do so same, subject to the following 
		terms and conditions (the "License").
		
		   2. The following copyright and trademark notice and these Terms and 
		Conditions shall be included in all copies of one or more of the Font 
		typefaces and any derivative work created as permitted under this 
		License:
		
			Copyright (c) 2001-2005 by the STI Pub Companies, consisting of 
		the American Institute of Physics, the American Chemical Society, the 
		American Mathematical Society, the American Physical Society, Elsevier, 
		Inc., and The Institute of Electrical and Electronic Engineers, Inc. 
		Portions copyright (c) 1998-2003 by MicroPress, Inc. Portions copyright 
		(c) 1990 by Elsevier, Inc. All rights reserved. STIX Fonts-TM is a 
		trademark of The Institute of Electrical and Electronics Engineers, Inc.
		
		   3. You may (a) convert the Fonts from one format to another (e.g., 
		from TrueType to PostScript), in which case the normal and reasonable 
		distortion that occurs during such conversion shall be permitted and (b) 
		embed or include a subset of the Fonts in a document for the purposes of 
		allowing users to read text in the document that utilizes the Fonts. In 
		each case, you may use the STIX Fonts-TM mark to designate the resulting 
		Fonts or subset of the Fonts.
		
		   4. You may also (a) add glyphs or characters to the Fonts, or modify 
		the shape of existing glyphs, so long as the base set of glyphs is not 
		removed and (b) delete glyphs or characters from the Fonts, provided 
		that the resulting font set is distributed with the following 
		disclaimer: "This [name] font does not include all the Unicode points 
		covered in the STIX Fonts-TM set but may include others." In each case, 
		the name used to denote the resulting font set shall not include the 
		term "STIX" or any similar term.
		
		   5. You may charge a fee in connection with the distribution of the 
		Font Software, provided that no copy of one or more of the individual 
		Font typefaces that form the STIX Fonts-TM set may be sold by itself.
		
		   6. THE FONT SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY 
		KIND, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTIES 
		OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT 
		OF COPYRIGHT, PATENT, TRADEMARK OR OTHER RIGHT. IN NO EVENT SHALL 
		MICROPRESS OR ANY OF THE STI PUB COMPANIES BE LIABLE FOR ANY CLAIM, 
		DAMAGES OR OTHER LIABILITY, INCLUDING, BUT NOT LIMITED TO, ANY GENERAL, 
		SPECIAL, INDIRECT, INCIDENTAL OR CONSEQUENTIAL DAMAGES, WHETHER IN AN 
		ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM OR OUT OF THE USE OR 
		INABILITY TO USE THE FONT SOFTWARE OR FROM OTHER DEALINGS IN THE FONT 
		SOFTWARE.
		
		   7. Except as contained in the notice set forth in Section 2, the 
		names MicroPress Inc. and STI Pub Companies, as well as the names of the 
		companies/organizations that compose the STI Pub Companies, shall not be 
		used in advertising or otherwise to promote the sale, use or other 
		dealings in the Font Software without the prior written consent of the 
		respective company or organization.
		
		   8. This License shall become null and void in the event of any 
		material breach of the Terms and Conditions herein by licensee.
		
		   9. A substantial portion of the STIX Fonts set was developed by 
		MicroPress Inc. for the STI Pub Companies. To obtain additional 
		mathematical fonts, please contact MicroPress, Inc., 68-30 Harrow 
		Street, Forest Hills, NY 11375, USA - Phone: (718) 575-1816.
		
		
    * **Multi-license:** BSD-3-Clause
        * Attribution:
        BSD-style license for gist/yorick colormaps.
		
		Copyright:
		
		  Copyright (c) 1996.  The Regents of the University of California.
					 All rights reserved.
		
		Permission to use, copy, modify, and distribute this software for any
		purpose without fee is hereby granted, provided that this entire
		notice is included in all copies of any software which is or includes
		a copy or modification of this software and in all copies of the
		supporting documentation for such software.
		
		This work was produced at the University of California, Lawrence
		Livermore National Laboratory under contract no. W-7405-ENG-48 between
		the U.S. Department of Energy and The Regents of the University of
		California for the operation of UC LLNL.
		
		
					      DISCLAIMER
		
		This software was prepared as an account of work sponsored by an
		agency of the United States Government.  Neither the United States
		Government nor the University of California nor any of their
		employees, makes any warranty, express or implied, or assumes any
		liability or responsibility for the accuracy, completeness, or
		usefulness of any information, apparatus, product, or process
		disclosed, or represents that its use would not infringe
		privately-owned rights.  Reference herein to any specific commercial
		products, process, or service by trade name, trademark, manufacturer,
		or otherwise, does not necessarily constitute or imply its
		endorsement, recommendation, or favoring by the United States
		Government or the University of California.  The views and opinions of
		authors expressed herein do not necessarily state or reflect those of
		the United States Government or the University of California, and
		shall not be used for advertising or product endorsement purposes.
		
		
						AUTHOR
		
		David H. Munro wrote Yorick and Gist.  Berkeley Yacc (byacc) generated
		the Yorick parser.  The routines in Math are from LAPACK and FFTPACK;
		MathC contains C translations by David H. Munro.  The algorithms for
		Yorick's random number generator and several special functions in
		Yorick/include were taken from Numerical Recipes by Press, et. al.,
		although the Yorick implementations are unrelated to those in
		Numerical Recipes.  A small amount of code in Gist was adapted from
		the X11R4 release, copyright M.I.T. -- the complete copyright notice
		may be found in the (unused) file Gist/host.c.
		 *OR* Python-2.0
        * Attribution:
        1\. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and the Individual or Organization ("Licensee") accessing and otherwise using this software ("Python") in source or binary form and its associated documentation.
		   2. Subject to the terms and conditions of this License Agreement, PSF hereby grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce, analyze, test, perform and/or display publicly, prepare derivative works, distribute, and otherwise use Python alone or in any derivative version, provided, however, that PSF's License Agreement and PSF's notice of copyright, i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006 Python Software Foundation; All Rights Reserved" are retained in Python alone or in any derivative version prepared by Licensee.
		   3. In the event Licensee prepares a derivative work that is based on or incorporates Python or any part thereof, and wants to make the derivative work available to others as provided herein, then Licensee hereby agrees to include in any such work a brief summary of the changes made to Python.
		   4. PSF is making Python available to Licensee on an "AS IS" basis. PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
		   5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON, OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
		   6. This License Agreement will automatically terminate upon a material breach of its terms and conditions.
		   7. Nothing in this License Agreement shall be deemed to create any relationship of agency, partnership, or joint venture between PSF and Licensee. This License Agreement does not grant permission to use PSF trademarks or trade name in a trademark sense to endorse or promote products or services of Licensee, or any third party.
		   8. By copying, installing or otherwise using Python, Licensee agrees to be bound by the terms and conditions of this License Agreement.<<beginOptional>> BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
		BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1<<endOptional>>
		   1. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the Individual or Organization ("Licensee") accessing and otherwise using this software in source or binary form and its associated documentation ("the Software").
		   2. Subject to the terms and conditions of this BeOpen Python License Agreement, BeOpen hereby grants Licensee a non-exclusive, royalty-free, world-wide license to reproduce, analyze, test, perform and/or display publicly, prepare derivative works, distribute, and otherwise use the Software alone or in any derivative version, provided, however, that the BeOpen Python License is retained in the Software, alone or in any derivative version prepared by Licensee.
		   3. BeOpen is making the Software available to Licensee on an "AS IS" basis. BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
		   4. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
		   5. This License Agreement will automatically terminate upon a material breach of its terms and conditions.
		   6. This License Agreement shall be governed by and interpreted in all respects by the law of the State of California, excluding conflict of law provisions. Nothing in this License Agreement shall be deemed to create any relationship of agency, partnership, or joint venture between BeOpen and Licensee. This License Agreement does not grant permission to use BeOpen trademarks or trade names in a trademark sense to endorse or promote products or services of Licensee, or any third party. As an exception, the "BeOpen Python" logos available at http://www.pythonlabs.com/logos.html may be used according to the permissions granted on that web page.
		   7. By copying, installing or otherwise using the software, Licensee agrees to be bound by the terms and conditions of this License Agreement.<<beginOptional>> IMPORTANT: PLEASE READ THE FOLLOWING AGREEMENT CAREFULLY.
		BY CLICKING ON "ACCEPT" WHERE INDICATED BELOW, OR BY COPYING, INSTALLING OR OTHERWISE USING PYTHON 1.6, beta 1 SOFTWARE, YOU ARE DEEMED TO HAVE AGREED TO THE TERMS AND CONDITIONS OF THIS LICENSE AGREEMENT.<<endOptional>>
		   1. This LICENSE AGREEMENT is between the Corporation for National Research Initiatives, having an office at 1895 Preston White Drive, Reston, VA 20191 ("CNRI"), and the Individual or Organization ("Licensee") accessing and otherwise using Python 1.6, beta 1 software in source or binary form and its associated documentation, as released at the www.python.org Internet site on August 4, 2000 ("Python 1.6b1").
		   2. Subject to the terms and conditions of this License Agreement, CNRI hereby grants Licensee a non-exclusive, royalty-free, world-wide license to reproduce, analyze, test, perform and/or display publicly, prepare derivative works, distribute, and otherwise use Python 1.6b1 alone or in any derivative version, provided, however, that CNRIs License Agreement is retained in Python 1.6b1, alone or in any derivative version prepared by Licensee.
		   Alternately, in lieu of CNRIs License Agreement, Licensee may substitute the following text (omitting the quotes): "Python 1.6, beta 1, is made available subject to the terms and conditions in CNRIs License Agreement. This Agreement may be located on the Internet using the following unique, persistent identifier (known as a handle): 1895.22/1011. This Agreement may also be obtained from a proxy server on the Internet using the URL:http://hdl.handle.net/1895.22/1011".
		   3. In the event Licensee prepares a derivative work that is based on or incorporates Python 1.6b1 or any part thereof, and wants to make the derivative work available to the public as provided herein, then Licensee hereby agrees to indicate in any such work the nature of the modifications made to Python 1.6b1.
		   4. CNRI is making Python 1.6b1 available to Licensee on an "AS IS" basis. CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6b1 WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
		   5. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF USING, MODIFYING OR DISTRIBUTING PYTHON 1.6b1, OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
		   6. This License Agreement will automatically terminate upon a material breach of its terms and conditions.
		   7. This License Agreement shall be governed by and interpreted in all respects by the law of the State of Virginia, excluding conflict of law provisions. Nothing in this License Agreement shall be deemed to create any relationship of agency, partnership, or joint venture between CNRI and Licensee. This License Agreement does not grant permission to use CNRI trademarks or trade name in a trademark sense to endorse or promote products or services of Licensee, or any third party.
		   8. By clicking on the "ACCEPT" button where indicated, or by copying, installing or otherwise using Python 1.6b1, Licensee agrees to be bound by the terms and conditions of this License Agreement.
		Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam, The Netherlands. All rights reserved.
		Permission to use, copy, modify, and distribute this software and its documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appear in all copies and that both that copyright notice and this permission notice appear in supporting documentation, and that the name of Stichting Mathematisch Centrum or CWI not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.
		STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
    * BSD-3-Clause
        * Attribution:
        BSD-style license for gist/yorick colormaps.
		
		Copyright:
		
		  Copyright (c) 1996.  The Regents of the University of California.
					 All rights reserved.
		
		Permission to use, copy, modify, and distribute this software for any
		purpose without fee is hereby granted, provided that this entire
		notice is included in all copies of any software which is or includes
		a copy or modification of this software and in all copies of the
		supporting documentation for such software.
		
		This work was produced at the University of California, Lawrence
		Livermore National Laboratory under contract no. W-7405-ENG-48 between
		the U.S. Department of Energy and The Regents of the University of
		California for the operation of UC LLNL.
		
		
					      DISCLAIMER
		
		This software was prepared as an account of work sponsored by an
		agency of the United States Government.  Neither the United States
		Government nor the University of California nor any of their
		employees, makes any warranty, express or implied, or assumes any
		liability or responsibility for the accuracy, completeness, or
		usefulness of any information, apparatus, product, or process
		disclosed, or represents that its use would not infringe
		privately-owned rights.  Reference herein to any specific commercial
		products, process, or service by trade name, trademark, manufacturer,
		or otherwise, does not necessarily constitute or imply its
		endorsement, recommendation, or favoring by the United States
		Government or the University of California.  The views and opinions of
		authors expressed herein do not necessarily state or reflect those of
		the United States Government or the University of California, and
		shall not be used for advertising or product endorsement purposes.
		
		
						AUTHOR
		
		David H. Munro wrote Yorick and Gist.  Berkeley Yacc (byacc) generated
		the Yorick parser.  The routines in Math are from LAPACK and FFTPACK;
		MathC contains C translations by David H. Munro.  The algorithms for
		Yorick's random number generator and several special functions in
		Yorick/include were taken from Numerical Recipes by Press, et. al.,
		although the Yorick implementations are unrelated to those in
		Numerical Recipes.  A small amount of code in Gist was adapted from
		the X11R4 release, copyright M.I.T. -- the complete copyright notice
		may be found in the (unused) file Gist/host.c.
		
    * Apache-2.0
        * Attribution:
        Apache-Style Software License for ColorBrewer Color Schemes
		
		Version 1.1
		
		Copyright (c) 2002 Cynthia Brewer, Mark Harrower, and The Pennsylvania 
		State University. All rights reserved. Redistribution and use in source 
		and binary forms, with or without modification, are permitted provided 
		that the following conditions are met:
		
		1\. Redistributions as source code must retain the above copyright notice, 
		this list of conditions and the following disclaimer.
		
		2\. The end-user documentation included with the redistribution, if any, 
		must include the following acknowledgment: "This product includes color 
		specifications and designs developed by Cynthia Brewer 
		(http://colorbrewer.org/)." Alternately, this acknowledgment may appear in 
		the software itself, if and wherever such third-party acknowledgments 
		normally appear.
		
		3\. The name "ColorBrewer" must not be used to endorse or promote products 
		derived from this software without prior written permission. For written 
		permission, please contact Cynthia Brewer at cbrewer@psu.edu.
		
		4\. Products derived from this software may not be called "ColorBrewer", 
		nor may "ColorBrewer" appear in their name, without prior written 
		permission of Cynthia Brewer.
		
		THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES, 
		INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
		AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
		CYNTHIA BREWER, MARK HARROWER, OR THE PENNSYLVANIA STATE UNIVERSITY BE 
		LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
		CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
		SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
		INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
		CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
		ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
		POSSIBILITY OF SUCH DAMAGE.
		



* Discovered License(s)
    * **Multi-license:** MIT *OR* MPL-2.0
    * **Multi-license:** BSD-3-Clause *OR* GPL-3.0-only *OR* LGPL-3.0-only *OR* Python-2.0
    * Python-2.0
    * **Multi-license:** LGPL-3.0-only *OR* Python-2.0
    * MPL-2.0
    * GPL-3.0-only
    * OFL-1.1






---
---

#### **numpy (1.19.4)**


* Declared License(s)



* Discovered License(s)
    * BSD-3-Clause
    * **Multi-license:** BSD-3-Clause *OR* GPL-3.0-only *OR* GPL-3.0-with-GCC-exception






---
---

#### **openpyxl (3.0.5)**


* Declared License(s)
    * MIT
        * Attribution:
        Copyright (c) 2010 openpyxl
		Permission is hereby granted, free of charge, to any person obtaining a copy
		of this software and associated documentation files (the "Software"), to deal
		in the Software without restriction, including without limitation the rights
		to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
		copies of the Software, and to permit persons to whom the Software is
		furnished to do so, subject to the following conditions:
		
		The above copyright notice and this permission notice shall be included in all
		copies or substantial portions of the Software.
		
		THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
		IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
		FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
		AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
		LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
		OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
		SOFTWARE.



* Discovered License(s)






---
---

#### **Pillow (8.0.1)**


* Declared License(s)
    * BSD-3-Clause
        * Attribution:
        The Python Imaging Library (PIL) is
		
		    Copyright © 1997-2011 by Secret Labs AB
		    Copyright © 1995-2011 by Fredrik Lundh
		
		Pillow is the friendly PIL fork. It is
		
		    Copyright © 2010-2020 by Alex Clark and contributors
		
		Like PIL, Pillow is licensed under the open source PIL Software License:
		
		By obtaining, using, and/or copying this software and/or its associated
		documentation, you agree that you have read, understood, and will comply
		with the following terms and conditions:
		
		Permission to use, copy, modify, and distribute this software and its
		associated documentation for any purpose and without fee is hereby granted,
		provided that the above copyright notice appears in all copies, and that
		both that copyright notice and this permission notice appear in supporting
		documentation, and that the name of Secret Labs AB or the author not be
		used in advertising or publicity pertaining to distribution of the software
		without specific, written prior permission.
		
		SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
		SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
		IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,
		INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
		LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
		OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
		PERFORMANCE OF THIS SOFTWARE.
		



* Discovered License(s)
    * public-domain
    * **Multi-license:** GPL-3.0-only *OR* LGPL-3.0-only
    * LGPL-3.0-only
    * OFL-1.1
    * MIT
    * GPL-3.0-or-later
    * Apache-2.0
    * open source PIL Software License






---
---

#### **savReaderWriter (3.4.2)**


* Declared License(s)
    * MIT
        * Attribution:
        Copyright (c) INFORMATION FOR savReaderWriter CONSISTS OF TWO PARTS
		Permission is hereby granted, free of charge, to any person obtaining a copy
		of this software and associated documentation files (the "Software"), to deal
		in the Software without restriction, including without limitation the rights
		to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
		copies of the Software, and to permit persons to whom the Software is
		furnished to do so, subject to the following conditions:
		
		The above copyright notice and this permission notice shall be included in all
		copies or substantial portions of the Software.
		
		THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
		IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
		FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
		AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
		LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
		OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
		SOFTWARE.



* Discovered License(s)
    * public-domain






---
---

#### **yarn (1.22.10)**


* Declared License(s)
    * BSD-2-Clause
        * Attribution:
        BSD 2-Clause License
		
		For Yarn software
		
		Copyright (c) 2016-present, Yarn Contributors. All rights reserved.
		
		Redistribution and use in source and binary forms, with or without modification,
		are permitted provided that the following conditions are met:
		
		 * Redistributions of source code must retain the above copyright notice, this
		   list of conditions and the following disclaimer.
		
		 * Redistributions in binary form must reproduce the above copyright notice,
		   this list of conditions and the following disclaimer in the documentation
		   and/or other materials provided with the distribution.
		
		THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
		ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
		WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
		DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
		ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
		(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
		LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
		ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
		(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
		SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
		



* Discovered License(s)
    * BSD-3-Clause
    * **Multi-license:** Apache-2.0 *OR* MIT






---
---






***Deep dependencies not included.***



***Full license list not included.***




[FOSSA]: # (Do not touch the comments below)

[FOSSA]: # (==depsig=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855==)




***


_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
