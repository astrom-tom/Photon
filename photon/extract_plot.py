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
import sys



class loadplot(object):

    def __init__(self, config):
        '''
        Class constructor
        '''
        ###create the configuration object
        conf = configparser.ConfigParser()
        conf.read(config)


        self.plotconf = {}

        ####read the first (mandatory section)
        TYPES = {}
        TYPES['line'] = conf.getint('Types', 'line')
        TYPES['scatter'] = conf.getint('Types', 'scatter')
        TYPES['scatter_CB'] = conf.getint('Types', 'scatter_cb')
        TYPES['error'] = conf.getint('Types', 'error')
        TYPES['text'] = conf.getint('Types', 'text')
        TYPES['segments'] = conf.getint('Types', 'segments')
        TYPES['image'] = conf.getint('Types', 'image')
        TYPES['diag'] = conf.getint('Types', 'diag')
        TYPES['hist'] = conf.getint('Types', 'hist')
        TYPES['strip'] = conf.getint('Types', 'strip')
        TYPES['band'] = conf.getint('Types', 'band')
        TYPES['xmin'] = conf.get('Types', 'xmin')
        TYPES['xmax'] = conf.get('Types', 'xmax')
        TYPES['ymin'] = conf.get('Types', 'ymin')
        TYPES['ymax'] = conf.get('Types', 'ymax')
        TYPES['xlabel'] = conf.get('Types', 'x_label')
        TYPES['ylabel'] = conf.get('Types', 'y_label')

        self.plotconf['types'] = TYPES

        ###retrieve each plot conf
        for i in range(TYPES['line']):
            self.get_line_conf(conf, i+1)

        for i in range(TYPES['scatter']):
            self.get_scat_conf(conf, i+1)

        for i in range(TYPES['scatter_CB']):
            self.get_scatcb_conf(conf, i+1)

        for i in range(TYPES['text']):
            self.get_text_conf(conf, i+1)
        
        for i in range(TYPES['segments']):
            self.get_stra_conf(conf, i+1)
        
        for i in range(TYPES['strip']):
            self.get_stri_conf(conf, i+1)

        for i in range(TYPES['hist']):
            self.get_hist_conf(conf, i+1)
            
        for i in range(TYPES['error']):
            self.get_err_conf(conf, i+1)
        
        for i in range(TYPES['image']):
            self.get_imag_conf(conf, i+1)
        
        for i in range(TYPES['band']):
            self.get_band_conf(conf, i+1)
 
    def get_line_conf(self, conf, n):
        '''
        get the configuration the for the line plots number n
        '''
        LINE = {}
        LINE['file'] = conf.get('line_%s'%n, 'file')
        LINE['label'] = conf.get('line_%s'%n, 'label')
        LINE['x'] = conf.get('line_%s'%n, 'x')
        LINE['y'] = conf.get('line_%s'%n, 'y')
        LINE['color'] = conf.get('line_%s'%n, 'color')
        LINE['style'] = conf.get('line_%s'%n, 'style')
        LINE['color_fb'] = conf.get('line_%s'%n, 'color_fb')
        LINE['thickness'] = conf.get('line_%s'%n, 'thickness')
        LINE['fb'] = conf.get('line_%s'%n, 'fb')
        LINE['bp'] = conf.get('line_%s'%n, 'bp')
        LINE['smooth'] = conf.get('line_%s'%n, 'smooth')
        LINE['zorder'] = conf.get('line_%s'%n, 'zorder')
        self.plotconf['Line_%s'%n] = LINE

    def get_band_conf(self, conf, n):
        '''
        get the configuration the for the scatter plots number n
        '''
        BAND = {}
        BAND['file'] = conf.get('band_%s'%n, 'file')
        BAND['label'] = conf.get('band_%s'%n, 'label')
        BAND['x'] = conf.get('band_%s'%n, 'x')
        BAND['y1'] = conf.get('band_%s'%n, 'y1')
        BAND['y2'] = conf.get('band_%s'%n, 'y2')
        BAND['color'] = conf.get('band_%s'%n, 'color')
        #BAND['hatch'] = conf.get('band_%s'%n, 'hatch')
        BAND['zorder'] = conf.get('band_%s'%n, 'zorder')
        self.plotconf['Band_%s'%n] = BAND

    def get_scat_conf(self, conf, n):
        '''
        get the configuration the for the scatter plots number n
        '''
        SCAT = {}
        SCAT['file'] = conf.get('scat_%s'%n, 'file')
        SCAT['label'] = conf.get('scat_%s'%n, 'label')
        SCAT['x'] = conf.get('scat_%s'%n, 'x')
        SCAT['y'] = conf.get('scat_%s'%n, 'y')
        SCAT['color'] = conf.get('scat_%s'%n, 'color')
        SCAT['marker'] = conf.get('scat_%s'%n, 'marker')
        SCAT['thickness'] = conf.get('scat_%s'%n, 'thickness')
        SCAT['empty'] = conf.get('scat_%s'%n, 'empty')
        SCAT['transparency'] = conf.get('scat_%s'%n, 'transparency')
        SCAT['size'] = conf.getint('scat_%s'%n, 'size')
        SCAT['zorder'] = conf.get('scat_%s'%n, 'zorder')
        self.plotconf['Scat_%s'%n] = SCAT

    def get_scatcb_conf(self, conf, n):
        '''
        get the configuration the for the scatter plots number n
        '''
        SCATCB = {}
        SCATCB['file'] = conf.get('sccb_%s'%n, 'file')
        SCATCB['label'] = conf.get('sccb_%s'%n, 'label')
        SCATCB['labelcb'] = conf.get('sccb_%s'%n, 'labelcb')
        SCATCB['x'] = conf.get('sccb_%s'%n, 'x')
        SCATCB['y'] = conf.get('sccb_%s'%n, 'y')
        SCATCB['z'] = conf.get('sccb_%s'%n, 'z')
        SCATCB['colormap'] = conf.get('sccb_%s'%n, 'colormap')
        SCATCB['marker'] = conf.get('sccb_%s'%n, 'marker')
        SCATCB['thickness'] = conf.get('sccb_%s'%n, 'thickness')
        SCATCB['empty'] = conf.get('sccb_%s'%n, 'empty')
        SCATCB['transparency'] = conf.get('sccb_%s'%n, 'transparency')
        SCATCB['size'] = conf.getint('sccb_%s'%n, 'size')
        SCATCB['vmin'] = conf.get('sccb_%s'%n, 'vmin')
        SCATCB['vmax'] = conf.get('sccb_%s'%n, 'vmax')
        SCATCB['zorder'] = conf.get('sccb_%s'%n, 'zorder')
        SCATCB['fontlabel'] = conf.get('sccb_%s'%n, 'fontlabel')
        SCATCB['fonttickslabel'] = conf.get('sccb_%s'%n, 'fonttickslabel')
        SCATCB['Labelsize'] = conf.getint('sccb_%s'%n, 'Labelsize')
        SCATCB['tickLabelsize'] = conf.getint('sccb_%s'%n, 'tickLabelsize')
        SCATCB['labelpad'] = conf.get('sccb_%s'%n, 'labelpad')

        self.plotconf['sccb_%s'%n] = SCATCB

    def get_err_conf(self, conf, n):
        '''
        get the configuration the for the scatter plots number n
        '''
        ERR = {}
        ERR['file'] = conf.get('erro_%s'%n, 'file')
        ERR['label'] = conf.get('erro_%s'%n, 'label')

        ERR['x'] = conf.get('erro_%s'%n, 'x')
        ERR['xerrp'] = conf.get('erro_%s'%n, 'xerrp')
        ERR['xerrm'] = conf.get('erro_%s'%n, 'xerrm')
        ERR['y'] = conf.get('erro_%s'%n, 'y')
        ERR['yerrp'] = conf.get('erro_%s'%n, 'yerrp')
        ERR['yerrm'] = conf.get('erro_%s'%n, 'yerrm')

        ERR['color'] = conf.get('erro_%s'%n, 'color')
        ERR['marker'] = conf.get('erro_%s'%n, 'marker')
        ERR['empty'] = conf.get('erro_%s'%n, 'empty')

        ERR['transparency'] = conf.getint('erro_%s'%n, 'transparency')
        ERR['size'] = conf.getint('erro_%s'%n, 'size')
        ERR['capsize'] = conf.getint('erro_%s'%n, 'capsize')
        ERR['barsize'] = conf.getint('erro_%s'%n, 'barsize')
        ERR['zorder'] = conf.get('erro_%s'%n, 'zorder')
        self.plotconf['Erro_%s'%n] = ERR



    def get_hist_conf(self, conf, n):
        '''
        get the configuration the for the scatter plots number n
        '''
        HIST = {}
        HIST['file'] = conf.get('hist_%s'%n, 'file')
        HIST['label'] = conf.get('hist_%s'%n, 'label')
        HIST['x'] = conf.get('hist_%s'%n, 'x')
        HIST['color'] = conf.get('hist_%s'%n, 'color')
        HIST['linestyle'] = conf.get('hist_%s'%n, 'linestyle')
        HIST['histstyle'] = conf.get('hist_%s'%n, 'histstyle')
        HIST['thickness'] = conf.getint('hist_%s'%n, 'thickness')
        HIST['bin'] = conf.get('hist_%s'%n, 'bin')
        HIST['transparency'] = conf.getint('hist_%s'%n, 'transparency')
        HIST['norm'] = conf.get('hist_%s'%n, 'norm')
        HIST['zorder'] = conf.get('hist_%s'%n, 'zorder')
        self.plotconf['Hist_%s'%n] = HIST

    def get_text_conf(self, conf, n):
        '''
        get the configuration for the text number n
        '''
        TEXT = {}
        TEXT['text'] = conf.get('text_%s'%n, 'text') 
        TEXT['coor'] = conf.get('text_%s'%n, 'coor') 
        TEXT['color'] = conf.get('text_%s'%n, 'color') 
        TEXT['angle'] = conf.getint('text_%s'%n, 'angle') 
        TEXT['size'] = conf.getint('text_%s'%n, 'size') 
        TEXT['zorder'] = conf.get('text_%s'%n, 'zorder')
        self.plotconf['Text_%s'%n] = TEXT

    def get_stra_conf(self, conf, n):
        '''
        get the configuration for the straight line number n
        '''

        Stra = {}
        Stra['dir'] = conf.get('stra_%s'%n, 'dir')
        Stra['color'] = conf.get('stra_%s'%n, 'color')
        Stra['style'] = conf.get('stra_%s'%n, 'style')
        Stra['thickness'] = conf.getint('stra_%s'%n, 'thickness')
        Stra['coor'] = conf.get('stra_%s'%n, 'coor')
        Stra['zorder'] = conf.get('stra_%s'%n, 'zorder')
        self.plotconf['Stra_%s'%n] = Stra

    def get_stri_conf(self, conf, n):
        '''
        get the configuration for the straight line number n
        '''
        Stri = {}
        Stri['dir'] = conf.get('stri_%s'%n, 'dir')
        Stri['color'] = conf.get('stri_%s'%n, 'color')
        Stri['transparency'] = conf.getint('stri_%s'%n, 'transparency')
        Stri['coor'] = conf.get('stri_%s'%n, 'coor')
        Stri['zorder'] = conf.get('stri_%s'%n, 'zorder')
        self.plotconf['Stri_%s'%n] = Stri

    def get_imag_conf(self, conf, n):
        '''
        get the configuration for the image number n
        '''
        imag = {}
        imag['file'] = conf.get('imag_%s'%n, 'file')
        imag['zorder'] = conf.get('imag_%s'%n, 'zorder')
        imag['colormap'] = conf.get('imag_%s'%n, 'colormap')
        imag['contour_color'] = conf.get('imag_%s'%n, 'contour_color')
        imag['zscale'] = conf.get('imag_%s'%n, 'zscale')
        imag['contour'] = conf.get('imag_%s'%n, 'contour')
        imag['contour_lw'] = conf.getint('imag_%s'%n, 'contour_lw')
        imag['contour_size'] = conf.getint('imag_%s'%n, 'contour_size')
        self.plotconf['Imag_%s'%n] = imag
