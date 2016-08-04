import thriftpy
from thriftpy.rpc import make_client
import os
from thriftpy.transport import TFramedTransportFactory


def getClient():
    wwfAPIpathname = os.path.join('thrift', 'wwf_api.thrift')
    wwfAPI_thrift = thriftpy.load(path=wwfAPIpathname, module_name='wwfAPI_thrift', include_dirs=['thrift'])
    tTransport = TFramedTransportFactory()
    client = make_client(wwfAPI_thrift.WwfApi, port=9090, trans_factory=tTransport)
    return client
