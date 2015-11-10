from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec
from nipype.utils.filemanip import split_filename

import nibabel as nib
import numpy as np
import os

class LogicInputSpec(BaseInterfaceInputSpec):
    in_files = traits.List(mandatory=True,
                           exists=True,
                           desc="List of Nifti files to merge")

    operation_type = traits.Enum('and','or','not','xor'
                                 desc='everything below this value will be set to zero',
                                 mandatory=True)

class LogicOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc="thresholded volume")

class Logic(BaseInterface):
    input_spec = LogicInputSpec
    output_spec = LogicOutputSpec

    def _AND(self, vol1, vol2, label=1):
        if vol1.shape != vol2.shape:
            raise ValueError('input arrays should have smae shape.')
        output_vol = np.zeros(vol1.shape)
        output_vol[vol1==label and vol1==vol2] = label
        return output_vol

    def _OR(self, vol1, vol2, label=1):
        if vol1.shape != vol2.shape:
            raise ValueError('input arrays should have smae shape.')
        output_vol = np.zeros(vol1.shape)
        output_vol[vol1==label or vol2==label] = label
        return output_vol

    def _run_interface(self, runtime):
        niis = [nib.load(fn) for fn in self.input_spec.in_files]
        if operation_type=='and':
            logic_function=self._AND
        elif operation_type=='or':
            logic_function=self._OR

        output_vol=None

        for i in niis:
            if output_vol is not None:
                output_vol=logic_function(output_vol,i.get_data())
            else:
                output_vol= i.get_data()

        new_img = nb.Nifti1Image(output_vol, niis[0].get_affine(), niis[0].get_header())
        _, base, _ = split_filename(fname)
        nb.save(new_img, base + '_thresholded.nii')
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        fname = self.inputs.volume
        _, base, _ = split_filename(fname)
        outputs["thresholded_volume"] = os.path.abspath(base + '_thresholded.nii')
        return outputs