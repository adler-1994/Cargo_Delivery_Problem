# Random Search implementation on the package delivery problem

import random
import numpy as np
import pandas as pd
import math

Num_Lorries_sample = 100000
Case = "2019.4"
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

# sort the indexes of COMPANIES in desending order
companies_lorries = list(zip(COMPANIES, COMPLORRIES, COMPDISTEMPTY,COMPFARES))       #  here a change
sorted_companies_lorries = sorted(companies_lorries, key=lambda x: x[1], reverse=True)
COMPANIES = [x[0] for x in sorted_companies_lorries]
COMPLORRIES = [x[1] for x in sorted_companies_lorries]
COMPDISTEMPTY = [x[2] for x in sorted_companies_lorries]    # here a change
COMPFARES = [x[3] for x in sorted_companies_lorries]    
#print(COMPANIES)
#print(COMPLORRIES)

#concatenate our lorries with third party lorries
LORRIES_TP = []
TP = [COMPANIES[i] for i in range(len(COMPANIES)) for j in range(COMPLORRIES[i])]
LORRIES_TP.extend(LORRIES)
LORRIES_TP.extend(TP)
#print(f"Lorries_TP: {LORRIES_TP}")

# define refernces for of private lorries and third party lorries 
LORRIES_REFERENCE = []
LORRIES_REFERENCE.append(len(LORRIES)-1)
for i in range (len(COMPANIES)):
    LORRIES_REFERENCE.append(LORRIES_REFERENCE[i] + COMPLORRIES[i])
#print(f"LORRIES_REFERENCE: {LORRIES_REFERENCE}")

LORRIES_indexs = list(range(len(LORRIES_TP))) # change to match TP
#print(f"Lorries indexs: {LORRIES_indexs}")

# make the random samples and check if TP lorries are valid
samples = []
for i in range(Num_Lorries_sample):   
    samples.append(random.sample(LORRIES_indexs,len(PICKUPS))) # colecte random sample of lorries and check for validty
    j = 0
    while j < (len(PICKUPS)):
        index = next((d for d, val in enumerate(LORRIES_REFERENCE) if val >= samples[i][j]), len(LORRIES_REFERENCE))
        if index == 0:
            j +=1
            continue
        elif distance_matrix[(LORRIES_TP[samples[i][j]]-1)*number_of_cities+PICKUPS[j]-1] <= COMPDISTEMPTY[index-1]:
            j +=1
            continue
        else:
            random_number = random.randint(LORRIES_indexs[0], LORRIES_indexs[-1])
            while random_number in samples[i]:
                random_number = random.randint(LORRIES_indexs[0], LORRIES_indexs[-1])             
            samples[i][j]= random_number

PICK_DROP_DIST = []
for i in range(len(PICKUPS)): 
    PICK_DROP_DIST.append(distance_matrix[(PICKUPS[i]-1)*number_of_cities+DROPOFF[i]-1])

best_fitness = float('inf')  # set to inifnty
for i in range(Num_Lorries_sample):
    fitness = 0
    for j in range(len(PICKUPS)):
        index = next((d for d, val in enumerate(LORRIES_REFERENCE) if val >= samples[i][j]), len(LORRIES_REFERENCE))
        if index == 0:
            fitness += PICK_DROP_DIST[j] + distance_matrix[(LORRIES_TP[samples[i][j]]-1)*number_of_cities+PICKUPS[j]-1] # empty + full distatnce OURS
        else:
            fitness += PICK_DROP_DIST[j]*COMPFARES[index-1] # full distance TP

    if (fitness < best_fitness):
        best_fitness = fitness
        best_index = i
        print(f"sample {best_index+1} : dist {best_fitness}")

print(f"\Best Lorries sample is {best_index+1}: {samples[best_index][:]} with total distance of : {best_fitness}")
    

#print(dist_matrix.values[(start-1)*num_cities_execl+end-1][2])  # distance between cities 
