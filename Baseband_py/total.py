import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,11,1)
db_fad = np.arange(0,45,5)

# BPSK (AWGN) 
ber_bpsk = []
for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (2 * ratio))
    while each_error < 100:
        b = np.random.randint(0, 2)
        each_bit += 1
        phase = 0 if b == 1 else np.pi
        s = np.cos(phase)
        noise_gaussian = noise_sigma * np.random.randn()
        r = s + noise_gaussian
        b_detect = int(r > 0)
        each_error += int(b != b_detect)
    ber_bpsk.append(each_error / each_bit)

# BPSK (Fading)
ber_bpsk_fading = []
for ebno in db_fad:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (2 * ratio))
    while each_error < 100:
        b = np.random.randint(0, 2)
        each_bit += 1
        phase = 0 if b == 1 else np.pi
        s = np.cos(phase)
        h = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = h * s + noise_gaussian
        r_reverse = r / h
        b_detect = int(r_reverse.real > 0)
        each_error += int(b != b_detect)
    ber_bpsk_fading.append(each_error / each_bit)

# QPSK (AWGN)
ber_qpsk = []
for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (4 * ratio))
    while each_error < 100:
        b1 = np.random.randint(0, 2)
        b2 = np.random.randint(0, 2)
        each_bit += 2
        if b1 == 0 and b2 == 0:
            phase = np.pi / 4
        elif b1 == 1 and b2 == 0:
            phase = 3 * np.pi / 4
        elif b1 == 1 and b2 == 1:
            phase = 5 * np.pi / 4
        elif b1 == 0 and b2 == 1:
            phase = 7 * np.pi / 4
        s = np.cos(phase) + 1j * np.sin(phase)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = s + noise_gaussian
        theta = np.mod(np.angle(r), 2 * np.pi)
        if 0 <= theta < np.pi/2:
            b_detect = '00'
        elif np.pi/2 <= theta < np.pi:
            b_detect = '10'
        elif np.pi <= theta < 3*np.pi/2:
            b_detect = '11'
        elif 3*np.pi/2 <= theta < 2*np.pi:
            b_detect = '01'
        b1_detect, b2_detect = int(b_detect[0]), int(b_detect[1])
        each_error += (b1 != b1_detect) + (b2 != b2_detect)
    ber_qpsk.append(each_error / each_bit)

# QPSK (Fading)
ber_qpsk_fading = []
for ebno in db_fad:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (4 * ratio))
    while each_error < 100:
        b1 = np.random.randint(0, 2)
        b2 = np.random.randint(0, 2)
        each_bit += 2
        if b1 == 0 and b2 == 0:
            phase = np.pi / 4
        elif b1 == 1 and b2 == 0:
            phase = 3 * np.pi / 4
        elif b1 == 1 and b2 == 1:
            phase = 5 * np.pi / 4
        elif b1 == 0 and b2 == 1:
            phase = 7 * np.pi / 4
        s = np.cos(phase) + 1j * np.sin(phase)
        h = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = h * s + noise_gaussian
        r_reverse = r / h
        theta = np.mod(np.angle(r_reverse), 2 * np.pi)
        if 0 <= theta < np.pi/2:
            b_detect = '00'
        elif np.pi/2 <= theta < np.pi:
            b_detect = '10'
        elif np.pi <= theta < 3*np.pi/2:
            b_detect = '11'
        elif 3*np.pi/2 <= theta < 2*np.pi:
            b_detect = '01'
        b1_detect, b2_detect = int(b_detect[0]), int(b_detect[1])
        each_error += (b1 != b1_detect) + (b2 != b2_detect)
    ber_qpsk_fading.append(each_error / each_bit)

# 8PSK (AWGN) 
ber_8psk = []
for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (6 * ratio))
    while each_error < 100:
        b1 = np.random.randint(0, 2)
        b2 = np.random.randint(0, 2)
        b3 = np.random.randint(0, 2)
        each_bit += 3
        if b1 == 0 and b2 == 0 and b3 == 0:
            phase = np.pi / 8
        elif b1 == 0 and b2 == 0 and b3 == 1:
            phase = 3 * np.pi / 8
        elif b1 == 0 and b2 == 1 and b3 == 1:
            phase = 5 * np.pi / 8
        elif b1 == 0 and b2 == 1 and b3 == 0:
            phase = 7 * np.pi / 8
        elif b1 == 1 and b2 == 1 and b3 == 0:
            phase = 9 * np.pi / 8
        elif b1 == 1 and b2 == 1 and b3 == 1:
            phase = 11 * np.pi / 8
        elif b1 == 1 and b2 == 0 and b3 == 1:
            phase = 13 * np.pi / 8
        elif b1 == 1 and b2 == 0 and b3 == 0:
            phase = 15 * np.pi / 8
        s = np.cos(phase) + 1j * np.sin(phase)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = s + noise_gaussian
        theta = np.mod(np.angle(r), 2 * np.pi)
        if 0 <= theta < np.pi/4:
            b_detect = '000'
        elif np.pi/4 <= theta < np.pi/2:
            b_detect = '001'
        elif np.pi/2 <= theta < 3*np.pi/4:
            b_detect = '011'
        elif 3*np.pi/4 <= theta < np.pi:
            b_detect = '010'
        elif np.pi <= theta < 5*np.pi/4:
            b_detect = '110'
        elif 5*np.pi/4 <= theta < 3*np.pi/2:
            b_detect = '111'
        elif 3*np.pi/2 <= theta < 7*np.pi/4:
            b_detect = '101'
        elif 7*np.pi/4 <= theta < 2*np.pi:
            b_detect = '100'
        b1_detect, b2_detect, b3_detect = int(b_detect[0]), int(b_detect[1]), int(b_detect[2])
        each_error += (b1 != b1_detect) + (b2 != b2_detect) + (b3 != b3_detect)
    ber_8psk.append(each_error / each_bit)

# 8PSK (Fading)
ber_8psk_fading = []
for ebno in db_fad:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (6 * ratio))
    while each_error < 100:
        b1 = np.random.randint(0, 2)
        b2 = np.random.randint(0, 2)
        b3 = np.random.randint(0, 2)
        each_bit += 3
        if b1 == 0 and b2 == 0 and b3 == 0:
            phase = np.pi / 8
        elif b1 == 0 and b2 == 0 and b3 == 1:
            phase = 3 * np.pi / 8
        elif b1 == 0 and b2 == 1 and b3 == 1:
            phase = 5 * np.pi / 8
        elif b1 == 0 and b2 == 1 and b3 == 0:
            phase = 7 * np.pi / 8
        elif b1 == 1 and b2 == 1 and b3 == 0:
            phase = 9 * np.pi / 8
        elif b1 == 1 and b2 == 1 and b3 == 1:
            phase = 11 * np.pi / 8
        elif b1 == 1 and b2 == 0 and b3 == 1:
            phase = 13 * np.pi / 8
        elif b1 == 1 and b2 == 0 and b3 == 0:
            phase = 15 * np.pi / 8
        s = np.cos(phase) + 1j * np.sin(phase)
        h = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = h * s + noise_gaussian
        r_reverse = r / h
        theta = np.mod(np.angle(r_reverse), 2 * np.pi)
        if 0 <= theta < np.pi/4:
            b_detect = '000'
        elif np.pi/4 <= theta < np.pi/2:
            b_detect = '001'
        elif np.pi/2 <= theta < 3*np.pi/4:
            b_detect = '011'
        elif 3*np.pi/4 <= theta < np.pi:
            b_detect = '010'
        elif np.pi <= theta < 5*np.pi/4:
            b_detect = '110'
        elif 5*np.pi/4 <= theta < 3*np.pi/2:
            b_detect = '111'
        elif 3*np.pi/2 <= theta < 7*np.pi/4:
            b_detect = '101'
        elif 7*np.pi/4 <= theta < 2*np.pi:
            b_detect = '100'
        b1_detect, b2_detect, b3_detect = int(b_detect[0]), int(b_detect[1]), int(b_detect[2])
        each_error += (b1 != b1_detect) + (b2 != b2_detect) + (b3 != b3_detect)
    ber_8psk_fading.append(each_error / each_bit)

# 16_QAM_AWGN 채널
db_16_awgn = np.arange(0,13,1)
ber_16_awgn = []
a = 1 / np.sqrt(10) # a값 따로 빼주기 // 아래 코드는 정규화 안시킴

for ebno in db_16_awgn:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(2*4*ratio)) # m = 4

    while each_error < 1000:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit += 4

        
        gray_str= f"{b1}{b2}{b3}{b4}" # 그레이코드를 문자열로 생성

        if gray_str == '0000': # 16-QAM 매핑
            s = a * (3+1j*3)
        elif gray_str == '0001':
            s = a * (3+1j)
        elif gray_str == '0011':
            s = a * (1 + 1j)
        elif gray_str == '0010':
            s = a * (1 + 1j*3)
        elif gray_str == '0110':
            s = a * (1 - 1j*3)
        elif gray_str == '0111':
            s = a * (1 - 1j)
        elif gray_str == '0101':
            s = a * (3 - 1j)
        elif gray_str == '0100':
            s = a * (3 - 1j*3)
        elif gray_str == '1100':
            s = a * (-3 - 1j*3)
        elif gray_str == '1101':
            s = a * (-3 - 1j)
        elif gray_str == '1111':
            s = a * (-1 - 1j)
        elif gray_str == '1110':
            s = a * (-1 - 1j*3)
        elif gray_str == '1010':
            s = a * (-1 + 1j*3)
        elif gray_str == '1011':
            s = a * (-1 + 1j)
        elif gray_str == '1001':
            s = a * (-3 + 1j)
        elif gray_str == '1000':
            s = a * (-3 + 1j*3)
        
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = s + noise_gaussian

        def detect(value): # detect라는 함수를 정의 // 구간을 나누고 0~2까지 구간에서는 1로 return되도록, ㅣ2ㅣ보다 큰 경우에는 -3이 리턴 되도록
            if value >= 2:
                return 3
            elif 0<= value <2:
                return 1
            elif -2 < value < 0:
                return -1
            else:
                return -3
            
        i_detect = detect(r.real/a) # I 채널 쪽 detect 함수 사용 a 값 정규화 시켜야함
        q_detect = detect(r.imag/a) # Q 채널 쪽 detect 함수 사용 a 값 정규화

        if i_detect == 3 and q_detect == 3: # detect 함수를 사용해서 되돌려진 값에 따라서 다시 그레이 코드에 매칭시키기
            b1d, b2d, b3d, b4d = 0,0,0,0
        elif i_detect == 3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,0,1
        elif i_detect == 1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,1,1
        elif i_detect == 1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 0,0,1,0
        elif i_detect == 1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,1,0
        elif i_detect == 1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,1,1
        elif i_detect == 3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,0,1
        elif i_detect == 3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,0,0
        elif i_detect == -3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,0,0
        elif i_detect == -3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,0,1
        elif i_detect == -1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,1,1
        elif i_detect == -1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,1,0
        elif i_detect == -1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,1,0
        elif i_detect == -1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,1,1
        elif i_detect == -3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,0,1
        elif i_detect == -3 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,0,0

        each_error += (b1 != b1d) + (b2 != b2d) + (b3 != b3d) + (b4 != b4d)
    ber_16_awgn.append(each_error/each_bit)


db_16_fading = np.arange(0,45,5)
ber_16_fading = []
a = 1 / np.sqrt(10) # a값 따로 빼주기 // 아래 코드는 정규화 안시킴

for ebno in db_16_fading:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(2*4*ratio)) # m = 4

    while each_error < 1000:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit += 4

        
        gray_str= f"{b1}{b2}{b3}{b4}" # 그레이코드를 문자열로 생성

        if gray_str == '0000': # 16-QAM 매핑
            s = a * (3+1j*3)
        elif gray_str == '0001':
            s = a * (3+1j)
        elif gray_str == '0011':
            s = a * (1 + 1j)
        elif gray_str == '0010':
            s = a * (1 + 1j*3)
        elif gray_str == '0110':
            s = a * (1 - 1j*3)
        elif gray_str == '0111':
            s = a * (1 - 1j)
        elif gray_str == '0101':
            s = a * (3 - 1j)
        elif gray_str == '0100':
            s = a * (3 - 1j*3)
        elif gray_str == '1100':
            s = a * (-3 - 1j*3)
        elif gray_str == '1101':
            s = a * (-3 - 1j)
        elif gray_str == '1111':
            s = a * (-1 - 1j)
        elif gray_str == '1110':
            s = a * (-1 - 1j*3)
        elif gray_str == '1010':
            s = a * (-1 + 1j*3)
        elif gray_str == '1011':
            s = a * (-1 + 1j)
        elif gray_str == '1001':
            s = a * (-3 + 1j)
        elif gray_str == '1000':
            s = a * (-3 + 1j*3)
        
        h = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = h*s + noise_gaussian
        r_reverse = r / h


        def detect(value): # detect라는 함수를 정의 // 구간을 나누고 0~2까지 구간에서는 1로 return되도록, ㅣ2ㅣ보다 큰 경우에는 -3이 리턴 되도록
            if value >= 2:
                return 3
            elif 0<= value <2:
                return 1
            elif -2 < value < 0:
                return -1
            else:
                return -3
            
        i_detect = detect(r_reverse.real/a) # I 채널 쪽 detect 함수 사용 a 값 정규화 시켜야함
        q_detect = detect(r_reverse.imag/a) # Q 채널 쪽 detect 함수 사용 a 값 정규화

        if i_detect == 3 and q_detect == 3: # detect 함수를 사용해서 되돌려진 값에 따라서 다시 그레이 코드에 매칭시키기
            b1d, b2d, b3d, b4d = 0,0,0,0
        elif i_detect == 3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,0,1
        elif i_detect == 1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,1,1
        elif i_detect == 1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 0,0,1,0
        elif i_detect == 1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,1,0
        elif i_detect == 1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,1,1
        elif i_detect == 3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,0,1
        elif i_detect == 3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,0,0
        elif i_detect == -3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,0,0
        elif i_detect == -3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,0,1
        elif i_detect == -1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,1,1
        elif i_detect == -1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,1,0
        elif i_detect == -1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,1,0
        elif i_detect == -1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,1,1
        elif i_detect == -3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,0,1
        elif i_detect == -3 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,0,0

        each_error += (b1 != b1d) + (b2 != b2d) + (b3 != b3d) + (b4 != b4d)
    ber_16_fading.append(each_error/each_bit)

plt.figure(figsize=(9,6))
plt.semilogy(db,     ber_bpsk,       'o-',  label='BPSK (AWGN)')
plt.semilogy(db_fad, ber_bpsk_fading,'o--', label='BPSK (Fading)')
plt.semilogy(db,     ber_qpsk,       's-',  label='QPSK (AWGN)')
plt.semilogy(db_fad, ber_qpsk_fading,'s--', label='QPSK (Fading)')
plt.semilogy(db,     ber_8psk,       'd-',  label='8PSK (AWGN)')
plt.semilogy(db_fad, ber_8psk_fading,'d--', label='8PSK (Fading)')
plt.semilogy(db_16_awgn, ber_16_awgn, 'x-', label='16-QAM(awgn)')
plt.semilogy(db_16_fading, ber_16_fading, 'x--', label='16-QAM(Fading)')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('BPSK, QPSK, 8PSK (AWGN vs Rayleigh Fading)')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()