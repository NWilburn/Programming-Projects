function [M, location] = Calculate_M_Matrix(vue)
    %function is used to calculate camera matrix by taking K * [R|t] and
    %get the location of the camera for current vue.
    M = vue.Kmat * vue.Pmat;
    location = vue.position;