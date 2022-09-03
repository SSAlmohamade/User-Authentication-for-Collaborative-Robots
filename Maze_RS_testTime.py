#!/usr/bin/env python

# KUKA API for ROS

# Oct 2019 Shurook Amohamade  Shurook2017@hotmail.com.com
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
from Maze_extract_features import*
from Maze_extract_featuresTime import*
from ML import*

'''---------------------------------------------------- '''

''' Information befor start'''

filename='Result_2_segments_RF'
Interval = 0.1      # Collectin data evry (?) seconds
Task_No =1 # How many task you wat to do 
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

def Op_Mode(my_client):
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
		# for ssfety reason, we  should limit the velocity when compliance is off
		 time.sleep(Interval)
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
    
def Create_profile_For_TestData(Data,userID,task):
	Feature_object=Features()
    	time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z =PraData(Data)
	
	ToolForce_Magnitude = Feature_object.Compute_Magnitude(ToolForce_x,ToolForce_y,ToolForce_z)
	ToolTorque_Magnitude = Feature_object.Compute_Magnitude(ToolTorque_x,ToolTorque_y,ToolTorque_z)
	
	# find feataer
	TF_x_Feature= Feature_object.FindFeatures(ToolForce_x)
	TF_y_Feature= Feature_object.FindFeatures(ToolForce_y)
	TF_z_Feature= Feature_object.FindFeatures(ToolForce_z)
	TF_M_Feature= Feature_object.FindFeatures(ToolForce_Magnitude)
	
	TT_x_Feature= Feature_object.FindFeatures(ToolTorque_x)
	TT_y_Feature= Feature_object.FindFeatures(ToolTorque_y)
	TT_z_Feature= Feature_object.FindFeatures(ToolTorque_z)
	TT_M_Feature= Feature_object.FindFeatures(ToolTorque_Magnitude)
	
	# create profile 
	T= time_stamp[len(time_stamp)-1]-time_stamp[0]
	
	#34 featuers
	#profile	=Feature_object.Creatprofile_test_selected_featuers34(task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature)
	
	#19 featuers
	profile	=Feature_object.Creatprofile_test_selected_featuers19(task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature)
	
	print 'profile',profile
	return profile
		
		
def PraData(Data):
		time_stamp=[]
		Toolpos_x=[]
		Toolpos_y=[]
		Toolpos_z=[]
		ToolForce_x=[]
		ToolForce_y=[]
		ToolForce_z=[]
		ToolTorque_x=[]
		ToolTorque_y=[]
		ToolTorque_z=[]
		Task_No=[]
		for i in Data:
		    time_stamp.append(i[0])
		    Task_No.append(i[1])
		    
		    Toolpos_x.append(i[9])
		    Toolpos_y.append(i[10])
		    Toolpos_z.append(i[11])
		    
		    ToolForce_x.append(i[15])
		    ToolForce_y.append(i[16])
		    ToolForce_z.append(i[17])
		    
		    ToolTorque_x.append(i[18])
		    ToolTorque_y.append(i[19])
		    ToolTorque_z.append(i[20]) 
		    
		time_stamp=np.array(time_stamp).astype(float)
		
		Task_No=np.array(Task_No).astype(int)
		
		Toolpos_x=np.array(Toolpos_x).astype(float)
		Toolpos_y=np.array(Toolpos_y).astype(float)
		Toolpos_z=np.array(Toolpos_z).astype(float)
		
		ToolForce_x=np.array(ToolForce_x).astype(float)
		ToolForce_y=np.array(ToolForce_y).astype(float)
		ToolForce_z=np.array(ToolForce_z).astype(float)
		
		ToolTorque_x=np.array(ToolTorque_x).astype(float)
		ToolTorque_y=np.array(ToolTorque_y).astype(float)
		ToolTorque_z=np.array(ToolTorque_z).astype(float)
		
		return time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z
		
def Authentication(DataFile,profile):
	ML_Object=Machine_Learning()
	print '---------------'
	print '---------------'
	x_Data=[]
	y_Lable=[]
	with open(DataFile) as csvfile:
			next (csvfile)
			next (csvfile)
			Data = csv.reader(csvfile,delimiter=',')
			for i in Data:
				y_Lable.append(i[0])
				x_Data.append(i[1:])
			#print y_Lable
			#print shape(x_Data)
			#print shape(profile)
					
	csvfile.close()
	
	Y_pred, Y_prob= ML_Object.Random_ForestClassifier(profile,x_Data,y_Lable)
    
	return Y_pred, Y_prob
	
	
def Trust_Model(Y_pred, Y_prob, Tscore,Z,TS):
	
	
	
	
	if  Y_prob>=0.5:
		
		Tscore=min(Tscore+((Z/2)+Y_prob),100)
		
	elif  Y_prob<0.5 and Y_prob>=0.3:
		Tscore=max(Tscore-((Z/2)-Y_prob),0)
		
	else:
		Tscore=max(Tscore-(Z),0)
		
		
	return Tscore
		
def Save_Data(Data):
		
		with open(filename +'.csv', 'a') as writeFile:
			writer = csv.writer(writeFile , delimiter = ',')
			writer.writerow(Data)
		writeFile.close()
		
 
	
#==================================================================================================================================================	
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
			
	
		
		
		
    def new_task(self, client,Task_No,Present_task):
        client.send_command('resetCompliance')  
        # Compliance OFF
        #print'Compliance OFF\n'
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
		Temp_Data.append(my_client.ToolPosition[0][0])
		Temp_Data.append(my_client.ToolPosition [0][1])
		Temp_Data.append(my_client.ToolPosition[0][2])
		Temp_Data.append(my_client.ToolPosition[0][3])
		Temp_Data.append(my_client.ToolPosition[0][4])
		Temp_Data.append(my_client.ToolPosition[0][5])
		
		
		Temp_Data.append(my_client.ToolForce[0][0]) 
		Temp_Data.append(my_client.ToolForce[0][1]) 
		Temp_Data.append(my_client.ToolForce[0][2])
		
		Temp_Data.append(my_client.ToolTorque [0][0]) 
		Temp_Data.append(my_client.ToolTorque[0][1]) 
		Temp_Data.append(my_client.ToolTorque[0][2]) 
		
		
		
		'''-----------------------------------------'''
		'''Joint Data'''
		Temp_Data.append(my_client.JointPosition[0][0])
		Temp_Data.append(my_client.JointPosition[0][1])
		Temp_Data.append(my_client.JointPosition[0][2])
		Temp_Data.append(my_client.JointPosition[0][3])
		Temp_Data.append(my_client.JointPosition[0][4])
		Temp_Data.append(my_client.JointPosition[0][5])
		Temp_Data.append(my_client.JointPosition[0][6])
		
		'''-----------------------------------------'''
		'''Joint Jerk, Acceleration,Velocity '''
		Temp_Data.append(my_client.JointJerk [0]) 
		Temp_Data.append(my_client.JointVelocity [0]) 
		Temp_Data.append(my_client.JointAcceleration[0])  
		
		return Temp_Data
		
		

#======================================[   Main   ]===================================

if __name__ == '__main__':
    
    Present_task=1

    ''' Creat object ( end point)'''
    End_point = Maze(470, 274,140) # point No:1
    

    ''' Creat new csv file as 'name of user.csv'''
    my_client = kuka_iiwa_ros_client()                                  # Making a connection object.
   

    '''--- Waiting kuka iiwa connecting---'''
    print '\n-----------------[ Start ]---------------------------'
    Op_Mode(my_client)
    while (not my_client.isready): pass  
    #print 'Ok Ready'
   
   
    print 'Task_No =',Present_task
    new_start(my_client)  
    
         
    ''' Start'''  
    start =time.time() 
    print('start1',start)
    Timestep= time.time() -start
    loopNo=0
    Data1=[]
    Data2=[]
    
    
    Data=[]
    Tscore=100
    Z=7
    TS=0.5
    Trust_limit=80
    Proba=[]
    Trust=[]
    y_prd=[]
    
    Proba.append(filename+"_proba")
    Trust.append(filename+"_trust")
    y_prd .append(filename+"_pred")
   
    print 'Tscore=',Tscore
   
    
    while True:
		
		
		if End_point.is_EndOf_maze(my_client):
			Present_task=Present_task+1
			profile=Create_profile_For_TestData(Data2,filename,Present_task)
			Y_pred, Y_prob= Authentication('profile_2Segment_2_23.csv',profile)
			print 'Y_prob',Y_prob
			Tscore= Trust_Model(Y_pred, Y_prob, Tscore,Z,TS)
			print 'Tscore=',Tscore
			Proba.append(Y_prob)
			Trust.append(Tscore)
			y_prd.append(Y_pred)
			
			Save_Data(Proba)
			Save_Data(Trust)
			Save_Data(y_prd)
			
			if Tscore> Trust_limit:
				
				End_point.new_task(my_client,Task_No,Present_task)
			else:
				print 'Tscore=',Tscore
				print ('Stop !!!!')
				End_point.new_task(my_client,Task_No,Present_task)
			
		
			
			print('start2',start)
			start =time.time() 
			Timestep= time.time() -start
			
		else:
			
			T=round(Timestep,5)
			
			if loopNo == 0:
				Present_task=0
				Timestep=0.0
				Temp_Data =End_point.Read_data(my_client,Timestep,Present_task)
				Data1.append(Temp_Data)
				
				
				
			else:
				if (T<=4): 
					print ('S1',T)
					time.sleep(Interval)
					Timestep= time.time()-start
					Temp_Data =End_point.Read_data(my_client,Timestep,Present_task)
					Data1.append(Temp_Data)
					T=round(Timestep,5)
					
					if (T>4): 
							
							profile=Create_profile_For_TestData(Data1,filename,Present_task)
							Y_pred, Y_prob= Authentication('profile_2Segment_2_23.csv',profile)
							print 'Y_prob',Y_prob
							Tscore= Trust_Model(Y_pred, Y_prob, Tscore,Z,TS)
							print 'Tscore=',Tscore
							Proba.append(Y_prob)
							Trust.append(Tscore)
							y_prd.append(Y_pred)
							
							Save_Data(Proba)
							Save_Data(Trust)
							Save_Data(y_prd)
							T=round(Timestep,5)
					
					
					
				
					
					
				elif(T>4): 
					print ('S2',T)
					
					time.sleep(Interval)
					Timestep= time.time()-start
					Temp_Data =End_point.Read_data(my_client,Timestep,Present_task)
					Data2.append(Temp_Data)
					
					
										
					
		
		loopNo=loopNo + 1
		
		
   
    time.sleep(0.1)
    
    
	   
	
    print ('-----------[exit]----------')
    
#=========================================================================================

