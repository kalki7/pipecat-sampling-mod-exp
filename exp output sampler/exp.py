from internal_proto import ProtobufFrameSerializer


bytes = b'\x12\x8b\x03\x08\xc0$\x12\x12AudioRawFrame#2207\x1a\xec\x02RIFFd\x01\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00@\x1f\x00\x00\x80>\x00\x00\x02\x00\x10\x00data@\x01\x00\x00b\x02\x0e\x01\xc7\xff{\x00\xed\x02)\x00\xfe\x05\x9f\x1d\x9c\x16\x97\x05L\x12\x08\x13)\x06K\xfc\xe3\xf3-\xf3\xf8\xf9\xb9\xf4%\xeb6\xf4\x8e\x01&\x03\x17\xfe?\xfe\xe5\x06\x12\tc\x00\x98\xf9O\xf8\xde\xfc`\xfb\xd9\xf1P\xf3\xb9\xfd\x86\x02\x1e\x02\xe6\x02\x8e\x06\xcd\x0c\xb8\x0e\xc4\x04\x8d\xfe\xff\x04\x13\x03\xcf\xf8\xa4\xf8]\xfcD\xfe\xe2\x00\xa0\xfe\x81\xfe\xbc\x08;\t\xcd\x00\xe5\x00P\x03\x98\x02\xc6\xfd\x1b\xf8\xff\xfaT\x02\x81\xff\xbe\xf9>\xfe4\x06z\x04\x03\xfd\x9d\xfd\xa8\x02y\x00u\xf9\xe0\xf6\xc4\xfal\xfd\xef\xf8P\xf4\x93\xf9j\xffZ\xfb\r\xfar\xfd\x96\x00\xdb\x01\xd9\xfd\x8b\xfd\x83\x02\xc5\x02\xc6\xfe9\xfd[\x00\x92\x03#\xff1\xffU\x02a\x02\xaa\x04\x92\x00\xfa\xffV\x02\x87\x05\xdc\x05\x0c\x10\xf2 \x0e\x0bj\rC\x1a\xae\x02\x81\x017\xfa\xf3\xf00\xf8\xf3\xf3[\xec\xb4\xf4\xb0\x01\xfc\xfd0\xfe\x97\x02\xc6\x02\xe6\x05o\xfek\xf45\xfa\xbd\xfd\xd9\xf4\xc2\xf2\xa9\xf7q\xfd\xd0\x02\xca\xff\x19\x01G\x0b\x18\x0ep\x05b\x00+\x03\xf8\x03\xa7\xfcH\xf4-\xfbo\x03\xce\x01w\xfc\x12\x01\r\x0f\x19\x0b\x83\x01\x00\x04\xbb\x07d\x04P\xfd\xab\xfa\x14\xfc?\xff\x13\xfc\x19\xfc\xd3\xff>\x03\xa4\nW\x01 \xc0>(\x01'

s = ProtobufFrameSerializer()

x = s.deserialize(bytes)

print(s)