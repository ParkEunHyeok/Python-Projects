import sys

# 가격은 100원 단위이므로 상수 값을 100으로 선언
PRICE_UNIT = 100

class texts:
    # 관리하기 편하도록 클래스로 만듦.
    title           = "#### 클래스 %s 자판기 입니다. ####"
    product         = "%s:%s(%s원)"
    insert_coin     = "동전을 넣어 주세요. : "
    n_enough_coin   = "동전이 부족합니다.\n거스름돈은 %s원 입니다."
    select_product  = "원하시는 상품번호를 선택하세요."
    select_fault    = "잘못 누르셨습니다."
    product_out     = "선택하신 %s입니다. 거스름돈은 %s원입니다.\n감사합니다."

class Product:
    # 제품 종류, 가격을 코드 변경 없이 데이터를 쉽게 추가하거나 변경할 수 있다.#
    # 밑의 로직을 바꾸지 않기 위해 빈 배열 형태로 선언함.
    # productType     = {"1":"설탕커피", "2":"설탕커피", "3":"원두커피"}
    productType = []
    # productValue    = {"1":200, "2":300, "3":400}
    productValue = []

# Product 클래스를 상속받음.    
class CoffeeVM(Product):
    _product_info_file = "coffee.txt"
    _name = "커피"

    def __init__(self):
        # 사용자가 자판기 종류를 선택하면 _name 출력한다.
        print(texts.title %self._name)

    def set_products(self):
        # 제품 종류, 가격 리스트를 초기화한다.
        Product.productType = []
        Product.productValue = []

        with open(self._product_info_file, "r", encoding="UTF-8") as fd:
            for line in fd:
                # 라인 끝에 있는 \n을 제거하고 , 로 구분하는 리스트를 만든다.       
                list = line.strip('\n').split(',')
                # 제품 종류, 가격 리스트에 필요한 값을 입력받는다.
                Product.productType.append((list[0]+','+list[1]))
                Product.productValue.append((list[0]+','+list[2]))
 
    def run(self):
        self.set_products()

        while True:
            try:
                inputCoin = float(input(texts.insert_coin))
            except:
                # 잘못된 값을 입력받으면 에러 메시지를 출력한다.
                print(texts.select_fault)
            else:
                self.selectProduct(inputCoin)

    def selectProduct(self, coin):
        # 제품 종류를 리스트로 선언하여 코드변경없이 데이터를 동적으로 보여준다.
        description = ''
        for selection, item in Product.productType.items():
            # 제품 가격을 가져온다.
            price  = self.getProductValue(selection)
            description += selection+' : '+item+'('+str(price)+'원)'

        print(description)
        inputProduct = input(texts.select_product)
        productValue = self.getProductValue(inputProduct)

        # 입력한 값에 해당하는 내용이 리스트에 없으면 0 반환
        if productValue:
            productName = self.getProductName(inputProduct)
            self.payment(coin, productName, productValue)
        else:
            # 잘못된 값을 입력받으면 에러 메시지를 출력하고 제품 선택 메뉴로 이동한다.
            print(texts.select_fault)
            self.selectProduct(coin)

    def getProductValue(self, product):
        returnValue = 0
        for selection, value in Product.productValue.items():
            if selection == product:
                returnValue = value
        return returnValue 

    def getProductName(self, product):
        for selection, name in Product.productType.items():
            if selection == product:
                return name
    
    def payment(self, coin, name, value):
        coinValue = coin * PRICE_UNIT
        if coinValue >= value:
            balance = coinValue - value
            print(texts.product_out %(name, int(balance)))
        else:
            print(texts.n_enough_coin %int(coinValue))
        # 지불을 마치면 초기 메뉴로 이동한다.
        self.run()


# 과자 클래스는 커피 클래스를 상속받는다.
class SnackVM(CoffeeVM):
    _product_info_file = "snack.txt"
    _name = "과자"

    def __init__(self): 
        # Product 제품 종류, 가격을 Overriding 한다
        Product.productType = {"1":"오감자", "2":"오징어땅콩", "3":"빼뺴로", "4":"칸쵸"}
        Product.productValue = {"1":400, "2":400, "3":600, "4":500}
        # 사용자가 자판기 종류를 선택하면 _name 출력한다.
        print(texts.title %self._name)

    
if __name__ == '__main__':
    print("1:커피, 2:과자")
    select_vm = input("구동할 자판기를 선택하세요.").strip()

    if select_vm =="1":
        vm = CoffeeVM()

    elif select_vm == "2":
        vm = SnackVM()

    else:
        print("잘못 누르셨습니다. 다시 실행 해주세요.")
        sys.exit(-1)

    try:
        vm.run()
    
    except KeyboardInterrupt as exc:
        print("판매를 종료합니다.")
