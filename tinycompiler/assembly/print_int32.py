def print_int32(n):
    buffer = [ None ]*16 # output string buffer
    ecx = 0              # number of characters stored in the buffer

    eax = abs(n)
    while True:
        edx = eax %  10
        eax = eax // 10
        buffer[ecx] = chr(edx + ord('0'))
        ecx += 1
        if eax == 0: break

    if n<0:
        buffer[ecx] = '-'
        ecx += 1

    print(''.join(buffer[ecx-1::-1]))


print_int32(-729)
