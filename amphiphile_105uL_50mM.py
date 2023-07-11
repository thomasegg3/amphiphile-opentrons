'''
Thomas Egg
July 11, 2023
Code for optimization of amphiphile experimentation with the opentrons
'''

# Libraries
from opentrons import protocol_api
import pandas as pd

# Initialize metadata
metadata = {'apiLevel': '2.14'}

# Function to extract volume from string
def extract_volumes(values, solution):
    '''
    Function to extract values from dataframe cells

    @param values : the values to parse for volumes
    @param solution : the solution to parse for
    '''

    # Loop through and collect values
    volumes = []
    for value in values:

        # Save correct entry
        try:

            if value[solution]:
                volumes.append(value[solution])
            else:
                volumes.append(0)

        except:
            print('SOLUTION NOT FOUND')

    # Return data
    return volumes

# Function to transfer requisite volumes
def transfer_solution(pipette, plate, df, solution, tube):
    '''
    Function to transfer variable volumes of solution to deepwell plate. This function
    is meant to handle single channel pipette.

    @param pipette : pipetting instrument
    @param plate : deepwell plate
    @param df : dataframe containing specifications for deep well plate
    @param solution : solution of interest, MUST be the samne as in dataframe cells
    @param solution_dict : dictionary of solutions and locations
    '''

    # Pick up tips
    pipette.pick_up_tip()

    # List of plate wells
    well_list = plate.wells()

    # Get information from dataframe
    volume_data = []
    df = df.iloc[:, 1:]
    for (_, col_data) in df.iteritems():

        # Save volume to list
        volumes = extract_volumes(col_data.values)

        # Reformat
        for volume in volumes:

            volume_data.append(volume)

    # Filter so only wells that need solution are passed through
    indices_to_remove = [i for i, val in enumerate(volume_data) if val == 0]
    volume_data = [val for i, val in enumerate(volume_data) if i not in indices_to_remove]
    well_list = [val for i, val in enumerate(well_list) if i not in indices_to_remove]

    # Transfer liquid
    pipette.transfer(
        volume_data,
        tube,
        [plate.wells_by_name()[well_name] for well_name in plate.wells()],
        new_tip='never'
    )

    # Drop tip
    pipette.drop_tip()

# Function to run protocol
def run(protocol: protocol_api.ProtocolContext):

    # Initialize labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    tube = protocol.load_labware('opentrons_15_tuberack_5500000ul', 6)
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack])
    W1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    W2 = protocol.load_labware('corning_96_wellplate_360ul_flat', 3)

    # Save dataframes
    df1 = pd.read_csv()
    df2 = pd.read_csv()

    # Distribution of Decanoic Acid - 1mM
    transfer_solution(p300, W1, df1, 'D1')
    transfer_solution(p300, W2, df2, 'D1')