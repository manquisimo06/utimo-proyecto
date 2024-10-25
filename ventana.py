import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import colorchooser
main_window=tk.Tk()
main_window.config(width=900, height=950)
logo_umg=tk.PhotoImage(file="logo4.png")
lavel=ttk.Label(main_window, image=logo_umg, )
lavel.place(x=50, y=35, width=100, height=100)
archivo_avierto=None
#Para desabilitar el boton guardar por si no hay algun archivo abierto por que este es un boton de guardar cambios si usted quiere 
#guardar un nuevo archivo precione guardar como y le puede poner la extencion que le aparezca y necesite
def desabilitar_boton():
    '''se creo esta variable gloval para hacer posible su uso ya que en esta funcion se crea y se le 
    asigna un dato que nos sera util en otro procedimiento, de lo contrario se aria imposible la utilizacion
    de dicha variable en otra funcion.
    '''
    global archivo_avierto
    if archivo_avierto is None:
        boton_guardar.config(state=tk.DISABLED)
    else:
        boton_guardar.config(state=tk.NORMAL)
def deshacer_archivo():
    texto1.event_generate("<<Undo>>")
def rehacer_texto():
    texto1.event_generate("<<Redo>>")
'''El Scrolledtext es un cuadro de texto que incluye una barra de desplazamiento, aqui mismo realizamos
la activacion o habilitamos el uso del undo (deshacer) que se utiliza en otra funcion'''
texto1=ScrolledText(main_window, undo=True)
texto1.place(x=50, y=200,width=600, height=700)

estilo=ttk.Style()
estilo.configure('Tlavel', padding=20)
'''Se decidio hacer uso de una caja de mensaje emergente para que muestre los nomres de los integrantes '''
def mensaje_integrantes():
    messagebox.showinfo(message="Danny Ivan Hernandez Rodas Carne No. 7690-24-26409\n"
                        "Alizon Marisol Alvarez Barillas Carne No. 7690-24-22844\n"
                        "Franklin Estuardo Andrade Chew Carne No. 7690-24-25388", title="Integrantes")

palabra_para_buscar=tk.Entry(main_window)
palabra_para_buscar.place(x=50, y=150, width=600, height=25)
def abrir_texto():
    global archivo_avierto
    filetypes=(
        ('all file', '*.*'),
        ('text file','*.txt'),
        ('python file', '*.py'),
        ('C++', '*.cpp'),
        ('C#', '*.cs')
    )
    archivo=askopenfilename(filetypes=filetypes)
    if archivo:
        texto1.delete(1.0, tk.END)
        with open(archivo,"r") as file:
            texto1.insert(1.0, file.read())
    archivo_avierto=(open(archivo,"w"))
    desabilitar_boton()

def guardar():
    global archivo_avierto
    if archivo_avierto:
        archivo_avierto.write(str(texto1.get(1.0, "end")))
        archivo_avierto.close()
        archivo_avierto=None
        desabilitar_boton()

def guardar_como_texto():
    extensiones=(
        ('', '*.*'),
        ('tex','*.txt'),
        ('python', '*.py'),
        ('C++', '*.cpp'),
        ('C#', '*.cs')
    )
    archivo = asksaveasfile(filetypes = extensiones, defaultextension = extensiones)
    if archivo:
            archivo.write(str(texto1.get(1.0, "end")))
            archivo.close()

def buscar_texto():
    texto_de_busqueda = texto1.get("1.0", tk.END)
    lineas = texto_de_busqueda.splitlines()
    palabra_para_buscar_text = palabra_para_buscar.get()
    buscador = re.escape(palabra_para_buscar_text)
    patas = re.compile(buscador)

    texto1.tag_remove("highlight", "1.0", tk.END)
    #codigo robado me canse de intentar y no me salia 
    #procedi a buscar codigos y me fije que estaba haciendo mal 
    #la busqueda en el for y pues procedi a usar la tecnica milenaria XD
    '''En resumen el buscador en el ciclo for (para) enumera las lineas para que el segundo
    ciclo proceda hacer la buscaqueda llevando un orden logico y cuando encuentra el resultado 
    procede a resaltarlo de color amarillo y la fuente de la letra en color negro''' 
    for linea_num, linea in enumerate(lineas):
        start_idx = f"{linea_num + 1}.0"
        end_idx = f"{linea_num + 1}.end"

        for match in patas.finditer(linea):
            start = f"{linea_num + 1}.{match.start()}"
            end = f"{linea_num + 1}.{match.end()}"
            texto1.tag_add("highlight", start, end)
    
    texto1.tag_config("highlight", background="yellow", foreground="black")
'''Para hacer el uso de ciertos recursos se procedio a la instalacion de algunas librerias que 
se debe de hacer de forma manual, con ayuda de la trermina despues de hacer la instalacion con PYP
podemos hacer uso de los recursos que nos ofrece la libreria (pip install accelerate)'''
def copiar_archivo():
    texto1.event_generate("<<Copy>>")
def pegar_archivo():
    texto1.event_generate("<<Paste>>")
def cortar_archivo():
    texto1.event_generate("<<Cut>>")

'''Se realizo este menu utilizando los comandos '''
menu_formuario=tk.Menu()
opciones_menu=tk.Menu(menu_formuario, tearoff=False)
opciones_menu.add_command(
    label="Abrir",
    accelerator="Ctrl+O",
    command=abrir_texto
)

opciones_menu.add_command(
    label="Guardar",
    accelerator="Ctrl+G",
    command=guardar   
)
opciones_menu.add_command(
    label="Guardar como",
    accelerator="Alt+F,A",
    command=guardar_como_texto
)
opciones_menu.add_command(
    label="Buscar",
    accelerator="Ctrl+B"
)
menu_formuario.add_cascade(menu=opciones_menu, label="Archivo")
editar_menu=tk.Menu(menu_formuario, tearoff=False)
editar_menu.add_command(
    label="Deshcer",
    accelerator="Ctrl+Z",
    command=deshacer_archivo
)
editar_menu.add_command(
    label="Rehacer",
    accelerator="Ctrl+Y",
    command=rehacer_texto

)
menu_formuario.add_cascade(menu=editar_menu, label="Editar")
ayuda_menu=tk.Menu(menu_formuario, tearoff=False)
ayuda_menu.add_command(
    label="Informacion"
)
ayuda_menu.add_command(
    label="Manuel de usuario"
)
ayuda_menu.add_command(
    label="Integrantes",
    command=mensaje_integrantes
)
menu_formuario.add_cascade(menu=ayuda_menu, label="Ayuda")


'''Asignacion de los comandos en los diferentes botones que se crearon para el proyecto
adicional se les modifico el tamaño para que fuera mas agradable a la vista del usuario'''
boton_guardar=ttk.Button(text="Guardar", command=guardar)
boton_guardar.place(x=700, y=700, width=150,height=75)
boton_guardar_como=ttk.Button(text="Guardar como", command=guardar_como_texto)
boton_guardar_como.place(x=700, y=800, width=150,height=75)
boton_abrir=ttk.Button(main_window,text="Abrir", command=abrir_texto)
boton_abrir.place(x=700, y=200, width=150,height=40)
boton_buscar=ttk.Button(text="Buscar", command=buscar_texto)
boton_buscar.place(x=700, y=140, width=150,height=40)
boton_copiar=ttk.Button(main_window, text="copiar", command=copiar_archivo)
boton_copiar.place(x=700, y=300, width=75, height=50)
boton_pegar=ttk.Button(main_window, text="pegar", command=pegar_archivo)
boton_pegar.place(x=780, y=300, width=75, height=50)
boton_cortar=ttk.Button(main_window, text="cortar", command=cortar_archivo)
boton_cortar.place(x=700, y=350, width=75, height=50)
boton_deshacer=ttk.Button(text="deshacer", command=deshacer_archivo)
boton_deshacer.place(x=700, y=400,width=75,height=50)
boton_rehacer=ttk.Button(text="rehacer", command=rehacer_texto)
boton_rehacer.place(x=780, y=400,width=75,height=50)

'''Se realizo esta funcion ya que al abrir un archivo y cerrarlo se perdian los datos del archivo 
y para no perder la informacion se decidio utilizar la funcion guardar realizada en la parte de arriva 
y el .destroy que sirve para destruir el widget, entonces, primero guarda cambios y despues se destruye 
el widget'''
def salir_guardando_los_cambios_para_no_perder_nada():
    guardar()
    main_window.destroy()
boton_salida=ttk.Button(text="Salir", command=salir_guardando_los_cambios_para_no_perder_nada)
boton_salida.place(x=700, y=600, width=150,height=75)

main_window.protocol("WM_DELETE_WINDOW", salir_guardando_los_cambios_para_no_perder_nada)


main_window.config(menu=menu_formuario)
'''Para mostrar el widget o el userform en otros programas, se utiliza un comando para mostrar el 
widget (.mainloop())'''
main_window.mainloop()