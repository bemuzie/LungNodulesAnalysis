from nipype.interfaces.base import TraitedSpec, CommandLineInputSpec, CommandLine, File, traits, Interface
import os

class AntsThresholdInputSpec(CommandLineInputSpec):
        input_volume = File(desc = "Input volume",
                            exists = True,
                            mandatory = True,
                            argstr = "%s",
                            position = 2)
        output_volume = File(desc = "Input volume",
                            exists = False,
                            mandatory = False,
                            argstr = "%s",
                            position = 3,
                            name_template='%s_threshold.nii',
                            name_source='input_volume',
                            genfile=True)

        threshold_low = traits.Int(desc = "some parameter",
                                   position = 4,
                                   argstr = "%d")
        threshold_high = traits.Int(desc = "some parameter",
                                   position = 5,
                                   argstr = "%d")
        dimensions = traits.Int(desc = "some parameter",
                                position = 1,
                                argstr = "%d",
                                default_value=3,
                                usedefault = True)


class AntsThresholdOutputSpec(TraitedSpec):
        output_volume = File(desc = "Output volume",exists=True)


class AntsImageMathInputSpec(CommandLineInputSpec):
    input_volume = File(desc = "Input volume",
                            exists = True,
                            mandatory = True,
                            argstr = "%s",
                            position = 4)
    output_volume = File(desc = "Input volume",
                            exists = False,
                            mandatory = False,
                            argstr = "%s",
                            position = 2,
                            name_template='%s_imagemath.nii',
                            name_source='input_volume',
                            genfile=True)
    dimensions = traits.Int(desc = "some parameter",
                                position = 1,
                                argstr = "%d",
                                default_value=3,
                                usedefault = True)
    function = traits.Enum('GetLargestComponent','FillHoles',
                           decs = 'some desc',
                           position =3)

class AntsThreshold(CommandLine):
    input_spec = AntsThresholdInputSpec
    output_spec = AntsThresholdOutputSpec
    cmd = 'ThresholdImage'

class AntsGetLargestComponent(CommandLine):
    input_spec = AntsImageMathInputSpec
    input_spec.function = traits.Constant('GetLargestComponent',
                                          position=3)

    output_spec = AntsThresholdOutputSpec
    cmd = 'ImageMath'

class AntsFillHoles(CommandLine):
    input_spec = AntsImageMathInputSpec
    input_spec.function = traits.Constant('FillHoles',
                                          position=3)

    output_spec = AntsThresholdOutputSpec
    cmd = 'ImageMath'


if __name__=='__main__':
    thresholder = AntsThreshold(input_volume = '/home/denest/Copy/LungRCC_experiment/RAW/test.3dresample.nii',
                                output_volume = '/home/denest/Copy/LungRCC_experiment/RAW/test.3dresample_threshold.nii',
                                threshold_low = -2000,
                                threshold_high = -600)
    print thresholder.cmdline
    thresholder.run()