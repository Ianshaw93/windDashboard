"""IEA Task 37 Combined Case Study AEP Calculation Code
Written by Nicholas F. Baker, PJ Stanley, and Jared Thomas (BYU FLOW lab)
Created 10 June 2018
Updated 11 Jul 2018 to include read-in of .yaml turb locs and wind freq dist.
Completed 26 Jul 2018 for commenting and release
Modified 22 Aug 2018 implementing multiple suggestions from Erik Quaeghebeur:
    - PEP 8 adherence for blank lines, length(<80 char), var names, docstring.
    - Altered multiple comments for clarity.
    - Used print_function for compatibility with Python 3.
    - Used structured datatype (coordinate) and recarray to couple x,y coords.
    - Removed unused variable 'sWindRose' (getTurbLocYAML).
    - Removed unecessary "if ... < 0" case (WindFrame).
    - Simplified calculations for sin/cos_wind_dir (WindFrame).
    - Eliminated unecessary calculation of 0 values (GaussianWake, DirPower).
    - Turbine diameter now drawn from <.yaml> (GaussianWake)
    - Used yaml.safe_load.
    - Modified .yaml reading syntax for brevity.
    - Removed some (now) unused array initializations.
"""
from __future__ import print_function   # For Python 3 compatibility
import numpy as np
import math
import sys
import yaml                             # For reading .yaml files
from math import radians as DegToRad    # For converting degrees to radians


# Structured datatype for holding coordinate pair
coordinate = np.dtype([('x', 'f8'), ('y', 'f8')])

# no need for this
# def WindFrame(turb_coords, wind_dir_deg):
#     """Convert map coordinates to downwind/crosswind coordinates."""
#
#     # Convert from meteorological polar system (CW, 0 deg.=N)
#     # to standard polar system (CCW, 0 deg.=W)
#     # Shift so North comes "along" x-axis, from left to right.
#     wind_dir_deg = 270. - wind_dir_deg
#
#     # Convert inflow wind direction from degrees to radians
#     wind_dir_rad = DegToRad(wind_dir_deg)
#
#     # Constants to use below
#     cos_dir = np.cos(-wind_dir_rad)
#     sin_dir = np.sin(-wind_dir_rad)
#     # Convert to downwind(x) & crosswind(y) coordinates
#     frame_coords = np.recarray(turb_coords.shape, coordinate)
#     frame_coords.x = (turb_coords.x * cos_dir) - (turb_coords.y * sin_dir)
#     frame_coords.y = (turb_coords.x * sin_dir) + (turb_coords.y * cos_dir)
#
#     return frame_coords

# Test parameters
# Default turbine - user will be able to select different ones
rated_power = 3350000
radius = 65.0
rotor_area = 2.0 * math.pi * radius**2.0
turb_diam = 2*radius
hub_height = 110.0
cut_in_wind_speed = 4
cut_out_wind_speed = 25
rated_wind_speed = 9.8

# test wind data
wind_speed = [4, 8, 10]
# wind_dir_deg = [] # leave blank for test - assume all towards turbine i.e. theoretical max

power_produced = []
turb_pwr = []
turb_pwr_list = []


# new function created turbulence coefficient k for different wind speeds
# def Get_turbulence(wind_speed):
#     k = (3/2)*((wind_speed*0.09)**2)
#     return k

# def GaussianWake(frame_coords, turb_diam, wind_speedList):
#     """Return each turbine's total loss due to wake from upstream turbines"""
#     # Equations and values explained in <iea37-wakemodel.pdf>
#     num_turb = len(frame_coords)
#
#     # Constant thrust coefficient
#     CT = 4.0*1./3.*(1.0-1./3.)
#     # Constant, relating to a turbulence intensity of 0.075
#     #k = 0.0324555 #previous k taken as constant as wind speed was always 9.8m/s
#     # Array holding the wake deficit seen at each turbine
#     loss = np.zeros(num_turb)
#
#     for i in range(num_turb):            # Looking at each turb (Primary)
#         loss_array = np.zeros(num_turb)  # Calculate the loss from all others
#         for windspeed in wind_speedList: #additional for loop for k considering differing wind speeds
#             k = Get_turbulence(windspeed)
#             for j in range(num_turb):        # Looking at all other turbs (Target)
#                 x = frame_coords.x[i] - frame_coords.x[j]   # Calculate the x-dist
#                 y = frame_coords.y[i] - frame_coords.y[j]   # And the y-offset
#                 if x > 0.:                   # If Primary is downwind of the Target
#                     sigma = k*x + turb_diam/np.sqrt(8.)  # Calculate the wake loss
#                     # Simplified Bastankhah Gaussian wake model
#                     exponent = -0.5 * (y/sigma)**2
#                     radical = 1. - CT/(8.*sigma**2 / turb_diam**2)
#                     loss_array[j] = (1.-np.sqrt(radical)) * np.exp(exponent)
#                 # Note that if the Target is upstream, loss is defaulted to zero
#             # Total wake losses from all upstream turbs, using sqrt of sum of sqrs
#             loss[i] = loss[i] + np.sqrt(np.sum(loss_array**2))  # loss[i]+= np.sqrt(np.sum(loss_array**2))
#     for i in range(num_turb): # further for loop to get average loss for each turbine
#         loss[i] = loss[i]/len(wind_speedList) # /=
#     return loss

# choose standard turbine stats
def DirPower(wind_speed, turb_diam, cut_in_wind_speed,
             cut_out_wind_speed, rated_wind_speed, rated_power): # turb_coords, wind_dir_deg,
    """Return the power produced by each turbine."""
    # num_turb = len(turb_coords)

    # Shift coordinate frame of reference to downwind/crosswind
    # show max output if facing optimal direction/changing directions
    # frame_coords = WindFrame(turb_coords, wind_dir_deg)
    # Use the Simplified Bastankhah Gaussian wake model for wake deficits
    # loss = GaussianWake(frame_coords, turb_diam, wind_speedList) # bring in losses - 3 dummy values added for wind speed
    # Effective windspeed is freestream multiplied by wake deficits
    # wind_speed_eff = wind_speed*(1.-loss)
    # By default, the turbine's power output is zero
    # turb_pwr = np.zeros(num_turb)

    # Check to see if turbine produces power for experienced wind speed
    # for n in range(num_turb):
        # If we're between the cut-in and rated wind speeds
    # calc for turbine always turning into optimal direction;
    # later show for fixed direction
    turb_pwr_list = []

    num_wind_speed = len(wind_speed)
    for i in range(num_wind_speed):
        if ((cut_in_wind_speed <= wind_speed[i])
                and (wind_speed[i] < rated_wind_speed)):
            # Calculate the curve's power
            turb_pwr = rated_power * ((wind_speed[i] - cut_in_wind_speed)
                                      / (rated_wind_speed - cut_in_wind_speed)) ** 3
            turb_pwr_list.append(turb_pwr)
        # If we're between the rated and cut-out wind speeds
        elif ((rated_wind_speed <= wind_speed[i])
                and (wind_speed[i] < cut_out_wind_speed)):
            # Produce the rated power
            turb_pwr = rated_power
            turb_pwr_list.append(turb_pwr)

        # Sum the power from all turbines for this direction
        # pwrDir = np.sum(turb_pwr)

        # return pwrDir
        print(turb_pwr)
    print(turb_pwr_list)
    return turb_pwr_list

def calcAEP(power_produced):
    """Calculate the wind farm AEP."""
    # num_bins = len(wind_freq)  # Number of bins used for our windrose
    #
    # #  Power produced by the wind farm from each wind direction
    # pwr_produced = np.zeros(num_bins)
    # # For each wind bin
    # for i in range(num_bins):
    #     # Find the farm's power for the current direction
    #     pwr_produced[i] = DirPower(turb_coords, wind_dir[i], wind_speed,
    #                                turb_diam, cut_in_wind_speed, cut_out_wind_speed,
    #                                rated_ws, rated_power)

    AEP_list = []
    AEP_total = 0
    # will need to convert directional info to frequency from direction
    # wind_freq = 1 # 1 for test
    wind_freq = 1 / len(wind_speed)

    #  Convert power to AEP
    hrs_per_year = 365.*24.
    for i in range(len(wind_speed)):
        # wind_freq = 1/len(wind_speed)
        AEP = hrs_per_year * (wind_freq * power_produced[i])
        AEP /= 1.E6  # Convert to MWh
        AEP_list.append(AEP)
    print(AEP_list)
    # AEP would be total of list
    for item in range(len(wind_speed)):
        AEP_total += AEP_list[item]
    print(AEP_total)
    return AEP

#
# def getTurbLocYAML(file_name):
#     """ Retrieve turbine locations and auxiliary file names from <.yaml> file.
#     Auxiliary (reference) files supply wind rose and turbine attributes.
#     """
#     # Read in the .yaml file
#     with open(file_name, 'r') as f:
#         defs = yaml.safe_load(f)['definitions']
#
#     # Rip the x- and y-coordinates (Convert from <list> to <ndarray>)
#     turb_xc = np.asarray(defs['position']['items']['xc'])
#     turb_yc = np.asarray(defs['position']['items']['yc'])
#     turb_coords = np.recarray(turb_xc.shape, coordinate)
#     turb_coords.x, turb_coords.y = turb_xc, turb_yc
#
#     # Rip the expected AEP, used for comparison
#     # AEP = defs['plant_energy']['properties']
#     #           ['annual_energy_production']['default']
#
#     # Read the auxiliary filenames for the windrose and the turbine attributes
#     ref_list_turbs = defs['wind_plant']['properties']['layout']['items']
#     ref_list_wr = (defs['plant_energy']['properties']
#                        ['wind_resource_selection']['properties']['items'])
#
#     # Iterate through all listed references until we find the one we want
#     # The one we want is the first reference not internal to the document
#     # Note: internal references use '#' as the first character
#     fname_turb = next(ref['$ref']
#                       for ref in ref_list_turbs if ref['$ref'][0] != '#')
#     fname_wr = next(ref['$ref']
#                     for ref in ref_list_wr if ref['$ref'][0] != '#')
#
#     # Return turbine (x,y) locations, and the filenames for the others .yamls
#     return turb_coords, fname_turb, fname_wr


# def getWindRoseYAML(file_name):
#     """Retrieve wind rose data (bins, freqs, speeds) from <.yaml> file."""
#     # Read in the .yaml file
#     with open(file_name, 'r') as f:
#         props = yaml.safe_load(f)['definitions']['wind_inflow']['properties'] #do I need to add to this??
#
#     # Rip wind directional bins, their frequency, and the farm windspeed
#     # (Convert from <list> to <ndarray>)
#     wind_dir = np.asarray(props['direction']['bins'])
#     # average speed data affiliated with wind frequency added to windrose yaml
#     average_speedList = np.asarray(props['speed']['average_speed'])
#     wind_freq = np.asarray(props['probability']['default'])
#     # (Convert from <list> to <float>)
#     wind_speed = float(props['speed']['default'])
#
#     return wind_dir, wind_freq, wind_speed, average_speedList


# def getTurbAtrbtYAML(file_name):
#     '''Retreive turbine attributes from the <.yaml> file'''
#     # Read in the .yaml file
#     with open(file_name, 'r') as f:
#         defs = yaml.safe_load(f)['definitions']
#         op_props = defs['operating_mode']['properties']
#         turb_props = defs['wind_turbine_lookup']['properties']
#         rotor_props = defs['rotor']['properties']
#
#     # Rip the turbine attributes
#     # (Convert from <list> to <float>)
#     turb_ci = float(op_props['cut_in_wind_speed']['default'])
#     turb_co = float(op_props['cut_out_wind_speed']['default'])
#     rated_ws = float(op_props['rated_wind_speed']['default'])
#     rated_pwr = float(turb_props['power']['maximum'])
#     turb_diam = float(rotor_props['radius']['default']) * 2.
#
#     return turb_ci, turb_co, rated_ws, rated_pwr, turb_diam


#initialized instance of class or object - auto called when new instance of class created
if __name__ == "__main__":
    """Used for demonstration.
    An example command line syntax to run this file is:
        python iea37-aepcalc.py iea37-ex16.yaml
    For Python .yaml capability, in the terminal type "pip install pyyaml".
    """
    power_produced = DirPower(wind_speed, turb_diam, cut_in_wind_speed,
                              cut_out_wind_speed, rated_wind_speed, rated_power)
    AEP = calcAEP(power_produced)

    # #print('debug')
    # # Read necessary values from .yaml files
    # # Get turbine locations and auxiliary <.yaml> filenames
    # turb_coords, fname_turb, fname_wr = getTurbLocYAML(sys.argv[1])
    # print(fname_wr)
    # # Get the array wind sampling bins, frequency at each bin, and wind speed
    # wind_dir, wind_freq, wind_speed, average_windList = getWindRoseYAML(fname_wr)
    # print(average_windList)
    # # Pull the needed turbine attributes from file
    # turb_ci, turb_co, rated_ws, rated_pwr, turb_diam = getTurbAtrbtYAML(
    #     fname_turb)
    #
    # # Calculate the AEP from ripped values
    # AEP = calcAEP(turb_coords, wind_freq, wind_speed, wind_dir,
    #               turb_diam, turb_ci, turb_co, rated_ws, rated_pwr)
    # # Print AEP for each binned direction, with 5 digits behind the decimal.
    # print(np.array2string(AEP, precision=5, floatmode='fixed',
    #                       separator=', ', max_line_width=62))
    # # Print AEP summed for all directions
    # print(np.around(np.sum(AEP), decimals=5))
    #print(getWindRoseYAML())