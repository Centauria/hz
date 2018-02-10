# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:09:56 2018

@author: Administrator
"""

import click
import synthesizer as syn

@click.command()
@click.option('-n','--note',default='A4',\
	help="""The note you want to play.
	Default: A4
	""")
@click.option('-t','--time',default=1.,\
	help="""The sustain time of the note in seconds.
	Default: 1
	""")
@click.option('-h','--harmonics',\
	help="""The harmonics that the wave have.
	Default: 1,1,1
	""")
@click.option('-T','--tuning',default=440.,\
	help="""The frequency of note A4 in Hz.
	Default: 440
	""")
@click.option('-S','--sample-rate',default=44100,\
	help="""The sample rate of the audio playback.
	Default: 44100
	""")
def hz(note,time,harmonics,tuning,sample_rate):
	n=syn.Note(note)
	if harmonics:
		harm=list(map(float,harmonics.split(',')))
	else:
		harm=syn.HARMONIC_PIANO
	# synth=synthesizer.Synth(np.sinc(np.arange(0,10*np.pi,np.pi/5)),sample_rate,tuning)
	synth=syn.Synth(harmonics=harm,sample_rate=sample_rate,tuning=tuning)
	print(n)
	synth.play(n,time)

if __name__=='__main__':
	hz()