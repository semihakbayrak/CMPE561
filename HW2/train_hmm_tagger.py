#-*- coding: utf-8 -*- 

#PartOfSpeech Tagging with HMM training part

import os
import codecs
import textwrap
import csv

#filename = '/Users/semihakbayrak/Dersler/CMPE561/HW2/metu_sabanci_cmpe_561/train/turkish_metu_sabanci_train.conll'
#pos_type = 'CPOSTAG'

filename = raw_input('Enter the directory of the training data: ')
pos_type = raw_input('Enter the pos type as POSTAG or CPOSTAG: ')

#control the pos tag type
if pos_type == 'POSTAG':
	pos_num = 4
elif pos_type == 'CPOSTAG':
	pos_num = 3
else:
	print 'Invalid Pos Tag type'

#start to count for training
number_of_sentences = 0
tag_Voc = {} #to keep tag frequencies
first_tag_Voc = {} #to keep tag occurances in the first word of sentence, will be converted from counts to probabilities
word_tag_Voc = {} #to keep word-tag pair occurances, will be converted from counts to probabilities
tag_tag_Voc = {} #to keep tag-tag pair occurances, will be converted from counts to probabilities

#read from conll format
train_file = open(filename).read()
train_file = train_file.split()

#every line has 10 columns
count = 1
for i in range(len(train_file)/10):
	num = 10*i
	#to detect sentnece begining
	if train_file[num] == str(1):
		count = count - 1
	if train_file[num+1] != '_'.encode('utf-8'):
		tag = train_file[num+pos_num]
		if count == 0:
			count = 1
			oldtag = tag
			number_of_sentences = number_of_sentences + 1 #increase number of sentences
			# tag occurances in the begining of the sentences
			if tag in first_tag_Voc:
				first_tag_Voc[tag] = first_tag_Voc[tag] + 1
			else:			
				first_tag_Voc[tag] = 1
		else:
			#tag transitions
			if (oldtag,tag) in tag_tag_Voc:
				tag_tag_Voc[(oldtag,tag)] = tag_tag_Voc[(oldtag,tag)] + 1
			else:
				tag_tag_Voc[(oldtag,tag)] = 1
			oldtag = tag
		#counting all tags
		if tag in tag_Voc:
			tag_Voc[tag] = tag_Voc[tag] + 1
		else:
			tag_Voc[tag] = 1
		#counting for word likelihoods
		word = train_file[num+1]
		if (word,tag) in word_tag_Voc:
			word_tag_Voc[(word,tag)] = word_tag_Voc[(word,tag)] + 1
		else:
			word_tag_Voc[(word,tag)] = 1

#normalizations to transform counts to probabilities
for key in first_tag_Voc:
	first_tag_Voc[key] = 1.0*first_tag_Voc[key]/number_of_sentences

for key in tag_tag_Voc:
	tag_tag_Voc[key] = 1.0*tag_tag_Voc[key]/tag_Voc[key[0]]

for key in word_tag_Voc:
	word_tag_Voc[key] = 1.0*word_tag_Voc[key]/tag_Voc[key[1]]

#writing to csv file to use in test progress
w = csv.writer(open("first_tag.csv", "w"))
for key, val in first_tag_Voc.items():
    w.writerow([key, val])

w = csv.writer(open("tag_tag.csv", "w"))
for key, val in tag_tag_Voc.items():
    w.writerow([key, val])

w = csv.writer(open("word_tag.csv", "w"))
for key, val in word_tag_Voc.items():
    w.writerow([key, val])

w = csv.writer(open("all_tags.csv", "w"))
for key, val in tag_Voc.items():
    w.writerow([key, val])


