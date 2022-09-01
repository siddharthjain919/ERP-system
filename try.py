n=int(input())
c=0
for i in range(n):
	s=input()
	if len(s)<2:
		continue
	if s==s[::-1]:
		c+=1
	else:
		temp=len(s)//2
		temp=s[:temp]
		print(temp)
		if temp==temp[::-1]:
			c+=1
		else:
			temp=-(-len(s)//2)
			temp=s[temp:]
			print(temp)
			if temp==temp[::-1]:
				c+=1
print(c)
