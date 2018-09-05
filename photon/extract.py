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


def header(inputfile):
    '''
    This function looks inside the
    catalog and extract the header.
    If the number of column is different
    from the number of header index
    columns are renamed colX, colY...
    (see function fake header)
    Parameters:
    -----------
    inputfile   str, path/and/name to the catalog

    Return:
    -------
    Headers     list of string, one string for each column
    '''

    ####extract number of column
    A = numpy.genfromtxt(inputfile, dtype='str').T
    if len(A.shape) == 1:
        Nc = 1
    else:
        Nc = len(A)

    with open(inputfile, 'r') as F:
        ##we look at the first line
        firstLine = F.readline()
        ##if it starts by a # it comes with a header
        if firstLine[0] == '#':
            ###[1:-1]--> this remove '#' and the '\n' at the end
            firstLine = firstLine[1:]
            ###count the number of element in the first line
            Nh = len(firstLine.split())
            firstLine.split()    
            if Nh == Nc:
                #if yes we take the splitted header
                header = firstLine.split()
            else:
                #if no we create a fake header
                header = fake_header(Nc)

        else:
            #if no we create a fake header
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
    if len(columns) == 1:
        return numpy.genfromtxt(cat, dtype='str')
    else:
        cat = numpy.genfromtxt(cat, dtype='str').T
        return cat[index_in_cat]


