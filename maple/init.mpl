with(combstruct):
DistanceHereditary:={SX=Prod(Union(Z,C,SC),Set(Union(Z,C,SX),card>=1)),SC=Set(Union(Z,C,SX),card>=2),C=Set(Union(Z,SC,SX),card>=2)}:
Order:=12: 
OGF:=gfeqns(DistanceHereditary,unlabeled,z):
OGS:=gfseries(DistanceHereditary,unlabeled,z):
acc:=1000:
cpoly:=add(count([C,DistanceHereditary,unlabeled],size=i)*z^i,i=0..acc):
dcpoly:=add(i*count([C,DistanceHereditary,unlabeled],size=i)*z^(i-1),i=0..acc):
d2cpoly:=add(i*(i-1)*count([C,DistanceHereditary,unlabeled],size=i)*z^(i-2),i=0..acc):
sxpoly:=add(count([SX,DistanceHereditary,unlabeled],size=i)*z^i,i=0..acc):
dsxpoly:=add(i*count([SX,DistanceHereditary,unlabeled],size=i)*z^(i-1),i=0..acc):
xdsxpoly:=expand(z*dsxpoly):
d2sxpoly:=add(i*(i-1)*count([SX,DistanceHereditary,unlabeled],size=i)*z^(i-2),i=0..acc):
scpoly:=add(count([SC,DistanceHereditary,unlabeled],size=i)*z^i,i=0..acc):
dscpoly:=add(i*count([SC,DistanceHereditary,unlabeled],size=i)*z^(i-1),i=0..acc):
d2scpoly:=add(i*(i-1)*count([SC,DistanceHereditary,unlabeled],size=i)*z^(i-2),i=0..acc):
xddhpoly:=expand(z*(sxpoly+scpoly+cpoly) + z^2*subs(z=z^2,dsxpoly) + z^2*subs(z=z^2,dscpoly) + z*(1+dcpoly+dscpoly+dsxpoly) - z*(1+dscpoly+dsxpoly)*(1+z+cpoly+scpoly+sxpoly) - z^2*(1+subs(z=z^2,dsxpoly)+subs(z=z^2,dscpoly)) + (z+cpoly+scpoly)*(z*(1+dcpoly+dscpoly+dsxpoly) - z*(1+dcpoly+dsxpoly)*(1+z+cpoly+scpoly+sxpoly))):
dhpoly:=add(coeff(xddhpoly, z, i)/i*z^i,i=1..acc):
sx:=proc(x) eval(sxpoly,z=x); end proc:
dsx:=proc(x) eval(dsxpoly,z=x); end proc:
xdsx:=proc(x) x*dsx(x); end proc:
d2sx:=proc(x) eval(d2sxpoly,z=x); end proc:
sc:=proc(x) eval(scpoly,z=x); end proc:
dsc:=proc(x) eval(dscpoly,z=x); end proc:
d2sc:=proc(x) eval(d2scpoly,z=x); end proc:
c:=proc(x) eval(cpoly,z=x); end proc:
dc:=proc(x) eval(dcpoly,z=x); end proc:
d2c:=proc(x) eval(d2cpoly,z=x); end proc:
xcsx:=proc(x) x+c(x)+sx(x); end proc:
xscsx:=proc(x) x+sc(x)+sx(x); end proc:
dxcsx:=proc(x) 1+dc(x)+dsx(x); end proc:
dxscsx:=proc(x) 1+dsc(x)+dsx(x); end proc:
xddh:=proc(x) eval(xddhpoly,z=x); end proc:
dh:=proc(x) eval(dhpoly,z=x); end proc:
read "proba_laws.mpl":
max_index:=proc(A, x) local U,v,k,j; U := random(); k := 0; v := 1/evalf(exp(Sum(A(x^j)/j,j=1..infinity))); while v < U do k := k+1; v := v * (evalf(exp(A(x^k)/k))); od; return k; end proc:
max_index_geq_1:=proc(A, x) local U,v,c,k,j; U:=random(); k:=1; v:=evalf(exp(A(x))); c:=1/evalf(exp(Sum(A(x^j)/j,j=1..infinity))-1); while (v-1)*c < U do k:=k+1; v:=v*evalf(exp(A(x^k)/k)); od; return k; end proc:
gen_set_of:=proc(x, inner_oracle, inner_gen, length_lower_bound) local S,i,j,J,k,kJ,t,copy; S:=NULL; if length_lower_bound <= 0 then J:=max_index(inner_oracle, x); if J <> 0 then kJ:=non_zero_poiss(inner_oracle(x^J)/J); end if; elif length_lower_bound = 1 then J:=max_index_geq_1(inner_oracle, x); kJ:=non_zero_poiss(inner_oracle(x^J)/J); elif length_lower_bound = 2 then do J:=max_index_geq_1(inner_oracle,x); kJ:=non_zero_poiss(inner_oracle(x^J)/J); if J>1 or kJ>1 then break; end if; od; else error "not implemented" end if; for j from 1 to J do if j < J then k:=poiss(inner_oracle(x^j)/j); else k:=kJ; end if; for i from 1 to k do t:=inner_gen(x^j); for copy from 1 to j do S:=S,t; od; od; od; return S end proc:
bern_option:=proc(a, b, c) if bern(a/(a+b+c))=1 then 0; elif bern(b/(b+c))=1 then 1; else 2; end if; end proc:
gen_xcsc:=proc(x) local n; n:=bern_option(x, c(x), sc(x)); return piecewise(n=0, Z, n=1, gen_c(x), n=2, gen_sc(x)); end proc:
gen_xcsx:=proc(x) local n; n:=bern_option(x, c(x), sx(x)); return piecewise(n=0, Z, n=1, gen_c(x), n=2, gen_sx(x)); end proc:
gen_xscsx:=proc(x) local n; n:=bern_option(x, sc(x), sx(x)); return piecewise(n=0, Z, n=1, gen_sc(x), n=2, gen_sx(x)); end proc:
gen_sx:=proc(x) local gamma,n; gamma:=gen_xcsc(x); return SX(gamma, gen_set_of(x, xcsx, gen_xcsx, 1)); end proc:
gen_sc:=proc(x) return SC(gen_set_of(x, xcsx, gen_xcsx, 2)); end proc:
gen_c:=proc(x) return C(gen_set_of(x, xscsx, gen_xscsx, 2)); end proc:
root_cycle_size:=proc(x, d_inner_oracle) local U,c,k,v,j; U:=random(); k:=0; v:=0; c:=evalf(Sum(x^j*d_inner_oracle(x^j),j=1..infinity)); while v < c*U do k:=k+1; v:=v+x^k*d_inner_oracle(x^k); end do; return k; end proc:
root_cycle_size_geq_2:=proc(x, d_inner_oracle) local U,c,k,v,j; U:=random(); k:=1; v:=0; c:=evalf(Sum(x^j*d_inner_oracle(x^j),j=2..infinity)); while v < c*U do k:=k+1; v:=v+x^k*d_inner_oracle(x^k); end do; return k; end proc:
gen_cycle_pointed_set_of:=proc(x, inner_oracle, d_inner_oracle, inner_gen, inner_gen_cycle_pointed, length_lower_bound, symmetric) local K,gamma,S,copy,j; S:=NULL; if symmetric then if length_lower_bound <= 2 then K:=root_cycle_size_geq_2(x, d_inner_oracle); S:=gen_set_of(x, inner_oracle, inner_gen, 0); elif length_lower_bound = 3 then do K:=root_cycle_size_geq_2(x, d_inner_oracle); S:=gen_set_of(x, inner_oracle, inner_gen, 0); if K>2 or S<>NULL then break; end if; od; else error "not implemented" end if; else if length_lower_bound <= 1 then K:=root_cycle_size(x, d_inner_oracle); S:=gen_set_of(x, inner_oracle, inner_gen, 0); elif length_lower_bound = 2 then do K:=root_cycle_size(x, d_inner_oracle); S:=gen_set_of(x, inner_oracle, inner_gen, 0); if K>1 or S<>NULL then break; end if; od; else error "not implemented" end if; end if; gamma:=inner_gen_cycle_pointed(x^K); for copy from 1 to K do S:=S,gamma; od; return S end proc:
gen_xcsc_cycle_pointed:=proc(x) local n; n:=bern_option(x, x*dc(x), x*dsc(x)); return piecewise(n=0, Z, n=1, gen_c_cycle_pointed(x), n=2, gen_sc_cycle_pointed(x)); end proc:
gen_xcsx_cycle_pointed:=proc(x) local n; n:=bern_option(x, x*dc(x), x*dsx(x)); return piecewise(n=0, Z, n=1, gen_c_cycle_pointed(x), n=2, gen_sx_cycle_pointed(x)); end proc:
gen_xscsx_cycle_pointed:=proc(x) local n; n:=bern_option(x, x*dsc(x), x*dsx(x)); return piecewise(n=0, Z, n=1, gen_sc_cycle_pointed(x), n=2, gen_sx_cycle_pointed(x)); end proc:
gen_sx_cycle_pointed:=proc(x) local gamma,S,j; if bern(((x+x*dc(x)+x*dsc(x))*(evalf(exp(Sum((x^j + c(x^j) + sx(x^j))/j,j=1..infinity))) - 1))/(x*dsx(x)))=1 then gamma:=gen_xcsc_cycle_pointed(x); S:=gen_set_of(x, xcsx, gen_xcsx, 1); return SX(gamma, S); else gamma:=gen_xcsc(x); S:=gen_cycle_pointed_set_of(x, xcsx, dxcsx, gen_xcsx, gen_xcsx_cycle_pointed, 1, false); return SX(gamma, S); end if; end proc:
gen_sc_cycle_pointed:=proc(x) return SC(gen_cycle_pointed_set_of(x, xcsx, dxcsx, gen_xcsx, gen_xcsx_cycle_pointed, 2, false)); end proc:
gen_c_cycle_pointed:=proc(x) return C(gen_cycle_pointed_set_of(x, xscsx, dxscsx, gen_xscsx, gen_xscsx_cycle_pointed, 2, false)); end proc:
gen_cscsx:=proc(x) local n; n:=bern_option(c(x), sc(x), sx(x)); return piecewise(n=0, gen_c(x), n=1, gen_sc(x), n=2, gen_sx(x)); end proc:
gen_dh_cycle_pointed:=proc(x) local tau; if bern((x*(sx(x)+sc(x)+c(x)))/(xddh(x)))=1 then return Z(gen_cscsx(x)) elif bern((x^2*dsx(x^2))/(xddh(x) - x*(sx(x)+sc(x)+c(x))))=1 then tau:=gen_sx_cycle_pointed(x^2); return e(tau, tau); elif bern((x^2*dsc(x^2))/(xddh(x) - x*(sx(x)+sc(x)+c(x)) - x^2*dsx(x^2)))=1 then tau:=gen_sc_cycle_pointed(x^2); return e(tau, tau); elif bern((x*(1+dc(x)+dsc(x)+dsx(x)) - x*(1+dsc(x)+dsx(x))*(1+x+c(x)+sc(x)+sx(x)) - x^2*(1+dsx(x^2)+dsc(x^2)))/(xddh(x) - x*(sx(x)+sc(x)+c(x)) - x^2*dsx(x^2) - x^2*dsc(x^2)))=1 then return CR(gen_cycle_pointed_set_of(x, xscsx, dxscsx, gen_xscsx, gen_xscsx_cycle_pointed, 3, true)); else return SR(gen_xcsc(x), gen_cycle_pointed_set_of(x, xcsx, dxcsx, gen_xcsx, gen_xcsx_cycle_pointed, 2, true)); end if; end proc: