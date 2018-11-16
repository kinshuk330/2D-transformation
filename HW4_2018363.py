# CSE 101 - IP HW4
# Transformations of 2-Dimensional Geometric Objects
# Name:Sandeep kumar singh
# Roll Number:2018363
# Section:B
# Group:4

import copy
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from random import uniform as uni
plt.ion()
c=0
def multiplymatrix(A,B):#for multiplying 2 matrices
	'''
	Pre condition:
	1.number of columns of A must be equal to number of rows of B
	2.data in matrix is stored as row wise i.e A is a list of rows of A which means A[0] is the first row of A and so on
	'''	
	if len(A[0])!=len(B):
		print("can't multiply matrices",A,B)
		quit()

	Multiplex=[[0 for i in range(len(B[0]))]for j in range(len(A))]#initializing the required matrix with required size with '0'

	for i in range(len(Multiplex)):
		for j in range(len(Multiplex[0])):
			for k in range(len(A[0])):
				Multiplex[i][j]+=A[i][k]*B[k][j]
		
	return Multiplex

def rotate(x,Q,shape='polygon'):#for rotating the matrix of co-ordinates
	'''
	Arguments:
	Q is the angle of rotation in degrees
	x is a list of co-ordinate matrix of vertices in row form along with a 1 in last row
	in case of "disc" x is list of center coordinates and height and width
	'''
	Q=math.radians(Q)
	rot_array=[ [math.cos(Q),-math.sin(Q),0],
				[math.sin(Q), math.cos(Q),0],
				[0          ,0           ,1]]
	rotated_matrix=[]
	if shape=='disc':
		return multiplymatrix(rot_array,[x[0],x[1],[1]])[:2]+x[2:]
	for i in x:
		rotated_matrix.append(multiplymatrix(rot_array,i))
	return rotated_matrix

def scale(x,sx,sy,shape='polygon'):#for scaling the  matrix of coordinates
	'''
	Arguments:
	sx and sy are scaling factors in x and y axis respectively
	x is a list of co-ordinate matrix of verices in row form along with a 1 in last row
	in case of "disc" x is list of center coordinates and radius
	'''
	scal_array=[[sx,0,0],
				[0,sy,0],
				[0,0 ,1]]
	scaled_matrix=[]
	if shape=='disc':
		return x[:2]+multiplymatrix(scal_array,[x[2],x[3],[1]])[:2]
	for i in x:
		scaled_matrix.append(multiplymatrix(scal_array,i))
	return scaled_matrix

def translate(x,dx,dy,shape='polygon'):#for translating the matrix of coordinates
	'''
	arguments:
	dx and dy are translating factors in x and y axis respectively
	x is a list of co-ordinate matrix of vertices in row form along with a 1 in last row
	in case of "disc" x is list of center coordinates and height and width
	'''
	tran_array=[[1,0,dx],
				[0,1,dy],
				[0,0,1 ]]
	translated_matrix=[]
	if shape=='disc':
		return multiplymatrix(tran_array,[x[0],x[1],[1]])[:2]+x[2:]

	for i in x:
		translated_matrix.append(multiplymatrix(tran_array,i))
	return translated_matrix

def show_polygon(newx):# for showing converted polygon 
	global c
	temp=[]
	newy=[]
	for i in newx:
		newy.append(i[1][0])
		temp.append(i[0][0])
	newx=temp

	maximum=max(max(newx),max(newy))
	minimum=min(min(newx),min(newy))
	if minimum>0:
		minimum=0
	
	plt.xlim(minimum-maximum,maximum*2)
	plt.ylim(minimum-maximum,maximum*2)
	c+=1
	conversion_label=str(c)+" Conversion"
	plt.plot(newx,newy,color=[round(uni(0, 1), 1),round(uni(0, 1), 1),round(uni(0, 1), 1)],label=conversion_label)
	plt.legend()
	plt.pause(0.0001)
	
def show_disc(newx,x):# for showing converted disc
	global c
	temp=[]
	for i in newx:
		temp.append(i[0])
	newx=temp
	c+=1

	maximum=max(max(x),max(newx))
	minimum=min(min(x),min(newx))
	conversion_label=str(c)+" Conversion"
	#genrating ra
	new_ellipse=Ellipse(xy=(newx[0],newx[1]),width=2*newx[2],height=2*newx[3],color=[round(uni(0, 1), 1),round(uni(0, 1), 1),round(uni(0, 1), 1)],label=conversion_label)
	ax.add_patch(new_ellipse)
	ax.set_xlim((minimum-maximum)*2,(maximum+x[2])*2)
	ax.set_ylim((minimum-maximum)*2,(maximum+x[2])*2)
	ax.legend()#for showing labels on graph
	plt.pause(0.0001)

def show_details(x,shape='polygon'):#for showing various details after every transformation
	if shape=='polygon':
		detc='NEW Co-ordinates(x,y): '
		for i in x[:-1]:
			detc+='('+str(i[0][0])+','+str(i[1][0])+')'+" "
		print(detc)

	else:
		print("center:(",x[0][0],",",x[1][0],") Height:",x[3][0],"Width:",x[2][0])

def query_handling(newx,x,shape):#for handing queries
	while 1:
		query=input("Query: ").split()
		if query[0].lower()=='q'or query[0].lower()=='quit':
			break
		elif query[0].upper()=='T':
			if len(query)!=3:
				print("Not sufficient values given")
				continue
			newx=translate(newx,float(query[1]),float(query[2]),shape)
		elif query[0].upper()=='R':
			if len(query)!=2:
				print("Not sufficient values given")
				continue
			newx=rotate(newx,float(query[1]),shape)
		elif query[0].upper()=='S':
			if len(query)!=3:
				print("Not sufficient values given")
				continue
			newx=scale(newx,float(query[1]),float(query[2]),shape)
		else:
			print("-----Not valid Query-----")
			continue
		show_details(newx,shape)
		if shape=='disc':
			show_disc(newx,x)
		else:
			show_polygon(newx)

if __name__=="__main__":
	while 1:
		shape=input("Enter shape: ")
		shape=shape.lower()
		if shape=="polygon":
			n=int(input("Enter No. of vertices: "))
			x=[]
			for i in range(n):
				x.append(list(map(float, input("enter coordinates(x,y): ").split())))
			x.append(x[0])
			newx=[]
			for i in range(len(x)):#conversion of list in required form so as to get it multiplied easily during matrix multiplication
				newx.append([[x[i][0]],[x[i][1]],[1]])
			#for plotting the very first polynomial
			yi=[]
			temp=[]
			for i in x:
				yi.append(i[1])
				temp.append(i[0])
			xi=temp
			fig = plt.figure('HW4 by 2018363')	
			plt.xlabel("X-axis")
			plt.ylabel("Y-axis")
			plt.grid()
			plt.plot(xi,yi,color='b',label='ORIGINAL')
			plt.legend()
			plt.pause(0.0001)

		elif shape=='disc':
			while 1:
				x=list(map(float, input("enter center coordinates and Radius: ").split()))
				if len(x)!=3:
					print("----please enter correct values---")
					continue
				break
			x.append(x[2])
			
			#plotting the very first disc
			fig=plt.figure("Disc")
			ax=plt.gca()
			orig_ellipse=Ellipse(xy=(x[0],x[1]),width=2*x[2],height=2*x[3],color='b', label="ORIGINAL")
			ax.add_patch(orig_ellipse)
			ax.grid()
			ax.set_xlabel("X-axis")
			ax.set_ylabel("Y-axis")
			ax.legend()#for showing labels on graph
			plt.pause(0.0001)

			newx=[]
			for i in range(len(x)):#conversion of list in required form so as to get it multiplied easily during matrix multiplication
				newx.append([x[i]])
		else:
			print("Non Recgnisable shape\n\tRe-enter")
			continue

		query_handling(newx,x,shape)
		break