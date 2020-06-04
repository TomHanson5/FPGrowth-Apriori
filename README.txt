Thomas Hanson
CSC 240: Project 1 - Frequent Itemset Mining
Apriori and FPGrow algorithms 

The two files are Apriori.py and fp_grow.py
Both are python files and require no non-standard libraries.

Both files, at the bottom, have a __main__='__main__' block which has a args variable.
This variable is the arguments for the algorithms as a list of length 2 with the first item in the list being the name of the data file. For example: "Data.csv" is what I used for testing and is the UCI Census dataset given with the non-age continous coloumns removed. Included are coloumns 0, 1, 3, 4, 5, 6, 7, 8, 9, 13, 14 from the initial dataset, and this file is included in this zip file.

The second argument is a minimum support, for example: .6 or .1

The Apriori.py file has several functions with commented out lines for runtime testing. These all look like 'start = time.time()', 'end = time.tim()', and 'print('something: ', (end - start))'. uncommenting all three of those lines will print the runtime for that function.
This includes the main function, which therefore includes the entire program in its runtime. 

The fp_grow.py file will also track and report the support count of each frequent itemset. However there is only runtime printing for the algorithm overall.