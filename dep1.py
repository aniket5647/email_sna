import networkx as nx
import matplotlib.pyplot as plt

with open('./dep1.csv', 'r') as f:
    data_file = f.readlines()

# Create graph object
Graph1 = nx.Graph()

# Add nodes and edges to graph
for line in data_file:
    source, dest, time = line.strip().split(' ')
    Graph1.add_edge(source, dest, weight=time)


#----------------------------------------------------------------------- Draw the graph
nx.draw(Graph1)
plt.title("Department-1 Visualization")
# plt.bar_label("Department-1 Visualization")
plt.show()


# ------------------------------------------------------------------------degree each user 
degree_dict = dict(Graph1.degree())
email_counts = {}
for node, degree in degree_dict.items():
    email_counts[node] = degree
print(email_counts)








# # ------------------------------------------------------------------calculate in-degree and out-degree of nodes
# in_degree_dict = dict(Graph1.in_degree())
# out_degree_dict = dict(Graph1.out_degree())

# # print the in-degree and out-degree of each node
# for node in Graph1.nodes():
#     print(f"Node {node} has in-degree {in_degree_dict[node]} and out-degree {out_degree_dict[node]}")












# ------------------------------------------------------------------------------Calculate degree centrality
degree_centrality = nx.degree_centrality(Graph1)
total_centrality = sum(degree_centrality.values())
centralitty__array={}
# Print degree centrality of each node
for node, centrality in degree_centrality.items():
    centralitty__array[node]= centrality
    # print(f"Node {node} has degree centrality {centrality}")
print("Degree Centrality")
print(centralitty__array)

print("Total Centrality:", total_centrality)

#avg each user centrality
avg_centralitty_array = {}
for node, centrality in degree_centrality.items():
    avg_centralitty_array[node] = centrality / total_centrality
    
print("AVG Degree Centrality")
print(avg_centralitty_array)






#--------------------------------------------------------------------------- find response score
# response_scores = {}
# for user in Graph1.nodes():
#     sent = 0
#     responded = 0
#     for source, target in Graph1.edges():
#         if source == user:
#             sent += 1
#             if (target, source) in Graph1.edges():
#                 responded += 1
#         elif target == user:
#             if (source, target) in Graph1.edges():
#                 sent += 1
#                 responded += 1
#     response_scores[user] = responded / sent if sent > 0 else 0

# # Print response score for each user
# print("Response Scores")
# print(response_scores)










# ------------------------------------------------------------------------find total contribution
# Calculate betweenness centrality
betweenness_centrality = nx.betweenness_centrality(Graph1)


#--------------------------------------------------------------------- Calculate total contribution for each user
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
print(total_contribution)












#Now find the social score 
degree_centrality_weight = 0.5

#---------------------------------------------------------------------- Calculate social score for each user
social_scores = {}
for user in Graph1.nodes():
    contribution = total_contribution[user]
    response = response_scores[user]
    degree = degree_centrality[user]
    avgCentralitty_array = avg_centralitty_array[user]
    social_score = contribution / (response + avgCentralitty_array*degree)
    social_scores[user] = social_score

# Print social score for each user
# print("Social Scores")
# print(social_scores)

sorted_social_scores = sorted(social_scores.items(), key=lambda x: x[1],reverse=True)

# Print sorted social scores
print("Social Scores (sorted in ascending order):")
# for user, score in sorted_social_scores:
#     print(user, score)

# Print top 10 users with highest social scores
print("Top 10 Users by Social Score:")
for user, score in sorted_social_scores[:10]:
    print(user, score)
    
    
    
    
    
    
    
    
    
# ---------------------------------------------------------------------------Create dictionary of users with the same social score
users_by_social_score = {}
for user, score in social_scores.items():
    if score in users_by_social_score:
        users_by_social_score[score].append(user)
    else:
        users_by_social_score[score] = [user]

# # Print users with the same social score
# for score, users in users_by_social_score.items():
#     if len(users) > 1:
#         print(f"Users with social score {score}: {users}")


# Sort users_by_social_score by social score in descending order
sorted_users_by_social_score = {k: v for k, v in sorted(users_by_social_score.items(), key=lambda item: item[0], reverse=True)}

# Print users with the same social score in descending order
for score, users in sorted_users_by_social_score.items():
    if len(users) > 1:
        # print(f"Users with social score {score} in descending order:")
        print(f"Users with similar social score {score}:")
        for user in sorted(users):
            print(user)








# # Calculate shortest paths between all pairs of nodes
# shortest_paths = dict(nx.shortest_path_length(Graph1, weight='time'))

# # Calculate response score for each node
# response_scores = {}
# for node in Graph1.nodes():
#     total_response_time = 0
#     num_responses = 0
#     for other_node in Graph1.nodes():
#         if node != other_node:
#             if other_node in shortest_paths[node]:
#                 shortest_path_length = shortest_paths[node][other_node]
#                 if shortest_path_length > 0:
#                     # Find the timestamp for the last message from other_node to node
#                     last_message_time = None
#                     for line in data_file:
#                         source, dest, time = line.strip().split(' ')
#                         if source == other_node and dest == node:
#                             if last_message_time is None or time > last_message_time:
#                                 last_message_time = time

#                     if last_message_time is not None:
#                         total_response_time += int(last_message_time) - int(data_file[0].strip().split(' ')[2])
#                         num_responses += 1

#     if num_responses > 0:
#         response_scores[node] = total_response_time / num_responses

# # Print response score for each node
# print("Response Scores")
# print(response_scores)


