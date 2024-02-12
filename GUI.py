from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

import matplotlib.pyplot as plt

# TODO: look in the slides for creating circles and lines with matplotlib

# plot function is created for  
# plotting the graph in  
# tkinter window 
def plot(): 
  
    # # the figure that will contain the plot 
    # fig = Figure(figsize = (5, 5), 
    #              dpi = 100) 
  
    # # list of squares 
    # y = [i**2 for i in range(101)] 
  
    # # adding the subplot 
    # plot1 = fig.add_subplot(111) 
  
    # # plotting the graph 
    # plot1.plot(y)

    figure, axes = plt.subplots()
    Drawing_colored_circle = plt.Circle(( 0.6 , 0.6 ), 0.2 )
 
    axes.set_aspect( 1 )
    axes.add_artist( Drawing_colored_circle )
    plt.title( 'Colored Circle' )
  
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(figure, 
                               master = window)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   window) 
    toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
# the main Tkinter window 
window = Tk() 
  
# setting the title  
window.title('Plotting in Tkinter') 
  
# dimensions of the main window 
window.geometry("500x500") 
  
# button that displays the plot 
plot_button = Button(master = window,  
                     command = plot, 
                     height = 2,  
                     width = 10, 
                     text = "Plot") 
  
# place the button  
# in main window 
plot_button.pack() 
  
# run the gui 
window.mainloop() 