import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
with open('./dep1.csv', 'r') as f:
    data_file = f.readlines()

# Create graph object
Graph1 = nx.DiGraph()

# Add nodes and edges to graph
for line in data_file:
    source, dest, time = line.strip().split(' ')
    Graph1.add_edge(int(source), int(dest), weight=float(time))
    
node_list = sorted(Graph1.nodes())
adj_matrix = np.zeros((len(node_list), len(node_list)))

for source, dest, weight in Graph1.edges.data('weight'):
    adj_matrix[node_list.index(source), node_list.index(dest)] = weight

# Print adjacency matrix
print(adj_matrix)

# nx.draw(Graph1, with_labels=True, font_size=5)
# plt.title("Department-1 Visualization")
# # plt.bar_label("Department-1 Visualization")
# plt.show()
# Define node colors
#'5': ['2', '13', '19', '27', '29', '209', '226'], 
node_color = ['blue' if node != '172' else 'red' for node in Graph1.nodes()]
# Draw graph
pos = nx.spring_layout(Graph1)  # Compute layout
nx.draw_networkx_nodes(Graph1, pos, node_color=node_color)
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
            # contribution += betweenness_centrality[source] + email_counts[source] 
    total_contribution[user] = contribution

# Print total contribution for each user
print("Total Contribution")
# print(total_contributio
#Now find the social score 
degree_centrality_weight = 0.5
social_scores = {}
for user in Graph1.nodes():
    contribution = total_contribution[user]
    # response = response_scores[user]
    degree = degree_centrality[user]
    avgCentralitty_array = avg_centralitty_array[user]
    social_score = contribution / (avgCentralitty_array*(in_degrees[node] + out_degrees[node]))
    social_scores[user] = social_score
    # social_score[node] = (in_degrees[node] + out_degrees[node]) * avg_centralitty_array[node] * response_score[node]
    

# Print social score for each user
print("Social Scores")
# print(social_scores)

total_social_score = sum(social_scores.values())
# print(total_social_score)

avg_social_score = {}
for node, social_score in social_scores.items():
    avg_social_score[node] = (social_score / total_social_score)*100
    
print("AVG Social/ Centrality")
# print(avg_social_score)

neighbors_list = {}

# Loop through each node in the graph
for node in Graph1.nodes():
    neighbors = list(Graph1.neighbors(node))

    neighbors_list[node] = neighbors

print("Neighbors:")
print(neighbors_list)



# degree_between_neighbors = {}
# for node, neighbors in Graph1.adjacency():
#     for neighbor in neighbors:

#         # get the degree of the node and neighbor
#         node_degree = Graph1.degree(node)
#         neighbor_degree = Graph1.degree(neighbor)

#         # get the in-degree and out-degree of the neighbor
#         in_degree = Graph1.in_degree(neighbor)
#         out_degree = Graph1.out_degree(neighbor)

#         # add the node, neighbor, node degree, neighbor degree, in-degree, and out-degree to the dictionary
#         degree_between_neighbors[(node, neighbor)] = [node_degree, neighbor_degree, in_degree, out_degree]

# # print the degree_between_neighbors dictionary
# print("degree_between_neighbors")
# print(degree_between_neighbors)
degree_dict = {}

# Loop over each node in the graph
for node in Graph1.nodes():
    # Initialize the in-degree and out-degree of the node to zero
    in_degree = 0
    out_degree = 0
    # Loop over each neighbor of the node
    for neighbor in Graph1.neighbors(node):
        # If the neighbor has an edge pointing to the node, increment the in-degree of the node
        if Graph1.has_edge(neighbor, node):
            in_degree += 1
        # If the node has an edge pointing to the neighbor, increment the out-degree of the node
        if Graph1.has_edge(node, neighbor):
            out_degree += 1
    # Store the in-degree and out-degree of the node in the degree_dict
    degree_dict[node] = {'in_degree': in_degree, 'out_degree': out_degree}

# Print the in-degree and out-degree of each node
for node, degree in degree_dict.items():
    print(f"Node {node}: In-degree={degree['in_degree']}, Out-degree={degree['out_degree']}")
    
frequency_between_two_node={}
for node, neighbors in neighbors_list.items():
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            in_degree = Graph1.in_degree(neighbor)
            out_degree = Graph1.out_degree(neighbor)
            
            frequency_between_two_node[(node, neighbor)] = [in_degree+out_degree]

print("Frequency between 2 node:")
# print(frequency_between_two_node)



response_score_between_two_node={}
for node, neighbors in neighbors_list.items():
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            
            in_degree = Graph1.in_degree(neighbor)
            out_degree = Graph1.out_degree(neighbor)
            if out_degree == 0:
                response_score_between_two_node[(node, neighbor)] = [0] # or any other value that makes sense for your use case
            else:
                response_score_between_two_node[(node, neighbor)] = [in_degree/out_degree]

  


print("Frequency between 2 node:")
# print(response_score_between_two_node)



new_neighbors_list = {}
for node, neighbors in neighbors_list.items():
    new_neighbors = []
    for neighbor in neighbors:
        if Graph1.has_edge(node, neighbor):
            freq = frequency_between_two_node[(node, neighbor)][0]
            score = response_score_between_two_node[(node, neighbor)][0]
            neighbor_social_score = social_scores[neighbor]
            new_value = freq + score + neighbor_social_score
            new_neighbors.append((neighbor, new_value))
    new_neighbors_list[node] = new_neighbors
print("Personal rank")
# print(new_neighbors_list)





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

