from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD, nametofont

#initializing gedoe

window = Tk()
window.update()
window.state("zoomed");
namew, nameh = 100, 50
width, height = window.winfo_width(), window.winfo_height()
window.title("naamplaatjes \t \t size:{} {}".format(width, height))
window.geometry('{}x{}'.format(width, height))
canvas = Canvas(window, width=width, height=height, bg= 'white')
#gedaan met initalizing gedoe
'''
vaste variabelen
'''
menuwidth = width*1/6
menuwoffset = width*5/6
menuheight = height;

kleur = ("zwart", "geel", "rood", "groen", "blauw", "paars")
colors = {"zwart": "black", "geel": "yellow", "rood": "red", "groen": "green", "blauw": "blue", "paars": "purple"}

names = []
categories = ['unassigned','cat1', 'cat2','empty','empty','empty','empty','empty']
assignment = {}
for el in categories:
    if el != 'empty':
        assignment[el] = []
    

'''
einde vaste variabelen
'''
'''
functions
'''
def handle_focus_in(_, entry):
    entry.delete(0, END)
    entry.config(fg='black')

def handle_focus_out(_, entry):
    entry.delete(0, END)
    entry.config(fg='grey')
    entry.insert(0, " geef naam in")
    gen_name.focus()
    
def toggle():
    if delval.get() == "Delete - AAN":
        canvas.itemconfig(delval, background = 'grey')
    else:
        canvas.itemconfig(delval, background = 'light grey')
        
def move(event, tag, name):
    draw = True
    if ((event.x < namew/2 or event.x > width - namew/2) or (event.y < nameh/2 or event.y > height - nameh/2)):
        draw = False
    if draw:
        x0, y0, x1, y1 = canvas.coords(tag)
        hwidth = (x1-x0)/2
        hheight = (y1-y0)/2
        canvas.coords(tag, event.x - hwidth, event.y - hheight, event.x + hwidth, event.y + hheight)
        canvas.coords(name, event.x, event.y)
    check_unassigned()
        
def check_unassigned():
        return
    
def deleterect(_, tag, name):
    if delval.get() == "Delete - AAN":
        names.remove(name)
        for key in assignment:
            if name in assignment[key]:
                assignment[key].remove(name)
        canvas.delete(tag)
        canvas.delete('t.'+ name)
        check_unassigned()
    
def make_namecard():
    gen_name.focus();
    color = colors[chosen_color.get()]
    x0, y0, cardw, cardh = 100, 90 + 60*len(assignment['unassigned']), 125, 50
    name = name_entry.get();
    canvas.itemconfig(noname_error, state='hidden')
    canvas.itemconfig(empty_error, state= 'hidden')
    canvas.itemconfig(double_error, state= 'hidden')
    
    if name == ' geef naam in':
        canvas.itemconfig(noname_error, state = 'normal')
        return
  
    if name == '':
        canvas.itemconfig(empty_error, state= 'normal')
        return
    if name in names:
        canvas.itemconfig(double_error, state= 'normal')
        return
    nametag = 't.' + name.replace(" ","")
    recttag = 'r.' + name.replace(" ","")
    names.append(name);
    assignment['unassigned'].append(name)
    rect = canvas.create_rectangle(x0 - cardw/2, y0 - cardh/2, x0 + cardw/2, y0 + cardh/2, outline= color, width= 4, fill = 'white', tags = recttag)
    text = canvas.create_text(x0, y0, font= (BOLD, 13), text=name, tags= nametag)
    canvas.tag_bind(nametag, '<B1-Motion>', lambda event: move(event, recttag, nametag))
    canvas.tag_bind(recttag, '<B1-Motion>', lambda event: move(event, recttag, nametag))
    canvas.tag_bind(nametag, '<ButtonPress-1>', lambda event: deleterect(event, recttag, name));
    canvas.tag_bind(recttag, '<ButtonPress-1>', lambda event: deleterect(event, recttag, name));
    canvas.tag_bind(nametag, '<ButtonRelease-1>', lambda event: assign_cat(event, recttag, name));
    canvas.tag_bind(recttag, '<ButtonRelease-1>', lambda event: assign_cat(event, recttag, name));
    
def del_name(name):
    for e in categories:
        if e != 'empty':
            for el in assignment[e]:
                if el == name:
                    assignment[e].remove(name)  
     
def which_cat(x):
    if x < 200:
        return 0
    else:
        temp = (x-200)//150
        return temp + 1

def assign_cat(event, tag, name):
    kolom = which_cat(event.x)
    rang = len(assignment[categories[kolom]])
    del_name(name)
    assignment[categories[kolom]].append(name)
    nametag = 't.' + name
    x0, y0, cardw, cardh = 100, 90 + 60*(len(assignment[categories[kolom]])-1), 125, 50
    if kolom == 0:
        canvas.coords(tag, x0 - cardw/2, y0 - cardh/2, x0 + cardw/2, y0 + cardh/2)
        canvas.coords(nametag, x0, y0)
    else:
        x0 = 275 + (kolom-1)*150
        canvas.coords(tag, x0 - cardw/2, y0 - cardh/2, x0 + cardw/2, y0 + cardh/2)
        canvas.coords(nametag, x0, y0)  
    print(kolom)
    print(assignment)
    
    return
        
def make_column():
    name = category_entry.get()
    canvas.itemconfig(no_more_cat_error, state='hidden')
    if categories.count('empty') == 0:
        canvas.itemconfig(no_more_cat_error, state='normal')
        return
    categories[categories.index('empty')] = name;
    assignment[name] = []
    draw_categories()
    print(categories)

def draw_categories():
    canvas.create_line(200, 15, 200, height - 15, fill='black', width=2)
    for i in range(8):
        if categories[i] != 'empty':
            if i > 0:
                canvas.create_line(200 + 150*(i-1), 50 , 200 + 150*(i), 50, fill = 'black', width = 5)
                canvas.create_line(200 + (i)*catwidht, 15, 200 + (i)*catwidht, height - 15, fill='black', width = 2)
                canvas.create_text(50 + catwidht/2 + i*catwidht,30, text = categories[i])
'''
end functions
'''
'''
menu
'''

canvas.create_rectangle(menuwoffset, 0, width, height, fill='grey')

noname_error = canvas.create_text(menuwoffset + menuwidth/3, 150, state= 'hidden', font= ('arial', 14), fill = 'white', text= 'ongeldig! \n', justify=CENTER)
empty_error = canvas.create_text(menuwoffset + menuwidth/3, 160, state= 'hidden', font= ('arial', 14), fill = 'white', text= 'ongeldig! \ngeen naam\n meegegeven', justify=CENTER)
double_error = canvas.create_text(menuwoffset + menuwidth/3, 150, state= 'hidden', font= ('arial', 14), fill = 'white', text= 'ongeldig! \nnaam bestaat al ', justify=CENTER)

'''name entry'''
name_entry = Entry(canvas,relief=SUNKEN, fg = 'grey', width = 20)
name_entry.insert(END, ' geef naam in')
name_entry.place(x=menuwoffset+menuwidth/3, y=70, anchor="center", height= 23)
name_entry.bind("<FocusIn>", lambda event: handle_focus_in(event, name_entry))
name_entry.bind("<FocusOut>", lambda event: handle_focus_out(event, name_entry))

gen_name = Button(canvas, text= 'voeg naam toe', bd= 3, command= lambda: make_namecard())
gen_name.place(x=menuwoffset + menuwidth/3, y=105, anchor="center", width= 125)

chosen_color = StringVar()
colormenu = ttk.OptionMenu(canvas, chosen_color, kleur[0], *kleur)
colormenu.place(x=menuwoffset + menuwidth*2/3+20, y=70, anchor="center", width= 70)

'''categorie entry'''
canvas.create_line(menuwoffset+5, 200, width-5, 200, fill= 'black')

category_entry = Entry(canvas,relief= SUNKEN, fg = 'grey')
category_entry.insert(END, ' geef categorie in')
category_entry.place(x = menuwoffset + menuwidth/3, y = 225, anchor="center", height=23);
category_entry.bind("<FocusIn>", lambda event: handle_focus_in(event, category_entry))
category_entry.bind("<FocusOut>", lambda event: handle_focus_out(event, category_entry))

gen_category = Button(canvas, text= 'voeg categorie toe', bd= 3, command= lambda: make_column())
gen_category.place(x=menuwoffset + menuwidth/3, y =260, anchor='center', width = 125)
delval = StringVar()
toggle = Checkbutton(canvas, onvalue="Delete - AAN", offvalue="Delete - UIT", width=10, indicatoron=False, variable=delval, textvariable=delval, anchor=NW,selectcolor="gray", background="light gray", command=toggle)
toggle.place(x=menuwoffset + menuwidth/2, y= 500, anchor = 'center')
delval.set("Delete - UIT")
''' end menu '''

''' workfield'''
maxwidth = menuwoffset - 80
catwidht = 150
draw_categories()

no_more_cat_error = canvas.create_text(menuwoffset + menuwidth/3, 150, state= 'hidden', font= ('arial', 14), fill = 'white', text= 'ongeldig!\n alle categorieën\n in gebruik', justify=CENTER)


''' unassigned '''
canvas.create_text(100, 30, text = 'niet toegewezen', font = (11), anchor=CENTER)
canvas.create_line(25, 50, 175, 50, fill='black', width=5)


''' assigned '''


    


''' end workfield'''
'''
finishing touch
'''

canvas.pack(fill = "both", expand=True)
window.mainloop()
