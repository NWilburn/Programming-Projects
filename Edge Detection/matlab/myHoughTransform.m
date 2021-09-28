function [H, rhoScale, thetaScale] = myHoughTransform(Im, threshold, rhoRes, thetaRes)
    %Invert image and get size of image
    Im = Im';
    [M, N] = size(Im);
    %Determine rhoMax by getting the magnitude of the input image and find
    %thetaMax
    rhoMax = sqrt(M.^2+N.^2); 
    thetaMax = 2.0*pi / thetaRes;
    %Create thetaScale and rhoScale using thetaRes, thetaMax, rhoRes, and
    %rhoMax
    thetaScale = (thetaRes * ((1:thetaMax)-1));
    rhoScale = (0:rhoRes:rhoMax);
    %Create accumulator matrix using size of rho and theta
    H = zeros([length(rhoScale), length(thetaScale)]);
    %Loop through every pixel of input image
    for M = 1:M
        for N = 1:N
            %Check if value at pixel is greater than threshold value
            if Im(M,N) > threshold
                %Loop through every theta
                for theta = 1:length(thetaScale)
                    %Calculate rho using theta and pixel coordinates
                    rho = floor(M*cos(thetaScale(theta)) + N*sin(thetaScale(theta)));
                    %Check if rho is positive and then add 1 vote to the
                    %correct coordinates in the accumulator
                    if rho > 0
                        H(floor((rho/2)+1), theta) = H(floor((rho/2)+1), theta) + 1;
                    end
                end
            end
        end
    end
end
        
        