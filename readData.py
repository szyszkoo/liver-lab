import pydicom
import nrrd
import os
import numpy as np
from matplotlib.path import Path

pathIN = "./data"
rtFILE = './data/1_Case.RTSTRUCT.J_BRZUSZNA_P_wa.5.0.2019.03.11.22.05.49.698.73069853.dcm'

liverDataTuple = []
# TODO: Get rid of the hardcoded values below
liverDataCube = np.zeros((320, 260, 96), dtype=int)

for filename in sorted(os.listdir(pathIN)):
    if filename.endswith(".dcm"):
        dataset = pydicom.dcmread(os.path.join(pathIN, filename))

        if dataset.Modality == "MR" and dataset.SeriesDescription == 't1_vibe_e-dixon_tra_p4_bh_W':
            if 'PixelData' in dataset:
                liverDataTuple.append((dataset.ImagePositionPatient, np.transpose(dataset.pixel_array)))
                rows = int(dataset.Rows)
                cols = int(dataset.Columns)
              
                if 'PixelSpacing' in dataset:
                    dcm_pixel_spacing = dataset.PixelSpacing
              
liverDataSorted = sorted(liverDataTuple, key = lambda x: x[0][2])
patientPositionArray = np.asarray([x[0] for x in liverDataSorted])

for index, singleTuple in enumerate(liverDataSorted):
    liverDataCube[:,:,index] = singleTuple[1]

# TODO: uncomment the line below in order to save the liver data to the nrrd file
# nrrd.write('myTestLiverCube2.nrrd', liverDataCube)

# RT file (ROI)
rt_file = pydicom.read_file(rtFILE, force=True)
dcm_size = [rows, cols]
contours = rt_file.ROIContourSequence
dicom_RT_seq = rt_file.StructureSetROISequence

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
            roi_mask = np.zeros((int(dcm_size[1]), int(dcm_size[0]), len(patientPositionArray)), dtype=bool)
            print(roi_mask.shape)

            for ctr in current_roi.ContourSequence:
                ctr_data = ctr.ContourData
                ctr_data_mtx = np.reshape(ctr_data, (-1, 3))
                # Get last column - Z patient location
                z_location = ctr_data_mtx[:, 2].copy()

                # Check if Z location is unique
                if len(np.unique(z_location)) == 1:
                    # Find slice location in numpy 3d matrix using data from patientPositionArray
                    aa = np.around(patientPositionArray[:, 2], decimals=1)
                    aa = np.transpose(aa)
                    itemindex = np.where(aa == z_location[0])

                    iteindex = itemindex[0][0]

                    start_point_x = float(patientPositionArray[iteindex, 0])
                    start_point_y = float(patientPositionArray[iteindex, 1])

                    x_location = (ctr_data_mtx[:, 0:1].copy() - start_point_x) / float(dcm_pixel_spacing[0])
                    y_location = (ctr_data_mtx[:, 1:2].copy() - start_point_y) / float(dcm_pixel_spacing[1])

                    polygon = np.concatenate((x_location, y_location), axis=1)
                    polygon = polygon.astype(int)
                    width, height = int(dcm_size[0]), int(dcm_size[1])

                    poly_path = Path(polygon)

                    x, y = np.mgrid[:height, :width]
                    coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))

                    mask = poly_path.contains_points(coors)

                    # Insert mask on index with AND operation
                    roi_mask[:, :, int(iteindex)] = np.ma.mask_or(roi_mask[:, :, int(iteindex)], mask.reshape(height, width))
                
# TODO: Create ROI nrrd file (uncomment the line below)
# nrrd.write('myROI_' + structure.ROIName + '2.nrrd', roi_mask.astype(int)*255)
print(roi_mask.astype(int)*255)



