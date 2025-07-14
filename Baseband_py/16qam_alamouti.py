import numpy as np
import matplotlib.pyplot as plt

db = np.arange(0, 25, 5)
ber = []

a = 1 / np.sqrt(10)  # 정규화 상수 // 평균 E = 10A**2 // 따라서 1로 정규화 시키기 위해 a = 1/루트10 

for ebno in db:
    each_bit = 0
    each_error = 0
    ratio = 10 ** (ebno / 10)
    noise_sigma = np.sqrt(1 / (2 * 4 * ratio))  # 16QAM: 심볼당 4비트 // m = 4 

    while each_error < 500:
      
        b1 = np.random.randint(0, 2)   # 4비트 랜덤 생성 // 첫번째 x1 심볼값 매핑
        b2 = np.random.randint(0, 2)
        b3 = np.random.randint(0, 2)
        b4 = np.random.randint(0, 2)
        each_bit += 4
        gray_str1 = f"{b1}{b2}{b3}{b4}" # 각 비트를 문자열로 만들어주기

        if gray_str1 == '0000':
            s1 = a * (3+1j*3)
        elif gray_str1 == '0001':
            s1 = a * (3+1j)
        elif gray_str1 == '0011':
            s1 = a * (1+1j)
        elif gray_str1 == '0010':
            s1 = a * (1+1j*3)
        elif gray_str1 == '0110':
            s1 = a * (1-1j*3)
        elif gray_str1 == '0111':
            s1 = a * (1-1j)
        elif gray_str1 == '0101':
            s1 = a * (3-1j)
        elif gray_str1 == '0100':
            s1 = a * (3-1j*3)
        elif gray_str1 == '1100':
            s1 = a * (-3-1j*3)
        elif gray_str1 == '1101':
            s1 = a * (-3-1j)
        elif gray_str1 == '1111':
            s1 = a * (-1-1j)
        elif gray_str1 == '1110':
            s1 = a * (-1-1j*3)
        elif gray_str1 == '1010':
            s1 = a * (-1+1j*3)
        elif gray_str1 == '1011':
            s1 = a * (-1+1j)
        elif gray_str1 == '1001':
            s1 = a * (-3+1j)
        elif gray_str1 == '1000':
            s1 = a * (-3+1j*3)

        
        b5 = np.random.randint(0, 2)   # 4비트 랜덤 생성 // 두번째 x2 심볼값 매핑
        b6 = np.random.randint(0, 2)
        b7 = np.random.randint(0, 2)
        b8 = np.random.randint(0, 2)
        each_bit += 4 
        gray_str2 = f"{b5}{b6}{b7}{b8}" # 각 비트 문자열로 만들기

        if gray_str2 == '0000':
            s2 = a * (3+1j*3)
        elif gray_str2 == '0001':
            s2 = a * (3+1j)
        elif gray_str2 == '0011':
            s2 = a * (1+1j)
        elif gray_str2 == '0010':
            s2 = a * (1+1j*3)
        elif gray_str2 == '0110':
            s2 = a * (1-1j*3)
        elif gray_str2 == '0111':
            s2 = a * (1-1j)
        elif gray_str2 == '0101':
            s2 = a * (3-1j)
        elif gray_str2 == '0100':
            s2 = a * (3-1j*3)
        elif gray_str2 == '1100':
            s2 = a * (-3-1j*3)
        elif gray_str2 == '1101':
            s2 = a * (-3-1j)
        elif gray_str2 == '1111':
            s2 = a * (-1-1j)
        elif gray_str2 == '1110':
            s2 = a * (-1-1j*3)
        elif gray_str2 == '1010':
            s2 = a * (-1+1j*3)
        elif gray_str2 == '1011':
            s2 = a * (-1+1j)
        elif gray_str2 == '1001':
            s2 = a * (-3+1j)
        elif gray_str2 == '1000':
            s2 = a * (-3+1j*3)

        
        h = (np.random.randn(2,1) + 1j * np.random.randn(2,1)) / np.sqrt(2)  # h 채널(rayliegh) h1,h2 (2x1) // h = (G+jG)/sqrt(2) ->정규화
        h1 = h[0,0] # 첫번째 채널 h1
        h2 = h[1,0] # 두번째 채널 h2
        n1 = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        n2 = noise_sigma * (np.random.randn() + 1j * np.random.randn())

        
        r1 = h1*s1 + h2*s2 + n1 # 시공간에서의 부호화 // i에서, h1-h2 에서의
        r2 = -h1*np.conj(s2) + h2*np.conj(s1) + np.conj(n2) # 시공간에서의 부호화 // i+1에서, h1-h2에서의

       
        y1 = np.conj(h1)*r1 + h2*np.conj(r2)  # H의 hermitian값에 r(2x1) 값을 곱하면// H(her) x r = alpha x I x x(2x1) + noise
        y2 = np.conj(h2)*r1 - h1*np.conj(r2)
        alpha = np.abs(h1)**2 + np.abs(h2)**2 # alpha 값은 절대값 h1**2 + 절대값 h2**2
        s1_hat = y1 / alpha # x(2x1) = y / alpha 
        s2_hat = y2 / alpha

        
        def detect(value): # detect라는 함수를 정의 // 구간을 나누고 0~2까지 구간에서는 1로 return되도록, ㅣ2ㅣ보다 큰 경우에는 -3이 리턴 되도록
            if value >= 2*a:
                return 3
            elif 0 <= value < 2*a:
                return 1
            elif -2*a < value < 0:
                return -1
            else:
                return -3

        
        i1 = detect(s1_hat.real) # I채널 쪽 detect 함수 사용
        q1 = detect(s1_hat.imag) # Q채널 쪽 detect 함수 사용
        
        i2 = detect(s2_hat.real)
        q2 = detect(s2_hat.imag)

        # s1_hat 을 통해 그레이코드 역으로 찾기
        if i1 == 3 and q1 == 3:         
            b1d, b2d, b3d, b4d = 0,0,0,0
        elif i1 == 3 and q1 == 1:       
            b1d, b2d, b3d, b4d = 0,0,0,1
        elif i1 == 1 and q1 == 1:       
            b1d, b2d, b3d, b4d = 0,0,1,1
        elif i1 == 1 and q1 == 3:       
            b1d, b2d, b3d, b4d = 0,0,1,0
        elif i1 == 1 and q1 == -3:      
            b1d, b2d, b3d, b4d = 0,1,1,0
        elif i1 == 1 and q1 == -1:      
            b1d, b2d, b3d, b4d = 0,1,1,1
        elif i1 == 3 and q1 == -1:      
            b1d, b2d, b3d, b4d = 0,1,0,1
        elif i1 == 3 and q1 == -3:      
            b1d, b2d, b3d, b4d = 0,1,0,0
        elif i1 == -3 and q1 == -3:    
            b1d, b2d, b3d, b4d = 1,1,0,0
        elif i1 == -3 and q1 == -1:     
            b1d, b2d, b3d, b4d = 1,1,0,1
        elif i1 == -1 and q1 == -1:     
            b1d, b2d, b3d, b4d = 1,1,1,1
        elif i1 == -1 and q1 == -3:     
            b1d, b2d, b3d, b4d = 1,1,1,0
        elif i1 == -1 and q1 == 3:      
            b1d, b2d, b3d, b4d = 1,0,1,0
        elif i1 == -1 and q1 == 1:      
            b1d, b2d, b3d, b4d = 1,0,1,1
        elif i1 == -3 and q1 == 1:      
            b1d, b2d, b3d, b4d = 1,0,0,1
        elif i1 == -3 and q1 == 3:      
            b1d, b2d, b3d, b4d = 1,0,0,0
        # s2_hat 을 통해 그레이코드 역으로 찾기
        if i2 == 3 and q2 == 3:         
            b5d, b6d, b7d, b8d = 0,0,0,0
        elif i2 == 3 and q2 == 1:       
            b5d, b6d, b7d, b8d = 0,0,0,1
        elif i2 == 1 and q2 == 1:       
            b5d, b6d, b7d, b8d = 0,0,1,1
        elif i2 == 1 and q2 == 3:       
            b5d, b6d, b7d, b8d = 0,0,1,0
        elif i2 == 1 and q2 == -3:      
            b5d, b6d, b7d, b8d = 0,1,1,0
        elif i2 == 1 and q2 == -1:      
            b5d, b6d, b7d, b8d = 0,1,1,1
        elif i2 == 3 and q2 == -1:      
            b5d, b6d, b7d, b8d = 0,1,0,1
        elif i2 == 3 and q2 == -3:      
            b5d, b6d, b7d, b8d = 0,1,0,0
        elif i2 == -3 and q2 == -3:     
            b5d, b6d, b7d, b8d = 1,1,0,0
        elif i2 == -3 and q2 == -1:     
            b5d, b6d, b7d, b8d = 1,1,0,1
        elif i2 == -1 and q2 == -1:     
            b5d, b6d, b7d, b8d = 1,1,1,1
        elif i2 == -1 and q2 == -3:    
            b5d, b6d, b7d, b8d = 1,1,1,0
        elif i2 == -1 and q2 == 3:      
            b5d, b6d, b7d, b8d = 1,0,1,0
        elif i2 == -1 and q2 == 1:      
            b5d, b6d, b7d, b8d = 1,0,1,1
        elif i2 == -3 and q2 == 1:      
            b5d, b6d, b7d, b8d = 1,0,0,1
        elif i2 == -3 and q2 == 3:      
            b5d, b6d, b7d, b8d = 1,0,0,0

        # 에러합산
        each_error += (b1 != b1d) + (b2 != b2d) + (b3 != b3d) + (b4 != b4d) + (b5 != b5d) + (b6 != b6d) + (b7 != b7d) + (b8 != b8d)

    ber.append(each_error / each_bit)
    print(f"Eb/N0={ebno} dB, BER={ber[-1]:.5e}")

plt.figure(figsize=(9,6))
plt.semilogy(db, ber, 'o-', label='Alamouti 2x1 16QAM')
plt.xlabel('Eb/N0')
plt.ylabel('BER')
plt.title('Alamouti 2x1 16QAM BER')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()