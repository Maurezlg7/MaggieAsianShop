import json
import tkinter as tk
from tkinter import Frame, ttk, messagebox, font
from tkcalendar import DateEntry
from src.models import *
from config.config import *

class LoginVentana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión")
        self.configure(bg="#fff")
        self.resizable(False, False)
        width = 905
        height = 500
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.iconbitmap(icon_path)

        self.Donuts = font.Font(family="Monday Donuts", size=25)

        self.original_image = tk.PhotoImage(file=imagen_path)
        self.scaled_image = self.original_image.subsample(5, 5)
        tk.Label(self, image=self.scaled_image, bg='white').place(x=50, y=50)

        self.frame = Frame(self, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)

        self.heading = tk.Label(self.frame, text='Inicio Sesión', fg='#F700FF', bg='white', font=(self.Donuts, 25))
        self.heading.place(x=100, y=5)

        self.Ingresante = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white')
        self.Ingresante.place(x=45, y=80)
        self.Ingresante.insert(0, 'Usuario o Correo Electronico')
        self.Ingresante.bind('<FocusIn>', self.on_enter)
        self.Ingresante.bind('<FocusOut>', self.on_leave)
        self.linea_ingresante = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_ingresante.place(x=40, y=107)

        self.Contraseña = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white', show='*')
        self.Contraseña.place(x=45, y=140)
        self.Contraseña.insert(0, 'Contraseña')
        self.Contraseña.bind('<FocusIn>', self.on_enter_password)
        self.Contraseña.bind('<FocusOut>', self.on_leave_password)
        self.linea_contraseña = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_contraseña.place(x=40, y=167)

        tk.Button(self.frame, width=39, pady=7, text='Acceder', bg='#F538C3', fg='white', border=0, command=self.iniciar_sesion).place(x=50, y=204)
        tk.Label(self.frame, text='¿No tienes una cuenta?', fg='black', bg='white', font=9).place(x=70, y=270)
        self.Entrar = tk.Button(self.frame, width=8, text='Registrate', border=0, bg='white', cursor='hand2', fg='#5965FF', font=9, command=self.abrir_registro)
        self.Entrar.place(x=240, y=268)
    
    def abrir_registro(self):
        self.withdraw()
        registro = RegistroVentana(self)
        registro.protocol("WM_DELETE_WINDOW", self.cerrar_registro)
        registro.mainloop()

    def cerrar_registro(self):
        self.deiconify()

    def on_enter(self, event):
        if self.Ingresante.get() == 'Usuario o Correo Electronico':
            self.Ingresante.delete(0, 'end')

    def on_enter_password(self, event):
        if self.Contraseña.get() == 'Contraseña':
            self.Contraseña.delete(0, 'end')

    def on_leave(self, event):
        if not self.Ingresante.get():
            self.Ingresante.insert(0, 'Usuario o Correo Electronico')

    def on_leave_password(self, event):
        if not self.Contraseña.get():
            self.Contraseña.insert(0, 'Contraseña')

    def iniciar_sesion(self):
        usuario = self.Ingresante.get()
        contraseña = self.Contraseña.get()

        usuario_login = Inicio(usuario, contraseña)
        try:
            if usuario_login.Comprobar():
                print("Inicio de sesión exitoso")
                self.Tabla = TablaDatos()
                self.Tabla.lift()
                self.Tabla.focus_force()

                self.withdraw()
            else:
                messagebox.showerror("Error", "Usuario no existe o ingresó mal un dato")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")




class RegistroVentana(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro")
        self.configure(bg="#fff")
        self.resizable(False, False)
        width = 925
        height = 500
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.iconbitmap(icon_path)

        self.original_image = tk.PhotoImage(file=imagen_path)
        self.scaled_image = self.original_image.subsample(5, 5)
        tk.Label(self, image=self.scaled_image, bg='white').place(x=50, y=50)

        self.frame = Frame(self, width=350, height=400, bg='white')
        self.frame.place(x=480, y=70)

        self.heading = tk.Label(self.frame, text='Registro', fg='#F700FF', bg='white', font=(Donuts, 25))
        self.heading.place(x=125, y=0)
        
        self.Nombre = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white')
        self.Nombre.place(x=45, y=70)
        self.Nombre.insert(0, 'Nombre/s')
        self.Nombre.bind('<FocusIn>', self.on_enter_name)
        self.Nombre.bind('<FocusOut>', self.on_leave_name)
        self.linea_Nombre = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_Nombre.place(x=40, y=95)

        self.Apellido = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white')
        self.Apellido.place(x=45, y=110)
        self.Apellido.insert(0, 'Apellido/s')
        self.Apellido.bind('<FocusIn>', self.on_enter_surname)
        self.Apellido.bind('<FocusOut>', self.on_leave_surname)
        self.linea_Apellido = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_Apellido.place(x=40, y=135)

        self.Nacimiento = DateEntry(self.frame, width=25, background='darkblue', foreground='white', borderwidth=0)
        self.Nacimiento.place(x=45, y=150)

        self.Usuario = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white')
        self.Usuario.place(x=45, y=190)
        self.Usuario.insert(0, 'Usuario')
        self.Usuario.bind('<FocusIn>', self.on_enter_user)
        self.Usuario.bind('<FocusOut>', self.on_leave_user)
        self.linea_Usuario = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_Usuario.place(x=40, y=215)

        self.Correo = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white')
        self.Correo.place(x=45, y=230)
        self.Correo.insert(0, 'Correo')
        self.Correo.bind('<FocusIn>', self.on_enter_mail)
        self.Correo.bind('<FocusOut>', self.on_leave_mail)
        self.linea_Correo = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_Correo.place(x=40, y=255)

        self.Contraseña = tk.Entry(self.frame, width=25, fg='black', border=0, bg='white', show='*')
        self.Contraseña.place(x=45, y=270)
        self.Contraseña.insert(0, 'Contraseña')
        self.Contraseña.bind('<FocusIn>', self.on_enter_password)
        self.Contraseña.bind('<FocusOut>', self.on_leave_password)
        self.linea_Contraseña = Frame(self.frame, width=295, height=2, bg='black')
        self.linea_Contraseña.place(x=40, y=295)

        tk.Button(self.frame, width=39, pady=7, text='Registrarse', bg='#F538C3', fg='white', border=0, command=self.registrar_usuario).place(x=50, y=320)
        tk.Label(self.frame, text='¿Ya tienes una cuenta?', fg='black', bg='white', font=9).place(x=70, y=360)
        self.Entrar = tk.Button(self.frame, width=8, text='Ingresa', border=0, bg='white', cursor='hand2', fg='#5965FF', font=9, command=self.volver_login)
        self.Entrar.place(x=235, y=358)

    def volver_login(self):
        self.destroy()
        self.master.deiconify()

    def registrar_usuario(self):
        nombre = self.Nombre.get()
        apellido = self.Apellido.get()
        nacimiento = self.Nacimiento.get()
        usuario = self.Usuario.get()
        correo = self.Correo.get()
        contraseña = self.Contraseña.get()

        nuevo_usuario = Registro(nombre, apellido, nacimiento, usuario, correo, contraseña)

        nuevo_usuario.guardar_usuario()
        
    """----------------ENTER----------------------"""

    def on_enter_name(self, event):
        if self.Nombre.get() == 'Nombre/s':
            self.Nombre.delete(0, 'end')

    def on_enter_surname(self, event):
        if self.Apellido.get() == 'Apellido/s':
            self.Apellido.delete(0, 'end')

    def on_enter_user(self, event):
        if self.Usuario.get() == 'Usuario':
            self.Usuario.delete(0, 'end')

    def on_enter_mail(self, event):
        if self.Correo.get() == 'Correo':
            self.Correo.delete(0, 'end')

    def on_enter_password(self, event):
        if self.Contraseña.get() == 'Contraseña':
            self.Contraseña.delete(0, 'end')

    """----------------LEAVE----------------------"""

    def on_leave_name(self, event):
        if not self.Nombre.get():
            self.Nombre.insert(0, 'Nombres/s')

    def on_leave_surname(self, event):
        if not self.Apellido.get():
            self.Apellido.insert(0, 'Apellido/s')

    def on_leave_user(self, event):
        if not self.Usuario.get():
            self.Usuario.insert(0, 'Usuario')
    
    def on_leave_mail(self, event):
        if not self.Correo.get():
            self.Correo.insert(0, 'Correo')

    def on_leave_password(self, event):
        if not self.Contraseña.get():
            self.Contraseña.insert(0, 'Contraseña')

class TablaDatos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro")
        self.configure(bg="#FFBCD9")
        self.resizable(False, False)
        width = 925
        height = 500
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.protocol("WM_DELETE_WINDOW", self.cerrar_programa)
        self.Venta_x_cliente = Venta()

        self.iconbitmap(icon_path)

        self.venta_instancia = Venta()

        self.tree = ttk.Treeview(self, padding=10)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.tree["columns"] = ("ID", "Producto", "Cantidad", "Precio", "Total")

        self.tree.heading("ID", text="ID", anchor='center')
        self.tree.heading("Producto", text="Producto", anchor='center')
        self.tree.heading("Cantidad", text="Cantidad", anchor='center')
        self.tree.heading("Precio", text="Precio", anchor='center')
        self.tree.heading("Total", text="Total", anchor='center')

        self.tree.column("#0", stretch=False, minwidth=0, width=0)
        column_width = width // 5
        self.tree.column("ID", stretch=False, minwidth=0, width=column_width, anchor='center')
        self.tree.column("Producto", stretch=False, minwidth=0, width=column_width, anchor='center')
        self.tree.column("Cantidad", stretch=False, minwidth=0, width=column_width, anchor='center')
        self.tree.column("Precio", stretch=False, minwidth=0, width=column_width, anchor='center')
        self.tree.column("Total", stretch=False, minwidth=0, width=column_width, anchor='center')

        self.cargar_datos_desde_json(routes_Productos)

        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self, bg="#FFBCD9")
        button_frame.pack(side=tk.LEFT, padx=220, pady=10)

        self.boton(button_frame, "Añadir", self.abrir_ventana_añadir)
        self.boton(button_frame, "Comprar", self.Hacer_Compra)
        self.boton(button_frame, "Eliminar", self.eliminar_producto)
        self.boton(button_frame, "Editar", self.boton_editar)
        self.boton(button_frame, "Salir", self.cerrar_programa)

        self.update_idletasks()
        self.state("normal")

        self.id_seleccionado = None
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_item)

    def boton(self, button_frame, texto, comando):
        boton = tk.Button(button_frame, text=texto, command=comando, bg='#5FD1EB', fg='black', font=20, width=7)
        boton.config(borderwidth=0, highlightthickness=0, bd=0, padx=3, pady=3)
        boton.pack(side=tk.LEFT, padx=10)
        return boton

    def seleccionar_item(self, event):
        item = self.tree.selection()
        if item:
            self.id_seleccionado = self.tree.item(item, 'values')[0]
        else:
            self.id_seleccionado = None

    def Hacer_Compra(self):
        self.venta_instancia.guardar_datos()

        for item in self.tree.get_children():
            self.tree.delete(item)

        with open(routes_Productos, 'w') as file:
            file.truncate()

    def cerrar_programa(self):
        self.master.destroy()

    def eliminar_producto(self):
        if self.id_seleccionado:
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[0] == str(self.id_seleccionado):
                    self.tree.delete(item)

            Productos.eliminar_producto(int(self.id_seleccionado))

            self.id_seleccionado = None


    def cargar_datos_desde_json(self, json_path):
        try:
            with open(json_path, 'r') as file:
                datos = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = []

        for idx, venta in enumerate(datos, start=1):
            id_venta = venta.get('ID', idx)
            Producto = venta['Datos'].get('Producto', '')
            Cantidad = venta['Datos'].get('Cantidad', '')
            Precio = venta['Datos'].get('Precio', '')
            Total = venta['Datos'].get('Total', '')

            self.tree.insert("", "end", values=(id_venta, Producto, Cantidad, Precio, Total))

    def boton_editar(self):
        if self.id_seleccionado:
            ventana_editar = tk.Toplevel(self)
            ventana_editar.title("Editar Cantidad")
            ventana_editar.configure(bg="#5AB5E6")
            ventana_editar.resizable(False, False)
            width = 300
            height = 200
            x = (self.winfo_screenwidth() - width) // 2
            y = (self.winfo_screenheight() - height) // 2
            ventana_editar.geometry(f"{width}x{height}+{x}+{y}")

            ventana_editar.iconbitmap(icon_path)

            custom_font = font.Font(family="Arial", size=15, weight="bold")

            tk.Label(ventana_editar, text="Nueva Cantidad:", bg='#5AB5E6', fg='white', font=custom_font).pack(pady=10)
            entry_nueva_cantidad = tk.Entry(ventana_editar)
            entry_nueva_cantidad.pack(pady=10)

            def aplicar_edicion():
                nueva_cantidad = entry_nueva_cantidad.get()
                if nueva_cantidad.isdigit() and int(nueva_cantidad) >= 0:
                    # Obtener los valores actuales
                    for item in self.tree.get_children():
                        if self.tree.item(item, 'values')[0] == str(self.id_seleccionado):
                            valores_actuales = self.tree.item(item, 'values')
                            id_producto, producto_actual, cantidad_actual, precio_actual, total_actual = valores_actuales

                            nuevo_total = float(precio_actual) * int(nueva_cantidad)

                            self.tree.item(item, values=(id_producto, producto_actual, nueva_cantidad, precio_actual, nuevo_total))

                            self.guardar_datos_en_json()

                            ventana_editar.destroy()
                else:
                    tk.messagebox.showerror("Error", "La cantidad debe ser un número entero no negativo.")

            tk.Button(ventana_editar, text="Aplicar Edición", command=aplicar_edicion).pack(pady=10)

    def guardar_datos_en_json(self):
        datos = []
        for item in self.tree.get_children():
            valores = self.tree.item(item, 'values')
            id_venta, producto, cantidad, precio, total = valores
            datos.append({
                'ID': id_venta,
                'Datos': {
                    'Producto': producto,
                    'Cantidad': cantidad,
                    'Precio': precio,
                    'Total': total
                }
            })

        with open(routes_Productos, 'w') as file:
            json.dump(datos, file, indent=4, sort_keys=True)

    def Opciones_Productos(self):
        with open(routes_Lista_Productos, 'r') as file:
            diccionario_productos = json.load(file)
        return diccionario_productos

    def abrir_ventana_añadir(self):
        ventana_añadir = tk.Toplevel(self)
        ventana_añadir.title("Añadir Producto")
        ventana_añadir.configure(bg="#5AB5E6")
        ventana_añadir.resizable(False, False)
        width = 400
        height = 300
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        ventana_añadir.geometry(f"{width}x{height}+{x}+{y}")

        ventana_añadir.iconbitmap(icon_path)

        custom_font = font.Font(family="Arial", size=15, weight="bold")

        tk.Label(ventana_añadir, text="Producto:", bg='#5AB5E6', fg='white', font=custom_font).pack(pady=10)
        combo = ttk.Combobox(ventana_añadir, values=self.Opciones_Productos())
        combo.pack(pady=10)

        tk.Label(ventana_añadir, text="Cantidad:", bg='#5AB5E6', fg='white', font=custom_font, padx=20).pack(pady=10)
        entry_cantidad = tk.Entry(ventana_añadir)
        entry_cantidad.pack(pady=10)

        label_precio = tk.Label(ventana_añadir, text="Precio: $0.0", bg='#5AB5E6', fg='white', font=custom_font)
        label_precio.pack(pady=(10, 0))

        self.precios_productos = self.Opciones_Productos()
        combo['values'] = list(self.precios_productos.keys())

        def actualizar_precio(*args):
            producto_seleccionado = combo.get()
            precio = self.precios_productos.get(producto_seleccionado, 0)
            label_precio.config(text=f"Precio: ${precio}")

        combo.bind("<<ComboboxSelected>>", actualizar_precio)

        def añadir_registro():
            producto = combo.get()
            cantidad = entry_cantidad.get()
            precio = self.precios_productos.get(producto, 0)

            if producto and cantidad and precio:
                for item in self.tree.get_children():
                    if self.tree.item(item, 'values')[1] == producto:
                        valores_actuales = self.tree.item(item, 'values')
                        id_producto, producto_actual, cantidad_actual, precio_actual, total_actual = valores_actuales

                        nueva_cantidad = int(cantidad_actual) + int(cantidad)
                        nuevo_total = nueva_cantidad * float(precio)

                        self.tree.item(item, values=(id_producto, producto_actual, nueva_cantidad, precio_actual, nuevo_total))

                        self.guardar_datos_en_json()

                        ventana_añadir.destroy()
                        return

                nueva_venta = Productos(producto, cantidad, precio)
                nueva_venta.calcular_total()
                venta_dict = nueva_venta.guardar_venta()
                nuevo_id = venta_dict['ID']
                self.tree.insert("", "end", values=(nuevo_id, producto, cantidad, precio, venta_dict['Datos']['Total']))

                self.guardar_datos_en_json()

                ventana_añadir.destroy()
            else:
                tk.messagebox.showerror("Error", "Todos los campos son obligatorios")

        tk.Button(ventana_añadir, text="Añadir", command=añadir_registro).pack(pady=10)

