#!/usr/bin/env python

#  Stage 2 Extracting Featurs 

# Jun 2019 Shurook Amohamade  Shurook2017@hotmail.com.com
# The university of sheffield   http://www.sheffield.ac.uk/
#==================================================================================================================================
# This script:  
#
#==================================================================================================================================

'''Importing required libraries '''

import scipy.spatial.distance as Dist
import time, os
import csv
import math
import numpy as np
from scipy.stats import skew,kurtosis
'''---------------------------------------------------- '''

#====================================================================================================================

class Features:
    

    def ImportData(self,DataFile):
		selected_data=[]
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
		
		#print '\n ********************************************************'
		#print ' 1- open file and import data '
		#print '********************************************************'
		print 'filename is  = ', DataFile
		
		with open(DataFile) as csvfile:
			next (csvfile)
			Data = csv.reader(csvfile,delimiter=',')
			for i in Data:
			    #print i [9]
			    
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
			#selected_data.append(temp)
			
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
		
	
			
			
    def FindFeatures(self,Tool_featuer):
		# ********************************************************'
		#2- Find Features'
		# ********************************************************'
		temp =[]
		
		Mean= np.mean(Tool_featuer)
		temp.append(Mean)
		
		STD= np.std(Tool_featuer)
		temp.append(STD)
		
		SKEW =skew(Tool_featuer)
		temp.append(SKEW)
		
		KURTOSIS =kurtosis(Tool_featuer)
		temp.append(KURTOSIS)
		
		return temp
		
		
		
    def Compute_Magnitude(self,Tool_x,Tool_y,Tool_z):
		Magnitude=[]
		
		for i in range(0,len (Tool_x)):
			Mag = math.sqrt((Tool_x[i])**2+(Tool_y[i])**2+(Tool_z[i])**2)
			Magnitude.append(Mag)
			
		return Magnitude
		
		
	
			

    def ExportFeatures (self,filename,Data):
		print '********************************************************'
		print 'Export Features to CSV file (Features_File ) '+filename
		print'********************************************************'
		
		with open(filename +'.csv', 'a') as writeFile:
			writer = csv.writer(writeFile , delimiter = ',')
			writer.writerow(Data)
		writeFile.close()
		
		
	# for selected featuers 34		
    def Creatprofile(self,userID,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
		profile =[]
		profile.append(userID)
		profile.append(task)
		profile.append(T)
		
		
		for  n in range(len(TF_x_Feature)):
			profile.append(TF_x_Feature[n])
			
		for  i in range(len(TF_y_Feature)):
			profile.append(TF_y_Feature[i])
			
		for  i in range(len(TF_z_Feature)):
			profile.append(TF_z_Feature[i])
			
		for  i in range(len(TF_M_Feature)):
			profile.append(TF_M_Feature[i])
			
			
		for  i in range(len(TT_x_Feature)):
			profile.append(TT_x_Feature[i])
			
		for  i in range(len(TT_y_Feature)):
			profile.append(TT_y_Feature[i])
			
		for  i in range(len(TT_z_Feature)):
			profile.append(TT_z_Feature[i])
			
		for  i in range(len(TT_M_Feature)):
			profile.append(TT_M_Feature[i])
		
		return profile
		
    def Creatprofile2(self,userID,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
		profile =[]
		profile.append(userID)
		#profile.append(task)
		profile.append(T)
		
		
		for  n in range(len(TF_x_Feature)):
			profile.append(TF_x_Feature[n])
			
		for  i in range(len(TF_y_Feature)):
			profile.append(TF_y_Feature[i])
			
		for  i in range(len(TF_z_Feature)):
			profile.append(TF_z_Feature[i])
			
		for  i in range(len(TF_M_Feature)):
			profile.append(TF_M_Feature[i])
			
			
		for  i in range(len(TT_x_Feature)):
			profile.append(TT_x_Feature[i])
			
		for  i in range(len(TT_y_Feature)):
			profile.append(TT_y_Feature[i])
			
		for  i in range(len(TT_z_Feature)):
			profile.append(TT_z_Feature[i])
			
		for  i in range(len(TT_M_Feature)):
			profile.append(TT_M_Feature[i])
		
		return profile
	
	# for selected featuers 34	
    def Creatprofile_test_selected_featuers34(self,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
		profile =[]
		
		profile.append(task)
		profile.append(T)
		
		
		for  n in range(len(TF_x_Feature)):
			profile.append(TF_x_Feature[n])
			
		for  i in range(len(TF_y_Feature)):
			profile.append(TF_y_Feature[i])
			
		for  i in range(len(TF_z_Feature)):
			profile.append(TF_z_Feature[i])
			
		for  i in range(len(TF_M_Feature)):
			profile.append(TF_M_Feature[i])
			
			
		for  i in range(len(TT_x_Feature)):
			profile.append(TT_x_Feature[i])
			
		for  i in range(len(TT_y_Feature)):
			profile.append(TT_y_Feature[i])
			
		for  i in range(len(TT_z_Feature)):
			profile.append(TT_z_Feature[i])
			
		for  i in range(len(TT_M_Feature)):
			profile.append(TT_M_Feature[i])
		
		return profile
		
	# for selected featuers 27
    def Creatprofile_test_selected_featuers27(self,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
	
		profile =[]
		
		#profile.append(task)
		#profile.append(T)
		
		
		for  n in range(len(TF_x_Feature)):
				profile.append(TF_x_Feature[n])
		
		for  i in range(len(TF_y_Feature)):
			profile.append(TF_y_Feature[i])
		
		for  i in range(len(TF_z_Feature)):
			profile.append(TF_z_Feature[i])
		
		for  i in range(len(TF_M_Feature)):
			profile.append(TF_M_Feature[i])
		
		
		for  i in range(len(TT_x_Feature)):
			profile.append(TT_x_Feature[i])
		
		for  i in range(len(TT_y_Feature)):
			profile.append(TT_y_Feature[i])
		
		
		profile.append(TT_z_Feature[0])
		profile.append(TT_z_Feature[1])
		profile.append(TT_z_Feature[0])
		
		
		
		
		
		return profile
	# for selected featuers 19
    def Creatprofile_featuers19(self,userID,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
	
		profile =[]
		profile.append(userID)
		#profile.append(task)
		profile.append(T)
		
		
		
		
		
		profile.append(TF_x_Feature[1])
		profile.append(TF_x_Feature[2])
		
		
		
		profile.append(TF_y_Feature[1])
		
		
		profile.append(TF_z_Feature[0])
		profile.append(TF_z_Feature[1])
		profile.append(TF_z_Feature[3])
		
		
		profile.append(TF_M_Feature[0])
		profile.append(TF_M_Feature[2])
		
		
		profile.append(TT_x_Feature[0])
		
		profile.append(TT_y_Feature[0])
		profile.append(TT_y_Feature[2])
		profile.append(TT_y_Feature[3])
		
		for  i in range(len(TT_z_Feature)):
			profile.append(TT_z_Feature[i])	
		
		profile.append(TT_M_Feature[0])
		profile.append(TT_M_Feature[1])
		
		
		
		return profile
	# for selected featuers 19
    def Creatprofile_test_selected_featuers19(self,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
	
		profile =[]
		
		#profile.append(task)
		profile.append(T)
		
		
		
		
		
		profile.append(TF_x_Feature[1])
		profile.append(TF_x_Feature[2])
		
		
		
		profile.append(TF_y_Feature[1])
		
		
		profile.append(TF_z_Feature[0])
		profile.append(TF_z_Feature[1])
		profile.append(TF_z_Feature[3])
		
		
		profile.append(TF_M_Feature[0])
		profile.append(TF_M_Feature[2])
		
		
		profile.append(TT_x_Feature[0])
		
		profile.append(TT_y_Feature[0])
		profile.append(TT_y_Feature[2])
		profile.append(TT_y_Feature[3])
		
		for  i in range(len(TT_z_Feature)):
			profile.append(TT_z_Feature[i])	
		
		profile.append(TT_M_Feature[0])
		profile.append(TT_M_Feature[1])
		
		
		
		return profile
	 
    def Creatprofile_test_selected_featuers24(self,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
		profile =[]
		
		#profile.append(task)
		#profile.append(T)
		
		
		
		
		profile.append(TF_x_Feature[3])
		
		
			
		for  i in range(len(TF_y_Feature)):
			profile.append(TF_y_Feature[i])
			
		for  i in range(len(TF_z_Feature)):
			profile.append(TF_z_Feature[i])
			
		for  i in range(len(TF_M_Feature)):
			profile.append(TF_M_Feature[i])
			
			
		for  i in range(len(TT_x_Feature)):
			profile.append(TT_x_Feature[i])
			
		
		profile.append(TT_y_Feature[0])
		profile.append(TT_y_Feature[1])
		profile.append(TT_y_Feature[2])
		
			
		
		profile.append(TT_z_Feature[0])
		profile.append(TT_z_Feature[3])
		
			
		
		profile.append(TT_M_Feature[0])
		profile.append(TT_M_Feature[2])
		
		
		return profile

    def featuers23(self,user,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature,SegmentNo):
		profile =[]
		
		#profile.append(task)
		#profile.append(userID)
		profile.append(T)
		
		
		
		for  n in range(len(TF_x_Feature)):
			profile.append(TF_x_Feature[n])
		
		
		profile.append(TF_y_Feature[1])
		profile.append(TF_y_Feature[2])
			
		for  i in range(len(TF_z_Feature)-1):
			profile.append(TF_z_Feature[i])
			
		
		profile.append(TF_M_Feature[0])
		profile.append(TF_M_Feature[1])
			
			
		
		profile.append(TT_x_Feature[0])
		profile.append(TT_x_Feature[1])
			
		
		profile.append(TT_y_Feature[0])
		profile.append(TT_y_Feature[1])
		profile.append(TT_y_Feature[2])
		
			
		
		for  i in range(len(TT_z_Feature)):
			profile.append(TT_z_Feature[i])	
		
			
		
		profile.append(TT_M_Feature[0])
		profile.append(TT_M_Feature[1])
		
		
		return profile

   
    def Create_1_profile(self,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user ):
		
	 
   
	    TF_x_Feature= Feature_1.FindFeatures(ToolForce_x)
	    TF_y_Feature= Feature_1.FindFeatures(ToolForce_y)
	    TF_z_Feature= Feature_1.FindFeatures(ToolForce_z)
	    TF_M_Feature= Feature_1.FindFeatures(ToolForce_Magnitude)
	    TT_x_Feature= Feature_1.FindFeatures(ToolTorque_x)
	    TT_y_Feature= Feature_1.FindFeatures(ToolTorque_y)
	    TT_z_Feature= Feature_1.FindFeatures(ToolTorque_z)
	    TT_M_Feature= Feature_1.FindFeatures(ToolTorque_Magnitude)
	    T= (time_stamp[len(time_stamp)-1]-time_stamp[0])/TaskNo
	    #print 'Time =',T
	    profile	=Feature_1.Creatprofile2(user,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature)	
	    print '\n----------------------------------------------------------------------------'	
	    #print'profile',profile
	    print '\n----------------------------------------------------------------------------'	
	    
	    Feature_1.ExportFeatures('profile_34F_EachUser1' ,profile)
	    #----------------------------------------------------------------------------
	    
    
    def Create_15_profile(self,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user ):
		 task =1
		 for j in range (1,TaskNo+1):
			TF_x=[]
			TF_y=[]
			TF_z=[]
			TT_x=[]
			TT_y=[]
			TT_z=[]
			TF_M=[]
			TT_M=[]
			Time_s=[]
			profile =[]
			profile2 =[]
			
			
			for i in range(len(Task_No)):
			    if (Task_No[i]==task):
				   #print 'task',task
				   #print 'Task_No[i]',Task_No[i]
				   TF_x.append(ToolForce_x[i])
				   TF_y.append(ToolForce_y[i])
				   TF_z.append(ToolForce_z[i])
				   TT_x.append(ToolTorque_x[i])
				   TT_y.append(ToolTorque_y[i])
				   TT_z.append(ToolTorque_z[i])
				   TF_M.append(ToolForce_Magnitude[i])
				   TT_M.append(ToolTorque_Magnitude[i])
				   Time_s.append(time_stamp[i])
				   
				   
			   
			
			
			TF_x_Feature= Feature_1.FindFeatures(TF_x)
			TF_y_Feature= Feature_1.FindFeatures(TF_y)
			TF_z_Feature= Feature_1.FindFeatures(TF_z)
			TF_M_Feature= Feature_1.FindFeatures(TF_M)
			
			TT_x_Feature= Feature_1.FindFeatures(TT_x)
			TT_y_Feature= Feature_1.FindFeatures(TT_y)
			TT_z_Feature= Feature_1.FindFeatures(TT_z)
			TT_M_Feature= Feature_1.FindFeatures(TT_M)
			
			print 'TF_x_Feature [',j,']',TF_x_Feature
			T= Time_s[len(Time_s)-1]-Time_s[0]
			#print 'Time =',T
			profile	=Feature_1.Creatprofile(user,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature)
			profile2=Feature_1.Creatprofile_featuers19(user,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature)	
				
			
				
			print '\n----------------------------------------------------------------------------'	
			print'profile',profile
			print '\n----------------------------------------------------------------------------'	
			fil_nm=str(task)
			
			Feature_1.ExportFeatures('profile_34F_EachUser15' ,profile)
			Feature_1.ExportFeatures('profile_19F_EachUser15' ,profile2)
			task+=1	
		
#===========================[   Main   ]=====================

if __name__ == '__main__':
    
    TaskNo =15
    fileID='User_.csv'
    user='User_21'
    
    ''' Creat object '''
    Feature_1 = Features()
    
    time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z = Feature_1.ImportData(user+'.csv')
   
    ToolForce_Magnitude = Feature_1.Compute_Magnitude(ToolForce_x,ToolForce_y,ToolForce_z)
    ToolTorque_Magnitude = Feature_1.Compute_Magnitude(ToolTorque_x,ToolTorque_y,ToolTorque_z)
    
   
    
    #''' Creat new csv file as 'name of user.csv'''
    #for i in range (1,15):
        #fil_nm=str(i)
        #with open('profile_34F_EachUser15.csv', 'w') as writeFile:
	            #writer = csv.writer(writeFile , delimiter = ',')
	            #writer.writerow([('userID '),('task '),('Time '),
	            #('ToolForce_xMean'),('ToolForce_xMax'),('ToolForce_xMin '),('ToolForce_xSTD '),('ToolForce_xSKEW '),('ToolForce_xKURTOSIS '),
	            #('ToolForce_yMean'),('ToolForce_yMax'),('ToolForce_yMin '),('ToolForce_y_STD'),('ToolForce_y_SKEW '),('ToolForce_y_KURTOSIS '),
	            #('ToolForce_z_Mean'),(' ToolForce_z_Max'),('ToolForce_z_Min '),('ToolForce_z_STD '),(' ToolForce_z_SKEW'),('ToolForce_z_KURTOSIS'),
	            #('ToolForce_M_Mean'),('ToolForce_M_Max'),('ToolForce_M_Min '),('ToolForce_M_STD '),('ToolForce_M_SKEW '),(' ToolForce_M_KURTOSIS'),
	            #('ToolTorque_x_Mean'),(' ToolTorque_x_Max'),('ToolTorque_x_Min '),('ToolTorque_x_STD '),(' ToolTorque_x_SKEW'),(' ToolTorque_x_KURTOSIS'),
	            #('ToolTorque_y_Mean'),('ToolTorque_y_Max'),('ToolTorque_y_Min '),('ToolTorque_y_STD '),('ToolTorque_y_SKEW '),(' ToolTorque_y_KURTOSIS'),
	            #('ToolTorque_z_Mean'),(' ToolTorque_z_Max'),(' ToolTorque_z_Min'),('ToolTorque_z_STD '),(' ToolTorque_z_SKEW'),('ToolTorque_z_KURTOSIS '),
	            #('ToolTorque_M_Mean'),('ToolTorque_M_Max'),(' ToolTorque_M_Min'),(' ToolTorque_M_STD'),('ToolTorque_M_SKEW '),('ToolTorque_M_KURTOSIS')])
	    
	    ##writefile.close()
	#--------------------------------------------------------
	 # create 1 profile from 15 tasks for each uesr
    #Feature_1.Create_1_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user )
    Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user )
    
    # create 15 profile from 15 tasks for each uesr
    for i in range(32):
		i_str=str(i)
		user='User_'+i_str
		#Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user )
		
	
    
