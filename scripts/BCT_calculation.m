function [           global_efficiency_wei, ...
    maximized_modularity_wei, ...
    assortativity_wei, ...
    optimal_number_of_modules_wei, ...
    small_wordness_index_wei, ...
    characteristic_path_length_wei, ...
    mean_clustering_coefficient_wei,  ...
    ...
    global_efficiency_bin, ...
    maximized_modularity_bin, ...
    assortativity_bin, ...
    optimal_number_of_modules_bin, ...
    small_wordness_index_bin, ...
    characteristic_path_length_bin, ...
    mean_clustering_coefficient_bin, ...
    ...
    strength_wei, ...
    clustering_coef_wei, ...
    local_efficiency_wei, ...
    betweenness_wei, ...
    eigenvector_wei, ...
    pagerank_wei, ...
    degree_wei, ...
    ...
    strength_bin, ...
    clustering_coef_bin, ...
    local_efficiency_bin, ...
    betweenness_bin, ...
    eigenvector_bin, ...
    subgraph_bin, ...
    pagerank_bin, ...
    kcoreness_bin, ...
    flow_coefficiency, ...
    PSW_optimal_wei, ...
    PSW_optimal_bin ...
    ] = BCT_calculation(data)
%% 利用BCT工具箱，计算网络拓扑值
%
%   Data 是相关矩阵
%   HDU, Bocheng Wang 2018.10

%% Search for maximum GCE with the optimal threshold value in weighted network
GCE_max = 0;
PSW_optimal = 0;
GCEs = zeros(100, 1);
data_fixed = weight_conversion(data, 'autofix'); % Bocheng Wang, 2019.09.28 remove all Inf and NaN values
for index = 1:80
    PSW = index/100;
    w = threshold_proportional(data_fixed, PSW);
    w_normalized = weight_conversion(w, 'normalize'); % Bocheng Wang, 2019.09.28 rescale matrix to [0, 1]
    GCE = efficiency_wei(w_normalized, 0) - PSW;
    GCEs(index) = GCE;
    if GCE > GCE_max
        GCE_max = GCE;
        PSW_optimal = PSW;
    end
end
%% 阈值处理
PSW_optimal_wei = PSW_optimal;
data_threshed = threshold_proportional(data_fixed, PSW_optimal);
%% weighted network
data_threshed_normalized = weight_conversion(data_threshed, 'normalize'); % Bocheng Wang, 2019.09.28 rescale matrix to [0, 1]
weighted_network = data_threshed_normalized;
% 计算特性
[    strength_wei, ...
    clustering_coef_wei, ...
    local_efficiency_wei, ...
    betweenness_wei, ...
    eigenvector_wei, ...
    pagerank_wei, ...
    degree_wei, ...
    global_efficiency_wei, ...
    maximized_modularity_wei, ...
    assortativity_wei, ...
    optimal_number_of_modules_wei, ...
    small_wordness_index_wei, ...
    characteristic_path_length_wei, ...
    mean_clustering_coefficient_wei ...
    ] = Features_calculation_wei(weighted_network);

%% Search for maximum GCE with the optimal threshold value in binarized network
GCE_max = 0;
PSW_optimal = 0;
GCEs = zeros(100, 1);
for index = 1:100
    PSW = index/100;
    w = threshold_proportional(data_fixed, PSW);
    w = weight_conversion(w, 'binarize');
    GCE = efficiency_bin(w, 0) - PSW;
    GCEs(index) = GCE;
    if GCE > GCE_max
        GCE_max = GCE;
        PSW_optimal = PSW;
    end
end
%% 阈值处理
PSW_optimal_bin = PSW_optimal;
data_threshed = threshold_proportional(data_fixed, PSW_optimal);
%% binary network
binarized_network = weight_conversion(data_threshed, 'binarize');
% 计算特性
[    strength_bin, ...
    clustering_coef_bin, ...
    local_efficiency_bin, ...
    betweenness_bin, ...
    eigenvector_bin, ...
    subgraph_bin, ...
    pagerank_bin, ...
    global_efficiency_bin, ...
    maximized_modularity_bin, ...
    assortativity_bin, ...
    optimal_number_of_modules_bin, ...
    small_wordness_index_bin, ...
    characteristic_path_length_bin, ...
    mean_clustering_coefficient_bin, ...
    kcoreness_bin, ...
    flow_coefficiency ...
    ] = Features_calculation_bin(binarized_network);


