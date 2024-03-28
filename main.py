"""
TODO's
- Fix DFS tree visualization
- Write README file
- Finish requirements.txt
- Finish step 5
- Finish step 7
- Look at feedback from assignment 3 and onwards
- Put force-directed .py files inside of Assignment 3 directory
- Create all graphs in the same format? if yes, which format?
- Create referencable functions (per assignment) so i can import them in here

- Radial tree also in main.py?
- Tree draw all edges and only draw tree edges option
- 
"""

# libs
import os

from dataclasses import dataclass
from typing import List

# visualizations imports
from Assignments.Assignment_1.Random import drawRandom
from Assignments.Assignment_1.Circle import drawCircle

@dataclass
class Network:
    files: List
    algorithms: List
    settings: List

""" Networks
ArgumentationNetwork
BlogosphereNetwork
JazzNetwork
LeagueNetwork
LesMiserables
SmallDirectedNetwork
"""

# for visualization function (with values also for networks function)
networks = {'Simple': Network(['LesMiserables', 'LeagueNetwork'], 
                              ['Random positions', 'Points on a circle'],
                              []), 
            'Tree': Network(['LesMiserables', 'JazzNetwork'],
                            ['Breadth-first search', 'Depth-first search'],
                            []), 
            'Force-directed': Network(['LesMiserables', 'JazzNetwork', 'SmallDirectedNetwork', 'LeagueNetwork'],
                                      [],
                                      []), 
            'Layered': Network(['SmallDirectedNetwork', 'LeagueNetwork'],
                               [],
                               []), 
            'Clustered': Network(['ArgumentationNetwork'],
                                 [],
                                 []), 
            'Projections': Network(['LesMiserables', 'JazzNetwork', 'LeagueNetwork'],
                                   ['Multidimensional scaling', 't-distributed stochastic neighbor embedding'],
                                   []), 
            'Quality-measurement': Network(['TODOTODO', 'TODO2'],
                                         ['TODO yes'],
                                         ['TODO row3', 'TODO testing'])} # + network

def display_title():
    os.system('cls' if os.name == 'nt' else 'clear')
              
    print("\t---------------------------------------------")
    print("-----------  Awesome Viz Data visualization tool  -----------")
    print("\t---------------------------------------------\n")

def display_visualizations():
    choice = '' 

    display_title()

    # print options
    print("What kind of visualization would you like to create?")
    for i, network in enumerate(networks.keys()):

        print(f" - [{i + 1}] {network} network")
    print(" - [q] Quit")

    # handle input
    choice = input("\n > ")
    if choice.isdigit() and int(choice)  <= len(networks.keys()) and int(choice) > 0:
        choice_network = list(networks.keys())[int(choice) - 1]

        display_settings({'name': choice_network})

    elif choice == 'q':
        return
    else:
        display_visualizations()

# displays the selected settings
def display_selected_settings(settings_dict):
    if len(settings_dict) > 1:
                for setting_name, setting in settings_dict.items():
                    
                    if setting_name == 'name':
                        print(f"Picked {setting} network visualization settings:")
                    else:
                        print(f" - {setting_name}: {setting}")

# takes a dict of already filled in settings as input
def display_settings(settings_dict):
    """
    - name
    - algorithm
    - file
    - settings
    """

    # -------------
    # print options
    # -------------
    network = networks[settings_dict['name']]

    # determine what input will be requested
    new_setting = ''
    new_setting_options = []
    if 'algorithm' not in settings_dict.keys():
        new_setting = 'algorithm'
        new_setting_options = network.algorithms
    elif 'file' not in settings_dict.keys():
        new_setting = 'file'
        new_setting_options = network.files
    else:
        new_setting = 'settings'
        new_setting_options = network.settings

    # head to next function if no settings are left to set
    if new_setting in settings_dict.keys():
        draw_visualization(settings_dict)
    # skip printing the options if <= 1
    elif len(new_setting_options) == 0:
        settings_dict[new_setting] = 'None'
        display_settings(settings_dict)
    elif len(new_setting_options) == 1:
        settings_dict[new_setting] = new_setting_options[0]
        display_settings(settings_dict)
    else:
        choice = '' 

        display_title()

        # print settings that were provided previously
        display_selected_settings(settings_dict)

        # print the actual options
        print(f"\nChoose {new_setting} options:")
        for i, setting in enumerate(new_setting_options):
            print(f" - [{i + 1}] {setting}")

        print(" - [b] Back")
        print(" - [q] Quit")

        # get input
        choice = input("\n > ")

        # handle input
        if choice.isdigit() and int(choice) <= len(new_setting_options) and int(choice) > 0:
            choice_setting = new_setting_options[int(choice) - 1]

            settings_dict[new_setting] = choice_setting
            display_settings(settings_dict)

        elif choice == "b":
            display_visualizations()
        elif choice == "q":
            return
        else:
            display_settings(settings_dict)


def draw_visualization(settings_dict):
    display_title()

    # print settings that were provided previously
    display_selected_settings(settings_dict)

    # print(settings_dict)
    if settings_dict['name'] == 'Simple':
        if settings_dict['algorithm'] == 'Points on a circle':
            drawCircle(settings_dict['file'])
        else:
            drawRandom(settings_dict['file'])

    elif settings_dict['name'] == 'Tree':
        print("TODO")
    elif settings_dict['name'] == 'Force-directed':
        print("TODO")
    elif settings_dict['name'] == 'Layered':
        print("TODO")
    elif settings_dict['name'] == 'Clustered':
        print("TODO")
    elif settings_dict['name'] == 'Projections':
        print("TODO")
    elif settings_dict['name'] == 'Quality-measurement':
        print("TODO")

    display_visualizations()


# The program itself
display_visualizations()