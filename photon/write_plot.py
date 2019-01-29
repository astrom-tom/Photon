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
    plotconfig.set('Types', 'scatter_CB', str(plot.scatterCBindex))
    plotconfig.set('Types', 'error', str(plot.errorindex))
    plotconfig.set('Types', 'text', str(plot.text_index))
    plotconfig.set('Types', 'segments', str(plot.straight_index))
    plotconfig.set('Types', 'Image', str(plot.imageindex))
    plotconfig.set('Types', 'diag', str(plot.imageindex))
    plotconfig.set('Types', 'hist', str(plot.histindex))
    plotconfig.set('Types', 'strip', str(plot.strip_index))
    plotconfig.set('Types', 'band', str(plot.band_index))
    plotconfig.set('Types', 'xmin', str(plot.plot.get_xlim()[0]))
    plotconfig.set('Types', 'xmax', str(plot.plot.get_xlim()[1]))
    plotconfig.set('Types', 'ymin', str(plot.plot.get_ylim()[0]))
    plotconfig.set('Types', 'ymax', str(plot.plot.get_ylim()[1]))
    plotconfig.set('Types', 'x_label', str(plot.plot.get_xlabel()))
    plotconfig.set('Types', 'y_label', str(plot.plot.get_ylabel()))


    config = save_line(plot, plotconfig) 
    config = save_scatter(plot, config)
    config = save_scatterCB(plot, config)
    config = save_text(plot, config)
    config = save_straight(plot, config)
    config = save_span(plot, config)
    config = save_hist(plot, config)
    config = save_error(plot, config)
    config = save_image(plot, config)
    config = save_band(plot, config)
    
    with open(filesave, 'w') as myconfig:
        config.write(myconfig)


def save_line(plot, plotconfig):

    typeplot = 'line'
    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLabel)
    for j in name:
        if j.objectName()[:4] == 'line' and j.objectName()[-9:] == 'labelfile':
            ident = int(j.objectName()[5:6])
            idents.append(ident)

    plotconfig.set('Types', 'line', str(len(idents)))
    k = 0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'line_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())


        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'line_%s_label'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'label', label)
            if j.objectName() == 'line_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)

        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'line_%s_X'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'X', X)
            if j.objectName() == 'line_%s_Y'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Y', Y)
            if j.objectName() == 'line_%s_color'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Color', color)
            if j.objectName() == 'line_%s_style'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Style', color)
            if j.objectName() == 'line_%s_color_fb'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Color_fb', color)

        ###retrieve combo boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName()[5:] == '%s_fb'%(i):
                fb = j.isChecked() 
                if fb == False:
                    fb = 'No'
                if fb == True:
                    fb = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'fb', fb)
            if j.objectName()[5:] == '%s_bp'%(i):
                bp = j.isChecked() 
                if bp == False:
                    bp = 'No'
                if bp == True:
                    bp = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'bp', bp)
         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'line_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'thickness', str(sli))

        ###retrieve spinbox
        spin = plot.plotarea.parentWidget().findChildren(QSpinBox)
        for j in spin:
            if j.objectName() == 'line_%s_sb'%str(i):
                sm = spin[0].value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'smooth', str(sm))

        k+=1
    return plotconfig

def save_scatterCB(plot, plotconfig):

    typeplot = 'sccb'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLabel)
    for j in name:
        if j.objectName()[:4] == 'sccb' and j.objectName()[-9:] == 'labelfile':
            ident = int(j.objectName()[5:6])
            idents.append(ident)


    plotconfig.set('Types', 'scatter_CB', str(len(idents)))
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'sccb_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())
        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'sccb_%s_label'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'label', label)

            if j.objectName() == 'sccb_%s_labelcb'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'labelcb', label)

            if j.objectName() == 'sccb_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)

            if j.objectName() == 'sccb_%s_vmin'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'vmin', zorder)

            if j.objectName() == 'sccb_%s_vmax'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'vmax', zorder)

        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'sccb_%s_X'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'X', X)
            if j.objectName() == 'sccb_%s_Y'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Y', Y)
            if j.objectName() == 'sccb_%s_Z'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Z', Y) 
            if j.objectName() == 'sccb_%s_mapcolor'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Colormap', color)
            if j.objectName() == 'sccb_%s_cbfontaxis'%(i):
                marker = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'fontlabel', marker)
            if j.objectName() == 'sccb_%s_cbfontaxisticks'%(i):
                marker = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'fonttickslabel', marker)
            if j.objectName() == 'sccb_%s_marker'%(i):
                marker = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'marker', marker)



        ###retrieve check boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName() == 'sccb_%s_empty'%(i):
                fb = j.isChecked() 
                if fb == False:
                    fb = 'No'
                if fb == True:
                    fb = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'empty', fb)
         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'sccb_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'thickness', str(sli))
            if j.objectName() == 'sccb_%s_tr'%str(i):
                tr = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'transparency', str(tr))

        ###retrieve spinbox
        spin = plot.plotarea.parentWidget().findChildren(QSpinBox)
        for j in spin:
            if j.objectName() == 'sccb_%s_size'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'size', str(sm))
            if j.objectName() == 'sccb_%s_labelpad'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'labelpad', str(sm))
            if j.objectName() == 'sccb_%s_lst'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'tickLabelsize', str(sm))
            if j.objectName() == 'sccb_%s_labsize'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Labelsize', str(sm))




        k+=1
    return plotconfig


def save_scatter(plot, plotconfig):

    typeplot = 'scat'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLabel)
    for j in name:
        if j.objectName()[:4] == 'scat' and j.objectName()[-9:] == 'labelfile':
            ident = int(j.objectName()[5:6])
            idents.append(ident)


    plotconfig.set('Types', 'scatter', str(len(idents)))
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'scat_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())
        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'scat_%s_label'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'label', label)
            if j.objectName() == 'scat_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'scat_%s_X'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'X', X)
            if j.objectName() == 'scat_%s_Y'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Y', Y)
            if j.objectName() == 'scat_%s_color'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Color', color)
            if j.objectName() == 'scat_%s_marker'%(i):
                marker = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'marker', marker)

        ###retrieve combo boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName() == 'scat_%s_empty'%(i):
                fb = j.isChecked() 
                if fb == False:
                    fb = 'No'
                if fb == True:
                    fb = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'empty', fb)
         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'scat_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'thickness', str(sli))
            if j.objectName() == 'scat_%s_tr'%str(i):
                tr = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'transparency', str(tr))

        ###retrieve spinbox
        spin = plot.plotarea.parentWidget().findChildren(QSpinBox)
        for j in spin:
            if j.objectName() == 'scat_%s_size'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'size', str(sm))

        k+=1
    return plotconfig

def save_text(plot, plotconfig):

    typeplot = 'text'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLineEdit)
    for j in name:
        if j.objectName()[:4] == 'text' and j.objectName()[-4:] == 'text':
            ident = int(j.objectName()[5:-5])
            idents.append(ident)

    
    plotconfig.set('Types', 'text', str(len(idents)))


    ##and create sections for each of the plot
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))


        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'text_%s_text'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'text', label)
            
            if j.objectName() == 'text_%s_coor'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'coor', label)

            if j.objectName() == 'text_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ##combo box
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'text_%s_color'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'color', X)
         
        ###retrieve spinbox
        spin = plot.plotarea.parentWidget().findChildren(QSpinBox)
        for j in spin:
            if j.objectName() == 'text_%s_angle'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'angle', str(sm))

        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'text_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'size', str(sli))

        k+=1
        
    return plotconfig


def save_straight(plot, plotconfig):

    typeplot = 'stra'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLineEdit)
    for j in name:
        if j.objectName()[:4] == 'stra' and j.objectName()[-4:] == 'coor':
            ident = int(j.objectName()[5:6])
            idents.append(ident)

    plotconfig.set('Types', 'segments', str(len(idents)))

    k = 0 
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))
        
        ##combo box
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'stra_%s_color'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'color', X)
            if j.objectName() == 'stra_%s_dir'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'dir', X)
            if j.objectName() == 'stra_%s_ls'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'style', X)
         
        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'stra_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'stra_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'thickness', str(sli))

        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'stra_%s_coor'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'coor', label)

        k+=1


    return plotconfig


def save_span(plot, plotconfig):

    typeplot = 'stri'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLineEdit)
    for j in name:
        if j.objectName()[:4] == 'stri' and j.objectName()[-4:] == 'coor':
            ident = int(j.objectName()[5:6])
            idents.append(ident)

    plotconfig.set('Types', 'strip', str(len(idents)))
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))
        
        ##combo box
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'stri_%s_color'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'color', X)
            if j.objectName() == 'stri_%s_dir'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'dir', X)

        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'stri_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)

        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'stri_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'transparency', str(sli))

        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'stri_%s_coor'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'coor', label)

        k+=1


    return plotconfig

def save_hist(plot, plotconfig):

    typeplot = 'hist'
    i = 0

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLineEdit)
    for j in name:
        if j.objectName()[:4] == 'hist' and j.objectName()[-3:] == 'bin':
            ident = int(j.objectName()[5:-4])
            idents.append(ident)


    plotconfig.set('Types', 'hist', str(len(idents)))

    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))
        
        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'hist_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())

        ##combo box
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'hist_%s_ls'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'linestyle', X)
            if j.objectName() == 'hist_%s_hs'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'histstyle', X)
            if j.objectName() == 'hist_%s_X'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'X', X)
            if j.objectName() == 'hist_%s_color'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'color', X)
         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'hist_%s_slider'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'transparency', str(sli))
            if j.objectName() == 'hist_%s_sliderlw'%str(i):
                sli = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'thickness', str(sli))

        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'hist_%s_label'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'label', label)
            if j.objectName() == 'hist_%s_bin'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'bin', label)
            if j.objectName() == 'hist_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ###retrieve combo boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName() == 'hist_%s_norm'%(i):
                norm = j.isChecked() 
                if norm == False:
                    norm = 'No'
                if norm == True:
                    norm = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'norm', norm)
         

        k+=1


    return plotconfig

def save_error(plot, plotconfig):

    typeplot = 'erro'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLabel)
    for j in name:
        if j.objectName()[:4] == 'erro' and j.objectName()[-4:] == '_col':
            ident = int(j.objectName()[5:-4])
            idents.append(ident)


    plotconfig.set('Types', 'error', str(len(idents)))
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'erro_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())


        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'erro_%s_label'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'label', label)
            if j.objectName() == 'erro_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'erro_%s_X'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'X', X)
            if j.objectName() == 'erro_%s_xerrp'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Xerrp', X)
            if j.objectName() == 'erro_%s_xerrm'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Xerrm', X)

            if j.objectName() == 'erro_%s_Y'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Y', Y)
            if j.objectName() == 'erro_%s_yerrp'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Yerrp', Y)
            if j.objectName() == 'erro_%s_yerrm'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Yerrm', Y) 

            if j.objectName() == 'erro_%s_color'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Color', color)
            if j.objectName() == 'erro_%s_marker'%(i):
                marker = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'marker', marker)

        ###retrieve combo boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName() == 'erro_%s_empty'%(i):
                fb = j.isChecked() 
                if fb == False:
                    fb = 'No'
                if fb == True:
                    fb = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'empty', fb)

         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'erro_%s_tr'%str(i):
                tr = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'transparency', str(tr))

        ###retrieve spinbox
        spin = plot.plotarea.parentWidget().findChildren(QSpinBox)
        for j in spin:
            if j.objectName() == 'erro_%s_size'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'size', str(sm))
            if j.objectName() == 'erro_%s_barsize'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'barsize', str(sm))
            if j.objectName() == 'erro_%s_capsize'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'capsize', str(sm))

        k+=1
    return plotconfig

def save_image(plot, plotconfig):

    typeplot = 'imag'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLabel)
    for j in name:
        if j.objectName()[:4] == 'imag' and j.objectName()[-4:] == '_col':
            ident = int(j.objectName()[5:-4])
            idents.append(ident)

    plotconfig.set('Types', 'Image', str(len(idents)))
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'imag_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())


        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'imag_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'imag_%s_mapcolor'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Colormap', color)
            if j.objectName() == 'imag_%s_color'%(i):
                marker = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'contour_color', marker)

        ###retrieve check boxes
        checks = plot.plotarea.parentWidget().findChildren(QCheckBox)
        for j in checks:
            if j.objectName() == 'imag_%s_zscale'%(i):
                zs = j.isChecked() 
                if zs == False:
                    zsv = 'No'
                if zs == True:
                    zsv = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'zscale', zsv)

            if j.objectName() == 'imag_%s_contour'%(i):
                contour = j.isChecked() 
                if contour == False:
                    zsv = 'No'
                if contour == True:
                    zsv = 'Yes'
                plotconfig.set('%s_%s'%(typeplot, k+1), 'contour', zsv)


         
        ###retrieve slider 
        slide = plot.plotarea.parentWidget().findChildren(QSlider)
        for j in slide:
            if j.objectName() == 'imag_%s_slider'%str(i):
                tr = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'contour_lw', str(tr))

        ###retrieve spinbox
        spin = plot.plotarea.parentWidget().findChildren(QSpinBox)
        for j in spin:
            if j.objectName() == 'imag_%s_size'%str(i):
                sm = j.value()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'contour_size', str(sm))
 
        k+=1
    return plotconfig

def save_band(plot, plotconfig):

    typeplot = 'band'

    #####check the index that are left
    idents = []
    name = plot.plotarea.parentWidget().findChildren(QLabel)
    for j in name:
        if j.objectName()[:4] == 'band' and j.objectName()[-9:] == 'labelfile':
            ident = int(j.objectName()[5:6])
            idents.append(ident)


    plotconfig.set('Types', 'band', str(len(idents)))
    k=0
    for i in idents:
        ##create the section in the configuration
        plotconfig.add_section('%s_%s'%(typeplot, k+1))

        ##filename
        name = plot.plotarea.parentWidget().findChildren(QLabel)
        for j in name:
            if j.objectName() == 'band_%s_labelfile'%(i):
                plotconfig.set('%s_%s'%(typeplot, k+1), 'file', j.text())
        ###retrieve the label of the plot
        Edits = plot.plotarea.parentWidget().findChildren(QLineEdit)
        for j in Edits:
            if j.objectName() == 'band_%s_label'%str(i):
               label = j.text()  
               plotconfig.set('%s_%s'%(typeplot, k+1), 'label', label)
            if j.objectName() == 'band_%s_zorder'%str(i):
               zorder = j.text()
               plotconfig.set('%s_%s'%(typeplot,k+1), 'zorder', zorder)


        ###retrieve combo boxes
        combo = plot.plotarea.parentWidget().findChildren(QComboBox)
        for j in combo:
            if j.objectName() == 'band_%s_X'%(i):
                X = j.currentText() 
                plotconfig.set('%s_%s'%(typeplot, k+1), 'X', X)
            if j.objectName() == 'band_%s_Y1'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Y1', Y)
            if j.objectName() == 'band_%s_Y2'%(i):
                Y = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Y2', Y) 
            if j.objectName() == 'band_%s_bcolor'%(i):
                color = j.currentText()
                plotconfig.set('%s_%s'%(typeplot, k+1), 'Color', color)
            #if j.objectName() == 'band_%s_hatchband'%(i):
            #    marker = j.currentText()
            #    plotconfig.set('%s_%s'%(typeplot, k+1), 'hatch', marker)

        k+=1
    return plotconfig


