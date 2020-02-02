left = True
right = False
enable_flash = True
distance = 400

(left << 7) + (right << 6) + (enable_flash << 5) + ((distance & 7936) >> 8)

send_bytes = [
    ord('$'),
    (left << 7) + (right << 6) + (enable_flash << 5) + ((distance & 7936) >> 8),
    distance & 255,
    ord('\n')
]

print(bytearray(send_bytes))

