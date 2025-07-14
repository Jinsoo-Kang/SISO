import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0, 45, 5)
ber = []

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
        h = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = h * s + noise_gaussian
        r_eq = r / h
        theta = np.mod(np.angle(r_eq), 2 * np.pi)

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

    ber.append(each_error / each_bit)

plt.semilogy(db, ber, 's--', label='8PSK (Rayleigh Fading + EQ)')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('8PSK BER over Rayleigh Fading Channel')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()