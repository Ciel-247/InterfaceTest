sStr1 = 'ab,cde,fgh,ijk'
sStr2 = ','
sStr3 = 'ijk'
sStr1 = sStr1[sStr1.find(sStr2) + 1:sStr1.find(sStr3)]
print (sStr1)
if __name__ == "__main__":
    pass