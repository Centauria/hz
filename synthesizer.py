# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:22:08 2018

@author: Administrator
"""

import numpy as np
import sounddevice as sd
import re

NOTE_NORMAL=('C','D','E','F','G','A','B')
NOTE_NORMAL_INDEX=(0,2,4,5,7,9,11)
ALTER=('b','#','x')
ALTER_NUM=(-1,1,2)
NOTE_NORMALIZED=('C','#C','D','bE','E','F','#F','G','bA','A','bB','B')

ALPHA=2**(1/12)

class Note:
	def __init__(self,note_string):
		self.__note_num=Note.get_note_num(note_string)
		pass
	
	def __repr__(self):
		return Note.get_note_string(self.__note_num)
	
	@staticmethod
	def get_note_num(note_string):
		if re.match('.*[0-9]+$',note_string):
			octave=int(re.search('[0-9]+$',note_string).group())
		else:
			raise Exception('Expecting octave at the end')
		name=None
		alt=[]
		for v in note_string:
			if v in NOTE_NORMAL:
				if name:
					raise Exception('Multiple note found')
				else:
					name=v
			if v in ALTER:
				alt.append(v)
		if name:
			res=NOTE_NORMAL_INDEX[NOTE_NORMAL.index(name)]+12*octave
			for a in alt:
				res+=ALTER_NUM[ALTER.index(a)]
			return res
		else:
			raise Exception('No note found')
	
	@staticmethod
	def get_note_string(note_num,style='default'):
		"""style={'default','flat','sharp'}"""
		octave=note_num//12
		num=note_num%12
		if style=='default':
			return NOTE_NORMALIZED[num]+str(octave)
		elif style=='flat':
			if num in NOTE_NORMAL_INDEX:
				return NOTE_NORMAL[NOTE_NORMAL_INDEX.index(num)]+str(octave)
			else:
				return ALTER[0]+NOTE_NORMAL[NOTE_NORMAL_INDEX.index(num+1)]+str(octave)
		elif style=='sharp':
			if num in NOTE_NORMAL_INDEX:
				return NOTE_NORMAL[NOTE_NORMAL_INDEX.index(num)]+str(octave)
			else:
				return ALTER[1]+NOTE_NORMAL[NOTE_NORMAL_INDEX.index(num-1)]+str(octave)
	
	@property
	def note_num(self):
		return self.__note_num

class ADSR:
	"""Record the ADSR feature of a timbre.
	Consists of 5 parts:
	attack_time,attack_level,decay_time,sustain_level,release_time
	time is in seconds,
	while level is relative.
	"""
	def __init__(self,attack_time=0,attack_level=1,decay_time=0,\
	sustain_level=1,release_time=0):
		max_level=np.maximum(attack_level,sustain_level)
		self.__attack_time=attack_time
		self.__attack_level=attack_level/max_level
		self.__decay_time=decay_time
		self.__suatain_level=sustain_level/max_level
		self.__release_time=release_time
		pass
	
	@property
	def attack_time(self):
		return self.__attack_time
	
	@property
	def attack_level(self):
		return self.__attack_level
	
	@property
	def decay_time(self):
		return self.__decay_time
	
	@property
	def sustain_level(self):
		return self.__suatain_level
	
	@property
	def release_time(self):
		return self.__release_time
	
	def envelope(self,t,T):
		attack_velocity=self.attack_level/self.attack_time
		decay_velocity=(self.attack_level-self.sustain_level)/self.decay_time
		result=0
		if T<0:
			raise Exception("T can't be lower than 0")
		if T<self.attack_time:
			release_level=attack_velocity*T
		elif T<self.attack_time+self.decay_time:
			release_level=self.attack_level-decay_velocity*(T-self.attack_time)
		else:
			release_level=self.sustain_level
		if t>T+self.release_time:
			result=0
		elif t>T:
			result=release_level*(T+self.release_time-t)/self.release_time
		elif t>self.attack_time+self.decay_time:
			result=self.sustain_level
		elif t>self.attack_time:
			result=self.attack_level-decay_velocity*(t-self.attack_time)
		elif t>0:
			result=attack_velocity*t
		else:
			result=0
		return result
	

ADSR_PIANO=ADSR(0.02,1,20,0,0.5)

HARMONIC_PIANO=[1.,0.56234133,0.22387211,0.28183829,0.12589254,\
	0.08912509,0.03162278,0.01,0.,0.05623413,0.01412538]

class Synth:
	def __init__(self,harmonics=HARMONIC_PIANO,adsr=ADSR_PIANO,sample_rate=44100,tuning=440):
		harm=np.array(harmonics)
		norm=np.sqrt(np.sum(harm*harm))
		harm=harm/(norm*2)
		self.harmonics=harm
		self.adsr=adsr
		self.sample_rate=sample_rate
		self.tuning=tuning
		pass
	
	def freq(self,note):
		return self.tuning*ALPHA**(note.note_num-57)
	
	def generate(self,time,freq_base):
		t=np.arange(0,time+self.adsr.release_time,1/self.sample_rate)
		s=np.zeros(t.shape)
		for i in range(len(self.harmonics)):
			if 2*(i+1)*freq_base<=self.sample_rate:
				s+=(self.harmonics[i]*np.sin(2*np.pi*(i+1)*freq_base*t+np.random.randn()))
		for i in range(len(t)):
			s[i]*=self.adsr.envelope(t[i],time)
		return s
	
	def play(self,note,time):
		s=self.generate(time,self.freq(note))
		sd.play(s,self.sample_rate,blocking=True)
#		sd.play(s,self.sample_rate)
	