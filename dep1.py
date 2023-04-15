import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
with open('./all_dept.csv', 'r') as f:
    data_file = f.readlines()

# Create graph object
Graph1 = nx.DiGraph()
matrix = [[0 for _ in range(2000)] for _ in range(2000)]

# Add nodes and edges to graph
for line in data_file:
    source, dest, time = line.strip().split(' ')
    matrix[int(source)][int(dest)] +=1 
    Graph1.add_edge(int(source), int(dest), weight=float(time))
    
# print(matrix)

# Draw graph
pos = nx.spring_layout(Graph1)  # Compute layout
nx.draw_networkx_edges(Graph1, pos)
nx.draw_networkx_labels(Graph1, pos, font_size=5)

plt.title("Department-1 Visualization")
plt.show()


in_degrees = dict(Graph1.in_degree())
out_degrees = dict(Graph1.out_degree())
in__degrees_list = {}
for node in Graph1.nodes():
    in__degrees_list[node] = in_degrees[node]
    
print("Indegree:")
# print(in__degrees_list)


out__degrees_list = {}
for node in Graph1.nodes():
    out__degrees_list[node] = out_degrees[node]
    
print("Outdegree:")
# print(out__degrees_list)

degree_centrality = nx.degree_centrality(Graph1)
total_centrality = sum(degree_centrality.values())
print("Degree Centrality:")
degree_centrality_list={}
for node, dc in degree_centrality.items():
    degree_centrality_list[node] = dc

# print(degree_centrality_list) 
# print("Total Centrality:", total_centrality)
   
avg_centralitty_array = {}
for node, centrality in degree_centrality.items():
    avg_centralitty_array[node] = centrality / total_centrality
    
print("AVG Degree Centrality")
# print(avg_centralitty_array)

# Calculate betweenness centrality
betweenness_centrality = nx.betweenness_centrality(Graph1)
total_contribution = {}
for user in Graph1.nodes():
    contribution = betweenness_centrality[user]
    for source, target in Graph1.edges():
        if source == user or target == user:
            contribution += betweenness_centrality[source] + betweenness_centrality[target] 
          
    total_contribution[user] = contribution

# Print total contribution for each user
print("Total Contribution")
# print(total_contributio)


#Now find the social score 
social_scores = {}
for user in Graph1.nodes():
    contribution = total_contribution[user]
    # response = response_scores[user]
    degree = degree_centrality[user]
    avgCentralitty_array = avg_centralitty_array[user]
    social_score = contribution/ (avgCentralitty_array*(in_degrees[node] + out_degrees[node]))
    social_scores[user] = social_score

# Print social score for each user
print("Social Scores")
# print(social_scores)

total_social_score = sum(social_scores.values())
# print(total_social_score)

avg_social_score = {}
for node, social_score in social_scores.items():
    avg_social_score[node] = (social_score / total_social_score)*100
    
print("AVG Social/ Centrality")
print(avg_social_score)


neighbors_list = {}
# Loop through each node in the graph
for node in Graph1.nodes():
    neighbors = list(Graph1.neighbors(node))

    neighbors_list[node] = neighbors

print("Neighbors:")
print(neighbors_list)



degree_between_neighbors = {}
for node, neighbors in Graph1.adjacency():
    for neighbor in neighbors:

      

        # get the in-degree and out-degree of the neighbor
        in_degree = matrix[node][neighbor]
        out_degree = matrix[neighbor][node]

        
        degree_between_neighbors[(node, neighbor)] = [in_degree,out_degree]

# print the degree_between_neighbors dictionary
print("degree_between_neighbors")
print(degree_between_neighbors)



response_score_between_two_node={}
for node, neighbors in neighbors_list.items():
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            
            in_degree = matrix[node][neighbor]
            out_degree = matrix[neighbor][node]
            if out_degree == 0:
                response_score_between_two_node[(node, neighbor)] = [0] # or any other value that makes sense for your use case
            else:
                response_score_between_two_node[(node, neighbor)] = [in_degree/out_degree]

  
print("response score between 2 node:")
print(response_score_between_two_node)

frequency_between_two_node={}
for node, neighbors in neighbors_list.items():
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            in_degree = matrix[node][neighbor]
            out_degree = matrix[neighbor][node]
            
            frequency_between_two_node[(node, neighbor)] = [in_degree+out_degree]

print("Frequency between 2 node:")
print(frequency_between_two_node)



Personal_score_list = {}
for node, neighbors in neighbors_list.items():
    new_neighbors = []
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            freq = frequency_between_two_node[(node, neighbor)][0]
            score = response_score_between_two_node[(node, neighbor)][0]
            neighbor_social_score = social_scores[neighbor]
            new_value = freq + score + neighbor_social_score
            new_neighbors.append((neighbor, new_value))
    Personal_score_list[node] = new_neighbors
print("Personal rank")
print(Personal_score_list)





#-----------------Sorting 
sorted_list = {}
for node, neighbors in neighbors_list.items():
    new_neighbors = []
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            freq = frequency_between_two_node[(node, neighbor)][0]
            score = response_score_between_two_node[(node, neighbor)][0]
            neighbor_social_score = social_scores[neighbor]
            new_value = freq + score + neighbor_social_score
            new_neighbors.append((neighbor, new_value))
    new_neighbors = sorted(new_neighbors, key=lambda x: x[1], reverse=True) # sort neighbors by score
    # top_neighbors = [neighbor[0] for neighbor in new_neighbors[:3]] # get top 3 neighbors
    sorted_list[node] = [neighbor[0] for neighbor in new_neighbors[:3]]

# print("Top 3 neighbors with highest score:")
# print(sorted_list)

print("Top  neighbors with highest score:")
for node, neighbors in sorted_list.items():
    print(f"User {node}: {neighbors}")

