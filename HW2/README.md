This repository contains 3 python scripts, all written in python 2.7. 

If you run the train_hmm_tagger.py, it will ask you enter the directory of the training file first. As an example:

/Users/semihakbayrak/Dersler/CMPE561/HW2/metu_sabanci_cmpe_561/train/turkish_metu_sabanci_train.conll

Then it will ask you to enter tag type as POSTAG or CPOSTAG. It will creates some csv files to use later in test scripts.

When you run hmm_tagger.py, it will ask you to enter the directory of the test file. Then it will ask you the tag type again.

evaluate_hmm_tagger.py requests same raw inputs from you, directory of test file and tag type.

Important note: My trainer creates files with the same name for POSTAG and CPOSTAG. So if you trained the system for POSTAG, you are expected to test for POSTAG again. Then if you would like to evaluate the performance of my code for CPOSTAG, you should run train_hmm_tagger.py first for CPOSTAG.
