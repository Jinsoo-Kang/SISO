import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,11,1) # 0~10까지 db를 증가
ber = [] # ber 리스트 생성

for ebno in db:# db 하나씩
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1 / (2 * ratio))

    while each_error <100: # 오류가 100개 미만까지 while문 반복, 100순간 loop exit
        b1 = np.random.randint(0,2) # 실수부 0,1 랜덤비트 생성
        b2 = np.random.randint(0,2) # 허수부 0,1 랜덤비트 생성
        each_bit +=2 # 생성한 비트 더해주기 // 0으로 하면 오류나옴
        s = ((1-2*b1) + (1-2*b2)*1j) / np.sqrt(2) # symbol 생성. 실수부 + 허수부 (00, 01, 10, 11) // 이후 sprt(2) 나눠주면서 1을 루트2 분의 1로 만들기
        noise_gaussian = noise_sigma*(np.random.randn()+np.random.randn()*1j) # (Re + Im) 노이즈 생성
        r = s + noise_gaussian # 수신단 변환된 비트 + 노이즈

        b1_de = int(r.real<0) # 매핑 00: 1+1j, 01: 1-1j, 10: -1+1j, 11: -1-1j // b1의 정수값 판단
        b2_de = int(r.imag<0) # b2값 판단

        each_error += ((b1 != b1_de) + (b2 != b2_de)) # 변환된 값과 생성된 값 비교 // 에러 수 더하기

    ber.append(each_error/each_bit) # BER



plt.semilogy(db, ber, 's--', label='QPSK')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('QPSK BER Curve')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()