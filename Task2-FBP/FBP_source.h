#pragma once
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
using namespace cv;
using namespace std;

//�˲�������
#define RLFILTER 1
#define SLFILTER 2

//��ò�ͬ�Ƕȵ�ͶӰ
void projection(unsigned char angle, Mat origin, Mat projectionData, int nLength);
//����ת��
double find(double x, double y, Mat origin);

//�˲�
double h_func(const int& i, int type);
double a_func(int i, double* p, int len);
void convolutionFilter(int angle, double* p, int len, int filType);

//��ͶӰ
void backprojection(int angle, double* data, Mat result, int lenData);

//ʾͼ
void outputOfProjection(Mat projection);
void outputOfResult(Mat result);
