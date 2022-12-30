import chardet

def main():
    data = \
    b'\x16\x03\x03\x00H\x02\x00\x00D\x03\x03c\xae\xca\xea\x9c0\x17\xf2\x1b\xdf\xbd\xb2\x97\xc5WRle\xa0\x91}O*\xb2DOWNGRD\x01\x00\xc0/\x00\x00\x1c\x00\x17\x00\x00\xff\x01\x00\x01\x00\x00\x0b\x00\x02\x01\x00\x00#\x00\x00\x00\x10\x00\x05\x00\x03\x02h2\x16\x03\x03\x0b\xe2\x0b\x00\x0b\xde\x00\x0b\xdb\x00\x06\xe70\x82\x06\xe30\x82\x05\xcb\xa0\x03\x02\x01\x02\x02\x10\x06\xc8\x03s\xb9\x06C\xf6\x1e\xa1`\xe2\xbe}\x03\x000\r\x06\t*\x86H\x86\xf7\r\x01\x01\x0b\x05\x000O1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x150\x13\x06\x03U\x04\n\x13\x0cDigiCert Inc1)0\'\x06\x03U\x04\x03\x13 DigiCert TLS RSA SHA256 2020 CA10\x1e\x17\r221025000000Z\x17\r231125235959Z0z1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x130\x11\x06\x03U\x04\x08\x13\nCalifornia1\x160\x14\x06\x03U\x04\x07\x13\rMountain View1\x1c0\x1a\x06\x03U\x04\n\x13\x13Mozilla Corporation1 0\x1e\x06\x03U\x04\x03\x0c\x17*.telemetry.mozilla.org0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xa5 I\xb0\xa9\xbf6\x9b\xf8\xca|\x85\xde\xd7\x87K_\xbe\x0b\xab\x7f\xb2m\x97\xe9\xbb\xc434N\xaf\x8c\xe4}Y\r\x8c\xd9U\x7f\xe7\xf8\x14zE_\xca\x18\xef\x10 \xdf\x1aB\xdf8?\xd8\xd8\x83h\x1d\xcbI~\xfb\xa2Y4\xc1Z\xda\x8f\x13\xcc\x8cX\xe8\xab\xaa-!\x03\x82\xe7|\x83"\xb4\xa7\xfcp#\xc3\x81\x8ba\x04!\n(\xed\xf7\x0cmf)\xf7\x07\xfaG\xc02\xa4\xc8\xde\xf7,\xcd\x10\x9eUT\x0e\x0e\xaeu\x00\xe6\xb8\xb1\xe1tx\x1eL\xcd\\\xf9\x93\x1f\xaf\x8du\xad)\xf0gC4\x0e*\xd3\xa3\x01\nvE{,\x8ei\xb7\x86\x89\x1a\xbf\xf2\x19\xfdz\xb7\xeb\x16v\xed1I\xf3-\xf6Tc\xfdR\xef\x13\xd1\xa2\x8d\xad\xb8\xf3x*\x0b\xbaut\xa9\x92\xf8\xf8D.\n\xf0\x84\xb8\x9a\xd6\xe2\xba=\x84\x97\xb2\xac\xe5r \xc1\xf7|\xb9\xc6\xa2\x15\xfe+e1\x92\x8d\x81\'\xccd2Ev\xd7~\xd1r\x9c*\xdb\x97\x8e.\xd0Q\xf4#\x8b\x02\x03\x01\x00\x01\xa3\x82\x03\x8e0\x82\x03\x8a0\x1f\x06\x03U\x1d#\x04\x180\x16\x80\x14\xb7k\xa2\xea\xa8\xaa\x84\x8cy\xea\xb4\xda\x0f\x98\xb2\xc5\x95v\xb9\xf40\x1d\x06\x03U\x1d\x0e\x04\x16\x04\x14\xf4j\x8e\x80\xe9\xf9\x11eD\x1f\xb1\x89\xc1Q\x1f\xb4\xa1j\xdb\xbf09\x06\x03U\x1d\x11\x04200\x82\x17*.telemetry.mozilla.org\x82\x15telemetry.mozilla.org0\x0e\x06\x03U\x1d\x0f\x01\x01\xff\x04\x04\x03\x02\x05\xa00\x1d\x06\x03U\x1d%\x04\x160\x14\x06\x08+\x06\x01\x05\x05\x07\x03\x01\x06\x08+\x06\x01\x05\x05\x07\x03\x020\x81\x8f\x06\x03U\x1d\x1f\x04\x81\x870\x81\x840@\xa0>\xa0<\x86:http://crl3.digicert.com/DigiCertTLSRSASHA2562020CA1-4.crl0@\xa0>\xa0<\x86:http://crl4.digicert.com/DigiCertTLSRSASHA2562020CA1-4.crl0>\x06\x03U\x1d \x0470503\x06\x06g\x81\x0c\x01\x02\x020)0\'\x06\x08+\x06\x01\x05\x05\x07\x02\x01\x16\x1bhttp://www.digicert.com/CPS0\x7f\x06\x08+\x06\x01\x05\x05\x07\x01\x01\x04s0q0$\x06\x08+\x06\x01\x05\x05\x070\x01\x86\x18http://ocsp.digicert.com0I\x06\x08+\x06\x01\x05\x05\x070\x02\x86=http://cacerts.digicert.com/DigiCertTLSRSASHA2562020CA1-1.crt0\t\x06\x03U\x1d\x13\x04\x020\x000\x82\x01~\x06\n+\x06\x01\x04\x01\xd6y\x02\x04\x02\x04\x82\x01n\x04\x82\x01j\x01h\x00v\x00\xe8>\xd0\xda>\xf5\x0652\xe7W(\xbc\x89k\xc9\x03\xd3\xcb\xd1\x11k\xec\xebi\xe1w}m\x06\xbdn\x00\x00\x01\x84\x10;@\xa6\x00\x00\x04\x03\x00G0E\x02!\x00\xaf\x07}\xaf1xH\xc1\xa0\xcd\xae.\x1c\xb6\xdcW\xf80\xa2\xa5Vx\xfd>\x12\xfb\x93g\x89\xd9\xe9\xc1\x02 u\x96\xc8\x1a\rMQ\x19\xa1\xa5\x88Y;K(\xe1\xd5\x92D\xa70\x110t\xe1J\xfb\xd4Y-G\xb4\x00u\x00\xb7>\xfb$\xdf\x9cM\xbau\xf29\xc5\xbaX\xf4l]\xfcB\xcfz\x9f5\xc4\x9e\x1d\t\x81%\xed\xb4\x99\x00\x00\x01\x84\x10;@\xa2\x00\x00\x04\x03\x00F0D\x02 \x01\xec\x07z5\xea\x1bv:\x9b\xd7\x15\xe1Wn\xdd=\xee\xe0\xddm\xa7t\xe6\xbbjs.\x80\xfd\xe3l\x02 Y^\x9bs\xc0M\xfaB\x05\xc2\x8cc\x82\xc5\xddA\xb1\xe5\x08\xebs\x9e\x9d%\xc6\xb6\x9do\xe4j\x11\xf1\x00w\x00\xad\xf7\xbe\xfa|\xff\x10\xc8\x8b\x9d=\x9c\x1e>\x18j\xb4g)]\xcf\xb1\x0c$\xca\x85\x864\xeb\xdc\x82\x8a\x00\x00\x01\x84\x10;@\xe6\x00\x00\x04\x03\x00H0F\x02!\x00\xb1*\xd1\x82w($O2\xcdx\xe6\xb6b\'\xa9_\x9e\x18\xff\xac\xe6\xe00\xe6@\x01\x06\xf9Zh\x8f\x02!\x00\xaa\xbb\x96\x8bo\xdb\xe4N\x9d\x7f\xcf\x93\x84\xde\x1fE\x91\xfcNv\xae\xb8w~=\t`\xbel\xf3\xae\xa70\r\x06\t*\x86H\x86\xf7\r\x01\x01\x0b\x05\x00\x03\x82\x01\x01\x00|(\x88\x99\x9b\xa4\xb9\xc1\x01\xcb\x125\t\xc6\x0b\xee%\xd1\xa8\x15\xf8K\xbf\xd2l\xd5\xe9\x8c\xe6\x99\x8e!\xfbk\xa1}\xc3\xdf\x15\x19\n\xde\xdcI\x11\xe4)\x1d1^\x96u\x04\xc5%&GVZh\x0ec\x86\x17\x99\xb0\x1f\xfb\x03\xaa\xf0\xb65~!\xf2\xc6\xe4\xb21\x98\x99\xc9N \xc6\xf9\x0f\x192\xce=\x01>\x14\x02\xcb\x18\xcb\xfe\xf0<k2\xdc_I\xa6\x11j\xb6\xcd\x85\xc2\xe1\xe1K\xdaj\xc6\x96k\xd5i\x11\xed\r\x87\x91\x84\xf4$\x03\x8c6\x18\x11gH\xa24\xb4\xc3\x06W\x19\xc4z\xf7\xd9\xbd\xef\x12L\x1cY{\xb7\xc2\xfe\x0f\xc2\xadph\xa9\xf6\x00N1\xedL\x89L\xfa\xa7+\r|Q\xf9\xab\xafdTY\xb6bP.i\xc32\xdd\xad^\x87\x16\x17y\xd8\xbfB\xd94\x7f\xae6\xc6\x8d\xfc)1\xe3z$\xc82<\x82\xe4F\xbe\xb2)\x15{l\xb8\xfd\xc0)\x1e\x02JHT\x96|\xfaVV\x85]+\xb2\x95\x13\xc7\xf9\xe6\xcd*9\xc8\x0b\x00\x04\xee0\x82\x04\xea0\x82\x03\xd2\xa0\x03\x02\x01\x02\x02\x10\n5\x08\xd5\\)+\x01}\xf8\xade\xc0\x0f\xf7\xe40\r\x06\t*\x86H\x86\xf7\r\x01\x01\x0b\x05\x000a1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x150\x13\x06\x03U\x04\n\x13\x0cDigiCert Inc1\x190\x17\x06\x03U\x04\x0b\x13\x10www.digicert.com1 0\x1e\x06\x03U\x04\x03\x13\x17DigiCert Global Root CA0\x1e\x17\r200924000000Z\x17\r300923235959Z0O1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x150\x13\x06\x03U\x04\n\x13\x0cDigiCert Inc1)0\'\x06\x03U\x04\x03\x13 DigiCert TLS RSA SHA256 2020 CA10\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xc1K\xb3eGp\xbc\xddOX\xdb\xec\x9c\xed\xc3f\xe5\x1f1\x13T\xadJfF\x1f,\n\xecd\x07\xe5.\xdc\xdc\xb9\n \xed\xdf\xe3\xc4\xd0\x9e\x9a\xa9z\x1d\x82\x88\xe5\x11V\xdb\x1e\x9fX\xc2Q\xe7,4\r.\xd2\x92\xe1V\xcb\xf1y_\xb3\xbb\x87\xca%\x03{\x9aRAf\x10`OW\x13I\xf0\xe87g\x83\xdf\xe7\xd3KgL"Q\xa6\xdf\x0e\x99\x10\xedWQt&\xe2}\xc7\xcab.\x13\x1b\x7f#\x88%So\xc14X\x00\x8b\x84\xff\xf8\xbe\xa7XI"{\x96\xad\xa2\x88\x9b\x15\xbc\xa0|\xdf\xe9Q\xa8\xd5\xb0\xed7\xe26\xb4\x82Kb\xb5I\x9a\xec\xc7g\xd6\xe3>\xf5\xe3\xd6\x12^D\xf1\xbfqB}X\x84\x03\x80\xb1\x81\x01\xfa\xf9\xca2\xbb\xb4\x8e\'\x87\'\xc5+t\xd4\xa8\xd6\x97\xde\xc3d\xf9\xca\xceS\xa2V\xbcx\x17\x8eI\x03)\xae\xfbIO\xa4\x15\xb9\xce\xf2\\\x19Wmky\xa7+\xa2\' \x13\xb5\xd0=@\xd3!0\x07\x93\xea\x99\xf5\x02\x03\x01\x00\x01\xa3\x82\x01\xae0\x82\x01\xaa0\x1d\x06\x03U\x1d\x0e\x04\x16\x04\x14\xb7k\xa2\xea\xa8\xaa\x84\x8cy\xea\xb4\xda\x0f\x98\xb2\xc5\x95v\xb9\xf40\x1f\x06\x03U\x1d#\x04\x180\x16\x80\x14\x03\xdeP5V\xd1L\xbbf\xf0\xa3\xe2\x1b\x1b\xc3\x97\xb2=\xd1U0\x0e\x06\x03U\x1d\x0f\x01\x01\xff\x04\x04\x03\x02\x01\x860\x1d\x06\x03U\x1d%\x04\x160\x14\x06\x08+\x06\x01\x05\x05\x07\x03\x01\x06\x08+\x06\x01\x05\x05\x07\x03\x020\x12\x06\x03U\x1d\x13\x01\x01\xff\x04\x080\x06\x01\x01\xff\x02\x01\x000v\x06\x08+\x06\x01\x05\x05\x07\x01\x01\x04j0h0$\x06\x08+\x06\x01\x05\x05\x070\x01\x86\x18http://ocsp.digicert.com0@\x06\x08+\x06\x01\x05\x05\x070\x02\x864http://cacerts.digicert.com/DigiCertGlobalRootCA.crt0{\x06\x03U\x1d\x1f\x04t0r07\xa05\xa03\x861http://crl3.digicert.com/DigiCertGlobalRootCA.crl07\xa05\xa03\x861http://crl4.digicert.com/DigiCertGlobalRootCA.crl00\x06\x03U\x1d \x04)0\'0\x07\x06\x05g\x81\x0c\x01\x010\x08\x06\x06g\x81' \
    + b'\x0c\x01\x02\x010\x08\x06\x06g\x81\x0c\x01\x02\x020\x08\x06\x06g\x81\x0c\x01\x02\x030\r\x06\t*\x86H\x86\xf7\r\x01\x01\x0b\x05\x00\x03\x82\x01\x01\x00w\xab\xb7z\'=\xae\xbb\xf6\x7f\xe0ZV\xc9\x84\xaa\xca[q\x17\xdd"G\xfcN\x9f\xee\xd0\xc1\xa4\x04\xe1\xa3\xeb\xc5I\xc1\xfd\xd1\xc9\xdf\x8c\xaf\x94E,F*\xa3c9 \xf9\x9eJ$\x94A\xc8\xa9\xd9\xe2\x9cT\x05\x06\xcb\\\x1c\xbe\x00\x1b\x0f\xa8Z\xff\x19\xbbe\xc7\x16\xaf!V\xdda\x05\xc9\xe9\x8f\x98v\xdfk\x1b\xd0r\x0cP\xb90)z\xbf`Y\x10f\x13:-\xac\x15\x11l-#\x0c\x02>\x05;\xfe\xe5\xa1\x9c\xe2\x8a\xdb\x87\xd7J\xe8^\xe7H\x06\xeb\xab\x12\x9a\xf2\xaf\x84\xc3[\x83J\x99\x81\x83\xab\x00\xa1\xca\n<L\xa2%\x89*"\xa7\xa4\xf33L[\x8c.\x1a\x02\x97\x0f\x9d\x8fm-\x95\x08\xfbO\xda\xf1\x918%\xe1\x9cna\x18\x87j\xce\xb1\xbb\x000j\x9b\xb7\xaf\xda\xf1\xc5\x97\xfe\x8ax$\xaa\xea\x93\x80\xba3ez\xbc\xa1w\xe9\x7fi\x14\x0b\x00?w\x92\xb1M[s\x87\n\x13\xd0\x9c\xc8\xf2K9OR\x84I\xa6L\x90N\x1f\xf7\xb4\x16\x03\x03\x01,\x0c\x00\x01(\x03\x00\x1d t\x9fu\xf0oc\xaa\x07-\x8e\xdd\x9bv\xd2\x87\xe3\x1b\xbc\xce\xc6(\x7f\xb1\xb3\x19\xf5\xf1\xe1\x90\t\x13\x0c\x08\x04\x01\x00rI`K@\x8d\xc1\xbd\xc2\xadf\xd5\xad\x86\xc0\x9dl\x99/TE\x96T6\x0b{\xa7k\x98\xba\xa2+Re\xa8\xf6.\x18\xbd\x8cw\x17\x1d"R\x020*<\xfc\x13\xb5\xa4uU~E\xa2\xe1\xd8\x11~]\xd6\xab>\xea\xaa\xf8\x98i\x9b\xb3(,\xae^\xc1\xd9\xd5v51l\xd7\x99\xa0\xf1\x10\xb8\x89IR\x9d\x893\x08@\xc8\xe5Xlh\x10$\xb2\xfc(\xabT\xf8\xe4<\x7f-\xbf)\x17Dm*w\x17\x9d\xe4d\xa8\x12W\xa9\x7f\xad\xb6h&\x99i\xe0z\x8a*\xee\xb7\x18\\wXvN\x18\xe5\xf6l\x03C\xeb\xe5\x81s\xd5-l\xc5\xe5gF\xaa\xbbw7\xb6L\xbc\xd8@\xbc\xad^\x0c\xef,\x17\xe3V\x10\xec\x05\x01\xcd\xa5\xfb\x98$U\xf548\t\x8f\xbaH\xd4IL\xb9\x08\xe4\x95\x139)#\xa5\xd8\x9d(\x06\x9c\xf3\xd9\x83\xa0\xe1\x85\xcc\x9a1\xa4)\xabAf\xf4\xa1\x8c\xb7\x01*\x15]\xd4\x9c\xddm\xf97\xfd\x9aT\x12\xf5\x08\x98\xc9\xbb\xf0\x16\x03\x03\x00\x04\x0e\x00\x00\x00' \
    + b'\x16\x03\x03\x00\xef\x04\x00\x00\xeb\x00\x01\x89\xbf\x00\xe5\x02\xe6\xaf\xe2\x14\xd8V\x0fE\x06\xc6\x9c!Y\xe7H\xd5K\xa5\xd7\x1a\xa8\xd6\x80\xef\xad\x01L\x87\xc0\x19\xa6\x8c\xcf\x83Q\x08]\xd86\xee\xdb\xc5\x10\xb5\xca_D\x8eg"\xf0iy\n\x1d\xb0xCP\xed\x97\xc7\xb0\xbc\xa8\x05\x0er\x078\x08\xd5n\x8a\x16\xa0\xc0\xb7Tg\xf31\xc2\x91@\xaf\x8c\xeb\x9b\xf45\x07s\xf0>\x8bH@K\xca\xdc\x93\x9a\x86\xae\x88\xd6\x8aO,\xddW \x90\x82\xf0\x18-\xa6*Y\xc6z\x86\x0c\xff\xed\xb2\x89\xbeu`\x0b\x90\x0c\x8eeO&\x89c\x9c\x15\x103*\x13\xf3\xfd\xa4\xb1\xce\x999\xa2C\xb4I#y\xdevY\xf3\xa7\x89\xeb\xea6\xcd\x90\xeb\xa8\xe1\xd3i>\x88n0cP\xae\x1am(\x85\xd1\xf2Q\xe5\xa7\xd8\x9f\xe47\xc1\xa1\x85\x94\t\x17\x80\xe4\x1b\xe6\xc0\xed.\x9d\x14=3\x97\xdfe\xa5SYDd%\x9b\xd3\xfak\xbb\x8e\x14\x03\x03\x00\x01\x01\x16\x03\x03\x00(\x00\x00\x00\x00\x00\x00\x00\x00\xfc\x86^3nzT\xbd\x1d5\x17V\xcb\xbe \x7f\xc26\x94Q\x053\xc5"\x9d\xd4\xdd\xe2\xf7\xd2\x88:' \
    + b'\x17\x03\x03\x00F\x00\x00\x00\x00\x00\x00\x00\x01p\xbb\xc5\xf2O"\x03\xdb%\xb5\xed\x96\x19\xc6\xb74\xde\xe9\xe8}\x80\x13T\xbe,\xf0\xcf D\xec\x18U\xee\x9fX\xd3\x08\xde\xf0{\xf3\x9a\x8c1\xac\xb6aj\xd2\xc7;\xfa\xd6%yKi\xbd\xdb\x9c\xb1j' \
    + b'\x17\x03\x03\x00!\x00\x00\x00\x00\x00\x00\x00\x02Z\xc3\xe2J+J\xce~\xb2\xab\xca\xbb\x023\x87C.\xbf\x0c\x81\xf8\x86\xb5*\xaa' \
    + b'\x17\x03\x03\x01\xc5\x00\x00\x00\x00\x00\x00\x00\x03\x0csG.\x1a\xd0\xcew~#:\x83\xb8\xc5\x15\xc7\xc33\x88X\xbe\x95\x88\xe6\xee\xf9Y\xc2\xbbW\x01\x15\'\x0c\x8cg\xb1+1\xe7\xfe=\x90\xcd\x87"d\xc2\x07\x0e\x07\xa8\xf8\x85\x01\x00\x9d\xc8\xb4\x95\x979\x8b\xf1!\x15V\xc6\xc6^%\x9f\xf1\x98m52\xe1\x01\t\x91\x0c\xaaV\xe9\xb3\x8co\xc2\xc2}\x06\xfe\xbaf\xb6\x91\xc7\xbd\xa8W\xf5\xdd\xc4(\xb6tX\x91=\xb6\x9d\xd7\x97;\xda\xeao\xba\xd9\xef$i\xfe[\x9bl\xac\x12\xb2\xe9P\x9d`ON\xday;#\x1f\x1aB\xe5\xf2-\x8f\xe7)\xe5\xbcl\xdb4nd\xa6\x80\x15\xa9B\x1a\xf0?\xbe^\x86>fg\xc7);c\r\xa9s\xfa\xdea\x1bo\xe7_\xe5o\xb7l_\xff,75nwv\xe6\x86\xe6s\x1d[H\x82\xc3j\xdbi\x1eFil1$\xb9\xb1\xe5>\xb5p\xb1=u\xbb\\\xc8\x01\x96\xf1\\\xedq\xde\xd1\xc4\x84P\xf27\x0f\xb8\xac-sUO#\x0e\x91cTM\xdf\xae\xd8\xab@\xc2\r\x8c\xbb\x81\x8b"Z\xa9-\xc8x\x16i\xf6\xd9]\x8d\x94)\xefi\x82\x0e[\xfd\xd1fV\xf9\xf2\x0f \xd4\xdb-\x0feUz%\xaa$\xb7\xb0u\xabY[\x8dra\xafI\xf9\xab!\xfa\xa1\t\x1c\x8b\x84C@z\xd2\x9c\x1b\t\x97\x00\xd8\xcd\x82\x8c\x07\x12V\xf6\xc0\x03-\x92;I;fA\xd7eR\xe4\xa3\x90\xd4\xedH\xd3u\x01%7I\x9d\xe8\xc2\x17m\xb5\x93\xcdW\x1ek\xca\xdb\xebMJEN\xf0\x00\xae\x82?Z1\xb2*x\x9a\x05\xe5\xd7T\xe8\xae\xab\xe4\xd9FK\xdd\xe1\x84<\xd1J\xccj\xb8\xa2\xc8\xce \x03+k\x9cU_\x1cJ\r\xf0\xfd\x81\xb0\xed}(\xb0\xfd\x84`|\x9b\xc2\x14\xf9\x0e\x9d\xa6\x1e\xa7\xd5' \
    + b"\x17\x03\x03\x00)\x00\x00\x00\x00\x00\x00\x00\x04\x9f \xa2\xa8Q\x8f\xf8\xec\x96\xf8\x0bt\x9fV\x8d\xde'\xa8\x90\xaej\xda\x96\xd8i\x82g\xc6\x8a\x90\xe1\xdd_" \
    + b"\x17\x03\x03\x00)\x00\x00\x00\x00\x00\x00\x00\x05\x1c\x15\xf5\nj'\x80\xb2~\xc8\xbfF\xb3\x12|S \xaf\xaf\x16\xc5\xa8gG|\xd8s%f\xe8\xb3FA"

    encoding = chardet.detect(data)
    print(encoding)
    print(data.decode())


if __name__ == '__main__':
    main()
