function [img1] = myImageFilter(img0, h)
    %Get size of filter and determine the padding size for the rows and
    %columns
    [hrow, hcol] = size(h);
    padrow_size = (hrow-1)/2;
    padcol_size = (hcol-1)/2;
    %Pad image using sizes determined previously
    pad_img0 = padarray(img0, [padrow_size, padcol_size], 'replicate');
    %Create output img that is the same size as the input img and flip the
    %filter in both the x and y direction. Get size of input image
    img1=zeros(size(img0));
    h = flip(flip(h,2));
    [row, col] = size(img0);
    %Loop through every pixel and create a spot around the current pixel
    %that is the same size as the filter. Multiply that spot by the filter
    %and then sum it together. Put this sum into the output image at the
    %same coordinates as the current pixel being looked at in the input
    %image
    for M = 1:row
        for N = 1:col
            spot=pad_img0(M:M+2*padrow_size, N:N+2*padcol_size);
            img1(M,N) = sum(sum(spot.*h));
        end
    end
end
