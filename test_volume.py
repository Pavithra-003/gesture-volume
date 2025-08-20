from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Get default speaker
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get current volume
current_vol = volume.GetMasterVolumeLevel()
print("Current Volume Level:", current_vol)

# Set volume (example: -20.0 is low, 0.0 is max)
volume.SetMasterVolumeLevel(-10.0, None)
print("Volume changed to -10.0")

# Set volume back to max (0.0)
volume.SetMasterVolumeLevel(0.0, None)
print("Volume changed to 0.0")
