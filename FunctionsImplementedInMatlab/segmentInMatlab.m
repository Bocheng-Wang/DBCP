function  segmentInMatlab(workDir, subjectDir, output, subjectID, wbcommand)
% for the reason that the cifti file could only be opended in ciftiopen.m,
% here, we segment the dtseries.nii into windowed dtseries.nii, and
% parcellate them into tmp.ptseries.nii file
% This function should be saved in the folder outside the /cifti_data/
% Bocheng Wang October, 2020

%% Initialize 
addpath(genpath(pwd));


%% Load dtseries data into matlab
subject_dir = subjectDir;
cifti_file_dir = [workDir '/ciftify_output/' subjectID  '/MNINonLinear/Results/ses-01_task-rest_run-01/ses-01_task-rest_run-01_Atlas_s0.dtseries.nii'];       
workbench_dir = wbcommand;
cii = ciftiopen(cifti_file_dir, workbench_dir); 
dense_timeseries = cii.cdata;



%% Dynamic Segmentation
            fMRIVolumns_number = size(dense_timeseries,2);
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
                dtseries_tmp = ['/tmp/' num2str(windowIndex) '.tmp.dtseries.nii'];
                ciftisave(cii, dtseries_tmp, workbench_dir);
            end
            %% parcellation in multi thread (computation for the dynamic connectivity
            parfor windowIndex = 1:dWin_number
                label_dir = [workDir '\HCP_MMP_parcellation.dlabel.nii'];
                dtseries_tmp = ['/tmp/' num2str(windowIndex) '.tmp.dtseries.nii'];
                ptseries_file_tmp = [subject_dir '/HCP/' num2str(windowIndex) '.tmp.ptseries.nii'];
                cifti_parcellation(workbench_dir, dtseries_tmp, label_dir, ptseries_file_tmp);
                %% connectivity generation
                connection_file_tmp =  [subject_dir '/HCP/' num2str(windowIndex) '_tmp.pconn.nii'];
                cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp);
                conn_cii = ciftiopen(connection_file_tmp, workbench_dir); 
                conn = conn_cii.cdata;
                outputfolder = [output 'DynamicConnectivity/'];
                if ~exist(outputfolder, 'dir')
                    mkdir(outputfolder) ;
                end
                saveConnectivityIntoMatfile([outputfolder  '' num2str(windowIndex) '.mat'], conn);
%                 delete(ptseries_file_tmp, dtseries_tmp, connection_file_tmp); 
            end
           
%% computation for the average (static) connectivity
             label_dir = [workDir '\HCP_MMP_parcellation.dlabel.nii'];
             dtseries_tmp = cifti_file_dir;
             ptseries_file_tmp = [subject_dir '/HCP/average.tmp.ptseries.nii'];
             cifti_parcellation(workbench_dir, dtseries_tmp, label_dir, ptseries_file_tmp);
             connection_file_tmp =  [subject_dir '/HCP/average_tmp.pconn.nii'];
             cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp);
             conn_cii = ciftiopen(connection_file_tmp, workbench_dir); 
             conn = conn_cii.cdata;
             outputfolder = [output 'StaticConnectivity/'];
             if ~exist(outputfolder, 'dir')
                 mkdir(outputfolder) ;
             end
             saveConnectivityIntoMatfile([outputfolder  'staticConnectivity.mat'], conn);
%              delete(ptseries_file_tmp, connection_file_tmp); 
end

function saveConnectivityIntoMatfile(dir, connectivity)
%% save function could not be used in parfor directly. We implement it in this function
%     Bocheng Wang, October, 2020

save(dir, 'connectivity');
end

