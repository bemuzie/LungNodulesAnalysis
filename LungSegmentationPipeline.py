from nipype.pipeline.engine import Workflow, Node
from nipype.interfaces import ants
from nipype.interfaces import afni as afni
from nipype.interfaces import io as nio
import nipype.interfaces.utility as util
import os
import ants_extensions as ae
import sys
import subprocess

#BASE_DIR = sys.argv[1]
BASE_DIR = '/home/denest/Copy/LungRCC_experiment/nipype_test'



lowres = Node(afni.Resample(outputtype= 'NIFTI',
                            voxel_size= (2.,2.,2.),
                            in_file = os.path.join(BASE_DIR ,'20150615_143106ChestAbdomenHCTPARCHUFGL03101946s005a003.nii'),
                            resample_mode = 'Cu'),
              name='make_lowres')

mask_air = Node(ae.AntsThreshold(threshold_low = -2000,
                                 threshold_high = -600),
                name='mask_air')
mask_body = Node(ae.AntsThreshold(threshold_low = -600,
                                 threshold_high = 3000),
                name='mask_body')

cut_largest = Node(ae.AntsGetLargestComponent(),
                   name= 'cut_largest')
fill_holes =  Node(ae.AntsFillHoles(),
                   name= 'fill_holes')

highres = Node(afni.Resample(outputtype= 'NIFTI',
                            voxel_size= (0.7,0.7,0.5),
                             resample_mode = 'Cu'),
              name='make_highres')


segflow = Workflow(name='segmentation_flow')
segflow.base_dir = os.path.abspath(BASE_DIR)
segflow.connect([
                    (lowres,mask_air,[('out_file','input_volume')]),
                    (mask_air,highres,[('output_volume','in_file')]),
                ])



# Datasink
datasink = Node(nio.DataSink(base_directory=BASE_DIR,
                             container='temp_folder'),
                name="datasink")

# Use the following DataSink output substitutions
substitutions = [('_subject_id', ''),
                 ('_session_id_', '')]
datasink.inputs.substitutions = substitutions

# Connect SelectFiles and DataSink to the workflow

#segflow.write_graph()
segflow.run()