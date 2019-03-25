newarr=['a']*28
final="B0C2A2C6A3A7C5@6B5F0A4G2B5A2"
local_2c=0
while( True ):
  sVar3 = len(newarr)
  if (sVar3 <=local_2c):
    break
  bVar1 =(local_2c >> 0x37)
  newarr[local_2c]=chr(ord(final[local_2c])+(bVar1 >> 6)^(local_2c+(bVar1 >> 6) & 3))
  # final[local_2c]=chr(newarr[local_2c]^(local_2c+(bVar1 >> 6) & 3) - (bVar1 >> 6))
  local_2c = local_2c + 1
print(''.join(newarr))


