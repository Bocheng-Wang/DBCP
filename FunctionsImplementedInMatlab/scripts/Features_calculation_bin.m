function [   strength, ...
             clustering_coef, ...
             local_efficiency, ...
             betweenness, ...
             eigenvector, ...
             subgraph, ...
             pagerank, ...
             ...
             global_efficiency, ...
             maximized_modularity, ...
             assortativity, ...
             optimal_number_of_modules, ...
             small_wordness_index, ...
             characteristic_path_length, ...
             mean_clustering_coefficient, ...
             kcoreness, ...
             flow_coefficiency ...
] = Features_calculation_bin(network)
%% 2019.1, Bocheng Wang

%% 2019.09.28 Bocheng Wang  See BCT weight_conversion.m 
%  some distance based measures shoule be computed by length
network_distance_based_measure = weight_conversion(network, 'lengths');
%% local metrics 360 x 360 
strength = (strengths_und(network));
clustering_coef = clustering_coef_bu(network)';
local_efficiency = (efficiency_bin(network, 1)');
betweenness = (betweenness_bin(network_distance_based_measure));
eigenvector = (eigenvector_centrality_und(network)');
subgraph = ((subgraph_centrality(network)'));
kcoreness = (kcoreness_centrality_bu(network));
flow_coefficiency = (flow_coef_bd(network));
pagerank = (pagerank_centrality(network, 0.85)');

%% global metrics 1 x 1
number_of_all_possible_edges = 360 * 359 / 2; %上三角形，不包含对角线
number_of_random_network = 100;

global_efficiency = efficiency_bin(network, 0) * number_of_all_possible_edges / sum(sum(network));
mean_clustering_coefficient = mean(clustering_coef');
characteristic_path_length = charpath(network);

%% small_worldness_index
small_wordness_array = zeros(1, number_of_random_network);
for i = 1:number_of_random_network
    % generated random network
    edge = randi(number_of_all_possible_edges);
    random_network = makerandCIJ_und(360, edge);
    
    gam_rand = mean(clustering_coef_bu(random_network));
    lam_rand = charpath(random_network);
    
    % normalization according to Eq.(9) and (10) in paper :
    % Cheng H, Wang Y, Sheng J, et al. Characteristics and 
    % variability of structural networks derived from diffusion 
    % tensor imaging[J]. Neuroimage, 2012, 61(4): 1153-1164.
    characteristic_path_length_normalized = characteristic_path_length * sum(sum(network)) / number_of_all_possible_edges;
    mean_clustering_coef_normalized = mean_clustering_coefficient * number_of_all_possible_edges / sum(sum(network));
    lam_rand_normalized = lam_rand * sum(sum(random_network)) / number_of_all_possible_edges;
    gam_rand_normalized = gam_rand * number_of_all_possible_edges / sum(sum(random_network));
    
    small_wordness_array(1, i) = (mean_clustering_coef_normalized/gam_rand_normalized)/(characteristic_path_length_normalized/lam_rand_normalized);
end
small_wordness_index = mean(small_wordness_array(isfinite(small_wordness_array)));

%% assortativity
assortativity = assortativity_bin(network, 0);

%% optimal_number_of_modules and visualization
[Ci, maximized_modularity] = modularity_und(network, 1);
[Hpos,Hneg] = diversity_coef_sign(network, Ci);

optimal_number_of_modules = max(Ci);

% [C,Q] = modularity_und(network);     % get community assignments
% [X,Y,INDSORT] = grid_communities(C); % call function
% imagesc(network(INDSORT,INDSORT));           % plot ordered adjacency matrix
% hold on;                                 % hold on to overlay community visualization
% plot(X,Y,'r','linewidth',2);             % plot community boundaries


