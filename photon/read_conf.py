'''

The photon Project 
-------------------
File: read_conf.py

This file reads the configuration file

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import configparser
import os


class Conf:
    """
    This Class defines the arguments to be calle to use SPARTAN
    For the help, you can use 'SPARTAN -h' or 'SPARTAN --help'
    """
    def __init__(self,conf):
        """
        Class constructor, defines the attributes of the class
        and run the argument section
        """
        if conf == None:
            ##if no configuration was passed, we take the default one
            dir_path = os.path.dirname(os.path.realpath(__file__))
            default_file = os.path.join(dir_path, 'properties.conf')
            self.read_conf(default_file)

        else:
            self.read_conf(conf)


        
    def read_conf(self, fileconf):
        '''
        Method that reads the configuration file passed to the code
        '''
        config = configparser.ConfigParser()
        config.read(fileconf)

        ###background color
        self.BACK = config.get('background', 'back_color')

        ##AXIS properties
        AXIS = {'Color' : '', 'Label_color' : '', 'lw' : '', 'Labelsize' : '', 'Axis_label_font' : ''}
        AXIS['Color'] = config.get('AXIS', 'Color')
        AXIS['Label_color'] = config.get('AXIS', 'Label_Color')
        AXIS['lw'] = config.getfloat('AXIS', 'linewidth')
        AXIS['Labelsize'] = config.getfloat('AXIS', 'Labelsize')
        AXIS['Axis_label_font'] = config.get('AXIS', 'Axis_label_font')
        self.axis = AXIS

        ####Ticks properties
        TICKS = {'Minor' : '', 'placement' : '', 'Major_size' : '', 'Minor_size' : '', \
                'Major_width' : '', 'Minor_width' : '', 'Ticks_color' : '', 'Label_color' : '',\
                'Ticks_label_font' : '', }

        TICKS['Minor'] = config.get('TICKS', 'Minor')
        TICKS['placement'] = config.get('TICKS', 'placement')
        TICKS['Major_size'] = config.getfloat('TICKS', 'Major_size')
        TICKS['Minor_size'] = config.getfloat('TICKS', 'Minor_size')
        TICKS['Major_width'] = config.getfloat('TICKS', 'Major_width')
        TICKS['Minor_width'] = config.getfloat('TICKS', 'Minor_width')
        TICKS['Ticks_color'] = config.get('TICKS', 'Ticks_color')
        TICKS['Label_color'] = config.get('TICKS', 'Label_color')
        TICKS['Label_size'] = config.getfloat('TICKS', 'Label_size')
        TICKS['Ticks_label_font'] = config.get('TICKS', 'Ticks_label_font')
        self.ticks = TICKS


        ###legend
        LEGEND = {'Frame' : '', 'font_size' : '', 'Legend_font' : '',\
                'Label_font_color' : '', 'ncol' : '', 'location':''}
        LEGEND['Frame'] = config.get('LEGEND', 'Frame')
        LEGEND['font_size'] = config.getfloat('LEGEND', 'font_size')
        LEGEND['Legend_font'] = config.get('LEGEND', 'Legend_font')
        LEGEND['Label_font_color'] = config.get('LEGEND', 'Label_font_color')
        LEGEND['location'] = config.get('LEGEND', 'location')
        self.legend = LEGEND

        


