function plotSkeleton(good_frames, frameNum)
    %goal of this function is to plot both the original 3D coordinates and
    %the reconstructed 3D coordinates. This only works if all 12 joints are
    %good. otherwise it doesn't display anything.
    
    if (length(good_frames(frameNum).joints) == 12)
        %creating skeleton for original world coordinates first
        figure;
        title('Skeleton of 3D Original World Coordinates for Frame 8998');
        hold on;
        coord_list = good_frames(frameNum).coord_list;

        %go through each joint and connect them to the proper other joints.
        %right shoulder to right elbow, right elbow to right wrist, etc.
        plot3([coord_list(1, 1), coord_list(2, 1)], [coord_list(1, 2), coord_list(2, 2)], [coord_list(1, 3), coord_list(2, 3)], 'b');
        plot3([coord_list(2, 1), coord_list(3, 1)], [coord_list(2, 2), coord_list(3, 2)], [coord_list(2, 3), coord_list(3, 3)], 'b');
        plot3([coord_list(1, 1), coord_list(4, 1)], [coord_list(1, 2), coord_list(4, 2)], [coord_list(1, 3), coord_list(4, 3)], 'b');
        plot3([coord_list(4, 1), coord_list(5, 1)], [coord_list(4, 2), coord_list(5, 2)], [coord_list(4, 3), coord_list(5, 3)], 'b');
        plot3([coord_list(5, 1), coord_list(6, 1)], [coord_list(5, 2), coord_list(6, 2)], [coord_list(5, 3), coord_list(6, 3)], 'b');
        plot3([coord_list(7, 1), coord_list(10, 1)], [coord_list(7, 2), coord_list(10, 2)], [coord_list(7, 3), coord_list(10, 3)], 'b');
        plot3([coord_list(7, 1), coord_list(8, 1)], [coord_list(7, 2), coord_list(8, 2)], [coord_list(7, 3), coord_list(8, 3)], 'b');
        plot3([coord_list(8, 1), coord_list(9, 1)], [coord_list(8, 2), coord_list(9, 2)], [coord_list(8, 3), coord_list(9, 3)], 'b');
        plot3([coord_list(10, 1), coord_list(11, 1)], [coord_list(10, 2), coord_list(11, 2)], [coord_list(10, 3), coord_list(11, 3)], 'b');
        plot3([coord_list(11, 1), coord_list(12, 1)], [coord_list(11, 2), coord_list(12, 2)], [coord_list(11, 3), coord_list(12, 3)], 'b');
        %calculate midpoint for line connnecting left and right shoulder
        %and the line connecting the left and right hip. draw line from one
        %midpoint to the other
        midpoint_1 = (coord_list(1, :) + coord_list(4, :)).'/2;
        midpoint_2 = (coord_list(7, :) + coord_list(10, :)).'/2;
        plot3([midpoint_1(1, 1), midpoint_2(1, 1)], [midpoint_1(2, 1), midpoint_2(2, 1)], [midpoint_1(3, 1), midpoint_2(3, 1)], 'b');
        
        %repeat same process as above but this time for the reconstructed
        %world coordinates
        figure;
        title('Skeleton of 3D Reconstructed World Coordinates for Frame 8998');
        hold on;
        coors_3D = good_frames(frameNum).coors_3D;

        plot3([coors_3D(1, 1), coors_3D(2, 1)], [coors_3D(1, 2), coors_3D(2, 2)], [coors_3D(1, 3), coors_3D(2, 3)], 'r');
        plot3([coors_3D(2, 1), coors_3D(3, 1)], [coors_3D(2, 2), coors_3D(3, 2)], [coors_3D(2, 3), coors_3D(3, 3)], 'r');
        plot3([coors_3D(1, 1), coors_3D(4, 1)], [coors_3D(1, 2), coors_3D(4, 2)], [coors_3D(1, 3), coors_3D(4, 3)], 'r');
        plot3([coors_3D(4, 1), coors_3D(5, 1)], [coors_3D(4, 2), coors_3D(5, 2)], [coors_3D(4, 3), coors_3D(5, 3)], 'r');
        plot3([coors_3D(5, 1), coors_3D(6, 1)], [coors_3D(5, 2), coors_3D(6, 2)], [coors_3D(5, 3), coors_3D(6, 3)], 'r');
        plot3([coors_3D(7, 1), coors_3D(10, 1)], [coors_3D(7, 2), coors_3D(10, 2)], [coors_3D(7, 3), coors_3D(10, 3)], 'r');
        plot3([coors_3D(7, 1), coors_3D(8, 1)], [coors_3D(7, 2), coors_3D(8, 2)], [coors_3D(7, 3), coors_3D(8, 3)], 'r');
        plot3([coors_3D(8, 1), coors_3D(9, 1)], [coors_3D(8, 2), coors_3D(9, 2)], [coors_3D(8, 3), coors_3D(9, 3)], 'r');
        plot3([coors_3D(10, 1), coors_3D(11, 1)], [coors_3D(10, 2), coors_3D(11, 2)], [coors_3D(10, 3), coors_3D(11, 3)], 'r');
        plot3([coors_3D(11, 1), coors_3D(12, 1)], [coors_3D(11, 2), coors_3D(12, 2)], [coors_3D(11, 3), coors_3D(12, 3)], 'r');
        midpoint_1 = (coors_3D(1, :) + coors_3D(4, :)).'/2;
        midpoint_2 = (coors_3D(7, :) + coors_3D(10, :)).'/2;
        plot3([midpoint_1(1, 1), midpoint_2(1, 1)], [midpoint_1(2, 1), midpoint_2(2, 1)], [midpoint_1(3, 1), midpoint_2(3, 1)], 'r');
    else
        disp("All 12 joints must be good to display skeleton")
    end

