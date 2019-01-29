'''

The photon Project 
-------------------
File: parameters_matplotlib.py

This code creates the widget of the 
parameters of matplotlib to be tunes

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt

'''

#### Python Libraries
from functools import partial
import numpy

####qt5
from PyQt5 import *
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *

###matplotlib
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib import container
import matplotlib.font_manager
import warnings
warnings.simplefilter(action='ignore', category=matplotlib.mplDeprecation)

##local imports
################matplotlib colors
allcolors = numpy.array([i for i in matplotlib.colors.cnames])


#####################for section header
myFont_sec=QtGui.QFont()
myFont_sec.setBold(True)
myFont_sec.setPointSize(10)
#####################for individual widget
myFont=QtGui.QFont()
myFont.setPointSize(9)
######################

###################################################
######### Axis limits #############################
###################################################
def axis_lim(grid, win, plot, figure, loadplot, conf):
    '''
    this function creates the QLineEdit
    for X and Y axis limits
    '''

    xmin = QLineEdit(loadplot.plotconf['types']['xmin'])
    xmin.setObjectName('xmin')
    grid.addWidget(xmin, 1, 0, 1, 1)
    xmin.setFont(myFont)  
    xmax = QLineEdit(loadplot.plotconf['types']['xmax'])
    xmax.setObjectName('xmax')
    grid.addWidget(xmax, 1, 1, 1, 1)
    xmax.setFont(myFont)  

    ymin = QLineEdit(loadplot.plotconf['types']['ymin'])
    ymin.setObjectName('ymin')
    grid.addWidget(ymin, 2, 0, 1, 1)
    ymin.setFont(myFont)  
    ymax = QLineEdit(loadplot.plotconf['types']['ymax'])
    ymax.setObjectName('ymax')
    grid.addWidget(ymax, 2, 1, 1, 1)
    ymax.setFont(myFont)  

    LogX = QCheckBox('Log x-axis')
    grid.addWidget(LogX, 3, 0, 1, 1)
    LogX.setFont(myFont)  
    LogY = QCheckBox('Log y-axis')
    grid.addWidget(LogY, 3, 1, 1, 1)
    LogY.setFont(myFont)  

    axis_lim_event(grid, win, plot, figure, xmin, xmax, ymin, ymax, LogX, LogY, conf)
 
    xmin.textChanged.connect(partial(axis_lim_event, grid, win, plot, figure, xmin, \
            xmax, ymin, ymax, LogX, LogY, conf))
    xmax.textChanged.connect(partial(axis_lim_event, grid, win, plot, figure, xmin, \
            xmax, ymin, ymax, LogX, LogY, conf))
    ymin.textChanged.connect(partial(axis_lim_event, grid, win, plot, figure, xmin, \
            xmax, ymin, ymax, LogX, LogY, conf))
    ymax.textChanged.connect(partial(axis_lim_event, grid, win, plot, figure, xmin, \
            xmax, ymin, ymax, LogX, LogY, conf))
    LogY.stateChanged.connect(partial(axis_lim_event, grid, win, plot, figure, xmin, \
            xmax, ymin, ymax, LogX, LogY, conf)) 
    LogX.stateChanged.connect(partial(axis_lim_event, grid, win, plot, figure, xmin, \
            xmax, ymin, ymax, LogX, LogY, conf))
    axis_lim_event(grid, win, plot, figure, xmin, xmax, ymin, ymax, LogX, LogY, conf)

def axis_lim_event(grid, win, plot, figure, wid1, wid2, wid3, wid4, logx, logy, conf):
    '''
    This function changes the axis limits of the plot.
    Parameters:
    -----------
    win         FigureCanvas, obj
    plot        subplot, obj
    figure      Figure, obj
    wid         QComboBox widget
    '''

    ##get the current limit
    x1, x2 = plot.get_xlim()
    y1, y2 = plot.get_ylim()

    ##get texts
    try:
        xmin = float(wid1.text())
    except:
        xmin = x1

    try: 
        xmax = float(wid2.text())
    except:
        xmax = x2

    try:
        ymin = float(wid3.text())
    except:
        ymin = y1

    try:
        ymax = float(wid4.text())
    except:
        ymax = y2

    plot.axis([xmin, xmax, ymin, ymax])
        
    if logx.isChecked():
        plot.set_xscale('log')
    else:
        plot.set_xscale('linear')
    
    if logy.isChecked():
        plot.set_yscale('log')
    else:
        plot.set_yscale('linear')

    #update ticks
    ticks(grid, win, plot, figure, conf.ticks)
    figure.tight_layout()


    ###and update the figure
    win.draw()
    
 

###################################################
#####  first property is background colors   ######
###################################################
def background(grid, win, plot, figure, conf):
    '''
    This function creates the combobox for
    background color selection
    Parameters:
    -----------
    grid        QgridLayout object
    win         FigureCanvas object
    plot        subplot object
    figure      Figure object
    conf        color from configuration file
    Return:
    -------
    none
    '''
    ####label
    BG = QLabel('Back Color:')
    grid.addWidget(BG, 4, 0, 1, 1)
    BG.setFont(myFont_sec)
    
    ###combobox
    facecolor_combo = QComboBox()
    grid.addWidget(facecolor_combo, 4, 1, 1, 1)
    ##that we fill with color list
    for i in allcolors:
        facecolor_combo.addItem(i)
    ###we set default value to white
    from_conf = numpy.where(allcolors == conf.BACK)[0][0]
    facecolor_combo.setCurrentIndex(from_conf)

    background_event(win, plot, figure, facecolor_combo, conf)

    ###and link an event when the color is selected in the combo box
    facecolor_combo.currentIndexChanged.connect(partial(background_event, 
        win, plot, figure, facecolor_combo, conf))

def background_event(win, plot, figure, wid, conf):
    '''
    This function is the background color change.
    Parameters:
    -----------
    win         FigureCanvas, obj
    plot        subplot, obj
    figure      Figure, obj
    wid         QComboBox widget
    '''
    ##get current text displayed in combobox
    color = wid.currentText()

    ###set color inside the plot
    plot.set_facecolor(color)

    ###set color outside the plot
    figure.set_facecolor(color)

    matplotlib.rcParams['savefig.facecolor'] = color
    figure.tight_layout()
    ###and update the figure
    conf.BACK = color
    win.draw()
    
    
#####################################################
########## Then we tune the axis of the plot ########
#####################################################

def axis(grid, win, plot, figure, conf):
    '''
    This function creates the widget
    for axis properties color selection
    Parameters:
    -----------
    grid        QgridLayout object
    win         FigureCanvas object
    plot        subplot object
    figure      Figure object
    Return:
    -------
    none
    '''

    ###name of the section
    ax = QLabel('--AXIS--')  ###label
    grid.addWidget(ax, 5, 0, 1, 1)
    ax.setFont(myFont_sec)

    ####axiscolor
    ax = QLabel('Color:')  ###label
    grid.addWidget(ax, 6, 0, 1, 1)
    ax.setFont(myFont)
    edgecolor_combo = QComboBox()  ##creation combobox
    grid.addWidget(edgecolor_combo, 6, 1, 1, 2)
    for i in allcolors:  ###fill it
        edgecolor_combo.addItem(i)
    from_conf = numpy.where(allcolors == conf['Color'])[0][0]
    edgecolor_combo.setCurrentIndex(from_conf) ##set default

    ####axis width
    axw = QLabel('linewidth:')  ###label
    grid.addWidget(axw, 7, 0, 1, 1)
    axw.setFont(myFont)
    axwidth = QSpinBox()  ##spinbox linewidth
    grid.addWidget(axwidth, 7, 1, 1, 1)
    axwidth.setMinimum(0)
    axwidth.setMaximum(100)
    from_conf_lw = conf['lw']
    axwidth.setValue(from_conf_lw) ###set default

    ####axis label width
    laxw = QLabel('Label size:')  ###label
    grid.addWidget(laxw, 8, 0, 1, 1)
    laxw.setFont(myFont)
    laxwidth = QSpinBox()  ##spinbox linewidth
    grid.addWidget(laxwidth, 8, 1, 1, 1)
    laxwidth.setMinimum(0)
    laxwidth.setMaximum(100)
    from_conf_ls = conf['Labelsize']
    laxwidth.setValue(from_conf_ls) ###set default


    ####labelaxiscolor
    lc = QLabel('Label color:')  ###label
    grid.addWidget(lc, 9, 0, 1, 1)
    lc.setFont(myFont)
    lc_combo = QComboBox()  ##creation combobox
    grid.addWidget(lc_combo, 9, 1, 1, 2)
    for i in allcolors:  ###fill it
        lc_combo.addItem(i)
    from_conf = numpy.where(allcolors == conf['Label_color'])[0][0]
    lc_combo.setCurrentIndex(from_conf) ##set default



    axis_event(win, plot, figure, edgecolor_combo, axwidth, laxwidth, lc_combo, conf) 

    ###and lick an event to each widget
    edgecolor_combo.currentIndexChanged.connect(partial(axis_event, 
        win, plot, figure, edgecolor_combo, axwidth, laxwidth, lc_combo, conf))
    axwidth.valueChanged.connect(partial(axis_event, 
        win, plot, figure, edgecolor_combo, axwidth, laxwidth, lc_combo, conf))
    laxwidth.valueChanged.connect(partial(axis_event, 
        win, plot, figure, edgecolor_combo, axwidth, laxwidth, lc_combo, conf))
    lc_combo.currentIndexChanged.connect(partial(axis_event, 
        win, plot, figure, edgecolor_combo, axwidth, laxwidth, lc_combo, conf))

def axis_event(win, plot, figure, coloraxis, axlw, laxlw, labelcolor, conf):
    '''
    This function change the axis of the plot.
    Parameters:
    -----------
    win         FigureCanvas, obj
    plot        subplot, obj
    figure      Figure, obj
    coloraxis   QComboBox widget
    axlw        QspinBox    ''  
    laxw        QspinBox    ''
    labelcolor  QComboBox   ''
    '''
    ##get current text displayed in combobox
    color = coloraxis.currentText()

    ##get current value for axis linewidth
    lw = axlw.value()

    ##get current value for axis linewidth
    llw = laxlw.value()
    
    ##get current text displayed in combobox
    lcolor = labelcolor.currentText()

    ###update configuration object
    conf['Color'] = color
    conf['Label_color'] = lcolor
    conf['lw'] = lw
    conf['Labelsize'] = llw

    ##labelsize
    plot.xaxis.label.set_size(llw)
    plot.yaxis.label.set_size(llw)

    ###labelcolor
    plot.xaxis.label.set_color(lcolor)
    plot.yaxis.label.set_color(lcolor)
    
    ###set color of axis and linewidth
    for spine in plot.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(lw)

    figure.tight_layout()
    ###and update the figure
    win.draw()
    

#####################################################
########## Then we tune the ticks of the plot ########
#####################################################

def ticks(grid, win, plot, figure, conf):
    '''
    This function creates the widget
    for axis properties color selection
    Parameters:
    -----------
    grid        QgridLayout object
    win         FigureCanvas object
    plot        subplot object
    figure      Figure object
    conf        config from user
    Return:
    -------
    none
    '''

    ###name of the section
    ax = QLabel('--TICKS--')  ###label
    grid.addWidget(ax, 10, 0, 1, 2)
    ax.setFont(myFont_sec)
    
    ###minorticks
    minors = QCheckBox('Minor On/Off')

    if conf['Minor'].lower() == 'on':
        minors.setChecked(True)
    elif conf['Minor'].lower() == 'off':
        minors.setChecked(False)

    grid.addWidget(minors, 11, 0, 1, 1)
    minors.setFont(myFont)

    ###minorticks
    inout = QCheckBox('Ticks In/Out')
    if conf['placement'].lower() == 'in':
        inout.setChecked(True)
    elif conf['placement'].lower() == 'out':
        inout.setChecked(False)
    grid.addWidget(inout, 11, 1, 1, 1)
    inout.setFont(myFont)

    ####tick size label width
    tms = QLabel('Major size:')  ###label
    grid.addWidget(tms, 12, 0, 1, 1)
    tms.setFont(myFont)
    tmsize = QSpinBox()  ##spinbox linewidth
    grid.addWidget(tmsize, 12, 1, 1, 1)
    tmsize.setMinimum(0)
    tmsize.setMaximum(100)
    from_conf_tm = conf['Major_size']
    tmsize.setValue(from_conf_tm) ###set default

    ####tick size label width
    tmis = QLabel('Minor size:')  ###label
    grid.addWidget(tmis, 13, 0, 1, 1)
    tmis.setFont(myFont)
    tmisize = QSpinBox()  ##spinbox linewidth
    grid.addWidget(tmisize, 13, 1, 1, 1)
    tmisize.setMinimum(0)
    tmisize.setMaximum(100)
    from_conf_tmi= conf['Minor_size']
    tmisize.setValue(from_conf_tmi) ###set default

    ####tick width label width
    tmw = QLabel('Major width:')  ###label
    grid.addWidget(tmw, 14, 0, 1, 1)
    tmw.setFont(myFont)
    tmwidth = QSpinBox()  ##spinbox linewidth
    grid.addWidget(tmwidth, 14, 1, 1, 1)
    tmwidth.setMinimum(0)
    tmwidth.setMaximum(100)
    from_conf_tmw = conf['Major_width']
    tmwidth.setValue(from_conf_tmw) ###set default


    ####tick width label width
    tmiw = QLabel('Minor width:')  ###label
    grid.addWidget(tmiw, 15, 0, 1, 1)
    tmiw.setFont(myFont)
    tmiwidth = QSpinBox()  ##spinbox linewidth
    grid.addWidget(tmiwidth, 15, 1, 1, 1)
    tmiwidth.setMinimum(0)
    tmiwidth.setMaximum(100)
    from_conf_tmwi = conf['Minor_width']
    tmiwidth.setValue(from_conf_tmwi) ###set default
    
    ####axiscolor
    tc = QLabel('Ticks Color:')  ###label
    grid.addWidget(tc, 16, 0, 1, 1)
    tc.setFont(myFont)
    tc_combo = QComboBox()  ##creation combobox
    grid.addWidget(tc_combo, 16, 1, 1, 2)
    for i in allcolors:  ###fill it
        tc_combo.addItem(i)
    from_conf = numpy.where(allcolors == conf['Ticks_color'])[0][0]
    tc_combo.setCurrentIndex(from_conf) ##set default

    ####axiscolor
    ltc = QLabel('Label Color:')  ###label
    grid.addWidget(ltc, 17, 0, 1, 1)
    ltc.setFont(myFont)
    ltc_combo = QComboBox()  ##creation combobox
    grid.addWidget(ltc_combo, 17, 1, 1, 2)
    for i in allcolors:  ###fill it
        ltc_combo.addItem(i)
    from_conf = numpy.where(allcolors == conf['Label_color'])[0][0]
    ltc_combo.setCurrentIndex(from_conf) ##set default

    ####tick width label width
    ls = QLabel('Label Size:')  ###label
    grid.addWidget(ls, 18, 0, 1, 1)
    ls.setFont(myFont)
    ls_box = QSpinBox()  ##spinbox linewidth
    grid.addWidget(ls_box, 18, 1, 1, 2)
    ls_box.setMinimum(0)
    ls_box.setMaximum(100)
    from_conf_ls = conf['Label_size']
    ls_box.setValue(from_conf_ls) ###set default

    ###load the default values
    ticks_event(win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf)

    ##link the event to the function
    minors.stateChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    inout.stateChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    ls_box.valueChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    ltc_combo.currentIndexChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    tc_combo.currentIndexChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    tmisize.valueChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    tmsize.valueChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    tmwidth.valueChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))

    tmiwidth.valueChanged.connect(partial(ticks_event, 
        win, plot, figure, minors, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf))



def ticks_event(win, plot, figure, minor, inout, tmsize, tmisize, tmwidth, \
                tmiwidth, tc_combo, ltc_combo, ls_box, conf):
    '''
    This function change the ticks parameters of the plot.
    Parameters:
    -----------
    win         FigureCanvas, obj
    plot        subplot, obj
    figure      Figure, obj
    minor       QCheckBox   widget
    inout       ''          ''
    tmsize
    tmisize
    tmwidth,
    tmiwidth
    tc_combo
    ltc_combo
    ls_box
    '''
    ###add minorticks
    if minor.isChecked():
        plot.minorticks_on()
        plot.tick_params(axis='both', which='both', top='on', bottom='on', \
                    left = 'on', right ='on')
    else:
        plot.minorticks_off()
        plot.tick_params(axis='both', which='major', top='off', right ='off')


    ###ticks in out
    if inout.isChecked():
        plot.tick_params(which='both',axis='both', direction='in')
    else:
        plot.tick_params(which='both',axis='both', direction='out')

    ###label size
    ls = ls_box.value()
    plot.tick_params(axis='both', which='major', labelsize=ls)
    plot.tick_params(axis='both', which='minor', labelsize=ls)

    ###colors
    tc = tc_combo.currentText()
    ltc = ltc_combo.currentText()
    plot.tick_params(which='both' ,color=tc, labelcolor=ltc)

    ###tick sizes and widths
    tmsi = tmsize.value()
    tmisi = tmisize.value()
    tmw = tmwidth.value()
    tmiw = tmiwidth.value()

    if minor.isChecked():
        conf['Minor'] = 'on'
    else:
        conf['Minor'] = 'off'

    if inout.isChecked():
        conf['placement'] = 'in'
    else:
        conf['placement'] = 'out'


    conf['Major_size'] = tmsi 
    conf['Major_width'] = tmw
    conf['Minor_size'] = tmisi
    conf['Minor_width'] = tmiw
    conf['Ticks_color'] = tc
    conf['Label_color'] = ltc
    conf['Label_size'] = ls

    plot.tick_params(axis='both', which='major', width=tmw, size=tmsi )
    plot.tick_params(axis='both', which='minor', width=tmiw, size=tmisi )

    figure.tight_layout()
    win.draw()
    
##############################################
######## Fonts ###############################
##############################################
def fonts(grid, win, plot, figure, conf):
    '''
    This function creates the widget
    for font properties

    Parameters:
    -----------
    grid        QgridLayout object
    win         FigureCanvas object
    plot        subplot object
    figure      Figure object
    Return:
    -------
    none
    '''

    ####load font names
    flist = matplotlib.font_manager.get_fontconfig_fonts()
    names = []
    for fname in flist:
        try:	
            a = matplotlib.font_manager.FontProperties(fname=fname).get_name()
            names.append(a)
        except:
            pass
    ###name of the section
    names = numpy.array(names)
    names = numpy.delete(names,numpy.where(names == 'Goha-Tibeb Zemen' ) )

    ax = QLabel('--FONTS--')  ###label
    grid.addWidget(ax, 19, 0, 1, 1)
    ax.setFont(myFont_sec)

    ####font axis
    flab = QLabel('Font axis label:')  ###label
    grid.addWidget(flab, 20, 0, 1, 1)
    flab.setFont(myFont)
    fontlab_combo = QComboBox()  ##creation combobox
    grid.addWidget(fontlab_combo, 20, 1, 1, 2)
    for i in names:  ###fill it
        fontlab_combo.addItem(i)

    fonts = numpy.where(names == conf.axis['Axis_label_font'])
    if len(fonts[0]) == 0:
        from_conf = 0
    else:
        from_conf = fonts[0][0]
    fontlab_combo.setCurrentIndex(from_conf) ##set default

    ####font ticks
    fticks = QLabel('Font ticks label:')  ###label
    grid.addWidget(fticks, 21, 0, 1, 1)
    fticks.setFont(myFont)
    fticks_combo = QComboBox()  ##creation combobox
    grid.addWidget(fticks_combo, 21, 1, 1, 1)
    for i in names:  ###fill it
        fticks_combo.addItem(i)

    fonts = numpy.where(names == conf.ticks['Ticks_label_font'])
    if len(fonts[0]) == 0:
        from_conf = 0
    else:
        from_conf = fonts[0][0]
    fticks_combo.setCurrentIndex(from_conf) ##set default

    ###load default parameters
    fonts_event(win, plot, figure, fontlab_combo, fticks_combo, conf)
    ###load the default values

    fontlab_combo.currentIndexChanged.connect(partial(fonts_event, win, \
                plot, figure, fontlab_combo, fticks_combo, conf))

    fticks_combo.currentIndexChanged.connect(partial(fonts_event, win, \
                plot, figure, fontlab_combo, fticks_combo, conf))



def fonts_event(win, plot, figure, fontlab_box, fticks_box, conf):
    '''
    This function change the font of the plot.
    Parameters:
    -----------
    win         FigureCanvas, obj
    plot        subplot, obj
    figure      Figure, obj
    fontlab_box QComboBox widget
    fticks_box      ''      ''
    flegend_box     ''      ''
    '''
    ####retrieve information
    flabel = fontlab_box.currentText()
    fticks = fticks_box.currentText()

    ###update conf
    conf.axis['Axis_label_font'] = flabel
    conf.ticks['Ticks_label_font'] = fticks

    ####fontname for axus label
    labx = plot.xaxis.get_label()
    laby = plot.yaxis.get_label()
    labx.set_fontname(flabel)
    laby.set_fontname(flabel)

    ####tick label font
    if fticks not in ['Goha-Tibeb Zemen']:
        labels = plot.get_xticklabels()
        for i in labels:
            i.set_fontproperties(fticks)
        
        labels = plot.get_yticklabels()
        for i in labels:
            i.set_fontproperties(fticks)
        
    figure.tight_layout()
    win.draw()


##############################################
######## Legend ##############################
##############################################
def legend(grid, win, plot, figure, conf):
    '''
    This function creates the widget
    for legend properties

    Parameters:
    -----------
    grid        QgridLayout object
    win         FigureCanvas object
    plot        subplot object
    figure      Figure object

    Return:
    -------
    none
    '''
    flist = matplotlib.font_manager.get_fontconfig_fonts()

    names = []
    for fname in flist:
        try:	
            a = matplotlib.font_manager.FontProperties(fname=fname).get_name()
            names.append(a)
        except:
            pass
    ###name of the section
    names = numpy.array(names)
    names = numpy.delete(names,numpy.where(names == 'Goha-Tibeb Zemen' ) )


    ###name of the section
    ax = QLabel('--LEGEND--')  ###label
    grid.addWidget(ax, 22, 0, 1, 1)
    ax.setFont(myFont_sec)

    ###frame on, off
    frame = QCheckBox('Frame On/Off')
    if conf['Frame'].lower() == 'on':
        frame.setChecked(True)
    elif conf['Frame'].lower() == 'off':
        frame.setChecked(False)

    grid.addWidget(frame, 23, 0, 1, 1)
    frame.setFont(myFont)

    ####legend fontsize width label width
    lfs = QLabel('Legend size:')  ###label
    grid.addWidget(lfs, 24, 0, 1, 1)
    lfs.setFont(myFont)
    lfsize = QSpinBox()  ##spinbox linewidth
    grid.addWidget(lfsize, 24, 1, 1, 1)
    lfsize.setMinimum(0)
    lfsize.setMaximum(100)
    lfsize.setValue(conf['font_size']) ###set default
    
    ####font 
    flegend = QLabel('Font legend:')  ###label
    grid.addWidget(flegend, 26, 0, 1, 1)
    flegend.setFont(myFont)
    flegend_combo = QComboBox()  ##creation combobox
    grid.addWidget(flegend_combo, 26, 1, 1, 1)
    for i in names:  ###fill it
        flegend_combo.addItem(i)
    
    fonts = numpy.where(names == conf['Legend_font'])
    if len(fonts[0]) == 0:
        from_conf = 0
    else:
        from_conf = fonts[0][0]
    flegend_combo.setCurrentIndex(from_conf) ##set default


    ####color
    leg_col = QLabel('Label Color:')  ###label
    grid.addWidget(leg_col, 27, 0, 1, 1)
    leg_col.setFont(myFont)
    leg_col_combo = QComboBox()  ##creation combobox
    grid.addWidget(leg_col_combo, 27, 1, 1, 2)
    for i in allcolors:  ###fill it
        leg_col_combo.addItem(i)

    font_col = numpy.where(allcolors == conf['Label_font_color'])
    if len(fonts[0]) == 0:
        from_conf = 0
    else:
        from_conf = font_col[0][0]
    leg_col_combo.setCurrentIndex(from_conf) ##set default


    ####location
    leg_loc = QLabel('Legend location:')  ###label
    grid.addWidget(leg_loc, 28, 0, 1, 1)
    leg_loc.setFont(myFont)
    leg_loc_combo = QComboBox()  ##creation combobox
    grid.addWidget(leg_loc_combo, 28, 1, 1, 2)
    locations = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'left',\
            'center left', 'center right', 'lower center', 'upper center', 'center']
    for i in locations:
        leg_loc_combo.addItem(i)
    name_id = location_leg(conf['location'])
    leg_loc_combo.setCurrentIndex(name_id) ##set default


    ###load default values
    legend_event(win, plot, figure, frame, lfsize, flegend_combo, leg_col_combo, conf, leg_loc_combo) 

    ##events
    frame.stateChanged.connect(partial(legend_event, win, plot, figure, \
            frame, lfsize, flegend_combo, leg_col_combo, conf, leg_loc_combo))
    lfsize.valueChanged.connect(partial(legend_event, win, plot, figure, \
            frame, lfsize, flegend_combo, leg_col_combo, conf, leg_loc_combo))
    flegend_combo.currentIndexChanged.connect(partial(legend_event, win, plot, figure, \
            frame, lfsize, flegend_combo, leg_col_combo, conf, leg_loc_combo))
    leg_col_combo.currentIndexChanged.connect(partial(legend_event, win, plot, figure, \
            frame, lfsize, flegend_combo, leg_col_combo, conf, leg_loc_combo))
    leg_loc_combo.currentIndexChanged.connect(partial(legend_event, win, plot, figure, \
            frame, lfsize, flegend_combo, leg_col_combo, conf, leg_loc_combo))


def legend_event(win, plot, figure, frame, lfsize, flegend_box, leg_col_box, conf, leg_loc_box):
    '''
    This function change the propertoes of the legend.
    Parameters:
    -----------
    win             FigureCanvas, obj
    plot            subplot, obj
    figure          Figure, obj
    frame           QCheckBox
    lfsize          QSpinBox
    flegend_comvo   QComboBox
    leg_col_combo   QComboBox
    '''

    ####retrieve information
    frame_status = frame.isChecked()
    fontsize = lfsize.value()
    flegend = flegend_box.currentText()
    leg_col = leg_col_box.currentText()
    leg_loc = leg_loc_box.currentText()

    ##update conf
    if frame_status == True:
        conf['Frame'] = 'on'
    if frame_status == False:
        conf['Frame'] = 'off'

    conf['font_size'] = fontsize
    conf['Label_font_color'] = leg_col
    conf['Legend_font'] = flegend
    conf['location'] = leg_loc


    #####
    leg = plot.legend(loc = leg_loc, \
            fontsize = fontsize)

    leg.get_frame().set_facecolor('none')

    ####frame
    leg.set_frame_on(frame_status)
    handles, labels = plot.get_legend_handles_labels()

    if len(handles)>0:
        for i in leg.get_texts():
            i.set_y(-2)
            i.set_color(leg_col)
            i.set_fontname(flegend)
    else:
        leg.remove()

    figure.tight_layout()
    win.draw()
    return frame_status


def location_leg(loc):
    locations = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'left', \
            'center left', 'center right', 'lower center', 'upper center', 'center']
    return numpy.where(loc==numpy.array(locations))[0][0]
     

