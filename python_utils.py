from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec
from nipype.utils.filemanip import split_filename

import nibabel as nib
import numpy as np
import os

class SimpleThresholdInputSpec(BaseInterfaceInputSpec):
    in_files = traits.List(mandatory=True,
                           exists=True,
                           desc="List of Nifti files to merge")

    operation_type = traits.Enum('and','or','not',
                                 desc='everything below this value will be set to zero',
                                 mandatory=True)

class SimpleThresholdOutputSpec(TraitedSpec):
    thresholded_volume = File(exists=True, desc="thresholded volume")


class SimpleThreshold(BaseInterface):
    input_spec = SimpleThresholdInputSpec
    output_spec = SimpleThresholdOutputSpec

    def _imgAND(self,vol1,vol2,label=[0,]):
        vol1_goodvalues = np.zeros


    def _run_interface(self, runtime):
        niis = [nib.load(fn) for fn in self.input_spec.in_files]
        if self.input_spec.operation_type == 'and':
            for


        data = np.array(img.get_data())

        active_map = data > self.inputs.threshold

        thresholded_map = np.zeros(data.shape)
        thresholded_map[active_map] = data[active_map]

        new_img = nb.Nifti1Image(thresholded_map, img.get_affine(), img.get_header())
        _, base, _ = split_filename(fname)
        nb.save(new_img, base + '_thresholded.nii')

        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        fname = self.inputs.volume
        _, base, _ = split_filename(fname)
        outputs["thresholded_volume"] = os.path.abspath(base + '_thresholded.nii')
        return outputs