import socket
from


sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sok.connect(('192.168.0.119', 8000))

input = '{asdassokpfkmlsdvkksvofkld kfvslmdfdvs vlfsdfedsvfkld vvfsdmklvflk}'

# Whatever Is your buffer size
splitLen = 20


for lines in range(0, len(input), splitLen):
    outputData = input[lines:lines+splitLen]
    sok.send(outputData)

sok.send('EOF')
