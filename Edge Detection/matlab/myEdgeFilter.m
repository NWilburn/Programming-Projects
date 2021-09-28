function img1 = myEdgeFilter(img0, sigma)
    %Determine hsize and create a gaussian filter using hsize and sigma.
    %After getting h, convolve it with input image using myImageFilter to
    %smooth out the input image
    hsize = 2 * ceil(3 * sigma) + 1;
    h = fspecial('gaussian', hsize, sigma);
    img0_smooth = myImageFilter(img0, h);
    %Create sobel function and pass it and the smoothed image through
    %myImageFilter to get the gradient derivate in the x direction. Do this
    %again but invert sobel function to get the gradient derivate in the y
    %direction
    h_sob = fspecial('sobel');
    imgx = myImageFilter(img0_smooth, h_sob);
    imgy = myImageFilter(img0_smooth, h_sob');
    %get magnitude of img to get both x and y edges on output image
    img1_mag = sqrt(imgx.^2+imgy.^2);
    
    %Edges in magnitude are rather thick. Need to use non-maximum
    %suppression to ideally get edges that are 1 pixel wide. We will need
    %the gradient direction of the edges, so take arctan to get those
    %angles. Shift it up by 90 degrees just to make it a little easier to
    %work with. Angles will vary from 0 - 180 degrees
    img1_ang = atand(imgy./imgx) + 90;
    
    %NMS step. Start by getting size of output image and set output image
    %equal to the gradient magnitude
    [row, col] = size(img1_mag);
    img1 = img1_mag;
    %Loop through every pixel except for the ones on the ends
    for M = 2:row-1
        for N = 2:col-1
            %Check to see if angle at current pixel is close to 0/180, 45, 90,
            %or 135. After finding the angle, check the two neighboring
            %pixels along that gradient direction. If the center pixel is
            %smaller than either neighbor, set the center pixel to 0
            if img1_ang(M,N) < 22.5 || img1_ang(M,N) > 157.5
                if (img1_mag(M,N+1) > img1_mag(M,N)) || (img1_mag(M,N-1) > img1_mag(M,N))
                   img1(M,N) = 0;
                end
            elseif img1_ang(M,N) >= 22.5 && img1_ang(M,N) < 67.5
               if (img1_mag(M-1,N+1) > img1_mag(M,N)) || (img1_mag(M+1,N-1) > img1_mag(M,N))
                   img1(M,N) = 0;
               end
            elseif img1_ang(M,N) >= 67.5 && img1_ang(M,N) < 112.5
                if (img1_mag(M-1,N) > img1_mag(M,N)) || (img1_mag(M+1,N) > img1_mag(M,N))
                   img1(M,N) = 0;
                end
            elseif (img1_ang(M,N) >= 112.5 && img1_ang(M,N) <= 157.5)
                if (img1_mag(M+1,N+1) > img1_mag(M,N)) || (img1_mag(M-1,N-1) > img1_mag(M,N))
                   img1(M,N) = 0;
               end
            end
        end
    end
end
    
                
        
        
