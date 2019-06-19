import json
from binding_transceiver import sliceable_transceiver_sdm
from pyangbind.lib.serialise import pybindIETFXMLEncoder
import pyangbind.lib.pybindJSON as pybindJSON
import requests

def createTransceiver(slot_width, constellation, bandwidth, fec):
  trans = sliceable_transceiver_sdm()
  
  trans.transceiver.transceiverid="1"
  sliceobj=trans.transceiver.slice.add("1")
  counter = 1
  modes = ["LP01", "LP11a", "LP11b", "LP21a", "LP21b", "LP02"]
  channels = ["137", "129", "121", "113", "105", "97", "89", "81", "73", "65", "57", "49", "41", "33", "25", "17"]
  for i in range(0, len(modes)):
      for j in range(0, len(channels)):
          optical_channel = sliceobj.optical_channel.add('%s' % counter)
          optical_channel.coreid = '%s' % counter
          optical_channel.modeid = '%s' % modes[i]
          fs=optical_channel.frequency_slot
          fs.ncf='%s' % channels[j]
          fs.slot_width = slot_width
          counter += 1
  for i in range(1, len(channels) * len(modes) + 1):
      optical_signal  = sliceobj.optical_signal.add('%s' % i)
      optical_signal.constellation = constellation
      optical_signal.bandwidth = bandwidth
      optical_signal.fec = fec
      equalization = optical_signal.equalization
      equalization.equalizationid = 1
      equalization.mimo = "true"
      equalization.num_taps = "500"
  print(pybindJSON.dumps(trans))
  return trans
if __name__ == '__main__':
    transceiver = createTransceiver(2, "qam16", 12000000000, "sd-fec")
    #requests.post('https://localhost:5000/config/transceiver/', json=pybindJSON.dumps(transceiver), verify=False)
    requests.get('https://localhost:5000/config/transceiver/slice/monitoring/ber/', verify=False)