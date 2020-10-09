#include "FBP_source.h"


//反投影
void backprojection(int angle, double* data, Mat result, int lenData)
{
	int length = result.cols;
	if (angle <= 90) {
		for (int i = 0; i < length; ++i) {
			double* rowResult = result.ptr<double>(i);
			for (int j = 0; j < length; ++j) {
				double x_interval = j + 0.5 - length / 2;
				double y_interval = length / 2 - (i + 0.5);

				double line = sqrt(y_interval * y_interval + x_interval * x_interval);
				double lineX_angle;
				if (fabs(x_interval) <= 0.001) {
					lineX_angle = CV_PI / 2;
					if (y_interval < 0) lineX_angle = -lineX_angle;
				}
				else if (fabs(y_interval) <= 0.001) {
					lineX_angle = 0;
					if (x_interval < 0) lineX_angle = -lineX_angle;
				}
				else {
					lineX_angle = atan(y_interval / x_interval);
					if (lineX_angle < 0) {
						if (y_interval > 0) {
							lineX_angle += CV_PI;
						}
					}
					else {
						if (y_interval < 0) {
							lineX_angle += CV_PI;
						}
					}
				}
				lineX_angle -= angle / 180.0 * CV_PI;
				double interval = line * sin(lineX_angle);
				double index = -interval + (lenData / 2.0) - 0.5;
				int latter = (int)index;
				rowResult[j] += data[latter] * (1 - index + latter) + data[latter + 1] * (index - latter);
			}
		}
	}

	else {
		for (int i = 0; i < length; ++i) {
			double* rowResult = result.ptr<double>(i);
			for (int j = 0; j < length; ++j) {
				double x_interval = j + 0.5 - length / 2;
				double y_interval = length / 2 - (i + 0.5);
				double line = sqrt(y_interval * y_interval + x_interval * x_interval);
				double lineX_angle;
				if (fabs(x_interval) <= 0.001) { lineX_angle = CV_PI / 2; }
				else { lineX_angle = atan(y_interval / x_interval); }

				if (lineX_angle < 0) {
					if (y_interval > 0) {
						lineX_angle += CV_PI;
					}
					else {}
				}
				else if (y_interval < 0) {
					lineX_angle += CV_PI;
				}

				lineX_angle -= (180 - angle) * CV_PI / 180;
				double interval = line * sin(lineX_angle);
				double index = interval + (lenData / 2.0) - 0.5;
				int latter = (int)index;
				rowResult[length - 1 - j] += data[latter] * (1 - index + latter) + data[latter + 1] * (index - latter);
			}
		}
	}

}

//滤波 根据所选滤波器类型
double a_func(int i, double* p, int len)
{

	if (i < 0) {
		return (p[0] + p[1]) / 2;
	}
	else if (i >= len) {
		return (p[len - 1] + p[len - 2]) / 2;
	}
	else {
		return p[i];
	}
}

double h_func(const int& i, int type)
{
	if (type == RLFILTER) {
		if (i == 0) {
			return 0.25;
		}
		else if (i % 2 == 0) {
			return 0;
		}
		else {
			return  -1 / (i * i * 3.14 * 3.14);
		}
	}
	else if (type == SLFILTER) {
		return -2 / (CV_PI * CV_PI * (4 * i * i - 1));
	}

}

void convolutionFilter(int angle, double* p, int len, int filType)
{
	//this vector is used as buffer.
	vector<double> result(len, 0);

	for (int n = 0; n < len; ++n) {
		for (int i = 1; i < (len * 2 - 1); ++i) {
			result[n] += a_func(n + i - len, p, len) * h_func(i - len, filType);
		}
	}

	for (int n = 0; n < len; ++n) {
		p[n] = result[n];
	}
}

//坐标转换
double find(double x, double y, Mat origin)
{
	int a = (int)(x - 0.5);
	int b = (int)(y + 0.5);
	if (a < 0) a = a - 1;
	if (b < 0) b = b - 1;
	double x_interval = x - a - 0.5;
	double y_interval = y - b + 0.5;
	int x_result = origin.rows / 2 - b;
	int y_result = a + origin.cols / 2;
	if (x_result < 1 || y_result < 0 || x_result >= origin.rows || y_result >= (origin.cols - 1)) {
		return 0;
	}
	else {
		double value1 = origin.at<unsigned char>(x_result - 1, y_result);
		double value2 = origin.at<unsigned char>(x_result - 1, y_result + 1);
		double value3 = origin.at<unsigned char>(x_result, y_result);
		double value4 = origin.at<unsigned char>(x_result, y_result + 1);
		return (value1 * (1 - x_interval) + value2 * x_interval) * y_interval + (value3 * (1 - x_interval) + value4 * x_interval) * (1 - y_interval);

	}

}

//正投影 霍登变换
void projection(unsigned char angle, Mat origin, Mat projectionData, int nLength)
{
	double* angleData = projectionData.ptr<double>(angle);
	if (angle == 0) {
		for (int i = 0; i < origin.rows; ++i) {
			unsigned char* p = origin.ptr<unsigned char>(i);
			for (int j = 0; j < origin.cols; ++j)
			{
				angleData[i + (nLength - origin.cols) / 2] += p[j];
			}
		}
		return;
	}
	else if (angle == 90) {
		for (int i = 0; i < origin.cols; ++i) {
			for (int j = 0; j < origin.rows; ++j)
			{
				angleData[i + (nLength - origin.cols) / 2] += origin.at<unsigned char>(j, i);
			}
		}
		return;
	}
	//Because the projections of angle x and angle 180-x are Symmetric, so they are processed simultaneously.
	//projection begins in middle of the projection lines.And changes to both sides simultaneously.
	//In each specific projection line, the process begins in the middle of the line,and goes to both endpoint simultaneously.
	double* angleData2 = projectionData.ptr<double>(180 - angle);
	double angleConv = angle * CV_PI / 180;
	double perX = cos(angleConv);
	double perY = sin(angleConv);
	double perOriY = perX;;
	double perOriX = -perY;
	double oriY = perOriY / 2;
	double oriX1 = -perOriX / 2;
	double oriX2 = perOriX / 2;   //negative 
	for (int i = 0; i < nLength / 2; ++i) {
		for (int j = 0; j < nLength / 2; ++j) {
			//projection of angle aimed.

			angleData[nLength / 2 - 1 - i] += find(oriX1 + perX * j, oriY + perY * j, origin);
			angleData[nLength / 2 - 1 - i] += find(oriX2 - perX * j, oriY - perY * j, origin);
			angleData[nLength / 2 + i] += find(-(oriX1 + perX * j), -(oriY + perY * j), origin);
			angleData[nLength / 2 + i] += find(-(oriX2 - perX * j), -(oriY - perY * j), origin);


			//projection of angle of (180-angle).
			angleData2[nLength / 2 + i] += find(-(oriX1 + perX * j), oriY + perY * j, origin);
			angleData2[nLength / 2 + i] += find(-(oriX2 - perX * j), oriY - perY * j, origin);
			angleData2[nLength / 2 - 1 - i] += find(oriX1 + perX * j, -(oriY + perY * j), origin);
			angleData2[nLength / 2 - 1 - i] += find(oriX2 - perX * j, -(oriY - perY * j), origin);
		}
		//The beginning of line is changing while the line changes.
		oriY += perOriY;
		oriX1 += perOriX;
		oriX2 += perOriX;
	}
}

//图像显示 
void outputOfProjection(Mat projectionData)
{
	Mat output;
	normalize(projectionData, output, 0, 255, NORM_MINMAX);
	imwrite("projection.bmp", output);

	normalize(projectionData, output, 0, 1, NORM_MINMAX);
	namedWindow("projection", WINDOW_AUTOSIZE);
	imshow("projection", output);
	waitKey(0);
}

void outputOfResult(Mat result)
{
	Mat output;

	//1.0/50 is a empirical numb.
	result.convertTo(output, CV_8UC1, 1.0 / 50);
	namedWindow("FBP", WINDOW_AUTOSIZE);
	imwrite("result.bmp", output);
	imshow("FBP", output);
	waitKey(0);
}
