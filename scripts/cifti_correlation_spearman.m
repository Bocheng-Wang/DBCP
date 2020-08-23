function [connectivity] = cifti_correlation_spearman(series, correlation_name)
%%Written by Bocheng Wang, 2020,06.01
% Recently, when computed the correlation coefficients among dynamic
% window in fMRI, I found that the connectivity between two windowed series
% changed heavily though the moving step was only 1. I think that it is
% caused by the pearson correlatioship. So I change the computing way into
% Spearman coefficients. 
% While, in wb_commands of CIFTI, it is not supported in
% --cifti-correlation option. Thus I implement it here in my codes.

%% Start function
Dimension = size(series, 1);
connectivity = zeros(360);
for ROI = 1 : Dimension
    for Other_ROI = 1 : Dimension
        coefficient = corr(series(ROI,:)', series(Other_ROI,:)', 'type', correlation_name);
        connectivity(Other_ROI, ROI) = coefficient;
    end
end
end

