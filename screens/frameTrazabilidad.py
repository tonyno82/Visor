import tkinter as tk
from tkinter import StringVar, ttk
from PIL import ImageTk, Image
from pathlib import Path

class FrameTraza(tk.Frame):
    def __init__(self, manager):
        super().__init__(manager)
        self.configure(height=980, width=1280)
        # background='#fcba03', 
        self.manager = manager
        self.logger = self.manager.logger
        self.gestionBBDD = self.manager.gestionBBDD
        self.referenciaIntroducida = StringVar()
        self.diccionarioReferenciasBBDD = {}

        self.menuPopup = tk.Menu(self.manager)
        self.menuPopup.add_command(label='No se encontraron imagenes que mostrar', state=tk.DISABLED)
        self.menuPopup.add_separator()
        self.contadorItemMenu = 1

        self._iniciarFrames()
        self._iniciarRecogidaInformacion()
        self.arbol = ttk.Treeview(self.frameArbol)
        self._iniciarVistaInferiorArbol()

    def _iniciarVistaInferiorArbol(self):
        columnas = self.gestionBBDD.listadoColumnas()
        self.arbol['columns'] = columnas
        for nombre in columnas:
            tamanoColumna = len(nombre)*8
            self.arbol.column(nombre, width=tamanoColumna, anchor='center')
            self.arbol.heading(nombre, text=nombre)
        self.arbol.place(height=760, width=1260)
        self.scrollx = tk.Scrollbar(self.frameArbol, orient="horizontal", command=self.arbol.xview)
        self.scrolly = tk.Scrollbar(self.frameArbol, orient="vertical", command=self.arbol.yview)
        self.scrollx.place(relx=0, y=760, height=20, relwidth=1)
        self.scrolly.place(rely=0, x=1260, width=20, relheight=1)
        self.arbol.configure(xscrollcommand=self.scrollx.set)
        self.arbol.configure(yscrollcommand=self.scrolly.set)
        self.arbol.bind('<3>', self._crearMenuPopup)
        # self.arbol.bind('<<TreeviewSelect>>', self._imprimeValor)

    def _crearMenuPopup(self, evento):
        # Limpio el menu
        if self.contadorItemMenu > 2:
            for numeroItem in range(2, self.contadorItemMenu):
                self.menuPopup.delete(numeroItem, 'end')
        self.contadorItemMenu = 1
        self.gestionArchivos = self.manager.gestionArchivos
        itemSeleccionado = self.arbol.selection()[0]
        if 'ID' in itemSeleccionado:
            listaValoresSeleccionados = self.arbol.item(itemSeleccionado)["values"]
            listaImagenes = list(filter(lambda item: '.jpeg' in str(item) or '.bmp' in str(item),listaValoresSeleccionados))
            diccionarioImagenesEncontradas = self.gestionArchivos.buscaArchivos(listaImagenes)
        if not diccionarioImagenesEncontradas:
            self.menuPopup.entryconfigure(0, label='No se encontraron imagenes que mostrar')
        else:
            for foto in diccionarioImagenesEncontradas:
                self.contadorItemMenu += 1
                self.rutaFotoFinal = diccionarioImagenesEncontradas[foto]
                self.menuPopup.entryconfigure(0, label='Fotos encontradas:')
                self.menuPopup.add_command(label=foto, command=lambda i = self.rutaFotoFinal: self._presentarFoto(i))
                print(self.rutaFotoFinal)

        self.menuPopup.post(evento.x_root, evento.y_root)
        
    def _presentarFoto(self, foto):
        self.foto = foto
        self.logger.debug(f'Sacando por pantalla {foto}')
        self.ventanaFoto = tk.Toplevel(self.manager)
        self.frameFoto = tk.Frame(self.ventanaFoto)
        self.frameFoto.grid(column=0, row=0)
        self.frameFoto.rowconfigure(0, weight=1)
        self.frameFoto.columnconfigure(0, weight=1)
        self.imagen = Image.open(self.foto)
        self.imagentk = ImageTk.PhotoImage(self.imagen)
        self.logger.debug(self.imagen.size)
        self.laberImagen = tk.Label(self.frameFoto, text = self.foto, image=self.imagentk, compound='top')
        self.laberImagen.pack()
        

    def _buscarItem(self):
        contador = 0
        self._borrarArbol()
        referenciaIntroducida = self.referenciaIntroducida.get()
        listaReferenciasEncontradas = self.gestionBBDD.encuentraReferencia(referenciaIntroducida)
        for lineaCompleta in listaReferenciasEncontradas:
            self.diccionarioReferenciasBBDD.setdefault(lineaCompleta[1], [])
            self.diccionarioReferenciasBBDD[lineaCompleta[1]].append(lineaCompleta)
        for referenciaCorta in self.diccionarioReferenciasBBDD:
            self.arbol.insert('', 'end', referenciaCorta, text=referenciaCorta)
            for linea in self.diccionarioReferenciasBBDD[referenciaCorta]:
                self.arbol.insert(referenciaCorta, 'end', 'ID' + str(contador), text=linea[0], values=linea)
                contador += 1
        
    def _iniciarFrames(self):
        self.frameIntrudirDatos = tk.Frame(self)
        self.frameIntrudirDatos.configure( height=200, width=1280, padx=10, pady=30)
        # background='#1403fc',
        self.frameIntrudirDatos.grid(column=0, row=0)
        self.frameIntrudirDatos.grid_propagate(False)

        self.frameArbol = tk.Frame(self)
        self.frameArbol.configure(background='#d203fc', height=780, width=1280)
        self.frameArbol.grid(column=0, row=1)
        self.frameArbol.grid_propagate(False)

    def _borrarTodo(self):
        self._borrarArbol()
        self.cuadroTexto.delete(0, 'end')
    
    def _borrarArbol(self):
        if self.diccionarioReferenciasBBDD:
            for item in self.diccionarioReferenciasBBDD:
                self.arbol.delete(item)
        self.diccionarioReferenciasBBDD = {}


    def _iniciarRecogidaInformacion(self):

        self.labelTextoaBuscar = tk.Label(self.frameIntrudirDatos, text='Referencia a buscar :')
        self.labelTextoaBuscar.grid(column=0, row=0, sticky=tk.W, pady=5)

        self.cuadroTexto = ttk.Entry(self.frameIntrudirDatos, textvariable=self.referenciaIntroducida, width=50)
        self.cuadroTexto.grid(column=0, row=1, pady=5)

        self.frameBotones = tk.Frame(self.frameIntrudirDatos)
        self.frameBotones.grid(column=0, row=2, sticky=tk.W, pady=5)

        self.botonBuscar = ttk.Button(self.frameBotones, text='Buscar', command=self._buscarItem)
        self.botonBuscar.grid(column=0, row=0, pady=5)

        self.botonBorrar = ttk.Button(self.frameBotones, text='Borrar', command=self._borrarTodo)
        self.botonBorrar.grid(column=1, row=0, pady=5)
