#!/usr/bin/python
'''
############################
#####
#####       Photon
#####      R. THOMAS
#####        2018
#####        Main
#####
##### Usage: photon [-h] [-t] file
#####---------------------------------------
#####
###########################
@License: GPL - see LICENCE.txt
'''
####Public General Libraries
import warnings
import os
from functools import partial
import numpy
import fitsio
from scipy.ndimage import gaussian_filter 

######Qt5
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QVBoxLayout, \
        QTabWidget, QTabWidget, QLineEdit, QLineEdit, QInputDialog, QCheckBox, \
        QHBoxLayout, QScrollArea, QComboBox, QPushButton, QLabel, QSlider, QFileDialog,\
        QSpinBox, QFrame

###matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib.colors as col
import matplotlib
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=matplotlib.mplDeprecation)
warnings.simplefilter(action='ignore', category=UserWarning)

####some matplotlib fixed parameters
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['savefig.directory'] = ''
matplotlib.rcParams['savefig.format'] = 'eps'

####local imports
from . import cli 
from . import extract 
from . import parameters_matplotlib as pm
from . import tooltips 
from . import write_conf as write
from . import write_plot as saveplot
from . import barplot as barplot
from . import read_conf as conf
from . import extract_plot as loadplot
from . import zscale as ds9
from . import get_axis_limits as limits
from . import __info__


#####################FONT QT4, size and bold
myFont = QtGui.QFont()
myFont.setBold(True)
myFont.setPointSize(9)
#######################################################################################

################matplotlib colors
allcolors = [i for i in matplotlib.colors.cnames]
allcolors = numpy.array(allcolors+list(map(str,numpy.arange(1,10,0.5)/10)))
################matplotlib linestyle
linestyles = list(matplotlib.lines.lineStyles.keys())
finalstyles = numpy.array([i for i in linestyles if i != 'None' and i != None and i != ' ' and i != ''])
################matplotlib markers
markers = list(matplotlib.markers.MarkerStyle.markers.keys())
finalmarkers = numpy.array([i for i in markers if i not in range(12) and i != 'None' and i != None])
################matplotlib cmaps
maps = numpy.array(list(m for m in plt.cm.datad if not m.endswith("_r")))
#######################################################################################

class Main_window(QWidget):

    def __init__(self, cli_args):
        '''
        Class constructor
        '''
        super().__init__()
        self.args = cli_args
        self.lineindex = 0
        self.scatterindex = 0
        self.errorindex = 0
        self.imageindex = 0
        self.histindex = 0
        self.diag_index = 0
        self.plot_index = 0
        self.dico_widget = {}
        self.straight_index = 0
        self.strip_index = 0
        self.text_index = 0
        self.widget_list = []
        self.initUI()
        if self.args.file:
            self.setWindowTitle('Photon V%s, file: %s' %(__info__.__version__, self.args.file))
        else:
            self.setWindowTitle('Photon V%s, plot: %s' %(__info__.__version__, self.args.plot))

    def initUI(self):
        '''
        This method creates the main window
        '''

        ### 1 we create the grid
        self.Global = QVBoxLayout(self)
        self.setLayout(self.Global)
        grid = QGridLayout()
        self.Global.addLayout(grid)

        ### a- space for plot
        self.tab = QTabWidget()
        self.figure = Figure()
        self.figure.subplots_adjust(hspace=0, right=0.95, top=0.94, left=0.15)
        self.win = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.win, self.win)
        grid.addWidget(self.win, 0, 0, 1, 3)
        grid.addWidget(self.toolbar, 1, 0, 1, 3)
        self.plot = self.figure.add_subplot(111)
        self.plot.legend()

        #### b- plot!
        self.buttonaddcurve = QPushButton("Add element in plot")
        grid.addWidget(self.buttonaddcurve, 2, 0, 1, 3)
        self.buttonaddcurve.clicked.connect(self.adddisplay)
        self.buttonaddcurve.setToolTip(tooltips.tt_button_add())

        #### c- labels
        if self.args.plot:
            self.loaded_plot = loadplot.loadplot(self.args.plot) 
            xlab = self.loaded_plot.plotconf['types']['xlabel']
            ylab = self.loaded_plot.plotconf['types']['ylabel']
        else:
            xlab = 'Xlabel'
            ylab = 'Ylabel'

        self.xlabl = QLineEdit()
        grid.addWidget(self.xlabl, 3, 1, 1, 1)
        self.xlabl.setText(xlab)
        self.xlabl.textChanged.connect(self.changexlabl)
        self.xlabl.setFont(myFont)
        self.plot.set_xlabel(xlab)

        self.ylabl = QLineEdit()
        grid.addWidget(self.ylabl, 3, 2, 1, 1)
        self.ylabl.textChanged.connect(self.changeylabl)
        self.ylabl.setText(ylab)
        self.ylabl.setFont(myFont)
        self.plot.set_ylabel(ylab)


        ####we create a horizontal split and add it the to global
        ####box
        panels = QHBoxLayout()
        self.Global.addLayout(panels)

        ###multi curve area
        #####we create a scroll area what we put inside the panels
        scrollplot = QScrollArea()
        scrollplot.setMinimumWidth(int(float(self.args.width)/2))
        scrollplot.setWidgetResizable(True)
        scrollplot.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrollplot.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        widgetplt = QWidget()
        self.plotarea = QGridLayout()
        widgetplt.setLayout(self.plotarea)
        scrollplot.setWidget(widgetplt)
        panels.addWidget(scrollplot)
        [self.plotarea.setRowStretch(i, 2) for i in range(31)]

        ###button save plot
        buttonsave = QPushButton("Save plot")
        self.plotarea.addWidget(buttonsave, 0, 0, 1, 2)
        buttonsave.clicked.connect(self.save_fig)
        self.plot_index += 1
 

        ###parameter area
        ### a - we create the grid in a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        widget = QWidget()
        self.properties = QGridLayout()
        widget.setLayout(self.properties)
        
        ### b - and creates the widgets
        self.config = conf.Conf(self.args.custom)
        if self.args.plot == None:
            self.loaded_plot = type('test', (object,), {})()
            self.loaded_plot.plotconf = {}
            self.loaded_plot.plotconf['types'] = {'xmin':'Xmin', 'xmax':'Xmax', \
                    'ymin':'Ymin', 'ymax':'Ymax'}
        pm.axis_lim(self.properties, self.win, self.plot, self.figure, self.loaded_plot, self.config)
        pm.background(self.properties, self.win, self.plot, self.figure, self.config)
        pm.axis(self.properties, self.win, self.plot, self.figure, self.config.axis)
        pm.fonts(self.properties, self.win, self.plot, self.figure, self.config)

        buttontheme = QPushButton("Save new Theme")
        self.properties.addWidget(buttontheme, 29, 0, 1, 2)
        buttontheme.clicked.connect(self.save_theme)

        scroll.setWidget(widget)
        panels.addWidget(scroll)


        ##load configuration, if one was given
        if self.args.plot:
            all_load = list(self.loaded_plot.plotconf.keys())
            for i in all_load:
                if i[:4] == 'Line':
                    self.add_line(self.loaded_plot.plotconf[i])
                if i[:4] == 'Scat':
                    self.add_scatter(self.loaded_plot.plotconf[i])
                if i[:4] == 'Text':
                    self.add_text(self.loaded_plot.plotconf[i]) 
                if i[:4] == 'Stra':
                    self.add_straightline(self.loaded_plot.plotconf[i])
                if i[:4] == 'Stri':
                    self.add_span(self.loaded_plot.plotconf[i])
                if i[:4] == 'Hist':
                    self.add_hist(self.loaded_plot.plotconf[i])
                if i[:4] == 'Erro':
                    self.add_error(self.loaded_plot.plotconf[i])
                if i[:4] == 'Imag':
                    self.add_image(self.loaded_plot.plotconf[i])
                 
        pm.ticks(self.properties, self.win, self.plot, self.figure, self.config.ticks)
        pm.legend(self.properties, self.win, self.plot, self.figure, self.config.legend)

        self.figure.tight_layout()
        self.win.draw()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        logo = os.path.join(dir_path, 'logo.png')

        self.setWindowIcon(QtGui.QIcon(logo))
        self.show()

    def save_fig(self):
        '''
        Method that save all the configuration of the plot
        so one can reload it and see the plot directly
        '''
        save_file = QFileDialog.getSaveFileName(self, "Save plot configuration")[0]
        if save_file != '':
            saveplot.save(save_file, self)

    def save_theme(self):
        '''
        MEthod that send the properties object to
        create a new property file with the current
        configuration.
        '''
        save_file = QFileDialog.getSaveFileName(self, "Save Files")[0]
        if save_file != '':
            write.save(save_file, self.config)


    def changeylabl(self):
        '''
        This method changes the ylabel of the plot
        '''

        lab = self.plot.yaxis.label
        text = self.ylabl.text()
        try:
            lab.set_text(text)
            lab._get_layout(self.figure.canvas.renderer)
        except:
            pass
        else:
            self.figure.tight_layout()
            self.win.draw_idle()

    def changexlabl(self):
        '''
        This method changes the xlabel of the plot
        '''
        lab = self.plot.xaxis.label
        text = self.xlabl.text()
        try:
            lab.set_text(text)
            lab._get_layout(self.figure.canvas.renderer)
        except:
            pass
        else:
            self.figure.tight_layout()
            self.win.draw_idle()

    def changeleg(self, text):
        '''
        This is a trick method to check that legend labels
        are ok to be displayed out
        '''
        lab = self.plot.yaxis.label
        try:
            lab.set_text(text)
            lab._get_layout(self.figure.canvas.renderer)
        except:
            return 'nok'
        else:
            self.win.draw_idle()
            self.figure.tight_layout()
            return 'ok'



    def adddisplay(self):
        '''
        This selects the type of plot to add
        '''
        ###define types of plot
        if self.args.file == None:
            typs = ['line / new file', 'scatter / new file', 'histogram / new file', \
                    'straight-line', 'Span', 'Text', 'Error / New file', 'Image / New file']
        else:
            typs = ['line', 'line / new file', 'scatter',\
                'scatter / new file', 'histogram', 'histogram / new file', \
                'straight-line', 'Span', 'Text', 'Error', 'Error / New file', \
                'Image', 'Image / New file']

        ###display the popup choices
        typ, okpressed = QInputDialog.getItem(self, "Plot type", "Choose:", typs, 0, False)
        if okpressed is True:
            if typ == 'scatter':
                self.add_scatter(self.args.file)
            if typ == 'scatter / new file':
                inputfile = self.browse()
                self.add_scatter(inputfile)
            if typ == 'line':
                self.add_line(self.args.file)
            if typ == 'line / new file':
                inputfile = self.browse()
                self.add_line(inputfile)
            if typ == 'histogram':
                self.add_hist(self.args.file)
            if typ == 'histogram / new file':
                inputfile = self.browse()
                self.add_hist(inputfile)
            if typ == 'Error / New file':
                inputfile = self.browse()
                self.add_error(inputfile)
            if typ == 'Error':
                self.add_error(self.args.file)
            if typ == 'straight-line':
                self.add_straightline('fake')
            if typ == 'Span':
                self.add_span('fake')
            if typ == 'Text':
                self.add_text('fake')
            if typ == 'Image':
                self.add_image(self.args.file)
            if typ == 'Image / New file':
                inputfile = self.browse(args.file)
                self.add_image()


    def browse(self):
        '''
        This method open a file dialog to choose a new catalog file
        '''
        new_file = QFileDialog.getOpenFileName(self, "Find Files")[0]
        if new_file == '':
            new_file = self.args.file
        return new_file

    def add_image(self, conf):
        '''
        This adds a scatter plot with errors configuration to the plot area
        '''

        if isinstance(conf, str) is True:
            inputfile=conf
            conf = {}
            conf['file'] = inputfile
            conf['zscale'] = 'Yes'
            conf['zorder'] = '0'
            conf['colormap'] = 'Greys'
            conf['contour'] = 'No'
            conf['contour_color'] = 'black'
            conf['contour_size'] = 1
            conf['contour_lw'] = 1

        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'Image plot'+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('imag_%s_separation'%self.imageindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
 
        ###upgrade index
        self.imageindex += 1

        #### a - file
        self.labelfile = QLabel('%s'%conf['file'])
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('imag_%s_labelfile'%self.imageindex)
        self.labelfile.setFont(myFont)
        
        #### b- label
        #self.label = QLineEdit()
        #self.label.setFont(myFont)
        #self.plotarea.addWidget(self.label, self.plot_index, 0, 1, 1)
        #self.label.setObjectName('imag_%s_label'%self.imageindex)
        #self.label.setText('image plot number%s'%self.imageindex)
        #self.label.setToolTip(tooltips.legend())

        #### c - empty marker
        self.zscale = QCheckBox('zscale')
        if conf['zscale'] == 'Yes':
            self.zscale.setChecked(True)
        self.plotarea.addWidget(self.zscale, self.plot_index, 1, 1, 1)
        self.zscale.setFont(myFont)
        self.zscale.setObjectName("imag_%s_zscale"%self.imageindex)
        self.zscale.setToolTip(tooltips.zscale())

        self.plot_index += 1
 
        #### d - scrooling list color
        self.map = QLabel('Colormap:')
        self.plotarea.addWidget(self.map, self.plot_index, 0, 1, 1)
        self.map.setObjectName('imag_%s_map'%self.imageindex)
        self.map.setFont(myFont)
        self.mapcombocolor = QComboBox(self)
        self.plotarea.addWidget(self.mapcombocolor, self.plot_index, 1, 1, 1)
        for i in maps:
            self.mapcombocolor.addItem(i)
        self.mapcombocolor.setObjectName("imag_%s_mapcolor"%self.imageindex)
        index = numpy.where(numpy.array(maps) == conf['colormap'])[0][0]
        self.mapcombocolor.setCurrentIndex(index)
        self.plot_index += 1

        ### e -contour 
        self.contourCB = QCheckBox('Contour')
        if conf['contour'] == 'Yes':
            self.contourCB.setChecked(True)
        self.plotarea.addWidget(self.contourCB, self.plot_index, 0, 1, 1)
        self.contourCB.setFont(myFont)
        self.contourCB.setObjectName("imag_%s_contour"%self.imageindex)
        self.zscale.setToolTip(tooltips.contour())

        self.contsize = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.contsize, self.plot_index, 1, 1, 1)
        self.contsize.setMinimum(0)
        self.contsize.setMaximum(100)
        self.contsize.setValue(conf['contour_size']) ###set default
        self.contsize.setObjectName("imag_%s_size"%self.imageindex)
        self.plot_index += 1

        ### f - slider lw
        self.sliderlw = QSlider(QtCore.Qt.Horizontal)
        self.sliderlw.setMinimum(1)
        self.sliderlw.setMaximum(100)
        self.sliderlw.setValue(conf['contour_lw'])
        self.plotarea.addWidget(self.sliderlw, self.plot_index, 0, 1, 2)
        self.sliderlw.setObjectName("imag_%s_slider"%self.imageindex)
        self.sliderlw.setToolTip(tooltips.slider_lw())
        self.plot_index += 1
 
        #### d - scrooling list color
        self.col = QLabel('Color contour:')
        self.plotarea.addWidget(self.col, self.plot_index, 0, 1, 1)
        self.col.setObjectName('imag_%s_col'%self.imageindex)
        self.col.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        self.combocolor.setObjectName("imag_%s_color"%self.imageindex)
        index = numpy.where(allcolors == conf['contour_color'])[0][0]
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling zorder
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('imag_%s_zorderlabel'%self.imageindex)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("imag_%s_zorder"%self.imageindex)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1

        self.make_imageplot(self.imageindex, conf['file'])

        ##events
        self.mapcombocolor.currentIndexChanged.connect(partial(self.make_imageplot, \
                self.imageindex, conf['file']))

        #self.label.textChanged.connect(partial(self.make_imageplot, \
        #        self.imageindex, inputfile))

        self.zscale.stateChanged.connect(partial(self.make_imageplot, \
                self.imageindex, conf['file']))

        self.contourCB.stateChanged.connect(partial(self.make_imageplot, \
                self.imageindex, conf['file']))

        self.contsize.valueChanged.connect(partial(self.make_imageplot, \
                self.imageindex, conf['file']))

        self.sliderlw.valueChanged.connect(partial(self.make_imageplot, \
                self.imageindex, conf['file']))

        self.combocolor.currentIndexChanged.connect(partial(self.make_imageplot, \
                self.imageindex, conf['file']))


    def make_imageplot(self, index, inputfile):
        '''
        This function makes the errorbar plot.

        Parameters
        ----------
        index       str, index of errorbar plot
        inputfile   str, path/and/name of the catalog we are drawing from
        '''

        ##check if this scatter plot was already in place
        ##if yes, we remove it
        if 'imag_'+str(index) in self.dico_widget.keys():
            self.dico_widget['imag_'+str(index)]._label = ''
            self.dico_widget['imag_'+str(index)].remove()
            self.win.draw()

        if 'cont_'+str(index) in self.dico_widget.keys():
            col = self.dico_widget['cont_'+str(index)].collections
            try:
                for i in col:
                    i.remove()
            except:
                pass
            self.win.draw()

        ###extract fits
        IM = fitsio.read(inputfile)

        a = self.plotarea.parentWidget().findChildren(QComboBox, 'imag_%s_mapcolor'%index)
        color = a[0].currentText()

        ##size
        a = self.plotarea.parentWidget().findChildren(QSpinBox, 'imag_%s_size'%index)
        size = a[0].value()/100

        ##zscale
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'imag_%s_zscale'%index)
        scale = a[0].isChecked()

        ##contour
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'imag_%s_contour'%index)
        contour = a[0].isChecked()

        #tr
        a = self.plotarea.parentWidget().findChildren(QSlider, 'imag_%s_slider'%index)
        lw = a[0].value()/10

        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'imag_%s_color'%index)
        colorc = a[0].currentText()

        ###plot
        if scale is True:

            z1, z2 = ds9.zscale_algo().zscale(IM)

            self.image = self.plot.imshow(IM, cmap=color, vmin=z1, vmax=z2,\
                     origin='lower', interpolation='nearest')

        else:
            self.image = self.plot.imshow(IM, cmap=color, 
                    origin='lower', interpolation='nearest')

        if contour is True:
            self.cont = self.plot.contour(IM, levels=[size], linewidths=[lw], colors=[colorc])
            self.dico_widget['cont_'+str(index)] = self.cont
        else:
            pass

        ###save the plot in a dictionnary
        self.dico_widget['imag_'+str(index)] = self.image

        ###tight layouts
        self.figure.tight_layout()

        ##redraw
        self.win.draw()


    def add_error(self, conf):
        '''
        This adds a scatter plot with errors configuration to the plot area
        '''

        if isinstance(conf, str) is True:
            inputfile=conf
            conf = {}
            conf['file'] = inputfile
            conf['label'] = 'error plot number %s'%(self.errorindex) 
            conf['color'] = 'black'
            conf['marker'] = '.'
            conf['transparency'] = 10
            conf['barsize'] = 10
            conf['capsize'] = 50
            conf['size'] = 10
            conf['empty'] = 'No'
            conf['zorder'] = '1'



        #Retrieve columns
        columns = numpy.array(extract.header(conf['file']))

        if 'x' not in conf.keys():
            conf['x'] = columns[0]
            conf['xerrm'] = columns[0]
            conf['xerrp'] = columns[0]
            conf['y'] = columns[0]
            conf['yerrm'] = columns[0]
            conf['yerrp'] = columns[0]

        ###upgrade index
        self.errorindex += 1

        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'Error plot'+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('erro_%s_separation'%self.errorindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        self.filX = QLabel('File:')
        self.plotarea.addWidget(self.filX, self.plot_index, 0, 1, 1)
        self.filX.setObjectName('erro_%s_filex'%self.errorindex)
        self.filX.setFont(myFont)

        #### c - scrooling list X
        self.labelfile = QLabel(conf['file'])
        self.plotarea.addWidget(self.labelfile, self.plot_index, 1, 1, 2)
        self.labelfile.setObjectName('erro_%s_labelfile'%self.errorindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        #### a- label
        self.label = QLineEdit()
        self.label.setFont(myFont)
        self.plotarea.addWidget(self.label, self.plot_index, 0, 1, 1)
        self.label.setObjectName('erro_%s_label'%self.errorindex)
        self.label.setText(conf['label'])
        self.label.setToolTip(tooltips.legend())

        #### b- plot!
        self.buttondel = QPushButton("Delete data")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.errorindex, 'erro'))
        self.buttondel.setObjectName('erro_%s_del'%self.errorindex)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### b - scrooling list X
        ####label
        self.labelX = QLabel('X:')
        self.plotarea.addWidget(self.labelX, self.plot_index, 0, 1, 1)
        self.labelX.setObjectName('erro_%s_labelx'%self.errorindex)
        self.labelX.setFont(myFont)
        self.comboX = QComboBox(self)
        self.plotarea.addWidget(self.comboX, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboX.addItem(columns[i])
        self.comboX.setObjectName("erro_%s_X"%self.errorindex)
        index = numpy.where(columns == conf['x'])[0][0]
        self.comboX.setCurrentIndex(index)
        self.plot_index += 1

        #### c - scrooling list X
        self.labelY = QLabel('Y:')
        self.plotarea.addWidget(self.labelY, self.plot_index, 0, 1, 1)
        self.labelY.setObjectName('erro_%s_labely'%self.errorindex)
        self.labelY.setFont(myFont)
        self.comboY = QComboBox(self)
        self.plotarea.addWidget(self.comboY, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboY.addItem(columns[i])
        self.comboY.setObjectName("erro_%s_Y"%self.errorindex)
        index = numpy.where(columns == conf['y'])[0][0]
        self.comboY.setCurrentIndex(index)
        self.plot_index += 1


        #### d - scrooling list Xerrp
        ####label
        self.labelXp = QLabel('Xerr+:')
        self.plotarea.addWidget(self.labelXp, self.plot_index, 0, 1, 1)
        self.labelXp.setObjectName('erro_%s_labelyerrp'%self.errorindex)
        self.labelXp.setFont(myFont)
        self.comboXp = QComboBox(self)
        self.plotarea.addWidget(self.comboXp, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboXp.addItem(columns[i])
        self.comboXp.addItem('None')
        self.comboXp.setObjectName("erro_%s_xerrp"%self.errorindex)
        columnbis = numpy.array(columns.tolist()+ ['None'])
        index = numpy.where(columnbis == conf['xerrp'])[0][0]
        self.comboXp.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling list Xerrp
        ####label
        self.labelXm = QLabel('Xerr-:')
        self.plotarea.addWidget(self.labelXm, self.plot_index, 0, 1, 1)
        self.labelXm.setObjectName('erro_%s_labelyerrm'%self.errorindex)
        self.labelXm.setFont(myFont)
        self.comboXm = QComboBox(self)
        self.plotarea.addWidget(self.comboXm, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboXm.addItem(columns[i])
        self.comboXm.addItem('None')
        self.comboXm.setObjectName("erro_%s_xerrm"%self.errorindex)
        columnbis = numpy.array(columns.tolist() + ['None'])
        index = numpy.where(columnbis == conf['xerrp'])[0][0]
        self.comboXm.setCurrentIndex(index)
        self.plot_index += 1

        #### f - scrooling list Yerrp
        self.labelYp = QLabel('Yerr+:')
        self.plotarea.addWidget(self.labelYp, self.plot_index, 0, 1, 1)
        self.labelYp.setObjectName('erro_%s_labelyerrp'%self.errorindex)
        self.labelYp.setFont(myFont)
        self.comboYp = QComboBox(self)
        self.plotarea.addWidget(self.comboYp, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboYp.addItem(columns[i])
        self.comboYp.addItem('None')
        self.comboYp.setObjectName("erro_%s_yerrp"%self.errorindex)
        columnbis = numpy.array(columns.tolist()+['None'])
        index = numpy.where(columnbis == conf['yerrp'])[0][0]
        self.comboYp.setCurrentIndex(index)
        self.plot_index += 1

        #### g - scrooling list Yerrp
        self.labelYm = QLabel('Yerr-:')
        self.plotarea.addWidget(self.labelYm, self.plot_index, 0, 1, 1)
        self.labelYm.setObjectName('erro_%s_labelyerrm'%self.errorindex)
        self.labelYm.setFont(myFont)
        self.comboYm = QComboBox(self)
        self.plotarea.addWidget(self.comboYm, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboYm.addItem(columns[i])
        self.comboYm.addItem('None')
        self.comboYm.setObjectName("erro_%s_yerrm"%self.errorindex)
        columnbis = numpy.array(columns.tolist()+['None'])
        index = numpy.where(columnbis == conf['yerrm'])[0][0]
        self.comboYm.setCurrentIndex(index)
        self.plot_index += 1

        #### d - scrooling list color
        self.errcol = QLabel('Color:')
        self.plotarea.addWidget(self.errcol, self.plot_index, 0, 1, 1)
        self.errcol.setObjectName('erro_%s_col'%self.errorindex)
        self.errcol.setFont(myFont)
        self.errcombocolor = QComboBox(self)
        self.plotarea.addWidget(self.errcombocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.errcombocolor.addItem(i)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.errcombocolor.setObjectName("erro_%s_color"%self.errorindex)
        self.errcombocolor.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling list markers
        self.errmarkerlab = QLabel('Marker:')
        self.plotarea.addWidget(self.errmarkerlab, self.plot_index, 0, 1, 1)
        self.errmarkerlab.setObjectName('erro_%s_mlab'%self.errorindex)
        self.errmarkerlab.setFont(myFont)
        self.errcombomarkers = QComboBox(self)
        for i in finalmarkers:
            self.errcombomarkers.addItem(str(i))
        index = numpy.where(finalmarkers == conf['marker'])[0][0]
        self.errcombomarkers.setObjectName("erro_%s_marker"%self.errorindex)
        self.plotarea.addWidget(self.errcombomarkers, self.plot_index, 1, 1, 1)
        self.plot_index += 1
        
        #### f - marker_width
        self.errslab = QLabel('Size:')
        self.plotarea.addWidget(self.errslab, self.plot_index, 0, 1, 1)
        self.errslab.setObjectName('erro_%s_slab'%self.errorindex)
        self.errslab.setFont(myFont)
        self.errscatsize = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.errscatsize, self.plot_index, 1, 1, 1)
        self.errscatsize.setMinimum(0)
        self.errscatsize.setMaximum(500)
        self.errscatsize.setValue(conf['size']) ###set default
        self.errscatsize.setObjectName("erro_%s_size"%self.errorindex)
        self.plot_index += 1


        #### g - empty marker
        self.errempty = QCheckBox('Empty marker')
        if conf['empty'] == 'Yes':
            self.errempty.setChecked(True)
        self.plotarea.addWidget(self.errempty, self.plot_index, 0, 1, 1)
        self.errempty.setFont(myFont)
        self.errempty.setObjectName("erro_%s_empty"%self.errorindex)
        self.errempty.setToolTip(tooltips.empty())
        self.plot_index += 1

        ### h - slider lw
        '''
        self.errslider = QSlider(QtCore.Qt.Horizontal)
        self.errslider.setMinimum(1)
        self.errslider.setMaximum(30)
        self.errslider.setValue(10)
        self.plotarea.addWidget(self.errslider, self.plot_index, 0, 1, 2)
        self.errslider.setObjectName("erro_%s_slider"%self.errorindex)
        self.errslider.setToolTip(tooltips.slider_lw())
        self.plot_index += 1
        '''

        ### i - slider transparency
        self.errslidertr = QSlider(QtCore.Qt.Horizontal)
        self.errslidertr.setMinimum(1)
        self.errslidertr.setMaximum(10)
        self.errslidertr.setValue(conf['transparency'])
        self.plotarea.addWidget(self.errslidertr, self.plot_index, 0, 1, 2)
        self.errslidertr.setObjectName("erro_%s_tr"%self.errorindex)
        self.errslidertr.setToolTip(tooltips.slider_tr())
        self.plot_index += 1
 
        #### g - bar size
        self.lbarsize = QLabel('error bar tickness:')
        self.plotarea.addWidget(self.lbarsize, self.plot_index, 0, 1, 1)
        self.lbarsize.setObjectName('erro_%s_lbarsize'%self.errorindex)
        self.lbarsize.setFont(myFont)

        self.barsize = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.barsize, self.plot_index, 1, 1, 1)
        self.barsize.setMinimum(0)
        self.barsize.setMaximum(500)
        self.barsize.setValue(conf['barsize']) ###set default
        self.barsize.setObjectName("erro_%s_barsize"%self.errorindex)
        self.plot_index += 1

        #### h - capsize
        self.lcapsize = QLabel('error bar cap size:')
        self.plotarea.addWidget(self.lcapsize, self.plot_index, 0, 1, 1)
        self.lcapsize.setObjectName('erro_%s_lcapsize'%self.errorindex)
        self.lcapsize.setFont(myFont)

        self.capsize = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.capsize, self.plot_index, 1, 1, 1)
        self.capsize.setMinimum(0)
        self.capsize.setMaximum(500)
        self.capsize.setValue(conf['capsize']) ###set default
        self.capsize.setObjectName("erro_%s_capsize"%self.errorindex)
        self.plot_index += 1

        #### e - scrooling zorder
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('erro_%s_zorderlabel'%self.errorindex)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("erro_%s_zorder"%self.errorindex)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1

        ##load first
        self.make_errplot(self.errorindex, conf['file'])
        
        ##events
        self.comboY.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.comboX.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.comboXp.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.comboXm.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.comboYp.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.comboYm.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.errscatsize.valueChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.errcombomarkers.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.errcombocolor.currentIndexChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.label.textChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.zorderedit.textChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.errempty.stateChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        #self.errslider.valueChanged.connect(partial(self.make_errplot, \
        #        self.errorindex, inputfile))

        self.errslidertr.valueChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.barsize.valueChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))

        self.capsize.valueChanged.connect(partial(self.make_errplot, \
                self.errorindex, conf['file']))




    def make_errplot(self, index, inputfile):
        '''
        This function makes the errorbar plot.

        Parameters
        ----------
        index       str, index of errorbar plot
        inputfile   str, path/and/name of the catalog we are drawing from
        '''

        ##check if this scatter plot was already in place
        ##if yes, we remove it
        if 'erro_'+str(index) in self.dico_widget.keys():
            self.dico_widget['erro_'+str(index)]._label = ''
            self.dico_widget['erro_'+str(index)].remove()
            self.win.draw()

        ###get columns
        columns = extract.header(inputfile)

        ###get marker
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_marker'%index)
        marker = a[0].currentText()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'erro_%s_label'%index)
        label = a[0].text()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'erro_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = int(zorder)
        except:
            zorder = 1

        ###get X data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_X'%index)
        X = a[0].currentText()
        try:
            Xl = [float(i) for i in extract.column(X, columns, inputfile)]
        except:
            Xl = numpy.ones(len(extract.column(X, columns, inputfile)))


        ####get error Xp and Xm
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_xerrp'%index)
        Xp = a[0].currentText()
        if Xp == 'None':
            Xp = numpy.zeros(len(extract.column(X, columns, inputfile))) 
        else:
            try:
                Xp = [float(i) for i in extract.column(Xp, columns, inputfile)]
            except:
                Xp = numpy.zeros(len(extract.column(X, columns, inputfile)))

        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_xerrm'%index)
        Xm = a[0].currentText()
        if Xm == 'None':
            Xm = numpy.zeros(len(extract.column(X, columns, inputfile))) 
        else:
            try:
                Xm = [float(i) for i in extract.column(Xm, columns, inputfile)]
            except:
                Xm = numpy.zeros(len(extract.column(X, columns, inputfile)))

        ###get Y data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_Y'%index)
        Y = a[0].currentText()
        try:
            Yl = [float(i) for i in extract.column(Y, columns, inputfile)]
        except: 
            Yl = numpy.ones(len(extract.column(Y, columns, inputfile)))

        ####get error Yp and Ym
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_yerrp'%index)
        Yp = a[0].currentText()
        if Yp == 'None':
            Yp = numpy.zeros(len(extract.column(Y, columns, inputfile)))
        else:
            try:
                Yp = [float(i) for i in extract.column(Yp, columns, inputfile)]
            except:
                Yp = numpy.zeros(len(extract.column(Y, columns, inputfile)))

        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_yerrm'%index)
        Ym = a[0].currentText()
        if Ym == 'None':
            Ym = numpy.zeros(len(extract.column(Y, columns, inputfile)))
        else:
            try:
                Ym = [float(i) for i in extract.column(Ym, columns, inputfile)]
            except:
                Ym = numpy.zeros(len(extract.column(Y, columns, inputfile)))
        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'erro_%s_color'%index)
        color = a[0].currentText()

        ##size
        a = self.plotarea.parentWidget().findChildren(QSpinBox, 'erro_%s_size'%index)
        size = a[0].value()

        ##checkbox
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'erro_%s_empty'%index)
        empty = a[0].isChecked()

        ##lw
        #a = self.plotarea.parentWidget().findChildren(QSlider, 'erro_%s_slider'%index)
        #lw = a[0].value()/10

        #tr
        a = self.plotarea.parentWidget().findChildren(QSlider, 'erro_%s_tr'%index)
        tr = a[0].value()/10

        #barsize
        a = self.plotarea.parentWidget().findChildren(QSpinBox, 'erro_%s_barsize'%index)
        bsize = a[0].value()/10

        #capsize
        a = self.plotarea.parentWidget().findChildren(QSpinBox, 'erro_%s_capsize'%index)
        capsize = a[0].value()/10


        ###plot
        if empty is True:
            self.errors = self.plot.errorbar(Xl, Yl, yerr = [Ym, Yp], xerr = [Xm, Xp], ls = 'none', \
                    marker=marker, alpha = tr, label=r'%s'%label, markersize = size, \
                    markerfacecolor=self.figure.get_facecolor(), color=color, \
                    capsize=capsize, elinewidth=bsize, zorder = zorder)

        else:
            self.errors = self.plot.errorbar(Xl, Yl, yerr = [Ym, Yp], xerr = [Xm, Xp], ls = 'none', \
                    marker=marker, alpha = tr, label=r'%s'%label, markersize = size, color=color, \
                    capsize=capsize, elinewidth=bsize, zorder=zorder)


        ###save the plot in a dictionnary
        self.dico_widget['erro_'+str(index)] = self.errors

        ###add legend
        ###this is a quick and dirty trick to check if
        ###the mathText entry are ok
        labl = self.errors.get_label()
        p = self.changeleg(labl)
        if p == 'nok':
            self.changeleg(self.ylabl.text())
            self.dico_widget['erro_'+str(index)]._label = 'retry'
            self.changeylabl()
        else:
            self.changeleg(self.ylabl.text())

        ###add legend
        handles, labels = self.plot.get_legend_handles_labels()
        self.plot.legend(handles, labels)

        ###tight layouts
        self.figure.tight_layout()

        ##redraw
        self.win.draw()

       



    def add_text(self, conf):
        '''
        This method adds widget for span strips (vertical or horizontal)
        '''

        if conf == 'fake':
            conf = {}
            conf['text'] = 'text'
            conf['coor'] = '0.3, 0.7'
            conf['color'] = 'black'
            conf['angle'] = 0
            conf['size'] = 20
            conf['zorder'] = '1'


        ##update index
        self.text_index += 1

        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'text display'+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('text_%s_separation'%self.text_index)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        self.filX = QLabel('File:')
        self.plotarea.addWidget(self.filX, self.plot_index, 0, 1, 1)
        self.filX.setObjectName('text_%s_filex'%self.text_index)
        self.filX.setFont(myFont)




        #### a- delete
        self.buttondel = QPushButton("Delete text")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.text_index, 'text'))
        self.buttondel.setObjectName('text_%s_del'%self.text_index)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### b- text
        self.text = QLabel('Text')
        self.plotarea.addWidget(self.text, self.plot_index, 0, 1, 1)
        self.text.setObjectName("text_%s_text"%self.text_index)
        self.text.setFont(myFont)
        self.text = QLineEdit()
        self.text.setFont(myFont)
        self.plotarea.addWidget(self.text, self.plot_index, 1, 1, 1)
        self.text.setObjectName('text_%s_text'%self.text_index)
        self.text.setText(conf['text'])
        self.widget_list.append(self.text)
        self.text.setToolTip(tooltips.coordinates_strip())
        self.plot_index += 1

        #### c- coordinates
        self.BG = QLabel('Coordinates')
        self.plotarea.addWidget(self.BG, self.plot_index, 0, 1, 1)
        self.BG.setObjectName("text_%s_coorlab"%self.text_index)
        self.BG.setFont(myFont)
        self.coor = QLineEdit()
        self.coor.setFont(myFont)
        self.plotarea.addWidget(self.coor, self.plot_index, 1, 1, 1)
        self.coor.setObjectName('text_%s_coor'%self.text_index)
        self.coor.setText(conf['coor'])
        self.widget_list.append(self.coor)
        self.coor.setToolTip(tooltips.coordinates_strip())
        self.plot_index += 1

        #### d - scrooling list color
        self.coll = QLabel('Color:')
        self.plotarea.addWidget(self.coll, self.plot_index, 0, 1, 1)
        self.coll.setObjectName("text_%s_collab"%self.text_index)
        self.coll.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.combocolor.setObjectName("text_%s_color"%self.text_index)
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1

        ### e- slider lw
        self.size = QSlider(QtCore.Qt.Horizontal)
        self.size.setMinimum(1)
        self.size.setMaximum(200)
        self.size.setValue(conf['size'])
        self.plotarea.addWidget(self.size, self.plot_index, 0, 1, 2)
        self.size.setObjectName("text_%s_slider"%self.text_index)
        self.plot_index += 1

        
        ### f - barplot
        self.angle = QLabel('Angle:')
        self.plotarea.addWidget(self.angle, self.plot_index, 0, 1, 1)
        self.angle.setObjectName("text_%s_anglelabel"%self.text_index)
        self.angle.setFont(myFont)
        self.textangle = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.textangle, self.plot_index, 1, 1, 1)
        self.textangle.setMinimum(0)
        self.textangle.setMaximum(360)
        self.textangle.setValue(conf['angle']) ###set default
        self.textangle.setObjectName("text_%s_angle"%self.text_index)
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('text_%s_zorderlabel'%self.text_index)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("text_%s_zorder"%self.text_index)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1

        #events
        self.combocolor.currentIndexChanged.connect(partial(self.make_text, \
                self.text_index))

        self.coor.textChanged.connect(partial(self.make_text, \
                self.text_index))

        self.text.textChanged.connect(partial(self.make_text, \
                self.text_index))

        self.size.valueChanged.connect(partial(self.make_text, \
                self.text_index))

        self.textangle.valueChanged.connect(partial(self.make_text, \
                self.text_index))

        self.zorderedit.textChanged.connect(partial(self.make_text, \
                self.text_index))

        self.make_text(self.text_index)

    def make_text(self, index):
        '''
        This method add the straight line depending on the
        parameters given by the user in the widgets.
        '''

        ##check if this hist plot was already in place
        ##if yes, we remove it
        if 'text_'+str(index) in self.dico_widget.keys():
            self.dico_widget['text_'+str(index)].remove()
            self.win.draw()

        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'text_%s_color'%index)
        color = a[0].currentText()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'text_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = int(zorder)
        except:
            zorder = 1


        ##text
        text = self.plotarea.parentWidget().findChildren(QLineEdit, 'text_%s_text'%index)
        text = text[0].text()

        ##size
        a = self.plotarea.parentWidget().findChildren(QSlider, 'text_%s_slider'%index)
        size = a[0].value()

        ##coordinate
        coor = self.plotarea.parentWidget().findChildren(QLineEdit, 'text_%s_coor'%index)

        ##vertical
        orientation = self.plotarea.parentWidget().findChildren(QSpinBox, 'text_%s_angle'%index)
        angle = orientation[0].value()

        p = self.changeleg(text)
        if p == 'nok':
            self.changeleg(self.ylabl.text())
            text = 'retry'
            self.changeylabl()
        else:
            self.changeleg(self.ylabl.text())

        try:
            coor = [float(i) for i in coor[0].text().split(',')]
            self.text = self.plot.text(coor[0], coor[1], text, fontsize = size, color = color, \
                    rotation=angle, zorder = zorder)
        except:
            self.text = self.plot.text(0.5, 0.5, text, fontsize = size, color = color, \
                    rotation=angle, zorder=zorder)
    
        ##refresh
        self.win.draw()

        ###save the plot in a dictionnary
        self.dico_widget['text_'+str(index)] = self.text


    def add_span(self, conf):
        '''
        This method adds widget for span strips (vertical or horizontal)
        '''

        if conf == 'fake':
            conf = {}
            conf['dir'] = 'Vertical'
            conf['color'] = 'black'
            conf['coor'] = '0.3, 0.7'
            conf['transparency'] = 90
            conf['zorder'] = '1'


        ##update index
        self.strip_index += 1


        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'Draw span'+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('stri_%s_separation'%self.strip_index)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        self.filX = QLabel('File:')
        self.plotarea.addWidget(self.filX, self.plot_index, 0, 1, 1)
        self.filX.setObjectName('stri_%s_filex'%self.strip_index)
        self.filX.setFont(myFont)



        #### a - direction
        self.direction = QComboBox(self)
        self.plotarea.addWidget(self.direction, self.plot_index, 0, 1, 1)
        for i in ['Vertical', 'Horizontal']:
            self.direction.addItem(i)
        index = numpy.where(numpy.array(['Vertical', 'Horizontal']) == conf['dir'])[0][0]
        self.direction.setObjectName("stri_%s_dir"%self.strip_index)
        self.direction.setCurrentIndex(index)
        self.direction.setToolTip(tooltips.direction_span())

        #### b- delete
        self.buttondel = QPushButton("Delete data")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.strip_index, 'stri'))
        self.buttondel.setObjectName('stri_%s_del'%self.strip_index)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### c - coordinates
        self.BG = QLabel('Coordinates')
        self.plotarea.addWidget(self.BG, self.plot_index, 0, 1, 1)
        self.BG.setObjectName("stri_%s_coorlab"%self.strip_index)
        self.BG.setFont(myFont)
        self.coor = QLineEdit()
        self.coor.setFont(myFont)
        self.plotarea.addWidget(self.coor, self.plot_index, 1, 1, 1)
        self.coor.setObjectName('stri_%s_coor'%self.strip_index)
        self.coor.setText(conf['coor'])
        self.widget_list.append(self.coor)
        self.coor.setToolTip(tooltips.coordinates_strip())
        self.plot_index += 1

        #### d - scrooling list color
        self.coll = QLabel('Color:')
        self.plotarea.addWidget(self.coll, self.plot_index, 0, 1, 1)
        self.coll.setObjectName("stri_%s_collab"%self.strip_index)
        self.coll.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.combocolor.setObjectName("stri_%s_color"%self.strip_index)
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1


        ### f - slider lw
        self.trans = QSlider(QtCore.Qt.Horizontal)
        self.trans.setMinimum(1)
        self.trans.setMaximum(100)
        self.trans.setValue(conf['transparency'])
        self.plotarea.addWidget(self.trans, self.plot_index, 0, 1, 2)
        self.trans.setObjectName("stri_%s_slider"%self.strip_index)
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('stri_%s_zorderlabel'%self.strip_index)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("stri_%s_zorder"%self.strip_index)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1


        self.make_strip(self.strip_index)

        #events
        self.direction.currentIndexChanged.connect(partial(self.make_strip, \
                self.strip_index))

        self.trans.valueChanged.connect(partial(self.make_strip, \
                self.strip_index))

        self.combocolor.currentIndexChanged.connect(partial(self.make_strip, \
                self.strip_index))

        self.coor.textChanged.connect(partial(self.make_strip, \
                self.strip_index))

        self.zorderedit.textChanged.connect(partial(self.make_strip, \
                self.scatterindex))


    def make_strip(self, index):
        '''
        This method add the straight line depending on the
        parameters given by the user in the widgets.
        '''

        ##check if this strip was already in place
        ##if yes, we remove it
        if 'stri_'+str(index) in self.dico_widget.keys():
            self.dico_widget['stri_'+str(index)].remove()
            self.win.draw()

        ###get direction
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'stri_%s_dir'%index)
        direction = a[0].currentText()

        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'stri_%s_color'%index)
        color = a[0].currentText()

        ##size
        a = self.plotarea.parentWidget().findChildren(QSlider, 'stri_%s_slider'%index)
        tr = a[0].value()/100.

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'stri_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = float(zorder) 
        except:
            zorder = 1


        ##coordinate
        coor = self.plotarea.parentWidget().findChildren(QLineEdit, 'stri_%s_coor'%index)

        try:
            coor = [float(i) for i in coor[0].text().split(',')]
            if direction == 'Vertical':
                self.span = self.plot.axvspan(coor[0], coor[1], ls='-', lw=0, alpha=tr, color=color, zorder = zorder)

            if direction == 'Horizontal':
                self.span = self.plot.axhspan(coor[0], coor[1], ls='-', lw=0, alpha=tr, color=color, zorder = zorder)

        except:
            self.span = self.plot.axvspan(1, 2, ls='-', lw=0, alpha=tr, color=color, zorder = zorder)
    
        ###adjust axis
        minx, maxx, miny, maxy = limits.get_axis_limits(self.loaded_plot, self) 
        self.plot.set_xlim(minx, maxx)
        self.plot.set_ylim(miny, maxy)

        ###save the plot in a dictionnary
        self.dico_widget['stri_'+str(index)] = self.span

        ##refresh
        self.win.draw()

    def add_straightline(self, conf):
        '''
        This method adds widget for straight line (vertical or horizontal)
        '''

        ##update index
        self.straight_index += 1

        if conf == 'fake':
            conf = {}
            conf['dir'] = 'Vertical'
            conf['color'] = 'black'
            conf['style'] = '-'
            conf['thickness'] = 10
            conf['coor'] = '0.5, 0.3,0.8'
            conf['zorder'] = '1'


        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'Segment '+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('stra_%s_separation'%self.straight_index)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        self.filX = QLabel('File:')
        self.plotarea.addWidget(self.filX, self.plot_index, 0, 1, 1)
        self.filX.setObjectName('stra_%s_filex'%self.straight_index)
        self.filX.setFont(myFont)

        #### a - direction
        self.direction = QComboBox(self)
        self.plotarea.addWidget(self.direction, self.plot_index, 0, 1, 1)
        for i in ['Vertical', 'Horizontal', 'Diagonal']:
            self.direction.addItem(i)
        index = numpy.where(numpy.array(['Vertical', 'Horizontal', 'Diagonal']) == conf['dir'])[0][0]
        self.direction.setObjectName("stra_%s_dir"%self.straight_index)
        self.direction.setCurrentIndex(index)
        self.direction.setToolTip(tooltips.direction())

        #### b- delete
        self.buttondel = QPushButton("Delete data")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.straight_index, 'stra'))
        self.buttondel.setObjectName('stra_%s_del'%self.straight_index)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### c - coordinates
        self.BG = QLabel('Coordinates')
        self.plotarea.addWidget(self.BG, self.plot_index, 0, 1, 1)
        self.BG.setObjectName("stra_%s_coorlab"%self.straight_index)
        self.BG.setFont(myFont)
        self.coor = QLineEdit()
        self.coor.setFont(myFont)
        self.plotarea.addWidget(self.coor, self.plot_index, 1, 1, 1)
        self.coor.setObjectName('stra_%s_coor'%self.straight_index)
        self.coor.setText(conf['coor'])
        self.widget_list.append(self.coor)
        self.coor.setToolTip(tooltips.coordinates())
        self.plot_index += 1

        #### d - scrooling list color
        self.coll = QLabel('Color:')
        self.plotarea.addWidget(self.coll, self.plot_index, 0, 1, 1)
        self.coll.setObjectName("stra_%s_collab"%self.straight_index)
        self.coll.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.combocolor.setObjectName("stra_%s_color"%self.straight_index)
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.lslab = QLabel('linestyle:')
        self.plotarea.addWidget(self.lslab, self.plot_index, 0, 1, 1)
        self.lslab.setObjectName("stra_%s_lslab"%self.straight_index)
        self.lslab.setFont(myFont)
        self.combols = QComboBox(self)
        for i in finalstyles:
            self.combols.addItem(str(i))
        index = numpy.where(finalstyles == conf['style'])[0][0]
        self.combols.setObjectName("stra_%s_ls"%self.straight_index)
        self.plotarea.addWidget(self.combols, self.plot_index, 1, 1, 1)
        self.combols.setCurrentIndex(index)
        self.plot_index += 1

        ### f - slider lw
        self.sliderline = QSlider(QtCore.Qt.Horizontal)
        self.sliderline.setMinimum(1)
        self.sliderline.setMaximum(100)
        self.sliderline.setValue(conf['thickness'])
        self.plotarea.addWidget(self.sliderline, self.plot_index, 0, 1, 2)
        self.sliderline.setObjectName("stra_%s_slider"%self.straight_index)
        self.sliderline.setToolTip(tooltips.slider_lw())
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('stra_%s_zorderlabel'%self.straight_index)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("stra_%s_zorder"%self.straight_index)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1


        ###load first plot
        self.make_straight(self.straight_index)

        #events
        self.direction.currentIndexChanged.connect(partial(self.make_straight, \
                self.straight_index))

        self.sliderline.valueChanged.connect(partial(self.make_straight, \
                self.straight_index))

        self.combocolor.currentIndexChanged.connect(partial(self.make_straight, \
                self.straight_index))

        self.combols.currentIndexChanged.connect(partial(self.make_straight, \
                self.straight_index))

        self.coor.textChanged.connect(partial(self.make_straight, \
                self.straight_index))

        self.zorderedit.textChanged.connect(partial(self.make_straight, \
                self.scatterindex))


    def make_straight(self, index):
        '''
        This method add the straight line depending on the
        parameters given by the user in the widgets.
        '''

        ##check if this hist plot was already in place
        ##if yes, we remove it
        if 'stra_'+str(index) in self.dico_widget.keys():
            self.dico_widget['stra_'+str(index)][0].remove()
            self.win.draw()

        ###get linestyle
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'stra_%s_ls'%index)
        linestyle = a[0].currentText()

        ###get direction
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'stra_%s_dir'%index)
        direction = a[0].currentText()

        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'stra_%s_color'%index)
        color = a[0].currentText()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'stra_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = float(zorder) 
        except:
            zorder = 1

        ##size
        a = self.plotarea.parentWidget().findChildren(QSlider, 'stra_%s_slider'%index)
        lw = a[0].value()/10.

        ##coordinate
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'stra_%s_coor'%index)
        if direction in ['Vertical', 'Horizontal']:
            try:
                coor = [float(i) for i in a[0].text().split(',')]
                if len(coor)!=3:
                    coor = [0.5, 0, 1]
            except:
                coor = [0,1,2] 
        else:
            try:
                coor = [float(i) for i in a[0].text().split(',')]

            except:
                coor = [0, 1]

        if direction == 'Vertical':
            #self.straight = self.plot.axvline(coor, ls=linestyle, lw=lw, color=color)
            xx = [coor[0],coor[0]]
            yy = [coor[1], coor[2]]
            self.straight = self.plot.plot(xx, yy, ls=linestyle, lw=lw, color=color, zorder = zorder)

        if direction == 'Horizontal':
            xx = [coor[1],coor[2]]
            yy = [coor[0], coor[0]] 
            self.straight = self.plot.plot(xx, yy, ls=linestyle, lw=lw, color=color, zorder = zorder)

        if direction == 'Diagonal':
            self.straight = self.plot.plot(coor, coor, \
                ls=linestyle, lw=lw, color=color, zorder = zorder)

        ###adjust axis
        minx, maxx, miny, maxy = limits.get_axis_limits(self.loaded_plot, self) 
        self.plot.set_xlim(minx, maxx)
        self.plot.set_ylim(miny, maxy)

        ###save the plot in a dictionnary
        self.dico_widget['stra_'+str(index)] = self.straight

        ##refresh
        self.win.draw()



    def add_hist(self, conf):
        '''
        This adds a line plot configuration to the plot area
        '''
        if isinstance(conf, str) is True:
            inputfile=conf
            conf = {}
            conf['file'] = inputfile
            conf['label'] = 'hist plot number %s'%(self.lineindex) 
            conf['style'] = '-'
            conf['color'] = 'black'
            conf['thickness'] = 10
            conf['transparency'] = 10
            conf['linestyle'] = '-'
            conf['histstyle'] = 'bar'
            conf['bin'] = '0.0, 1.0, 0.1'
            conf['norm'] = 'No'
            conf['zorder'] = '1'

        #Retrieve columns
        columns = numpy.array(extract.header(conf['file']))

        if 'x' not in conf.keys():
            conf['x'] = columns[0]
            conf['y'] = columns[0]


        ###upgrade index
        self.histindex += 1

        ###file
        self.labelfile = QLabel(conf['file'])
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('hist_%s_labelfile'%self.histindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1

        #### a- label
        self.label = QLineEdit()
        self.label.setFont(myFont)
        self.plotarea.addWidget(self.label, self.plot_index, 0, 1, 1)
        self.label.setObjectName('hist_%s_label'%self.histindex)
        self.label.setText(conf['label'])
        self.widget_list.append(self.label)
        self.label.setToolTip(tooltips.legend())

        #### b- plot!
        self.buttondel = QPushButton("Delete data")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.histindex, 'hist'))
        self.buttondel.setObjectName('hist_%s_del'%self.histindex)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### b - scrooling list X
        self.BG = QLabel('X:')
        self.plotarea.addWidget(self.BG, self.plot_index, 0, 1, 1)
        self.BG.setObjectName("hist_%s_Xlabel"%self.histindex)
        self.BG.setFont(myFont)
        self.comboX = QComboBox(self)
        self.plotarea.addWidget(self.comboX, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboX.addItem(columns[i])
        index = numpy.where(columns == conf['x'])[0][0]
        self.comboX.setObjectName("hist_%s_X"%self.histindex)
        self.widget_list.append(self.comboX)
        self.comboX.setCurrentIndex(index)
        self.plot_index += 1

        #### b- binning
        #### a- label
        self.b = QLabel('Binning')
        self.plotarea.addWidget(self.b, self.plot_index, 0, 1, 1)
        self.b.setObjectName("hist_%s_binlab"%self.histindex)
        self.b.setFont(myFont)
        self.bin = QLineEdit()
        self.bin.setFont(myFont)
        self.plotarea.addWidget(self.bin, self.plot_index, 1, 1, 1)
        self.bin.setObjectName('hist_%s_bin'%self.histindex)
        self.bin.setToolTip(tooltips.bin())
        self.bin.setText(conf['bin'])
        self.widget_list.append(self.bin)
        self.plot_index += 1


        #### c - scrooling list color
        self.coll = QLabel('Color:')
        self.plotarea.addWidget(self.coll, self.plot_index, 0, 1, 1)
        self.coll.setObjectName("hist_%s_collab"%self.histindex)
        self.coll.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.combocolor.setObjectName("hist_%s_color"%self.histindex)
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1

        #### d - scrooling list linestyle
        self.htlab = QLabel('hist type:')
        self.plotarea.addWidget(self.htlab, self.plot_index, 0, 1, 1)
        self.htlab.setObjectName("hist_%s_htlab"%self.histindex)
        self.htlab.setFont(myFont)
        self.combohs = QComboBox(self)
        finallist = numpy.array(['bar', 'barstacked', 'step', 'stepfilled'])
        for i in range(len(finallist)):
            self.combohs.addItem(str(finallist[i]))
        index = numpy.where(finallist == conf['histstyle'])[0][0]
        self.combohs.setObjectName("hist_%s_hs"%self.histindex)
        self.plotarea.addWidget(self.combohs, self.plot_index, 1, 1, 1)
        self.combohs.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.lslab = QLabel('linestyle:')
        self.plotarea.addWidget(self.lslab, self.plot_index, 0, 1, 1)
        self.lslab.setObjectName("hist_%s_lslab"%self.histindex)
        self.lslab.setFont(myFont)
        self.combols = QComboBox(self)
        for i in finalstyles:
            self.combols.addItem(str(i))
        index = numpy.where(finalstyles == conf['linestyle']) [0][0]
        self.combols.setObjectName("hist_%s_ls"%self.histindex)
        self.plotarea.addWidget(self.combols, self.plot_index, 1, 1, 1)
        self.combols.setCurrentIndex(index)
        self.plot_index += 1

        ### f - slider lw
        self.sliderhtr = QSlider(QtCore.Qt.Horizontal)
        self.sliderhtr.setMinimum(1)
        self.sliderhtr.setMaximum(10)
        self.sliderhtr.setValue(conf['transparency'])
        self.plotarea.addWidget(self.sliderhtr, self.plot_index, 0, 1, 2)
        self.sliderhtr.setObjectName("hist_%s_slider"%self.histindex)
        self.sliderhtr.setToolTip(tooltips.slider_tr())
        self.plot_index += 1

        ### g - slider lw
        self.sliderhlw = QSlider(QtCore.Qt.Horizontal)
        self.sliderhlw.setMinimum(0)
        self.sliderhlw.setMaximum(100)
        self.sliderhlw.setValue(conf['thickness'])
        self.plotarea.addWidget(self.sliderhlw, self.plot_index, 0, 1, 2)
        self.sliderhlw.setObjectName("hist_%s_sliderlw"%self.histindex)
        self.sliderhlw.setToolTip(tooltips.slider_lw())
        self.plot_index += 1

        ### h - Normalize
        self.norm = QCheckBox('Norm')
        if conf['norm'] == 'Yes':
            self.norm.setChecked(True)
        self.plotarea.addWidget(self.norm, self.plot_index, 0, 1, 1)
        self.norm.setFont(myFont)
        self.norm.setObjectName("hist_%s_norm"%self.histindex)
        self.norm.setToolTip(tooltips.hist_norm())
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('hist_%s_zorderlabel'%self.histindex)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("hist_%s_zorder"%self.histindex)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1


        ###load everything on plot
        self.make_histplot(self.histindex, conf['file'])

        ##events
        self.comboX.currentIndexChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.combocolor.currentIndexChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.label.textChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.bin.textChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.sliderhtr.valueChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.sliderhlw.valueChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.combols.currentIndexChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.combohs.currentIndexChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.norm.stateChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))

        self.zorderedit.textChanged.connect(partial(self.make_histplot, \
                self.histindex, conf['file']))



    def make_histplot(self, index, inputfile):
        '''
        This function make the line plot.
        '''
        ##check if this hist plot was already in place
        ##if yes, we remove it
        if 'hist_'+str(index) in self.dico_widget.keys():
            [b.remove() for b in self.dico_widget['hist_'+str(index)][2]]
            self.win.draw()

        ###get columns
        columns = extract.header(inputfile)


        ###get linestyle
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'hist_%s_ls'%index)
        linestyle = a[0].currentText()

        ###get histtype
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'hist_%s_hs'%index)
        histtype = a[0].currentText()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'hist_%s_label'%index)
        label = a[0].text()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'hist_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = float(zorder) 
        except:
            zorder = 1



        ###get binning
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'hist_%s_bin'%index)
        try:
            binning = [float(i) for i in a[0].text().split(',')]
            if binning[2] == 0 or (binning[0] == binning[1]) or (binning[0]>binning[1]):
                binning = [0.0, 1.0, 0.1]
        except:
            binning = [0.0, 1.0, 0.1]

        ###get X data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'hist_%s_X'%index)
        X = a[0].currentText()

        try:
            Xl = [float(i) for i in extract.column(X, columns, inputfile)]
        except:
            Xl = numpy.ones(len(extract.column(X, columns, inputfile)))
        

        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'hist_%s_color'%index)
        color = a[0].currentText()

        ##transparency
        a = self.plotarea.parentWidget().findChildren(QSlider, 'hist_%s_sliderlw'%index)
        lw = a[0].value()/10.

        ##size
        a = self.plotarea.parentWidget().findChildren(QSlider, 'hist_%s_slider'%index)
        tr = a[0].value()/10.



        ##norm
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'hist_%s_norm'%index)
        n = a[0].isChecked()

        ###add legend
        ###this is a quick and dirty trick to check if
        ###the mathText entry are ok
        p = self.changeleg(label)
        if p == 'nok':
            self.changeleg(self.ylabl.text())
            label = 'retry'
            self.changeylabl()
        else:
            self.changeleg(self.ylabl.text())

        ###remove possible infinite 
        inf = float('+inf')
        minf = float('-inf')
        Xl = numpy.array(Xl)
        boo = [Xl < inf]
        Xl = Xl[numpy.where(boo[0]==True)]
        boo = [Xl > minf]
        Xl = Xl[numpy.where(boo[0]==True)]


        ###and plot
        if n is True:
            weights = numpy.ones_like(Xl)/float(len(Xl))
            self.hist = self.plot.hist(Xl, bins=numpy.arange(binning[0], binning[1], binning[2]),\
                histtype=histtype, ls=linestyle, label=label, color=color, alpha=tr, weights=weights,\
                lw=lw, zorder = zorder)

        else:
            self.hist = self.plot.hist(Xl, bins=numpy.arange(binning[0], binning[1], binning[2]),\
                histtype=histtype, ls=linestyle, label=label, color=color, alpha=tr, lw=lw, zorder=zorder)


        ###set legend
        handles, labels = self.plot.get_legend_handles_labels()
        self.plot.legend(handles, labels)

        ###save the plot in a dictionnary
        self.dico_widget['hist_'+str(index)] = self.hist

        ###adjust axis
        minx, maxx, miny, maxy = limits.get_axis_limits(self.loaded_plot, self) 
        self.plot.set_xlim(minx, maxx)
        self.plot.set_ylim(miny, maxy)

        ###add legend
        handles, labels = self.plot.get_legend_handles_labels()
        self.plot.legend(handles, labels)

        ###tight layouts
        self.figure.tight_layout()

        ##redraw
        self.win.draw()

    def add_line(self, conf):
        '''
        This adds a line plot configuration to the plot area
        '''
            
        if isinstance(conf, str) is True:
            inputfile=conf
            conf = {}
            conf['file'] = inputfile
            conf['label'] = 'Line plot number %s'%(self.lineindex) 
            conf['style'] = '-'
            conf['color'] = 'black'
            conf['color_fb'] = '0.5'
            conf['thickness'] = 10
            conf['smooth'] = 0
            conf['fb'] = 'No'
            conf['bp'] = 'No'
            conf['zorder'] = '1'

        #Retrieve columns
        columns = numpy.array(extract.header(conf['file']))

        if 'x' not in conf.keys():
            conf['x'] = columns[0]
            conf['y'] = columns[0]
        
        ###upgrade index
        self.lineindex += 1

        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'Line plot'+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('line_%s_separation'%self.lineindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        self.filX = QLabel('File:')
        self.plotarea.addWidget(self.filX, self.plot_index, 0, 1, 1)
        self.filX.setObjectName('line_%s_filex'%self.lineindex)
        self.filX.setFont(myFont)

        ###file
        self.labelfile = QLabel('%s'%conf['file'])
        self.plotarea.addWidget(self.labelfile, self.plot_index, 1, 1, 2)
        self.labelfile.setObjectName('line_%s_labelfile'%self.lineindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1

        #### a- label
        self.label = QLineEdit()
        self.label.setFont(myFont)
        self.plotarea.addWidget(self.label, self.plot_index, 0, 1, 1)
        self.label.setObjectName('line_%s_label'%self.lineindex)
        self.label.setText(conf['label'])
        self.label.setToolTip(tooltips.legend())

        #### b- plot!
        self.buttondel = QPushButton("Delete data")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.lineindex, 'line'))
        self.buttondel.setObjectName('line_%s_del'%self.lineindex)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### b - scrooling list X
        ####label
        self.labelX = QLabel('X:')
        self.plotarea.addWidget(self.labelX, self.plot_index, 0, 1, 1)
        self.labelX.setObjectName('line_%s_xlabel'%self.lineindex)
        self.labelX.setFont(myFont)
        self.comboX = QComboBox(self)
        self.plotarea.addWidget(self.comboX, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboX.addItem(columns[i])
        index = numpy.where(columns == conf['x'])[0][0]
        self.comboX.setObjectName("line_%s_X"%self.lineindex)
        self.comboX.setCurrentIndex(index)
        self.plot_index += 1

        #### c - scrooling list X
        self.labelY = QLabel('Y:')
        self.plotarea.addWidget(self.labelY, self.plot_index, 0, 1, 1)
        self.labelY.setObjectName('line_%s_ylabel'%self.lineindex)
        self.labelY.setFont(myFont)
        self.comboY = QComboBox(self)
        self.plotarea.addWidget(self.comboY, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboY.addItem(columns[i])
        index = numpy.where(columns == conf['y'])[0][0]
        self.comboY.setObjectName("line_%s_Y"%self.lineindex)
        self.comboY.setCurrentIndex(index)
        self.plot_index += 1

        #### d - scrooling list color
        self.lcol = QLabel('Color:')
        self.plotarea.addWidget(self.lcol, self.plot_index, 0, 1, 1)
        self.lcol.setObjectName('line_%s_lcol'%self.lineindex)
        self.lcol.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        self.combocolor.setObjectName("line_%s_color"%self.lineindex)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.lslab = QLabel('linestyle:')
        self.plotarea.addWidget(self.lslab, self.plot_index, 0, 1, 1)
        self.lslab.setObjectName('line_%s_lslab'%self.lineindex)
        self.lslab.setFont(myFont)
        self.combols = QComboBox(self)
        for i in finalstyles:
            self.combols.addItem(str(i))
        self.combols.setObjectName("line_%s_style"%self.lineindex)
        index = numpy.where(finalstyles == conf['style'])[0][0]
        self.combols.setCurrentIndex(index)
        self.plotarea.addWidget(self.combols, self.plot_index, 1, 1, 1)
        self.plot_index += 1

        ### f - slider lw
        self.sliderline = QSlider(QtCore.Qt.Horizontal)
        self.sliderline.setMinimum(1)
        self.sliderline.setMaximum(30)
        self.sliderline.setValue(int(conf['thickness']))
        self.plotarea.addWidget(self.sliderline, self.plot_index, 0, 1, 2)
        self.sliderline.setObjectName("line_%s_slider"%self.lineindex)
        self.sliderline.setToolTip(tooltips.slider_lw())
        self.plot_index += 1

        ### g - fill_between
        self.fib = QCheckBox('fill_between')
        if conf['fb'] == 'Yes':
            self.fib.setChecked(True)
        self.plotarea.addWidget(self.fib, self.plot_index, 0, 1, 1)
        self.fib.setFont(myFont)
        self.fib.setObjectName("line_%s_fb"%self.lineindex)
        self.fib.setToolTip(tooltips.fill())

        #### h - scrooling list color
        self.combocolor_fb = QComboBox(self)
        self.plotarea.addWidget(self.combocolor_fb, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor_fb.addItem(i)
        index = numpy.where(allcolors == conf['color_fb'])[0][0]
        self.combocolor_fb.setObjectName("line_%s_color_fb"%self.lineindex)
        self.combocolor_fb.setCurrentIndex(index)
        self.plot_index += 1

        ### g - barplot
        self.bp = QCheckBox('barplot')
        if conf['bp'] == 'Yes':
            self.bp.setChecked(True)
        self.plotarea.addWidget(self.bp, self.plot_index, 0, 1, 1)
        self.bp.setFont(myFont)
        self.bp.setObjectName("line_%s_bp"%self.lineindex)
        self.bp.setToolTip(tooltips.barplot())

        ### h - smooth
        self.smoothsb = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.smoothsb, self.plot_index, 1, 1, 1)
        self.smoothsb.setMinimum(0)
        self.smoothsb.setMaximum(10000)
        self.smoothsb.setValue(int(conf['smooth']))
        self.smoothsb.setToolTip(tooltips.gauss())
        self.smoothsb.setObjectName("line_%s_sb"%self.lineindex)
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('line_%s_zorderlabel'%self.lineindex)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("line_%s_zorder"%self.lineindex)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1

        ##events
        self.comboY.currentIndexChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.comboX.currentIndexChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.combols.currentIndexChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.combocolor.currentIndexChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.combocolor_fb.currentIndexChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.label.textChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.zorderedit.textChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.sliderline.valueChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.fib.stateChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))

        self.bp.stateChanged.connect(partial(self.make_lineplot, \
                self.lineindex, conf['file']))
        
        self.smoothsb.valueChanged.connect(partial(self.make_lineplot, self.lineindex, conf['file']))

        self.make_lineplot(self.lineindex, conf['file'])

    def make_lineplot(self, index, inputfile):
        '''
        This function make the line plot.
        '''
        ##check if this line plot was already in place
        ##if yes, we remove it
        if 'line_'+str(index) in self.dico_widget.keys():
            self.dico_widget['line_'+str(index)][0].remove()
            self.win.draw()


        ###get columns
        columns = extract.header(inputfile)

        ###get linestyle
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'line_%s_style'%index)
        linestyle = a[0].currentText()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'line_%s_label'%index)
        label = a[0].text()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'line_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = int(zorder)
        except:
            zorder=0

        ###get X data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'line_%s_X'%index)
        X = a[0].currentText()
        try:
            Xl = [float(i) for i in extract.column(X, columns, inputfile)]
        except:
            Xl = numpy.ones(len(extract.column(X, columns, inputfile)))

        ###get Y data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'line_%s_Y'%index)
        Y = a[0].currentText()
        try:
            Yl = [float(i) for i in extract.column(Y, columns, inputfile)]
        except:
            Yl = numpy.ones(len(extract.column(Y, columns, inputfile)))
        
        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'line_%s_color'%index)
        color = a[0].currentText()

        ###get color fb
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'line_%s_color_fb'%index)
        color_fb = a[0].currentText()

        ##size
        a = self.plotarea.parentWidget().findChildren(QSlider, 'line_%s_slider'%index)
        linewidth = a[0].value()/10.

        ##fill between
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'line_%s_fb'%index)
        fb = a[0].isChecked()

        ##barplot
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'line_%s_bp'%index)
        bp = a[0].isChecked()

        ##get smooth value
        smooth = self.plotarea.parentWidget().findChildren(QSpinBox, 'line_%s_sb'%index)
        sm = smooth[0].value()/10

        ###smooth
        if sm!=0:
            new_Xl = numpy.arange(Xl[0], Xl[-1], 1)
            new_Yl = numpy.interp(new_Xl, Xl, Yl)
            smoothed = gaussian_filter(new_Yl, sm)
            Xl = new_Xl
        else:
            smoothed = Yl

        ###plot
        if bp is True:
            newX, newY = barplot.create_barplot(Xl, smoothed)
            self.line = self.plot.plot(newX, newY, ls=linestyle, color=color, \
                    lw=linewidth, label=label, zorder = zorder)
        else:
            self.line = self.plot.plot(Xl, smoothed, \
                    ls=linestyle, color=color, lw=linewidth, label=label, zorder = zorder)

        ##fill between
        if fb is True:
            if 'fb_'+str(index) in self.dico_widget.keys():
                self.dico_widget['fb_'+str(index)].remove()
                del self.dico_widget['fb_'+str(index)]

            self.fb = self.plot.fill_between(Xl, 0, smoothed, lw=0, color=color_fb, zorder=zorder)
            self.dico_widget['fb_'+str(index)] = self.fb

        if fb is False:
            if 'fb_'+str(index) in self.dico_widget.keys():
                self.dico_widget['fb_'+str(index)].remove()
                del self.dico_widget['fb_'+str(index)]

        ###save the plot in a dictionnary
        self.dico_widget['line_'+str(index)] = self.line

        ###add legend
        ###this is a quick and dirty trick to check if
        ###the mathText entry are ok
        labl = self.line[0].get_label()
        p = self.changeleg(labl)
        if p == 'nok':
            self.changeleg(self.ylabl.text())
            self.line[0].set_label('retry')
            self.changeylabl()
        else:
            self.changeleg(self.ylabl.text())

        handles, labels = self.plot.get_legend_handles_labels()
        self.plot.legend(handles, labels)

        ###adjust axis
        minx, maxx, miny, maxy = limits.get_axis_limits(self.loaded_plot, self) 
        self.plot.set_xlim(minx, maxx)
        self.plot.set_ylim(miny, maxy)

        ###tight layouts
        self.figure.tight_layout()

        ##redraw
        self.win.draw()


    def add_scatter(self, conf):
        '''
        This adds a scatter plot configuration to the plot area
        '''
        if isinstance(conf, str) is True:
            inputfile=conf
            conf = {}
            conf['file'] = inputfile
            conf['label'] = 'Line plot number %s'%(self.lineindex) 
            conf['style'] = '-'
            conf['color'] = 'black'
            conf['thickness'] = 10
            conf['transparency'] = 10
            conf['empty'] = 'No'
            conf['size'] = 100
            conf['marker'] = '.'
            conf['zorder'] = '1'

        #Retrieve columns
        columns = numpy.array(extract.header(conf['file']))

        if 'x' not in conf.keys():
            conf['x'] = columns[0]
            conf['y'] = columns[0]

        ###upgrade index
        self.scatterindex += 1

        #### 0 - separation
        self.labelfile = QLabel(20*'-'+'Scatter plot'+20*'-')
        self.plotarea.addWidget(self.labelfile, self.plot_index, 0, 1, 2)
        self.labelfile.setObjectName('scat_%s_separation'%self.scatterindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1
        
        self.filX = QLabel('File:')
        self.plotarea.addWidget(self.filX, self.plot_index, 0, 1, 1)
        self.filX.setObjectName('scat_%s_filex'%self.scatterindex)
        self.filX.setFont(myFont)

        #### c - scrooling list X
        self.labelfile = QLabel(conf['file'])
        self.plotarea.addWidget(self.labelfile, self.plot_index, 1, 1, 2)
        self.labelfile.setObjectName('scat_%s_labelfile'%self.scatterindex)
        self.labelfile.setFont(myFont)
        self.plot_index += 1

        #### a- label
        self.label = QLineEdit()
        self.label.setFont(myFont)
        self.plotarea.addWidget(self.label, self.plot_index, 0, 1, 1)
        self.label.setObjectName('scat_%s_label'%self.scatterindex)
        self.label.setText(conf['label'])
        self.label.setToolTip(tooltips.legend())


        #### b- plot!
        self.buttondel = QPushButton("Delete data")
        self.plotarea.addWidget(self.buttondel, self.plot_index, 1, 1, 1)
        self.buttondel.clicked.connect(partial(self.delete_widget, self.scatterindex, 'scat'))
        self.buttondel.setObjectName('scat_%s_del'%self.scatterindex)
        self.buttondel.setToolTip(tooltips.delete_plot())
        self.plot_index += 1

        #### b - scrooling list X
        ####label
        self.labelX = QLabel('X:')
        self.plotarea.addWidget(self.labelX, self.plot_index, 0, 1, 1)
        self.labelX.setObjectName('scat_%s_labelx'%self.scatterindex)
        self.labelX.setFont(myFont)
        self.comboX = QComboBox(self)
        self.plotarea.addWidget(self.comboX, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboX.addItem(columns[i])
        index = numpy.where(columns == conf['x'])[0][0]
        self.comboX.setCurrentIndex(index)
        self.comboX.setObjectName("scat_%s_X"%self.scatterindex)
        self.plot_index += 1

        #### c - scrooling list X
        self.labelY = QLabel('Y:')
        self.plotarea.addWidget(self.labelY, self.plot_index, 0, 1, 1)
        self.labelY.setObjectName('scat_%s_labely'%self.scatterindex)
        self.labelY.setFont(myFont)
        self.comboY = QComboBox(self)
        self.plotarea.addWidget(self.comboY, self.plot_index, 1, 1, 1)
        for i in range(len(columns)):
            self.comboY.addItem(columns[i])
        index = numpy.where(columns == conf['y'])[0][0]
        self.comboY.setCurrentIndex(index)
        self.comboY.setObjectName("scat_%s_Y"%self.scatterindex)
        self.plot_index += 1

        #### d - scrooling list color
        self.scatcol = QLabel('Color:')
        self.plotarea.addWidget(self.scatcol, self.plot_index, 0, 1, 1)
        self.scatcol.setObjectName('scat_%s_col'%self.scatterindex)
        self.scatcol.setFont(myFont)
        self.combocolor = QComboBox(self)
        self.plotarea.addWidget(self.combocolor, self.plot_index, 1, 1, 1)
        for i in allcolors:
            self.combocolor.addItem(i)
        index = numpy.where(allcolors == conf['color'])[0][0]
        self.combocolor.setObjectName("scat_%s_color"%self.scatterindex)
        self.combocolor.setCurrentIndex(index)
        self.plot_index += 1

        #### e - scrooling list markers
        self.markerlab = QLabel('Marker:')
        self.plotarea.addWidget(self.markerlab, self.plot_index, 0, 1, 1)
        self.markerlab.setObjectName('scat_%s_mlab'%self.scatterindex)
        self.markerlab.setFont(myFont)
        self.combomarkers = QComboBox(self)
        for i in finalmarkers:
            self.combomarkers.addItem(str(i))
        index = numpy.where(finalmarkers == conf['marker'])[0][0]
        self.combomarkers.setObjectName("scat_%s_marker"%self.scatterindex)
        self.combomarkers.setCurrentIndex(index)
        self.plotarea.addWidget(self.combomarkers, self.plot_index, 1, 1, 1)
        self.plot_index += 1

        #### f - marker_width
        self.slab = QLabel('Size:')
        self.plotarea.addWidget(self.slab, self.plot_index, 0, 1, 1)
        self.slab.setObjectName('scat_%s_slab'%self.scatterindex)
        self.slab.setFont(myFont)

        self.scatsize = QSpinBox()  ##spinbox linewidth
        self.plotarea.addWidget(self.scatsize, self.plot_index, 1, 1, 1)
        self.scatsize.setMinimum(0)
        self.scatsize.setMaximum(500)
        self.scatsize.setValue(int(conf['size'])) ###set default
        self.scatsize.setObjectName("scat_%s_size"%self.scatterindex)
        self.plot_index += 1

        #### g - empty marker
        self.empty = QCheckBox('Empty marker')
        if conf['empty'] == 'Yes':
            self.empty.setChecked(True)
        self.plotarea.addWidget(self.empty, self.plot_index, 0, 1, 1)
        self.empty.setFont(myFont)
        self.empty.setObjectName("scat_%s_empty"%self.scatterindex)
        self.empty.setToolTip(tooltips.empty())
        self.plot_index += 1

        ### h - slider lw
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setValue(int(conf['thickness']))
        self.plotarea.addWidget(self.slider, self.plot_index, 0, 1, 2)
        self.slider.setObjectName("scat_%s_slider"%self.scatterindex)
        self.slider.setToolTip(tooltips.slider_lw())
        self.plot_index += 1

        ### i - slider transparency
        self.slidertr = QSlider(QtCore.Qt.Horizontal)
        self.slidertr.setMinimum(1)
        self.slidertr.setMaximum(10)
        self.slidertr.setValue(int(conf['transparency']))
        self.plotarea.addWidget(self.slidertr, self.plot_index, 0, 1, 2)
        self.slidertr.setObjectName("scat_%s_tr"%self.scatterindex)
        self.slidertr.setToolTip(tooltips.slider_tr())
        self.plot_index += 1

        #### e - scrooling list linestyle
        self.zorder = QLabel('Zorder:')
        self.plotarea.addWidget(self.zorder, self.plot_index, 0, 1, 1)
        self.zorder.setObjectName('scat_%s_zorderlabel'%self.scatterindex)
        self.zorder.setFont(myFont)
        self.zorderedit = QLineEdit(self)
        self.zorderedit.setObjectName("scat_%s_zorder"%self.scatterindex)
        self.zorderedit.setText(conf['zorder'])
        self.plotarea.addWidget(self.zorderedit, self.plot_index, 1, 1, 1)
        self.zorderedit.setToolTip(tooltips.zorder())
        self.plot_index += 1



        ##events
        self.comboY.currentIndexChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.comboX.currentIndexChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.scatsize.valueChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.combomarkers.currentIndexChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.combocolor.currentIndexChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.label.textChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.zorderedit.textChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.empty.stateChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.slider.valueChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.slidertr.valueChanged.connect(partial(self.make_scatplot, \
                self.scatterindex, conf['file']))

        self.make_scatplot(self.scatterindex, conf['file'])

    def make_scatplot(self, index, inputfile):
        '''
        This function make the scatter plot.
        we take as X, self.Xv, and a label of self.X
                as Y, self.Yv, and a labal of self.Y
        '''
        ##check if this scatter plot was already in place
        ##if yes, we remove it
        if 'scat_'+str(index) in self.dico_widget.keys():
            self.dico_widget['scat_'+str(index)].remove()
            self.win.draw()

        ###get columns
        columns = extract.header(inputfile)

        ###get marker
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'scat_%s_marker'%index)
        marker = a[0].currentText()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'scat_%s_label'%index)
        label = a[0].text()

        ###get label
        a = self.plotarea.parentWidget().findChildren(QLineEdit, 'scat_%s_zorder'%index)
        zorder = a[0].text()
        try:
            zorder = float(zorder) 
        except:
            zorder = 1

        ###get X data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'scat_%s_X'%index)
        X = a[0].currentText()
        try:
            Xl = [float(i) for i in extract.column(X, columns, inputfile)]
        except:
            Xl = numpy.ones(len(extract.column(X, columns, inputfile)))

        ###get Y data
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'scat_%s_Y'%index)
        Y = a[0].currentText()
        try:
            Yl = [float(i) for i in extract.column(Y, columns, inputfile)]
        except: 
            Yl = numpy.ones(len(extract.column(Y, columns, inputfile)))

        ###get color
        a = self.plotarea.parentWidget().findChildren(QComboBox, 'scat_%s_color'%index)
        color = a[0].currentText()

        ##size
        a = self.plotarea.parentWidget().findChildren(QSpinBox, 'scat_%s_size'%index)
        size = a[0].value()

        ##checkbox
        a = self.plotarea.parentWidget().findChildren(QCheckBox, 'scat_%s_empty'%index)
        empty = a[0].isChecked()

        ##lw
        a = self.plotarea.parentWidget().findChildren(QSlider, 'scat_%s_slider'%index)
        lw = a[0].value()/10

        #tr
        a = self.plotarea.parentWidget().findChildren(QSlider, 'scat_%s_tr'%index)
        tr = a[0].value()/10


        ###plot
        if empty is True:
            self.scatter = self.plot.scatter(Xl, Yl, marker=marker, \
                color=color, s=size, label=r'%s'%label, facecolor='none', lw=lw, alpha=tr, zorder = zorder)

        else:
            self.scatter = self.plot.scatter(Xl, Yl, marker=marker, \
                color=color, s=size, label=r'%s'%label, lw=lw, alpha=tr, zorder = zorder)

        ###save the plot in a dictionnary
        self.dico_widget['scat_'+str(index)] = self.scatter

        ###add legend
        ###this is a quick and dirty trick to check if
        ###the mathText entry are ok
        labl = self.scatter.get_label()
        p = self.changeleg(labl)
        if p == 'nok':
            self.changeleg(self.ylabl.text())
            self.scatter.set_label('retry')
            self.changeylabl()
        else:
            self.changeleg(self.ylabl.text())

        ###add legend
        handles, labels = self.plot.get_legend_handles_labels()
        self.plot.legend(handles, labels)

        ###adjust axis
        minx, maxx, miny, maxy = limits.get_axis_limits(self.loaded_plot, self) 
        self.plot.set_xlim(minx, maxx)
        self.plot.set_ylim(miny, maxy)

        ###tight layouts
        self.figure.tight_layout()

        ##redraw
        self.win.draw()

    def delete_widget(self, index, typeplot):
        '''
        This removes all the widgets of a given index
        and type of plot
        '''
        ###line edits
        w = self.plotarea.parentWidget().findChildren(QLineEdit)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()
        ##combobox
        w = self.plotarea.parentWidget().findChildren(QComboBox)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()

        ##Qlabel
        w = self.plotarea.parentWidget().findChildren(QLabel)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()

        ##QSpinBox
        w = self.plotarea.parentWidget().findChildren(QSpinBox)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()

        ##QSlider
        w = self.plotarea.parentWidget().findChildren(QSlider)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()

        ##QPushButton
        w = self.plotarea.parentWidget().findChildren(QPushButton)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()

        ##QCheckBox
        w = self.plotarea.parentWidget().findChildren(QCheckBox)
        for i in w:
            if i.objectName()[:6] == '%s_%s'%(typeplot, index):
                i.deleteLater()

        ###and remove plot
        if typeplot == 'hist':
            if 'hist_'+str(index) in self.dico_widget.keys():
                a = [b.remove() for b in self.dico_widget['hist_'+str(index)][2]]
                self.win.draw()

        if typeplot == 'line':
            if 'line_'+str(index) in self.dico_widget.keys():
                self.dico_widget['line_'+str(index)][0].remove()
                self.win.draw()

        if typeplot == 'stra':
            if 'stra_'+str(index) in self.dico_widget.keys():
                self.dico_widget['stra_'+str(index)][0].remove()
                self.win.draw()

        if typeplot == 'scat':
            if 'scat_'+str(index) in self.dico_widget.keys():
                self.dico_widget['scat_'+str(index)].remove()
                self.win.draw()

        if typeplot == 'stri':
            if 'stri_'+str(index) in self.dico_widget.keys():
                self.dico_widget['stri_'+str(index)].remove()
                self.win.draw()

        if typeplot == 'text':
            if 'text_'+str(index) in self.dico_widget.keys():
                self.dico_widget['text_'+str(index)].remove()
                self.win.draw()

        if typeplot == 'erro':
            if 'erro_'+str(index) in self.dico_widget.keys():
                self.dico_widget['erro_'+str(index)].remove()
                self.dico_widget['erro_'+str(index)]._label = ''
                self.win.draw()


