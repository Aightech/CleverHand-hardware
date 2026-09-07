import re, uuid, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from sexp import parse, find, find1, prop, pins

LCSC_LIB="/home/adev/KICAD/kicad_libs/easyeda_library/00_lcsc.kicad_sym"
STD="/usr/share/kicad/symbols/"
LIBS={"00_lcsc":LCSC_LIB,"Device":STD+"Device.kicad_sym","power":STD+"power.kicad_sym",
      "Connector_Generic":STD+"Connector_Generic.kicad_sym","Connector":STD+"Connector.kicad_sym"}
_libtext={}; _libparsed={}
def libtext(lib):
    if lib not in _libtext: _libtext[lib]=open(LIBS[lib]).read()
    return _libtext[lib]
def libparsed(lib):
    if lib not in _libparsed:
        root=parse(libtext(lib))[0]; _libparsed[lib]={s[1]:s for s in find(root,"symbol")}
    return _libparsed[lib]
def symbol_text(lib,name):
    """raw text of a top-level symbol definition, with name prefixed by lib"""
    s=libtext(lib); key='(symbol "%s"'%name
    ms=list(re.finditer(r'\n[ \t]+'+re.escape(key)+r'(?=[\s)])',s))
    if not ms: raise KeyError(f"{lib}:{name}")
    m=ms[-1]
    i=m.end()-len(key); depth=0; j=i; instr=False
    while True:
        c=s[j]
        if instr:
            if c=='\\': j+=1
            elif c=='"': instr=False
        else:
            if c=='"': instr=True
            elif c=='(': depth+=1
            elif c==')':
                depth-=1
                if depth==0: break
        j+=1
    txt=s[i:j+1]
    return txt.replace(key,'(symbol "%s:%s"'%(lib,name),1)
def sym_pins(lib,name): return pins(libparsed(lib)[name])
def sym_prop(lib,name,p): return prop(libparsed(lib)[name],p)
def U(): return str(uuid.uuid4())
def f(v): return ("%.4f"%v).rstrip("0").rstrip(".") if isinstance(v,float) else str(v)
def esc(s): return s.replace('\\','\\\\').replace('"','\\"')

class Sheet:
    def __init__(s,project,title,paper="A3"):
        s.project=project; s.title=title; s.paper=paper; s.uuid=U()
        s.libsyms={}; s.items=[]; s.refcount={}
    def nextref(s,prefix):
        s.refcount[prefix]=s.refcount.get(prefix,0)+1; return f"{prefix}{s.refcount[prefix]}"
    def _prop(s,name,val,x,y,hide=False,justify=None):
        j=f"\n\t\t\t\t(justify {justify})" if justify else ""
        h="\n\t\t\t(hide yes)" if hide else ""
        return f'\t\t(property "{esc(name)}" "{esc(val)}"\n\t\t\t(at {f(x)} {f(y)} 0){h}\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t){j}\n\t\t\t)\n\t\t)\n'
    def wire(s,x1,y1,x2,y2):
        s.items.append(f'\t(wire\n\t\t(pts\n\t\t\t(xy {f(x1)} {f(y1)}) (xy {f(x2)} {f(y2)})\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid "{U()}")\n\t)\n')
    def label(s,name,x,y,rot=0,glob=False,shape="passive"):
        just={0:"left bottom",90:"left bottom",180:"right bottom",270:"right bottom"}[rot]
        if glob:
            s.items.append(f'\t(global_label "{esc(name)}"\n\t\t(shape {shape})\n\t\t(at {f(x)} {f(y)} {rot})\n\t\t(fields_autoplaced yes)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just.split()[0]})\n\t\t)\n\t\t(uuid "{U()}")\n\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"\n\t\t\t(at {f(x)} {f(y)} 0)\n\t\t\t(hide yes)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left)\n\t\t\t)\n\t\t)\n\t)\n')
        else:
            s.items.append(f'\t(label "{esc(name)}"\n\t\t(at {f(x)} {f(y)} {rot})\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{U()}")\n\t)\n')
    def noconnect(s,x,y):
        s.items.append(f'\t(no_connect\n\t\t(at {f(x)} {f(y)})\n\t\t(uuid "{U()}")\n\t)\n')
    def text(s,txt,x,y,size=1.5):
        s.items.append(f'\t(text "{esc(txt)}"\n\t\t(exclude_from_sim no)\n\t\t(at {f(x)} {f(y)} 0)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size {size} {size})\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "{U()}")\n\t)\n')
    def power(s,net,x,y,rot=0):
        x=round(x/1.27)*1.27; y=round(y/1.27)*1.27
        lib,name="power",net
        key=f"{lib}:{name}"
        if key not in s.libsyms: s.libsyms[key]=symbol_text(lib,name)
        ref=s.nextref("#PWR0")
        body=f'\t(symbol\n\t\t(lib_id "{key}")\n\t\t(at {f(x)} {f(y)} {rot})\n\t\t(unit 1)\n\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp no)\n\t\t(uuid "{U()}")\n'
        body+=s._prop("Reference",ref,x,y+6.35,hide=True)+s._prop("Value",net,x,y+3.81 if rot==0 and net=="GND" else y-3.81)+s._prop("Footprint","",x,y,True)+s._prop("Datasheet","",x,y,True)+s._prop("Description","",x,y,True)
        body+=f'\t\t(pin "1"\n\t\t\t(uuid "{U()}")\n\t\t)\n\t\t(instances\n\t\t\t(project "{s.project}"\n\t\t\t\t(path "/{s.uuid}"\n\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n'
        s.items.append(body)
    def part(s,prefix,lib,name,x,y,nets,value=None,footprint=None,lcsc=None,rot=0,stub=2.54,ref=None,glob_nets=(),desc=None,labelall=True):
        """nets: {pin_number: net}; net = 'NAME' | 'G:NAME' (global) | 'P:+3.3V' (power symbol) | 'NC' ; pins not listed are left open"""
        key=f"{lib}:{name}"
        if key not in s.libsyms: s.libsyms[key]=symbol_text(lib,name)
        ref=ref or s.nextref(prefix)
        value=value or sym_prop(lib,name,"Value") or name
        footprint=footprint if footprint is not None else (sym_prop(lib,name,"Footprint") or "")
        ds=sym_prop(lib,name,"Datasheet") or ""
        assert rot==0, "only rotation 0 supported"
        x=round(x/1.27)*1.27; y=round(y/1.27)*1.27
        ps=sym_pins(lib,name)
        xs=[p['x'] for p in ps]; ys=[p['y'] for p in ps]
        w=(max(xs)-min(xs)) if ps else 10; h=(max(ys)-min(ys)) if ps else 5
        body=f'\t(symbol\n\t\t(lib_id "{key}")\n\t\t(at {f(x)} {f(y)} 0)\n\t\t(unit 1)\n\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp no)\n\t\t(uuid "{U()}")\n'
        if lib=="Device" and name in ("R","C","L"):
            body+=s._prop("Reference",ref,x+1.6,y-1.4,justify="left")+s._prop("Value",value,x+1.6,y+1.4,justify="left")
        elif prefix in ("TP","#PWR0"):
            body+=s._prop("Reference",ref,x,y-2.54)+s._prop("Value",value,x,y+2.54)
        else:
            body+=s._prop("Reference",ref,x-w/2,y-h/2-2.5,justify="left")+s._prop("Value",value,x-w/2,y+h/2+2.5,justify="left")+s._prop("Footprint",footprint,x,y,True,"left")+s._prop("Datasheet",ds,x,y,True,"left")+s._prop("Description",desc or (sym_prop(lib,name,"Description") or ""),x,y,True)
        if lcsc: body+=s._prop("LCSC",lcsc,x,y,True)
        for p in ps:
            body+=f'\t\t(pin "{esc(p["num"])}"\n\t\t\t(uuid "{U()}")\n\t\t)\n'
        body+=f'\t\t(instances\n\t\t\t(project "{s.project}"\n\t\t\t\t(path "/{s.uuid}"\n\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n'
        s.items.append(body)
        # nets
        seen=set()
        for p in ps:
            if p['num'] in seen: continue
            seen.add(p['num'])
            net=nets.get(p['num'])
            if net is None: continue
            px,py=x+p['x'],y-p['y']
            r=int(p['rot'])%360
            dx,dy={0:(-1,0),180:(1,0),90:(0,1),270:(0,-1)}[r]
            if net=="NC":
                s.noconnect(px,py); continue
            st=stub*2 if net.startswith('P:') else stub
            ex,ey=px+dx*st,py+dy*st
            s.wire(px,py,ex,ey)
            if net.startswith("P:"):
                pw=net[2:]
                s.power(pw,ex,ey,0)
            else:
                g=net.startswith("G:"); nm=net[2:] if g else net
                lrot={(-1,0):180,(1,0):0,(0,1):270,(0,-1):90}[(dx,dy)]
                shape="input"
                s.label(nm,ex,ey,lrot,glob=g or (nm in glob_nets),shape=shape)
        return ref
    def flag(s,net,x,y):
        x=round(x/1.27)*1.27; y=round(y/1.27)*1.27
        s.power(net,x,y,0)
        s.power("PWR_FLAG",x,y,0)
    def passive(s,kind,value,x,y,net1,net2,size="0201",lcsc=None):
        lib="Device"; name={"C":"C","R":"R","L":"L"}[kind]
        fp={"C":{"0201":"Capacitor_SMD:C_0201_0603Metric","0402":"Capacitor_SMD:C_0402_1005Metric","0603":"Capacitor_SMD:C_0603_1608Metric"},
            "R":{"0201":"Resistor_SMD:R_0201_0603Metric","0402":"Resistor_SMD:R_0402_1005Metric","0805":"Resistor_SMD:R_0805_2012Metric"},
            "L":{"0201":"Inductor_SMD:L_0201_0603Metric","0402":"Inductor_SMD:L_0402_1005Metric"}}[kind][size]
        return s.part(kind,lib,name,x,y,{"1":net1,"2":net2},value=value,footprint=fp,lcsc=lcsc,stub=1.27)
    def write(s,path):
        out=f'(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n\t(uuid "{s.uuid}")\n\t(paper "{s.paper}")\n\t(title_block\n\t\t(title "{esc(s.title)}")\n\t\t(date "2026-09-05")\n\t\t(rev "0.1")\n\t\t(company "Aightech")\n\t\t(comment 1 "generated draft: parts placed and netted by labels, layout to be tidied")\n\t)\n\t(lib_symbols\n'
        for k,t in s.libsyms.items():
            out+="\t\t"+t.replace("\n","\n\t")+"\n"
        out+="\t)\n"+"".join(s.items)
        out+='\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n\t(embedded_fonts no)\n)\n'
        open(path,"w").write(out)

def write_project(dirpath,name,sheet,template_pro,template_pcb,libtables=None):
    os.makedirs(dirpath,exist_ok=True)
    j=json.load(open(template_pro))
    j["meta"]["filename"]=f"{name}.kicad_pro"
    j["sheets"]=[[sheet.uuid,"Root"]]
    for k in ("boards",): j[k]=[]
    json.dump(j,open(os.path.join(dirpath,f"{name}.kicad_pro"),"w"),indent=2)
    # pcb: keep header items only, copied verbatim (re-serializing would lose string quoting)
    s=open(template_pcb).read()
    keep=("version","generator","generator_version","general","paper","layers","setup")
    out="(kicad_pcb\n"
    i=s.index("(kicad_pcb")+len("(kicad_pcb")
    while i<len(s):
        j=s.find("(",i)
        if j<0: break
        # read head token
        m=re.match(r'\(([A-Za-z_]+)',s[j:])
        depth=0; k=j; instr=False
        while True:
            c=s[k]
            if instr:
                if c=='\\': k+=1
                elif c=='"': instr=False
            else:
                if c=='"': instr=True
                elif c=='(': depth+=1
                elif c==')':
                    depth-=1
                    if depth==0: break
            k+=1
        if m and m.group(1) in keep: out+="\t"+s[j:k+1].strip()+"\n"
        i=k+1
        if s[j-1:j]=="" : break
    out+='\t(net 0 "")\n)\n'
    out=out.replace("(version 20241229)","(version 20260206)").replace('(generator_version "9.0")','(generator_version "10.0")')
    out=out.replace('(title "Com. module")',f'(title "{name}")')
    open(os.path.join(dirpath,f"{name}.kicad_pcb"),"w").write(out)
    if libtables:
        rel=libtables
        open(os.path.join(dirpath,"sym-lib-table"),"w").write(f'(sym_lib_table\n  (version 7)\n  (lib (name "clvhd_stack")(type "KiCad")(uri "${{KIPRJMOD}}/{rel}/clvhd_stack.kicad_sym")(options "")(descr "CleverHand stack field symbols"))\n)\n')
        open(os.path.join(dirpath,"fp-lib-table"),"w").write(f'(fp_lib_table\n  (version 7)\n  (lib (name "clvhd_stack")(type "KiCad")(uri "${{KIPRJMOD}}/{rel}/clvhd_stack.pretty")(options "")(descr "CleverHand stack field footprints"))\n)\n')
