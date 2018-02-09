# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:22:08 2018

@author: Administrator
"""

#import util
import numpy as np
import sounddevice as sd

ALPHA=2**(1/12)

class Synth:
	def __init__(self,harmonics=[1],sample_rate=44100,tuning=440):
		harm=np.array(harmonics)
		norm=np.sqrt(np.sum(harm*harm))
		harm=harm/(norm*2)
		self.harmonics=harm
		self.sample_rate=sample_rate
		self.tuning=tuning
		pass
	
	def freq(self,note):
		return self.tuning*ALPHA**(note.note_num-57)
	
	def generate(self,time,freq_base):
		t=np.arange(0,time,1/self.sample_rate)
		s=np.zeros(t.shape)
		for i in range(len(self.harmonics)):
			if 2*(i+1)*freq_base<=self.sample_rate:
				s+=(self.harmonics[i]*np.sin(2*np.pi*(i+1)*freq_base*t+np.random.randn()))
		return s
	
	def play(self,note,time):
		s=self.generate(time,self.freq(note))
		sd.play(s,self.sample_rate,blocking=True)
	