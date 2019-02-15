"""
@author: Halit Uyanık
"""
import sys
import numpy as np
import random

class Location:
    def __init__(self, ID, demand, x, y):
        self.demand = demand
        self.ID = ID
        self.x = x
        self.y = y
        self.vehicle_id = -1
        self.region = 0   # which region
        self.region_i = 0 # which order in region
    def __str__(self):
        return "ID: " + str(self.ID) + " Demand: " + str(self.demand) + \
                " x: " + str(self.x) + " y: " + str(self.y) + " region index: " + str(self.region) + \
                " region order: " + str(self.region_i) + \
                " vehicle ID: " + str(self.vehicle_id)

def read_file(file_name):
    f = open(file_name)
    N, V, c = [int(el) for el in f.readline().rstrip().split(" ")]
    #print("Number of customers: ", N, " Number of vehicles: ", V, " Vehicle capacity: ", c)
    location_list = []
    ID_ctr = 0
    empty_lines = 0
    for line in f:
        try:
            line_items = [el for el in line.rstrip().split(" ")] 
            location_list.append(Location(ID_ctr, int(line_items[0]), float(line_items[1]), float(line_items[2])))
            ID_ctr += 1
        except:
            #print("Empty Line.")
            empty_lines += 1
    #if empty_lines > 0:
        #print("Number of empty lines: ", empty_lines)            
    return N, V, c, location_list

def euclidean_distance(x, x_i, y, y_i):
    return np.sqrt((x - x_i)**2 + (y - y_i)**2)

def path_total_demand(v, locations):
    demand = 0
    for loc in locations:
        if loc.vehicle_id == v:
            demand += loc.demand
    return demand

def feasibilty(population, c, V, locations):
    for v in range(V):
        demand = 0
        for i in range(1, len(population)):
            if population[i] == v:
                demand += locations[i].demand
        if demand > c:
            return False
    return True

def list_feasibility(population, c, V, locations):
    for p in population:
        if not feasibilty(p, c, V, locations):
            return False
    return True

def initialSolution(N, V, c, location_list):
    global pList
    # Initial sorting
    locations = sorted(location_list[1:], key=lambda x: x.demand, reverse=True)
    # Rules:
    # If it is not possible to keep two demands in the same location they have to be in different vehicles!
    # So first we separate these points.
    v = 0
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            if locations[i].demand + locations[j].demand > c:
                v += 1
                break
    for i in range(v):
        locations[i].vehicle_id = i
    guaranteedLocations = locations[:v]
    locations = locations[v:]

    # Second Rule:
    # We need to select points which are closest to a given point
    # But the problem is to put them in a way that can fill the maximum capacity of the vehicle!
    for i in range(v):
        pList = []
        crr_x, crr_y = guaranteedLocations[i].x, guaranteedLocations[i].y
        locations = sorted(locations, key=lambda x: euclidean_distance(x.x, crr_x, x.y, crr_y))

        # Get the locations which satisfy the vehicle limit condition
        demand_list = [x for x in locations]
        perfectSubset(demand_list, len(demand_list), c - guaranteedLocations[i].demand)
        # Sort the lists (pList) in ascending order according to their sum distance to current location
        # and take the first list
        pList = sorted(pList, key=lambda x: total_distance(crr_x, crr_y, x), reverse=False)[0]
        # Add them to the current vehicle list
        for p in pList:
            p.vehicle_id = i
        # remove them from the locations
        for p in pList:
            locations.remove(p)
    # Third Rule:
    # Remaining points should be dispersed in a way that wont cause too much distanced relationships
    # For remaining vehicles most important part is to choose a central point!
    for i in range(v, V):
        # Random selection
        init = np.random.choice(locations, 1)[0]

        # High demand selection
        # init = sorted(locations, key=lambda x: x.demand, reverse=True)[0]

        init.vehicle_id = i
        locations.remove(init)

        crr_x, crr_y = init.x, init.y

        locations = sorted(locations, key=lambda x: euclidean_distance(x.x, crr_x, x.y, crr_y))

        # Get the locations which satisfy the vehicle limit condition
        pList = []
        demand_list = [x for x in locations]
        perfectSubset(demand_list, len(demand_list), c - init.demand)

        if len(pList) == 0:
            continue
        else:     
            # Sort the lists (pList) in ascending order according to their sum distance to current location
            # and take the first list
            pList = sorted(pList, key=lambda x: total_distance(crr_x, crr_y, x), reverse=False)[0]
            # Add them to the current vehicle list
            for p in pList:
                p.vehicle_id = i
            # remove them from the locations
            for p in pList:
                locations.remove(p)
    # Fourth Rule:
    # if there are any demands left untouched put them into any of the feasible vehicles
    for loc in locations:
        for v in range(V):
            if path_total_demand(v, location_list) + loc.demand <= c:
                loc.vehicle_id = v
                break

def total_distance(crr_x, crr_y, x):
    # Distance from one point to another
    distance = 0.0
    o_x, o_y = crr_x, crr_y
    passer = x.copy()
    passer = sorted(passer, key=lambda el: euclidean_distance(el.x, o_x, el.y, o_y), reverse=False)
    while len(passer) > 0:
        distance += euclidean_distance(passer[0].x, o_x, passer[0].y, o_y)
        o_x, o_y = passer[0].x, passer[0].y
        passer = passer[1:]
        passer = sorted(passer, key=lambda el: euclidean_distance(el.x, o_x, el.y, o_y), reverse=False)

    return distance

# return True and return False are added later on may create problems!
pList = []
def subset(array, i, S, p):
    global dp, pList
    if len(pList) > 0:
        return True

    if i == 0 and S != 0 and dp[0][S]:
        p.append(array[i])
        #
        pList.append(p.copy())
        #
        #print(p)
        p.clear()
        return True
    
    if i == 0 and S == 0:
        #
        pList.append(p.copy())
        #        
        #print(p)
        p.clear()
        return True
    
    if dp[i-1][S]:
        b = []
        b = [item for item in p]
        subset(array, i-1, S, b)
    
    if S >= array[i].demand and dp[i-1][S-array[i].demand]:
        p.append(array[i])
        subset(array, i-1, S-array[i].demand,p)

dp = []
# Finding Perfect Sum Subsets Using DP
def perfectSubset(array, n, S):
    global dp
    if n == 0 or S < 0:
        return True
    
    dp = np.zeros((n, S + 1), dtype=bool)
    for i in range(n):
        dp[i][0] = True
    if array[0].demand <= S:
        dp[0][array[0].demand] = True
    for i in range(n):
        for j in range(S+1):
            if array[i].demand <= j:
                dp[i][j] = (dp[i-1][j] or dp[i-1][j-array[i].demand])
            else:
                dp[i][j] = dp[i-1][j]
    if dp[n-1][S] == False:
        # print("No subsets exist for given sum!")
        return False
    p = []
    subset(array, n-1, S, p)

import matplotlib.pyplot as plt
import copy

if __name__ == "__main__":
    N, V, c, location_list = read_file(sys.argv[1])
    
    best_solution = copy.deepcopy(location_list)
    best_distance = 1e100
    for i in range(50):

        initialSolution(N, V, c, location_list)

        origin = location_list[0]
        init_s = location_list[1:]

        total_dist = 0.0
        for v in range(V):
            vehicle_locs = [loc for loc in init_s if loc.vehicle_id == v]

            """
            Fix the distances
            """
            # First go towards outer side
            if vehicle_locs:
                # Take closest point as start
                vehicle_locs = sorted(vehicle_locs, key=lambda x: euclidean_distance(x.x, origin.x, x.y, origin.y), reverse=False)
                passerMemo = vehicle_locs.copy()
                initialLoc = vehicle_locs[0]
                crr_x, crr_y = initialLoc.x, initialLoc.y
                #
                step = 1
                outer_locs = [loc for loc in vehicle_locs[1:] if euclidean_distance(loc.x, origin.x, loc.y, origin.y) > euclidean_distance(initialLoc.x, origin.x, initialLoc.y, origin.y)]
                # While it is possible to go further outer
                while len(outer_locs) != 0:
                    outer_locs = sorted(outer_locs, key=lambda x: euclidean_distance(x.x, crr_x, x.y, crr_y), reverse=False)
                    crr_x, crr_y = outer_locs[0].x, outer_locs[0].y
                    vehicle_locs[step] = outer_locs[0]
                    outer_locs.remove(outer_locs[0])
                    step += 1
                    outer_locs = [loc for loc in outer_locs if euclidean_distance(loc.x, origin.x, loc.y, origin.y) > euclidean_distance(initialLoc.x, origin.x, initialLoc.y, origin.y)]
                    if len(outer_locs) == 0:
                        step -= 1
                # Rest is to choose furthest from origin at each step
                innerLocs = [loc for loc in passerMemo if not loc in vehicle_locs[:step]]
                while len(innerLocs) != 0:
                    nextLoc = sorted(innerLocs, key=lambda x: euclidean_distance(x.x, origin.x, x.y, origin.y), reverse=True)[0]
                    vehicle_locs[step] = nextLoc
                    step += 1
                    innerLocs.remove(nextLoc)
            """
            Distance Fix Done
            """

            curr_x, curr_y = origin.x, origin.y
            curr_dist = 0.0
            demand = 0
            for loc in vehicle_locs:
                demand += loc.demand

                curr_dist += euclidean_distance(loc.x, curr_x, loc.y, curr_y)
                curr_x = loc.x
                curr_y = loc.y
            # Dont forget the last return to warehouse
            curr_dist += euclidean_distance(origin.x, curr_x, origin.y, curr_y)
            total_dist += curr_dist

        if total_dist < best_distance:
            best_distance = total_dist
            best_solution = copy.deepcopy(location_list)

        if i == 49:
            init_s = best_solution[1:]
            # Printing results
            print(best_distance)
            for v in range(V):
                vehicle_locs = [loc for loc in init_s if loc.vehicle_id == v]
                """
                Fix the distances
                """
                # First go towards outer side
                if vehicle_locs:
                    # Take closest point as start
                    vehicle_locs = sorted(vehicle_locs, key=lambda x: euclidean_distance(x.x, origin.x, x.y, origin.y), reverse=False)
                    passerMemo = vehicle_locs.copy()
                    initialLoc = vehicle_locs[0]
                    crr_x, crr_y = initialLoc.x, initialLoc.y
                    #
                    step = 1
                    outer_locs = [loc for loc in vehicle_locs[1:] if euclidean_distance(loc.x, origin.x, loc.y, origin.y) > euclidean_distance(initialLoc.x, origin.x, initialLoc.y, origin.y)]
                    # While it is possible to go further outer
                    while len(outer_locs) != 0:
                        outer_locs = sorted(outer_locs, key=lambda x: euclidean_distance(x.x, crr_x, x.y, crr_y), reverse=False)
                        crr_x, crr_y = outer_locs[0].x, outer_locs[0].y
                        vehicle_locs[step] = outer_locs[0]
                        outer_locs.remove(outer_locs[0])
                        step += 1
                        outer_locs = [loc for loc in outer_locs if euclidean_distance(loc.x, origin.x, loc.y, origin.y) > euclidean_distance(initialLoc.x, origin.x, initialLoc.y, origin.y)]
                        if len(outer_locs) == 0:
                            step -= 1
                    # Rest is to choose furthest from origin at each step
                    innerLocs = [loc for loc in passerMemo if not loc in vehicle_locs[:step]]
                    while len(innerLocs) != 0:
                        nextLoc = sorted(innerLocs, key=lambda x: euclidean_distance(x.x, origin.x, x.y, origin.y), reverse=True)[0]
                        vehicle_locs[step] = nextLoc
                        step += 1
                        innerLocs.remove(nextLoc)
                """
                Distance Fix Done
                """        
                print(0, end=' ')
                for loc in vehicle_locs:
                    print(str(loc.ID), end=' ')
                if v == V - 1:
                    print(0, end='')
                else:
                    print(0)