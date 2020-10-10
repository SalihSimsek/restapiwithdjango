import random
def create_slug():
    slug = ''
    while len(slug)<21:
        a = random.randint(0,2)
        if(a==0):
            buyuk=random.randint(65,90)
            slug+= chr(buyuk)
        elif(a==1):
            kucuk = random.randint(97,122)
            slug+= chr(kucuk)
        elif(a==2):
            sayi = random.randint(0,9)
            slug+=str(sayi)
    return slug