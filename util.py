# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:24:14 2018

@author: Administrator
"""

import re

NOTE_NORMAL=('C','D','E','F','G','A','B')
NOTE_NORMAL_INDEX=(0,2,4,5,7,9,11)
ALTER=('b','#','x')
ALTER_NUM=(-1,1,2)
NOTE_NORMALIZED=('C','#C','D','bE','E','F','#F','G','bA','A','bB','B')

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
	