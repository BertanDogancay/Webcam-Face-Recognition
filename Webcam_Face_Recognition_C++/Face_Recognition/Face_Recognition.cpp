#include <iostream>
#include <stdlib.h>
#include <stdio.h>

#include <opencv2\objdetect\objdetect.hpp>
#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2\highgui\highgui.hpp>
#include "opencv2\core.hpp"
#include <opencv2\core\core.hpp>
#include <opencv2\opencv.hpp>
#include <opencv2/face.hpp>

#include "FaceRec.h"

#include <fstream>
#include <sstream>

using namespace std;
using namespace cv;
using namespace cv::face;

static size_t my_write(void* buffer, size_t size, size_t nmemb, void* param)
{
	std::string& text = *static_cast<std::string*>(param);
	size_t totalsize = size * nmemb;
	text.append(static_cast<char*>(buffer), totalsize);
	return totalsize;
}

int main()
{
	int choice;
	cout << "1. Recognise Face\n";
	cout << "2. Add Face\n";
	cout << "Choose One: ";
	cin >> choice;

	switch (choice)
	{
	case 1:
		FaceRecognition();
		break;
	case 2:
		addFace();
		eigenFaceTrainer();
		break;
	default:
		return 0;
	}
	return 0;
}
