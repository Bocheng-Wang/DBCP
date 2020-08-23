function MapHCP2RSN()
%% Written by Bocheng Wang, 2020.06.16
% Map HCP areas into RSN 7 networks


%% Initialize 
clc; clear all; close all; fclose('all');
addpath(genpath(pwd));

%% 
HCP_file = '.\Atlas\Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii';
RSN_file = '.\Atlas\RSN-networks.32k_fs_LR.dlabel.nii';
workbench_dir = [pwd '\workbench\wb_command.exe'];

RSN_map_num = 1;

%% Extract CIFTI index by using Brain Index in dLabel file
[HCP_left, HCP_right] = cifti_export_dense_mapping(workbench_dir, HCP_file);
[RSN_left, RSN_right] = cifti_export_dense_mapping(workbench_dir, RSN_file);

%% Extract Parcellation Info by using dLabel file
HCP_areas_ci = ciftiopen(HCP_file, workbench_dir);
RSN_areas_ci = ciftiopen(RSN_file, workbench_dir);

HCP_areas = HCP_areas_ci.cdata;
RSN_areas = RSN_areas_ci.cdata(:, 1);


HCP_RSN_mapping_left = zeros(180, 2);
HCP_RSN_mapping_left(:, 1) = 181:360;

HCP_RSN_mapping_right = zeros(180, 2);
HCP_RSN_mapping_right(:, 1) = 1:180;

%% For right hemisphere
for HCP_area_index = 1:180 
    area_index_in_HCP = find(HCP_areas==HCP_area_index);
    tmp = HCP_right(:, 1);
    areas_index_in_CIFTI = zeros(1);
    for i = 1:size(area_index_in_HCP)
        area_index_in_CIFTI = HCP_right(tmp == area_index_in_HCP(i) , 2);
        areas_index_in_CIFTI = [areas_index_in_CIFTI; area_index_in_CIFTI];
    end
    areas_index_in_CIFTI(1) = [];
    
    tmp = RSN_right(:, 2);
    areas_index_in_RSN = zeros(1);
    for i = 1:size(areas_index_in_CIFTI)
        mm = find(tmp == areas_index_in_CIFTI(i));
        area_index_in_RSN = RSN_right(tmp == areas_index_in_CIFTI(i), 1);
        areas_index_in_RSN = [areas_index_in_RSN; area_index_in_RSN];
    end
    areas_index_in_RSN(1) = [];
    
    RSN = RSN_areas(areas_index_in_RSN);
    stastisInfo = tabulate(RSN);
    tmp1 = stastisInfo(:, 2);
    Final_RSN = stastisInfo(tmp1 == max(stastisInfo(:, 2)), 1);
    HCP_RSN_mapping_right(HCP_area_index, 2) = Final_RSN(1);
end
 
%% For left hemisphere
for HCP_area_index = 181:360
    area_index_in_HCP = find(HCP_areas==HCP_area_index);
    tmp = HCP_left(:, 1);
    areas_index_in_CIFTI = zeros(1);
    for i = 1:size(area_index_in_HCP)
        area_index_in_CIFTI = HCP_left(tmp == area_index_in_HCP(i) , 2);
        areas_index_in_CIFTI = [areas_index_in_CIFTI; area_index_in_CIFTI];
    end
    areas_index_in_CIFTI(1) = [];
    
    tmp = RSN_left(:, 2);
    areas_index_in_RSN = zeros(1);
    for i = 1:size(areas_index_in_CIFTI)
        area_index_in_RSN = RSN_left(tmp == areas_index_in_CIFTI(i), 1);
        areas_index_in_RSN = [areas_index_in_RSN; area_index_in_RSN];
    end
    areas_index_in_RSN(1) = [];
 
    RSN = RSN_areas(areas_index_in_RSN);
    stastisInfo = tabulate(RSN);
    tmp1 = stastisInfo(:, 2);
    Final_RSN = stastisInfo(tmp1 == max(stastisInfo(:, 2)), 1);
    HCP_RSN_mapping_left(HCP_area_index - 180, 2) = Final_RSN(1);
end

HCP_RSN_mapping = [HCP_RSN_mapping_right; HCP_RSN_mapping_left];
save('HCP_RSN_mapping.mat', 'HCP_RSN_mapping');





