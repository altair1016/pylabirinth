#!/usr/bin/env python
# -*- coding: Utf-8 -*
'''
@author: Marco Iannella, Mattia Primavera
@copyright: Copyrights for code authored by Marco Iannella, Mattia Primavera
@version: 1.0.0
'''
import tkinter
import sys
import os
import time
from threading import *
from labyrinthe import *
if __name__ == "__main__":
	lab = Labyrinthe()
	lab.modalitePartie()

	
	
	
	if lab.gagne == 1:
		print(lab.mouvements)