#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Initialisation of test case scenario at user workshop Frascati 2018.

    Copyright (C) 2018  Thomas Ramsauer
"""

import yaml

from datetime import datetime

import multiply_workshop_utils.utils as utils

from multiply_data_access import DataAccessComponent
from multiply_prior_engine import PriorEngine
from multiply_core.util import AttributeDict

__author__ = ["Thomas Ramsauer"]
__copyright__ = "Copyright 2018, Thomas Ramsauer"
__credits__ = ["Thomas Ramsauer"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Thomas Ramsauer"
__email__ = "t.ramsauer@iggf.geo.uni-muenchen.de"
__status__ = "Prototype"


class Initialize_Munich(object):
    """Initialize config creation, ... of MULTIPLY platform
    for the user workshop Frascati.
    """

    valid_priors = ['Vegetation',
                    'SoilMoisture_measured',
                    'SoilMoisture_CCI']

    def __init__(self, **kwargs):
        self.priors = kwargs.get('priors', None)
        assert self.priors is not None, 'There must be priors defined!'
        self._create_config()
        self._set_up_data_access()
        self._load_prior_paths()
        self._write_prior_config()
        self._get_prior_files()

    def _create_config(self):
        y_min = 48.1999915829779
        y_max = 48.3399661722341
        x_min = 11.6000596879027
        x_max = 11.8099591388747
        # roi = 'POLYGON ((48.0 11.3, 48.2 11.3, 48.1 11.1, 48.0 11.0, 48.0 11.3))'
        roi = 'POLYGON (({} {}, {} {}, {} {}, {} {}))'.format(x_min, y_max,
                                                              x_max, y_max,
                                                              x_max, y_min,
                                                              x_min, y_min) 
        start_time_as_string = '2017-05-01'
        end_time_as_string = '2017-08-31'
        time_interval = 8
        time_interval_unit = 'days' # days or weeks
        spatial_resolution_x = 10 # in m
        spatial_resolution_y = 10 # in m
        variables = ['sm', 'lai', 'cab']

    def _set_up_data_access(self, data_stores):
        data_access_component = DataAccessComponent()
        data_stores_file = utils.get_data_stores_file()
        data_access_component.read_data_stores(data_stores_file)
        return data_access_component
    
    def _load_prior_paths(self):
        prior_dirs = {}
        for prior in self.priors:
            assert prior in valid_priors, '{} is not a valid prior name!'.format(prior)
            if 'SoilMoisture_CCI' in prior:
                prior_dirs.update({prior: data_access_component.get_data_urls(roi, start_time_as_string, 
                                                            end_time_as_string,
                                                            'SoilMoisture_CCI')[0]})
            elif 'SoilMoisture_measured' in prior:
                prior_dirs.update({prior: data_access_component.get_data_urls(roi, start_time_as_string, 
                                                            end_time_as_string,
                                                            'SoilMoisture_measured')[0]})
            elif 'Vegetation' in prior:
                prior_dirs.update({prior: data_access_component.get_data_urls(roi, start_time_as_string, 
                                                            end_time_as_string,
                                                            'Vegetation')[0]})
        return prior_dirs

    def _write_prior_config(self):
        # TODO how to integrate the priors here?
        config = utils.get_config(priors_sm_dir=priors_sm_dir, priors_veg_dir=priors_veg_dir, 
                          roi=roi, start_time=start_time_as_string, 
                          end_time=end_time_as_string, variables=variables, 
                          time_interval=time_interval, 
                          time_interval_unit=time_interval_unit,
                          spatial_resolution_x=spatial_resolution_x,
                          spatial_resolution_y=spatial_resolution_y)
        config_file_name = '{}config.yml'.format(utils.get_out_path())
        yaml.dump(config, open(config_file_name, 'w+'))
        config_as_dict = AttributeDict(**config)
        return config_as_dict

    def _create_time_vector(self):
        start_time = datetime.strptime(start_time_as_string, "%Y-%m-%d")
        end_time = datetime.strptime(end_time_as_string, "%Y-%m-%d")

        current_time = start_time

    def _get_prior_files(self):
        prior_file_dicts = []
        while current_time < end_time:
            time_string = current_time.strftime("%Y-%m-%d")
            prior_engine = PriorEngine(datestr=time_string, variables=variables, config=(config_file_name))
            prior_file_dicts.append(prior_engine.get_priors())
            current_time = utils.increase_time_step(current_time, time_interval, time_interval_unit)
        return prior_file_dicts
