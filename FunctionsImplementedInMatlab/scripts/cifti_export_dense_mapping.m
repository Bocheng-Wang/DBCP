function [left_pair, right_pair] = cifti_export_dense_mapping (wb_dir, input)
%% left_pair || right_pair are in format of <brain_vertex_index> <cifti_(left or right)_index>
% Written by Bocheng Wang 2020.06.16

wb_command = [ wb_dir    '  -cifti-export-dense-mapping ' ...
                             input      ' '                                             ...
                            ' COLUMN -surface '                               ...
                            'CORTEX_LEFT '                                       ...
                            'left.txt'
                            ]; 
system(wb_command);
fid = fopen('left.txt');
left_pair = cell2mat(textscan(fid, '%d %d'));
fclose(fid);
delete('left.txt');

wb_command = [ wb_dir    '  -cifti-export-dense-mapping ' ...
                             input      ' '                                             ...
                            ' COLUMN -surface '                               ...
                            'CORTEX_RIGHT '                                       ...
                            'right.txt'
                            ]; 
system(wb_command);
fid = fopen('right.txt');
right_pair = cell2mat(textscan(fid, '%d %d'));
fclose(fid);
delete('right.txt');

 


