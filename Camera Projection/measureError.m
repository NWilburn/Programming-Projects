function [stat_data, error] = measureError(good_frames)
    %goal of function is to generate data points for average, std, min,
    %median, and max, and to get the L^2 sums so that they can be plotted
    %to show error
    error = zeros(length(good_frames), 1);
    L_all = NaN(length(good_frames), 12);
    stat_data = zeros(13, 5);
    %loop through each frame and calculate L^2 for each joint
    for i = 1:length(good_frames)
        X = (good_frames(i).coord_list(:,1) - good_frames(i).coors_3D(:, 1)).^2;
        Y = (good_frames(i).coord_list(:,2) - good_frames(i).coors_3D(:, 2)).^2;
        Z = (good_frames(i).coord_list(:,3) - good_frames(i).coors_3D(:, 3)).^2;
        L = sqrt(X + Y + Z);
        %sum every L^2 and put it in error array
        error(i) = sum(L);
        L_all(i, 1:length(good_frames(i).coord_list)) = L.';
    end
    %compute data for each L^2 individually and then compute data for all
    %L^2 total
    stat_data(1:12, 1) = mean(L_all, 'omitnan');
    stat_data(13, 1) = mean(L_all, 'all', 'omitnan');
    stat_data(1:12, 2) = std(L_all, 'omitnan');
    stat_data(13, 2) = std(L_all, 0, 'all', 'omitnan');
    stat_data(1:12, 3) = min(L_all);
    stat_data(13, 3) = min(L_all, [], 'all');
    stat_data(1:12, 4) = median(L_all, 'omitnan');
    stat_data(13, 4) = median(L_all, 'all', 'omitnan');
    stat_data(1:12, 5) = max(L_all);
    stat_data(13, 5) = max(L_all, [], 'all');
    
end

