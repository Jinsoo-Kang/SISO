import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,11,1)

#QPSK
ber_qpsk = []
for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1 / (4 * ratio))
    print(f"{ebno} dB")

    while each_error < 100: # 오류가 100개 미만까지 while문 반복, 100순간 loop exit
        b1 = np.random.choice([np.cos(np.pi/4), -np.cos(np.pi/4)]) # 실수부 pi/4, -pi/4 랜덤비트 생성
        b2 = np.random.choice([np.sin(np.pi/4), -np.sin(np.pi/4)]) # 허수부 pi/4, -pi/4 랜덤비트 생성
        bit1 = int(b1 < 0) # 심볼값 비트 변환 // -0.707인 경우에 1이라는 비트 나오도록 // 1사분면:00 , 2: 10, 3: 11, 4:01
        bit2 = int(b2 < 0) # 동일
        each_bit += 2 # 생성한 비트 더해주기 // 0으로 하면 오류나옴
        s = b1 + b2*1j # symbol 생성. 실수부 + 허수부 (00, 01, 10, 11)
        noise_gaussian = noise_sigma*(np.random.randn() + np.random.randn()*1j) # (Re + Im) 노이즈 생성
        r = s + noise_gaussian # 수신단 변환된 비트 + 노이즈
        b1_de = int(r.real < 0) # s에서 실수부 1이 됨, r에서 1+nosie, r값이 0보다 크면 b1_de가 0 
        b2_de = int(r.imag < 0) # b2값 판단
        each_error += (bit1 != b1_de) + (bit2 != b2_de) # b1과 b1_de 비교(2도) // 에러 수 더하기
    ber_qpsk.append(each_error/each_bit) # BER

#BPSK
ber_bpsk = []
for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1 / (2 * ratio))
    print(f"{ebno} dB")

    while each_error < 100:
        b = np.random.randint(0,2)
        each_bit += 1
        s = 2*b -1
        noise_gaussian = noise_sigma * np.random.randn()
        r = s + noise_gaussian
        b_de = int(r>0)
        each_error += (b != b_de)
    ber_bpsk.append(each_error/each_bit)

plt.semilogy(db, ber_qpsk, 's--', color='r', label='QPSK')
plt.semilogy(db, ber_bpsk, 'o-', color='b', label='BPSK')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('BER Curve')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()