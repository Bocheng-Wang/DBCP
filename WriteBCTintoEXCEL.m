function WriteBCTintoEXCEL()
%% Written by Bocheng Wang, 2020.06.08
% Write subject`s BCTs of dynamic windows into EXCEL files.


%% Initialize 
clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

% By default, dynamic_windows_number = 125; 
dynamic_windows_number = 125; 

classes = {'0.Normal';'2.EMCI';'4.LMCI';'5.AD';};
start_line = 2; % with one head row, start from Row #2

Excel_base_dir = ['.\data\0.static_BCTs\Excels\'];
Strength_Wei_file = [Excel_base_dir 'Weighted\0.strength_wei.xlsx' ];
clustering_coef_wei_file = [Excel_base_dir 'Weighted\1.clustering_coef_wei.xlsx' ];
local_efficiency_wei_file = [Excel_base_dir 'Weighted\2.local_efficiency_wei.xlsx' ];
betweenness_wei_file = [Excel_base_dir 'Weighted\3.betweenness_wei.xlsx' ];
eigenvector_wei_file = [Excel_base_dir 'Weighted\4.eigenvector_wei.xlsx' ];
pagerank_wei_file = [Excel_base_dir 'Weighted\5.pagerank_wei.xlsx' ];
degree_wei_file = [Excel_base_dir 'Weighted\6.degree_wei.xlsx' ];
PSW_weight_file = [Excel_base_dir 'Weighted\7.PSW_optimal_wei.xlsx' ];

Global_file = [Excel_base_dir 'Global.xlsx' ];
strength_bin_file = [Excel_base_dir 'Binary\0.strength_bin.xlsx' ];
clustering_coef_bin_file =  [Excel_base_dir 'Binary\1.clustering_coef_bin.xlsx' ];
local_efficiency_bin_file =  [Excel_base_dir 'Binary\2.local_efficiency_bin.xlsx' ];
betweenness_bin_file =  [Excel_base_dir 'Binary\3.betweenness_bin.xlsx' ];
eigenvector_bin_file =  [Excel_base_dir 'Binary\4.eigenvector_bin.xlsx' ];
pagerank_bin_file =  [Excel_base_dir 'Binary\5.pagerank_bin.xlsx' ];
kcoreness_bin_file =  [Excel_base_dir 'Binary\6.kcoreness_bin.xlsx' ];
flow_coefficiency_file =  [Excel_base_dir 'Binary\7.flow_coefficiency.xlsx' ];        
PSW_binary_file =  [Excel_base_dir 'Binary\8.PSW_optimal_bin.xlsx' ];

for index = 1:size(classes)
    group = char(classes(index, 1));
    base_path = ['.\data\0.static_BCTs\'  group '\'];
    subjectFolder = dir([base_path, '\*.mat']);
    
    for subject_index = 1:size(subjectFolder, 1)
        tic;
        subject_ID = subjectFolder(subject_index).name;
        BCTs =  importdata(subject_ID);
        subject_ID = strsplit(subject_ID, {'-', '.mat'});
        subject_ID = char(subject_ID(2));
        dynamic_windows_number =size(BCTs, 1);
        
        Global_Value = BCTs(:, 1:14);
        
        Strength_Wei_Value = BCTs(:, 15:374);
        clustering_coef_wei_Value = BCTs(:, 375:734);
        local_efficiency_wei_Value = BCTs(:, 735:1094);
        betweenness_wei_Value = BCTs(:, 1095:1454);
        eigenvector_wei_Value = BCTs(:, 1455:1814);
        pagerank_wei_Value = BCTs(:, 1815:2174);
        degree_wei_Value = BCTs(:, 2175:2534);
        
        strength_bin_Value = BCTs(:, 2535:2894);
        clustering_coef_bin_Value = BCTs(:, 2895:3254);
        local_efficiency_bin_Value = BCTs(:, 3255:3614);
        betweenness_bin_Value = BCTs(:, 3615:3974);
        eigenvector_bin_Value = BCTs(:, 3975:4334);
        pagerank_bin_Value = BCTs(:, 4335:4694);
        kcoreness_bin_Value = BCTs(:, 4695:5054);
        flow_coefficiency_Value = BCTs(:, 5055:5414);
        PSW_weight_Value = BCTs(:, 5415);
        PSW_binary_Value = BCTs(:, 5416);
              
        end_line = start_line + dynamic_windows_number - 1;
        
        %% Write Global
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(Global_Value)];
        xlswrite(Global_file, write_cell, 1, ['A' num2str(start_line) ': Q' num2str(end_line)]);
        
       %% Write Strength Weighted
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(Strength_Wei_Value)];
        xlswrite(Strength_Wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write clustering_coef_wei
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(clustering_coef_wei_Value)];
        xlswrite(clustering_coef_wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  local_efficiency_wei
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(local_efficiency_wei_Value)];
        xlswrite(local_efficiency_wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  betweenness_wei
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(betweenness_wei_Value)];
        xlswrite(betweenness_wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  eigenvector_wei
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(eigenvector_wei_Value)];
        xlswrite(eigenvector_wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  pagerank_wei
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(pagerank_wei_Value)];
        xlswrite(pagerank_wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  degree_wei
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(degree_wei_Value)];
        xlswrite(degree_wei_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  PSW_weight
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(PSW_weight_Value)];
        xlswrite(PSW_weight_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  strength_bin_file
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(strength_bin_Value)];
        xlswrite(strength_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  clustering_coef_bin
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(clustering_coef_bin_Value)];
        xlswrite(clustering_coef_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  local_efficiency_bin
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(local_efficiency_bin_Value)];
        xlswrite(local_efficiency_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  betweenness_bin
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(betweenness_bin_Value)];
        xlswrite(betweenness_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  eigenvector_bin
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(eigenvector_bin_Value)];
        xlswrite(eigenvector_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  pagerank_bin
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(pagerank_bin_Value)];
        xlswrite(pagerank_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  kcoreness_bin
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(kcoreness_bin_Value)];
        xlswrite(kcoreness_bin_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  flow_coefficiency
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(flow_coefficiency_Value)];
        xlswrite(flow_coefficiency_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        %% Write  PSW_binary
        write_cell = {};
        write_cell = [write_cell, repelem(classes(index, 1), dynamic_windows_number)'];
        write_cell = [write_cell, repelem({subject_ID}, dynamic_windows_number)'];
        write_cell = [write_cell, num2cell([1:dynamic_windows_number]')];
        write_cell = [write_cell, num2cell(PSW_binary_Value)];
        xlswrite(PSW_binary_file, write_cell, 1, ['A' num2str(start_line) ': MY' num2str(end_line)]);
        
        start_line = end_line + 1;
    end
end