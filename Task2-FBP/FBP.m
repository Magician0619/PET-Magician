P = phantom(128); % 创建一幅图像
theta = 1:180;    %投影角度

% radon变换 
[R,xp] = radon(P,theta);
%快速傅里叶变换的宽度
width = 2^nextpow2(size(R,1)); 

%对投影进行一维傅里叶变换
proj_fft = fft(R, width);

% 滤波 采用RL滤波器
% 构造滤波器
filter = 2*[0:(width/2-1), width/2:-1:1]'/width;
%滤波 频域相乘 空间域卷积
proj_filtered = zeros(width,180);
for i = 1:180
    proj_filtered(:,i) = proj_fft(:,i).*filter;
end

% 滤波后进行一维傅里叶反变换
proj_ifft = real(ifft(proj_filtered)); % get the real part of the result

% 反投影
fbp = zeros(128); %像素大小
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

% 画图
subplot(1, 2, 1), imshow(P), title('Original')
subplot(1, 2, 2), imshow(fbp), title('FBP')