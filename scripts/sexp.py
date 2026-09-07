import re
def parse(s):
    tok=re.finditer(r'"(?:[^"\\]|\\.)*"|\(|\)|[^\s()"]+', s)
    stack=[[]]
    for m in tok:
        t=m.group(0)
        if t=="(": stack.append([])
        elif t==")":
            l=stack.pop(); stack[-1].append(l)
        else:
            stack[-1].append(t[1:-1].replace('\\"','"') if t.startswith('"') else t)
    return stack[0]
def find(node, key):
    return [x for x in node if isinstance(x,list) and x and x[0]==key]
def find1(node,key):
    f=find(node,key); return f[0] if f else None
def prop(sym,name):
    for p in find(sym,"property"):
        if p[1]==name: return p[2]
    return None
def pins(sym):
    out=[]
    def walk(n):
        for x in n:
            if isinstance(x,list):
                if x and x[0]=="pin":
                    at=find1(x,"at"); ln=find1(x,"length"); nm=find1(x,"name"); num=find1(x,"number")
                    out.append(dict(num=num[1],name=nm[1],x=float(at[1]),y=float(at[2]),rot=float(at[3]) if len(at)>3 else 0.0,length=float(ln[1]),etype=x[1]))
                else: walk(x)
    walk(sym); return out
def load_lib(path):
    root=parse(open(path).read())[0]
    return {s[1]:s for s in find(root,"symbol")}
