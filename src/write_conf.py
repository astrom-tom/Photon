'''

The photon Project 
-------------------
File: write_conf.py

This file writes down a new the configuration file

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import configparser
import os


def save(fileconf, config):
    '''
    Function that writes down the current configuration
    Parameters:
    ----------
    fileconf        str, path/to/file/to/be/saved
    config          obj, config to be saved
    '''

    ##open default file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    default_file = os.path.join(dir_path, 'properties.conf')

    ####read the default file that we will modify
    fileconfig = configparser.ConfigParser()
    fileconfig.read(default_file)

    ###background color
    fileconfig.set('background', 'back_color', config.BACK)

    ##AXIS properties
    fileconfig.set('AXIS', 'Color', config.axis['Color'])
    fileconfig.set('AXIS', 'Label_Color', config.axis['Label_color'])
    fileconfig.set('AXIS', 'linewidth', str(config.axis['lw']))
    fileconfig.set('AXIS', 'Labelsize', str(config.axis['Labelsize']))
    fileconfig.set('AXIS', 'Axis_label_font', config.axis['Axis_label_font'])

    ####Ticks properties
    fileconfig.set('TICKS', 'Minor', config.ticks['Minor'])
    fileconfig.set('TICKS', 'placement', config.ticks['placement'])
    fileconfig.set('TICKS', 'Major_size', str(config.ticks['Major_size']))
    fileconfig.set('TICKS', 'Minor_size', str(config.ticks['Minor_size']))
    fileconfig.set('TICKS', 'Major_width', str(config.ticks['Major_width']))
    fileconfig.set('TICKS', 'Minor_width', str(config.ticks['Minor_width']))
    fileconfig.set('TICKS', 'Ticks_color', config.ticks['Ticks_color'])
    fileconfig.set('TICKS', 'Label_color', config.ticks['Label_color'])
    fileconfig.set('TICKS', 'Label_size', str(config.ticks['Label_size']))
    fileconfig.set('TICKS', 'Ticks_label_font', config.ticks['Ticks_label_font'])
    

    ###legend
    fileconfig.set('LEGEND', 'Frame', config.legend['Frame'])
    fileconfig.set('LEGEND', 'font_size', str(config.legend['font_size']))
    fileconfig.set('LEGEND', 'Legend_font', config.legend['Legend_font'])
    fileconfig.set('LEGEND', 'Label_font_color', config.legend['Label_font_color'])
    fileconfig.set('LEGEND', 'location', config.legend['location'])
    
    with open(fileconf, 'w') as myconfig:
            fileconfig.write(myconfig)



