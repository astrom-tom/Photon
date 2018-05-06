'''

The photon Project 
-------------------
File: extract.py

This file contains the code
who extract data from the catalog

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import numpy


def header(inputfile, args):
    '''
    This function looks inside the
    catalog and extract the header.
    If the number of column is different
    from the number of header index
    columns are renamed colX, colY...
    (see function fake header)
    Parameters:
    -----------
    args        obj, containing argument of the cli

    Return:
    -------
    Headers     list of string, one string for each column
    '''
    ####extract number of column
    A = numpy.genfromtxt(inputfile, dtype='str').T
    Nc = len(A)
    if args.header == True:
        ####read the first line of the raw file
        with open(inputfile, 'r') as F:
            ###[1:-1]--> this remove '#' and the '\n' at the end
            firstLine = F.readline()[1:-1]
     
        ###count the number of element in the first line
        Nh = len(firstLine.split())
        firstLine.split()    
        
        ##check if they are equal:
        if Nh == Nc:
            #if yes we take the splitted header
            header = firstLine.split()
        else:
            print('Number of entries in the header dif from number of columns: Nc = %s and Nh = %s'%(Nc, Nh))
            #if not, we create a fake header
            header = fake_header(Nc)

    else:
        header = fake_header(Nc)
           
    return header


def fake_header(Nc):
    '''
    This function creates a fake header
    From the number of columns, the header
    will contain colX, colY...
    Parameters:
    -----------
    Nc      int, number of column in the file

    Return
    ------
    fake_header list, of string with fake header
    '''

    fake_header = []
    for i in range(Nc):
        fake_header.append('col%s'%str(i+1))
         
    return fake_header


def column(name_col, columns, cat):
    '''
    This function extract the column corresponding to the name
    given in argument
    Parameters:
    -----------
    name_col    str, name of the column to plt
    column      list of str, with columns name
    cat         str, catalog to open
    Return:
    -------

    '''
    ###we find the index of the column in the catalog
    index_in_cat = numpy.where(name_col == numpy.array(columns) )[0][0]

    ##we load the catalog
    cat = numpy.genfromtxt(cat, dtype='str').T

    return cat[index_in_cat]


