import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,25,5)
ber =[]

for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(2*ratio)) # 안테나 수만큼

    while each_error < 100:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        each_bit += 2

        if b1 == 1:
            phase1 = 0
        elif b1 == 0:
            phase1 = np.pi
        if b2 == 1:
            phase2 = 0
        elif b2 == 0:
            phase2 = np.pi

        x1 = np.cos(phase1)
        x2 = np.cos(phase2)
        x = np.array([[x1],[x2]])

        h = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1 = h[0,0]
        h2 = h[1,0]
       
        noise_gaussian1 = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        noise_gaussian2 = noise_sigma * (np.random.randn() + 1j * np.random.randn())

        
        r1 = h1*x1 + h2*x2 + noise_gaussian1
        r2 = -h1 * np.conj(x2) + h2 * np.conj(x1) + noise_gaussian2
        
        y1 = np.conj(h1) * r1 + h2 * np.conj(r2)
        y2 = np.conj(h2) * r1 - h1 * np.conj(r2)
        alpha = np.abs(h1) ** 2 + np.abs(h2) ** 2
        x1_hat = y1 / alpha
        x2_hat = y2 / alpha

        
        b1_detect = int(x1_hat.real > 0)
        b2_detect = int(x2_hat.real > 0)
        each_error += (b1 != b1_detect) + (b2 != b2_detect)
        each_bit += 2
        
    ber.append(each_error / each_bit)

plt.semilogy(db, ber, 'o-', label='2x1 BPSK')
plt.xlabel('Eb/N0')
plt.ylabel('BER')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.title('2x2 MIMO BPSK')
plt.show() 




        


        







