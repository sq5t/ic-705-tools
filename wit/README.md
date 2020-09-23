## wit - WiFi Image Transfer (for Icom IC-705).
'wit' is simple utility to send picture directly to radio over WiFi. IC-705 need to be accessible over IP with TCP port 60000 to work with this tool.

You can watch this software in action on my youtube channel https://youtu.be/BRDKWNSRsig

#### How it works?
In gimp or any other software create jpeg file with resolution 640x480 and disabled interlace. In script change IP (line 17) and change filename (line 22). After that run script, acknowledge transfer on radio and wait :)

#### Simple protocol specification.
Create tcp connection to radio to port 60000 and send command:

`\x01\x00\x00\x00\x00\x04\x00\x00\x00` + file size in hex (2 bytes)

Radio will answer with command ack:

`\x01\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00`

and receive ack:

`\x01\x02\x00\x00\x00\x02\x00\x00\x04\x00`

Now we can send header:

`\x01\x03\x00\x00\x04\x03\x00\x00\x01` + size of data + 1024 bytes of data

and wait for receive ack.

On last package of data we need to send:

`\x01\x03\x00\x00\x00\x74\x00\x00\x01` + size of data (2 bytes) + last part of data (<= 1024B).

------------

Yes, on test photo is my hedgehog :) 

No, this tool is not some kind of wit, it's only acronym :)
