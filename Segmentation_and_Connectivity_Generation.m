
%% timer on ³ÌÐò¿ªÊ¼
tic;
%% Initialize 
clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

%% Read out the dense time series in 91,282 vertices of CIFTI space
classes = {'0.Normal';'2.EMCI';'4.LMCI';'5.AD';};
for index = 1:size(classes)
    base_path = ['./data/input/'  char(classes(index, 1)) '/'];
    files = dir(base_path);
    for file_index = 1:size(files, 1)
        if (files(file_index).isdir == 1) && (~strcmp(files(file_index).name, '.') && ~strcmp(files(file_index).name, '..'))
            subject_ID = files(file_index).name;
            cifti_file_dir = [base_path subject_ID '/MNINonLinear/Results/ses-01_task-rest_run-01/ses-01_task-rest_run-01_Atlas_s0.dtseries.nii'];       
            workbench_dir = [pwd '\workbench\wb_command.exe'];
            cii = ciftiopen(cifti_file_dir, workbench_dir); 
            dense_timeseries = cii.cdata;

            %% Dynamic Segmentation
            fMRIVolumns_number = 140;
            step = 1;
            win_width = 15;
            vertex_total = 91282;

            dWin_number = fix((fMRIVolumns_number - win_width)/step);
            % window = gausswin(win_width, 3)';

            for windowIndex = 1:dWin_number
                windowed_dseries = zeros(vertex_total, win_width);
                start_point = 1 + step .* (windowIndex - 1);
                for vertexIndex = 1:vertex_total
                    windowed_dseries(vertexIndex, :) = dense_timeseries(vertexIndex, start_point : start_point + win_width - 1);
                end
                cii.cdata = windowed_dseries;
                dtseries_tmp = [pwd '\data\output\tmp.dtseries.nii'];
                ciftisave(cii, dtseries_tmp, workbench_dir);
                %% parcellation
                label_dir = [pwd '\data\label\Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii'];
                ptseries_file_tmp = [pwd '\data\output\tmp.ptseries.nii'];
                cifti_parcellation(workbench_dir, dtseries_tmp, label_dir, ptseries_file_tmp);
                %% connectivity generation
                connection_file_tmp =  [pwd '\data\output\' num2str(windowIndex) '_tmp.pconn.nii'];
                cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp);
                conn_cii = ciftiopen(connection_file_tmp, workbench_dir); 
                conn = conn_cii.cdata;
                outputfolder = [pwd '\data\output\' char(classes(index, 1)) '\' subject_ID '\'];
                if ~exist(outputfolder, 'dir')
                    mkdir(outputfolder) ;
                end
                [outputfolder subject_ID '_' num2str(windowIndex) ' --- Finished!']
                save([outputfolder subject_ID '_' num2str(windowIndex) '.mat'], 'conn');
                delete(ptseries_file_tmp, dtseries_tmp, connection_file_tmp); 
            end
            %%
            toc;
        end
    end
end
 



 
