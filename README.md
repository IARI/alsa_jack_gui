# alsa_jack_gui
a qt-based gui to manage *alsa_in* and *alsa_out* daemons

## Features

* read available in- and output devices (with aplay, arecord)
* start alsa_in (rsp. alsa_out) daemons with proper names for any detected device.
* stop running daemons on clean program exit
* remember for which devices daemons were started

Note: no jack routing is ever performed or saved by this program 

## Requirements

### Linux

* Python 3
* Pip for python 3
* Python modules : PyQT 5, pexpect
* jackd2 (including alsa-jack bridge)
* alsa utilities (*aplay*, *arecord*)


## Installation

No builds available, you gotta build it yourself for now..

### Linux (Ubuntu)

* Install python modules : 

        sudo apt-get install python3 python3-pip python3-pyqt5
        sudo pip3 install pexpect

* Install alsa utils and alsa-jack bridge: 

        sudo apt-get install alsa-utils

* check out this repository

        cd /your/install/path
        git clone https://github.com/IARI/alsa_jack_gui.git

* run 

        cd /your/install/path
        make 
  
  in the directory where you checked out the repo

## Running

### Linux

run the lightshow script from lightshow directory :

	python3 alsa_jack.py
	
## Contact

Feel free to send an email to julian.jarecki@gmail.com if you have any questions, remarks or if you find a bug.
