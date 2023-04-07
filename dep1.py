import networkx as nx
import matplotlib.pyplot as plt

with open('./dep1.csv', 'r') as f:
    data_file = f.readlines()

# Create graph object
Graph1 = nx.DiGraph()

# Add nodes and edges to graph
for line in data_file:
    source, dest, time = line.strip().split(' ')
    Graph1.add_edge(source, dest, weight=float(time))

nx.draw(Graph1)
plt.title("Department-1 Visualization")
# plt.bar_label("Department-1 Visualization")
plt.show()

in_degrees = dict(Graph1.in_degree())
out_degrees = dict(Graph1.out_degree())

in__degrees_list = {}
for node in Graph1.nodes():
    in__degrees_list[node] = in_degrees[node]
print(in__degrees_list)
out__degrees_list = {}
for node in Graph1.nodes():
    out__degrees_list[node] = out_degrees[node]
print(out__degrees_list)




degree_centrality = nx.degree_centrality(Graph1)
total_centrality = sum(degree_centrality.values())
print("Degree Centrality:")
degree_centrality_list={}
for node, dc in degree_centrality.items():
    degree_centrality_list[node] = dc

print(degree_centrality_list) 
print("Total Centrality:", total_centrality)
   
avg_centralitty_array = {}
for node, centrality in degree_centrality.items():
    avg_centralitty_array[node] = centrality / total_centrality
    
print("AVG Degree Centrality")
print(avg_centralitty_array)



# Calculate response time
# response_time = {}
# for node in Graph1.nodes():
#     distances, paths = nx.single_source_dijkstra(Graph1, node)
#     response_time[node] = sum(distances.values())
# print("Response Time")
# print(response_time)

response_score = {}
for node in Graph1.nodes():
    distances, paths = nx.single_source_dijkstra(Graph1, node)
    response_sum = sum(distances.values())
    response_score[node] = 1 / (1 + response_sum)
print("Response Score")
print(response_score)




social_score = {}
for node in Graph1.nodes():
    social_score[node] = (in_degrees[node] + out_degrees[node]) * avg_centralitty_array[node] * response_score[node]
    # # contribution = total_contribution[user]
    # response = response_time[node]
    # # degree = degree_centrality[user]
    # indeg= in__degrees_list[node]
    # outdeg= out__degrees_list[node]
    # avgCentralitty_array = avg_centralitty_array[node]
    # social_score =   (response + avgCentralitty_array*(indeg+outdeg))
    # social_score[node] = social_score
    
# Print social score for each node
print("Social Score:")
print(social_score)

top_3_users = {}
for node in Graph1.nodes():
    # Get the neighbors of the node
    neighbors = list(Graph1.neighbors(node))
    
    # Sort the neighbors based on their social score
    sorted_neighbors = sorted(neighbors, key=lambda x: social_score[x], reverse=True)
    
    # Get the top 3 neighbors
    top_3 = sorted_neighbors[:3]
    
    # Add the top 3 neighbors to the dictionary
    top_3_users[node] = top_3
    
# Print the top 3 important users for each user
print("Top 3 Important Users:")
for node, top_3 in top_3_users.items():
    print(node, ":", top_3)
