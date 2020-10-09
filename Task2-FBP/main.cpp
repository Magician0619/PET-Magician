#include "FBP_source.h"

int main(int argc, char** argv) {

	//滤波类型
	int fileType = RLFILTER;

	//读取图像
	Mat  origin = imread("C:\\Users\\xinzhiqiang\\Desktop\\1111\\FBP_3\\FBP_3\\FBP_3\\SL_512.png", 0);

	if (origin.empty()) {

		printf("could not load image...\n");

		return -1;

	}
	//图像大小
	int nRow = origin.rows;
	int nCol = origin.cols;

	////取图像最长线作为不同角度的投影线条数
	int nLength = sqrt(nRow * nRow + nCol * nCol);

	//存放正投影数据
	Mat projectionData(180, nLength, CV_64FC1, Scalar(0));
	//存放反投影数据
	Mat result(nRow, nRow, CV_64FC1, Scalar(0));
	//cout<< nRow <<origin;


	////霍登变换 获得正投影
	for (unsigned char i = 0; i < 91; ++i) {
		projection(i, origin, projectionData, nLength);
	}

	//显示正投影图像
	outputOfProjection(projectionData);

	////滤波 反投影
	for (int i = 0; i < 180; ++i) {
		double* p = projectionData.ptr<double>(i);
		convolutionFilter(i, p, projectionData.cols, SLFILTER);
		backprojection(i, p, result, projectionData.cols);
	}

	////显示反投影图像
	outputOfResult(result);




	/*namedWindow("test_opencv_setup", 0);

	imshow("test_opencv_setup", origin);

	waitKey(0);*/

	return 0;

}

