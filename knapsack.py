"""
@author: Halit Uyanık
"""
import numpy as np
import sys
from sklearn.preprocessing import normalize

def read_data_less_memo(file_name):
    file_o = open(file_name, 'r')
    # Read first line for content info
    info = file_o.readline().rstrip().split(" ")

    item_count = int(info[0])
    K_val = int(info[1])

    # Read items
    profit_list = np.zeros(item_count, dtype=int)
    weight_list = np.zeros(item_count, dtype=int)

    index = 0
    for line in file_o:
        try:
            new_item_info = line.rstrip().split(" ")

            profit_list[index] = int(new_item_info[0])
            weight_list[index] = int(new_item_info[-1])

            index += 1
        except:
            pass

    return K_val, item_count, weight_list, profit_list

"""
Main space optimized DP algorithm
Details about how it works is given in REPORT.txt
max_holder holds an array for each Weight which is always updated when a more optimal solution
for that weight is found.
This continue for all objects. Objects are sorted according to their fitness value
"""
def optimized_dynamic_solver(profits, weights, N, K):
    dynamicMatrix = np.zeros(K + 1)
    max_holder = []
    for i in range(K+1):
        max_holder.append([])

    for i in range(N):
        for j in range(K, -1, -1):
            if j < weights[i]:
                break
            before = dynamicMatrix[j]
            dynamicMatrix[j] = max(dynamicMatrix[j], profits[i] + dynamicMatrix[j - weights[i]])

            if dynamicMatrix[j] != before:
                # Reset the location
                max_holder[j] = []
                for item in max_holder[j - weights[i]]:
                    max_holder[j].append(item)
                max_holder[j].append(i)

    return max_holder[K], dynamicMatrix[K]

def main(data_f):
    # Generate data
    K_val, item_count, weight_list, profit_list = read_data_less_memo(data_f)
    # Sort data
    # Penalty of weight is higher
    # 
    perm = ((profit_list / weight_list) * (1.0 / weight_list)).argsort()

    profit_list = profit_list[perm]
    weight_list = weight_list[perm]

    # Run the algorithm
    items, max_val = optimized_dynamic_solver(profit_list, weight_list, item_count, K_val)

    # Get the original indices since we sorted
    originalIndices = np.array(perm).take(items)

    # Print results
    print(int(max_val))
    for i in range(item_count):
        if i in originalIndices:
            print(1, end=' ')
        else:
            print(0, end=' ')

if __name__ == "__main__":
    main(sys.argv[1])

