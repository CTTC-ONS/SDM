from __future__ import print_function

import grpc

import sliceable_transceiver_sdm_service_pb2
import sliceable_transceiver_sdm_service_pb2_grpc

def createTransceiver(slot_width, constellation, bandwidth, fec):
    transceiver=sliceable_transceiver_sdm_service_pb2.transceiver()
    transceiver.transceiverid="1"
    sliceobj=transceiver.slice.add()
    sliceobj.sliceid="1"
    counter = 1
    modes = ["LP01", "LP11a", "LP11b", "LP21a", "LP21b", "LP02"]
    channels = ["137", "129", "121", "113", "105", "97", "89", "81", "73", "65", "57", "49", "41", "33", "25", "17"]
    for i in range(0, len(modes)):
        for j in range(0, len(channels)):
            optical_channel = sliceobj.optical_channel.add()
            optical_channel.opticalchannelid = '%s' % counter
            optical_channel.coreid = '%s' % counter
            optical_channel.modeid = '%s' % modes[i]
            fs=optical_channel.frequency_slot
            fs.ncf='%s' % channels[j]
            fs.slot_width = slot_width
            counter += 1
    for i in range(1, len(channels) * len(modes) + 1):
        optical_signal  = sliceobj.optical_signal.add()
        optical_signal.opticalchannelid = '%s' % i
        optical_signal.constellation = constellation
        optical_signal.bandwidth = bandwidth
        optical_signal.fec = fec
        equalization = optical_signal.equalization
        equalization.equalizationid = 1
        equalization.mimo = "true"
        equalization.num_taps = "500"
    print(transceiver)
    return transceiver

def SetTransceiver(stub, transceiver):
    response = stub.SetTransceiver(transceiver)
    print("ConnectionService client received: " + str(response) )

#def listConnection(stub):
#    response = stub.ListConnection(google_dot_protobuf_dot_empty__pb2.Empty())
#    print("ConnectionService client received: " + str(response) )

def getBer(stub):
    sliceid=sliceable_transceiver_sdm_service_pb2.sliceid()
    sliceid.sliceid="1"
    responses = stub.GetBer(sliceid)
    for response in responses:
        print("Received Ber %s" % (response.ber) )

if __name__ == '__main__':
    transceiver = createTransceiver(2, 1, 12000000000, 1)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sliceable_transceiver_sdm_service_pb2_grpc.TransceiverServiceStub(channel)
        #SetTransceiver(stub, transceiver)
        #listConnection(stub)
        print (getBer(stub) )
