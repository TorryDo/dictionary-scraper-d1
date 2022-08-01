
n1: float = 1000
n2: int = 1852


if __name__ == '__main__':
    result = n1/n2
    result = round(number=result, ndigits=2) * 100
    print(str(int(result)))
