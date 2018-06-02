'''
The photon Project 
-------------------
File: tooltips.py

This file contains the tooltip
for the widgets

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

def tt_button_add():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Click here to populate the plot with line/scatter/histogram'
    return tooltip

def legend():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'What will appear in the legend.\nYou can use Latex syntax.'
    return tooltip

def delete_plot():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Will delete the plot'
    return tooltip

def bin():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'The binning of your histogram. Your choices:\n-Xmin, Xmax, dX\n-x1, x2, x3, x4, x5, x6...'
    return tooltip

def slider_tr():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Adjust transparency'
    return tooltip

def slider_lw():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Linewidth'
    return tooltip

def empty():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Will remove the centre of the markers.\nIf the marker is just composed of lines\nthey will disappear'
    return tooltip

def fill():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Will fill the space between your curve a straight line at 0.\nYour curve must have increasing X-values to make this works.'
    return tooltip 

def direction():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Choose between Horizontal, Vertical and Diagonal lines'
    return tooltip 

def direction_span():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Choose between Horizontal or Vertical '
    return tooltip 


def coordinates():
    '''
    Parameters:
    -----------

    Return:
    -------
    tooltip     str
    '''
    tooltip = 'For vertical: X, Ymin, Ymax. For Horizontal Y, Xmin, Xmax.\nFor diagonals Xmin, Xmax'
    return tooltip 


def coordinates_strip():
    '''
    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Two numbers only are necessary. Seprated by a coma.'
    return tooltip 



def hist_norm():
    '''
    Return:
    -------
    tooltip    str
    '''
    tooltip = 'Hit this box if you want the histogram to be normalized.'
    return tooltip

def barplot():
    '''
    Return:
    -------
    tooltip     str
    '''
    tooltip = 'Change line plot with peaks to line plot with bars'
    return tooltip


def gauss():
    '''
    Return
    ------
    tooltip    str
    '''
    tooltip = 'Apply gaussian filter of width selected number'
    return tooltip

def zscale():
    '''
    Return
    ------
    tooltip    str
    '''
    tooltip = 'display with ds9 zscale-like algorithm'
    return tooltip

def contour():
    '''
    Return
    ------
    tooltip    str
    '''
    tooltip = 'contour tooltip'
    return tooltip


def zorder():
    '''
    Return
    ------
    tooltip str
    '''
    tooltip = 'zorder: how data are pilled up. Weak number --> background \n high number --> foreground. Must be an integer'
    return tooltip
