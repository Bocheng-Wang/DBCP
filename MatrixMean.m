function MatrixMean
%% Written by Bocheng Wang 2020.06.01
%% timer on ³ÌÐò¿ªÊ¼
tic;
%% Initialize 
clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

%% Read out the parcellated time series in 360 regions of HCP MMP
classes = {'0.Normal';'2.EMCI';'4.LMCI';'5.AD';};
for index = 1:size(classes)
    base_path = ['.\data\output\'  char(classes(index, 1)) '\'];
    subjectFolder = dir(base_path);
    for folder_index = 3:size(subjectFolder, 1)
        if (subjectFolder(folder_index).isdir == 1) && (~strcmp(subjectFolder(folder_index).name, '.') && ~strcmp(subjectFolder(folder_index).name, '..'))
            subject_ID = subjectFolder(folder_index).name;
            connectivity_files =dir([base_path, subject_ID '\*.mat']);
            connectivity_files_sorted = sort_nat({connectivity_files.name})';
            subject_connectivity_means_stds = zeros(125, 2);
            for file_index = 1:size(connectivity_files_sorted, 1)
                connectivity_file = connectivity_files_sorted(file_index);
                connectivity_file = connectivity_file{:};
                connectivity_file = [base_path, subject_ID, '\',connectivity_file];
                connectivity = importdata(connectivity_file);
                subject_connectivity_means_stds(file_index, 1) = mean((connectivity(:)), 'omitnan');
                subject_connectivity_means_stds(file_index, 2) = std(connectivity(:), 'omitnan');
            end
            save([ '.\data\output\Correlations_Mean_STD\' char(classes(index, 1)) '\' subject_ID '_means_std.mat'], 'subject_connectivity_means_stds');
        end
    end
end
plotMatrixMean();

toc;

                