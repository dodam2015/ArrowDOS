import math
allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

print("---calculator---")
print("종료하려면 'exit'를 입력하세요.")

while True:
    try:
        expr = input("입력 >").strip()
        
        if expr.lower() in ['exit', 'quit']:
            print("계산기를 종료합니다.")
            break
            
        if not expr: continue

        # 수식 계산 실행
        result = eval(expr, {"__builtins__": None}, allowed_names)
        print(f"결과: {result}")

    except Exception as e:
        print(f"오류: {e}")