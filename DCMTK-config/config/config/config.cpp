// C++_Dicom_Sample.cpp : Defines the entry point for the console application.
//

/**/

#include "dcmtk/config/osconfig.h"
#include "dcmtk/dcmdata/dctk.h"
#include <iostream>


//bool ReadPatientName(DcmFileFormat& fileformat, std::string& filePath)
//{
//    OFCondition status = fileformat.loadFile(filePath.c_str());
//    if (!status.good())
//    {
//        std::cout << "Load Dimcom File Error: " << status.text() << std::endl;
//        return false;
//    }
//    OFString PatientName;
//    status = fileformat.getDataset()->findAndGetOFString(DCM_PatientName, PatientName);
//    if (status.good())
//    {
//        std::cout << "Get PatientName:" << PatientName << std::endl;
//    }
//    else
//    {
//        std::cout << "Get PatientName Error:" << status.text() << std::endl;
//        return false;
//    }
//    return true;
//}
//
//bool SavePatientName(DcmFileFormat& fileformat, std::string& filePath, const std::string& info)
//{
//    OFCondition status = fileformat.getDataset()->putAndInsertString(DCM_PatientName, info.c_str());
//    if (status.good())
//    {
//        std::cout << "Save PatientName:" << info.c_str() << std::endl;
//    }
//    else
//    {
//        std::cout << "Save PatientName Error: " << status.text() << std::endl;
//        return false;
//    }
//
//    status = fileformat.saveFile(filePath.c_str());
//    if (!status.good())
//    {
//        std::cout << "Save Dimcom File Error: " << status.text() << std::endl;
//        return false;
//    }
//    return true;
//}

int main()
{
    //DcmFileFormat dicomFileformat;

    //std::string dicomFile = "E:\\Learning\\C++\\Sample\\C++_Dicom_Sample\\x64\\Debug\\CT-MONO2-16-chest.dcm";

    //ReadPatientName(dicomFileformat, dicomFile);

    //SavePatientName(dicomFileformat, dicomFile, "John Snow");

    //ReadPatientName(dicomFileformat, dicomFile);

    //system("pause");

    return 0;
}