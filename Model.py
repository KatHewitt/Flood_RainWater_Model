
"""
@author: KatHewitt

"""

import framework
import csv
import matplotlib.pyplot
import matplotlib.animation
import tkinter
import matplotlib.backends.backend_tkagg


#load in data (raster of elevations)
f = open('input_elevations.txt', newline='')             
environment = []                                        
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []                                        
    for value in row:
        rowlist.append(value)                           
    environment.append(rowlist)                         
f.close()


area = []


#create window for animation
fig = matplotlib.pyplot.figure(figsize=(10,10))


#set variables
rainfall = 10
days_rain = 30

matplotlib.pyplot.imshow(environment)       

rain_area = []
for i in range (len(environment)):
    rain_row = []
    for j in range (len(environment[i])):
        rain_row.append(rainfall)
    rain_area.append(rain_row)

        
carry_on = True



def update(frame_number):
    
    
    fig.clear()
    global carry_on


    #create lists and variables used in program
    diff = []
    max_output = 10    
    group_total = 0
    flow_scalar = []

    
    #find the highest point
    max_row = list(map(max,environment[1:-1]))
    max_elevation = max(max_row[1:-1])
    
    
    #run process on each cell
    for i in range (len(environment[1:-1])):                             
        for j in range (len(environment[i][1:-1])):
            if environment[i][j] >= max_elevation:                      
                diff.append(environment[i][j]-environment[i-1][j-1])    
                diff.append(environment[i][j]-environment[i-1][j])
                diff.append(environment[i][j]-environment[i-1][j+1])
                diff.append(environment[i][j]-environment[i][j-1])
                diff.append(environment[i][j]-environment[i][j+1])
                diff.append(environment[i][j]-environment[i+1][j-1])
                diff.append(environment[i][j]-environment[i+1][j])
                diff.append(environment[i][j]-environment[i+1][j+1])
                
                
                for k in range (len (diff)):
                    #calcule total downhill slopes
                    framework.makescalar(diff[k], group_total, flow_scalar)
                    #check if cell has water stores 
                    framework.checkmax(diff[k],rain_area[i][j], max_output)
                
                
                #allocate a percetage of water output to each downhill direction  
                for k in range (len(diff)):
                    if diff[k] > 0:                                     
                        x = (k%3)-1                                      
                        y = (int((k - x)/3))-1                          
                        if rain_area[i][j] + environment[i][j] > rain_area[i+x][j+y] + environment[i+x][j+y]:   
                            rain_area[i+x][j+y] =+ (framework.checkmax.flow*flow_scalar[k])     
                                 
                    
                #level ground rule (prevent water for building up at the edge of a level feature)
                for k in range (len(diff)):
                    if all (values <= 0 for values in diff):            
                        if diff[k] == 0:                                
                            x = (k%3)-1                                 
                            y = (int((k - x)/3))-1                      
                            rain_share = (rain_area[i][j] + (rain_area[i+x][j+y]))/2    
                            rain_area[i][j] = rain_share
                            rain_area[i+x][j+y] = rain_share
                
                
                #clear values and lists
                framework.clear(diff, flow_scalar, group_total)
                
                
                
            
            max_elevation =- 0.1

     
    #add rainfall for next day        
    framework.addrain(rain_area,rainfall)
    
        
    #plot rain_area for each day    
    matplotlib.pyplot.ylim(len(environment))        
    matplotlib.pyplot.xlim(len(environment[i]))     
    matplotlib.pyplot.gca().invert_xaxis()
    matplotlib.pyplot.imshow(rain_area)


    #export final rain_area to 'waterlevels.txt' 
    f2 = open('waterlevels.txt', 'w', newline='') 
    writer = csv.writer(f2, delimiter=' ')
    for row in rain_area:		
    	writer.writerow(row)
    f2.close()


#check for repeat
def gen_function(b = [0]):
    """
    requires no setup
    """
    a = 0
    global carry_on
    while (a < days_rain) & (carry_on):     
        yield a			
        a = a + 1                            
    else:
        print("Flooding Conditions after",rainfall,"unit(s) of Daily Rainfall over",days_rain," Days")     #print stopping statement
     

#set animation to run
def run():
    """
    requires no setup
    """
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.show()


#build GUI
root = tkinter.Tk() 
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 


tkinter.mainloop()