import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,11,1)
ber =[]

for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(2*ratio))

    while each_error < 100:
        b = np.random.randint(0,2)
        each_bit += 1
        if b == 1:
            phase = 0
        elif b == 0:
            phase = np.pi

        s = np.cos(phase)
        noise_gaussian = noise_sigma * np.random.randn()
        r = s + noise_gaussian

        b_detect = int(r > 0)
        each_error += int(b != b_detect)

    ber.append(each_error / each_bit)

plt.semilogy(db, ber, 's--', label='BPSK')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('BPSK BER CURVE')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()