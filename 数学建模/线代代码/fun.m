%线代常见计算式
%1.计算特征值特征向量
M = input('输入矩阵:'); 
[x,y] = size(M);
R = eig(M);%求特征值
l = size(R);
%format rat %%%%% 转成专分数表示
disp("特征值：");
disp(R)
for i=1:l(1)
    T = M - eye(x).*R(i);
    P = rref(T);
    disp("对应最简形矩阵");
    disp(P);
end;
%2.矩阵对角化
M = input("输入矩阵");
R = eig(M;

    
