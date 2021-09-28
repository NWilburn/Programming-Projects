function [rhos, thetas] = myHoughLines(H, nLines)
    %Do NMS to isolate local maxima
    kern = (H > imdilate(H, [1 1 1; 1 0 1;1 1 1]));
    H = H.*kern;
    %Sort maxima in descending order and get their index location
    [~, indx] = sort(H(:), 'descend');
    %Get highest scoring lines from 1 to nLines
    mindx = indx(1:nLines);
    %Convert maxima index values to component coordinates and output
    [rhos, thetas] = ind2sub(size(H), mindx);
end
        