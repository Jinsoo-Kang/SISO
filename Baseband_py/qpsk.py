import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,11,1) # 0~10까지 db를 증가
ber = [] # ber 리스트 생성

for ebno in db:# db 하나씩
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1 / (4 * ratio))
   

    while each_error <100: # 오류가 100개 미만까지 while문 반복, 100순간 loop exit
        b1 = np.random.choice([np.cos(np.pi/4), -np.cos(np.pi/4)]) # 실수부 pi/4, -pi/4 랜덤비트 생성
        b2 = np.random.choice([np.sin(np.pi/4), -np.sin(np.pi/4)]) # 허수부 pi/4, -pi/4 랜덤비트 생성
        bit1 = int(b1 < 0) # 심볼값 비트 변환 // -0.707인 경우에 1이라는 비트 나오도록 // 1사분면:00 , 2: 10, 3: 11, 4:01
        bit2 = int(b2 < 0) # 동일
        each_bit +=2 # 생성한 비트 더해주기 // 0으로 하면 오류나옴
        s = b1 + b2*1j # symbol 생성. 실수부 + 허수부 (00, 01, 10, 11)
        noise_gaussian = noise_sigma*(np.random.randn()+np.random.randn()*1j) # (Re + Im) 노이즈 생성
        r = s + noise_gaussian # 수신단 변환된 비트 + 노이즈

        b1_de = int(r.real<0) # s에서 실수부 1이 됨, r에서 1+nosie, r값이 0보다 크면 b1_de가 0 
        b2_de = int(r.imag<0) # b2값 판단

        each_error += ((bit1 != b1_de) + (bit2 != b2_de)) # b1과 b1_de 비교(2도) // 에러 수 더하기

    ber.append(each_error/each_bit) # BER



plt.semilogy(db, ber, 's--', label='QPSK')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('QPSK BER Curve')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()