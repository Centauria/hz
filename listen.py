# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 15:04:09 2018

@author: Administrator
"""

import cmd
import sys
import numpy as np
import synthesizer as syn


class Client(cmd.Cmd):
	"""help
	"""
	
	prompt='-->'
	intro="""Listen!
	"""
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.synth=syn.Synth()
	
	def do_play(self,arg):
		notes=arg.split(' ')
		for i in range(len(notes)):
			notes[i]=syn.Note(notes[i])
		print('play: ',[n for n in notes])
		for n in notes:
			self.synth.play(n,2)
		pass
	
	def do_print(self,arg):
		notes=arg.split(' ')
		print(notes)
	
	def do_test(self,arg):
		if arg=='':
			num=10
		else:
			num=int(arg)
		if num<=0:
			raise Exception('Invalid argument')
		correct=0
		for i in range(num):
			note_num=np.random.randint(36,96)
			note=syn.Note(syn.Note.get_note_string(note_num))
			self.synth.play(note,2)
			answer=input('Please answer the note_string: ')
			note_num_answer=syn.Note.get_note_num(answer)
			if note_num==note_num_answer:
				correct+=1
				print('Right!')
			else:
				print('Wrong!')
			print('Right answer is: ',note)
		print('Total: ',num,'Correct: ',correct)
	pass

if __name__=='__main__':
	
	try:
		client=Client()
		client.cmdloop()
	except KeyboardInterrupt:
		sys.exit()