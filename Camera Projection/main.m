%Load videos and mocapJoints data
vue2video = VideoReader('Subject4-Session3-24form-Full-Take4-Vue2.mp4');
vue4video = VideoReader('Subject4-Session3-24form-Full-Take4-Vue4.mp4');
load('Subject4-Session3-Take4_mocapJoints.mat');

%loop through frames and joints to see if the confidence value for the
%joint is at 1. If it is, save the frame number, joints, and joint
%coordinates to a new structure called good_frames
good_frames = struct;
for i=1:length(mocapJoints)
    good_joints = double.empty;
    for j=1:12
        if mocapJoints(i,j,4) == 1
            good_joints(end+1)=j;
        end
    end
    if ~isempty(good_joints)
        if isempty(fieldnames(good_frames))
            good_frames(1).frame_num = i;
            good_frames(1).joints = good_joints;
            good_frames(1).coord_list = squeeze(mocapJoints(i, good_joints, 1:3));
        else
            good_frames(end+1).frame_num = i;
            good_frames(end).joints = good_joints;
            good_frames(end).coord_list = squeeze(mocapJoints(i, good_joints, 1:3));
        end
    end
end

%load calibration data
load('vue2CalibInfo.mat');
load('vue4CalibInfo.mat');

%calculate camera matrix for both vue2 and vue4
[M_2, location_2] = Calculate_M_Matrix(vue2);
[M_4, location_4] = Calculate_M_Matrix(vue4);

%project every point from good_frames from 3D to 2D and update good_frames
%to have a new field called pix_coord_2 for vue2 and pix_coord_4 for vue4
good_frames = project3Dto2D(M_2, good_frames);
good_frames = project3Dto2D(M_4, good_frames);

%set frameNum to be used for rest of project to demonstrate results
frameNum = 8998;

%overlay the 2D points for vue2 and vue4 onto the frame at frameNum set
%above
vue2video.CurrentTime = (frameNum-1)*(50/100)/vue2video.FrameRate;
vid2Frame = readFrame(vue2video);
figure; image(vid2Frame); hold on;
title('2D points overlayed on to frame 8998 of vue2');
plot((good_frames(frameNum).pix_coord_2(1,:)),(good_frames(frameNum).pix_coord_2(2,:)), 'r+', 'MarkerSize', 15, 'LineWidth', 2)

vue4video.CurrentTime = (frameNum-1)*(50/100)/vue4video.FrameRate;
vid4Frame = readFrame(vue4video);
figure; image(vid4Frame); hold on; 
title('2D points overlayed on to frame 8998 of vue4');
plot((good_frames(frameNum).pix_coord_4(1,:)),(good_frames(frameNum).pix_coord_4(2,:)), 'r+', 'MarkerSize', 15, 'LineWidth', 2)

%reconstruct 3D points from 2D points using triangulation and add them to
%a new field in good_frames called coors_3D
good_frames = myTriangulation(good_frames, M_2, M_4);

%plot 3D original coordinates and 3D reconstructed coordinates to create
%skeleton
plotSkeleton(good_frames, frameNum)

%calculate euclidean distance between reconstructed 3D points and original 3D points
%and collect mean, std, minimum, median, and average data on euclidean
%distances as well as sum all euclidean distances in each frame so that
%each frame's euclidean distance sum can be plotted
[stat_data, error] = measureError(good_frames);

%plot euclidean distance sum for each frame
figure; 
title('Total Euclidian Distance');
xlabel('Frame Number');
ylabel('L Squared Error');
hold on;
plot(1:length(error), error(:,1));

%draw epipolar lines on frameNum for both vue2 and vue4
drawEpipolarLines(vue2, vue4, M_2, M_4, good_frames, frameNum, vid2Frame, vid4Frame)