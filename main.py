# libs
import os

from dataclasses import dataclass
from typing import List, Dict

# visualizations imports
from Assignments.Assignment_1.Random import drawRandom
from Assignments.Assignment_1.Circle import drawCircle

from Assignments.Assignment_2.nodeTreePositioning import drawTree

from Assignments.Assignment_3.ForceDirectedLayout import drawForceDirected

from Assignments.Assignment_4.crossing_reduction import drawLayered, drawLayeredQuality

from Assignments.Assignment_5.edgeBundling import drawClusters

from Assignments.Assignment_6.MDS import drawMDS
from Assignments.Assignment_6.tsne import drawtSNE
from Assignments.Assignment_6.mds_quality import drawMDSQuality

@dataclass
class Network:
    files: List
    algorithms: List
    settings: Dict

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
                              {}), 
            'Tree': Network(['LesMiserables', 'JazzNetwork'],
                            ['Breadth-first search', 'Depth-first search'],
                            {'edge drawing':['All edges', 'Only tree edges'], 'root node':['1', '7', '11', '52', '71']}), 
            'Force-directed': Network(['LesMiserables', 'JazzNetwork', 'SmallDirectedNetwork', 'LeagueNetwork'],
                                      [],
                                      {'iteration':['50', '100', '200', '500']}), 
            'Layered': Network(['LesMiserables', 'SmallDirectedNetwork', 'LeagueNetwork', 'JazzNetwork'],
                               ['Median', 'Barycenter'],
                               {'dummy':['Dummy edges', 'Only direct edges']}), 
            'Clustered': Network(['ArgumentationNetwork'],
                                 [],
                                 {}), 
            'Projections': Network(['LesMiserables', 'JazzNetwork', 'LeagueNetwork'],
                                   ['Multidimensional scaling', 't-distributed stochastic neighbor embedding'],
                                   {'perplexity':['5', '10', '15', '20']}), 
            'Quality-measurement': Network(['LesMiserables', 'JazzNetwork', 'LeagueNetwork'],
                                         ['Multidimensional scaling', 'Layered network'],
                                         {})} # + network

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

        print(f" - [{i + 1}] {network} graph")
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
                        print(f"Picked {setting} graph visualization settings:")
                    elif setting_name == 'settings':

                        if len(settings_dict['settings']) > 0:
                            print(f" - {setting_name}:")

                            for k, v in setting.items():

                                if v != 'Irrelevant':
                                    print(f"\t- {k}: {v}")

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
    else:
        new_setting = 'file'
        new_setting_options = network.files
    # else:
    #     new_setting = 'settings'
    #     new_setting_options = network.settings

    # head to next function if no settings are left to set
    if new_setting in settings_dict.keys():
        display_specific_settings(settings_dict)
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




def display_specific_settings(settings_dict):
    network = networks[settings_dict['name']]

    # draw vis straight away if there are not settings
    if len(network.settings) == 0:
        draw_visualization(settings_dict)
    else:

        # add settings to settingsdict
        if 'settings' not in settings_dict:
            settings_dict['settings'] = {}

        # check if all settings have been iterated
        if len(settings_dict['settings']) == len(network.settings):
            print(settings_dict)
            draw_visualization(settings_dict)

        else:
            choice = '' 

            display_title()

            # print settings that were provided previously
            display_selected_settings(settings_dict)

            for setting, options in network.settings.items():

                # check which setting needs input
                if setting not in settings_dict['settings']:

                    # check if setting is possible with previous settings
                    if setting == 'perplexity' and settings_dict['algorithm'] == 'Multidimensional scaling' or setting == 'root node' and settings_dict['algorithm'] == 'Breadth-first search':
                        settings_dict['settings'][setting] = 'Irrelevant'
                        display_specific_settings(settings_dict)
                        break

                    # print the actual options
                    print(f"\nChoose {setting} options:")

                    for i, option in enumerate(options):
                        print(f" - [{i + 1}] {option}")

                    print(" - [b] Back")
                    print(" - [q] Quit")


                    # get input
                    choice = input("\n > ")

                    # handle input
                    if choice.isdigit() and int(choice) <= len(options) and int(choice) > 0:
                        choice_setting = options[int(choice) - 1]

                        settings_dict['settings'][setting] = choice_setting
                        display_specific_settings(settings_dict)

                    elif choice == "b":
                        display_settings(settings_dict)
                    elif choice == "q":
                        return
                    else:
                        display_specific_settings(settings_dict)

                    break



        



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
        fontsize, nodesize, xy = 5, 30, (110, -1.4)
        if settings_dict['file'] == 'LesMiserables':
            fontsize, nodesize, xy = 6, 100, (4, -0.9)

        draw_all_edges = False
        if settings_dict['settings']['edge drawing'] == 'All edges':
            draw_all_edges = True

        if settings_dict['algorithm'] == 'Breadth-first search':
            drawTree(settings_dict['file'], fontsize, nodesize, xy, draw_all_edges=draw_all_edges)
        else:
            root_node = settings_dict['settings']['root node']

            drawTree(settings_dict['file'], fontsize, nodesize, xy, draw_all_edges=draw_all_edges, MODE='dfs', START_NODE=root_node)


    elif settings_dict['name'] == 'Force-directed':
        sims = int(settings_dict['settings']['iteration'])

        drawForceDirected(settings_dict['file'], number_of_sims=sims)


    elif settings_dict['name'] == 'Layered':
        median = True
        if settings_dict['algorithm'] == 'Barycenter':
            median = False

        nodummies = True
        if settings_dict['settings']['dummy'] == 'Dummy edges':
            nodummies = False

        drawLayered(settings_dict['file'], draw_graph=True, nodummies=nodummies, median=median)
        
    elif settings_dict['name'] == 'Clustered':
        drawClusters(settings_dict['file'])
        
    elif settings_dict['name'] == 'Projections':
        if settings_dict['algorithm'] == 'Multidimensional scaling':
            drawMDS(settings_dict['file'])
        else:
            perplexity = int(settings_dict['settings']['perplexity'])

            drawtSNE(settings_dict['file'], perpl=perplexity)

    elif settings_dict['name'] == 'Quality-measurement':
        if settings_dict['algorithm'] == 'Multidimensional scaling':
            drawMDSQuality(settings_dict['file'])
        else:
            drawLayeredQuality(settings_dict['file'])

    display_visualizations()


# The program itself
display_visualizations()