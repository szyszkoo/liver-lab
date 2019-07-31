import pydicom
import nrrd
import math
import os
import csv
#from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('TkAgg') #Fix for MacOS framework bullsh*t
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from mpl_toolkits import mplot3d
from pyevtk.hl import gridToVTK
import pylab

# pathIN = "RT_ROIexample/Anonymized - 1219618/18-F[Fdg] Akwizycja Piersi/Body-Low Dose CT - 2"
pathIN = "./data"

# pathIN = "/Users/dborys/testdocker/PvS/101641/1.2.840.113704.1.111.2490.7469565.4/1.2.840.113704.1.111.3220.1361267740.8/"
# filename="/Users/dborys/testdocker/PvS/1030408/1.3.12.2.1107.5.1.4.11013.30000014061808114164000000002/1.3.46.670589.50.66692958234174.10596.1549279252073/1.3.46.670589.50.66692958234174.10596.1549279252057.dcm"
# pathIN="/Users/dborys/Documents/POLSL/_PROJEKTY/2019_SIEMENS_LIVER/Polsl_t1/"

rtFILE = './data/1_Case.RTSTRUCT.J_BRZUSZNA_P_wa.5.0.2019.03.11.22.05.49.698.73069853.dcm'
# rtFILE = "/Users/dborys/testdocker/PvS/101641/1.2.840.113704.1.111.2490.7469565.4/1.3.46.670589.50.66692958234174.21888.1554294295074.2/1.3.46.670589.50.66692958234174.21888.1554294295074.dcm"
# rtFILE="/Users/dborys/Documents/POLSL/_PROJEKTY/2019_SIEMENS_LIVER/Polsl_t1/1_Case.RTSTRUCT.J_BRZUSZNA_P_wa.5.0.2019.03.11.22.05.49.698.73069853.dcm"
paramsArray=[]
testTupleArray=[]

readdata, header = nrrd.read("./myROI_LIVER.nrrd")
liverDataCube = np.zeros((320, 260, 96), dtype=int)
i = 0

# todo: posortować slice'y 
# segmentacja - probowac rozne metody (naczynia, guzy, zdrowa tkanka)
# nie poprzez wartosci
for filename in sorted(os.listdir(pathIN)):
    if filename.endswith(".dcm"):
        dataset = pydicom.dcmread(os.path.join(pathIN, filename))

        if dataset.Modality == "MR" and dataset.SeriesDescription == 't1_vibe_e-dixon_tra_p4_bh_W':
            if 'PixelData' in dataset:
                testTupleArray.append((dataset.ImagePositionPatient, np.transpose(dataset.pixel_array)))
                rows = int(dataset.Rows)
                cols = int(dataset.Columns)
                # print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
                #    rows=rows, cols=cols, size=len(dataset.PixelData)))

                # liverDataCube[:,:,i] = np.transpose(dataset.pixel_array)
                # i = i+1
                if 'PixelSpacing' in dataset:
                    dcm_pixel_spacing = dataset.PixelSpacing
                #     print("Pixel spacing....:", dataset.PixelSpacing)
                # if 'ImagePositionPatient' in dataset:
                #     dcm_patient_position = dataset.ImagePositionPatient
                #     print("ImagePositionPatient....:", dataset.ImagePositionPatient)

                # paramsArray.append(dataset.ImagePositionPatient)

paramsArray = sorted(np.asarray(paramsArray), key = lambda x: x[2])
test = sorted(testTupleArray, key = lambda x: x[0][2])
paramsArray = [x[0] for x in test]

for index, singleTuple in enumerate(test):
    liverDataCube[:,:,index] = singleTuple[1]
# liverDataCube = [x[1] for x in test]
print(type(paramsArray))
paramsArray = np.asarray(paramsArray)
# nrrd.write('myTestLiverCube2.nrrd', liverDataCube)

rt_file = pydicom.read_file(rtFILE, force=True)
dcm_size = [rows, cols]
#ds.dir("contour")['ROIContourSequence']
contours = rt_file.ROIContourSequence


dicom_RT_seq=rt_file.StructureSetROISequence
for structure in dicom_RT_seq:
    #print structure
    print("Structure name: " + str(structure.ROIName))
    print(structure.ROINumber)
    roi_ref_id = int(structure.ROINumber)
    for current_roi in contours:
        if int(current_roi.ReferencedROINumber) == roi_ref_id:
            # print "ReferencedROINumber: " + str(roi_ref_id)
            # print(len(current_roi.ContourSequence))
            # Create empty 3d array
            roi_mask = np.zeros((int(dcm_size[1]), int(dcm_size[0]), len(paramsArray)), dtype=bool)
            print(roi_mask.shape)

            for ctr in current_roi.ContourSequence:
                ctr_data = ctr.ContourData
                # print(ctr_data)
                # Reshape data
                ctr_data_mtx = np.reshape(ctr_data, (-1, 3))
                #print ctr_data_mtx.shape
                # Get last column - Z patient location
                z_location = ctr_data_mtx[:, 2].copy()
                #print len(np.unique(z_location))

                # Check if Z location is unique
                if len(np.unique(z_location)) == 1:
                    #print np.unique(z_location)
                    # Find slice location in numpy 3d matrix using data from paramsArray
                    # itemindex = np.where(paramsArray[:,2] == z_location[0])

                    aa = np.around(paramsArray[:, 2], decimals=1)
                    aa = np.transpose(aa)
                    itemindex = np.where(aa == z_location[0])


                    iteindex = itemindex[0][0]
                    # print("Inserting contour to slice idx: " + str(int(itemindex[0])))
                    # Create clean mask
                    # temp_mask = np.zeros((int(dcm_size[0]), int(dcm_size[1])))
                    # Create contour from points
                    #polygon = [(x1,y1),(x2,y2),...] or [x1,y1,x2,y2,...]
                    start_point_x = float(paramsArray[iteindex, 0])
                    start_point_y = float(paramsArray[iteindex, 1])
                    print(start_point_y)
                    print(start_point_x)
                    # x_location = (ctr_data_mtx[:, 0:1].copy() - start_point_x)/float(dataset.PixelSpacing[0])
                    # y_location = (ctr_data_mtx[:, 1:2].copy() + start_point_y)/float(dataset.PixelSpacing[1])
                    x_location = (ctr_data_mtx[:, 0:1].copy() - start_point_x) / float(dcm_pixel_spacing[0])
                    y_location = (ctr_data_mtx[:, 1:2].copy() - start_point_y) / float(dcm_pixel_spacing[1])


                    #print str(x_location) #+ " " +str(y_location)
                    #astype(int)
                    polygon = np.concatenate((x_location, y_location), axis=1)
                    #print polygon.shape
                    polygon = polygon.astype(int)
                    #print polygon
                    width, height = int(dcm_size[0]), int(dcm_size[1])

                    poly_path = Path(polygon)

                    x, y = np.mgrid[:height, :width]
                    coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))  # coors.shape is (4000000,2)

                    mask = poly_path.contains_points(coors)
                    # print(mask)


                    # plt.imshow(mask.reshape(height, width))
                    # plt.show()

                    #img = Image.new('L', (int(dcm_size[0]), int(dcm_size[1])), 0)
                    #ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
                    #temp_mask = np.array(img)
                    #img.save(str(structure.ROIName) +str(int(itemindex[0]))+ 'polgon.jpg', 'JPEG')
                    #print temp_mask


                    # Insert mask on index with AND operation
                    roi_mask[:, :, int(iteindex)] = np.ma.mask_or(roi_mask[:, :, int(iteindex)], mask.reshape(height, width))
                # else:
                    # print "Skipping Contour ...."
            # Create ROI nrd file
            nrrd.write('myROI_' + structure.ROIName + '2.nrrd', roi_mask.astype(int)*255)



