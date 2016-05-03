#-*- coding: utf-8 -*- 

#PartOfSpeech Tagging with HMM test part

#from __future__ import unicode_literals

import os
import codecs
import textwrap
import csv
import numpy as np

#filename = '/Users/semihakbayrak/Dersler/CMPE561/HW2/metu_sabanci_cmpe_561/validation/turkish_metu_sabanci_val.conll'
#pos_type = 'CPOSTAG'

filename = raw_input('Enter the directory of the test data: ')
pos_type = raw_input('Enter the pos type as POSTAG or CPOSTAG: ')

#control the pos tag type
if pos_type == 'POSTAG':
	pos_num = 4
elif pos_type == 'CPOSTAG':
	pos_num = 3
else:
	print 'Invalid Pos Tag type'

first_tag_file = 'first_tag.csv'
word_tag_file = 'word_tag.csv'
tag_tag_file = 'tag_tag.csv'
all_tag_file = 'all_tags.csv'


first_tag_Voc = {} #tag of first word of sentence probabilities
word_tag_Voc = {} #word-tag pair probabilities
tag_tag_Voc = {} #tag-tag pair probabilities
tag_Voc = [] #all tags
seen_words = []

for key, val in csv.reader(open(first_tag_file)):
    first_tag_Voc[key] = val
for key, val in csv.reader(open(word_tag_file)):
    word_tag_Voc[key] = val
for key, val in csv.reader(open(tag_tag_file)):
    tag_tag_Voc[key] = val
for key, val in csv.reader(open(all_tag_file)):
    tag_Voc.append(key)

#function to label some unknown words
def unknownWordTag(x):
	if x[-len('ıp'):] == 'ıp':
		return 'Adv'
	if x[-len('ip'):] == 'ip':
		return 'Adv'
	if x[-len('up'):] == 'up':
		return 'Adv'
	if x[-len('üp'):] == 'üp':
		return 'Adv'
	if x[-len('arak'):] == 'arak':
		return 'Adv'
	if x[-len('erek'):] == 'erek':
		return 'Adv'
	if x[-len('ınca'):] == 'ınca':
		return 'Adv'
	if x[-len('ince'):] == 'ince':
		return 'Adv'
	if x[-len('unca'):] == 'unca':
		return 'Adv'
	if x[-len('ünce'):] == 'ünce':
		return 'Adv'
	if x[-len('madan'):] == 'madan':
		return 'Adv'
	if x[-len('meden'):] == 'meden':
		return 'Adv'
	if x[-len('maksızın'):] == 'maksızın':
		return 'Adv'
	if x[-len('meksizin'):] == 'meksizin':
		return 'Adv'
	if x[-len('dıkça'):] == 'dıkça':
		return 'Adv'
	if x[-len('dikçe'):] == 'dikçe':
		return 'Adv'
	if x[-len('dukça'):] == 'dukça':
		return 'Adv'
	if x[-len('dükçe'):] == 'dükçe':
		return 'Adv'
	if x[-len('tıkça'):] == 'tıkça':
		return 'Adv'
	if x[-len('tikçe'):] == 'tikçe':
		return 'Adv'
	if x[-len('tukça'):] == 'tukça':
		return 'Adv'
	if x[-len('tükçe'):] == 'tükçe':
		return 'Adv'
	if x[-len('alı'):] == 'alı':
		return 'Adv'
	if x[-len('eli'):] == 'eli':
		return 'Adv'
	if x[-len('ken'):] == 'ken':
		return 'Adv'
	if x[-len('dığında'):] == 'dığında':
		return 'Adv'
	if x[-len('diğinde'):] == 'diğinde':
		return 'Adv'
	if x[-len('duğunda'):] == 'duğunda':
		return 'Adv'
	if x[-len('düğünde'):] == 'düğünde':
		return 'Adv'
	if x[-len('tığında'):] == 'tığında':
		return 'Adv'
	if x[-len('tiğinde'):] == 'tiğinde':
		return 'Adv'
	if x[-len('tuğunda'):] == 'tuğunda':
		return 'Adv'
	if x[-len('tüğünde'):] == 'tüğünde':
		return 'Adv'
	if x[-len('cı'):] == 'cı':
		return 'Adj'
	if x[-len('ci'):] == 'ci':
		return 'Adj'
	if x[-len('cu'):] == 'cu':
		return 'Adj'
	if x[-len('cü'):] == 'cü':
		return 'Adj'
	if x[-len('cıl'):] == 'cıl':
		return 'Adj'
	if x[-len('cil'):] == 'cil':
		return 'Adj'
	if x[-len('cul'):] == 'cul':
		return 'Adj'
	if x[-len('cül'):] == 'cül':
		return 'Adj'
	if x[-len('çıl'):] == 'çıl':
		return 'Adj'
	if x[-len('çil'):] == 'çil':
		return 'Adj'
	if x[-len('çul'):] == 'çul':
		return 'Adj'
	if x[-len('çül'):] == 'çül':
		return 'Adj'
	if x[-len('ıncı'):] == 'ıncı':
		return 'Adj'
	if x[-len('inci'):] == 'inci':
		return 'Adj'
	if x[-len('uncu'):] == 'uncu':
		return 'Adj'
	if x[-len('üncü'):] == 'üncü':
		return 'Adj'
	if x[-len('li'):] == 'li':
		return 'Adj'
	if x[-len('lı'):] == 'lı':
		return 'Adj'
	if x[-len('lu'):] == 'lu':
		return 'Adj'
	if x[-len('lü'):] == 'lü':
		return 'Adj'
	if x[-len('lik'):] == 'lik':
		return 'Adj'
	if x[-len('lık'):] == 'lık':
		return 'Adj'
	if x[-len('luk'):] == 'luk':
		return 'Adj'
	if x[-len('lük'):] == 'lük':
		return 'Adj'
	if x[-len('deki'):] == 'deki':
		return 'Adj'
	if x[-len('sız'):] == 'sız':
		return 'Adj'
	if x[-len('siz'):] == 'siz':
		return 'Adj'
	if x[-len('suz'):] == 'suz':
		return 'Adj'
	if x[-len('süz'):] == 'süz':
		return 'Adj'
	if x[-len('an'):] == 'an':
		return 'Adj'
	if x[-len('en'):] == 'en':
		return 'Adj'
	if x[-len('ası'):] == 'ası':
		return 'Adj'
	if x[-len('esi'):] == 'esi':
		return 'Adj'
	if x[-len('mez'):] == 'mez':
		return 'Verb'
	if x[-len('maz'):] == 'maz':
		return 'Verb'
	if x[-len('mezler'):] == 'mezler':
		return 'Verb'
	if x[-len('mazlar'):] == 'mazlar':
		return 'Verb'
	if x[-len('ar'):] == 'ar':
		return 'Verb'
	if x[-len('er'):] == 'er':
		return 'Verb'
	if x[-len('ır'):] == 'ır':
		return 'Verb'
	if x[-len('ir'):] == 'ir':
		return 'Verb'
	if x[-len('ur'):] == 'ur':
		return 'Verb'
	if x[-len('ür'):] == 'ür':
		return 'Verb'
	if x[-len('arlar'):] == 'arlar':
		return 'Verb'
	if x[-len('erler'):] == 'erler':
		return 'Verb'
	if x[-len('ırlar'):] == 'ırlar':
		return 'Verb'
	if x[-len('irler'):] == 'irler':
		return 'Verb'
	if x[-len('urlar'):] == 'urlar':
		return 'Verb'
	if x[-len('ürler'):] == 'ürler':
		return 'Verb'
	if 'di' in x:
		return 'Verb'
	if 'dı' in x:
		return 'Verb'
	if 'ti' in x:
		return 'Verb'
	if 'tı' in x:
		return 'Verb'
	if 'ecek' in x:
		return 'Verb'
	if 'acak' in x:
		return 'Verb'
	if 'miş' in x:
		return 'Verb'
	if 'mış' in x:
		return 'Verb'
	if 'muş' in x:
		return 'Verb'
	if 'müş' in x:
		return 'Verb'



#read from conll format
test_file = open(filename).read()
test_file = test_file.split()

#every line has 10 columns
count = 1
all_sentence_tags = []
for i in range(len(test_file)/10):
	num = 10*i
	#to detect sentence begining
	if test_file[num] == str(1):
		count = count - 1
		viterbiProbs = np.empty((0,len(tag_Voc)),float) #to keep probabilities
		viterbiStates = np.empty((0,len(tag_Voc)),str) #to keep states
		sentence_tags = []
	if test_file[num+1] != '_'.encode('utf-8'):
		word = test_file[num+1]
		is_word_seen = 0
		if count == 0:
			count = 1 #this means valid word is seen
			probs = np.zeros((len(tag_Voc)))
			for j in range(len(tag_Voc)):
				if tag_Voc[j] in first_tag_Voc:
					probs[j] = np.log(float(first_tag_Voc[tag_Voc[j]])) #first tag probabilities
				else:
					probs[j] = -500
				if str((word,tag_Voc[j])) in word_tag_Voc:
					probs[j] = probs[j] + np.log(float(word_tag_Voc[str((word,tag_Voc[j]))])) #tag to word probabilities
					is_word_seen = 1
				else:
					probs[j] = probs[j] - 500
			if is_word_seen == 0:
				tag_by_hand = unknownWordTag(word)
				if tag_by_hand != None:
					idx = tag_Voc.index(tag_by_hand)
					probs[idx] = probs[idx] + 500
			else:
				seen_words.append(word)
		else:
			states = []
			#evaluation of all tags for new state
			for j in range(len(tag_Voc)):
				possible_probs = np.zeros((len(tag_Voc)))
				#evaluation of all the transitions from old tags to current tag
				for k in range(len(tag_Voc)):
					if str((tag_Voc[k],tag_Voc[j])) in tag_tag_Voc:
						possible_probs[k] = probs[k] + np.log(float(tag_tag_Voc[str((tag_Voc[k],tag_Voc[j]))])) #tag to tag transitions
					else:
						possible_probs[k] = probs[k] - 500
					if str((word,tag_Voc[j])) in word_tag_Voc:
						possible_probs[k] = possible_probs[k] + np.log(float(word_tag_Voc[str((word,tag_Voc[j]))])) #tag to word
						is_word_seen = 1
					else:
						possible_probs[k] = possible_probs[k] - 500
				probs[j] = np.max(possible_probs)
				states.append(tag_Voc[np.argmax(possible_probs)])
			if is_word_seen == 0:
				tag_by_hand = unknownWordTag(word)
				if tag_by_hand != None:
					idx = tag_Voc.index(tag_by_hand)
					probs[idx] = probs[idx] + 500
			else:
				seen_words.append(word)
			viterbiStates = np.append(viterbiStates,[states],axis=0) 
		viterbiProbs = np.append(viterbiProbs,[probs],axis=0)
	#check if sentence ends, and make backtracking
	if i == (len(test_file)/10 - 1):
		ar = np.argmax(probs)
		sentence_tags.append(tag_Voc[ar])
		for j in range(len(viterbiStates)):
			k = len(viterbiStates)-j-1
			sentence_tags.append(viterbiStates[k][ar])
		sentence_tags.reverse()
		all_sentence_tags = all_sentence_tags + sentence_tags
	else:
		if test_file[num+10] == str(1):
			ar = np.argmax(probs)
			sentence_tags.append(tag_Voc[ar])
			for j in range(len(viterbiStates)):
				k = len(viterbiStates)-j-1
				sentence_tags.append(viterbiStates[k][ar])
			sentence_tags.reverse()
			all_sentence_tags = all_sentence_tags + sentence_tags


#save the found tags to txt file
with open('output.txt',"w") as writer:
	c = 0
	for i in range(len(test_file)/10):
		num = 10*i
		if test_file[num+1] != '_'.encode('utf-8'):
			writer.write(test_file[num+1]+" "+all_sentence_tags[c])
			c = c + 1
		writer.write("\n")

#save the seen words to txt file
with open('seen_words.txt',"w") as writer:
	for word in seen_words:
		writer.write(word+" ")

			

