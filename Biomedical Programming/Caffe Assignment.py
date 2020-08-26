import time
import sys
# 라이브러리 import, sys는 프로그램 종료에 사용되는 라이브러리

# Menu.txt에 있는 메뉴의 이름,가격, 재고 등을 리스트에 각각 넣어준다.
# txt에 메뉴, 가격 재고순으로 만들어져 있다.
with open('menu.txt', 'r') as f: # f.open()을 f로 읽어준다
    menu = []
    price = []
    stock = []
    servinglimit = []
    for Q in f:
        Q = Q.strip().split() # strip은 공백과 \n을 지워주는 함수, split은 공백을 기준으로 리스트를 나누는 것
        price.append(int(Q[2].replace(',','')))
        # replace 함수로 천단위마다 해주었던 쉼표를 제거합니다. int를 사용하여 수로 표시해야하기 때문입니다.
        servinglimit.append(int(Q[3]))
        stock.append(int(Q[len(Q) - 1]))
        menu.append(" ".join(Q[:2]).lower())  # 리스트 이름을 전부 소문자로 변경해줍니다.
f.close()

# 아이디, 비밀번호 리스트를 만든다.
# Id.txt에 있는 아이디와 비밀번호를 리스트에 넣어준다.
# ID와 PW는 특별한 뛰어쓰기가 없고, 숫자로 변환해줄 필요가 없다. ID가 먼저 적혀있고, 그 뒤에 PW이 적혀있기 때문에 ID,PW 순으로 구해준다.
with open('id.txt', 'r') as f: # f.open()을 f로 읽어준다
    ID = []
    PW = []
    for Q in f:
        Q = Q.strip().split()
        ID.append(Q[0])
        PW.append(Q[1])
f.close()

def process_order(menu, price, servinglimit):
    print("*" * 65)
    print('어서오세요! 바의공 카페입니다!')
    print("메뉴 목록")
    for a, b, c in zip(menu, price, stock):  # zip은 [a, menu] [b, price] [c, stock] 형태로 만들어주는 함수
        print("{0} {1} {2}".format(a, format(b, ','), format(c, ',')))  # 메뉴명, 가격, 재고를 출력, 가격이나 재고의 경우 천 단위마다 콤마

    ordername = []  # 주문이 들어갈 리스트
    ordercount = []  # 들어간 주문과 그에 맞는 수량
    while True:
        d = input("무엇을 주문하시겠어요?")
        d = d.lower().strip()  # strip은 빈칸을 모두 제거해주고, lower는 대소문자 형태를 모두 소문자로 바꾸어준다.
        # 주문한 메뉴가 처음일 때, 이미 주문한 메뉴를 추가 주문할 때, 없는 메뉴를 주문할 때 세가지 경우를 생각해준다
        if d in ordername:  # 이미 주문한 메뉴를 추가 주문 할 때
            n = int(input("몇 잔 주문하시겠어요?"))  # input은 문자열을 출력하기 때문에 int 사용
            ordercount[ordername.index(d)] += n  # 주문 받은 메뉴의 숫자 리스트 + n 으로 수량을 늘린다.
            extra = input('추가 주문 하시겠습니까? [y/n]')  # y 또는 n 으로 받는다
            if extra == 'y':
                continue
            elif extra == 'n':
                break
            else:
                print('y 또는 n으로 대답해주세요!')
                return False

        elif d not in menu:  # 없는 메뉴를 주문 할 때
            print('존재하지 않는 메뉴입니다.')
            continue

        elif d not in ordername:  # 주문한 메뉴가 처음일 때
            n = int(input("몇 잔 주문하시겠어요?"))  # input은 문자열을 출력하기 때문에 int 사용
            ordername.append(d)  # 주문 받은 메뉴의 이름을 해당 리스트에 추가해줌
            ordercount.append(n)  # 주문 받은 메뉴의 수량을 해당 리스트에 추가해줌
            extra = input('추가 주문 하시겠습니까? [y/n]')  # y 또는 n 으로 받는다
            if extra == 'y':
                continue
            elif extra == 'n':
                break
            else:
                print('y 또는 n으로 대답해주세요!')
                return False

        # 주문받은 수량이 재고보다 많으면 재고 부족 표시
    for d, fa in zip(ordername, ordercount):
        if fa > stock[menu.index(d)]:
            print("죄송합니다 그 상품은 재고가 부족합니다 ")
            return False

    # 주문한 상품을 모두 알려준다.
    for d, fb in zip(ordername, ordercount):
        print('주문하신 {0} {1}잔 나왔습니다!'.format(d, fb))

    # 주문 받은 메뉴의 수량만큼을 해당 메뉴의 재고에서 빼준다.
    for d, fc in zip(ordername, ordercount):
        stock[menu.index(d)] -= fc

    # 영수증 발행
    receipt = input('영수증 필요하신가요? [y/n]')
    if receipt == 'y':  # 영수증이 필요할 때,
        df = time.localtime()
        y = open("{0}년{1}월{2}일{3}시{4}분.txt".format(df.tm_year, df.tm_mon, df.tm_mday, df.tm_hour, df.tm_min), 'w')
        # localtime은 time에서 반환한 값을 날짜와 시간형태로 변환해주는데, 현재지역의 표준시(한국 표준시)를 표시해줌.
        guestsum = 0  # guestsum = 주문자가 지불해야할 총 금액
        for d, fd in zip(ordername, ordercount):
            g = fd * price[menu.index(d)]  # 가격 X 주문 갯수로 메뉴당 가격을 구해준다.
            guestsum += g  # 가격 X 주문 갯수 한 값들을 for문으로 전부 더해준다.
            y.write("{0} {1} {2}\n".format(d, format(fd, ','), format(g, ',')))  # 영수증에 메뉴명, 수량, 메뉴당 지불해야할 가격을 써준다.
        y.write("합계 금액 : {0}".format(format(guestsum, ',')))  # 영수증에 주문자가 지불해야할 총 금액을 써준다.
        y.close()
        print('영수증 여기있습니다~ 다음에 또 오세요!')
    else:
        print('그럼 영수증은 버려드리겠습니다~ 다음에 또 오세요!')

    for a in stock:
        if not a == 0:
            return False
    print('재고가 전부 소진되어 카페 문을 닫습니다!')
    return True


# 1. Print the menu (from the menu.txt)
# 2. get the order from the prompt
# 3. Display the total amount of the order
# 4. 영수증 발행 (주문시간.txt, Hint : import time)

def process_admin(id, pw, menu, price, stock, servinglimit):
    for i in range(3):  # 로그인 기회는 3번
        iden = input('아이디 :')
        pas = input('비밀번호 :')
        if iden in id:  # 존재하는 아이디인지 확인
            if pas == pw[id.index(iden)]:
                break
        print('로그인 {0}회 오류'.format(i+1))
        if i == 2:  # 로그인 기회 3번을 전부 실패하면 처음으로 돌아가기
            print('처음으로 돌아갑니다.')
            return False
    print('로그인에 성공했습니다')

    login = True
    while login:
        print("관리자 모드로 들어갑니다.")
        print("*" * 65)
        # 관리자 모드 5가지
        print("1.메뉴 변경하기")
        print("2.아이디, 비밀번호 추가")
        print("3.주문량 확인")
        print("4.영업종료")
        print("5.처음화면으로")
        print("*" * 65)
        # choise 1,2,3으로 나누어 세분화가 가능하도록 조정, s는 오타
        choise = input("Choose the number:")
        # 메뉴 변경을 선택한 경우
        if int(choise) == 1:
            print("1.재고 수정하기")
            print("2.메뉴 이름 및 가격 변경하기")
            print("3.메뉴 추가하기")
            choise2 = input('Choose the number:')
            if int(choise2) == 1:  # 재고 수정하기를 선택하는 경우
                print("*" * 65)
                # 관리자에게 기존의 메뉴목록을 보여줌
                print("메뉴 목록")
                for a, b, c in zip(menu, price, stock):
                    print("{0} {1} {2}".format(a, format(b, ','), format(c, ',')))
                s = input("재고를 추가할 메뉴의 이름은?")
                s = s.lower().strip()
                # 존재하지 않는 메뉴를 입력한 경우, 메세지를 출력하고 관리자 모드의 처음으로 돌아감
                if s not in menu:
                    print("존재하지 않는 메뉴입니다.")
                    continue
                print('재고량을 빼고 싶은 경우 -를 붙여주세요')
                p = int(input('수정할 재고량은? :'))
                # 어떤 메뉴의 수량이 얼마만큼 추가되었는지 menu_updated.txt에 기록해줌
                f9 = open('menu_updated.txt', 'a')
                f9.write("{0}의 재고가 {1} 만큼 수정됨".format(s, p) + '\n')
                f9.close()
                # 수량 변화를 해당 리스트에 적용해줌
                stock[menu.index(s)] += p  # 새로 변경된 사항을 stock과 servinglimit에 적용
                servinglimit[menu.index(s)] += p
                print('변경 완료되었습니다.')
                return False
            elif int(choise2) == 2:
                print('*'*65)
                print('1.메뉴 이름 변경하기')
                print('2.메뉴 가격 변경하기')
                choise3 = input("Choose the number:")
                print('*'*65)
                if int(choise3) == 1:
                    for a, b, c in zip(menu, price, stock):
                        print("{0} {1} {2}".format(a, format(b, ','), format(c, ',')))
                    old2 = input('수정할 기존 메뉴를 입력하세요:')
                    old2 = old2.strip().lower()
                    new2 = input('바꿀 메뉴 이름을 입력하세요:')
                    new2 = new2.strip().lower()
                    if old2 not in menu:  # 없는 메뉴라면, 존재하지 않는다로 출력
                        print('존재하지 않는 메뉴입니다.')
                        continue
                    fo = open('menu_updated.txt', 'a')  # 'a'는 추가모드
                    fo.write(old2 + '에서' + new2 + '로 이름 변경' + '\n')
                    fo.close()
                    menu[menu.index(old2)] = new2  # 새로 변경된 사항을 메뉴에 적용
                    print('변경완료되었습니다.')
                    return False
                if int(choise3) == 2:
                    for a, b, c in zip(menu, price, stock):
                        print("{0} {1} {2}".format(a, format(b, ','), format(c, ',')))
                    old = (input('수정할 메뉴 이름을 입력하세요:'))
                    print('가격을 내리고 싶다면 -를 붙여주세요')
                    new = int((input('얼마를 수정하겠습니까?:')))
                    if old not in menu:
                        print('존재하지 않는 메뉴입니다.')
                        continue
                    f6 = open('menu_updated.txt', 'a')
                    f6.write(old + '에서 {0} 로 가격 변경'.format(new)+'\n')
                    f6.close()
                    price[menu.index(old)] += new  # 새로 변경된 사항을 가격에 적용
                    print('변경 완료되었습니다.')
                    return False
            elif int(choise2) == 3:
                a = input('추가할 메뉴 이름은?')
                a = a.lower().strip()
                b = input('추가할 메뉴 가격은?')
                c = input('추가할 메뉴 재고는?')
                # 메뉴를 추가하는 경우, 추가할 메뉴의 이름, 가격, 재고를 menu_updated.txt에 기록한다.
                f5 = open('menu_updated.txt', 'a')
                f5.write(a + " " + b + ' ' + c + "가 신메뉴로 추가되었습니다"+'\n')
                # 메뉴의 이름, 가격, 재고를 각각 해당 리스트에 추가해줌
                menu.append(a)
                price.append(int(b))
                stock.append(int(c))
                servinglimit.append(int(c))
                f5.close()
                return False
            else:
                print('Wrong number...')
        # 계정추가를 선택한 경우
        if int(choise) == 2:
            newid = input('추가할 ID를 입력하세요.')
            newpw = input('추가할 ID의 password를 입력하세요.')
            f1 = open('Id.txt', 'a')
            f1. write('\n' + newid + ' ' + newpw)
            f1.close()
            # 추가된 아이디와 비밀번호를 id_updated.txt에 기록해준다.
            f2 = open('id_updated.txt', 'a')
            f2.write(newid + " " + newpw + "새로추가됨." + '\n')
            # 새로 추가된 아이디와 비밀번호를 해당 리스트에 추가해줌
            id.append(newid)
            pw.append(newpw)
            f2.close()
            print('새로운 아이디, 비밀번호 저장 완료')
            sys.exit()  # 프로그램을 종료해준다. sys 라이브러리속 exit 함수
        # 주문량 확인을 선택한 경우
        if int(choise) == 3:
            allplus = 0  # 총 매출액
            for a, b, c, d in zip(menu, price, stock, servinglimit):
                print(a, d - c)  # 메뉴명과 메뉴의 (초기량-재고=)주문량을 출력한다.
                allplus += b * (d - c)  # 총 매출액에 해당 메뉴의 가격과 주문량의 곱을 더해준다.
            print('총 매출액 :', format(allplus, ','))  # 총 매출액을 출력한다.
            return False
        # 4번 영업종료
        if int(choise) == 4:
            print('영업을 종료합니다.')
            sys.exit()
        # 5번 처음화면으로
        if int(choise) == 5:
            print('처음화면으로 돌아갑니다')
            login = False
        else:
            print('Wrong number.. Try again...')  # 1~5 이외의 숫자가 입력될 경우


# 1. Try to login (the list (id,passwd) from the id.txt)
# 2. If you Fall to log in -> try to log in (3번의 기회, 다끝나면 초기화면으로)
# 3. Change menu -> menu_updated.txt에 반영되어야함.
# 4. Id, passwd 추가 -> ip_updated.txt에 반영되어야함.
# 5. 주문량 확인 : 현재까지 판매된 메뉴별 갯수와 총 매출액
# 6. 영업 종료 여부 선택

closed = False
while not closed:
    print("Welcome to BME cafe...")
    print("*" * 65)
    print("1.주문")
    print("2.관리자 모드")
    print("*" * 65)

    choice = input("Choose the number:")
    if int(choice) == 1:
        closed = process_order(menu, price, stock)
    elif int(choice) == 2:
        closed = process_admin(ID, PW, menu, price, stock, servinglimit)
    else:
        print('Wrong number.. Try again...')

print("영업 종료..")
#  -> menu_updated.txt와 id_updated.txt 에 반영되어야함.
