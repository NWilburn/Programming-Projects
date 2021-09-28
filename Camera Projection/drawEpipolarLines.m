function drawEpipolarLines(vue1, vue2, M_1, M_2, good_frames, frameNum, vid2Frame, vid4Frame)
    %goal of function is to draw epipolar lines onto image for given
    %frame. this is done by computing the epipole by projecting the
    %coordinates of the other camera onto the image space of the current
    %camera and then by drawing a line between this point and the joints.
    colors = ['y', 'm', 'c', 'r', 'g', 'b', 'w', 'k', 'y', 'm', 'c', 'r'];
    
    %get location of other camera and append a 1 so that the other camera
    %location can be projected onto the image space of the current camera.
    c1_loc = vue2.position;
    c1_loc(4) = 1;
    epipole_1 = M_1 * c1_loc.';
    epipole_1 = [epipole_1(1,:)./epipole_1(3,:); epipole_1(2,:)./epipole_1(3,:)];
    figure; image(vid2Frame); hold on;
    title('Epipolar Lines of Frame 8998 of vue2');
    %loop through every joint and compute the equation of the line that
    %connects the other camera and the joint coordinates
    for i = 1:length(good_frames(frameNum).joints)
        x_1 = [epipole_1(1), good_frames(frameNum).pix_coord_2(1,i)];
        y_1 = [epipole_1(2), good_frames(frameNum).pix_coord_2(2,i)];
        c = [[1; 1]  x_1(:)]\y_1(:);
        m = c(2);
        b = c(1);
        x = 1:1920;
        y = m*x + b;
        %after getting equation of the line, plot x and y values and put a
        %dot on the joint that the line is passing through
        plot(x, y, colors(i), 'LineWidth', 2)
        plot(good_frames(frameNum).pix_coord_2(1,i), good_frames(frameNum).pix_coord_2(2,i), strcat(colors(i), '*'), 'LineWidth', 5)
    end
    
    %repeat same steps as above but for the other camera now
    c2_loc = vue1.position;
    c2_loc(4) = 1;
    epipole_2 = M_2 * c2_loc.';
    epipole_2 = [epipole_2(1,:)./epipole_2(3,:); epipole_2(2,:)./epipole_2(3,:)];
    figure; image(vid4Frame); hold on;
    title('Epipolar Lines of Frame 8998 of vue4');
    for i = 1:length(good_frames(frameNum).joints)
        x_1 = [epipole_2(1), good_frames(frameNum).pix_coord_4(1,i)];
        y_1 = [epipole_2(2), good_frames(frameNum).pix_coord_4(2,i)];
        c = [[1; 1]  x_1(:)]\y_1(:);
        m = c(2);
        b = c(1);
        x = 1:1920;
        y = m*x + b;
        plot(x, y, colors(i), 'LineWidth', 2)
        plot(good_frames(frameNum).pix_coord_4(1,i), good_frames(frameNum).pix_coord_4(2,i), strcat(colors(i), '*'), 'LineWidth', 5)
    end
end

