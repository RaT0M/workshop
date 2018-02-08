from datetime import datetime, timedelta
from typing import List


def get_data_stores_file() -> str:
    return '{}frascati_data_stores.yml'.format(get_out_path())


def get_out_path() -> str:
    return '/home/multiply-user/framework/testpath/'


def increase_time_step(current_time: datetime, time_interval: int, time_interval_unit: str) -> datetime:
    if time_interval_unit is 'days':
        current_time += timedelta(days=time_interval)
    elif time_interval_unit is 'weeks':
        current_time += timedelta(weeks=time_interval)
    return current_time


def get_config(priors_sm_dir: str, priors_veg_dir: str, start_time: str, end_time: str, roi: str,
               variables: List[str], time_interval: int, time_interval_unit: str, spatial_resolution_x: int,
               spatial_resolution_y: int) -> dict:
    config = {}
    config['General'] = _get_general_config(start_time=start_time, end_time=end_time, roi=roi,
                                            time_interval=time_interval, time_interval_unit=time_interval_unit,
                                            spatial_resolution_x=spatial_resolution_x,
                                            spatial_resolution_y=spatial_resolution_y)
    config['Inference'] = _get_inference_config(variables)
    config['Prior'] = _get_prior_config(priors_sm_dir=priors_sm_dir, priors_veg_dir=priors_veg_dir)
    return config


def _get_general_config(start_time: str, end_time: str, roi: str, time_interval: int, time_interval_unit: str,
                        spatial_resolution_x: int, spatial_resolution_y: int) -> dict:
    start_time_as_string = start_time
    end_time_as_string = end_time
    spatial_resolution_x_unit = 'm'
    spatial_resolution_y_unit = 'm'
    path_to_state_mask = '/path/to/my/state_mask.tif'
    output_directory_root = '/some/where/'
    general_dict = {}
    general_dict['roi'] = roi
    general_dict['start_time'] = start_time_as_string
    general_dict['end_time'] = end_time_as_string
    general_dict['time_interval'] = time_interval
    general_dict['time_interval_unit'] = time_interval_unit
    general_dict['spatial_resolution_x'] = spatial_resolution_x
    general_dict['spatial_resolution_x_unit'] = spatial_resolution_x_unit
    general_dict['spatial_resolution_y'] = spatial_resolution_y
    general_dict['spatial_resolution_y_unit'] = spatial_resolution_y_unit
    general_dict['state_mask'] = path_to_state_mask
    general_dict['output_directory_root'] = output_directory_root
    return general_dict


def _get_inference_config(variables: List[str]) -> dict:
    parameters = variables
    optical_operator_library = 'some_operator.nc'
    sar_operator_library = 'some_other_operator.nc'
    a_matrix = 'identity'
    inflation = 1e3
    inference_dict = {}
    inference_dict['parameters'] = parameters
    inference_dict['optical_operator_library'] = optical_operator_library
    inference_dict['sar_operator_library'] = sar_operator_library
    inference_dict['a_matrix'] = a_matrix
    inference_dict['inflation'] = inflation
    return inference_dict


def _get_prior_config(priors_sm_dir: str, priors_veg_dir: str) -> dict:
    general_prior_directory = priors_veg_dir
    prior_general_dict = {}
    prior_general_dict['directory_data'] = general_prior_directory
    
    prior_sm_dict = {}
    if len(priors_sm_dir) > 1:
        if type(priors_sm_dir) is dict:
            for k in priors_sm_dir.keys():
                prior_sm_dict.update({str(k): {str(k)+'_dir': priors_sm_dir[k]}})
        elif type(priors_sm_dir) is list:
        #    for i, path in enumerate (priors_sm_dir):
        #        prior_sm_dict.update({str(i)+'_dir':path})
            print('please provide a dictionar wih dicts "climatology", "munich"')
        else:
            prior_sm_climatology_directory = priors_sm_dir
            prior_sm_climatology_dict = {}
            prior_sm_climatology_dict['climatology_dir'] = prior_sm_climatology_directory
            prior_sm_dict['climatology'] = prior_sm_climatology_dict
            
    prior_sm_climatology_directory = priors_sm_dir
    prior_sm_climatology_dict = {}
    prior_sm_climatology_dict['climatology_dir'] = prior_sm_climatology_directory
    prior_sm_dict = {}
    prior_sm_dict['climatology'] = prior_sm_climatology_dict
    prior_lai_dict = {}
    prior_lai_dict['database'] = None
    prior_cab_dict = {}
    prior_cab_dict['database'] = None
    prior_dict = {}
    prior_dict['General'] = prior_general_dict
    prior_dict['sm'] = prior_sm_dict
    prior_dict['lai'] = prior_lai_dict
    prior_dict['cab'] = prior_cab_dict
    return prior_dict
