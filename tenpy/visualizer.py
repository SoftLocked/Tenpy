from tkinter import *
from tkinter import ttk
import tenpy.utility.randomHex as ranhex
import math

def show_screen(data=[], size=500, scl_=1,  dimensions=2):

########################################################################################################################
### SET UP TKINTER
########################################################################################################################

    root = Tk()
    root.title("Vector Visualization")
    root.geometry(str(size)+"x"+str(size))
    root.config(bg='black')
    w = Label(root, text=str(data),bg ='gray')
    root.update()

########################################################################################################################
### CREATE CANVAS
########################################################################################################################

    canvas = Canvas(root, width=root.winfo_width(), height=root.winfo_height(), bg="black", bd=0, highlightthickness=0, relief='ridge')
    canvas.grid(row=0, column=0)

########################################################################################################################
### CREATE GRAPH
########################################################################################################################

    def create_full_graph():

########################################################################################################################
### GRID LINE MATHEMATICS
########################################################################################################################

        scl_factor = scl_ * 10
        while (root.winfo_width() % scl_factor != 0):
            scl_factor += 10
        scl = root.winfo_width() / scl_factor

        cols = math.floor(root.winfo_width() / scl)
        rows = math.floor(root.winfo_height() / scl)

########################################################################################################################
### GRID LINE RENDERING
########################################################################################################################

        def grid_lines():
            for i in range(cols):
                canvas.create_line(i * scl, 0, i*scl, root.winfo_height(), fill="#37b7de")
            for j in range(rows):
                canvas.create_line(0, j * scl, root.winfo_height(), j*scl, fill="#157cd6")

########################################################################################################################
### CREATE GRAPH
########################################################################################################################

        vector_bool = False
        matrix_bool = False

        def create_graph():
            repeat_bool = True
            frames = 0

########################################################################################################################
### DETERMINE VECTOR VS MATRIX
########################################################################################################################

            for i in range(len(data)):
                for j in range(len(data[i])):
                    if str(type(data[i][j])) != "<class 'list'>":
                        vector_bool = True
                        matrix_bool = False
                    else:
                        vector_bool = False
                        matrix_bool = True

########################################################################################################################
### VECTOR CASE
########################################################################################################################

                if (vector_bool == True):

########################################################################################################################
### GRID LINES
########################################################################################################################

                    grid_lines()

                    canvas.create_line((cols / 2) * scl, 0, (cols / 2) * scl, root.winfo_height(), width=3,
                                       fill="white")
                    canvas.create_line(0, (rows / 2) * scl, root.winfo_height(), (rows / 2) * scl, width=3,
                                       fill="white")

                    for j in range(cols):
                        canvas.create_text(j * scl + 10, (rows / 2) * scl + 10, fill="white",
                                           font="Times " + str(int(0.01 / scl_factor)) + " bold",
                                           text=str(int(j - cols / 2)))
                    for k in range(rows):
                        canvas.create_text((cols / 2) * scl + 10, k * scl + 10, fill="white",
                                           font="Times " + str(int(0.01 / scl_factor)) + " bold",
                                           text=str(int(-(k - cols / 2))))

########################################################################################################################
### GET VECTOR DATA
########################################################################################################################

                    x = data[i][0] * scl
                    y = -data[i][1] * scl

########################################################################################################################
### VECTOR LINE RENDER
########################################################################################################################

                    canvas.create_line(root.winfo_width()/2, root.winfo_height()/2, root.winfo_width()/2 + x, root.winfo_height()/2 + y, width=5, fill=ranhex.random_hex())

########################################################################################################################
### LABEL ALLIGNMENT OPTIMIZATION
########################################################################################################################

                    neg_x = 1
                    neg_y = -1

                    if (data[i][0] > 0) and (data[i][1] > 0):
                        neg_x = 1
                        neg_y = -1
                    elif (data[i][0] > 0) and (data[i][1] < 0):
                        neg_x = 1
                        neg_y = 1
                    elif (data[i][0] < 0) and (data[i][1] > 0):
                        neg_x = -1
                        neg_y = -1
                    elif (data[i][0] < 0) and (data[i][1] < 0):
                        neg_x = -1
                        neg_y = 1

########################################################################################################################
### LABEL RENDER
########################################################################################################################

                    canvas.create_text(root.winfo_width()/2 + x + (neg_x*30), root.winfo_height()/2 + y + (neg_y*15), fill="white", font="Times " + str(int(1/scl_factor)) + " bold", text=str(data[i]))

########################################################################################################################
### MATRIX CASE
########################################################################################################################

                if (matrix_bool == True):

########################################################################################################################
### LINE FILL SEED AND ANIMATION DELAY SET
########################################################################################################################

                    line_fill = ranhex.random_hex()
                    delay = 150

########################################################################################################################
### GETTING MATRIX DATA
########################################################################################################################

                    start_x = data[i][0][0] * scl
                    start_y = -data[i][1][0] * scl

                    end_x = data[i][0][1] * scl
                    end_y = -data[i][1][1] * scl

########################################################################################################################
### SETTING SLOPE BETWEEN START AND END
########################################################################################################################

                    slope = (end_y-start_y)/(end_x-start_x)

########################################################################################################################
### LABEL ALLIGNMENT OPTIMIZATION
########################################################################################################################

                    neg_x = 1
                    neg_y = -1

                    if ((root.winfo_width() / 2 + start_x) > 0) and ((root.winfo_height() / 2 + start_y) > 0):
                        neg_x = 1
                        neg_y = -1
                    elif ((root.winfo_width() / 2 + start_x) > 0) and ((root.winfo_height() / 2 + start_y) < 0):
                        neg_x = 1
                        neg_y = 1
                    elif ((root.winfo_width() / 2 + start_x) < 0) and ((root.winfo_height() / 2 + start_y) > 0):
                        neg_x = -1
                        neg_y = -1
                    elif ((root.winfo_width() / 2 + start_x) < 0) and ((root.winfo_height() / 2 + start_y) < 0):
                        neg_x = -1
                        neg_y = 1

########################################################################################################################
### MOVEMENT SPEED SET
########################################################################################################################

                    x_speed = 0
                    y_speed = 0

                    x_acc = 0.01
                    y_acc = 0.01

########################################################################################################################
### ANIMATION LOOP
########################################################################################################################

                    while repeat_bool:
                        canvas.delete("all")

########################################################################################################################
### LABEL RENDER
########################################################################################################################

                        vector_label = canvas.create_text(root.winfo_width() / 2 + start_x + (neg_x * 30),
                                                          root.winfo_height() / 2 + start_y + (neg_y * 15),
                                                          fill="white",
                                                          font="Times " + str(int(1 / scl_factor)) + " bold",
                                                          text=str(data[i]))

########################################################################################################################
### LINE RENDER
########################################################################################################################

                        vector_line = canvas.create_line(root.winfo_width() / 2, root.winfo_height() / 2,
                                                         root.winfo_width() / 2 + start_x,
                                                         root.winfo_height() / 2 + start_y, width=5,
                                                         fill=line_fill)

########################################################################################################################
### ANIMATOR
########################################################################################################################

                        if ((start_x != end_x) and (start_y != end_y)) and frames > delay:
                            if start_x > end_x:
                                x_speed += x_acc
                                start_x -= x_speed
                            else:
                                x_speed += x_acc
                                start_x += x_speed
                            if (start_y < end_y):
                                y_speed += y_acc
                                start_y += y_speed* slope
                            else:
                                y_speed += y_acc
                                start_y -= y_speed * slope


                            print(str(start_x) + " " + str(end_x))
                            canvas.move(vector_label, x_speed, y_speed)

########################################################################################################################
### GRID LINES
########################################################################################################################

                        grid_lines()

                        canvas.create_line((cols / 2) * scl, 0, (cols / 2) * scl, root.winfo_height(), width=3,
                                           fill="white")
                        canvas.create_line(0, (rows / 2) * scl, root.winfo_height(), (rows / 2) * scl, width=3,
                                           fill="white")

                        for j in range(cols):
                            canvas.create_text(j * scl + 10, (rows / 2) * scl + 10, fill="white",
                                               font="Times " + str(int(0.01 / scl_factor)) + " bold",
                                               text=str(int(j - cols / 2)))
                        for k in range(rows):
                            canvas.create_text((cols / 2) * scl + 10, k * scl + 10, fill="white",
                                               font="Times " + str(int(0.01 / scl_factor)) + " bold",
                                               text=str(int(-(k - cols / 2))))

########################################################################################################################
### LOOP BREAKER
########################################################################################################################

                        tolerance = 10

                        #if (start_x == end_x-x_speed) or (start_x == end_x+x_speed) or (start_y == end_y-y_speed) or (start_y == end_y+y_speed):
                        if ((start_x > end_x-tolerance) and (start_x < end_x+tolerance)) and ((start_y > end_y-tolerance) or (start_y < end_y+tolerance)):
                            repeat_bool = False

                        frames += 1

                        root.update()

########################################################################################################################
### MAIN CALLS
########################################################################################################################

        create_graph()
    create_full_graph()
    root.update()
    root.mainloop()