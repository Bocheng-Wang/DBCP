function Abnormal_check_in_boxplot()
%% Written by Bocheng Wang, 2020.06.11
% Recently, I realize there exist too much abnormal values in BCTs.
% Especially with the help of BoxPlot, outliers above or below the box are
% very obvious. So these values have to be removed or replaced by the mean
% value between windowed connectivity in dynamic fMRI analyze.

% Important! parameters set here are only suit for eight static or dynamic.
% They are different... For static BCTs, each subject occupy only one
% averaged connectivity related BCTs. The total number of rows is 160
% (ADNI2). While for dynamic, it should be multipled with window numbers,
% such as 125.

%% Initialize 
clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

% By default, dynamic_windows_number = 125; 
dynamic_windows_number = 125; 

start_line = 1; % with one head row, start from Row #2
end_line = 20001; % only for dynamic connectivity

classes = {'0.Normal';'2.EMCI';'4.LMCI';'5.AD';};


Excel_base_dir = ['.\data\0.OriginalBCTs\1.dynamic_BCTs\Excels\'];
Excel_output_dir = ['.\data\1.AnalysedBCTs_without_abnormal\1.dynamic_BCTs\Excels\'];

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

'For dynamic BCTs:  '

input_file = PSW_weight_file;
output_file ='Weighted\7.PSW_optimal_wei.xlsx'  ;

%% For BCT measures
[~,~,BCTs] = xlsread(input_file);
for column_index = 4:size(BCTs, 2)
    column_index
    Normal = cell2mat(BCTs(2:5376, column_index));
    EMCI = cell2mat(BCTs(5377:12001, column_index));
    LMCI = cell2mat(BCTs(12002:16251, column_index));
    AD = cell2mat(BCTs(16252:20001, column_index));
    
    %% For Normal
    IQR_range = prctile(Normal, [25, 75]);
    Q1_value = IQR_range(1, 1);
    Q3_value = IQR_range(1, 2);
    IQR = Q3_value - Q1_value;
    Maximum = Q3_value + 1.5 * IQR;
    Minimum  = Q1_value - 1.5 * IQR;

    Index = find(Normal > Maximum | Normal < Minimum);
    Normal(Normal > Maximum | Normal < Minimum) = median(Normal);

    %% For EMCI
    IQR_range = prctile(EMCI, [25, 75]);
    Q1_value = IQR_range(1, 1);
    Q3_value = IQR_range(1, 2);
    IQR = Q3_value - Q1_value;
    Maximum = Q3_value + 1.5 * IQR;
    Minimum  = Q1_value - 1.5 * IQR;
    EMCI(EMCI > Maximum | EMCI < Minimum) = median(EMCI);
    
    %% For LMCI
    IQR_range = prctile(LMCI, [25, 75]);
    Q1_value = IQR_range(1, 1);
    Q3_value = IQR_range(1, 2);
    IQR = Q3_value - Q1_value;
    Maximum = Q3_value + 1.5 * IQR;
    Minimum  = Q1_value - 1.5 * IQR;
    LMCI(LMCI > Maximum | LMCI < Minimum) = median(LMCI);
    
    %% For AD
    IQR_range = prctile(AD, [25, 75]);
    Q1_value = IQR_range(1, 1);
    Q3_value = IQR_range(1, 2);
    IQR = Q3_value - Q1_value;
    Maximum = Q3_value + 1.5 * IQR;
    Minimum  = Q1_value - 1.5 * IQR;
    AD(AD > Maximum | AD < Minimum) = median(AD);
    
    new = [Normal; EMCI; LMCI; AD];
    BCTs(2:size(BCTs, 1), column_index) = num2cell(new);
end

%% change group string to group index
GroupIndexes =zeros(end_line - 1, 1);
for i = 2:end_line
    groupname = cell2mat(BCTs(i, 1));
    GroupIndex = strsplit(groupname, '.');
    GroupIndexes(i - 1) = str2double(GroupIndex(1));
end
GroupIndexes = [{'GroupIndex'}; num2cell(GroupIndexes)];
result =  [GroupIndexes, BCTs];

%% Save results. For Global, the end column is R, for reginal BCTs, the end column is MZ
xlswrite([Excel_output_dir  output_file], result, 1, ['A' num2str(start_line) ': MZ' num2str(end_line)]);

    

  

    
