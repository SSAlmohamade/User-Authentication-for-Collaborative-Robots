#!/usr/bin/env python

# Stage 1 collect Data

# Jun 2019 Shurook Amohamade  Shurook2017@hotmail.com.com
# The University of Sheffield   http://www.sheffield.ac.uk/
#==================================================================================================================================
# This script:  
# 1- Derived from (demo5_ReadData.py and pic_and_place.py) https://github.com/jonaitken/KUKA-IIWA-API/blob/master/kuka_controller/
# 2- Generates a ROS node for communicating with KUKA iiwa
# 3- Dependence on [ conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot].
#==================================================================================================================================

'''Importing required libraries '''
from client_lib import *
import scipy.spatial.distance as Dist
import time, os
import csv
import math, numpy

'''---------------------------------------------------- '''

''' Information befor start'''

filename='User_'
Interval = 0.1      # Collectin data evry (?) seconds
Task_No = 15     
TaskInfo=Task_No
'''---------------------------------------------------- '''



def MaxT1Speed(my_client):
    my_client.send_command('setJointAcceleration 1.0')
    my_client.send_command('setJointVelocity 1.0')
    my_client.send_command('setJointJerk 1.0')
    my_client.send_command('setCartVelocity 1000')

def MaxT2Speed(my_client):
    my_client.send_command('setJointAcceleration 0.3')
    my_client.send_command('setJointVelocity 0.7')
    my_client.send_command('setJointJerk 0.3')
    my_client.send_command('setCartVelocity 1000')
   
def MaxAUTSpeed(my_client):
    my_client.send_command('setJointAcceleration 1.0')
    my_client.send_command('setJointVelocity 1.0')
    my_client.send_command('setJointJerk 1.0')
    my_client.send_command('setCartVelocity 1000')

def Op_Mode(client):
	global stableFT
	
	#1-Go to start position '
	my_client.send_command('setTool tool1')
	if my_client.OperationMode[0] == 'T1':
		MaxT1Speed(my_client)
		print 'OperationMode is T1'
	elif my_client.OperationMode[0] == 'T2':
		MaxT2Speed(my_client)
		print 'OperationMode is T2'
	else:
		print 'OperationMode is AUT'
		MaxAUTSpeed(my_client)
		#exit()

def new_start(client):
	global stableFT
	
	#time.sleep(0.5)
	is_safe=input(" Did you release the handle?  1= yes 2= No : ")
	while is_safe !=1:
	   is_safe=input("Did you release the handle?  1= yes 2= No")
	if is_safe ==1 :
		#  limit the velocity when compliance is off
		 client.send_command('setJointVelocity 0.5')
		 
		 client.send_command('setPositionXYZABC 472 -400 170 -180 0 -180 lin')
		 while Dist.euclidean(client.ToolPosition[0][0:3], [472, -400, 170]) > 10: pass
		 time.sleep(0.5)
		 stableFT = client.ToolForce[0]
		 while (Dist.cosine(stableFT, client.ToolForce[0]) < 0.1): pass
		 
		 #2-Turn on the Compliance ( alllow the hand guided) '
		 client.send_command('setJointVelocity 1.0')
		 client.send_command('setCompliance 8 8 50 300 300 300')# Compliance ON
		 print 'Compliance ON'
		 print '\n'  
	


def get_Velocity_and_Acceleration(client,p2x,p2y,p2z,T2,p1,T1,Velocity1):
	
	distance = math.sqrt( ((p1[0]-p2x)**2)+((p1[1]-p2y)**2)+((p1[2]-p2z)**2) )
	
	Vel_x= (p2x-p1[0])/(T2-T1)
	Vel_y= (p2y-p1[1])/(T2-T1)
	Vel_z= (p2z-p1[2])/(T2-T1)
	Velocity2=[Vel_x,Vel_y,Vel_z]
	
	
	
	
	#Acceleration x,y,z 
	Accel_x= (Velocity2[0]-Velocity1[0])/(T2-T1)
	Accel_y= (Velocity2[1]-Velocity1[1])/(T2-T1)
	Accel_z= (Velocity2[2]-Velocity1[2])/(T2-T1)
	Acceleration=[Accel_x,Accel_y,Accel_z]

	
	
	p1=p2
	T1=T2
	Velocity1=Velocity2
	return Velocity2,Acceleration,p1,T1
	
	
def get_spherical_coordinates(client,tool_pos):	
	radius      = math.sqrt( ((tool_pos[0])**2)+((tool_pos[1])**2)+((tool_pos[2])**2) )
	azimuth     = math.degrees(math.atan(tool_pos[1]/tool_pos[0]))
	inclination = math.degrees(math.acos(tool_pos[2]/radius))
	
	spherical_xyz=[radius,inclination,azimuth]
	
	#print 'spherical_xyz',spherical_xyz
	return spherical_xyz
	
		

class Maze:
    def __init__(self, x, y, z ):
        self.x = x
        self.y = y 
        self.z  = z
        
    def is_EndOf_maze(self, client):
		
		#3- Check if the currnt postion is the End Of maze ?  True: stop and go back' False: Print and Save data ' 
		
		if Dist.euclidean(client.ToolPosition[0][0:3], [self.x, self.y, self.z]) < 30: 
		    
		    return True
		else:
			
			return False
			
    def is_Testpoint(self, client):
		 
		
		if Dist.euclidean(client.ToolPosition[0][0:3], [self.x, self.y, self.z]) < 30: 
		    
		    return True
		else:
			
			return False	       
            
    def Print_data (self,client):
		#os.system('clear')
		print 'print data '
		print '==============================================='
		
		print 'Time\t=',my_client.OperationMode[1]
		print 'OperationMode\t=', my_client.OperationMode[0] 
		print 'isCollision\t=', my_client.isCollision[0]                # True when a collision has accured.
		print 'isCompliance\t=', my_client.isCompliance [0]             # True when robot is in Compliance mode.
		print 'isMastered\t=', my_client.isMastered[0]
		print 'isready\t\t=', my_client.isready                         # True when robot is connected
		print 'isReadyToMove\t=', my_client.isReadyToMove[0]            # True when robot can move, e.g. when the safety key is pressed...
		print 'ToolPosition:'                                 
		print  '\tX=', my_client.ToolPosition [0][0]
		print  '\tY=', my_client.ToolPosition [0][1]
		print  '\tZ=', my_client.ToolPosition [0][2]
		print  '\tA=', my_client.ToolPosition [0][3]
		print  '\tB=', my_client.ToolPosition [0][4]
		print  '\tC=', my_client.ToolPosition [0][5]
		print 'ToolForce\t=', my_client.ToolForce [0]                   # Reading Tool cartesian force
		print 'ToolTorque\t=', my_client.ToolTorque [0]                 # Reading Tool cartesian torque
		print 'JointAcceleration\t=', my_client.JointAcceleration [0]   # Current joint acceleration
		print 'JointJerk\t=', my_client.JointJerk  [0]                  # Current joint jerk
		print 'JointVelocity\t=', my_client.JointVelocity [0]           # Reading joints velocity
		# Reading joints position
		print 'JointPosition:'
		print  '\tA1=', my_client.JointPosition [0][0]
		print  '\tA2=', my_client.JointPosition [0][1]
		print  '\tA3=', my_client.JointPosition [0][2]
		print  '\tA4=', my_client.JointPosition [0][3]
		print  '\tA5=', my_client.JointPosition [0][4]
		print  '\tA6=', my_client.JointPosition [0][5]
		print  '\tA7=', my_client.JointPosition [0][6]
       
		
		print '==============================================='
		
		
    def new_task(self, client,Task_No,Present_task):
        client.send_command('resetCompliance')  
        # Compliance OFF
        time.sleep(1.5)
        client.send_command('setPositionXYZABC ' + str(self.x) + ' ' + str(self.y) + ' 170 -180 0 -180 ptp')  
        time.sleep(0.5)
        
        
        if  Task_No==Present_task:
			
			print'-------------------------------------------'
			print'\t[ Will done you do (',TaskInfo,') task/s ]'
			print'-------------------------------------------\n\n'
			exit()
        if  Task_No>0:
			
			print 'Task_No =',Present_task
			new_start(client)  
			Task_No=Task_No-1
		
    def Read_data (self, client,Timestep,Present_task):
		Temp_Data=[]
		
		
		
		Temp_Data.append(Timestep)
		Temp_Data.append(Present_task+1)
	
		Temp_Data.append(my_client.OperationMode[1])
		
		'''True false Data'''
		'''----------------------------------------'''
		Temp_Data.append(my_client.OperationMode[0])  
		Temp_Data.append(my_client.isCollision[0])
		Temp_Data.append(my_client.isCompliance[0])  
		Temp_Data.append(my_client.isMastered[0])
		Temp_Data.append(my_client.isready) 
		Temp_Data.append(my_client.isReadyToMove[0]) 
		'''-----------------------------------------'''
		
		'''End tool Data'''
		for i in range(6):
			Temp_Data.append(my_client.ToolPosition[0][i])
			
		for i in range(3):
			Temp_Data.append(my_client.ToolForce[0][i]) 
			
		for i in range(3):
			Temp_Data.append(my_client.ToolTorque [0][i])
			
		'''-----------------------------------------'''
		'''Joint Data'''
			
		for i in range(7):
			Temp_Data.append(my_client.JointPosition[0][i]) 

		'''-----------------------------------------'''
		'''Joint Jerk, Acceleration,Velocity '''
		Temp_Data.append(my_client.JointJerk [0]) 
		Temp_Data.append(my_client.JointVelocity [0]) 
		Temp_Data.append(my_client.JointAcceleration[0])  
		
		
		
		return Temp_Data
		
    def Save_Data(self,client, Data):
		with open(filename +'.csv', 'a') as writeFile:
			writer = csv.writer(writeFile , delimiter = ',')
			for row in Data:
				writer.writerow(row)
		writeFile.close()
		

#======================================[   Main   ]===================================

if __name__ == '__main__':
    #global stableFT
    Present_task=0
    ''' Creat object ( end point)'''
    End_point = Maze(470, 274,140) # point No:1
    Test_point = Maze(654, -57,158.7) # point No:2
    

    ''' Creat new csv file as 'name of user.csv'''
    my_client = kuka_iiwa_ros_client()               # Making a connection object.
    with open(filename +'.csv', 'w') as writeFile:
            writer = csv.writer(writeFile , delimiter = ',')
            writer.writerow([('Time/Second'),('Task_No'),('Time'),('OperationMode'),
            ('isCollision'),('isCompliance'),('isMastered'),('isready'),('isReadyToMove'),
            ('ToolPosition_x'),('ToolPosition_y'),('ToolPosition_z'),('ToolPosition_A'),('ToolPosition_b'),('ToolPosition_c'),
            ('ToolForce_x'),('ToolForce_y'),('ToolForce_z'),
            ('ToolTorque_x'),('ToolTorque_y'),('ToolTorque_z'),
            ('JointPosition'),('JointPosition'),('JointPosition'),('JointPosition'),('JointPosition'),('JointPosition'),('JointPosition'),
            ('JointJerk') ,('Tool_Velocity'),('Tool_Acceleration')])
    writeFile.close()

    '''--- Waiting kuka iiwa connecting---'''
    print '\n-----------------[ Start ]---------------------------'
    Op_Mode(my_client)
    while (not my_client.isready): pass  
    
   
   
    print 'Task_No =',Present_task
    new_start(my_client)  
    
         
    
    ''' Start'''  
    start =time.time() 
    Timestep= time.time() -start
    loopNo=0
    
    p1=[470, 274,140]
    T1=0.0
    Velocity1=[0.0,0.0,0.0]	
    Accl=[0.0,0.0,0.0]	
    #print 'Task_No',Task_No
    
    while True:
		Data=[]
		if End_point.is_EndOf_maze(my_client):
			
			Present_task=Present_task+1
			End_point.new_task(my_client,Task_No,Present_task)
			
			
		else:
			T=round(Timestep,2)
			
			if loopNo == 0:
				Present_task=0
				Timestep=0.0
				Temp_Data =End_point.Read_data(my_client,Timestep,Present_task)
				Data.append(Temp_Data)
				End_point.Save_Data(my_client,Data)
				
				
			else:
				time.sleep(Interval)
				Timestep= time.time()-start
				Temp_Data =End_point.Read_data(my_client,Timestep,Present_task)
				
				Data.append(Temp_Data)
				End_point.Save_Data(my_client,Data)
				
		       
		loopNo=loopNo + 1
       
    time.sleep(0.1)
	   
	
    print ('-----------[exit]----------')
    
#=========================================================================================

