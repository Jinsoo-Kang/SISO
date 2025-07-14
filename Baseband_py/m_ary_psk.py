import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0,11,1) # 0~10까지 Eb/N0 dB를 1씩 증가시키면서 BER 계산
m_list = [1,2,3] # 2^m-ary psk // m=1,2,3 리스트를 만들어줌. 추가 가능.

for m in m_list:
    ts = 2**m # ts = 토탈 심볼
    ber = [] # ber 리스트 생성

    if m == 1: #BPSK 매핑
        mapping = {  # 딕셔너리 생성 (비트값: 변수)
            (0,): 1,
            (1,): -1,
        }
    
    elif m == 2: # QPSK 매핑
        mapping = {  # 딕셔너리 생성
            (0, 0): 1/np.sqrt(2) + 1j/np.sqrt(2),
            (0, 1):  1/np.sqrt(2) - 1j/np.sqrt(2),
            (1, 1): -1/np.sqrt(2) - 1j/np.sqrt(2),
            (1, 0): -1/np.sqrt(2) + 1j/np.sqrt(2),
        }

    elif m == 3: #8PSK 매핑 // 3번째 심볼.. / 직접 매핑하니 계속 오류가 나옴.
        bit_table = [(0,0,0), (0,0,1), (0,1,1), (0,1,0), (1,1,0), (1,1,1), (1,0,1), (1,0,0)] # 그레이코드 순서대로 저장
        mapping = {} # 딕셔너리 생성 (비트값 : 변수)
        for k, bits in enumerate(bit_table): # 비트테이블에 있는 0~7까지 하나씩 증가시키며 k와 그레이코드를 둘 다 불러옴
            angle = k*(2*np.pi/8) # 각도 값 = k번째 * (2pi/8) // 2pi를 8등분
            mapping[bits] = np.cos(angle) + 1j*np.sin(angle) # 각 그레이코드에 매칭 시키기 = I채널 해당하는 cos(theta값) + Q채널 해당하는 복소수 sin(theta)값


    for ebno in db: 
        each_bit = 0 
        each_error = 0 
        ratio = 10 ** (ebno / 10)
        noise_sigma = np.sqrt(1 / (2 * m * ratio)) # 심볼 E
        while each_error < 100:
            bit = tuple(int(x) for x in np.random.randint(0, 2, m)) # m개 랜덤비트 생성 // 딕셔너리 키
            s = mapping[tuple(bit)] # ex) bit가 101이라면 0-1j 불러오기 // 해당부분 심볼 찾아오기
            noise = noise_sigma * (np.random.randn() + 1j * np.random.randn()) # 복소잡음
            r = s + noise # 수신단
            
            if m == 1:
                b_de = int(r.real < 0)
                det_bit = (b_de,) # 직접 매핑했으니까 튜플로 저장하기
            elif m == 2:
                b1_de = int(r.real < 0)
                b2_de = int(r.imag < 0)
                det_bit = (b1_de, b2_de) #직접 매핑 했으니까 튜플로 저장하기
            elif m == 3:
                theta = np.angle(r) # 각도
                if theta < 0: #각도 0~360도로 만들었음. 보기 편하게
                    theta += 2 * np.pi
                
                gray = int(np.round(theta / (2 * np.pi / 8))) % 8 #8등분 // 여기서 오류 많이 나옴. round말고 int쓰니까 ber이 계속 위에 떠있음.(반올림)
                det_bit = bit_table[gray] # 8등분한 부분의 그레이코드 정하기

            bit_errors = 0
            for i in range(m):
                if bit[i] != det_bit[i]: # bit, det bit이 다르면 에러에 1 더해주기
                    bit_errors += 1 
            each_bit += m
            each_error += bit_errors
        ber.append(each_error / each_bit)
    plt.semilogy(db, ber, marker='o', label=f'{ts}-PSK (m={m})')

plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('2^m-ary PSK BER Curve')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()