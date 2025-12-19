from tkinter import *
import tkinter.ttk as ttk
import pandas as pd
import sympy as sp

class App:
	def __init__(self, root):
		self.master = root
		self.nb = ttk.Notebook(self.master)
		
		self.frame1 = ttk.Frame(self.nb)
		# input: pv, n, i
		# output: A
		self.texthead = Label(self.frame1, text = "Masukkan Present Value, jumlah periode, dan tingkat inflasi per angsuran")   
		self.texthead.pack()
		self.btn1 = Button(self.frame1, text = "hitung", command = self.calc_A1)
		
		self.pv_input = Entry(self.frame1)
		self.n_input = Entry(self.frame1)
		self.r_input = Entry(self.frame1)
		
		self.frame12 = ttk.Frame(self.nb).pack()
		tpv = Label(self.frame1, text = "pv").pack()
		self.pv_input.pack()
		
		tn = Label(self.frame1, text = "N").pack()
		self.n_input.pack()
		
		tr = Label(self.frame1, text = "r").pack()
		self.r_input.pack()
		self.btn1.pack()
		
		self.res1text = StringVar(value = "Nilai angsuran =")
		self.res1 = Label(self.frame1, textvariable=self.res1text).pack()
		
		self.frame2 = ttk.Frame(self.nb)
		# input: pv, n, g, i
		# output: A, tabel, csv
		self.texthead = Label(self.frame2, wraplength = 200, text = "Masukkan Present Value, jumlah periode, tingkat petumbuhan angsuran, dan tingkat inflasi per angsuran")   
		self.texthead.pack()
		self.btn2 = Button(self.frame2, text = "hitung", command = self.calc_A2)
		
		self.pv2_input = Entry(self.frame2)
		self.n2_input = Entry(self.frame2)
		self.r2_input = Entry(self.frame2)
		self.g2_input = Entry(self.frame2)
		
		tpv = Label(self.frame2, text = "pv").pack()
		self.pv2_input.pack()
		
		tn = Label(self.frame2, text = "N").pack()
		self.n2_input.pack()
		
		tr = Label(self.frame2, text = "r").pack()
		self.r2_input.pack()
		
		tg = Label(self.frame2, text = "g").pack()
		self.g2_input.pack()
		self.btn2.pack()
		self.describe = {"A": 0., "n": 0 ,"i": 0.1,"g":0.}
		
		self.restext = StringVar(value="Nilai Angsuran:  ")
		res = Label(self.frame2, textvariable = self.restext).pack()
		self.kolom = ('AN')
		self.tree = ttk.Treeview(self.frame2, columns = self.kolom)
		
		self.data = {'N': [], 'A': []}
		
			
		self.tree.heading('#0', text='Angsuran ke-')
		self.tree.heading('AN', text='Nilai angsuran')
		
		#self.tree.insert('',END, 'fst', text = "1")
		#self.tree.set('fst', 'AN', '120') 
		self.tree.pack()
		
		self.frame3 = ttk.Frame(self.nb);
		# input: pv, A, n
		# output: i
		self.texthead = Label(self.frame3, text = "Masukkan Present Value, anuitas, dan jumlah periode")   
		self.texthead.pack()
		self.btn3 = Button(self.frame3, text = "Hitung", command = self.calc_r)
	
		
		self.pv3_input = Entry(self.frame3)
		self.A3_input = Entry(self.frame3)
		self.n3_input = Entry(self.frame3)
		
		tpv = Label(self.frame3, text = "pv").pack()
		self.pv3_input.pack()
		
		tn = Label(self.frame3, text = "A").pack()
		self.A3_input.pack()
		
		tr = Label(self.frame3, text = "N").pack()
		self.n3_input.pack()
		self.btn3.pack()
		
		self.res_rtext = StringVar(value = "r = ")
		self.res_r = Label(self.frame3, textvariable = self.res_rtext).pack()
		
		
		self.nb.add(self.frame1, text='Anuitas Biasa')
		self.nb.add(self.frame2, text='Anuitas Bertumbuh')
		self.nb.add(self.frame3, text = 'Perhitungan tingkat bunga anuitas biasa')
		
		self.nb.pack(expand = True, fill = BOTH)
	def calc_A1(self):
		pv = float(self.pv_input.get())
		n = int(self.n_input.get())
		r = float(self.r_input.get())
		
		an = (1 - pow(1 + r, -n))/r
		A = pv/an
		self.res1text.set(f"Nilai angsuran = {format(A, '.2f')}")
	def calc_A2(self):
		self.tree.delete(*self.tree.get_children())
		self.data["N"].clear()
		self.data["A"].clear()
		pv = float(self.pv2_input.get())
		n = int(self.n2_input.get())
		r = float(self.r2_input.get())
		g = float(self.g2_input.get())
		
		an = (1 - pow((1+g)/(1 + r), n))/(r - g)
		
		self.describe["A"] = format(pv/an, '.2f') 
		self.describe["n"] = n
		self.describe["r"] = r
		self.describe["g"] = g
		self.restext.set(f"Nilai angsuran awal: {self.describe['A']}.\nHasil disimpan di file Anuitas_bertumbuh.csv")
		
		A = pv/an
		for k in range(1,n+1):
			self.data["N"].append(k)
			self.data["A"].append(format(A*pow(1+g, k-1), '.2f'))
		df = pd.DataFrame(self.data)
		df.to_csv("Angsuran_bertumbuh.csv", index = False)
		rf = pd.read_csv("Angsuran_bertumbuh.csv")
		
		for k in range(n):
			n_k = rf.iloc[k, 0]
			A_k = rf.iloc[k, 1]
			
			self.tree.insert('', END, str(k), text = n_k)
			self.tree.set(str(k), 'AN', A_k)
	def calc_r(self):
		pv = float(self.pv3_input.get())
		n = int(self.n3_input.get())
		A = float(self.A3_input.get())
		
		i = sp.symbols('i')
		my_eq = pv*i - A*(1 - pow(1+i,-n))
		res = sp.nsolve(my_eq, i, 0.5)
		
		
		self.res_rtext.set(f"r = %{format(res*100, '.2f')}")
root = Tk()
root.geometry("750x650")
root.title("Proyek Matematika Keuangan: Utilitas")

window = App(root)
root.mainloop()
