#pragma once
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
using namespace cv;
using namespace std;

//滤波器类型
#define RLFILTER 1
#define SLFILTER 2

//获得不同角度的投影
void projection(unsigned char angle, Mat origin, Mat projectionData, int nLength);
//坐标转换
double find(double x, double y, Mat origin);

//滤波
double h_func(const int& i, int type);
double a_func(int i, double* p, int len);
void convolutionFilter(int angle, double* p, int len, int filType);

//反投影
void backprojection(int angle, double* data, Mat result, int lenData);

//示图
void outputOfProjection(Mat projection);
void outputOfResult(Mat result);
