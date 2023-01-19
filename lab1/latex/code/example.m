clf
clear all
set(0, 'defaultaxesfontsize', 16);
% Filter for part A
hA = 1/sqrt(2)*[1 1];
% Filter for part B
N = 16;
beta = 0.35;
n = -N:(N-1);
n = n + 0.5;
hB = 2*beta*cos((1+beta)*pi*n/2)./(pi*(1-4*beta^2*n.^2));
hB = hB+sin((1-beta)*pi*n/2)./(pi*(n-4*beta^2*n.^3));
hB = hB*sqrt(2);
