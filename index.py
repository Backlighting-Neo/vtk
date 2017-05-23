import vtk
reader = vtk.vtkDICOMImageReader()

# 读入CT图像
reader.SetDirectoryName('../CT2/test/')
reader.Update()
srange  =  reader.GetOutput().GetScalarRange()
min  =  srange[0]
max  =  srange[1]

diff  =  max - min
slope  =   40000 / diff
inter  =   - slope * min
shift  =  inter / slope

shifter  =  vtk.vtkImageShiftScale()
shifter.SetShift(shift)
shifter.SetScale(slope)
shifter.SetOutputScalarTypeToUnsignedShort()
shifter.SetInputConnection(reader.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()
shifterSrange = shifter.GetOutput().GetScalarRange()
min2 = shifterSrange[0]
max2 = shifterSrange[1]

print  min,max,slope,inter,shift
print min2,max2


# print reader.GetOutput() # You should see that 3rd dimension is > 1 now
# print reader.GetOutput().GetScalarRange()


# Create the standard renderer, render window and interactor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Create transfer mapping scalar value to opacity
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0)
opacityTransferFunction.AddPoint(20000, 0)
opacityTransferFunction.AddPoint(30000, 0.8)
opacityTransferFunction.AddPoint(40000, 1)

# Create transfer mapping scalar value to color
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0, 0, 0, 0)
colorTransferFunction.AddRGBPoint(40000, 1, 1, 1)

# The property describes how the data will look
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data
compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(compositeFunction)
volumeMapper.SetInputConnection(shifter.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

ren.AddVolume(volume)
ren.SetBackground(1, 1, 1)
renWin.SetSize(600, 600)
renWin.Render()

def CheckAbort(obj, event):
    if obj.GetEventPending() != 0:
        obj.SetAbortRender(1)

renWin.AddObserver("AbortCheckEvent", CheckAbort)

iren.Initialize()
renWin.Render()
iren.Start()
