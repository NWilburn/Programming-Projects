function points_3D = myTriangulation(good_frames, M_1, M_2)
    %goal of this function is to reconstruct the original 3D coordinates
    %using the pixel coordinates found earlier using triangulation
    points_3D = good_frames;
    %loop through every frame and every joint in frame
    for i = 1:length(good_frames)
        world_coors = zeros(length(good_frames(i).pix_coord_2), 3);
        for j = 1:length(good_frames(i).pix_coord_2)
            %good coordinates of joint in vue2 and vue4
            coo_1 = good_frames(i).pix_coord_2(:,j);
            coo_2 = good_frames(i).pix_coord_4(:,j);
            %use coordinates and camera matrices to construct A matrix
            A_1 = coo_1(2)*M_1(3,:) - M_1(2,:);
            A_2 = M_1(1,:) - coo_1(1)*M_1(3,:);
            A_3 = coo_2(2)*M_2(3,:) - M_2(2,:);
            A_4 = M_2(1,:) - coo_2(1)*M_2(3,:);
            A = [A_1; A_2; A_3; A_4];
            %do svd by computing eigenvalues and eigenvectors
            [u,d] = eigs(A'*A);
            %locate the smallest eigenvalue on the diagonal and save its
            %column number
            [~, col] = min([d(1,1),d(2,2),d(3,3),d(4,4)]);
            %set the eigenvector at determined column to be the world
            %coordinates for joint and divide X, Y, and Z values by fourth
            %value to get reconstructed 3D coordinates
            world_coors(j, 1:3) = u(1:3,col)/u(4,col); 
            
        end
        points_3D(i).coors_3D = world_coors;
    end