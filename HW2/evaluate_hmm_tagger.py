import os
import codecs
import textwrap
import csv
import numpy as np

#filename = '/Users/semihakbayrak/Dersler/CMPE561/HW2/metu_sabanci_cmpe_561/validation/turkish_metu_sabanci_val.conll'
#pos_type = 'CPOSTAG'

filename = raw_input('Enter the directory of the test data: ')
pos_type = raw_input('Enter the pos type as POSTAG or CPOSTAG: ')

all_tag_file = 'all_tags.csv'

tag_Voc = [] #all tags
for key, val in csv.reader(open(all_tag_file)):
    tag_Voc.append(key)

#control the pos tag type
if pos_type == 'POSTAG':
	pos_num = 4
elif pos_type == 'CPOSTAG':
	pos_num = 3
else:
	print 'Invalid Pos Tag type'

output_file = 'output.txt'
output_file = open(output_file).read()
output_file = output_file.split()

seen_words = 'seen_words.txt'
seen_words = open(seen_words).read()
seen_words = seen_words.split()

#read from conll format
test_file = open(filename).read()
test_file = test_file.split()

confusion = np.zeros((len(tag_Voc),len(tag_Voc)),float)

count = 0
count_known = 0
count_unknown = 0
correct_count = 0
correct_known = 0
correct_unknown = 0
for i in range(len(test_file)/10):
	num = 10*i
	if test_file[num+1] != '_'.encode('utf-8'):
		tag = test_file[num+pos_num]
		found_tag = output_file[2*count+1]
		count = count + 1
		print "Real tag = " + tag
		print "Found tag = " +found_tag
		idxTrue = tag_Voc.index(tag)
		idxFound = tag_Voc.index(found_tag)
		confusion[idxTrue,idxFound] = confusion[idxTrue,idxFound] + 1
		word = test_file[num+1]
		if word in seen_words:
			count_known = count_known + 1
			if tag == found_tag:
				correct_count = correct_count + 1
				correct_known = correct_known + 1
		else:
			count_unknown = count_unknown + 1
			if tag == found_tag:
				correct_count = correct_count + 1
				correct_unknown = correct_unknown + 1

accuracy = 1.0*correct_count/count
print accuracy

known_accuracy = 1.0*correct_known/count_known
print known_accuracy

unknown_accuracy = 1.0*correct_unknown/count_unknown
print unknown_accuracy

for i in range(len(confusion)):
	if sum(confusion[i]) != 0:
		confusion[i] = 100*confusion[i]/sum(confusion[i])

print confusion


