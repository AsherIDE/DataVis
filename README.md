# DataVis network visualizations program
This repository is dedicated to visualizing `.dot` files using `python`. It consists of 7 different visualization categories, including:
- Simple graph
- Tree graph
- Force-directed graph
- Layered graph
- Clustered graph
- Projections graph
- Quality-measurement graph

This repository has been tested with the following networks:
- ArgumentationNetwork.dot
- BlogosphereNetowrk.dot
- JazzNetwork.dot
- LeagueNetwork.dot
- LesMiserables.dot
- SmallDirectedNetwork.dot

The program itself will show which type of visualization is compatible with which type of network.

## Required packages
In order to use this repository, you do need to install some libraries which can be found inside of the `requirements.txt` inside of the root directory.

The required packages can be installed by running `pip install -r requirements.txt` inside of a terminal that is executed inside of the root directory.

## Running the program
The program is called `main.py` and it can also be found inside of the root directory. If all required packeges are installed you should simply be able to run the file, which will then launch a prompt. Inside of the prompt you are provided with options from which you will have to choose. Note that each type of graph comes with different types of settings.

## Running loose scripts
The following list of files are used for the `main.py` program. This is meant for people willing to get more into the technical details of the repository:
- `Assignments.Assignment_1.Random import`
- `Assignments.Assignment_1.Circle import`
- `Assignments.Assignment_2.nodeTreePositioning`
- `Assignments.Assignment_3.ForceDirectedLayout`
- `Assignments.Assignment_4.crossing_reduction`
- `Assignments.Assignment_5.edgeBundling`
- `Assignments.Assignment_6.MDS`
- `Assignments.Assignment_6.tsne`
- `Assignments.Assignment_6.mds_quality`

Note that some of these files reference helper functions in other files. Currently the above mentioned files reference helper functions in other files through a reference from the main branch. This means that if you were to round only of those functions seperately, you would have to remove `Assignments.Assignment_?` from the import statement at the top of the file.

At the bottom of the above mentioned files you will find a testing area with an example of how to execute the script. You can just uncomment it to get it to work. Don't forget that you can only have one `FILE_NAME` variable uncommented at the same time, otherwise you will only visualize the last variable called `FILE_NAME`.