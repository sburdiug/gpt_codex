
def makeGray(W,H,VAL=128):
    IMG = []
    for Y in range(H):
        ROW = []
        for X in range(W):
            ROW.append(VAL)
        IMG.append(ROW)
    return IMG

def bright(imgArr, deltaVal=10):
    OUT = []
    for y in range(len(imgArr)):
        row = []
        for x in range(len(imgArr[0])):
            v = imgArr[y][x] + deltaVal
            if v > 255: v = 255
            row.append(v)
        OUT.append(row)
    return OUT

def Brighten(imgArr, deltaVal=10):
    OUT = []
    for y in range(len(imgArr)):
        row = []
        for x in range(len(imgArr[0])):
            v = imgArr[y][x] + deltaVal
            if v > 255: v = 255
            row.append(v)
        OUT.append(row)
    return OUT

def BLUR(IMG):
    h = len(IMG); w = len(IMG[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            s = 0; c = 0
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    ny = y+dy; nx = x+dx
                    if 0<=ny<h and 0<=nx<w:
                        s += IMG[ny][nx]; c += 1
            row.append(s//c)
        out.append(row)
    return out

if __name__ == "__main__":
    im = makeGray(10,5,100)
    im = bright(im,30)
    im = BLUR(im)
    print(im[0][0])
