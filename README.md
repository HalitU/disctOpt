# disctOpt
Optimizations for Knapsack, Graph Coloring, and Vehicle Routing Problems, which I have done for my graduate level course BLG 545 - Discrete Optimization.

This repository includes three different solution approaches, one for each of the problems mentioned above.

## Knapsack

### Problem Description

Problem is the most basic 0-1 knapsack problem. For a single knapsack we try to fit the most optimal items from a list.

### Solution

Knapsack solution gives %100 optimized result, *however* for very complex big data, you will most probably 
have to wait quite a lot to get these results.

Dynamic Programming approach is used as a basis. But since vanilla DP solution has O(n*W) complexity which creates memory problems for huge amounts of data. I used an approach described in [here](https://stackoverflow.com/questions/17246670/0-1-knapsack-dynamic-programming-optimazion-from-2d-matrix-to-1d-matrix) to code a space efficient DP solution. However, since this solution only gives the most optimal solution and not the items for it, I hold an array for each weight for the optimal solution throughout the iterations. Second improvement I made is to create a fitness function which sorts the items in knapsack according to their value/weight**2. Reason why I give square penalty is that I recieved best solutions for that setting.

## Graph Coloring

### Problem Description

Aim is to color a graph without two nodes sharing an edge having the same color while keeping the color number minimum.

### Solution

For Graph Coloring problem I used the algorithm approach defined in [1]. MXRLF coloring is used to choose the nodes with the highest possible effect on their neighborhoods.
This helps algorithm to separate nodes into two sets, those who have a colored and non-colored neighborhoods. At each coloring phase, a node is
colored, and second and the further nodes are choosen from the set which has the most neighborhoods to the neighborhoods of the first node
we colored. With this approach I was able to obtain pretty good results.

## Vehicle Routing

### Problem Description

We have a delivery network where we want to dispatch our vehicles to customers. Limitation is that each vehicle has a capacity and our customers have fixed demands. Total sum of vehicle capacities will always be larger then or equal to total demand. We want to set a route for each vehicle in our delivery network, so that each customer will be visited by only one vehicle, and all of their demands will be satisfied.

### Solution

Out of all of the problems here, my solution for the vehicle routing problem is probably the most dirty one as the code will probably look a little messy. I tried to adapt existing research papers about ant colony algorithms, but since I was always getting stuck at local optima while using them (probably because I was missing some essential perturbation details), I wrote my own algorithm.
First I identify the demands which cannot co-exist together. An example is for capacity 40, demands with 28 and 24. Then I put all these into
separate vehicles. On the next step, I try to give those same vehicles locations closest to their initial points I gave just earlier. After all
these vehicles reach max capacity or cannot take anymore. I take the remaining vehicles and give them locations starting from the shortest-futhest
points away from origin until their capacity is also full. Method guarantees that there are no leftover demands.


## References
[1] Thang N. Bui, ThanhVu H. Nguyen, Chirag M. Patel, and Kim-Anh T. Phan. 2008. An ant-based algorithm for coloring graphs. Discrete Appl. Math. 156, 2 (January 2008), 190-200. DOI=http://dx.doi.org/10.1016/j.dam.2006.07.012