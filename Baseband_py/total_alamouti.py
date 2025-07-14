import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,25,5)

########################
# 2x1 Alamouti BPSK
########################
ber_bpsk = []
for ebno_bpsk in db:
    each_bit_bpsk = 0
    each_error_bpsk = 0
    ratio_bpsk = 10**(ebno_bpsk/10)
    noise_sigma_bpsk = np.sqrt(1/(2*ratio_bpsk))
    while each_error_bpsk < 100:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        each_bit_bpsk += 2

        if b1 == 1: phase1 = 0
        else: phase1 = np.pi
        if b2 == 1: phase2 = 0
        else: phase2 = np.pi

        x1 = np.cos(phase1)
        x2 = np.cos(phase2)

        h_bpsk = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1_bpsk = h_bpsk[0,0]
        h2_bpsk = h_bpsk[1,0]

        n1_bpsk = noise_sigma_bpsk * (np.random.randn() + 1j * np.random.randn())
        n2_bpsk = noise_sigma_bpsk * (np.random.randn() + 1j * np.random.randn())

        r1_bpsk = h1_bpsk*x1 + h2_bpsk*x2 + n1_bpsk
        r2_bpsk = -h1_bpsk * np.conj(x2) + h2_bpsk * np.conj(x1) + n2_bpsk

        y1_bpsk = np.conj(h1_bpsk)*r1_bpsk + h2_bpsk*np.conj(r2_bpsk)
        y2_bpsk = np.conj(h2_bpsk)*r1_bpsk - h1_bpsk*np.conj(r2_bpsk)
        alpha_bpsk = np.abs(h1_bpsk)**2 + np.abs(h2_bpsk)**2
        x1_hat_bpsk = y1_bpsk / alpha_bpsk
        x2_hat_bpsk = y2_bpsk / alpha_bpsk

        b1_detect = int(x1_hat_bpsk.real > 0)
        b2_detect = int(x2_hat_bpsk.real > 0)
        each_error_bpsk += (b1 != b1_detect) + (b2 != b2_detect)
    ber_bpsk.append(each_error_bpsk / each_bit_bpsk)
    print(f"Eb/N0={ebno_bpsk} dB, BER={ber_bpsk[-1]:.5e}")


########################
# 2x1 Alamouti QPSK
########################
ber_qpsk = []
for ebno_qpsk in db:
    each_bit_qpsk = 0
    each_error_qpsk = 0
    ratio_qpsk = 10**(ebno_qpsk/10)
    noise_sigma_qpsk = np.sqrt(1/(4*ratio_qpsk))
    while each_error_qpsk < 100:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        each_bit_qpsk += 2
        # QPSK 매핑
        if b1 == 0 and b2 == 0:
            phase = np.pi/4
        elif b1 == 1 and b2 == 0:
            phase = 3*np.pi/4
        elif b1 == 1 and b2 == 1:
            phase = 5*np.pi/4
        elif b1 == 0 and b2 == 1:
            phase = 7*np.pi/4
        x1 = np.cos(phase) + 1j*np.sin(phase)

        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit_qpsk += 2
        if b3 == 0 and b4 == 0:
            phase = np.pi/4
        elif b3 == 1 and b4 == 0:
            phase = 3*np.pi/4
        elif b3 == 1 and b4 == 1:
            phase = 5*np.pi/4
        elif b3 == 0 and b4 == 1:
            phase = 7*np.pi/4
        x2 = np.cos(phase) + 1j*np.sin(phase)

        h_qpsk = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1_qpsk = h_qpsk[0,0]
        h2_qpsk = h_qpsk[1,0]

        n1_qpsk = noise_sigma_qpsk * (np.random.randn() + 1j * np.random.randn())
        n2_qpsk = noise_sigma_qpsk * (np.random.randn() + 1j * np.random.randn())

        r1_qpsk = h1_qpsk*x1 + h2_qpsk*x2 + n1_qpsk
        r2_qpsk = -h1_qpsk*np.conj(x2) + h2_qpsk*np.conj(x1) + n2_qpsk

        y1_qpsk = np.conj(h1_qpsk)*r1_qpsk + h2_qpsk*np.conj(r2_qpsk)
        y2_qpsk = np.conj(h2_qpsk)*r1_qpsk - h1_qpsk*np.conj(r2_qpsk)
        alpha_qpsk = np.abs(h1_qpsk)**2 + np.abs(h2_qpsk)**2
        x1_hat_qpsk = y1_qpsk / alpha_qpsk
        x2_hat_qpsk = y2_qpsk / alpha_qpsk

        theta1 = np.mod(np.angle(x1_hat_qpsk), 2*np.pi)
        theta2 = np.mod(np.angle(x2_hat_qpsk), 2*np.pi)
        # QPSK 복조
        if   0 <= theta1 < np.pi/2: b1_detect, b2_detect = 0, 0
        elif np.pi/2 <= theta1 < np.pi: b1_detect, b2_detect = 1, 0
        elif np.pi <= theta1 < 3*np.pi/2: b1_detect, b2_detect = 1, 1
        elif 3*np.pi/2 <= theta1 < 2*np.pi: b1_detect, b2_detect = 0, 1

        if   0 <= theta2 < np.pi/2: b3_detect, b4_detect = 0, 0
        elif np.pi/2 <= theta2 < np.pi: b3_detect, b4_detect = 1, 0
        elif np.pi <= theta2 < 3*np.pi/2: b3_detect, b4_detect = 1, 1
        elif 3*np.pi/2 <= theta2 < 2*np.pi: b3_detect, b4_detect = 0, 1

        each_error_qpsk += (b1 != b1_detect) + (b2 != b2_detect) + (b3 != b3_detect) + (b4 != b4_detect)
    ber_qpsk.append(each_error_qpsk / each_bit_qpsk)
    print(f"Eb/N0={ebno_qpsk} dB, BER={ber_qpsk[-1]:.5e}")

########################
# 2x1 Alamouti 8PSK
########################
ber_8psk = []
for ebno_8psk in db:
    each_bit_8psk = 0
    each_error_8psk = 0
    ratio_8psk = 10**(ebno_8psk/10)
    noise_sigma_8psk = np.sqrt(1 / (2 * ratio_8psk * 3))
    while each_error_8psk < 100:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        each_bit_8psk += 3

        # 매핑
        if   b1==0 and b2==0 and b3==0: phase1 = np.pi/8
        elif b1==0 and b2==0 and b3==1: phase1 = 3*np.pi/8
        elif b1==0 and b2==1 and b3==1: phase1 = 5*np.pi/8
        elif b1==0 and b2==1 and b3==0: phase1 = 7*np.pi/8
        elif b1==1 and b2==1 and b3==0: phase1 = 9*np.pi/8
        elif b1==1 and b2==1 and b3==1: phase1 = 11*np.pi/8
        elif b1==1 and b2==0 and b3==1: phase1 = 13*np.pi/8
        elif b1==1 and b2==0 and b3==0: phase1 = 15*np.pi/8
        s1 = np.cos(phase1) + 1j*np.sin(phase1)

        b4 = np.random.randint(0,2)
        b5 = np.random.randint(0,2)
        b6 = np.random.randint(0,2)
        each_bit_8psk += 3
        if   b4==0 and b5==0 and b6==0: phase2 = np.pi/8
        elif b4==0 and b5==0 and b6==1: phase2 = 3*np.pi/8
        elif b4==0 and b5==1 and b6==1: phase2 = 5*np.pi/8
        elif b4==0 and b5==1 and b6==0: phase2 = 7*np.pi/8
        elif b4==1 and b5==1 and b6==0: phase2 = 9*np.pi/8
        elif b4==1 and b5==1 and b6==1: phase2 = 11*np.pi/8
        elif b4==1 and b5==0 and b6==1: phase2 = 13*np.pi/8
        elif b4==1 and b5==0 and b6==0: phase2 = 15*np.pi/8
        s2 = np.cos(phase2) + 1j*np.sin(phase2)

        h_8psk = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1_8psk, h2_8psk = h_8psk[0,0], h_8psk[1,0]
        n1_8psk = noise_sigma_8psk * (np.random.randn() + 1j * np.random.randn())
        n2_8psk = noise_sigma_8psk * (np.random.randn() + 1j * np.random.randn())

        r1_8psk = h1_8psk*s1 + h2_8psk*s2 + n1_8psk
        r2_8psk = -h1_8psk*np.conj(s2) + h2_8psk*np.conj(s1) + n2_8psk

        y1_8psk = np.conj(h1_8psk)*r1_8psk + h2_8psk*np.conj(r2_8psk)
        y2_8psk = np.conj(h2_8psk)*r1_8psk - h1_8psk*np.conj(r2_8psk)
        alpha_8psk = np.abs(h1_8psk)**2 + np.abs(h2_8psk)**2
        s1_hat_8psk = y1_8psk / alpha_8psk
        s2_hat_8psk = y2_8psk / alpha_8psk

        theta1 = np.mod(np.angle(s1_hat_8psk), 2*np.pi)
        theta2 = np.mod(np.angle(s2_hat_8psk), 2*np.pi)

        # 복조 (구간)
        if 0 <= theta1 < np.pi/4: b1_detect, b2_detect, b3_detect = 0,0,0
        elif np.pi/4 <= theta1 < 2*np.pi/4: b1_detect, b2_detect, b3_detect = 0,0,1
        elif 2*np.pi/4 <= theta1 < 3*np.pi/4: b1_detect, b2_detect, b3_detect = 0,1,1
        elif 3*np.pi/4 <= theta1 < 4*np.pi/4: b1_detect, b2_detect, b3_detect = 0,1,0
        elif 4*np.pi/4 <= theta1 < 5*np.pi/4: b1_detect, b2_detect, b3_detect = 1,1,0
        elif 5*np.pi/4 <= theta1 < 6*np.pi/4: b1_detect, b2_detect, b3_detect = 1,1,1
        elif 6*np.pi/4 <= theta1 < 7*np.pi/4: b1_detect, b2_detect, b3_detect = 1,0,1
        elif 7*np.pi/4 <= theta1 < 2*np.pi: b1_detect, b2_detect, b3_detect = 1,0,0

        if 0 <= theta2 < np.pi/4: b4_detect, b5_detect, b6_detect = 0,0,0
        elif np.pi/4 <= theta2 < 2*np.pi/4: b4_detect, b5_detect, b6_detect = 0,0,1
        elif 2*np.pi/4 <= theta2 < 3*np.pi/4: b4_detect, b5_detect, b6_detect = 0,1,1
        elif 3*np.pi/4 <= theta2 < 4*np.pi/4: b4_detect, b5_detect, b6_detect = 0,1,0
        elif 4*np.pi/4 <= theta2 < 5*np.pi/4: b4_detect, b5_detect, b6_detect = 1,1,0
        elif 5*np.pi/4 <= theta2 < 6*np.pi/4: b4_detect, b5_detect, b6_detect = 1,1,1
        elif 6*np.pi/4 <= theta2 < 7*np.pi/4: b4_detect, b5_detect, b6_detect = 1,0,1
        elif 7*np.pi/4 <= theta2 < 2*np.pi: b4_detect, b5_detect, b6_detect = 1,0,0

        each_error_8psk += (b1 != b1_detect) + (b2 != b2_detect) + (b3 != b3_detect) \
            + (b4 != b4_detect) + (b5 != b5_detect) + (b6 != b6_detect)
    ber_8psk.append(each_error_8psk / each_bit_8psk)
    print(f"Eb/N0={ebno_8psk} dB, BER={ber_8psk[-1]:.5e}")


########################
# 2x1 Alamouti 16QAM
########################
ber_16qam = []
a_16qam = 1/np.sqrt(10)
for ebno_16qam in db:
    each_bit_16qam = 0
    each_error_16qam = 0
    ratio_16qam = 10**(ebno_16qam/10)
    noise_sigma_16qam = np.sqrt(1 / (2*4*ratio_16qam))
    while each_error_16qam < 100:
        
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit_16qam += 4
        gray_str1 = f"{b1}{b2}{b3}{b4}"
        if gray_str1 == '0000': s1 = a_16qam * (3+1j*3)
        elif gray_str1 == '0001': s1 = a_16qam * (3+1j)
        elif gray_str1 == '0011': s1 = a_16qam * (1+1j)
        elif gray_str1 == '0010': s1 = a_16qam * (1+1j*3)
        elif gray_str1 == '0110': s1 = a_16qam * (1-1j*3)
        elif gray_str1 == '0111': s1 = a_16qam * (1-1j)
        elif gray_str1 == '0101': s1 = a_16qam * (3-1j)
        elif gray_str1 == '0100': s1 = a_16qam * (3-1j*3)
        elif gray_str1 == '1100': s1 = a_16qam * (-3-1j*3)
        elif gray_str1 == '1101': s1 = a_16qam * (-3-1j)
        elif gray_str1 == '1111': s1 = a_16qam * (-1-1j)
        elif gray_str1 == '1110': s1 = a_16qam * (-1-1j*3)
        elif gray_str1 == '1010': s1 = a_16qam * (-1+1j*3)
        elif gray_str1 == '1011': s1 = a_16qam * (-1+1j)
        elif gray_str1 == '1001': s1 = a_16qam * (-3+1j)
        elif gray_str1 == '1000': s1 = a_16qam * (-3+1j*3)
        # symbol 2
        b5 = np.random.randint(0,2)
        b6 = np.random.randint(0,2)
        b7 = np.random.randint(0,2)
        b8 = np.random.randint(0,2)
        each_bit_16qam += 4
        gray_str2 = f"{b5}{b6}{b7}{b8}"
        if gray_str2 == '0000': s2 = a_16qam * (3+1j*3)
        elif gray_str2 == '0001': s2 = a_16qam * (3+1j)
        elif gray_str2 == '0011': s2 = a_16qam * (1+1j)
        elif gray_str2 == '0010': s2 = a_16qam * (1+1j*3)
        elif gray_str2 == '0110': s2 = a_16qam * (1-1j*3)
        elif gray_str2 == '0111': s2 = a_16qam * (1-1j)
        elif gray_str2 == '0101': s2 = a_16qam * (3-1j)
        elif gray_str2 == '0100': s2 = a_16qam * (3-1j*3)
        elif gray_str2 == '1100': s2 = a_16qam * (-3-1j*3)
        elif gray_str2 == '1101': s2 = a_16qam * (-3-1j)
        elif gray_str2 == '1111': s2 = a_16qam * (-1-1j)
        elif gray_str2 == '1110': s2 = a_16qam * (-1-1j*3)
        elif gray_str2 == '1010': s2 = a_16qam * (-1+1j*3)
        elif gray_str2 == '1011': s2 = a_16qam * (-1+1j)
        elif gray_str2 == '1001': s2 = a_16qam * (-3+1j)
        elif gray_str2 == '1000': s2 = a_16qam * (-3+1j*3)

        h_16qam = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1_16qam, h2_16qam = h_16qam[0,0], h_16qam[1,0]
        n1_16qam = noise_sigma_16qam * (np.random.randn() + 1j * np.random.randn())
        n2_16qam = noise_sigma_16qam * (np.random.randn() + 1j * np.random.randn())

        r1_16qam = h1_16qam*s1 + h2_16qam*s2 + n1_16qam
        r2_16qam = -h1_16qam*np.conj(s2) + h2_16qam*np.conj(s1) + n2_16qam

        y1_16qam = np.conj(h1_16qam)*r1_16qam + h2_16qam*np.conj(r2_16qam)
        y2_16qam = np.conj(h2_16qam)*r1_16qam - h1_16qam*np.conj(r2_16qam)
        alpha_16qam = np.abs(h1_16qam)**2 + np.abs(h2_16qam)**2
        s1_hat_16qam = y1_16qam / alpha_16qam
        s2_hat_16qam = y2_16qam / alpha_16qam

        def detect_16qam(value):
            if value >= 2*a_16qam:
                return 3
            elif 0 <= value < 2*a_16qam:
                return 1
            elif -2*a_16qam < value < 0:
                return -1
            else:
                return -3

        i1 = detect_16qam(s1_hat_16qam.real)
        q1 = detect_16qam(s1_hat_16qam.imag)
        i2 = detect_16qam(s2_hat_16qam.real)
        q2 = detect_16qam(s2_hat_16qam.imag)

        # 심볼1 복조
        if i1 == 3 and q1 == 3:         b1d, b2d, b3d, b4d = 0,0,0,0
        elif i1 == 3 and q1 == 1:       b1d, b2d, b3d, b4d = 0,0,0,1
        elif i1 == 1 and q1 == 1:       b1d, b2d, b3d, b4d = 0,0,1,1
        elif i1 == 1 and q1 == 3:       b1d, b2d, b3d, b4d = 0,0,1,0
        elif i1 == 1 and q1 == -3:      b1d, b2d, b3d, b4d = 0,1,1,0
        elif i1 == 1 and q1 == -1:      b1d, b2d, b3d, b4d = 0,1,1,1
        elif i1 == 3 and q1 == -1:      b1d, b2d, b3d, b4d = 0,1,0,1
        elif i1 == 3 and q1 == -3:      b1d, b2d, b3d, b4d = 0,1,0,0
        elif i1 == -3 and q1 == -3:     b1d, b2d, b3d, b4d = 1,1,0,0
        elif i1 == -3 and q1 == -1:     b1d, b2d, b3d, b4d = 1,1,0,1
        elif i1 == -1 and q1 == -1:     b1d, b2d, b3d, b4d = 1,1,1,1
        elif i1 == -1 and q1 == -3:     b1d, b2d, b3d, b4d = 1,1,1,0
        elif i1 == -1 and q1 == 3:      b1d, b2d, b3d, b4d = 1,0,1,0
        elif i1 == -1 and q1 == 1:      b1d, b2d, b3d, b4d = 1,0,1,1
        elif i1 == -3 and q1 == 1:      b1d, b2d, b3d, b4d = 1,0,0,1
        elif i1 == -3 and q1 == 3:      b1d, b2d, b3d, b4d = 1,0,0,0
        # 심볼2 복조
        if i2 == 3 and q2 == 3:         b5d, b6d, b7d, b8d = 0,0,0,0
        elif i2 == 3 and q2 == 1:       b5d, b6d, b7d, b8d = 0,0,0,1
        elif i2 == 1 and q2 == 1:       b5d, b6d, b7d, b8d = 0,0,1,1
        elif i2 == 1 and q2 == 3:       b5d, b6d, b7d, b8d = 0,0,1,0
        elif i2 == 1 and q2 == -3:      b5d, b6d, b7d, b8d = 0,1,1,0
        elif i2 == 1 and q2 == -1:      b5d, b6d, b7d, b8d = 0,1,1,1
        elif i2 == 3 and q2 == -1:      b5d, b6d, b7d, b8d = 0,1,0,1
        elif i2 == 3 and q2 == -3:      b5d, b6d, b7d, b8d = 0,1,0,0
        elif i2 == -3 and q2 == -3:     b5d, b6d, b7d, b8d = 1,1,0,0
        elif i2 == -3 and q2 == -1:     b5d, b6d, b7d, b8d = 1,1,0,1
        elif i2 == -1 and q2 == -1:     b5d, b6d, b7d, b8d = 1,1,1,1
        elif i2 == -1 and q2 == -3:     b5d, b6d, b7d, b8d = 1,1,1,0
        elif i2 == -1 and q2 == 3:      b5d, b6d, b7d, b8d = 1,0,1,0
        elif i2 == -1 and q2 == 1:      b5d, b6d, b7d, b8d = 1,0,1,1
        elif i2 == -3 and q2 == 1:      b5d, b6d, b7d, b8d = 1,0,0,1
        elif i2 == -3 and q2 == 3:      b5d, b6d, b7d, b8d = 1,0,0,0

        each_error_16qam += (b1 != b1d) + (b2 != b2d) + (b3 != b3d) + (b4 != b4d) \
            + (b5 != b5d) + (b6 != b6d) + (b7 != b7d) + (b8 != b8d)
    ber_16qam.append(each_error_16qam / each_bit_16qam)
    print(f"Eb/N0={ebno_16qam} dB, BER={ber_16qam[-1]:.5e}")


##############################
# Plotting
##############################
plt.figure(figsize=(9,6))
plt.semilogy(db, ber_bpsk, 'o-', label='2x1 Alamouti BPSK')
plt.semilogy(db, ber_qpsk, 's-', label='2x1 Alamouti QPSK')
plt.semilogy(db, ber_8psk, '^-', label='2x1 Alamouti 8PSK')
plt.semilogy(db, ber_16qam, 'x-', label='2x1 Alamouti 16QAM')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('Alamouti 2x1 - BPSK, QPSK, 8PSK, 16QAM')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()