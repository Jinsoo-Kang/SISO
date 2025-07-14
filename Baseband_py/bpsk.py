import numpy as np
import matplotlib.pyplot as plt

n = int(1e7) # 전체 비트 10^7개
db = np.arange(0,13,1) #dB 0~10까지 1씩 증가
ber = [] # BER 저장 리스트 생성

for ebno in db: # db 하나씩 증가시키면
    bit = np.random.randint(0,2,n) # 0,1 랜덤비트 n개 생성 
    s = 2*bit - 1 # 0,1 랜덤비트를 1, -1로 변환 // 0 -> -1 , 1 -> 1
    ratio = 10**(ebno/10) # db를 ratio 변환 = ebno
    noise_sigma = np.sqrt(1/(2*ratio)) # sigma = sqrt(1/(2*ebno)) 
    noise_gaussian = noise_sigma*np.random.randn(n) # m = 0, noise_sigma 정규분포 생성 // AWGN 노이즈 생성
    r = s + noise_gaussian # 수신단에서 변환된 비트 + 노이즈
    decode = (r>0).astype(int) # 수신단에서 받은 비트가 0보다 크면 보낸 신호가 1이었을 것으로 판단, 0보다 작으면 0이었을 것으로 판단.
    error = np.sum(bit != decode) # bit 리스트와 decode의 리스트의 비트값을 비교하여 다른 개수 = 오류 수
    ber.append(error/n) # BER = 오류 비트수 / 전체 비트




plt.semilogy(db, ber, 's--', label='BPSK')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('BPSK BER CURVE')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()