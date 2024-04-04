import json
from datetime import datetime
import os
from config.config import routes_Usuarios, routes_Productos, routes_Usuario_Iniciado, routes_Ventas

class Registro:
    def __init__(self, Nombre, Apellido, Nacimiento, Usuario, Correo, Contraseña):
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Nacimiento = Nacimiento
        self.Usuario = Usuario
        self.Correo = Correo
        self.Contraseña = Contraseña

    def ID_Mayor(self):
        try:
            with open(routes_Usuarios, 'r') as file:
                usuarios = json.load(file)
            return max(usuario["ID"] for usuario in usuarios)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def to_dict(self):
        ID = self.ID_Mayor() + 1
        Datos = {
            'Nombre': self.Nombre,
            'Apellido': self.Apellido,
            'Nacimiento': self.Nacimiento,
            'Usuario': self.Usuario,
            'Correo': self.Correo,
            'Contrasenia': self.Contraseña
        }
        Usuario = {
            'Datos': Datos,
            'ID': ID
        }
        return Usuario

    def guardar_usuario(self):
        usuario_dict = self.to_dict()

        try:
            with open(routes_Usuarios, 'r') as file:
                usuarios = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            usuarios = []

        for usuario in usuarios:
            if usuario['Datos']['Usuario'] == self.Usuario or usuario['Datos']['Correo'] == self.Correo:
                print("Usuario o correo ya registrados. No se pudo guardar.")
                return

        usuarios.append(usuario_dict)

        try:
            with open(routes_Usuarios, 'w') as file:
                json.dump(usuarios, file, indent=4, sort_keys=True)
                print("Usuario registrado exitosamente.")
        except Exception as e:
            print(f"Error al intentar guardar el usuario: {e}")

class Inicio:
    def __init__(self, Ingresante, contraseña):
        self.Ingresante = Ingresante
        self.contraseña = contraseña
        self.Usuario = None
        self.ID_Usuario = None

    def get_Usuario(self):
        return self.Usuario

    def set_Usuario(self, Usuario):
        self.Usuario = Usuario

    def get_ID_Usuario(self):
        return self.ID_Usuario

    def set_ID_Usuario(self, ID_Usuario):
        self.ID_Usuario = ID_Usuario

    def Comprobar(self):
        UserBool = False
        PasswordBool = False
        with open(routes_Usuarios, 'r') as file:
            usuarios = json.load(file)

        for usuario in usuarios:
            if usuario['Datos']['Usuario'] == self.Ingresante or usuario['Datos']['Correo'] == self.Ingresante:
                UserBool = True
                self.set_Usuario(usuario['Datos']['Usuario'])
                self.set_ID_Usuario(usuario['ID'])
                with open(routes_Usuario_Iniciado, 'w') as file:
                    json.dump(usuario, file, indent=4)
            else:
                UserBool = False
                print('!ERROR NO EXISTE USUARIO¡')
            if usuario['Datos']['Contrasenia'] == self.contraseña:
                PasswordBool = True
            else:
                PasswordBool = False
                print("!CONTRASEÑA MAL NO COINCIDE CON EL USUARIO REGISTRADO¡")

        return UserBool and PasswordBool

class Productos:
    def __init__(self, Producto, Cantidad, Precio):
        self.Producto = Producto
        self.Cantidad = Cantidad
        self.Precio = Precio
        self.Total = None

    def calcular_total(self):
        try:
            cantidad = int(self.Cantidad)
            precio = float(self.Precio)
            self.Total = cantidad * precio
        except ValueError:
            self.Total = None

    @staticmethod
    def obtener_ventas():
        try:
            with open(routes_Productos, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def obtener_proximo_id():
        ventas = Productos.obtener_ventas()
        return max((int(venta.get('ID', 0)) for venta in ventas), default=0) + 1

    def to_dict(self):
        ID_venta = Productos.obtener_proximo_id()
        self.calcular_total()

        datos = {
            'ID': str(ID_venta),
            'Producto': self.Producto,
            'Cantidad': self.Cantidad,
            'Precio': self.Precio,
            'Total': self.Total,
        }

        venta = {
            'Datos': datos,
            'ID': str(ID_venta)
        }

        return venta

    def guardar_venta(self):
        datos = self.to_dict()
        try:
            with open(routes_Productos, 'r') as file:
                ventas = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            ventas = []

        ventas.append(datos)

        with open(routes_Productos, 'w') as file:
            json.dump(ventas, file, indent=4, sort_keys=True)

        return datos

    @staticmethod
    def eliminar_producto(id_producto):
        try:
            ventas = Productos.obtener_ventas()
            
            print("Ventas antes de la eliminación:")
            print(ventas)

            id_producto_str = str(id_producto)

            ventas_actualizadas = [venta for venta in ventas if venta['ID'] != id_producto_str]

            print("\nVentas después de la eliminación:")
            print(ventas_actualizadas)

            with open(routes_Productos, 'w') as file:
                json.dump(ventas_actualizadas, file, indent=4, sort_keys=True)
                print(f"Producto con ID {id_producto_str} eliminado exitosamente.")

        except Exception as e:
            print(f"Error al intentar eliminar el producto: {e}")

class Venta(Inicio):
    def __init__(self, Ingresante=None, contraseña=None):
        super().__init__(Ingresante, contraseña)
        self.Cliente = None
        self.Fecha = datetime.now()
        self.Compra = []
        self.Total = 0

    def obtener_usuario_logueado(self):
        try:
            with open(routes_Usuario_Iniciado, 'r') as file:
                usuario = json.load(file)
            return usuario
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def cargar_ventas(self):
        try:
            with open(routes_Ventas, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def cargar_compra(self):
        with open(routes_Productos, 'r') as file:
            productos = json.load(file)
            self.Compra = [venta['Datos'] for venta in productos]

    def cargar_total(self):
        self.Total = sum(float(venta['Total']) for venta in self.Compra)

    def ID_Mayor(self):
        ventas = self.cargar_ventas()
        print("DEBUG: ventas cargadas:", ventas)
        if ventas:
            return max(int(venta['Datos']['Cliente']) for venta in ventas)
        else:
            return 0

    def to_dict(self):
        self.Cliente = self.ID_Mayor() + 1
        self.cargar_compra()
        self.cargar_total()

        usuario_logueado = self.obtener_usuario_logueado()
        if usuario_logueado:
            Usuario = usuario_logueado.get('Datos', {}).get('Usuario', '')
            ID_Comprador = usuario_logueado.get('ID', '')

        datos = {
            'Nombre': Usuario,
            'ID Comprador': ID_Comprador,
            'Cliente': self.Cliente,
            'Fecha': str(self.Fecha),
            'Compra': self.Compra,
            'Total': self.Total
        }

        venta = {
            'Datos': datos,
            'ID': self.Cliente
        }

        return venta

    def guardar_datos(self):
        compra_dict = self.to_dict()

        if compra_dict is None:
            print("ERROR: to_dict retornó None")
            return

        compras = self.cargar_ventas()
        compras.append(compra_dict)

        fecha_formateada = datetime.strptime(compra_dict["Datos"]["Fecha"], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d_%H-%M-%S")

        with open(routes_Ventas, 'w') as file:
            json.dump(compras, file, indent=4, sort_keys=True)
            print("Compra registrada exitosamente.")

        ticket_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'ticket_{fecha_formateada}.txt')
        with open(ticket_path, 'w') as ticket_file:
            ticket_file.write(f'Ticket de Compra\n\n')
            ticket_file.write(f'Cliente: {compra_dict["Datos"]["Nombre"]}\n')
            ticket_file.write(f'Fecha: {compra_dict["Datos"]["Fecha"]}\n\n')
            
            ticket_file.write(f'{"Producto": <20} {"Cantidad": <10} {"Precio": <10} {"Total": <10}\n')
            ticket_file.write('-' * 60 + '\n')

            for producto in compra_dict["Datos"]["Compra"]:
                ticket_file.write(f'{producto["Producto"][:20]: <20} {producto["Cantidad"]: <10} {producto["Precio"]: <10} {producto["Total"]: <10}\n')

            ticket_file.write('-' * 60 + '\n')
            ticket_file.write(f'Total: {compra_dict["Datos"]["Total"]}\n')

        print(f'Ticket de compra guardado en: {ticket_path}')

        return compra_dict