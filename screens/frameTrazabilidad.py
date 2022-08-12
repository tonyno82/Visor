from distutils.cmd import Command
import tkinter as tk
from tkinter import StringVar, ttk

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
        self.arbol.bind('<3>', self._imprimeValor)
        # self.arbol.bind('<<TreeviewSelect>>', self._imprimeValor)


    def _imprimeValor(self, evento):
        self.gestionArchivos = self.manager.gestionArchivos
        itemSeleccionado = self.arbol.selection()[0]
        if 'ID' in itemSeleccionado:
            print(evento)
            listaValoresSeleccionados = self.arbol.item(itemSeleccionado)["values"]
            listaImagenes = list(filter(lambda item: '.jpeg' in str(item) or '.bmp' in str(item),listaValoresSeleccionados))
            diccionarioImagenesEncontradas = self.gestionArchivos.buscaArchivos(listaImagenes)
            print(diccionarioImagenesEncontradas)

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
