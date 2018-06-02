'''
The photon Project 
-------------------
File: write_plot.py

This file writes down the configuration of each plot

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import configparser
import os
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QVBoxLayout, \
        QTabWidget, QTabWidget, QLineEdit, QLineEdit, QInputDialog, QCheckBox, \
        QHBoxLayout, QScrollArea, QComboBox, QPushButton, QLabel, QSlider, QFileDialog,\
        QSpinBox, QFrame



def save(filesave, plot):
    '''
    Function that writes down the current plotting display
    Parameters:
    ----------
    fileconf        str, path/to/file/to/be/saved
    config          obj, config to be saved
    '''
    ''
    
    if os.path.isfile(filesave):
        os.remove(filesave)


    ####read the default file that we will modify
    plotconfig = configparser.ConfigParser()
    plotconfig.read(filesave)

    ###this section is mandatory in all plot file
    plotconfig.add_section('Types')
    plotconfig.set('Types', 'line', str(plot.lineindex))
    plotconfig.set('Types', 'scatter', str(plot.scatterindex))
    plotconfig.set('Types', 'error', str(plot.errorindex))
    plotconfig.set('Types', 'text', str(plot.text_index))
    plotconfig.set('Types', 'segments', str(plot.straight_index))
    plotconfig.set('Types', 'Image', str(plot.imageindex))
    plotconfig.set('Types', 'diag', str(plot.imageindex))
    plotconfig.set('Types', 'hist', str(plot.histindex))
    plotconfig.set('Types', 'strip', str(plot.strip_index))

    config = save_line(plot, plotconfig) 
    
    with open(filesave, 'w') as myconfig:
            plotconfig.write(myconfig)


def save_line(plot, plotconfig):

    typeplot = 'line'
    i = 0
    while i < plot.lineindex:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, i+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName()[5:] == '%s_labelfile'%(i+1):
                plotconfig.set('%s_%s'%(typeplot, i+1), 'file', j.text())


        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName()[:6] == '%s_%s'%(typeplot, i+1):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, i+1), 'label', label)


        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName()[5:] == '%s_X'%(i+1):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, i+1), 'X', X)
            if j.objectName()[5:] == '%s_Y'%(i+1):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, i+1), 'Y', Y)
            if j.objectName()[5:] == '%s_color'%(i+1):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, i+1), 'Color', color)
            if j.objectName()[5:] == '%s_style'%(i+1):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, i+1), 'Style', color)
            if j.objectName()[5:] == '%s_color_fb'%(i+1):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, i+1), 'Color_fb', color)

        ###retrieve combo boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName()[7:] == '%s_fb'%(i+1):
                fb = j.isChecked() 
                if fb == False:
                    fb = 'No'
                if fb == True:
                    fb = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, i+1), 'fb', fb)
            if j.objectName()[7:] == '%s_bp'%(i+1):
                bp = j.isChecked() 
                if bp == False:
                    bp = 'No'
                if bp == True:
                    bp = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, i+1), 'bp', bp)
         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        sli = slide[0].value()
        plotconfig.set('%s_%s'%(typeplot, i+1), 'thickness', str(sli))
        i+=1

    return plotconfig

