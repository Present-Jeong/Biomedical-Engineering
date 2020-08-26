function output = read_fiber(input)
%% READ_FIBER reads fiber information.
%
% Input: .dat fiber information file generated from DTI-Studio.
% Written by Sung-Woo Kim on May 2, 2017.
%
% Reference:
%   https://www.mristudio.org/wiki/faq#head-dc95149bbd3b16fb7a4abef8d63aafb5f435d60c

%% Main
fid=fopen(input);
chk1 = fread(fid, 8, '*char')'; % char sFiberFileTag[8]; // = "FiberDat"
if ~strcmp(chk1, 'FiberDat')
    error('Wrong Fiber Files! (Error Type 1)\n');
end

% Fiber Information
output.FiberNr = fread(fid, 1, 'int32'); % int nFiberNr; // number of fiber chain in this file
output.FiberLenMax = fread(fid, 1, 'int32'); % int nReserved: max-length of fibers
output.FiberLenMean = fread(fid,1, 'float'); % float fReserved: mean-length of fibers

% Image Demension
output.ImgWidth = fread(fid, 1, 'int32'); % int nImgWidth
output.ImgHeight = fread(fid, 1, 'int32'); % int nImgHeight
output.ImgSlice = fread(fid, 1, 'int32'); % int nImgSlices

% Voxel Size
output.PixelSizeWidth = fread(fid, 1, 'float'); % float fPixelSizeWidth
output.PixelSizeHeight = fread(fid, 1, 'float'); % float fPixelSizeHeight
output.SliceThickness = fread(fid, 1, 'float'); % float fSliceThickness

output.SliceOrientation = fread(fid, 1,'unsigned char'); % unsigned char cSliceOrientation; // 0=coronal, 1=axial, 2=sagittal
output.SliceSequencing =  fread(fid, 1,'unsigned char');% unsigned char cSliceSequencing; // 0=normal, 1=flipped
chk2 = fread(fid,82,'*char'); % offset128: move file pointer 128, where fiber-data starts
if ~isequal(double(chk2), zeros(82, 1))
    error('Wrong Fiber Files! (Error Type 1)\n');
end

output.Fiber = cell(output.FiberNr,1);
for i = 1:output.FiberNr
    output.Fiber{i}.nLength = fread(fid, 1, 'int32'); % int nFiberLength // fiber length
    output.Fiber{i}.nSelStatus = fread(fid, 1, 'unsigned char'); % unsigned char cReserved
    output.Fiber{i}.rgbColor = fread(fid, 3, 'unsigned char'); % rgbFiberColor // R-G-B, 3 bytes totally
    output.Fiber{i}.nSelLenStart = fread(fid, 1, 'int32'); % int nSelectFiberStartPoint
    output.Fiber{i}.nSelLenEnd = fread(fid, 1, 'int32'); % int nSelectFiberEndPoint
    output.Fiber{i}.pxyzChain = zeros(output.Fiber{i}.nLength, 3);
    for j = 1:output.Fiber{i}.nLength
        output.Fiber{i}.pxyzChain(j,:) = fread(fid, 3, 'float')';
    end
end

chk3 = fread(fid, 500, '*char');
if ~isempty(chk3)
    error('Wrong Fiber Files! (Error Type 3)\n');
end
fclose(fid);
end