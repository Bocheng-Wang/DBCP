function plotMatrixMean()
%% Written by Bocheng Wang 2020.06.01

clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

%% Start
classes = {'0.Normal';'2.EMCI';'4.LMCI';'5.AD';};
figure,
for index = 1:size(classes)
    base_path = ['.\data\output\Correlations_Mean_STD\'  char(classes(index, 1)) '\'];
    subjectFolder = dir([base_path '*.mat']);
    
    %% Save all the sessioned means and stds for each subject into single mat file.
    number_column = 128; % 125 for the windows number, 1 for a blank cell. The last two cell for the average and std in each subject.
    number_row = size(subjectFolder, 1);
    group_means = zeros(number_row, number_column);
    group_stds = zeros(number_row, number_column);
    
    %% Plot
    for Correlations_Mean_index = 1:size(subjectFolder, 1)
        correlation_file = [base_path, subjectFolder(Correlations_Mean_index).name];
        Correlations_Mean_STD = importdata(correlation_file);
        subplot(2,2,index);        
        Means = Correlations_Mean_STD(:,1);
        STDs = Correlations_Mean_STD(:,2);
        CVs = STDs ./ Means;
        plot(Means(:));
        title([char(classes(index, 1))]);
        hold on
        grid minor
        grid on
        
        %% Put each subject info into the single mat file
        group_means(Correlations_Mean_index, 1:125) = Means;
        group_means(Correlations_Mean_index, 127) = mean(Means);
        group_means(Correlations_Mean_index, 128) = std(Means);
        
        group_stds(Correlations_Mean_index, 1:125) = STDs;
        group_stds(Correlations_Mean_index, 127) = mean(STDs);
        group_stds(Correlations_Mean_index, 128) = std(STDs);
    end
    
    %% Save
    save(['.\data\output\Correlations_Mean_STD\dynamic_statistical_analysis\'   char(classes(index, 1)) '_group_means.mat'], 'group_means');
    save(['.\data\output\Correlations_Mean_STD\dynamic_statistical_analysis\'   char(classes(index, 1)) '_group_stds.mat'], 'group_stds');
end




