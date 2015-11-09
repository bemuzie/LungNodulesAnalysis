import nibabel as nib
import numpy as np
import os
import sys



def load_nii(path_to_nii):
    img = nib.load(path_to_nii)
    hdr = img.get_header()
    vol = img.get_data()
    mrx = hdr.get_sform()
    return img, hdr,vol, mrx


def find_bounding_box(roi_image,label=1,padding=0):
    label_indices = np.where(roi_image==label)
    return zip(np.min(label_indices,1)-padding,
               np.max(label_indices,1)+padding)


def crop_with_coords(image,crop_coords)	:
	"""
	Croping coords should be a list of tupples
	[(x_from, x_to), (y_from, y_to)]
	"""
	return image[[slice(i[0],i[1]) for i in crop_coords]]

def save_nii(nii,output_path):
    nib.nifti1.save(nii, output_path)

def make_nii(vol,affine_matrix, header):
    return nib.Nifti1Image(vol, affine_matrix, header)

def crop_image_by_mask(path_to_image,path_to_mask,output_path,padding=0):
    img, hdr, vol, mrx  = load_nii(path_to_image)
    img_roi, hdr_roi, vol_roi, mrx_roi = load_nii(path_to_mask)
    print vol_roi.ndim
    if vol_roi.ndim ==4:
        vol_roi = vol_roi[...,0]
    coords = find_bounding_box(vol_roi,padding=padding)
    croped_image = crop_with_coords(vol, coords)
    output_nii = make_nii(croped_image, mrx, hdr)
    save_nii(output_nii, output_path)


if __name__=='__main__':
    IMAGE_PATH = sys.argv[1]
    ROI_PATH = sys.argv[2]
    OUTPUT_PATH = sys.argv[3]

    img, hdr, vol, mrx  = load_nii(IMAGE_PATH)
    img_roi, hdr_roi, vol_roi, mrx_roi = load_nii(ROI_PATH)

    vol_roi = vol_roi[...,0]


    coords = find_bounding_box(vol_roi)
    print coords
    croped_image = crop_with_coords(vol, coords)
    print croped_image.shape

    output_nii = nib.Nifti1Image(croped_image, mrx, hdr)


    nib.nifti1.save(output_nii, OUTPUT_PATH)