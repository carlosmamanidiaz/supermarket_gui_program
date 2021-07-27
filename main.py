import sys
import requests
import pickle
import cognitive_face as CF
from PIL import Image, ImageDraw, ImageFont
import datetime

SUBSCRIPTION_KEY = 'key'
BASE_URL = 'url'

CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

class Persona():
	"""La clase Persona"""

	def __init__(self, person_id, name, gender, age, picture):
		"""Contructor"""
		self.person_id = person_id
		self.name = name
		self.gender = gender 
		self.age = age
		self.picture = picture
class Cajero(Persona):
	"""Clase Cajero que hereda de Persona"""
	def __init__(self, person_id, name, gender, age, picture, turno, horas_laboradas):
		"""Constructor"""
		Persona.__init__(self, person_id, name, gender, age, picture)
		self.turno = turno
		self.horas_laboradas = horas_laboradas
class Cliente(Persona):
	"""Clase Cliente que hereda de Persona"""

	def __init__(self, person_id, name, gender, age, picture, telefono, email):
		"""Constructor"""
		Persona.__init__(self, person_id, name, gender, age, picture)
		self.telefono = telefono
		self.email = email

class Jefe(Persona):
	"""Clase Jefe que hereda de Persona"""

	def __init__(self, person_id, name, gender, age, picture, area, empleados):
		Persona.__init__(self, person_id, name, gender, age, picture)
		self.area = area
		self.empleados = empleados


class Producto():
	"""Clase Porducto"""

	def __init__(self, id_producto, descripcion, precio):
		self.id_producto = id_producto
		self.descripcion = descripcion
		self.precio = precio

class Venta():
	"""Clase Venta """

	def __init__(self, id_cajero, id_cliente, id_factura, path_foto_cajero, path_foto_cliente, id_productos, precios):
		
		dt = datetime.datetime.now()
		self.fecha = datetime.date(dt.year, dt.month, dt.day)
		self.id_cajero = id_cajero
		self.id_cliente = id_cliente
		self.id_factura = id_factura
		self.path_foto_cajero = path_foto_cajero
		self.path_foto_cliente = path_foto_cliente
		#Lista de productos y lista de precios, se usara de esta forma para ir anadiendo los productos hasta que se detenga el while con la palabra clve : fin
		self.ids_de_productos = id_productos#id_productos es una lista
		self.precios= precios#precios es una lista
		
		# while True:
		# 	id_producto = input('Agregar producto/ No mas productos, digitar fin: ')
		# 	if id_producto != "fin":
		# 		precio = input("Ingresar los precios: ")
		# 		self.ids_de_productos.append((id_producto))
		# 		self.precios.append(float(precio))
		# 	else:
		# 		break
		# Se suma la lista de precios obtenida y se obtiene el monto total, esta sera la propiedad monto		
		self.monto = sum(self.precios)

def create_group(group_id, group_name):
	"""Crear un nuevo grupo de personas.
	Argumentos:
		group_id {int}          -- es el id del grupo
		group_name {str}        -- es el nombre del grupo

	Solo hay que crearlo la primera vez
	"""
	CF.person_group.create(group_id, group_name)
	print("Grupo creado")

def create_person(name, picture,group_name, group_id, p1, p2):
	"""Crear una persona en un grupo
	Argumentos:
		name {str}              -- es el nombre de la persona
		picture     {str}       -- es el path de la foto de la persona
		group_id    {str}       -- es el grupo al que se desea agregar la persona
		p1     {str}       -- es la propiedad exclusiva de cada grupo
		p2    {str}       -- es la propiedad exclusiva de cada grupo
	"""
	response = CF.person.create(group_id, name)
	#print(response)
	#En response viene el person_id de la persona que se ha creado
	# Obtener person_id de response
	person_id = response['personId']
	#print(person_id)
	#Sumarle una foto a la persona que se ha creado
	CF.person.add_face(picture, group_id, person_id)
	#print CF.person.lists(PERSON_GROUP_ID)
	
	#Re-entrenar el modelo porque se le agrego una foto a una persona
	CF.person_group.train(group_id)
	#Obtener el status del grupo
	response = CF.person_group.get_status(group_id)
	status = response['status']
	# print(status)
	#Obtener el genero y la edad usando M.Azure con la funcion emotions
	dic = emotions(picture)
	gender = str(dic[0]['faceAttributes']['gender'])
	age = str(int(dic[0]['faceAttributes']['age']))

	if group_name == "clientes":
		#Hay que llamar a la función emotions para obtener el gender y el age
		with open("clientes.bin", "ab") as f:
			cliente = Cliente(person_id, name, gender, age, picture, p1, p2)
			print('---------')
			print(f'Properties:\nperson_id = {cliente.person_id}\nname = {cliente.name}\ngender = {cliente.gender}\nage = {cliente.age}\ntelefono = {cliente.telefono}\nemail = {cliente.email}\npicture path = {cliente.picture}')
			pickle.dump(cliente, f, pickle.HIGHEST_PROTOCOL)
			print('---------')

	elif group_name == "cajeros":
		with open("cajeros.bin", "ab") as f:
			cajero = Cajero(person_id, name, gender, age, picture, p1, p2)
			print('---------')
			print(f'Properties:\nperson_id = {cajero.person_id}\nname = {cajero.name}\ngender = {cajero.gender}\nage = {cajero.age}\nturno = {cajero.turno}\nhoras_laboradas = {cajero.horas_laboradas}\npicture path = {cajero.picture}')
			print('---------')
			pickle.dump(cajero, f, pickle.HIGHEST_PROTOCOL)

	elif group_name == "jefes":
		with open("jefes.bin", "ab") as f:
			jefe = Jefe(person_id, name, gender, age, picture, p1, p2)
			print('---------')
			print(f'Properties:\nperson_id = {jefe.person_id}\nname = {jefe.name}\ngender = {jefe.gender}\nage = {jefe.age}\narea = {jefe.area}\nempleados = {jefe.empleados}\npicture path = {jefe.picture}')
			print('---------')
			pickle.dump(jefe, f, pickle.HIGHEST_PROTOCOL)

def create_venta (id_cajero, id_cliente, id_factura, path_foto_cajero, path_foto_cliente, id_productos, precios):
	"""Crea una venta y la almacena en un archivo binario, que sera usado para realizar consultas, ademas de las propiedas ingresadas tambien
	estan las propiedades generadas en la clase Venta: fecha, ids_de_productos, precios y monto, donde ids_de_productos y precios son listas de los
	productos y precios ingresados, monto es la suma de la lista precios y fecha es obtenido por la libreria datatime que nos da la fecha actual.
	Argumentos:
		id_cajero {strg}      -- id del cajero
		id_cliente {strg}      -- id del cliente
		id_factura {strg}      -- id de la factura
		path_foto_cajero {strg}      -- es la ruta de la foto del cajero al momento de esa venta
		path_foto_cliente {strg}      -- es la ruta de la foto del cliente al momento de esa venta
		id_producto {strg}      -- id del producto, se puede anadir varios productos 
		precio {strg}      -- precio del producto anteriormente ingresado.
	"""
	response = CF.person.create(5, id_factura)
	with open("ventas.bin", "ab") as f:
		venta = Venta(id_cajero, id_cliente, id_factura, path_foto_cajero, path_foto_cliente, id_productos, precios)
		print('---------')
		print(f'Properties:\nfecha = {venta.fecha}\nid_cajero = {venta.id_cajero}\nid_cliente = {venta.id_cliente}\nid_factura = {venta.id_factura}\nproductos = {venta.ids_de_productos}\nprecios = {venta.precios}\nmonto = {venta.monto}\npicture path cajero = {venta.path_foto_cajero}\npicture path cliente = {venta.path_foto_cliente}')
		print('---------')		
		pickle.dump(venta, f, pickle.HIGHEST_PROTOCOL)
	
def create_product(id_producto, descripcion,precio):
	"""Crea un producto y la almacena en un archivo binario, que sera usado para realizar consultas
	Argumentos:
		id_producto {strg}      -- id del producto
		descripcion {strg}      -- descripcion del producto
		precio {strg}      -- precio del producto
	"""
	response = CF.person.create(4, id_producto)
	with open("productos.bin", "ab") as f:
		produto = Producto(id_producto, descripcion,precio)
		print('---------')
		print(f'Properties:\nid producto = {produto.id_producto}\ndescripcion = {produto.descripcion}\nprecio = {produto.precio}')
		print('---------')
		pickle.dump(produto, f, pickle.HIGHEST_PROTOCOL)

def emotions(picture):
	"""Obtener las emociones de una persona
	Argumentos:
		picture {strg}      -- recibe el path de la foto de la persona que se desea obtener las emociones
	Retorna:
		analysis {lista}    -- retorna la lista con los diccionarios de los rostros, los atributos como edad, genero, emociones, etc
	"""
	image_path = picture
	image_data = open(image_path, "rb").read()
	headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	'Content-Type': 'application/octet-stream'}
	params = {
		'returnFaceId': 'true',
		'returnFaceLandmarks': 'false',
		'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
	}
	response = requests.post(
							 BASE_URL + "detect/", headers=headers, params=params, data=image_data)
	analysis = response.json()
	return analysis

def show_rectangle (picture, id, id_factura, tipo):
	"""#Imprimir la imagen del cliente/cajero o jefe con un cuadro al rededor de su rostro con las propiedades: 
	id cliente o id cajero, id de la factura y las emociones.
	Las emociones seran obtenidad de la funciones emotions y en la imagen solo sera impresa la emocion con mas valor, pero en la linea de comandos 
	se imprimi todo el diccionario completo.
		picture {str}      -- es el file path de la imagen
		id {str}      -- id del cliente o del cajero
		id_factura {str}      -- factura asociada a la venta
		tipo {str}      -- colocar si la imagen le corresponde a un cliente o a un cajero
	"""
	dic = emotions(picture)
	dic = dic[0]	
	emotion_dict = dic['faceAttributes']['emotion']

	max_key_emotion_dict = max(emotion_dict, key=emotion_dict.get)
	max_val_emotion_dict = max(emotion_dict.values())
	emotion = max_key_emotion_dict + ' : ' + str(round(max_val_emotion_dict, 2))

	faceRectangle = dic['faceRectangle']
	width = faceRectangle['width']
	top = faceRectangle['top']
	height = faceRectangle['height']
	left = faceRectangle['left']

	image=Image.open(picture)
	draw = ImageDraw.Draw(image)
	draw.rectangle((left,top,left + width,top+height), outline='red')
	font = ImageFont.load_default()

	if tipo == 'cliente':
		print(f'Emociones del {tipo}: {emotion_dict}')
		draw.text((50, 50), text = f'ID Cliente: {id}\nID_factura: {id_factura}\nEmotion: {emotion}', font=font,  fill="white")	
		
	elif tipo == 'cajero':
		print(f'Emociones del {tipo}: {emotion_dict}')
		draw.text((50, 50), text = f'ID Cajero: {id}\nID_factura: {id_factura}\nEmotion: {emotion}', font=font,  fill="white")	

	image.show()

def show_rectangle_extended (picture,person_name,age,gender):
	"""#Imprimir la imagen del cliente/cajero o jefe con un cuadro al rededor de su rostro con las propiedades: nombre, edad, genero y emociones.
	Las emociones seran obtenidad de la funciones emotions y en la imagen solo sera impresa la emocion con mas valor, pero en la linea de comandos 
	se imprimi todo el diccionario completo.
		picture {str}      -- es el file path de la imagen
		person_name {str}      -- nombre de la persona
		age {str}      -- edad de la persona
		gender {str}      -- genero de la persona
	"""
	dic = emotions(picture)
	dic = dic[0]
	emotion_dict = dic['faceAttributes']['emotion']
	print(f'Emociones: {emotion_dict}')
	max_key_emotion_dict = max(emotion_dict, key=emotion_dict.get)
	max_val_emotion_dict = max(emotion_dict.values())
	emotion = max_key_emotion_dict + ' : ' + str(round(max_val_emotion_dict, 2))

	faceRectangle = dic['faceRectangle']
	width = faceRectangle['width']
	top = faceRectangle['top']
	height = faceRectangle['height']
	left = faceRectangle['left']

	image=Image.open(picture)
	draw = ImageDraw.Draw(image)
	draw.rectangle((left,top,left + width,top+height), outline='red')
	font = ImageFont.load_default()
	draw.text((50, 50), person_name, font=font,  fill="white")
	draw.text((130, 50), text = f'Emotion: {emotion}\nGender: {gender} \nAge: {age}', font = font)

	image.show()

def consultar_clientes_cajeros_jefes(archivo):
	"""#Imprimir las propiedades de todas del grupo que se quiere consultar, los grupos y archivos binarios que tenemos son clientes,cajeros y jefes, cada uno
	tiene sus propiedad propias de cada grupo.
	Argumentos:
		archivo {str}      -- es el archivo binario que se desea consultar
	"""
	f = open(f"{archivo}.bin", "rb")
	f.seek(0)
	flag = 0
	while flag ==0:
		try:
			e = pickle.load(f)
			#print(e)
			if archivo == "clientes":
				print('---------')
				print(f'Properties:\nperson_id = {e.person_id}\nname = {e.name}\ngender = {e.gender}\nage = {e.age}\ntelefono = {e.telefono}\nemail = {e.email}\npicture path = {e.picture}')
				show_rectangle_extended (e.picture, e.name, e.age, e.gender)
				print('---------')

			elif archivo == "cajeros":
				print('---------')
				print(f'Properties:\nperson_id = {e.person_id}\nname = {e.name}\ngender = {e.gender}\nage = {e.age}\nturno = {e.turno}\nhoras_laboradas = {e.horas_laboradas}\npicture path = {e.picture}')
				show_rectangle_extended (e.picture, e.name, e.age, e.gender)
				print('---------')

			elif archivo == "jefes":
				print('---------')
				print(f'Properties:\nperson_id = {e.person_id}\nname = {e.name}\ngender = {e.gender}\nage = {e.age}\narea = {e.area}\nempleados = {e.empleados}\npicture path = {e.picture}')
				show_rectangle_extended (e.picture, e.name, e.age, e.gender)
				print('---------')

		except:
			print(f"End of the list")
			flag =1
	f.close

def consultar_lista_de_productos():
	"""#Imprimir todos los productos anadidos y sus propiedades id_producto/descripcion/precio
	"""
	f = open("productos.bin", "rb")
	f.seek(0)
	flag = 0
	while flag ==0:
		try:
			e = pickle.load(f)
			#print(e)
			print('---------')
			print(f'Properties:\nid producto = {e.id_producto}\ndescripcion = {e.descripcion}\nprecio = {e.precio}')
			print('---------')
		except:
			print("End of the list products")
			flag =1
	f.close

def consultar_ventas_por_cajero(id_cajero):
	"""#Imprimir las propiedades de todas la ventas realizadas por el cajero y muestra la foto del cajero y del cliente en el momento de la venta
	Argumentos:
		id_cajero {str}      -- es el id del cajero
	"""
	f = open("ventas.bin", "rb")
	f.seek(0)
	flag = 0
	while flag ==0:
		try:
			e = pickle.load(f)
			#print(e)
			if id_cajero == e.id_cajero:
				print('---------')
				print(f'Properties:\nfecha = {e.fecha}\nid_cajero = {e.id_cajero}\nid_cliente = {e.id_cliente}\nid_factura = {e.id_factura}\nproductos = {e.ids_de_productos}\nprecios = {e.precios}\nmonto = {e.monto}\npicture path cajero = {e.path_foto_cajero}\npicture path cliente = {e.path_foto_cliente}')
				show_rectangle (e.path_foto_cajero, e.id_cajero, e.id_factura, 'cajero')
				show_rectangle (e.path_foto_cliente, e.id_cliente, e.id_factura, 'cliente')
				print('---------')

		except:
			print(f"\nEnd of the list of sells of {id_cajero}")
			flag =1
	f.close

def print_people(group_id):
	"""#Imprimir la lista de personas que pertenecen a un grupo, esta es la informacion de la nube de Azure
	Argumentos:
		group_id {str}      -- es el id del grupo que se desea imprimir sus personas
	"""
	#Imprimir la lista de personas del grupo
	print(CF.person.lists(group_id))

if __name__ == "__main__":
	
	#Grupos creados :
	# clientes = 1
	# cajeros = 2
	# jefes = 3
	# productos = 4
	# ventas = 5

	# print("Escoja la tarea de sea realizar")
	# print("Dígite 1 -> Crear un grupo")
	# print("Dígite 2 -> Agregar una persona en un grupo")
	# print("Dígite 3 -> Agregar un producto")
	# print("Dígite 4 -> Agregar una venta")
	# print("Dígite 5 -> Consultar lista de productos")
	# print("Dígite 6 -> Consultar clientes/cajeros/jefes")
	# print("Dígite 7 -> Consular ventas por id del cajero")
	case = int(sys.argv[1])

	# case = int(input())
	if case == 1 :              #Crear grupo. Recibe el id y el nombre del grupo
		
		group_id = int(sys.argv[2])
		group_name = sys.argv[3]
		group_name = group_name.replace('&', ' ')
		# group_id = int(input("Dígite el id del grupo: "))
		# group_name = input("Dígite el nombre del grupo: ")
		create_group(group_id, group_name)

	elif case == 2 :             #Agregar una persona en unos de los grupos creados: clientes, cajeros o jefes
		group_name = sys.argv[2]

		# group_name = input("Digite el nombre del grupo: ")
		if group_name == "clientes":

			name = sys.argv[3]
			picture = sys.argv[4]
			group_id = int(sys.argv[5])
			p1 = int(sys.argv[6])
			p2 = sys.argv[7]
			name = name.replace('&', ' ')

			# name = input("Dígite el nombre: ")
			# picture = input("Dígite el path de la imagen: ")
			# group_id = input("Dígite el id del grupo: ")
			# p1 = input("Dígite el telefono: ")
			# p2 = input("Dígite el email: ")
		elif group_name == "cajeros":

			name = sys.argv[3]
			picture = sys.argv[4]
			group_id = int(sys.argv[5])
			p1 = sys.argv[6]
			p2 = float(sys.argv[7])
			name = name.replace('&', ' ')

			# name = input("Dígite el nombre: ")
			# picture = input("Dígite el path de la imagen: ")
			# group_id = input("Dígite el id del grupo: ")
			# p1 = input("Dígite el turno: ")
			# p2 = input("Dígite las horas laboradas: ")
		elif group_name == "jefes":

			name = sys.argv[3]
			picture = sys.argv[4]
			group_id = int(sys.argv[5])
			p1 = sys.argv[6] # por ejemplo: "tecnologias&de&informacion"
			p2 = int(sys.argv[7])
			name = name.replace('&', ' ')
			p1 = p1.replace('&', ' ')# luego queda como: "tecnologias de informacion"
			

			# name = input("Dígite el nombre: ")
			# picture = input("Dígite el path de la imagen: ")
			# group_id = input("Dígite el id del grupo: ")
			# p1 = input("Dígite el area: ")
			# p2 = input("Dígite numero de empleados a cargo: ")
		else:
			print("Solo existen los grupos clientes, cajeros o jefes")			
			sys.exit(0)
		create_person(name, picture,group_name, group_id, p1, p2)

	elif case == 3: # Agregar un producto

		id_producto = sys.argv[2]
		descripcion = sys.argv[3] # por ejemplo: "producto&basado&en&aceite&de&oliva"
		precio = float(sys.argv[4])
		descripcion.replace('&', ' ')# luego queda como: "producto basado en aceite de oliva"
		# id_producto = input("Dígita el id del producto: ")
		# descripcion = input("Dígita una descripcion del producto: ")
		# precio = input("Dígita el precio del producto: ")
		create_product(id_producto, descripcion, precio)

	elif case == 4:  # Agregar una venta, cuando se ingrese id_producto y precio, estas entradas van a una lista la cual va aumentando conforme le ingreses mas productos
					 # Si ya no se desea agregar mas productos, en la entrada de id_producto se debe digitan el texto : fin, de esta forma la lista se cierra 
					 # Con la lista de precios generada con lo anteiromente mencionado, se genera la propiedad monto que es la suma de los valores de la lista precios
					 # La propiedad fecha se obtiene usando la libreria datetime, nos da la fecha de cuando se realiza el ingreso de la venta.
		id_cajero = int(sys.argv[2])
		id_cliente = int(sys.argv[3])
		id_factura = int(sys.argv[4])
		path_foto_cajero = sys.argv[5]
		path_foto_cliente = sys.argv[6]
		id_productos = sys.argv[7] #llega un str como: "10,11,12,"
		precios = sys.argv[8] #llega un str como: "20.2,34.2,100.1,"

		id_productos = id_productos.split(',')
		id_productos = id_productos[:-1]
		precios = precios.split(',')
		precios = precios[:-1]

		id_productos_list = []
		precios_list = []

		for i in id_productos:
			id_productos_list.append(int(i))
		
		for i in precios:
			precios_list.append(float(i))


		create_venta (id_cajero, id_cliente, id_factura, path_foto_cajero, path_foto_cliente, id_productos_list, precios_list)

	elif case == 5:	# Consultar la lista completa de productos
		consultar_lista_de_productos()

	elif case == 6: # Consultar la lista completa de clientes,cajeros o jefes, con su respectiva foto, como entrada se debe escribir alguna de las opciones:clientes/cajeros/jefes
		lista = sys.argv[2]
		# lista = input("Dígita que lista desea ver: ")
		consultar_clientes_cajeros_jefes(lista)
		
	elif case == 7: # Consultar las ventas por cajer, para consultar se debe colocar el ID del cajero, opciones: 001 / 002
		id_cajero = sys.argv[2]
		# id_cajero = input("Dígita el codigo del cajero: ")
		consultar_ventas_por_cajero(id_cajero)
		
	elif case == 8 : # Para consultar la informacion que almacena la nube ... opcional, la informacion importante esta en los archivos binarios (.bin)
		group_id = int(input("Dígite el id del grupo: "))
		print_people(group_id)	
