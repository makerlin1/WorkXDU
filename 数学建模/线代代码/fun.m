%�ߴ���������ʽ
%1.��������ֵ��������
M = input('�������:'); 
[x,y] = size(M);
R = eig(M);%������ֵ
l = size(R);
%format rat %%%%% ת��ר������ʾ
disp("����ֵ��");
disp(R)
for i=1:l(1)
    T = M - eye(x).*R(i);
    P = rref(T);
    disp("��Ӧ����ξ���");
    disp(P);
end;
%2.����Խǻ�
M = input("�������");
R = eig(M;

    
