import numpy as np
import matplotlib.pyplot as plt

# AWGN 채널
db_awgn = np.arange(0,15,1)
ber_awgn = []
a = 1 / np.sqrt(10) # a값 따로 빼주기 // 아래 코드는 정규화 안시킴

for ebno in db_awgn:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(2*4*ratio)) # m = 4

    while each_error < 1000:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit += 4

        
        gray_str= f"{b1}{b2}{b3}{b4}" # 그레이코드를 문자열로 생성

        if gray_str == '0000': # 16-QAM 매핑
            s = a * (3+1j*3)
        elif gray_str == '0001':
            s = a * (3+1j)
        elif gray_str == '0011':
            s = a * (1 + 1j)
        elif gray_str == '0010':
            s = a * (1 + 1j*3)
        elif gray_str == '0110':
            s = a * (1 - 1j*3)
        elif gray_str == '0111':
            s = a * (1 - 1j)
        elif gray_str == '0101':
            s = a * (3 - 1j)
        elif gray_str == '0100':
            s = a * (3 - 1j*3)
        elif gray_str == '1100':
            s = a * (-3 - 1j*3)
        elif gray_str == '1101':
            s = a * (-3 - 1j)
        elif gray_str == '1111':
            s = a * (-1 - 1j)
        elif gray_str == '1110':
            s = a * (-1 - 1j*3)
        elif gray_str == '1010':
            s = a * (-1 + 1j*3)
        elif gray_str == '1011':
            s = a * (-1 + 1j)
        elif gray_str == '1001':
            s = a * (-3 + 1j)
        elif gray_str == '1000':
            s = a * (-3 + 1j*3)
        
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = s + noise_gaussian

        def detect(value): # detect라는 함수를 정의 // 구간을 나누고 0~2까지 구간에서는 1로 return되도록, ㅣ2ㅣ보다 큰 경우에는 -3이 리턴 되도록
            if value >= 2*a:
                return 3
            elif 0<= value <2*a:
                return 1
            elif -2*a < value < 0:
                return -1
            else:
                return -3
            
        i_detect = detect(r.real) # I 채널 쪽 detect 함수 사용
        q_detect = detect(r.imag) # Q 채널 쪽 detect 함수 사용

        if i_detect == 3 and q_detect == 3: # detect 함수를 사용해서 되돌려진 값에 따라서 다시 그레이 코드에 매칭시키기
            b1d, b2d, b3d, b4d = 0,0,0,0
        elif i_detect == 3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,0,1
        elif i_detect == 1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,1,1
        elif i_detect == 1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 0,0,1,0
        elif i_detect == 1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,1,0
        elif i_detect == 1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,1,1
        elif i_detect == 3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,0,1
        elif i_detect == 3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,0,0
        elif i_detect == -3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,0,0
        elif i_detect == -3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,0,1
        elif i_detect == -1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,1,1
        elif i_detect == -1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,1,0
        elif i_detect == -1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,1,0
        elif i_detect == -1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,1,1
        elif i_detect == -3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,0,1
        elif i_detect == -3 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,0,0

        each_error += (b1 != b1d) + (b2 != b2d) + (b3 != b3d) + (b4 != b4d)
    ber_awgn.append(each_error/each_bit)


# fading 채널
db_fading = np.arange(0,45,5)
ber_fading = []
a = 1 / np.sqrt(10) # a값 따로 빼주기 // 아래 코드는 정규화 안시킴

for ebno in db_fading:
    each_bit = 0
    each_error = 0
    ratio = 10**(ebno/10)
    noise_sigma = np.sqrt(1/(2*4*ratio)) # m = 4

    while each_error < 1000:
        b1 = np.random.randint(0,2)
        b2 = np.random.randint(0,2)
        b3 = np.random.randint(0,2)
        b4 = np.random.randint(0,2)
        each_bit += 4

        
        gray_str= f"{b1}{b2}{b3}{b4}" # 그레이코드를 문자열로 생성

        if gray_str == '0000': # 16-QAM 매핑
            s = a * (3+1j*3)
        elif gray_str == '0001':
            s = a * (3+1j)
        elif gray_str == '0011':
            s = a * (1 + 1j)
        elif gray_str == '0010':
            s = a * (1 + 1j*3)
        elif gray_str == '0110':
            s = a * (1 - 1j*3)
        elif gray_str == '0111':
            s = a * (1 - 1j)
        elif gray_str == '0101':
            s = a * (3 - 1j)
        elif gray_str == '0100':
            s = a * (3 - 1j*3)
        elif gray_str == '1100':
            s = a * (-3 - 1j*3)
        elif gray_str == '1101':
            s = a * (-3 - 1j)
        elif gray_str == '1111':
            s = a * (-1 - 1j)
        elif gray_str == '1110':
            s = a * (-1 - 1j*3)
        elif gray_str == '1010':
            s = a * (-1 + 1j*3)
        elif gray_str == '1011':
            s = a * (-1 + 1j)
        elif gray_str == '1001':
            s = a * (-3 + 1j)
        elif gray_str == '1000':
            s = a * (-3 + 1j*3)
        
        h = (np.random.randn() + 1j * np.random.randn()) / np.sqrt(2)
        noise_gaussian = noise_sigma * (np.random.randn() + 1j * np.random.randn())
        r = h*s + noise_gaussian
        r_reverse = r / h


        def detect(value): # detect라는 함수를 정의 // 구간을 나누고 0~2까지 구간에서는 1로 return되도록, ㅣ2ㅣ보다 큰 경우에는 -3이 리턴 되도록
            if value >= 2*a:
                return 3
            elif 0<= value <2*a:
                return 1
            elif -2*a < value < 0:
                return -1
            else:
                return -3
            
        i_detect = detect(r.real) # I 채널 쪽 detect 함수 사용
        q_detect = detect(r.imag) # Q 채널 쪽 detect 함수 사용

        if i_detect == 3 and q_detect == 3: # detect 함수를 사용해서 되돌려진 값에 따라서 다시 그레이 코드에 매칭시키기
            b1d, b2d, b3d, b4d = 0,0,0,0
        elif i_detect == 3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,0,1
        elif i_detect == 1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 0,0,1,1
        elif i_detect == 1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 0,0,1,0
        elif i_detect == 1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,1,0
        elif i_detect == 1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,1,1
        elif i_detect == 3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 0,1,0,1
        elif i_detect == 3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 0,1,0,0
        elif i_detect == -3 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,0,0
        elif i_detect == -3 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,0,1
        elif i_detect == -1 and q_detect == -1:
            b1d, b2d, b3d, b4d = 1,1,1,1
        elif i_detect == -1 and q_detect == -3:
            b1d, b2d, b3d, b4d = 1,1,1,0
        elif i_detect == -1 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,1,0
        elif i_detect == -1 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,1,1
        elif i_detect == -3 and q_detect == 1:
            b1d, b2d, b3d, b4d = 1,0,0,1
        elif i_detect == -3 and q_detect == 3:
            b1d, b2d, b3d, b4d = 1,0,0,0

        each_error += (b1 != b1d) + (b2 != b2d) + (b3 != b3d) + (b4 != b4d)
    ber_fading.append(each_error/each_bit)


plt.figure(figsize=(9, 6))
plt.semilogy(db_awgn, ber_awgn, 'o-', label='16-QAM(awgn)')
plt.semilogy(db_fading, ber_fading, 's-', label='16-QAM(fading)')
plt.xlabel('Eb/N0')
plt.ylabel('BER')
plt.title('16-QAM AWGN vs Fading (Error 1000)')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()



            

            




