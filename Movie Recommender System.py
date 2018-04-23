from tkinter import *
from PIL import ImageTk,Image
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import xlrd
root=Tk()
genres=[]
tags1=[]
result=[]
vel=[]
vel1=[]
comments=[]
i=1
users_data=pd.read_excel("users.xlsx","Sheet1")
keywords=["boring","awesome","emotional","adventure","romantic","childish","music","ammature","good","very good","bad","ridiculous","romance","science","sci-fi","funny"]
tags=[]
def getf(u,e):
	vel1.append(u.get())
	vel1.append(e.get())
def loginact():
	top3=Toplevel(root)
	users_data=pd.read_excel("users.xlsx","Sheet1")
	e=users_data['E-mail'].tolist()
	pas=users_data['Password'].tolist()
	u=users_data['Name'].tolist()
	if vel1[0] in e  and vel1[1] in pas:
		Label(top3,text="You are succesfully logged in").grid(row=0,column=0)
		Button(root,text=u[-1]).grid(row=0,column=1)
	else:
		Label(top3,text="Please enter valid email and password!").grid(row=0,column=0)
	top3.mainloop()


def login():
	top=Toplevel(root)
	Label(top,text="E-mail").grid(row=0,column=2)
	Label(top,text="Password").grid(row=1,column=2)
	e1=Entry(top)
	e1.grid(row=0,column=3)
	e2=Entry(top)
	e2.grid(row=1,column=3)
	c1=Button(top,text="Check",command=lambda:getf(e1,e2))
	Button(top,text="Log in",command=loginact).grid(row=2,column=3)
	
	c1.grid(row=2,column=4)
	top.mainloop()

	

def po():
	top2=Toplevel(root)
	if vel[2]==vel[3] and vel[2] and "@" in vel[1]:
		k=load_workbook("users.xlsx")
		s=k.active
		s.append((" ",vel[0],vel[1],vel[2]))
		k.save("users.xlsx")
		Label(top2,text="You are Succesfully Signed Up!").grid(row=0,column=0)		
		
	else:
		Label(top2,text="Please enter the valid credentials").grid(row=0,column=0)
	top2.mainloop()
		
def signup():
	master_2 = Toplevel(root)
	user_name = Entry(master_2)
	user_name.grid(row = 1, column = 2)
	email = Entry(master_2)
	email.grid(row = 2, column = 2)
	passw=Entry(master_2)
	passw.grid(row=3,column=2)
	confpassw=Entry(master_2)
	confpassw.grid(row=4,column=2)
	label_un = Label(master_2, text = "Full Name")
	label_un.grid(row = 1, column = 1)
	label_pwd = Label(master_2, text = "Email")
	label_pwd.grid(row = 2, column = 1)
	label_pwd1 = Label(master_2, text = "Password").grid(row=3,column=1)
	label_pwd2 = Label(master_2, text = "Confirm Password").grid(row=4,column=1)
	get_button = Button(master_2, text = "Save", command = lambda : getname(user_name,email,passw,confpassw))
	Button(master_2,text="Register",command=po).grid(row=5,column=1)
	get_button.grid(row=5, column = 2)
	master_2.mainloop() 


def getname(u,e,c,d):
	vel.append(u.get())
	vel.append(e.get())
	vel.append(c.get())
	vel.append(d.get())

	
	

root.title("Movie Recommender System")
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
frame1=Frame(root,height=100,width=100,bd=1)
frame1.place(x=200,y=10)
rating=IntVar()
log_in=Button(root,text="Log In",bg="orange",command=login).grid(row=0,column=2)
Sign_Up=Button(root,text="Sign Up",bg="orange",command=signup).grid(row=0,column=4)

Label(frame1,text="Enter the Genre of movie").grid(row=0,column=2)
Label(frame1,text="Enter the Ratings You Want").grid(row=0,column=4)
entry_rating=Entry(frame1,textvariable=rating).grid(row=1,column=4)
genre=StringVar()
movie=pd.read_csv("MOvies.csv")
rat=pd.read_csv("Ratings.csv")
tagg=pd.read_csv("tag.csv")
merg=pd.merge(movie,rat, on="movieId")
merged=pd.merge(merg,tagg,on="movieId")
def update_merge():
	writer = pd.ExcelWriter('output.xlsx')
	merged.to_excel(writer,"Sheet1")
	writer.save()
tag=StringVar()
entry=Entry(frame1,textvariable=genre).grid(row=1,column=2)
Label(frame1,text="Enter any tags if you want").grid(row=0,column=5)
tag_entry=Entry(frame1,textvariable=tag).grid(row=1,column=5)
comments=StringVar()
for i in merged['genres']:
    ke=i.split("|")
    genres.append(ke)
for i in merged["tag"]:
	k=i.split(",")
	tags.append(k)

def sort():
	row=1
	for i in result[::-1]:
		k=str(51-int(i[0]))
		p=k+i[1:len(i)]
		Label(innerframe,text=p).grid(row=row,column=0)
		row+=1
def semantic_analysis(e,r):
	k=e.get()
	a=k.split(" ")
	for i in a:
		if i in keywords:
			ke=result[r-1][1]
			merged["tag"][ke]=merged["tag"][ke]+","+str(i)
			update_merge()
def rating_update(e,r):
	k=e.get()
	k=int(k)
	ke=result[r-1][1]
	merged["ratings"][ke]=(merged["ratings"][ke]+k)/2
	update_merge()


def rating1(i):
	e=Entry(innerframe)
	e.grid(row=i,column=6)
	b1=Button(innerframe,text="Submit Rating",bg="orange",command=lambda r=i:rating_update(e,r))
	b1.grid(row=i,column=7)

def comment(i):
	k=StringVar()
	e=Entry(innerframe)
	e.grid(row=i,column=3)
	b1=Button(innerframe,text="Submit",bg="orange",command=lambda r=i:semantic_analysis(e,r))
	b1.grid(row=i,column=4)
	b2=Button(innerframe,text="Wanna Rate?",bg="orange",command=lambda r=i:rating1(i))
	b2.grid(row=i,column=5)
users_data=pd.read_excel("output.xlsx","Sheet1")
tagu=users_data["tag"].tolist()
for i in tagu:
	k=i.split(",")
	tags1.append(k)

def click():
	coun=1
	row=1
	for j in range(len(genres)):
		if genre.get() in genres[j] and coun<=50 and rating.get()<=merged['ratings'][j] and tag.get() in tags1[j]:
			st=str(row)+")"+"   "+str(merged['title'][j])
			result.append((str(merged['title'][j]),j))
			if(merged['ratings'][j]==2.5):
				im = Image.open("2.5.png")
				resized = im.resize((100, 30), Image.ANTIALIAS)
				image=ImageTk.PhotoImage(resized)
				myimg=Label(innerframe,image=image)
				myimg.image=image
				myimg.grid(row=row,column=1)
			if(merged['ratings'][j]==3):
				im = Image.open("3.png")
				resized = im.resize((100, 30), Image.ANTIALIAS)
				image=ImageTk.PhotoImage(resized)
				myimg=Label(innerframe,image=image)
				myimg.image=image
				myimg.grid(row=row,column=1)
			if(merged['ratings'][j]==3.5):
				im = Image.open("3.5.png")
				resized = im.resize((100, 30), Image.ANTIALIAS)
				image=ImageTk.PhotoImage(resized)
				myimg=Label(innerframe,image=image)
				myimg.image=image
				myimg.grid(row=row,column=1)
			if(merged['ratings'][j]==4.5):
				im = Image.open("4.5.jpg")
				resized = im.resize((100, 30), Image.ANTIALIAS)
				image=ImageTk.PhotoImage(resized)
				myimg=Label(innerframe,image=image)
				myimg.image=image
				myimg.grid(row=row,column=1)
			if(merged['ratings'][j]==4):
				im = Image.open("4.png")
				resized = im.resize((100, 30), Image.ANTIALIAS)
				image=ImageTk.PhotoImage(resized)
				myimg=Label(innerframe,image=image)
				myimg.image=image
				myimg.grid(row=row,column=1)
			if(merged['ratings'][j]==5):
				im = Image.open("5.png")
				resized = im.resize((100, 30), Image.ANTIALIAS)
				image=ImageTk.PhotoImage(resized)
				myimg=Label(innerframe,image=image)
				myimg.image=image
				myimg.grid(row=row,column=1)
			#Label(innerframe,text="Enter Your Comments").grid(row=0,column=2)
			Label(innerframe,text=st).grid(row=row,column=0)
			Button(innerframe,text="Comment Here",command= lambda row=row:comment(row)).grid(row=row,column=2)
			#Button(innerframe,text="Wanna Rate?",command=rating).grid(row=row,column=4)
			#Label(innerframe,text="Enter your ratings").grid(row=0,column=3)
			#Entry(innerframe,textvariable=k).grid(row=row,column=2)
			#Entry(innerframe,textvariable=ra).grid(row=row,column=3)
			Button(innerframe,text="sort",bg="red",command=sort).grid(row=0,column=0)
			#Button(innerframe,text="submit",bg="green").grid(row=row,column=4)
			if(coun==50):
				Button(innerframe,text="Next Page",bg="green").grid(row=51,column=2)
			coun +=1
			row +=1



def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=800,height=500)

button=Button(frame1,text="Click To See Results!",command=click).grid(row=2,column=3)
mainframe=Frame(root,height=100,width=100,relief=GROOVE,bd=1)
mainframe.place(x=200,y=100)
canvas=Canvas(mainframe)
innerframe=Frame(canvas)
myscrollbar=Scrollbar(mainframe,orient="vertical",command=canvas.yview)
myscrollbar1=Scrollbar(mainframe,orient="horizontal",command=canvas.xview)
canvas.configure(xscrollcommand=myscrollbar1.set)
Button(root,text="Guest").grid(row=0,column=1)
canvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar1.pack(side="bottom",fill="x")
myscrollbar.pack(side="right",fill="y")
canvas.pack(side=TOP,expand=True,fill=BOTH)
canvas.create_window((0,0),window=innerframe,anchor='nw')
innerframe.bind("<Configure>",myfunction)
root.mainloop()