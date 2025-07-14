import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,25,5)
ber = []

for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (2 * ratio * 3)) 

    while each_error < 500:
       
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        each_bit += 3

        if   b1==0 and b2==0 and b3==0: 
            phase1 = np.pi/8
        elif b1==0 and b2==0 and b3==1: 
            phase1 = 3*np.pi/8
        elif b1==0 and b2==1 and b3==1: 
            phase1 = 5*np.pi/8
        elif b1==0 and b2==1 and b3==0: 
            phase1 = 7*np.pi/8
        elif b1==1 and b2==1 and b3==0: 
            phase1 = 9*np.pi/8
        elif b1==1 and b2==1 and b3==1: 
            phase1 = 11*np.pi/8
        elif b1==1 and b2==0 and b3==1: 
            phase1 = 13*np.pi/8
        elif b1==1 and b2==0 and b3==0: 
            phase1 = 15*np.pi/8
        s1 = np.cos(phase1) + 1j * np.sin(phase1)



        b4 = np.random.randint(0,2)
        b5 = np.random.randint(0,2)
        b6 = np.random.randint(0,2)
        each_bit += 3

        if   b4==0 and b5==0 and b6==0: 
            phase2 = np.pi/8
        elif b4==0 and b5==0 and b6==1: 
            phase2 = 3*np.pi/8
        elif b4==0 and b5==1 and b6==1: 
            phase2 = 5*np.pi/8
        elif b4==0 and b5==1 and b6==0: 
            phase2 = 7*np.pi/8
        elif b4==1 and b5==1 and b6==0: 
            phase2 = 9*np.pi/8
        elif b4==1 and b5==1 and b6==1: 
            phase2 = 11*np.pi/8
        elif b4==1 and b5==0 and b6==1: 
            phase2 = 13*np.pi/8
        elif b4==1 and b5==0 and b6==0: 
            phase2 = 15*np.pi/8
        s2 = np.cos(phase2) + 1j * np.sin(phase2)

      
        h = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)
        h1, h2 = h[0,0], h[1,0]
        n1 = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        n2 = noise_sigma * (np.random.randn() + 1j * np.random.randn())

        
        r1 = h1 * s1 + h2 * s2 + n1
        r2 = -h1 * np.conj(s2) + h2 * np.conj(s1) + n2

    
        y1 = np.conj(h1)*r1 + h2*np.conj(r2)
        y2 = np.conj(h2)*r1 - h1*np.conj(r2)
        alpha = np.abs(h1)**2 + np.abs(h2)**2
        s1_hat = y1 / alpha
        s2_hat = y2 / alpha

        
        theta1 = np.mod(np.angle(s1_hat), 2*np.pi)
        if 0 <= theta1 < np.pi/4:
            b1_detect, b2_detect, b3_detect = 0,0,0
        elif np.pi/4 <= theta1 < 2*np.pi/4:
            b1_detect, b2_detect, b3_detect = 0,0,1
        elif 2*np.pi/4 <= theta1 < 3*np.pi/4:
            b1_detect, b2_detect, b3_detect = 0,1,1
        elif 3*np.pi/4 <= theta1 < 4*np.pi/4:
            b1_detect, b2_detect, b3_detect = 0,1,0
        elif 4*np.pi/4 <= theta1 < 5*np.pi/4:
            b1_detect, b2_detect, b3_detect = 1,1,0
        elif 5*np.pi/4 <= theta1 < 6*np.pi/4:
            b1_detect, b2_detect, b3_detect = 1,1,1
        elif 6*np.pi/4 <= theta1 < 7*np.pi/4:
            b1_detect, b2_detect, b3_detect = 1,0,1
        elif 7*np.pi/4 <= theta1 < 2*np.pi:
            b1_detect, b2_detect, b3_detect = 1,0,0

        theta2 = np.mod(np.angle(s2_hat), 2*np.pi)
        if 0 <= theta2 < np.pi/4:
            b4_detect, b5_detect, b6_detect = 0,0,0
        elif np.pi/4 <= theta2 < 2*np.pi/4:
            b4_detect, b5_detect, b6_detect = 0,0,1
        elif 2*np.pi/4 <= theta2 < 3*np.pi/4:
            b4_detect, b5_detect, b6_detect = 0,1,1
        elif 3*np.pi/4 <= theta2 < 4*np.pi/4:
            b4_detect, b5_detect, b6_detect = 0,1,0
        elif 4*np.pi/4 <= theta2 < 5*np.pi/4:
            b4_detect, b5_detect, b6_detect = 1,1,0
        elif 5*np.pi/4 <= theta2 < 6*np.pi/4:
            b4_detect, b5_detect, b6_detect = 1,1,1
        elif 6*np.pi/4 <= theta2 < 7*np.pi/4:
            b4_detect, b5_detect, b6_detect = 1,0,1
        elif 7*np.pi/4 <= theta2 < 2*np.pi:
            b4_detect, b5_detect, b6_detect = 1,0,0


        each_error += (b1 != b1_detect) + (b2 != b2_detect) + (b3 != b3_detect) + (b4 != b4_detect) + (b5 != b5_detect) + (b6 != b6_detect)

    ber.append(each_error / each_bit)
    print(f"Eb/N0={ebno} dB, BER={ber[-1]:.5e}")

plt.figure(figsize=(9,6))
plt.semilogy(db, ber, 'o-', label='Alamouti 2x1 8PSK')
plt.xlabel('Eb/N0')
plt.ylabel('BER')
plt.title('Alamouti 2x1 8PSK BER')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()

