import math



class Complex:
	def __init__(self,r,i):
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
		if (i<0):
			return f"{r}{i}j"
		return f"{r}+{i}j"



def calc_matrix(M):
	o=[None for _ in range(0,M*M)]
	a=math.pi/M
	b=a*2
	i=0
	for j in range(0,M):
		o[i]=Complex(1,0)
		i+=1
		c=a
		for k in range(1,M):
			o[i]=Complex(math.cos(c),math.sin(c))
			i+=1
			c+=a
		a+=b
	return o



def encode(M,N,v):
	m=[Complex(e.r,e.i) for e in N]
	o=[None for _ in range(0,M)]
	ii=0
	for i in range(0,M):
		c=m[ii+i]
		n=c.r**2+c.i**2
		f=Complex(c.r/n,-c.i/n)
		jj=0
		for j in range(0,M):
			if (i==0):
				o[j]=Complex(v[j],0)
			if (i!=j):
				c=m[jj+i]
				r=Complex(c.r*f.r-c.i*f.i,c.r*f.i+c.i*f.r)
				for k in range(0,M):
					c=m[ii+k]
					m[jj+k].r-=r.r*c.r-r.i*c.i
					m[jj+k].i-=r.r*c.i+r.i*c.r
				c=o[i]
				o[j].r-=r.r*c.r-r.i*c.i
				o[j].i-=r.r*c.i+r.i*c.r
			if (i==M-1):
				c=m[jj+j]
				d=c.r**2+c.i**2
				t=o[j].r*c.r+o[j].i*c.i
				o[j].i=(o[j].i*c.r-o[j].r*c.i)/d
				o[j].r=t/d
			jj+=M
		ii+=M
	return o



def decode(M,N,p):
	o=[None for _ in range(0,M)]
	ii=0
	for i in range(0,M):
		if (abs(p[0].i)>1e-8):
			raise RuntimeError
		v=Complex(p[0].r,0)
		for j in range(1,M):
			k=ii+j
			v.r+=p[j].r*N[k].r-p[j].i*N[k].i
			v.i+=p[j].r*N[k].i+p[j].i*N[k].r
		o[i]=v
		ii+=M
	return o



def add_poly(a,b,M):
	o=[None for _ in range(0,M)]
	for i in range(0,M):
		o[i]=Complex(a[i].r+b[i].r,a[i].i+b[i].i)
	return o



def mult_poly(a,b,M):
	o=[None for _ in range(0,M)]
	for i in range(0,M):
		o[i]=Complex(0,0)
	for i in range(0,M):
		c=a[i]
		k=i
		for j in range(0,M):
			cr=c.r*b[j].r-c.i*b[j].i
			ci=c.r*b[j].i+c.i*b[j].r
			if (k>=M):
				l=k-M
				o[l].r-=cr
				o[l].i-=ci
			else:
				o[k].r+=cr
				o[k].i+=ci
			k+=1
	return o[:M]



M=4
N=calc_matrix(M)
u=encode(M,N,[1,2,3,4])
v=encode(M,N,[-1,2,3,-4])
out=add_poly(u,v,M)
print(out,decode(M,N,out))
out=mult_poly(u,v,M)
print(out,decode(M,N,out))
