import cv2
import numpy as np 

def msg2bin(message):
  if type(message) == str:
    return ''.join([format(ord(i), '08b') for i in message])
  elif type(message) == bytes or type(message) == np.ndarray:
    return [ format(i, '08b') for i in message]
  elif type(message) == int or type(message) == np.uint8:
    return format(message, '08b')
  else:
    raise TypeError("Input type not supported")


def hideImage(image, message, output):
  img = cv2.imread(image)
  bytes_supported_for_msg = img.shape[0] * img.shape[1]
  message += "#####" #delimeter

  if len(message)>bytes_supported_for_msg:
    return("Error encountered insufficient bytes, need bigger image or less data!!")

  data_index = 0
  binary_msg = msg2bin(message)
  msg_length = len(binary_msg)

  for values in img:
    for pixel in values:
      r, g, b = msg2bin(pixel)
      if data_index<msg_length:
        pixel[0] = int(r[:-1] + binary_msg[data_index], 2)
        data_index += 1
      if data_index<msg_length:
        pixel[1] = int(g[:-1] + binary_msg[data_index], 2)
        data_index += 1
      if data_index<msg_length:
        pixel[2] = int(b[:-1] + binary_msg[data_index], 2)
        data_index += 1
      if data_index>=msg_length:
        break
  return cv2.imwrite(output, img)

def show(image):
  img = cv2.imread(image)
  binary_data = ''
  for values in img:
    for pixel in values:
      r, g, b = msg2bin(pixel)
      binary_data += r[-1]
      binary_data += g[-1]
      binary_data += b[-1]
    all_bytes = [ binary_data[i:i+8] for i in range(0, len(binary_data), 8) ]

    decoded_data = ''
    for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:] == "#####":
        break
  return decoded_data[:-5]

# To encode
# msg = 'Hello'
# print(msg2bin(msg))
# image = hideImage('a.jpg', msg)
# print(image)
# cv2.imwrite('btest.png', image)

# To decode
# print(show('btest.png'))


