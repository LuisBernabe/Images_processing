"""
Luis Gerardo Bernabe
luis_berna@ciencias.unam.mx
"""
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image
import utils
import filters


original_PIL = None
original_CV2 = None
panel2 = None
global imName

def reload_filtered_img(w, filter_to_apply, extras):

    fil = getattr(filters, filter_to_apply)
    filtered_img = fil('perrito.jpg', xt= extras)
    im = Image.open(filtered_img)
    tkimage = ImageTk.PhotoImage(im)
    panel=Label(w,image=tkimage)
    panel.pack(side='right')
    w.mainloop()

def load_image(w):
    try:
        f = askopenfilename()
        #print "f===",f
        im = Image.open(f)
        tkimage = ImageTk.PhotoImage(im)
        panel=Label(w,image=tkimage)
        panel.pack(side='left')
        w.mainloop()
    except TypeError as e:
        return


def main():
    w = Tk()
    w.title("filtros")
    w.geometry("1280x720")
    w.configure(background='gray')

    global panel2
    panel2 = Label(w)
    panel2.pack(side='right')

    menu_bar = Menu(w)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label = "Cargar imagen.", command=lambda : load_image(w))
    file_menu.add_command(label = "Guardar imagen.")
    file_menu.add_command(label = "Salir.", command = w.quit)

    menu_bar.add_cascade(label="File", menu=file_menu)

    filters_menu = Menu(menu_bar, tearoff=0)
    filters_menu.add_command(label = "Escala de grises.",
                             command = lambda : reload_filtered_img(w,
                                                            "escalaDeGrises", {}))

    menu_bar.add_cascade(label="Filtros", menu=filters_menu)
    w.config(menu=menu_bar)

    w.mainloop()


if __name__ == '__main__':
    main()
