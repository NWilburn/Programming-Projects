function points2D = project3Dto2D(M, good_frames)
    %this function projects all of the points in good_frames from 3D to 2D
    %pixel points
    points2D = good_frames;
    %check if pix_coord_2 field is already in good_frames. if it is, set
    %field to pix_coord_4. if not, set it to pix_coord_2
    if (isfield(good_frames, "pix_coord_2"))
        field = "pix_coord_4";
    else
        field = "pix_coord_2";
    end
    %loop through every frame
    for i = 1:length(good_frames)
        %for every frame, get the coordinates for all joints in that frame
        %and append a 1 to the fourth value of the coordinates
        cur_coord = good_frames(i).coord_list(:,:);
        cur_coord(:, 4) = 1;
        %transpose coordinates and multiply each coordinate by camera
        %matrix
        cam_coord = M * cur_coord.';
        %divide x and y values by third value to get pixel coordinates. add
        %coordinates to current frame and use field that was determined at
        %the beginning
        points2D(i).(field) = [cam_coord(1,:)./cam_coord(3,:); cam_coord(2,:)./cam_coord(3,:)];
    end