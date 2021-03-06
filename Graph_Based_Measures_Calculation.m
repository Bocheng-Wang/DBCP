function Graph_Based_Measures_Calculation()
%% Written by Bocheng Wang, 2020.06.02
% In ADNI2, fMRI contains 140 volumes with TR = 3s. By default, we set the
% width of dynamic window to be 15, thus totally 125 windowed segmentations
% generated. When calling this function, dynamic windows number should be
% given first.


%% Initialize 
clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

% By default, dynamic_windows_number = 125; 
dynamic_windows_number = 125; 

%% Read out the parcellated and windowed connectivities for each subject in folder 'data/output/'
classes = {'0.Normal';'2.EMCI';'4.LMCI';'5.AD';};
for index = 1:size(classes)
    base_path = ['.\data\output\'  char(classes(index, 1)) '\'];
    subjectFolder = dir(base_path);
    for folder_index = 3:size(subjectFolder, 1)
        tic;
        subject_ID = subjectFolder(folder_index).name;
        connectivity_files =dir([base_path, subject_ID '\*.mat']);
        connectivity_files_sorted = sort_nat({connectivity_files.name})';
        BCT_measures_for_each_subject_in_windows = zeros(dynamic_windows_number, 5416);
        for file_index = 1:size(connectivity_files_sorted, 1)
                connectivity_file = connectivity_files_sorted(file_index);
                connectivity_file = connectivity_file{:};
                connectivity_file = [base_path, subject_ID, '\',connectivity_file];
                connectivity = importdata(connectivity_file);
                %% Calculate the graph based measures in connectivity
                [   global_efficiency_wei, ...
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
                            ...
                            PSW_optimal_wei, ...
                            PSW_optimal_bin ...
                            ] = BCT_calculation(connectivity);
                        %% feature structure�� 7 weighted global metrics + 7 binary global metrics + 7 * 360 weighted local metrics + 8 * 360 binary local metrics
                        %    feature size: 1x5416
                        features = [     global_efficiency_wei, ...
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
                            pagerank_bin, ...
                            kcoreness_bin, ...
                            flow_coefficiency, ...
                            ...
                            PSW_optimal_wei, ...
                            PSW_optimal_bin ...
                            ];
                        BCT_measures_for_each_subject_in_windows(file_index, :) = features;
                        [subject_ID '.session.' num2str(file_index) '--finished BCT calculation']
                        toc;
        end
        %% Save BCTs for each subject with windowed connectivity
        folder = ['.\data\output\BCTs\', char(classes(index)), '\'];
                        if(~exist(folder, 'dir'))
                            mkdir(folder);
                        end
        save([folder subject_ID, '.mat'], 'BCT_measures_for_each_subject_in_windows');
    end
end

