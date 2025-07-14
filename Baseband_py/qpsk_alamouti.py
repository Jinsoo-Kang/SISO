import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,25,5)
ber = []

for ebno in db:
    each_bit = 0 
    each_error = 0 
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(4*ratio))  # QPSK

    while each_error < 500:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        each_bit += 2

        if b1 == 0 and b2 == 0:
            phase = np.pi/4
        elif b1 == 1 and b2 == 0:
            phase = 3*(np.pi/4)
        elif b1 == 1 and b2 == 1:
            phase = 5*(np.pi/4)
        elif b1 == 0 and b2 == 1:
            phase = 7*(np.pi/4)

        x1 = np.cos(phase) + 1j * np.sin(phase) #input 쪽 x1

        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit += 2

        if b3 == 0 and b4 == 0:
            phase = np.pi/4
        elif b3 == 1 and b4 == 0:
            phase = 3*(np.pi/4)
        elif b3 == 1 and b4 == 1:
            phase = 5*(np.pi/4)
        elif b3 == 0 and b4 == 1:
            phase = 7*(np.pi/4)

        x2 = np.cos(phase) + 1j * np.sin(phase) # input쪽 x2

        h = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1 = h[0,0]
        h2 = h[1,0]

        noise_gaussian1 = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        noise_gaussian2 = noise_sigma * (np.random.randn() + 1j * np.random.randn())

        r1 = h1*x1 + h2*x2 + noise_gaussian1
        r2 = -h1*np.conj(x2) + h2*np.conj(x1) + noise_gaussian2

        y1 = np.conj(h1)*r1 + np.conj(r2) * h2
        y2 = np.conj(h2)*r1 - np.conj(r2) * h1

        alpha = np.abs(h1)**2 + np.abs(h2)**2
        x1_hat = y1 / alpha
        x2_hat = y2 / alpha

        theta1 = np.mod(np.angle(x1_hat), 2*np.pi)
        theta2 = np.mod(np.angle(x2_hat), 2*np.pi)

        if   0 <= theta1 < np.pi/2:
            b1_detect, b2_detect = 0, 0
        elif np.pi/2 <= theta1 < np.pi:
            b1_detect, b2_detect = 1, 0
        elif np.pi <= theta1 < 3*np.pi/2:
            b1_detect, b2_detect = 1, 1
        elif 3*np.pi/2 <= theta1 < 2*np.pi:
            b1_detect, b2_detect = 0, 1

        if   0 <= theta2 < np.pi/2:
            b3_detect, b4_detect = 0, 0
        elif np.pi/2 <= theta2 < np.pi:
            b3_detect, b4_detect = 1, 0
        elif np.pi <= theta2 < 3*np.pi/2:
            b3_detect, b4_detect = 1, 1
        elif 3*np.pi/2 <= theta2 < 2*np.pi:
            b3_detect, b4_detect = 0, 1
        

        each_error += (b1 != b1_detect) + (b2 != b2_detect) + (b3 != b3_detect) + (b4 != b4_detect)
    ber.append(each_error / each_bit)
    print(f"Eb/N0={ebno} dB, BER={ber[-1]:.5e}")


plt.figure(figsize=(9,6))
plt.semilogy(db, ber, 'o-', label='Alamouti 2x1 QPSK')
plt.xlabel('Eb/N0')
plt.ylabel('BER')
plt.title('Alamouti 2x1 QPSK BER')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()


