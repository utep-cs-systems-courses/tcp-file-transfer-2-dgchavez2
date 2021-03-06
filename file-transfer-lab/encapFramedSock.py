import re

class EncapFramedSock:               # a facade
  def __init__(self, sockAddr):
    self.sock, self.addr = sockAddr
    self.rbuf = b""         # receive buffer
  def close(self):
    return self.sock.close()
  def send(self, payload, debugPrint=0):
    if debugPrint: print("framedSend: sending %d byte message" % len(payload))
    msg =  str(len(payload)).encode() + b':' + payload.encode() #removed b ':' .encode()
    while len(msg):
      nsent = self.sock.send(msg)
      msg = msg[nsent:]
  def receive(self, debugPrint=0):
    state = "getLength"
    msgLength = -1
    while True:
      if (state == "getLength"):
	#response.read().decode('utf-8') #added to see if it works now for re.match incompatibility
        match = re.match(b'([^:]+):(.*)', self.rbuf, re.DOTALL | re.MULTILINE) # look for colon and removed b '([
        if match:
          lengthStr, self.rbuf = match.groups()
          try: 
            msgLength = int(lengthStr)
          except:
            if len(self.rbuf):
              print("badly formed message length:", lengthStr)
              return None
          state = "getPayload"
      if state == "getPayload":
        if len(self.rbuf) >= msgLength:
         payload = self.rbuf[0:msgLength]
         self.rbuf = self.rbuf[msgLength:]
         return payload
      r = self.sock.recv(100)
      self.rbuf += r
      if len(r) == 0:
        if len(self.rbuf) != 0:
         print("FramedReceive: incomplete message. \n state=%s, length=%d, self.rbuf=%s" % (state, msgLength, self.rbuf))
        return None
      if debugPrint: print("FramedReceive: state=%s, length=%d, self.rbuf=%s" % (state, msgLength, self.rbuf))
