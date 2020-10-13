P = phantom(128); % ����һ��ͼ��
theta = 1:180;    %ͶӰ�Ƕ�

% radon�任 
[R,xp] = radon(P,theta);
%���ٸ���Ҷ�任�Ŀ��
width = 2^nextpow2(size(R,1)); 

%��ͶӰ����һά����Ҷ�任
proj_fft = fft(R, width);

% �˲� ����RL�˲���
% �����˲���
filter = 2*[0:(width/2-1), width/2:-1:1]'/width;
%�˲� Ƶ����� �ռ�����
proj_filtered = zeros(width,180);
for i = 1:180
    proj_filtered(:,i) = proj_fft(:,i).*filter;
end

% �˲������һά����Ҷ���任
proj_ifft = real(ifft(proj_filtered)); % get the real part of the result

% ��ͶӰ
fbp = zeros(128); %���ش�С
for i = 1:180
    rad = theta(i)*pi/180;
    for x = (-128/2+1):128/2
        for y = (-128/2+1):128/2
            t = round(x*cos(rad+pi/2)+y*sin(rad+pi/2));
            fbp(x+128/2,y+128/2)=fbp(x+128/2,y+128/2)+proj_ifft(t+round(size(R,1)/2),i);
        end 
    end
end
fbp = fbp/180;

% ��ͼ
subplot(1, 2, 1), imshow(P), title('Original')
subplot(1, 2, 2), imshow(fbp), title('FBP')