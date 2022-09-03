#!/usr/bin/env python

# KUKA API for ROS

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
#import pandas as pd
from scipy.stats import skew,kurtosis
from sklearn.preprocessing import minmax_scale
'''---------------------------------------------------- '''

#====================================================================================================================

class Features:
    

    def ImportData(self,DataFile):
		
		
		
		
		Alldata=[]
		
		
		#print '\n ********************************************************'
		#print ' 1- open file and import data '
		#print '********************************************************'
		print 'filename is  = ', DataFile
		
		with open(DataFile) as csvfile:
			next (csvfile)
			Data = csv.reader(csvfile,delimiter=',')
			for i in Data:
				Alldata.append(i)
		return Alldata
		
    def Data_segmentation(self, One_task):
		seg1=[]
		seg2=[]
		seg3=[]
		T=[]
		
		for t in One_task:
		    T.append(t[0])
		#print T
		T= minmax_scale (np.array(T))
		#print T
		
		j=0
		for i in One_task:
		    
		    print (i[0],T[j])
		    if (T[j] <=0.5):
				print ('s1: ',T[j])
				seg1.append(i)
				
		    if (T[j]>=0.5):# and T[j]<0.6): 
				print ('s2: ',T[j])
				seg2.append(i)
				
		    #else:
				#print ('s3: ',T[j])
				#seg3.append(i)
		    j+=1
		#print seg1
		
		return seg1,seg2,seg3
		
    def Selected_Data(self,segment):
	   
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
		
		for i in segment:
			    
			    
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
		#print 'Save data'
		with open(filename +'.csv', 'a') as writeFile:
			writer = csv.writer(writeFile , delimiter = ',')
			writer.writerow(Data)
		writeFile.close()
		
		
	# for selected featuers 34		
    def Creatprofile(self,userID,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature,SegmentNo):
		profile =[]
		profile.append(userID)
		profile.append(task)
		#profile.append(SegmentNo)
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
	 
    def Creatprofile_test_selected_featuers23(self,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature):
		profile =[]
		
		#profile.append(task)
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
		
    def featuers23(self,userID,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature,SegmentNo):
		profile =[]
		
		#profile.append(task)
		profile.append(userID)
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

   
	    
    
    def Create_15_profile(self,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user,SegmentNo,time_stamp ):
		 
			
			TF_x_Feature= Feature_1.FindFeatures(ToolForce_x)
			TF_y_Feature= Feature_1.FindFeatures(ToolForce_y)
			TF_z_Feature= Feature_1.FindFeatures(ToolForce_z)
			TF_M_Feature= Feature_1.FindFeatures(ToolForce_Magnitude)
			
			TT_x_Feature= Feature_1.FindFeatures(ToolTorque_x)
			TT_y_Feature= Feature_1.FindFeatures(ToolTorque_y)
			TT_z_Feature= Feature_1.FindFeatures(ToolTorque_z)
			TT_M_Feature= Feature_1.FindFeatures(ToolTorque_Magnitude)
			
			print 'TF_x_Feature [',j,']',TF_x_Feature
			print len(time_stamp)
			T= time_stamp[len(time_stamp)-1]-time_stamp[0]
			print 'Time =',T
			
			profile	 =   Feature_1.Creatprofile(user,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature,SegmentNo)
			profile2 =   Feature_1.featuers23(user,task,T,TF_x_Feature,TF_y_Feature,TF_z_Feature,TF_M_Feature,TT_x_Feature,TT_y_Feature,TT_z_Feature,TT_M_Feature,SegmentNo)	
			
				
			print '\n----------------------------------------------------------------------------'	
			print'profile',profile
			print '\n----------------------------------------------------------------------------'	
			fil_nm=str(task)
			#Feature_1.ExportFeatures('profile_TaskNo_'+fil_nm ,profile)
			Feature_1.ExportFeatures('profile_2Segment_2' ,profile)
			Feature_1.ExportFeatures('profile_2Segment_2_23' ,profile2)
			
		
#===========================[   Main   ]=====================

if __name__ == '__main__':
    
    TaskNo =15
    fileID='User_.csv'
    user='User_19'
   
    ''' Creat object '''
    Feature_1 = Features()
    
    
    AllData= Feature_1.ImportData(user+'.csv')
    
    
   
    
    task =1
    for j in range (15):
		oneTask=[]
		for i in AllData:
			 Task_No=np.array(i[1]).astype(int)
			 if (Task_No ==task):
				 oneTask.append(i)
		segment1,segment2,segment3= Feature_1.Data_segmentation(oneTask)
		#print 'segment3',segment3
		
		SegmentNo=1
		
		time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z = Feature_1.Selected_Data(segment1)
		ToolForce_Magnitude = Feature_1.Compute_Magnitude(ToolForce_x,ToolForce_y,ToolForce_z)
		ToolTorque_Magnitude = Feature_1.Compute_Magnitude(ToolTorque_x,ToolTorque_y,ToolTorque_z)
		Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user,SegmentNo,time_stamp)
		
		
		SegmentNo=2
		
		time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z = Feature_1.Selected_Data(segment2)
		ToolForce_Magnitude = Feature_1.Compute_Magnitude(ToolForce_x,ToolForce_y,ToolForce_z)
		ToolTorque_Magnitude = Feature_1.Compute_Magnitude(ToolTorque_x,ToolTorque_y,ToolTorque_z)
		Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user,SegmentNo,time_stamp)
		
		#SegmentNo=3
		
		#time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z = Feature_1.Selected_Data(segment3)
		#ToolForce_Magnitude = Feature_1.Compute_Magnitude(ToolForce_x,ToolForce_y,ToolForce_z)
		#ToolTorque_Magnitude = Feature_1.Compute_Magnitude(ToolTorque_x,ToolTorque_y,ToolTorque_z)
		#Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user,SegmentNo,time_stamp)
		
		
		task+=1
			 
		
    
    print 'oneTask',oneTask
    
   
    
    #time_stamp,Task_No,Toolpos_x,Toolpos_y,Toolpos_z,ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z = Feature_1.Selected_Data(user+'.csv')
   
    #ToolForce_Magnitude = Feature_1.Compute_Magnitude(ToolForce_x,ToolForce_y,ToolForce_z)
    #ToolTorque_Magnitude = Feature_1.Compute_Magnitude(ToolTorque_x,ToolTorque_y,ToolTorque_z)
    
   
  
	##--------------------------------------------------------
	 ## create 1 profile from 15 tasks for each uesr
    #Feature_1.Create_1_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user )
    #Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user )
    
    ## create 15 profile from 15 tasks for each uesr
    #for i in range(32):
		#i_str=str(i)
		#user='User_'+i_str
		##Feature_1.Create_15_profile(ToolForce_x,ToolForce_y,ToolForce_z,ToolTorque_x,ToolTorque_y,ToolTorque_z,ToolForce_Magnitude, ToolTorque_Magnitude,user )
		
	
    
