from tkinter import *
import tkinter as tk
from PIL import ImageTk
from PIL import Image
from tkinter import filedialog
import io
import requests
from io import BytesIO
import os
import subprocess
from tkinter import messagebox
import os

class Ventana(tk.Frame):

	def __init__(self, master=None):
		super(Ventana, self).__init__(master=master)
		Frame.__init__(self, master) 
		self.master = master
		self.iniciar_menu() 
		
		self.label = tk.Label(self, text="Select a option of the menu bar")
		self.label.pack(padx=20, pady=20)

		self.ids_sell = []
		self.prices_sell = []

	def iniciar_menu(self):

		self.master.title("Supermarket App")
		self.pack(fill=BOTH, expand=1)
		menu = Menu(self.master)
		self.master.config(menu=menu)
		
		#Menu bar Add
		Add = Menu(menu)
		Add.add_command(label="Group", command=self.group_command)
		Add.add_command(label="Client", command=self.client_command)
		Add.add_command(label="Cashier",command=self.cashier_command)
		Add.add_command(label="Boss",command=self.boss_command)
		Add.add_command(label="Product", command=self.product_command)
		Add.add_command(label="Sell", command=self.sell_command)
		menu.add_cascade(label="Add", menu=Add)

		#Menu bar Query
		Query = Menu(menu)
		Query.add_command(label="Clients", command=self.query_clients_command)
		Query.add_command(label="Cashiers", command=self.query_cashiers_command)
		Query.add_command(label="Bosses",command=self.query_bosses_command)
		Query.add_command(label="Products",command=self.query_products_command)
		Query.add_command(label="Sells",command=self.query_sells)
		menu.add_cascade(label="Query", menu=Query)

	def group_command(self):
		print("Create a group")
		ventana_group = tk.Toplevel()
		ventana_group.geometry('400x300')
		ventana_group.title('Create a group')
		
		title = tk.Label(ventana_group, text="Group Create", font="Arial 30", width=20)
		title.pack(side = TOP)
		
		#Group id
		groupid_text = tk.Label(ventana_group, text="Group ID", font="Arial 10", width=10)
		groupid_text.place(x=10, y=100)

		self.entry_groupid = tk.Entry(ventana_group)
		self.entry_groupid.place(x=100,y=100)

		#name
		name_text = tk.Label(ventana_group, text="Name", font="Arial 10", width=10)
		name_text.place(x=10,y=200)
		
		self.entry_name = tk.Entry(ventana_group)
		self.entry_name.place(x=100,y=200)
		
		#btn
		btn1 = Button(ventana_group, text="Create", bd = '5', command = self.btn1_action)
		btn1.place(x=150,y=250)
	
	def client_command(self):
		print("Create a client")
		person_group = tk.Toplevel()
		person_group.geometry('400x500')
		person_group.title('Create a client')	

		title = tk.Label(person_group, text="Client Create", font="Arial 30", width=20)
		title.pack(side = TOP)
		
		#name
		name_text = tk.Label(person_group, text="Name", font="Arial 10", width=10)
		name_text.place(x=10, y=100)

		self.entry_name_client = tk.Entry(person_group)
		self.entry_name_client.place(x=100,y=100)

		#path
		path_text = tk.Label(person_group, text = "Path", font="Arial 10", width=10)
		path_text.place(x=10, y=200)

		self.path_button = Button(person_group, text="Select Image", bd = '5', command = self.generar_ventana5)
		self.path_button.place(x=100,y=190)

		#phone
		phone_text = tk.Label(person_group, text = "Phone", font = "Arial 10", width = 10)
		phone_text.place(x=10,y=300)

		self.entry_phone_text = tk.Entry(person_group)
		self.entry_phone_text.place(x=100,y=300)

		#email
		email_text = tk.Label(person_group, text = "Email", font = "Arial 10", width = 10)
		email_text.place(x=10,y=400)

		self.entry_email_text = tk.Entry(person_group)
		self.entry_email_text.place(x=100,y=400)

		#btn
		btn2 = Button(person_group, text="Create", bd = '5', command = self.btn2_action)
		btn2.place(x=150,y=450)


	def cashier_command(self):
		print("Create a cashier")
		person_group = tk.Toplevel()
		person_group.geometry('400x500')
		person_group.title('Create a cashier')	

		title = tk.Label(person_group, text="Cashier Create", font="Arial 30", width=20)
		title.pack(side = TOP)
		
		#name
		name_text = tk.Label(person_group, text="Name", font="Arial 10", width=10)
		name_text.place(x=10, y=100)

		self.entry_name_cashier = tk.Entry(person_group)
		self.entry_name_cashier.place(x=100,y=100)

		#path
		path_text = tk.Label(person_group, text = "Path", font="Arial 10", width=10)
		path_text.place(x=10, y=200)

		self.path_button = Button(person_group, text="Select Image", bd = '5', command = self.generar_ventana5)
		self.path_button.place(x=100,y=190)

		#turn
		turn_text = tk.Label(person_group, text = "Turn", font = "Arial 10", width = 10)
		turn_text.place(x=10,y=300)

		self.entry_turn_text = tk.Entry(person_group)
		self.entry_turn_text.place(x=100,y=300)

		#hours
		hours_text = tk.Label(person_group, text = "Hours", font = "Arial 10", width = 10)
		hours_text.place(x=10,y=400)

		self.entry_hours_text = tk.Entry(person_group)
		self.entry_hours_text.place(x=100,y=400)

		#btn
		btn3 = Button(person_group, text="Create", bd = '5', command = self.btn3_action)
		btn3.place(x=150,y=450)

	def boss_command(self):
		print("Create a boss")
		person_group = tk.Toplevel()
		person_group.geometry('400x500')
		person_group.title('Create a boss')	

		title = tk.Label(person_group, text="Boss Create", font="Arial 30", width=20)
		title.pack(side = TOP)
		
		#name
		name_text = tk.Label(person_group, text="Name", font="Arial 10", width=10)
		name_text.place(x=10, y=100)

		self.entry_name_boss = tk.Entry(person_group)
		self.entry_name_boss.place(x=100,y=100)

		#path image
		path_text = tk.Label(person_group, text = "Path", font="Arial 10", width=10)
		path_text.place(x=10, y=200)

		self.path_button = Button(person_group, text="Select Image", bd = '5', command = self.generar_ventana5)
		self.path_button.place(x=100,y=190)
		
		#area
		area_text = tk.Label(person_group, text = "Area", font = "Arial 10", width = 10)
		area_text.place(x=10,y=300)

		self.entry_area_text = tk.Entry(person_group)
		self.entry_area_text.place(x=100,y=300)

		#employes
		employes_text = tk.Label(person_group, text = "Employes", font = "Arial 10", width = 10)
		employes_text.place(x=10,y=400)

		self.entry_employes_text = tk.Entry(person_group)
		self.entry_employes_text.place(x=100,y=400)

		#btn
		btn4 = Button(person_group, text="Create", bd = '5', command = self.btn4_action)
		btn4.place(x=150,y=450)

	def product_command(self):
		print("Create a product")
		person_group = tk.Toplevel()
		person_group.geometry('400x400')
		person_group.title('Create a product')

		title = tk.Label(person_group, text="Product Create", font="Arial 30", width=20)
		title.pack(side = TOP)

		#productid
		productid_text = tk.Label(person_group, text="Product ID", font="Arial 10", width=10)
		productid_text.place(x=10, y=100)

		self.productid_ = tk.Entry(person_group)
		self.productid_.place(x=100,y=100)

		#description
		description_text = tk.Label(person_group,text="Description", font="Arial 10", width=10)
		description_text.place(x=10,y=200)

		self.description = tk.Entry(person_group)
		self.description.place(x=100,y= 200)

		#price
		price_text = tk.Label(person_group, text="Price", font="Arial 10", width=10)
		price_text.place(x=10,y=300)

		self.price = tk.Entry(person_group)
		self.price.place(x=100,y=300)

		#btn
		btn5 = Button(person_group, text="Create", bd = '5', command = self.btn5_action)
		btn5.place(x=150,y=350)
	
	def sell_command(self):
		print("Create a sell")
		person_group = tk.Toplevel()
		person_group.geometry('400x900')
		person_group.title('Create a sell')

		title = tk.Label(person_group, text="Sell Create", font="Arial 30", width=20)
		title.pack(side = TOP)

		#idcashier
		idcashier_text = tk.Label(person_group, text="Id Cashier", font="Arial 10", width=10)
		idcashier_text.place(x=10, y=100)

		self.entry_idcashier = tk.Entry(person_group)
		self.entry_idcashier.place(x=100,y=100)

		#idclient
		idclient_text = tk.Label(person_group, text="Id Client", font="Arial 10",width=10)
		idclient_text.place(x=10, y=200)

		self.entry_idclient = tk.Entry(person_group)
		self.entry_idclient.place(x=100,y=200)

		#idfactura
		idfactura_text = tk.Label(person_group, text="Id Bill", font="Arial 10", width=10)
		idfactura_text.place(x=10,y=300)

		self.entry_idfactura = tk.Entry(person_group)
		self.entry_idfactura.place(x=100,y=300)

		#path_imagen_cajero
		path_cajero_text = tk.Label(person_group, text = "Cashier Picture", font="Arial 10", width=10)
		path_cajero_text.place(x=10, y=400)

		self.path_button = Button(person_group, text="Select Image", bd = '5', command = self.generar_ventana5)
		self.path_button.place(x=100,y=390)		

		#path_imagen_cliente
		path_client_text = tk.Label(person_group, text = "Client Picture", font="Arial 10", width=10)
		path_client_text.place(x=10, y=500)

		self.path_button_1 = Button(person_group, text="Select Image", bd = '5', command = self.generar_ventana6)
		self.path_button_1.place(x=100,y=490)		

		#id_product
		id_product_text = tk.Label(person_group, text = "Id Product", font="Arial 10", width=10)
		id_product_text.place(x=10, y= 600)

		self.entry_id_product_sell = tk.Entry(person_group)
		self.entry_id_product_sell.place(x=100,y=600)

		#precio
		precio_sell_text = tk.Label(person_group, text="Price", font="Arial 10",width=10)
		precio_sell_text.place(x=10, y= 700)

		self.entry_precio_sell = tk.Entry(person_group)
		self.entry_precio_sell.place(x=100,y=700)

		#continue_sell btn
		self.continue_btn = Button(person_group, text="Continue Sell", bd = '5', command = self.continue_sell_action)
		self.continue_btn.place(x=10,y=800)

		#finish_sell btn
		self.finish_btn = Button(person_group, text="Finish Sell", bd = '5', command = self.finish_sell_action)
		self.finish_btn.place(x=300,y=800)

	def query_sells(self):
		print("Begin a query sell by id cashier")

		top = tk.Toplevel()
		top.geometry('400x200')
		top.title('Query sells')
		
		title = tk.Label(top, text="Query sells", font="Arial 30", width=20)
		title.pack(side = TOP)
		
		chasierid_text = tk.Label(top, text="Cashier ID", font="Arial 10", width=10)
		chasierid_text.place(x=10, y=100)

		self.query_idcashier = tk.Entry(top)
		self.query_idcashier.place(x=100,y=100)

		btn1 = Button(top, text="Query", bd = '5', command = self.query_sells_command)
		btn1.place(x=150,y=150)

	def query_sells_command(self):
		print("Query sells by id cashier")

		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run(f"python3 trabajo_taller_luis.py 7 {self.query_idcashier.get()}", shell=True,stdout=fout,stderr=ferr)

				# reset file to read from it
				fout.seek(0)
				# save output (if any) in variable
				output=fout.read()

				# reset file to read from it
				ferr.seek(0) 
				# save errors (if any) in variable
				errors = ferr.read()	

		top = Toplevel()
		top.title('List of Sells')
		scroll = Scrollbar(top)
		scroll.pack(side=RIGHT, fill=Y)

		# Text Widget
		eula = Text(top, wrap=NONE, yscrollcommand=scroll.set)
		eula.insert(INSERT,output)
		eula.pack(side="left")

		# Configure the scrollbars
		scroll.config(command=eula.yview)
		eula.config(state=DISABLED)	

	def query_clients_command(self):
		print("Query clients.bin")
		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run('python3 trabajo_taller_luis.py 6 clientes', shell=True,stdout=fout,stderr=ferr)
				fout.seek(0)
				output=fout.read()
				ferr.seek(0) 
				errors = ferr.read()	

		top = Toplevel()
		top.title('List of Clients')
		scroll = Scrollbar(top)
		scroll.pack(side=RIGHT, fill=Y)

		# Text Widget
		eula = Text(top, wrap=NONE, yscrollcommand=scroll.set)
		eula.insert(INSERT,output)
		eula.pack(side="left")

		# Configure the scrollbars
		scroll.config(command=eula.yview)
		eula.config(state=DISABLED)		

	def query_cashiers_command(self):
		print("Query cajeros.bin")
		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run('python3 trabajo_taller_luis.py 6 cajeros', shell=True,stdout=fout,stderr=ferr)
				fout.seek(0)
				output=fout.read()
				ferr.seek(0) 
				errors = ferr.read()
					
		top = Toplevel()
		top.title('List of Cashiers')
		scroll = Scrollbar(top)
		scroll.pack(side=RIGHT, fill=Y)

		# Text Widget
		eula = Text(top, wrap=NONE, yscrollcommand=scroll.set)
		eula.insert(INSERT,output)
		eula.pack(side="left")

		# Configure the scrollbars
		scroll.config(command=eula.yview)
		eula.config(state=DISABLED)	

	def query_bosses_command(self):
		print("Query jefes.bin")
		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run('python3 trabajo_taller_luis.py 6 jefes', shell=True,stdout=fout,stderr=ferr)

				fout.seek(0)
				# save output (if any) in variable
				output=fout.read()

				# reset file to read from it
				ferr.seek(0) 
				# save errors (if any) in variable
				errors = ferr.read()
					

		top = Toplevel()
		top.title('List of Bosses')
		scroll = Scrollbar(top)
		scroll.pack(side=RIGHT, fill=Y)

		# Text Widget
		eula = Text(top, wrap=NONE, yscrollcommand=scroll.set)
		eula.insert(INSERT,output)
		eula.pack(side="left")

		# Configure the scrollbars
		scroll.config(command=eula.yview)
		eula.config(state=DISABLED)	

	def query_products_command(self):
		print("Query products.bin")
		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run('python3 trabajo_taller_luis.py 5', shell=True,stdout=fout,stderr=ferr)

				fout.seek(0)
				# save output (if any) in variable
				output=fout.read()

				# reset file to read from it
				ferr.seek(0) 
				# save errors (if any) in variable
				errors = ferr.read()
					

		top = Toplevel()
		top.title('List of Products')
		scroll = Scrollbar(top)
		scroll.pack(side=RIGHT, fill=Y)

		# Text Widget
		eula = Text(top, wrap=NONE, yscrollcommand=scroll.set)
		eula.insert(INSERT,output)
		eula.pack(side="left")

		# Configure the scrollbars
		scroll.config(command=eula.yview)
		eula.config(state=DISABLED)

	def btn1_action(self):
		print("Create a  group --> executing os.system")
		name = self.entry_name.get()
		name = name.replace(' ','&')

		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run(f'python3 trabajo_taller_luis.py 1 {self.entry_groupid.get()} {name}', shell=True,stdout=fout,stderr=ferr)

				fout.seek(0)
				# save output (if any) in variable
				output=fout.read()

				# reset file to read from it
				ferr.seek(0) 
				# save errors (if any) in variable
				errors = ferr.read()
				
		# print(output)
		# print(errors)

		if len(output) > 0:
			messagebox.showinfo(message=output, title="Success")
			print ("Its worked!!")

		elif len(errors) > 0:
			messagebox.showerror(message="Group not created", title="Failed")
			print ("There was a problem")

	def btn2_action(self):
		print("Crear client --> executing os.system")
		# print(self.entry_name_client.get())
		# print(self.image_path)
		# print(self.idgroup_client.get())
		# print(self.entry_phone_text.get())
		# print(self.entry_email_text.get())

		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run(f"python3 trabajo_taller_luis.py 2 clientes {self.entry_name_client.get()} {self.image_path} 1 {self.entry_phone_text.get()} {self.entry_email_text.get()}"
				, shell=True, stdout=fout, stderr=ferr)

				fout.seek(0)
				output=fout.read()

				ferr.seek(0) 
				errors = ferr.read()
			
		if len(output) > 0:
			messagebox.showinfo(message=output, title="Success")
			print ("Its worked!!")
			
		elif len(errors) > 0:
			messagebox.showerror(message="Client not created", title="Failed")
			print ("There was a problem, so do something else")

	def btn3_action(self):
		print("Create a cashier --> executing os.system")
		# print(self.entry_name_cashier.get())
		# print(self.image_path)
		# print(self.idgroup_cashier.get())
		# print(self.entry_turn_text.get())
		# print(self.entry_hours_text.get())

		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run(f"python3 trabajo_taller_luis.py 2 cajeros {self.entry_name_cashier.get()} {self.image_path} 2 {self.entry_turn_text.get()} {self.entry_hours_text.get()}"
				, shell=True, stdout=fout, stderr=ferr)

				fout.seek(0)
				output=fout.read()
				ferr.seek(0) 
				errors = ferr.read()

		if len(output) > 0:
			messagebox.showinfo(message=output, title="Success")
			print ("Its worked!!")
			
		elif len(errors) > 0:
			messagebox.showerror(message="Cashier not created", title="Failed")
			print ("There was a problem, so do something else")

	def btn4_action(self):
		print("Create a boss --> executing os.system")
		# print(self.entry_name_boss.get())
		# print(self.image_path)
		# print(self.idgroup_boss.get())
		# print(self.entry_area_text.get())
		# print(self.entry_employes_text.get())

		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run(f"python3 trabajo_taller_luis.py 2 jefes {self.entry_name_boss.get()} {self.image_path} 3 {self.entry_area_text.get()} {self.entry_employes_text.get()}"
				, shell=True, stdout=fout, stderr=ferr)

				fout.seek(0)
				output=fout.read()
				ferr.seek(0) 
				errors = ferr.read()
		
		if len(output) > 0:
			messagebox.showinfo(message=output, title="Success")
			print ("Its worked!!")
			
		elif len(errors) > 0:
			messagebox.showerror(message="Boss not created", title="Failed")
			print ("There was a problem")

	def btn5_action(self):
		print("Create a product --> executing os.system")
		# print(self.productid_.get())
		# print(self.description.get())
		# print(self.price.get())
		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				command_run = subprocess.run(f"python3 trabajo_taller_luis.py 3 {self.productid_.get()} {self.description.get()} {self.price.get()}"
				, shell=True, stdout=fout, stderr=ferr)

				fout.seek(0)
				output=fout.read()
				ferr.seek(0) 
				errors = ferr.read()

		if len(output) > 0:
			messagebox.showinfo(message=output, title="Success")
			print ("Its worked!!")
			
		elif len(errors) > 0:
			messagebox.showerror(message="Product not created", title="Failed")
			print ("There was a problem")

	def continue_sell_action(self):
		print("Continue Sell")
		self.ids_sell.append(int(self.entry_id_product_sell.get()))
		self.prices_sell.append(float(self.entry_precio_sell.get()))
		self.entry_id_product_sell.delete(0,END)
		self.entry_precio_sell.delete(0,END)

	def finish_sell_action(self):
		self.ids_sell.append(int(self.entry_id_product_sell.get()))
		self.prices_sell.append(float(self.entry_precio_sell.get()))

		ids_sell_aux = ''
		for i in self.ids_sell:
			ids_sell_aux = ids_sell_aux + str(i) + ','

		prices_sell_aux = ''
		for i in self.prices_sell:
			prices_sell_aux = prices_sell_aux + str(i) + ','

		self.entry_id_product_sell.delete(0,END)
		self.entry_precio_sell.delete(0,END)
		# print("Finish Sell")
		# print(self.entry_idcashier.get())
		# print(self.entry_idclient.get())
		# print(self.entry_idfactura.get())
		# print(self.image_path)
		# print(self.image_path_1)
		# print(self.ids_sell)
		# print(self.prices_sell)
		self.ids_sell = []
		self.prices_sell = []

		with open('out.txt','w+') as fout:
			with open('err.txt','w+') as ferr:
				cmd = f"python3 trabajo_taller_luis.py 4 {self.entry_idcashier.get()} {self.entry_idclient.get()} {self.entry_idfactura.get()} {self.image_path} {self.image_path_1} {ids_sell_aux} {prices_sell_aux}"
				print("cmd: ",cmd)
				command_run = subprocess.run(cmd, shell=True, stdout=fout, stderr=ferr)

				fout.seek(0)
				output=fout.read()

				ferr.seek(0) 
				errors = ferr.read()

		if len(output) > 0:
			messagebox.showinfo(message=output, title="Success")
			print ("Its worked!!")
			
		elif len(errors) > 0:
			messagebox.showerror(message="Sell not created", title="Failed")
			print ("There was a problem")

	def generar_ventana5(self):
		path_initial = os.popen('pwd').read()[:-1]
		print(path_initial)
		ventana5 = tk.Toplevel()
		ventana5.filename = filedialog.askopenfile(
            initialdir = path_initial,title = "Selecionar archivo",
            filetypes = (("jpeg files","*.jpg"),("all files","*.*"))   
        )
		a = ventana5.filename.name
		a = a.split('/')
		self.image_path = a[-2] + '/' + a[-1]
		self.path_button['text'] = ventana5.filename.name
		ventana5.img = Image.open(ventana5.filename.name)
		ventana5.img = ventana5.img.resize((283, 354), Image.ANTIALIAS)
		ventana5.img = ImageTk.PhotoImage(ventana5.img)
		ventana5.canvas = Canvas(ventana5, width=283, height=354)
		ventana5.canvas.pack(expand=YES, fill=BOTH)
		ventana5.canvas.create_image(0,0, anchor=NW, image=ventana5.img)
		ventana5.after(3000, ventana5.destroy)	

	def generar_ventana6(self):
		path_initial = os.popen('pwd').read()[:-1]
		ventana6 = tk.Toplevel()
		ventana6.filename = filedialog.askopenfile(
            initialdir = path_initial,title = "Selecionar archivo",
            filetypes = (("jpeg files","*.jpg"),("all files","*.*"))   
        )
		a = ventana6.filename.name
		a = a.split('/')
		self.image_path_1 = a[-2] + '/' + a[-1]
		self.path_button_1['text'] = ventana6.filename.name
		ventana6.img = Image.open(ventana6.filename.name)
		ventana6.img = ventana6.img.resize((283, 354), Image.ANTIALIAS)
		ventana6.img = ImageTk.PhotoImage(ventana6.img)
		ventana6.canvas = Canvas(ventana6, width=283, height=354)
		ventana6.canvas.pack(expand=YES, fill=BOTH)
		ventana6.canvas.create_image(0,0, anchor=NW, image=ventana6.img)
		ventana6.after(3000, ventana6.destroy)	

if __name__=="__main__":
	root = tk.Tk()
	root.geometry("400x300")
	
	main = Ventana(root)
	main.pack(fill="both", expand=True)
	root.mainloop()

