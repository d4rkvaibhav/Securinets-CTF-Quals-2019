So for this challenge i used [GHIDRA](https://www.ghidra-sre.org/) as many people told me to give it a try.

Now coming to the challenge we have been provided an elf file ([rev.elf](rev.elf)).

On running the file it ask for a PASSWORD.I randomly typed something it says "ACCESS DENIED".

On decompiling the file with GHIDRA i got the main ,you can see the full file here [decompiled file](decompiled.txt).

In the starting of the code there are 3 while loops in which is basically storing data in an array.The loop is as folows (i have made some changes in the variable name of the decompiled code):

There is a line in decompiled code 

	*(int *)(&DAT_00302140 + ((long)local_2c * 6 + (long)local_28) * 4) = local_24 + 0x41;

which means that there is an array named DAT_00302140 and "* (int * )(&DAT_00302140 + ((long)local_2c * 6 + (long)local_28) * 4)" is equivalent to :
	
	DAT_00302140[((local_2c*6) +local_28)*4]=local_24 + 0x41;
Continuing to code:

	local_24 = 0;
	local_2c = 0;
	int arr[200]; //i made this variable substituion for DAT_00302140 in decompiled code
	while (local_2c < 5) {
    local_28 = 0;
    while (local_28 < 5) {
      if (local_24 == 9) {
        local_28 = local_28 + -1;
      }
      else {
        arr[((local_2c*6) +local_28)*4]=local_24 + 0x41;
      }
      local_24 = local_24 + 1;
      local_28 = local_28 + 1;
    }
    local_2c = local_2c + 1;
	}

So the array is intitialised now and then moving forward the code asks for the password (varibale name : DAT_003020a0).

i will use inp instead of DAT_003020a0 variable name.

It is  now check if len(inp)== 14 , So our input len should be 14.

Now again we have 3 while loop in the code :

The line :

	(*(int *)(&arr + ((long)local_24 * 6 + (long)local_28) * 4)==(int)(char)(&inp)[(long)local_2c])

will be equivalent to:

	arr[(local_24 * 6 + local_28)*4]==inp[local_2c]
	
	local_20 = 0;
    local_2c = 0;
	while( true ) 
      {
        sVar3 = strlen(inp);
        if (sVar3 <= (ulong)(long)local_2c)
        	break;
        char newarr[28];//i will use this for DAT_003021e0
        local_24 = 0;
        while (local_24 < 5) {
          local_28 = 0;
          while (local_28 < 5) {
            if (arr[(local_24 * 6 + local_28)*4]==inp[local_2c]) 
            {
              newarr[(long)local_20] = (char)local_24 + 'A';
              newarr[(long)(local_20 + 1)] = (char)local_28 + '1';
              local_20 = local_20 + 2;
            }
            local_28 = local_28 + 1;
          }
          local_24 = local_24 + 1;
        }
        local_2c = local_2c + 1;
      }
    local_2c = 0;

So we have out newarr string generated.

Now the while final loop is doing some shift and xor operations.

	local_2c = 0;
	char final[28]; //using this for DAT_00302100
	while( true ) {
        sVar3 = strlen(newarr);
        if (sVar3 <= (ulong)(long)local_2c) 
        	break;
        bVar1 = (byte)(local_2c >> 0x37);
        final[(long)local_2c] =newarr[(long)local_2c] ^ ((char)local_2c + (bVar1 >> 6) & 3) - (bVar1 >> 6);
        local_2c = local_2c + 1;
      }

Since local_2c can have max value of 28. local_2c>>0x37 will always be 0 and hence bvar1 =0 always.

bvar1>>6 will always be 0. so our new equation will be:

        final[local_2c] =newarr[local_2c]^(local_2c & 3)-0;

In the next step this final string in compared with "B0C2A2C6A3A7C5@6B5F0A4G2B5A2" So we have to reverse this string according to the above while loop to find the correct input.

I converted all the code in python and then reversed it.

On running the code the "arr" generated was :
	
	[65, 0, 0, 0, 66, 0, 0, 0, 67, 0, 0, 0, 68, 0, 0, 0, 69, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0, 71, 0, 0, 0, 72, 0, 0, 0, 73, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 77, 0, 0, 0, 78, 0, 0, 0, 79, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 81, 0, 0, 0, 82, 0, 0, 0, 83, 0, 0, 0, 84, 0, 0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 86, 0, 0, 0, 87, 0, 0, 0, 88, 0, 0, 0, 89, 0, 0, 0, 90]

To find the newarr we can write a reverse code (file name : [rev3.py](rev3.py)) :

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


The newarr came out to be B1A1A3A5A2C4C4B5B4D3A5E1B4C1.

Now Since we know "arr" as well as "newarr" we can now find the correct input doing some reversing in the second part of the code.i did the following in python (file name : [rev2.py](rev2.py)).

	i=0
	arr=[65, 0, 0, 0, 66, 0, 0, 0, 67, 0, 0, 0, 68, 0, 0, 0, 69, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0, 71, 0, 0, 0, 72, 0, 0, 0, 73, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 77, 0, 0, 0, 78, 0, 0, 0, 79, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 81, 0, 0, 0, 82, 0, 0, 0, 83, 0, 0, 0, 84, 0, 0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 86, 0, 0, 0, 87, 0, 0, 0, 88, 0, 0, 0, 89, 0, 0, 0, 90]
	password=['a']*14
	newarr="B1A1A3A5A2C4C4B5B4D3A5E1B4C1"

	while(i<28):
	  for j in range(5):
	    for k in range(5):
	      if((newarr[i] == chr(j+65)) and (newarr[i+1] == chr(k+49))):
	       password[i//2]=chr(arr[(j*6+k)*4])
	  i+=2
	password="".join(password)
	print(password)

And the password came out to be :

	FACEBOOKISEVIL

we have got the password now !!!!!!

It's time to find the flag.

I entered the password and flag came out :
	
	1337_FD_DDLLLKMO_KUWRRRVL_HAHAHA

It was a time consuming task for me as i generally don't do rev questions in my team .
