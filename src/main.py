import math



class Complex:
	def __init__(self,r=0,i=0):
		self.r=r
		self.i=i
	def __repr__(self):
		r=round(self.r,8)
		i=round(self.i,8)
		if (i==0):
			if (r%1==0):
				return str(int(r))
			return str(r)
		if (r==0):
			return str(i)+"j"
		return f"{r} {i}j"



def encode(M,v):
	A=[]
	o=[None for _ in range(0,M)]
	a=math.pi/M
	b=a*2
	for i in range(0,M):
		r=[Complex(1,0)]
		c=a
		for j in range(1,M):
			r.append(Complex(math.cos(c),math.sin(c)))
			c+=a
		A.append(r)
		a+=b
		o[i]=Complex(v[i],0)
	for i in range(0,M):
		c=A[i][i]
		n=c.r**2+c.i**2
		f=Complex(c.r/n,-c.i/n)
		for j in range(0,M):
			if (i!=j):
				c=A[j][i]
				r=Complex(c.r*f.r-c.i*f.i,c.r*f.i+c.i*f.r)
				for k in range(0,M):
					c=A[i][k]
					A[j][k].r-=r.r*c.r-r.i*c.i
					A[j][k].i-=r.r*c.i+r.i*c.r
				c=o[i]
				o[j].r-=r.r*c.r-r.i*c.i
				o[j].i-=r.r*c.i+r.i*c.r
			if (i==M-1):
				c=A[j][j]
				d=c.r**2+c.i**2
				t=o[j].r*c.r+o[j].i*c.i
				o[j].i=(o[j].i*c.r-o[j].r*c.i)/d
				o[j].r=t/d
	return o



def decode(M,p):
	o=[None for _ in range(0,M)]
	a=math.pi/M
	b=a*2
	for i in range(0,M):
		v=Complex(p[0].r,p[0].i)
		c=a
		for j in range(1,M):
			cr=math.cos(c)
			ci=math.sin(c)
			v.r+=p[j].r*cr-p[j].i*ci
			v.i+=p[j].r*ci+p[j].i*cr
			c+=a
		o[i]=v
		a+=b
	return o



def add_poly(a,b,M):
	o=[None for _ in range(0,M)]
	for i in range(0,M):
		o[i]=Complex(a[i].r+b[i].r,a[i].i+b[i].i)
	return o



def mult_poly(a,b,M):
	o=[None for _ in range(0,M*2-1)]
	for i in range(0,M*2-1):
		o[i]=Complex(0,0)
	for i in range(0,M):
		c=a[i]
		for j in range(0,M):
			o[i+j].r+=c.r*b[j].r-c.i*b[j].i
			o[i+j].i+=c.r*b[j].i+c.i*b[j].r
	for i in range(M*2-2,M-1,-1):
		o[i-M].r-=o[i].r
		o[i-M].i-=o[i].i
	return o[:M]



M=4
u=encode(M,[1,2,3,4])
v=encode(M,[-1,2,3,-4])
out=add_poly(u,v,M)
print(out,decode(M,out))
out=mult_poly(u,v,M)
print(out,decode(M,out))
