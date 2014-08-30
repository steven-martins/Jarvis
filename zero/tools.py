__author__ = 'Steven'

import msgpack


class Pack:
    @staticmethod
    def pack_cmd(name, args = [], header = {}):
        return msgpack.packb((header, name, args), use_bin_type=True)

    @staticmethod
    def pack_resp(body, header = {}):
        return msgpack.packb((header, body), use_bin_type=True)

    @staticmethod
    def unpack_cmd(raw):
        unpacked_msg = msgpack.unpackb(raw)
        header = {}
        name = None
        args = []
        try:
            (header, name, args) = unpacked_msg
        except Exception as e:
            print("Exception; %s" % str(e))
        return (header, name, args)

    @staticmethod
    def unpack_resp(raw):
        unpacked_msg = msgpack.unpackb(raw)
        header = {}
        body = None
        try:
            (header, body) = unpacked_msg
        except Exception as e:
            print("Exception; %s" % str(e))
        return header, body
