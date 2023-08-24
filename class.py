class rabbit:
    def __init__(self):
        self.num = int(input("번호 입력"))
        self.name = input("이름 입력")
    def check(self):
        print(self.num, self.name, "출석체크!")
    def score(self, score):
        if score < 40:
            grade = "C"
        elif 40 <= score < 80: 
            grade = "B"
        else:
            grade = "A"
        print("{}점이고 학점은 {}입니다." .format(score, grade))

a = rabbit()
b = rabbit()
print("{}번 이름: {}" .format(a.num, a.name))
print("{}번 이름: {}" .format(b.num, b.name))
a.check()    
b.check()
a.score(20)
b.score(60)