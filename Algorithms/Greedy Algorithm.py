# Greedy Algorithm implementation on the package delivery problem


import random
import numpy as np
import pandas as pd
import math

Case = "2019.1"
#Read the problem instance
with open(Case + ".txt", 'r') as file:
    lines = file.readlines()
PICKUPS = list(map(int, lines[0].strip().split()))
DROPOFF = list(map(int, lines[1].strip().split()))
LORRIES = list(map(int, lines[2].strip().split()))
COMPANIES = list(map(int, lines[3].strip().split()))
COMPFARES = list(map(float, lines[5].strip().split()))
COMPLORRIES = list(map(int, lines[4].strip().split()))
COMPDISTEMPTY = list(map(int, lines[6].strip().split()))

#store distances in dist_matrix
Case = Case[:-2]
dist_matrix = pd.read_csv(Case + ".csv")
number_of_cities = int(math.sqrt(len(dist_matrix.values)))
distance_matrix = np.empty(len(dist_matrix.values),dtype=np.float16)
distance_matrix[:] = dist_matrix.iloc[:,2]  

# for later tests
PICKUPS1 = PICKUPS  
DROPOFF1 = DROPOFF 

# sort the indexes of COMPANIES in desending order
companies_lorries = list(zip(COMPANIES, COMPLORRIES, COMPDISTEMPTY,COMPFARES))       #  here a change
sorted_companies_lorries = sorted(companies_lorries, key=lambda x: x[1], reverse=True)
COMPANIES = [x[0] for x in sorted_companies_lorries]
COMPLORRIES = [x[1] for x in sorted_companies_lorries]
COMPDISTEMPTY = [x[2] for x in sorted_companies_lorries]    # here a change
COMPFARES = [x[3] for x in sorted_companies_lorries]        # here a change
#print(COMPANIES)
#print(COMPLORRIES)

 # to shuffle the indexes
temp_pickups =[]
temp_dropoff =[]
random_indexs = list(range(len(PICKUPS)))
random.shuffle(random_indexs)
#print(f"\ the shuffling vector is :{random_indexs}")
for i in random_indexs:
    temp_pickups.append(PICKUPS[i]) 
    temp_dropoff.append(DROPOFF[i])        
PICKUPS= temp_pickups    #SHUFFLED  PICKUPS
DROPOFF = temp_dropoff   #SHUFFLED  DROPOFF
#print(f"\ the new shuffled PICKUPS are :{PICKUPS}")
#print(f"\ the new shuffled DROPOFF are :{DROPOFF}")

#concatenate our lorries with third party lorries
LORRIES_TP = []
TP = [COMPANIES[i] for i in range(len(COMPANIES)) for j in range(COMPLORRIES[i])]
#print(f"TP lorries: {TP}")
LORRIES_TP.extend(LORRIES)
LORRIES_TP.extend(TP)
#print(f"Lorries_TP: {LORRIES_TP}")

# define refernces for of private lorries and third party lorries 
LORRIES_REFERENCE = []
LORRIES_REFERENCE.append(len(LORRIES)-1)
for i in range (len(COMPANIES)):
    LORRIES_REFERENCE.append(LORRIES_REFERENCE[i] + COMPLORRIES[i])
#print(f"LORRIES_REFERENCE: {LORRIES_REFERENCE}")


LORRIES_indexs = list(range(len(LORRIES_TP))) # change to match third party lorries
#print(f"Lorries indexs: {LORRIES_indexs}")

PICK_DROP_DIST = []
for i in range(len(PICKUPS)): 
    PICK_DROP_DIST.append(distance_matrix[(PICKUPS[i]-1)*number_of_cities+DROPOFF[i]-1]) # full distance 
PICK_DROP_DIST1 = []  
for i in range(len(PICKUPS)): 
    PICK_DROP_DIST1.append(distance_matrix[(PICKUPS1[i]-1)*number_of_cities+DROPOFF1[i]-1]) # full distance 
        
LORRIES_TEST = [0]* len(LORRIES_TP)    
LORRIES_TEST[:] = LORRIES_TP[:] 
LORRIES_Sample = []
total_fitness = 0
for i in range(len(PICKUPS)):
    best_fitness = float('inf') # set to inifnty
    remove = -1
    for j in range(len(LORRIES_TP)):
        if LORRIES_TP[j] == 0:
            continue
        else:    
            index = next((d for d, val in enumerate(LORRIES_REFERENCE) if val >= j), len(LORRIES_REFERENCE))
            #print(index)
            if index == 0:                  
                fitness =  PICK_DROP_DIST[i] + distance_matrix[(LORRIES_TP[j]-1)*number_of_cities+PICKUPS[i]-1]                       
            elif distance_matrix[(LORRIES_TP[j]-1)*number_of_cities+PICKUPS[i]-1] <= COMPDISTEMPTY[index-1]:                     
                fitness =  PICK_DROP_DIST[i]*COMPFARES[index-1]   
            else: 
                continue       
        if fitness < best_fitness:
            best_fitness = fitness
            remove = j
            
    LORRIES_Sample.append(remove)           
    LORRIES_TP[remove]=0  # remove the assigned lorry
    total_fitness += best_fitness        
    #print("total dist ", best_dist)
  

#assign the lorries to initial pickups dropoffs
LORRIES_finale =[0]* len(LORRIES_Sample)
for i in range(len(PICKUPS)):  
   LORRIES_finale[random_indexs[i]]= LORRIES_Sample[i]
    
LORRIES_Sample = LORRIES_finale   
print(f"\ Greedy Lorries sample is: {LORRIES_Sample} with total distance of : {total_fitness}")

"""
#for tests of consistency after shuffling packages
fitness = 0
for i in range(len(PICKUPS)):
            index = next((d for d, val in enumerate(LORRIES_REFERENCE) if val >= LORRIES_Sample[i]), len(LORRIES_REFERENCE))
            if index == 0:
               fitness += PICK_DROP_DIST1[i] + distance_matrix[(LORRIES_TEST[LORRIES_Sample[i]]-1)*number_of_cities+PICKUPS1[i]-1]
            elif distance_matrix[(LORRIES_TEST[LORRIES_Sample[i]]-1)*number_of_cities+PICKUPS1[i]-1] > COMPDISTEMPTY[index-1] :
              #fitness += 50000 
               fitness = float('inf')  # invalid soluation
               break
            else:
              fitness += PICK_DROP_DIST1[i]*COMPFARES[index-1]
              
print(fitness)
"""