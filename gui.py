#import necessary modules
from tkinter import *
import sqlite3,os,pyautogui,multiprocessing
from tkinter import filedialog,messagebox
from functools import partial
from smtplib import SMTP
from platform import system as sys
root=Tk()

class gui_packer:
	def __init__(self,root):
		#create the base window of the application.

		self.root = root
		self.root.title("Python modules Downloader")
		
		#capture the size of the screen
		self.screen_width,self.screen_height = pyautogui.size()
		#call the widgets input function
		self.db_manager()
		self.menu_btns()
		self.widgets_input()
		self.configurations()

	def menu_btns(self):
		main_menu=Menu(self.root)

		add_module=Menu(main_menu,tearoff=0)

		add_module.add_command(label="Add a module",command=self.add_moduler)
		
		add_module.add_command(label="Check the modules available")

		color=Menu(main_menu,tearoff=False)
		color.add_command(label="Change background color")
		color.add_command(label="remove color")

		contact_dev=Menu(main_menu,tearoff=False)
		contact_dev.add_command(label="Email",command=self.email_dev)
		contact_dev.add_command(label="Tel",command=self.tel_dev)

		#add the sub menus to the main menu on the screen.
		main_menu.add_cascade(label='menu',menu=add_module)
		main_menu.add_cascade(label="Color",menu=color)
		main_menu.add_cascade(label="contact dev",menu=contact_dev)
		
		self.root.configure(menu=main_menu)
	
	#email the developer
	def email_dev(self):
		messagebox.showinfo("Developer","Still under development")


	#telephone number.
	def tel_dev(self):
		messagebox.showinfo("Developer","My telephone number is: +254797494509")



	def widgets_input(self):
		
		try:
			self.main_frame=Frame(self.root,background="#456")
			
			self.lab1=Label(self.main_frame,background="#456",font=("sans serif",13,'italic'),text="Hello {}, We are glad you have decided to use our app.\nTo lauch the downloads just click on the button below.".format(os.getlogin()))
			self.lab1.pack(fill="both")


			#create the button widget
			self.txt_donwload=StringVar()
			
			self.txt_donwload.set("Download")
			
			Label(self.main_frame,padx=10,pady=5,background="#456").pack()
			
			self.download_btn=Button(self.main_frame,padx=10,pady=10,relief='raised',textvariable=self.txt_donwload,font=("sans serif",20,"bold"),cursor="plus",activeforeground='cyan',activebackground='#345')
			self.download_btn.bind("<Button-1>",self.download_manager)
			self.download_btn.bind("<Button-3>",self.download_manager)
			self.download_btn.pack()


			Label(self.main_frame,padx=10,pady=5,background="#456").pack()
			self.main_frame.pack(fill="both")

			self.main_frame2=LabelFrame(self.root,text = " Logging ...  ",foreground="#f00",font=('sans serif',14))
			#det_bar=ScrollBar(self.root,command=self.main_frame2.yview,orient='vertical')
			#det_bar.pack()
			self.main_frame2.pack(fill="both")

		
		except:
			print("Hello")


	def configurations(self):
		self.root.resizable(0,0)
		self.root.geometry("{}x{}+{}+{}".format(int(self.screen_width*.5),int(self.screen_height*.5),int(self.screen_width*.25),int(self.screen_height*.15)))
		self.root.configure(background="#456")

	

		#self.download_manager()

	def download_manager(self,event):
		self.txt_donwload.set("Downloading ...")
		self.download_btn.configure(background="#1e2f3f")
		

		#call the db_select module
		modules = self.db_select()
		
		#iterate over the modules
		for module in modules:
			command="pip install "
			module=module[1]
			#Label(self.main_frame2,text="{}. Donwloading - {}".format(module[0],module[1])).pack()
			os.system(command + module)
			print(command + module)



	def add_moduler(self):
		self.window_add_mod=Toplevel(self.root)
		self.window_add_mod.resizable(0,0)
		self.window_add_mod.geometry("{}x{}".format(int(self.screen_width*.4),int(self.screen_height*.14)))

		add_frame1 = Frame(self.window_add_mod)
		
		label_addmodule = Label(self.window_add_mod,text="Enter the module name ")
		label_addmodule.pack(side="left")
		self.module_name = Entry(self.window_add_mod,font=("sans serif",15,'italic'))
		self.module_name.pack(side="left")
		
		add_frame1.pack(side="top")

		add_frame2 = Frame(self.window_add_mod)
		
		btn_mod_submit = Button(add_frame2,text='Add',padx=5,pady=7,font=("sans serif",10,'italic'),background="gold",cursor="plus")

		btn_mod_submit.bind("<Button-1>",self.db_insert)
		btn_mod_submit.bind("<Button-3>",self.db_insert)
		btn_mod_submit.pack(side="top")
		
		add_frame2.pack(side="left")






	def db_manager(self):
		#connect to the database

		try:
			
			self.conn=sqlite3.connect("modules_db.db")
			cur=self.conn.cursor()
			cur.execute('''CREATE TABLE IF NOT EXISTS module_db(
				module_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				module_name TEXT UNIQUE NOT NULL,
				module_user TEXT NOT NULL
				);''')
			self.conn.commit()
		except Exception as e:
			print("Error: {}".format(e))




	#method to add module to the data base
	def db_insert(self,event):
		cur=self.conn.cursor()
		try:
		
			cur.execute("INSERT INTO module_db(module_name,module_user)VALUES(?,?)",(self.module_name.get().lower(),os.getlogin()))
		except sqlite3.IntegrityError as e:
			messagebox.showerror("Sql Error","Error: {}".format(e))
			
		else:
			messagebox.showinfo("Notification manager","Module {} added to the database sucessfully.\n Thank you for your contributions.".format(self.module_name.get()))
			self.window_add_mod.destroy()

		self.conn.commit()

	#method to View data from database
	def db_select(self):
		cur=self.conn.cursor()
		print("started executing the select")
		cached_obj=cur.execute("SELECT module_id,module_name FROM module_db")
		return cached_obj.fetchall()

	#method to remove data from the database,
	def db_delete(self):
		pass


gui_packer(root)

#enter the events mainloop
root.mainloop()