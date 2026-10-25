"""Gera a folha de sprites do Reino da Brasa (Lenda da Brasa).
Saídas: lenda-da-brasa-sprites.png (1x, pronto pro jogo), lenda-da-brasa-atlas.json,
lenda-da-brasa-preview.png (4x com nomes) e lenda-da-brasa-sprites.zip (PNGs individuais)."""
from PIL import Image, ImageDraw, ImageFont
import json, os, zipfile, io, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites')

PAL_HEX = {
 'k':'#1a1210','h':'#c9461f','H':'#f0843c','s':'#f0c49a','S':'#c98e6a','t':'#3d5566','T':'#29394a','o':'#f0a030',
 'b':'#5a3a22','w':'#fff6e6','y':'#e8b04a','Y':'#ffe08a','r':'#e0402a','R':'#8a2410','e':'#e8742a','E':'#ffb04a',
 'n':'#7a4a26','N':'#4a2e1a','a':'#6e6260','A':'#4a403e','i':'#7a6c78','I':'#9a8c98','P':'#a89aa6','d':'#4e4450',
 'x':'#120b0c','X':'#2e2226','z':'#6a3a5a','Z':'#8a5276','L':'#d8b4f0','l':'#a87ac8','Q':'#c8487a','O':'#f08ab0',
 'K':'#b0603a','B':'#7a3a22','W':'#ffd0a0','g':'#efe6da','c':'#8ad4e8','u':'#4a8ac4','v':'#6ec070','G':'#b8b0a8',
}
def rgba(h):
    if h.startswith('rgba'): return h
    h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),255)
PAL={k:rgba(v) for k,v in PAL_HEX.items()}

def grid(rows, size=(16,16), ox=0, oy=0, pal=PAL):
    img=Image.new('RGBA',size,(0,0,0,0)); px=img.load()
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch in pal and 0<=x+ox<size[0] and 0<=y+oy<size[1]: px[x+ox,y+oy]=pal[ch]
    return img

BAD=[]
def mirror(name, half, rmap=None):
    rmap=rmap or {}
    w=len(half[0]); rows=[]
    for i,r in enumerate(half):
        if len(r)!=w: BAD.append((name,i,r,len(r))); r=r.ljust(w,'.')[:w]
        rows.append(r+''.join(rmap.get(c,c) for c in reversed(r)))
    return rows

def check(name, rows, w):
    for i,r in enumerate(rows):
        if len(r)!=w: BAD.append((name,i,r,len(r)))
    return rows

def recolor(img, mapping):
    """troca cores: mapping {chave_paleta_origem: chave_destino ou tupla rgba}"""
    out=img.copy(); px=out.load()
    m={PAL[a]:(PAL[b] if isinstance(b,str) else b) for a,b in mapping.items()}
    for y in range(out.height):
        for x in range(out.width):
            p=px[x,y]
            if p[3] and p in m: px[x,y]=m[p]
    return out

def flash(img, col=(255,246,230,255), keep_outline=True):
    out=img.copy(); px=out.load()
    for y in range(out.height):
        for x in range(out.width):
            p=px[x,y]
            if p[3] and not (keep_outline and p==PAL['k']): px[x,y]=col
    return out

def shift(img, dx, dy):
    out=Image.new('RGBA',img.size,(0,0,0,0)); out.paste(img,(dx,dy),img); return out

# =============== HERÓI (Lume) — versão 2 ===============
HPAL={k:rgba(v) for k,v in {'k':'#1a1210','h':'#c9461f','H':'#f0843c','j':'#8a2410','s':'#f0c49a','S':'#c98e6a','w':'#fff6e6',
 't':'#3d6a7a','T':'#29455a','l':'#5a8a9a','c':'#e0402a','C':'#8a2410','y':'#e8b04a','b':'#5a3a22'}.items()}
HEAD_D=["................",".....kkkkkk.....","....kHHhhhhk....","...kHHhhhhhhk...","...khhhhhhhjk...","...khsshhsshk...","...kssssssssk...","...kskssssksk...","...kskssssksk...","....kSssssSk...."]
HEAD_U=HEAD_D[:5]+["...khhhhhhhhk...","...khhhhhhhjk...","...kjhhhhhhjk...","...kjjhhhhjjk...","....kjjjjjjk...."]
BODY_D=["...kcccccccCk...","..ktkllttttTktk.","..ksklttttTTksk.","...kyyyyyyyyk..."]
BODY_U=["...kcccccccCk...","..ktkTttttTTktk.","..kskTttttTTksk.","...kyyyyyyyyk..."]
ATK_D=[BODY_D[0],"..ktkllttttTktk.","...klttssttTk...",BODY_D[3]]
ATK_U=[BODY_U[0],"...kTttttTTTk...","...kTttttTTTk...",BODY_U[3]]
L_IDLE=["....kTTkkTTk....","...kbbbkkbbbk..."]
L_W1  =["....kTTkkTTk....","....kkkk.kbbbk.."]
L_W3  =["....kTTkkTTk....","..kbbbk.kkkk...."]
SIDE_H=["................","....kkkkkk......","...kHHhhhhk.....","..kHhhhhhhhk....","..khhhhhhhhhk...","..kjhhhhhsssk...","..kjhhhhsssssk..","..kjhhssskssk...","..kjhhssskssk...","...kjjSsssSk...."]
SIDE_B=["...kcccccccCk...","...kTttttttlk...","...kTttttkslk...","...kyyyyyyyyk..."]
SIDE_A=["...kcccccccCk...","...kTttttttksssk","...kTtttttttk...","...kyyyyyyyyk..."]
SL_IDLE=["....kTTkTTk.....","...kbbbkbbbk...."]
SL_W1  =["...kTTk.kTTk....","..kbbbk..kbbbk.."]
def H(name,rows,bob=0): return grid(check(name,rows,16),oy=-bob,pal=HPAL)
hero_sprites={}
for d,head,body in (('baixo',HEAD_D,BODY_D),('cima',HEAD_U,BODY_U)):
    hero_sprites[f'heroi_{d}_0']=H(d,head+body+L_IDLE)
    hero_sprites[f'heroi_{d}_1']=H(d,head+body+L_W1,1)
    hero_sprites[f'heroi_{d}_2']=H(d,head+body+L_IDLE)
    hero_sprites[f'heroi_{d}_3']=H(d,head+body+L_W3,1)
for i,(lg,bob) in enumerate(((SL_IDLE,0),(SL_W1,1),(SL_IDLE,0),(SL_W1,1))):
    r=H('lado',SIDE_H+SIDE_B+lg,bob); hero_sprites[f'heroi_direita_{i}']=r; hero_sprites[f'heroi_esquerda_{i}']=r.transpose(Image.FLIP_LEFT_RIGHT)
hero_sprites['heroi_ataque_baixo']=H('atk_d',HEAD_D+ATK_D+L_IDLE)
hero_sprites['heroi_ataque_cima']=H('atk_u',['......kssk......']+HEAD_U[1:]+ATK_U+L_IDLE)
hero_sprites['heroi_ataque_direita']=H('atk_s',SIDE_H+SIDE_A+SL_W1)
hero_sprites['heroi_ataque_esquerda']=hero_sprites['heroi_ataque_direita'].transpose(Image.FLIP_LEFT_RIGHT)
# pose de pegar item: braços erguidos ao lado da cabeça
g=[list(r) for r in HEAD_D+["...kcccccccCk...","...kltttttTTk...","...kltttttTTk...","...kyyyyyyyyk..."]+L_IDLE]
for y in range(3,11):
    for (o,i1,i2,o2) in ((1,2,3,4),(14,13,12,11)):
        g[y][o]='k'; g[y][i1]=g[y][i2]=('s' if y<5 else 't')
        if g[y][o2]=='.': g[y][o2]='k'
g[2][2]=g[2][3]=g[2][12]=g[2][13]='k'
hero_sprites['heroi_pega_item']=grid([''.join(r) for r in g],pal=HPAL)
def hrecolor(img,m):
    out=img.copy();px=out.load();mm={HPAL[a]:HPAL[b] if b in HPAL else rgba(b) for a,b in m.items()}
    for y in range(16):
        for x in range(16):
            if px[x,y][3] and px[x,y] in mm: px[x,y]=mm[px[x,y]]
    return out
hero_sprites['heroi_dano']=hrecolor(hero_sprites['heroi_baixo_0'],{'t':'#e0402a','l':'#ff8a6a','T':'#8a2410','h':'#fff6e6','H':'#fff6e6','j':'#d8c8b8','c':'#fff6e6'})

# espada (16x16) e composições de ataque
SWPAL={k:rgba(v) for k,v in {'k':'#1a1210','w':'#ffffff','l':'#dfe4ee','s':'#9aa4b8','y':'#e8b04a','Y':'#ffe08a','n':'#7a4a26','N':'#4a2e1a'}.items()}
SWORD_V=check('espada',[
 ".......k........",
 "......kwk.......",
 ".....kwlsk......",
 ".....kwlsk......",
 ".....kwlsk......",
 ".....kwlsk......",
 ".....kwlsk......",
 ".....kwlsk......",
 ".....kwlsk......",
 ".....kwlsk......",
 "...kkkkkkkkk....",
 "...kYyyyyyyk....",
 "...kkknnnkkk....",
 ".....knNnk......",
 ".....kyYyk......",
 "......kkk......."],16)
sw_up=grid(SWORD_V,pal=SWPAL); sw_down=sw_up.transpose(Image.FLIP_TOP_BOTTOM); sw_right=sw_up.rotate(-90); sw_left=sw_right.transpose(Image.FLIP_LEFT_RIGHT)
# espada na diagonal (ponta para cima-direita), no mesmo estilo
dg=Image.new('RGBA',(16,16),(0,0,0,0));dp=dg.load()
def P(x,y,c):
    if 0<=x<16 and 0<=y<16: dp[x,y]=SWPAL[c]
for i in range(9):
    cx,cy=13-i,2+i
    for dx in (-2,2): P(cx+dx,cy,'k')
for i in range(9):
    cx,cy=13-i,2+i
    if i==0: P(cx,cy,'w');P(cx+1,cy,'k');P(cx-1,cy,'k')
    else: P(cx-1,cy,'w');P(cx,cy,'l');P(cx+1,cy,'s')
P(14,1,'k');P(13,1,'k');P(15,1,'k');P(14,0,'k')
for (x,y) in ((1,8),(2,8),(1,9),(7,14),(8,14),(8,13)): P(x,y,'k')
for (x,y) in ((2,9),(3,10),(5,12),(6,13),(7,13)): P(x,y,'y')
P(4,11,'Y');P(2,10,'k');P(3,11,'k');P(6,12,'k')
for (x,y) in ((3,12),(2,13)): P(x,y,'n')
for (x,y) in ((2,12),(3,13),(4,12),(1,13),(2,14),(4,13)): P(x,y,'k')
P(1,14,'Y');P(0,14,'k');P(0,15,'k');P(1,15,'k');P(2,15,'k')
weapons={'espada_cima':sw_up,'espada_baixo':sw_down,'espada_direita':sw_right,'espada_esquerda':sw_left,'espada_diagonal':dg}
attack={}
def comp(size, parts):
    im=Image.new('RGBA',size,(0,0,0,0))
    for p,(x,y) in parts: im.paste(p,(x,y),p)
    return im
attack['ataque_baixo']=comp((16,32),[(sw_down,(0,10)),(hero_sprites['heroi_ataque_baixo'],(0,0))])
attack['ataque_cima']=comp((16,32),[(sw_up,(0,3)),(hero_sprites['heroi_ataque_cima'],(0,16))])
attack['ataque_direita']=comp((32,16),[(sw_right,(11,4)),(hero_sprites['heroi_ataque_direita'],(0,0))])
attack['ataque_esquerda']=attack['ataque_direita'].transpose(Image.FLIP_LEFT_RIGHT)

# =============== INIMIGOS ===============
enemies={}
SLIME=["........","........","........","........","......kk","....kkEE","...kEEee","..kEeeee","..keeeee",".keeekee",".keeekee",".keeeeee",".kReeeee","..kRRRRR","...kkkkk","........"]
s0=grid(mirror('brasinha',SLIME,{'E':'e'}))
SLIME_SQ=SLIME[:4]+["........"]+SLIME[5:12]+[SLIME[11]]+SLIME[12:]
s1=grid(mirror('brasinha2',SLIME_SQ,{'E':'e'}))
enemies['brasinha_0']=s0; enemies['brasinha_1']=s1; enemies['cinza_viva_0']=recolor(s0,{'e':(120,112,108,255),'E':(176,168,160,255),'R':(64,58,56,255)}); enemies['cinza_viva_1']=recolor(s1,{'e':(120,112,108,255),'E':(176,168,160,255),'R':(64,58,56,255)}); enemies['brasinha_pulo']=shift(s0,0,-3); enemies['brasinha_dano']=flash(s0)

BAT0=["........","........","........","k.......","kk....k.","kAk...kk","kaAk.kaa",".kaAkaaa",".kaaaaYa","..kaaaaa","..kakaaa","...k.kaa","......kk","........","........","........"]
BAT1=["........","........","........","........","......k.","......kk",".....kaa","kkkkkaaa","kAAaaaYa","kaaAkaaa",".kak.kaa",".k...kaa","......kk","........","........","........"]
enemies['morcego_0']=grid(mirror('morcego',BAT0)); enemies['morcego_1']=grid(mirror('morcego1',BAT1))
enemies['morcego_dano']=flash(enemies['morcego_0'])

SPIT=["........","........",".....kkk","...kkPPi","..kPPiii",".kPiiiii",".kiikkii","kiiikYii","kiiiiiii","kiiiikRR","kiiiikRe",".kiiiikk",".kdiiiii","..kddddd","...kkkkk","........"]
SPIT_BACK=SPIT[:6]+[".kiiiiii","kiiiiiii","kiiPiiii","kiiiiiii","kiiiiiii",".kiiiiii"]+SPIT[12:]
sp=grid(mirror('cuspidor',SPIT,{'P':'i'}))
enemies['cuspidor_frente']=sp
enemies['cuspidor_costas']=grid(mirror('cuspidor_c',SPIT_BACK,{'P':'i'}))
enemies['cuspidor_atira']=recolor(sp,{'R':'r','e':'Y'})
enemies['cuspidor_dano']=flash(sp)

KNIGHT=["......kk",".....kxx","....kxXX","....kXXX","....kxYk","....kXXX","..kkkxxx",".kXXkxex",".kXxkxEe",".kxxkxee",".kxkkxxx",".kek.kxx","..k..kxx",".....kxk","....kxxk","....kkkk"]
kn=grid(mirror('cavaleiro',KNIGHT,{'E':'e'}))
enemies['cavaleiro_magma_0']=kn
enemies['cavaleiro_magma_1']=recolor(kn,{'e':'E','Y':'w'})
enemies['cavaleiro_magma_dano']=flash(kn)

# fogo inimigo e onda de brasa
FIRE=check('fogo',["................","................","................","................","................","......kkkk......",".....kreerk.....","....kreEEerk....","....keEYYEek....","....keEYYEek....","....kreEEerk....",".....kreerk.....","......kkkk......","................","................","................"],16)
enemies['bola_de_fogo']=grid([r[:16] for r in FIRE])
WAVE=check('onda',["................","................","....kkkkkkkk....","...keeeeeeeek...","..keEEEEEEEEek..","..kEYYYYYYYYEk..","..kYwwwwwwwwYk..","...kkkkkkkkkk...","................","................","................","................","................","................","................","................"],16)
enemies['onda_de_brasa']=shift(grid(WAVE),0,3)

# =============== CHEFE: Guardião de Cinzas (32x32) ===============
BOSS=["................","...kk...........","..kxk...........","..kxxk..........","...kxxk..kkkkkkk","....kxxkkxxxxxxx","....kxxxxXXXXXXX","...kxxXXXXXXXXXX","..kxXXXXXXXXXXXX","..kxXXXXkkkXXXXX",".kxXXXXkYYYkXXXX",".kxXXXXkYeYkXXXX",".kxXXXXXkkkXXXXX",".kxXXeXXXXXXXXXX","kxXXXeXXXXXXXkkk","kxXXXeeXXXXXkeee","kxXXXXeXXXXXkkkk","kxXXXXXXXXXXXXXX","kxxXXXXXXXXeXXXX",".kxXXXXXXXXeXXXX",".kkxXXXXXXeeXXXX","kxxkxXXXXXXXXXXX","kxXkkxXXXXXXXXXX","kxXk.kxXXXXXXXXX","kxek.kxxXXXXXXXX",".kk..kxxxxxxxxxx",".....kxxxkkkkkkk",".....kxxk.......","....kxxxk.......","....kkkkk.......","................","................"]
boss=grid(mirror('chefe',BOSS),size=(32,32))
bosses={'guardiao_cinzas':recolor(boss,{'X':(110,98,96,255),'x':(58,52,52,255),'e':(140,128,120,255),'Y':(200,190,180,255)}),'guardiao_0':boss,'guardiao_1':recolor(boss,{'e':'E','Y':'w'}),'guardiao_furia':recolor(boss,{'e':'Y','Y':'w','X':'R'}),'guardiao_dano':flash(boss)}

# =============== PERSONAGENS ===============
chars={}
PRINC=["....k.kk","...kykyY","..kLyyyy",".kLLLLLL",".kLLssss",".kLsskss",".kLsssss","..kLLkss",".kLLkOQQ",".kLkOQQQ","..kOQQQQ","..kQQQyQ",".kQQQQQQ",".kOQQQQQ","kOQQQQQQ","kkkkkkkk"]
chars['princesa_lirian']=grid(mirror('princesa',PRINC,{'O':'Q'}))
chars['princesa_lirian_1']=shift(chars['princesa_lirian'],0,-1)
def elder(beard_extra=0):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    R=lambda x,y,w,h,c: d.rectangle([x,y,x+w-1,y+h-1],fill=PAL[c])
    R(2,4,10,12,'k');R(4,0,6,5,'k');R(3,5,8,10,'z');R(4,6,2,8,'Z');R(5,1,4,3,'s');R(4,3,6,4+beard_extra,'g');R(5,3,1,1,'k');R(8,3,1,1,'k')
    R(12,0,1,16,'n');R(11,0,3,2,'o');R(12,15,1,1,'k')
    return im
chars['anciao_0']=elder(); chars['anciao_1']=elder(1)
GUARD=["....kkkk","...kGGGG","..kGGGGG","..kGkkkk","..kGkYss",".kkkksss","kGGkuuuu","kGkuuuuu","kGkuuyuu","kGkkuuuu",".kssuuuu","..kkuuuu","...kGGGG","...kGkkk","...kbk..","...kkk.."]
chars['soldado_reino']=grid(mirror('soldado',GUARD))

# =============== OBJETOS ===============
objs={}
def canvas():
    im=Image.new('RGBA',(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    return im,(lambda x,y,w,h,c: d.rectangle([x,y,x+w-1,y+h-1],fill=PAL[c] if isinstance(c,str) else c))
POT=["........","........","........","....kkkk","...kBBBB","...kKKKK","....kKKK","...kWKKK","..kKKKKK",".kKKyyyy",".kKKKKKK",".kKKKKKK",".kBKKKKK","..kBBBBB","...kkkkk","........"]
objs['vaso']=grid(mirror('vaso',POT,{'W':'K','K':'K'}))
objs['vaso_quebrado']=grid(check('vaso_q',["................","................","................","................","................","................","................","................","................","....k...........","...kKk....kk....","..kKKBk..kKBk...",".kKBk.k.kKKk.k..",".kkk.kKkkkk.kBk.","......kk.....kk.","................"],16))
im,R=canvas();R(7,8,2,8,'N');R(1,2,14,8,'k');R(2,3,12,6,'n');R(2,3,12,1,'W');R(4,5,8,1,'N');R(4,7,6,1,'N');objs['placa']=im
for i,hh in enumerate((5,7,6)):
    im,R=canvas();R(6,8,4,8,'k');R(7,9,2,7,'n');R(5,7,6,2,'G');R(5,8-hh,6,hh,'r');R(6,9-hh,4,hh-1,'o');R(7,10-hh,2,max(1,hh-3),'Y');objs[f'tocha_{i}']=im
im,R=canvas();R(0,0,16,16,'k');R(1,1,14,14,'d');R(1,1,14,2,'P');R(1,1,2,14,'i');R(3,3,10,10,'i');R(5,5,6,6,'d');objs['bloco_empurrar']=im
im,R=canvas();R(2,10,12,5,'k');R(3,11,10,3,'d');R(5,7,6,4,'k');R(6,8,4,3,'r');objs['interruptor_off']=im
im,R=canvas();R(2,11,12,4,'k');R(3,12,10,2,'d');R(5,10,6,2,'k');R(6,10,4,1,'v');objs['interruptor_on']=im
KEY=check('chave',["......kkkk......",".....kyyyyk.....","....kyYkkyyk....","....kyk..kyk....","....kyykkyyk....",".....kyyyyk.....","......kyyk......","......kyyk......","......kyykk.....","......kyyyyk....","......kyykk.....","......kyyk......","......kyyyk.....","......kyykk.....",".......kk.......","................"],16)
objs['chave']=grid(KEY)
objs['chave_mestra']=recolor(objs['chave'],{'y':'r','Y':'E'})
HEART=["................","................","..kkk....kkk....",".krrrk..krrrk...",".kwrrrkkrrrrrk..".replace('..',''),"","","","","","","","","","",""]
def heart_big(fill):
    rows=["................","................","...kkk..kkk.....","..kwrrkkrrrk....","..kwrrrrrrrrk...".ljust(16,'.'),"..krrrrrrrrrk...","..krrrrrrrrrk...","...krrrrrrrk....","....krrrrrk.....",".....krrrk......","......krk.......",".......k........","................","................","................","................"]
    rows=[r[:16].ljust(16,'.') for r in rows]
    im=grid(rows);
    if fill<2:
        px=im.load()
        for y in range(16):
            for x in range(16):
                if px[x,y]==PAL['r'] and (fill==0 or x>=7): px[x,y]=(74,42,38,255)
                if px[x,y]==PAL['w'] and fill==0: px[x,y]=(74,42,38,255)
    return shift(im,1,1)
objs['coracao_cheio']=heart_big(2);objs['coracao_meio']=heart_big(1);objs['coracao_vazio']=heart_big(0)
objs['recipiente_coracao']=recolor(heart_big(2),{'k':'y'})
EMB=["................","................","................","................","......kkk.......",".....keeek......","....keEEEek.....","....keEwEek.....","....keEEEek.....","....keeEeek.....",".....keeek......","......kkk.......","................","................","................","................"]
objs['brasa']=grid(check('brasa',EMB,16)); objs['brasa_grande']=recolor(objs['brasa'],{'e':'E','E':'Y'})
def crystal(col):
    im,R=canvas()
    for (x,y,w,h) in ((7,1,2,1),(6,2,4,1),(5,3,6,1),(4,4,8,7),(5,11,6,1),(6,12,4,1),(7,13,2,1)): R(x,y,w,h,'k')
    for (x,y,w,h) in ((7,2,2,1),(6,3,4,1),(5,4,6,7),(6,11,4,1),(7,12,2,1)): R(x,y,w,h,col)
    R(6,4,1,4,'w');R(7,3,1,1,'w');R(9,7,1,3,(0,0,0,70))
    return im
objs['cristal_brasa']=crystal('r');objs['cristal_mares']=crystal('u');objs['cristal_ventos']=crystal('v')
PEND_COLS=[('sol','y'),('fogo','h'),('mar','u'),('floresta','v'),('sombra','Z'),('gelo','c'),('lua','g'),('estrela','o')]
for nome,col in PEND_COLS:
    im,R=canvas()
    R(7,1,2,4,'y');R(6,1,4,1,'y')
    for (x,y,w,h) in ((6,5,4,1),(5,6,6,1),(4,7,8,4),(5,11,6,1),(6,12,4,1)): R(x,y,w,h,'k')
    for (x,y,w,h) in ((6,6,4,1),(5,7,6,4),(6,11,4,1)): R(x,y,w,h,col)
    R(6,7,1,2,'w'); objs[f'pendente_{nome}']=im
objs['bau']=grid(check('bau',["................","................","..kkkkkkkkkkkk..",".kWWnnnnnnnnnnk.",".knnnnnnnnnnnnk.",".kyyyyykkyyyyyk.",".kNNNNkYYkNNNNk.",".kkkkkkYykkkkkk.",".knnnnkkkknnnnk.",".kynnnnnnnnnnyk.",".kynnnnnnnnnnyk.",".kyyyyyyyyyyyyk.",".kNNNNNNNNNNNNk.",".kkkkkkkkkkkkkk.","................","................"],16))
objs['bau_aberto']=grid(check('bau_aberto',["..kkkkkkkkkkkk..",".kNNNNNNNNNNNNk.",".kNnNNnNNNnNNNk.",".kyyyyyyyyyyyyk.","..kkkkkkkkkkkk..",".kkkkkkkkkkkkkk.",".kxxxxxxxxxxxxk.",".kxXXxxxxxxxXxk.",".kWWnnnnnnnnnnk.",".kynnnnnnnnnnyk.",".kynnnnnnnnnnyk.",".kyyyyyyyyyyyyk.",".kNNNNNNNNNNNNk.",".kkkkkkkkkkkkkk.","................","................"],16))
objs['bau_grande']=grid(check('bau_grande',["................",".kkkkkkkkkkkkkk.","kYyyyyyyyyyyyyyk","kyrrrrrrrrrrrryk","kyrrrrrrrrrrrryk","kyRRRRRkkRRRRRyk","kyyyyykYYkyyyyyk","kkkkkkkYykkkkkkk","kyrrrrkkkkrrrryk","kyrrrrrrrrrrrryk","kyrrrrrrrrrrrryk","kyRRRRRRRRRRRRyk","kYyyyyyyyyyyyyyk","kkkkkkkkkkkkkkkk","................","................"],16))
objs['bau_grande_aberto']=grid(check('bau_grande_aberto',[".kkkkkkkkkkkkkk.","kRRRRRRRRRRRRRRk","kRRrRRRRRRRrRRRk","kyyyyyyyyyyyyyyk",".kkkkkkkkkkkkkk.","kkkkkkkkkkkkkkkk","kxxxxxxxxxxxxxxk","kxXXxxxxxxxxXXxk","kYyyyyyyyyyyyyyk","kyrrrrrrrrrrrryk","kyrrrrrrrrrrrryk","kyRRRRRRRRRRRRyk","kYyyyyyyyyyyyyyk","kkkkkkkkkkkkkkkk","................","................"],16))

# =============== TILES ===============
C={k:rgba(v) for k,v in {
 'grass':'#5f6e3a','grassD':'#4c5a2e','grassL':'#7a8a44','sand':'#b8925e','sandD':'#9c7a4c','leaf':'#8a3a1c','leafL':'#c4602a','leafD':'#5a2412',
 'trunk':'#4a2e1a','rock':'#7a7068','rockL':'#9a8f84','rockD':'#4a423e','bush':'#6e7c32','bushL':'#94a244','bushD':'#3e4a1c','water':'#2d5668','waterL':'#5a8ea0',
 'wall':'#2b2225','wallD':'#1b1517','wallL':'#3d3134','floor':'#3a2e30','floorL':'#43373a','floorD':'#2f2528','lava':'#c4401a','lavaL':'#f07a2a','lavaY':'#ffd27a',
 'gold':'#e8b04a','wood':'#7a4a26','woodD':'#5a3418','dark':'#2a160a','black':'#000000','ember':'#e06a24','brick':'#6a2a1a','brickL':'#8a3a24','brickD':'#3e160c',
 'flowerR':'#e0402a','flowerY':'#ffd27a'}.items()}
def h32(x,y,s=0):
    h=(x*374761393+y*668265263+s*982451653)&0xffffffff
    h=((h^(h>>13))*1274126177)&0xffffffff
    return ((h^(h>>16))&0xffffffff)/4294967295
def tile(fn, seed=(3,5)):
    im=Image.new('RGBA',(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    def R(x,y,w,h,c): d.rectangle([x,y,x+w-1,y+h-1],fill=C[c] if isinstance(c,str) else c)
    def blob(x,y,w,h,c): R(x+1,y,w-2,h,c); R(x,y+1,w,h-2,c)
    fn(R,blob,seed); return im
def grass(R,blob,s):
    R(0,0,16,16,'grass')
    for i in range(5):
        a,b=h32(*s,i),h32(*s,i+9); R(int(a*14)+1,int(b*13)+1,1,2,'grassD' if i%2 else 'grassL')
def floor(R,blob,s): R(0,0,16,16,'floor');R(0,15,16,1,'floorD');R(15,0,1,16,'floorD');R(0,0,15,1,'floorL')
tiles={}
tiles['grama_0']=tile(grass,(3,5));tiles['grama_1']=tile(grass,(8,1));tiles['grama_2']=tile(grass,(11,7))
def flowers(R,blob,s):
    grass(R,blob,s)
    for (x,y,c) in ((3,4,'flowerR'),(10,3,'flowerY'),(6,10,'flowerY'),(12,11,'flowerR')): R(x,y,2,2,c);R(x,y+2,1,1,'grassD')
tiles['grama_flores']=tile(flowers)
def path(R,blob,s):
    R(0,0,16,16,'sand')
    for i in range(4): R(int(h32(*s,i)*15),int(h32(*s,i+5)*15),1,1,'sandD')
tiles['caminho']=tile(path)
def tree(R,blob,s):
    grass(R,blob,s);R(6,11,4,5,'trunk');blob(1,0,14,13,'leafD');blob(2,1,12,11,'leaf');blob(3,2,6,4,'leafL');R(9,6,2,1,'leafD');R(5,8,1,1,'leafD');R(11,3,1,1,'leafL')
tiles['arvore_outono']=tile(tree)
def rock(R,blob,s): grass(R,blob,s);blob(1,2,14,13,'rockD');blob(2,3,12,11,'rock');blob(3,4,6,3,'rockL');R(9,9,3,1,'rockD')
tiles['pedra']=tile(rock)
def bush(R,blob,s): grass(R,blob,s);blob(2,3,12,12,'bushD');blob(3,4,10,10,'bush');blob(4,5,4,3,'bushL');R(8,10,2,1,'bushD')
tiles['arbusto']=tile(bush)
def stump(R,blob,s): grass(R,blob,s);R(5,9,6,5,'bushD');R(6,10,4,3,'bushL')
tiles['arbusto_cortado']=tile(stump)
for f in range(2):
    def water(R,blob,s,f=f):
        R(0,0,16,16,'water'); o=f*5; R((o+2)%13,4,3,1,'waterL');R((o+9)%13,11,3,1,'waterL')
    tiles[f'agua_{f}']=tile(water)
    def lava(R,blob,s,f=f):
        R(0,0,16,16,'lava'); R(2,3,6,3,'lavaL' if f else 'ember');R(9,10,5,3,'ember' if f else 'lavaL');R(3+f*2,4,2,1,'lavaY');R(10,11+f,2,1,'lavaY')
    tiles[f'lava_{f}']=tile(lava)
def cave(R,blob,s): R(0,0,16,16,'rockD');R(0,0,16,4,'rock');blob(3,4,10,12,'black')
tiles['entrada_caverna']=tile(cave)
def gate(R,blob,s):
    R(0,0,16,16,'brick');R(0,0,16,1,'brickL')
    for y in range(4,16,4): R(0,y,16,1,'brickD')
    blob(2,2,12,14,'ember');blob(3,3,10,13,'black');R(4,15,8,1,(90,30,14,255))
tiles['portao_castelo']=tile(gate)
def castle_wall(R,blob,s):
    R(0,0,16,16,'brick')
    for y in range(0,16,4):
        R(0,y,16,1,'brickD'); o=0 if (y//4)%2 else 4
        for x in range(o,16,8): R(x,y,1,4,'brickD')
        R(0,y+1,16,1,'brickL')
tiles['muralha_castelo']=tile(castle_wall)
def battlement(R,blob,s):
    castle_wall(R,blob,s); R(0,0,16,5,(0,0,0,0)); R(0,0,5,5,'brick');R(10,0,6,5,'brick');R(0,0,5,1,'brickL');R(10,0,6,1,'brickL')
tiles['ameia_castelo']=tile(battlement)
def banner(R,blob,s):
    castle_wall(R,blob,s); R(4,0,8,13,'black');R(5,0,6,12,'flowerR');R(5,12,3,2,'flowerR');R(8,12,3,2,'flowerR');R(7,3,2,5,'gold');R(6,4,4,2,'gold')
tiles['estandarte']=tile(banner)
def wall(R,blob,s):
    R(0,0,16,16,'wall');R(0,7,16,1,'wallD');R(0,15,16,1,'wallD');R(4,0,1,7,'wallD');R(12,8,1,7,'wallD');R(0,0,16,1,'wallL');R(0,8,16,1,'wallL')
tiles['parede_castelo']=tile(wall)
tiles['piso_castelo']=tile(floor)
def carpet(R,blob,s): floor(R,blob,s);R(2,0,12,16,'brickD');R(3,0,10,16,'flowerR');R(4,0,1,16,'gold');R(11,0,1,16,'gold')
tiles['tapete_real']=tile(carpet)
def door(R,blob,s):
    R(0,0,16,16,'wall');R(0,1,16,15,'dark');R(1,2,14,14,'wood');R(5,2,1,14,'woodD');R(10,2,1,14,'woodD');R(6,7,4,5,'gold');R(7,8,2,2,'black');R(7,10,2,1,'black')
tiles['porta_trancada']=tile(door)
def door_boss(R,blob,s): door(R,blob,s);R(1,2,14,2,'flowerR');R(2,5,2,2,'flowerR');R(12,5,2,2,'flowerR')
tiles['porta_chefe']=tile(door_boss)
def stairs(R,blob,s):
    floor(R,blob,s)
    for i,c in enumerate(((42,32,34,255),(32,24,25,255),(22,15,16,255),(12,8,8,255))): R(0,4+i*3,16,3,c)
tiles['escada']=tile(stairs)
def shutter(R,blob,s):
    floor(R,blob,s)
    for i in range(1,16,4): R(i,0,2,16,'rockD')
    R(0,3,16,2,'rockL')
tiles['grade_fechada']=tile(shutter)
for f,hh in enumerate((5,8,6)):
    def braz(R,blob,s,hh=hh):
        floor(R,blob,s);R(3,9,10,6,'rockD');R(2,8,12,2,'rock');R(3,8,10,1,'rockL')
        R(4,8-hh,8,hh,'ember');R(5,9-hh,6,hh-1,'lavaL');R(7,11-hh,2,max(1,hh-3),'lavaY')
    tiles[f'braseiro_{f}']=tile(braz)
def statue(R,blob,s):
    floor(R,blob,s);R(3,12,10,4,'rockD');R(4,11,8,1,'rockL');blob(4,2,8,10,'rockD');blob(5,3,6,8,'rock');R(6,5,1,1,'flowerR');R(9,5,1,1,'flowerR');R(5,1,2,3,'rockD');R(9,1,2,3,'rockD')
tiles['estatua_guardia']=tile(statue)
def cracked(R,blob,s): floor(R,blob,s);R(4,3,1,4,'floorD');R(5,6,3,1,'floorD');R(8,7,1,5,'floorD');R(9,11,3,1,'floorD');R(5,6,1,1,'lavaL')
tiles['piso_rachado']=tile(cracked)
def braz_off(R,blob,s):
    floor(R,blob,s);R(3,9,10,6,'rockD');R(2,8,12,2,'rock');R(3,8,10,1,'rockL');R(4,6,8,2,(78,72,70,255));R(5,5,6,1,(110,102,98,255));R(7,4,1,1,(110,102,98,255))
tiles['braseiro_apagado']=tile(braz_off)
def barricade(R,blob,s):
    floor(R,blob,s)
    for y in (1,6,11):
        R(0,y,16,4,'dark');R(0,y+1,16,2,'wood');R(0,y+1,16,1,(160,104,58,255));R(2,y+1,1,1,'gold');R(13,y+1,1,1,'gold')
    for i in range(14):
        R(1+i,1+i,2,1,'woodD');R(14-i,1+i,2,1,'woodD')
tiles['barricada']=tile(barricade)

# =============== REINO DAS MARÉS ===============
C.update({k:rgba(v) for k,v in {'sand':'#e0c890','sandD':'#c8ac72','sandL':'#f0dcaa','sea':'#2d6a8a','seaL':'#5aa8c4','foam':'#d8f0f4',
 'deep':'#1e4a6a','deepL':'#3a78a0','palm':'#4a9a4a','palmL':'#7ac464','palmD':'#2a5a30','trunkP':'#8a6038','trunkPD':'#5a3a20',
 'rockS':'#7a8a96','rockSL':'#a0b0bc','rockSD':'#4a5662','kelp':'#3a8a5a','kelpL':'#6ac08a','kelpD':'#1e5034','plank':'#9a6a3a',
 'plankD':'#5a3a1e','plankL':'#c08a50','coral':'#e8708a','coralL':'#ffa0b4','coralD':'#a8405a','pit':'#05070a','pitE':'#1e3a50',
 'shellW':'#fff0e0','shellP':'#f0a0b0','post':'#7a4a26','postD':'#4a2e1a','ring':'#b8b0a8','outl':'#1a1210'}.items()})
tiles_m={}
def sand(R,blob,s):
    R(0,0,16,16,'sand')
    for i in range(6):
        a,b=h32(*s,i),h32(*s,i+9); R(int(a*15),int(b*15),1,1,'sandD' if i%2 else 'sandL')
tiles_m['areia_0']=tile(sand,(2,3)); tiles_m['areia_1']=tile(sand,(9,4))
def shells(R,blob,s):
    sand(R,blob,s)
    for (x,y,c) in ((3,4,'shellW'),(11,3,'shellP'),(7,11,'shellW'),(12,12,'shellP')): R(x,y,2,1,c);R(x,y+1,1,1,c)
tiles_m['areia_conchas']=tile(shells)
def pebbles(R,blob,s):
    sand(R,blob,s)
    for i in range(7):
        x,y=int(h32(*s,i+20)*12)+1,int(h32(*s,i+30)*12)+1; R(x,y,3,2,'rockSD');R(x,y,2,1,'rockSL')
tiles_m['caminho_pedras']=tile(pebbles,(5,5))
def palm(R,blob,s):
    sand(R,blob,s)
    for (x,y) in ((8,14),(8,12),(7,10),(7,8),(8,6)): R(x,y,3,2,'trunkPD');R(x,y,2,1,'trunkP')
    blob(1,0,14,8,'palmD');blob(2,1,12,6,'palm');R(0,4,4,3,'palmD');R(12,4,4,3,'palmD');R(1,5,2,1,'palm');R(13,5,2,1,'palm');R(4,1,5,2,'palmL');R(7,4,3,2,'trunkPD')
tiles_m['palmeira']=tile(palm)
def srock(R,blob,s): sand(R,blob,s);blob(1,3,14,12,'rockSD');blob(2,4,12,10,'rockS');blob(3,5,6,3,'rockSL');R(9,10,3,1,'rockSD')
tiles_m['rocha_mar']=tile(srock)
def kelp(R,blob,s):
    sand(R,blob,s)
    for (x,h) in ((3,10),(6,13),(9,11),(12,9)): R(x,16-h,2,h,'kelpD');R(x,17-h,1,h-2,'kelpL')
    blob(2,7,12,8,'kelpD');blob(3,8,10,6,'kelp');R(4,9,3,2,'kelpL')
tiles_m['alga']=tile(kelp)
def kelpcut(R,blob,s): sand(R,blob,s);R(5,11,6,3,'kelpD');R(6,12,4,1,'kelpL')
tiles_m['alga_cortada']=tile(kelpcut)
for f in range(2):
    def sea(R,blob,s,f=f):
        R(0,0,16,16,'sea');o=f*4
        R((o+1)%12,3,4,1,'seaL');R((o+8)%12,9,4,1,'seaL');R((o+4)%12,13,3,1,'foam')
    tiles_m[f'mar_{f}']=tile(sea)
    def deep(R,blob,s,f=f):
        R(0,0,16,16,'deep');o=f*5
        R((o+2)%12,4,4,1,'deepL');R((o+9)%12,11,3,1,'deepL')
    tiles_m[f'agua_funda_{f}']=tile(deep)
def pier(R,blob,s):
    R(0,0,16,16,'sea')
    for y in (0,5,10): R(0,y,16,5,'plankD');R(0,y,16,4,'plank');R(0,y,16,1,'plankL');R(3,y+2,1,1,'plankD');R(12,y+2,1,1,'plankD')
tiles_m['pier']=tile(pier)
def pit(R,blob,s): R(0,0,16,16,'pit');R(0,0,16,2,'pitE');R(0,2,16,1,(14,30,44,255))
tiles_m['abismo']=tile(pit)
def post(R,blob,s):
    R(5,5,6,11,'postD');R(6,5,4,10,'post');R(6,5,1,10,'plankL');R(4,1,8,5,'outl');R(5,2,6,3,'ring');R(7,3,2,1,'outl');R(4,14,8,2,'postD')
tiles_m['poste_gancho']=tile(post)
def coral(R,blob,s):
    for (x,y,w,h) in ((3,6,2,9),(7,3,2,12),(11,7,2,8),(5,9,3,2),(9,6,3,2),(2,6,2,2),(12,5,2,2)): R(x,y,w,h,'coralD')
    for (x,y,w,h) in ((3,6,1,8),(7,3,1,11),(11,7,1,7),(7,3,2,1)): R(x,y,w,h,'coral')
    R(7,2,2,1,'coralL');R(3,5,1,1,'coralL');R(11,6,1,1,'coralL');R(2,14,12,2,'coralD')
tiles_m['coral']=tile(coral)
def remap(img,m):
    out=img.copy();px=out.load();mm={rgba(a):rgba(b) for a,b in m.items()}
    for y in range(out.height):
        for x in range(out.width):
            p=px[x,y]
            if p[3] and p in mm: px[x,y]=mm[p]
    return out
SEA_IN={'#2b2225':'#22344a','#1b1517':'#16222f','#3d3134':'#34506a','#3a2e30':'#2e4250','#43373a':'#38505e','#2f2528':'#243540'}
SEA_OUT={'#6a2a1a':'#3a5a7a','#8a3a24':'#5a7a9a','#3e160c':'#26405a','#e0402a':'#2aa0b0','#e06a24':'#4ac4d8','#5a1e0e':'#1e5a6a'}
for a,b in (('parede_castelo','parede_mares'),('piso_castelo','piso_mares'),('porta_trancada','porta_trancada_mares'),('porta_chefe','porta_chefe_mares'),
            ('escada','escada_mares'),('grade_fechada','grade_fechada_mares'),('estatua_guardia','estatua_mares'),('tapete_real','tapete_mares')):
    tiles_m[b]=remap(tiles[a],{**SEA_IN,**SEA_OUT})
for a,b in (('muralha_castelo','muralha_mares'),('ameia_castelo','ameia_mares'),('estandarte','estandarte_mares'),('portao_castelo','portao_mares')):
    tiles_m[b]=remap(tiles[a],SEA_OUT)

enemies_m={}
CRAB=["........","........","........",".kk.....","kRRk..k.","kRrrk.wk",".kkrk.k.","...krkkk","..krrrrr",".krrrrrr",".krRrrrr","..krrrrr",".k.kkkkk","k.k.k...","........","........"]
CRAB1=CRAB[:13]+[".k.k.k..","........","........"]
cr=grid(mirror('caranguejo',CRAB)); enemies_m['caranguejo_0']=cr; enemies_m['caranguejo_1']=grid(mirror('caranguejo1',CRAB1))
enemies_m['caranguejo_dano']=flash(cr)
enemies_m['caranguejinho']=shift(recolor(cr,{'r':'v','R':(40,110,60,255)}),0,1)
JELLY=["........","........",".....kkk","...kkccc","..kcwccc",".kcwcccc",".kccckcc",".kcccccc","..kkkkkk","..k.c.c.","...c.c.c","..c.c.c.","...c...c","........","........","........"]
JELLY1=JELLY[:9]+["...c.c.c","..c.c.c.","...c.c.c","..c...c.","........","........","........"]
jl=grid(mirror('agua_viva',JELLY,{'w':'c'}))
enemies_m['agua_viva_0']=jl; enemies_m['agua_viva_1']=grid(mirror('agua_viva1',JELLY1,{'w':'c'}))
enemies_m['agua_viva_carregada']=recolor(jl,{'c':'Y','w':'w'}); enemies_m['agua_viva_dano']=flash(jl)
COR=["......kkkk......",".....kQQQQk.....","....kQOQQQQk....","....kQQQQQQk....","....kQssssQk....","....kskssksk....",".....kssssk.....","..kkkkuuuukkk...",".kQQkuuuuuukn...",".kQOQkuuuuukn...",".kQQQkuuuuukn...",".kQOQkyyyykkn...","..kQkkuuuuk.n...",".....kuuuuk.n...",".....kbkkbk.k...",".....kkk.kkk...."]
COR=[list(r) for r in check('coral',COR,16)]
for y in (5,6): COR[y][12]='G'
COR[4][12]='k'
cof=grid([''.join(r) for r in COR])
CORB=[r[:] for r in COR]; CORB[4]=list("....kQQQQQQk..k."); CORB[5]=list("....kQQQQQQk..G."); CORB[6]=list(".....kQQQQk..G..")
enemies_m['guerreiro_coral_frente']=cof
enemies_m['guerreiro_coral_costas']=grid([''.join(r) for r in CORB])
enemies_m['guerreiro_coral_dano']=flash(cof)
enemies_m['tinta']=recolor(enemies['bola_de_fogo'],{'r':'x','e':'z','E':'Z','Y':'L'})

KRAKEN=["................","................","..........kkkkkk","........kkZZZZZZ",".......kZZZZZZZZ","......kZZLLZZZZZ",".....kZZLLZZZZZZ",".....kZZZZZZZZZZ","....kZZZZZZZZZZZ","....kZZZZkkkZZZZ","....kZZZkwwwkZZZ","....kZZZkwkwkZZZ","....kZZZkwwwkZZZ","....kZZZZkkkZZZZ","....kZZZZZZZZZZZ",".....kZZZZZZkkkk",".....kZZZZZkrrrr","......kZZZZZkkkk",".......kkZZZZZZZ","....kk..kkZZZZZZ","...kZZk..kZZkZZZ","..kZZk..kZZk.kZZ","..kZk..kZZk..kZZ",".kZZk.kZZk...kZZ",".kZk..kZk...kZZk",".kZZk.kZZk..kZk.","..kZZk.kZk..kZZk","...kk..kk....kk.","................","................","................","................"]
kr=grid(mirror('kraken',KRAKEN),size=(32,32))
bosses_m={'kraken_0':kr,'kraken_1':recolor(kr,{'w':'Y'}),'kraken_puxado':recolor(kr,{'w':'k','L':'z'}),'kraken_dano':flash(kr)}

chars_m={}
BOAT=["........","....kkkk","...kyyyy","..kyyyyy",".kkkkkkk","...kssss","...kskss","...kssss","...kgggg","..kkgggg",".kuukggg",".kuuuuuu",".ksuuuuu","..knnnnn","..knnkkn","..kkk..k"]
bq=grid(mirror('barqueiro',BOAT)); chars_m['barqueiro']=bq; chars_m['barqueiro_1']=shift(bq,0,-1)
chars_m['pescador']=recolor(bq,{'y':'u','u':'v'})
im=Image.new('RGBA',(32,16),(0,0,0,0));dd=ImageDraw.Draw(im)
def RR(x,y,w,h,c): dd.rectangle([x,y,x+w-1,y+h-1],fill=PAL[c] if isinstance(c,str) else c)
RR(15,0,2,10,'N');RR(17,1,9,8,'g');RR(17,1,1,8,'w');RR(18,8,8,1,'G')
RR(2,9,28,2,'k');RR(3,11,26,3,'k');RR(5,14,22,1,'k');RR(3,9,26,2,'n');RR(4,11,24,2,'N');RR(6,13,20,1,'N');RR(3,9,26,1,'W')
chars_m['barco']=im

# =============== REINO DOS VENTOS ===============
C.update({k:rgba(v) for k,v in {'gr':'#8ac06a','grD':'#6aa04a','grL':'#b0e090','path2':'#b8b0a0','path2D':'#8a8474','path2L':'#d4cec0',
 'pine':'#2e6a4a','pineL':'#4a8a5a','pineD':'#1a4030','mrock':'#a8a8a8','mrockL':'#d8d8d4','mrockD':'#6e6e70','shrub':'#7ab85a','shrubL':'#a8dc7a','shrubD':'#3e7a34',
 'sky':'#7ab8e8','skyL':'#a8d4f4','cloud':'#f4f8fc','cloudD':'#d0e2f0','flw':'#fffaf0','fly':'#ffe08a'}.items()})
tiles_v={}
def grass2(R,blob,s):
    R(0,0,16,16,'gr')
    for i in range(6):
        a,b=h32(*s,i),h32(*s,i+9); R(int(a*14)+1,int(b*13)+1,1,2,'grD' if i%2 else 'grL')
tiles_v['grama_alta_0']=tile(grass2,(4,2)); tiles_v['grama_alta_1']=tile(grass2,(7,9))
def wflowers(R,blob,s):
    grass2(R,blob,s)
    for (x,y,c) in ((3,3,'flw'),(11,4,'fly'),(6,10,'flw'),(12,12,'flw'),(2,12,'fly')): R(x,y,2,2,c);R(x,y+2,1,1,'grD')
tiles_v['flores_brancas']=tile(wflowers)
def mpath(R,blob,s):
    R(0,0,16,16,'path2D')
    for (x,y,w,h) in ((0,0,7,5),(8,0,8,4),(0,6,5,5),(6,5,6,6),(13,5,3,6),(0,12,8,4),(9,12,7,4)): R(x,y,w,h,'path2');R(x,y,w,1,'path2L')
tiles_v['caminho_montanha']=tile(mpath)
def pine(R,blob,s):
    grass2(R,blob,s);R(7,12,2,4,'trunk')
    for i,(y,w) in enumerate(((1,4),(3,6),(5,8),(7,10),(9,12))): R(8-w//2,y,w,3,'pineD');R(8-w//2+1,y,w-2,2,'pine')
    R(6,4,2,1,'pineL');R(5,8,2,1,'pineL');R(7,1,2,1,'pineL')
tiles_v['pinheiro']=tile(pine)
def mrock(R,blob,s): grass2(R,blob,s);blob(1,3,14,12,'mrockD');blob(2,4,12,10,'mrock');blob(3,5,6,3,'mrockL');R(9,10,3,1,'mrockD')
tiles_v['pedra_montanha']=tile(mrock)
def shrub(R,blob,s): grass2(R,blob,s);blob(2,3,12,12,'shrubD');blob(3,4,10,10,'shrub');blob(4,5,4,3,'shrubL');R(8,10,2,1,'shrubD')
tiles_v['arbusto_ventos']=tile(shrub)
def shrubcut(R,blob,s): grass2(R,blob,s);R(5,9,6,5,'shrubD');R(6,10,4,3,'shrubL')
tiles_v['arbusto_ventos_cortado']=tile(shrubcut)
for f in range(2):
    def skyp(R,blob,s,f=f):
        R(0,0,16,16,'sky');o=f*5
        blob((o+1)%14-2,3,9,4,'cloudD');blob((o+1)%14-1,2,7,4,'cloud');blob((o+8)%14,10,8,4,'cloudD');blob((o+8)%14+1,9,6,4,'cloud');R(0,0,16,1,'skyL')
    tiles_v[f'abismo_nuvens_{f}']=tile(skyp)
SKY_IN={'#2b2225':'#9a968c','#1b1517':'#6a665e','#3d3134':'#c8c4b8','#3a2e30':'#bdb8a8','#43373a':'#cfcabb','#2f2528':'#a49f90','#e0402a':'#4a9a5a','#3e160c':'#2a5a34'}
SKY_OUT={'#6a2a1a':'#a8a49a','#8a3a24':'#d0ccc0','#3e160c':'#7a766c','#e0402a':'#4a9a5a','#e06a24':'#e8b04a','#5a1e0e':'#6a5a2a'}
for a,b in (('parede_castelo','parede_ventos'),('piso_castelo','piso_ventos'),('porta_trancada','porta_trancada_ventos'),('porta_chefe','porta_chefe_ventos'),
            ('escada','escada_ventos'),('grade_fechada','grade_fechada_ventos'),('estatua_guardia','estatua_ventos'),('tapete_real','tapete_ventos')):
    tiles_v[b]=remap(tiles[a],{**SKY_IN})
for a,b in (('muralha_castelo','muralha_ventos'),('ameia_castelo','ameia_ventos'),('estandarte','estandarte_ventos'),('portao_castelo','portao_ventos')):
    tiles_v[b]=remap(tiles[a],SKY_OUT)

enemies_v={}
HARPY=["........","........","k.......","kGk....k","kGGk..kZ",".kGGkkZZ",".kGgGkss","..kGGksk","...kkkss",".....kZZ","....kZZZ","....kyky",".....k.k","........","........","........"]
hp=grid(mirror('harpia',HARPY)); enemies_v['harpia_0']=hp; enemies_v['harpia_1']=shift(hp,0,1); enemies_v['harpia_dano']=flash(hp)
GOLEM=["........","........","....kkkk","...kaGGG","..kaaGGG","..kaaYaa","..kaaaaa",".kkkaaaa","kaakAaaa","kaaakaaa","kaaakAAA",".kkkaaaa","...kaaak","...kAAAk","...kkkkk","........"]
gl=grid(mirror('golem',GOLEM,{'G':'a'})); enemies_v['golem_0']=gl; enemies_v['golem_1']=shift(gl,0,1); enemies_v['golem_dano']=flash(gl)
for fr in range(2):
    im=Image.new('RGBA',(16,16),(0,0,0,0));dd=ImageDraw.Draw(im)
    for i,(w,y) in enumerate(((14,2),(12,5),(10,8),(7,11),(4,13))):
        x0=8-w//2+((i+fr)%2*2-1)
        dd.ellipse([x0,y,x0+w-1,y+3],outline=PAL['G'] if (i+fr)%2 else PAL['g'])
    enemies_v[f'redemoinho_{fr}']=im
ar=recolor(enemies_m['guerreiro_coral_frente'],{'Q':'g','O':'G','u':'v'}); enemies_v['arqueiro_frente']=ar
enemies_v['arqueiro_costas']=recolor(enemies_m['guerreiro_coral_costas'],{'Q':'g','O':'G','u':'v'}); enemies_v['arqueiro_dano']=flash(ar)
im=Image.new('RGBA',(16,16),(0,0,0,0));dd=ImageDraw.Draw(im)
def AR(x,y,w,h,c): dd.rectangle([x,y,x+w-1,y+h-1],fill=PAL[c])
AR(2,7,10,2,'k');AR(3,7,9,1,'n');AR(11,6,3,4,'k');AR(12,7,3,2,'G');AR(14,7,1,2,'w');AR(1,6,2,4,'g');AR(0,6,1,1,'g');AR(0,9,1,1,'g')
enemies_v['flecha']=im
CHICK=["........","........","........","........","........","........","......kk","....kkgg","...kgggg","..kgkggg","..kggggo","...kgggg","....kkkk",".....y.y","........","........"]
enemies_v['filhote']=grid(mirror('filhote',CHICK))
GRIF=["................","................","kk..............","knk..........kkk","knnk........kggg",".knnk......kgggg",".knnnk....kggggg","..knnnk..kgggkgg","..knnnnkkkggggoo","...knnnnkkggggoo","...knnnnnkkggggk","....knnnnkyyyyyy","....knnnnkyyyyyy",".....knnkyyyyyyy",".....knkyyyyYyyy","......kyyyyyyyyy","......kyyyyyyyyy",".....kyyyyyyyyyy",".....kyyyykyyyyy","......kyyyykyyyy","......kyyyykkyyy",".......kyyyk.kyy",".......kyyk...ky","......kyyk....ky","......kook.....k","......kkkk......","................","................","................","................","................","................"]
gf=grid(mirror('grifo',GRIF),size=(32,32))
bosses_v={'grifo_0':gf,'grifo_1':shift(gf,0,-2),'grifo_atordoado':recolor(gf,{'g':'G','y':'n'}),'grifo_dano':flash(gf)}
chars_v={'aguia':recolor(gf,{'y':'n','Y':'N','o':'y'}),'monge':recolor(chars['anciao_0'],{'z':'v','Z':(150,210,120,255)}),'monge_1':recolor(chars['anciao_1'],{'z':'v','Z':(150,210,120,255)})}
REINO={'w':(230,255,250,255),'o':'c'}
for k,v in list(weapons.items()):
    chars_v['espada_reinos_'+k.split('_',1)[1]]=remap(v,{'#dfe4ee':'#8ad4e8','#9aa4b8':'#2a8aa0','#ffffff':'#e6fffa'})

# =============== SANTUÁRIOS: VULCÃO E GRUTA ===============
C.update({k:rgba(v) for k,v in {'ash':'#4a4040','ashD':'#2e2626','ashL':'#6a5a54','emb':'#e0561e','bas':'#3a3436','basL':'#5a5052','basD':'#241e20',
 'dead':'#2a2224','deadL':'#4a3e3e','vrock':'#1e1a1c','vrockL':'#3a3234','crack':'#f07a2a','stone':'#8a8478','stoneL':'#b0aa9c','stoneD':'#5a5650','rune':'#8ad4e8'}.items()})
tiles_s={}
def ash(R,blob,s):
    R(0,0,16,16,'ash')
    for i in range(7):
        a,b=h32(*s,i),h32(*s,i+11); R(int(a*15),int(b*15),1,1,'ashD' if i%2 else 'ashL')
tiles_s['cinza_0']=tile(ash,(3,8)); tiles_s['cinza_1']=tile(ash,(10,2))
def ashe(R,blob,s):
    ash(R,blob,s)
    for (x,y) in ((3,4),(11,3),(6,11),(12,12)): R(x,y,1,1,'emb');R(x+1,y,1,1,'crack')
tiles_s['cinza_brasas']=tile(ashe)
def basalt(R,blob,s):
    R(0,0,16,16,'basD')
    for (x,y,w,h) in ((0,0,7,7),(8,0,8,6),(0,8,6,8),(7,7,9,9)): R(x,y,w,h,'bas');R(x,y,w,1,'basL');R(x,y,1,h,'basL')
tiles_s['caminho_basalto']=tile(basalt)
def deadtree(R,blob,s):
    ash(R,blob,s);R(7,6,2,10,'dead');R(7,6,1,10,'deadL');R(4,3,1,4,'dead');R(5,5,2,1,'dead');R(11,2,1,5,'dead');R(9,6,2,1,'dead');R(6,1,1,5,'dead');R(9,9,3,1,'dead');R(12,8,1,2,'dead')
tiles_s['arvore_morta']=tile(deadtree)
def vrock(R,blob,s):
    ash(R,blob,s);blob(1,3,14,12,'vrock');blob(2,4,12,10,'vrockL');R(4,6,4,1,'crack');R(7,7,1,3,'crack');R(8,9,3,1,'crack');R(3,4,4,1,(90,80,82,255))
tiles_s['rocha_vulcanica']=tile(vrock)
def portal(R,blob,s):
    R(1,2,4,14,'stoneD');R(11,2,4,14,'stoneD');R(2,2,2,14,'stone');R(12,2,2,14,'stone');R(2,2,1,14,'stoneL');R(12,2,1,14,'stoneL')
    R(1,0,14,4,'stoneD');R(2,1,12,2,'stone');R(2,1,12,1,'stoneL');R(5,4,6,12,(8,10,14,255));R(7,1,2,2,'rune');R(2,6,1,1,'rune');R(13,6,1,1,'rune');R(2,10,1,1,'rune');R(13,10,1,1,'rune')
tiles_s['portal_santuario']=tile(portal)

enemies_s={}
SAL=["................","................","..............kk","..............kr","..............kr",".............krr",".............kre","...kk.......krrr","..krrk.....krree","..krrrk...krrrre","...kkrrkkkrrrree",".....krrrrrrreee","......krrrrrreee","......krrrrrrEee","......krrrrrrree",".....krrrrrrreee","...kkrrkkkrrrree","..krrrk...krrrre","..krrk.....krrrr","...kk.......krrr","............krrr","...........krrrr","..........krrrrr","..........krYkrr","..........krrrrr","...........krrrr","............kkrr","..............kk","................","................","................","................"]
sl=grid(mirror('salamandra',SAL),size=(32,32))
enemies_s['salamandra_0']=sl; enemies_s['salamandra_1']=shift(sl,0,1); enemies_s['salamandra_tonta']=recolor(sl,{'r':(160,70,50,255),'Y':'w'}); enemies_s['salamandra_dano']=flash(sl)
ck=enemies_m['caranguejo_0'].resize((32,32),Image.NEAREST)
ck=recolor(ck,{'r':'Z','R':'z'})
px=ck.load()
for (x,y) in ((12,2),(14,1),(16,0),(17,0),(18,1),(20,2),(13,3),(15,3),(16,3),(17,3),(18,3),(19,3)): px[x,y]=PAL['y']
enemies_s['caranguejo_rei']=ck; enemies_s['caranguejo_rei_1']=shift(ck,0,1)
enemies_s['caranguejo_rei_virado']=ck.transpose(Image.FLIP_TOP_BOTTOM); enemies_s['caranguejo_rei_dano']=flash(ck)
im=Image.new('RGBA',(16,16),(0,0,0,0));dd=ImageDraw.Draw(im);dd.ellipse([4,4,11,11],outline=PAL['c'],fill=(138,212,232,90));dd.point((6,6),fill=PAL['w']);dd.point((7,6),fill=PAL['w'])
enemies_s['bolha']=im


# =============== MASMORRAS — mecanismos e decoração ===============
mech={}
def peg(up,col,colL,colD):
    im,R=canvas()
    if up:
        R(2,3,12,12,'k');R(3,4,10,10,colD);R(3,4,10,8,col);R(4,5,8,2,colL);R(4,5,2,6,colL);R(3,12,10,2,colD);R(2,14,12,1,'k')
    else:
        R(2,9,12,6,'k');R(3,10,10,4,colD);R(4,10,8,1,col);R(3,13,10,1,'k')
    return im
for nm,(c,cl,cd) in {'azul':('u','c','T'),'laranja':('e','E','R')}.items():
    mech['pino_alto_'+nm]=peg(True,c,cl,cd); mech['pino_baixo_'+nm]=peg(False,c,cl,cd)
def orb(col,colL,colD):
    im=Image.new('RGBA',(16,16),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rectangle([3,12,12,15],fill=PAL['k']);d.rectangle([4,12,11,14],fill=PAL['A'])
    d.ellipse([2,1,13,12],fill=PAL['k']);d.ellipse([3,2,12,11],fill=PAL[colD]);d.ellipse([4,3,11,10],fill=PAL[col])
    d.rectangle([5,4,6,5],fill=PAL['w']);d.point((7,4),fill=PAL[colL]);return im
mech['orbe_azul']=orb('u','c','T'); mech['orbe_laranja']=orb('e','E','R')
for i in range(2):
    im,R=canvas();R(3,11,10,4,'k');R(4,12,8,2,'A');R(4,12,8,1,'a')
    if i==0: R(7,3,2,9,'k');R(7,4,1,7,'G');R(5,1,6,4,'k');R(6,2,4,2,'r')
    else: R(9,5,2,7,'k');R(9,6,1,5,'G');R(9,2,6,4,'k');R(10,3,4,2,'v')
    mech[f'alavanca_{i}']=im
im,R=canvas();R(0,1,16,14,'k');R(1,2,14,12,'N');R(1,2,14,1,'n')
for yy in (5,9): R(1,yy,14,1,'k')
for xx in (3,12): R(xx,3,1,1,'G');R(xx,11,1,1,'G')
mech['plataforma']=im
# itens de masmorra
im,R=canvas();R(2,3,12,11,'k');R(3,4,10,9,'W');R(3,4,10,1,'g');R(5,6,3,2,'n');R(9,7,2,4,'n');R(5,10,4,1,'n');R(10,5,1,1,'r');R(1,3,2,11,'n');R(13,3,2,11,'n')
mech['mapa_masmorra']=im
im=Image.new('RGBA',(16,16),(0,0,0,0));d=ImageDraw.Draw(im);d.ellipse([1,2,14,15],fill=PAL['k']);d.ellipse([2,3,13,14],fill=PAL['y']);d.ellipse([4,5,11,12],fill=PAL['g'])
d.polygon([(7,5),(9,5),(8,8)],fill=PAL['r']);d.polygon([(7,12),(9,12),(8,9)],fill=PAL['u']);d.rectangle([7,0,8,2],fill=PAL['k'])
mech['bussola']=im
im,R=canvas();R(3,1,10,14,'k');R(4,2,8,12,'y');R(4,2,8,2,'Y');R(6,5,4,4,'k');R(7,6,2,2,'r');R(5,11,6,1,'R')
mech['chave_chefe']=im
def column(R,blob,s):
    floor(R,blob,s);R(2,13,12,3,'wallD');R(3,1,10,13,'wallD');R(4,1,8,13,'rockD');R(5,1,3,13,'rock');R(5,1,1,13,'rockL');R(2,0,12,2,'rockD');R(3,0,10,1,'rock')
mech['coluna']=tile(column)
def bones(R,blob,s):
    floor(R,blob,s);R(3,9,7,1,'rockL');R(2,8,2,3,'rockL');R(9,8,2,3,'rockL');R(10,4,3,3,'rockL');R(11,5,1,1,'floorD');R(5,12,4,1,'rockD')
mech['ossos']=tile(bones)
def rubble(R,blob,s):
    floor(R,blob,s);blob(2,8,5,4,'rockD');blob(3,8,3,3,'rock');blob(9,10,4,3,'rockD');blob(10,10,3,3,'rock');R(7,4,2,2,'rockD')
mech['entulho']=tile(rubble)
def upstairs(R,blob,s):
    R(0,0,16,16,'wallD')
    for i in range(5): R(1,13-i*3,14,3,'rockD');R(1,13-i*3,14,1,'rockL');R(2,14-i*3,12,1,'rock')
mech['escada_sobe']=tile(upstairs)
def drypit(R,blob,s): R(0,0,16,16,(20,26,30,255));R(0,0,16,3,(34,46,54,255));R(2,8,3,1,(44,60,70,255));R(10,12,4,1,(44,60,70,255))
mech['fosso_seco']=tile(drypit)
def wetfloor(R,blob,s):
    floor(R,blob,s);R(3,4,5,2,'waterL');R(4,5,3,1,'water');R(9,10,4,2,'waterL');R(10,11,2,1,'water')
mech['piso_molhado']=tile(wetfloor)
def cwall(R,blob,s):
    wall(R,blob,s);R(5,4,1,4,'black');R(6,7,3,1,'black');R(8,8,1,4,'black');R(9,11,2,1,'black');R(4,3,1,1,'black')
mech['parede_rachada']=tile(cwall)
for n in ('coluna','ossos','entulho','escada_sobe','parede_rachada','piso_molhado'):
    mech[n+'_mares']=remap(mech[n],{**SEA_IN,**SEA_OUT}); mech[n+'_ventos']=remap(mech[n],{**SKY_IN})
# =============== MONTAGEM DA FOLHA ===============
SECTIONS=[('Herói — Lume',{**hero_sprites,**weapons}),('Herói — ataques',attack),('Inimigos',enemies),('Chefe',bosses),
          ('Personagens',chars),('Objetos e itens',objs),('Cenário — Reino da Brasa',tiles),('Inimigos — Marés',enemies_m),('Chefe — Kraken',bosses_m),('Personagens — Marés',chars_m),('Cenário — Reino das Marés',tiles_m),('Inimigos — Ventos',enemies_v),('Chefe — Grifo',bosses_v),('Personagens e espada — Ventos',chars_v),('Cenário — Reino dos Ventos',tiles_v),('Santuários — mini-chefes',enemies_s),('Santuários — cenário',tiles_s),('Masmorras — mecanismos',mech)]
if BAD:
    for b in BAD: print('LINHA COM TAMANHO ERRADO:',b)
SHEET_W=256
atlas={}; placed=[]; y=0
for title,group in SECTIONS:
    x=0; shelf=0
    for name,img in group.items():
        if x+img.width>SHEET_W: x=0; y+=shelf; shelf=0
        placed.append((name,img,x,y)); atlas[name]={'x':x,'y':y,'w':img.width,'h':img.height,'grupo':title}
        x+=img.width; shelf=max(shelf,img.height)
    y+=shelf
sheet=Image.new('RGBA',(SHEET_W,y),(0,0,0,0))
for name,img,x,yy in placed: sheet.paste(img,(x,yy),img)
sheet.save(os.path.join(OUT,'lenda-da-brasa-sprites.png'))
json.dump({'imagem':'lenda-da-brasa-sprites.png','tile':16,'sprites':atlas},open(os.path.join(OUT,'lenda-da-brasa-atlas.json'),'w'),ensure_ascii=False,indent=1)

# prévia 4x com nomes
S=4; CELLW=16*S+60; PAD=24
try:
    f_title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
    f_lab=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
except Exception:
    f_title=ImageFont.load_default(26); f_lab=ImageFont.load_default(12)
COLS_PER_ROW=10; W_PREV=PAD*2+COLS_PER_ROW*CELLW
blocks=[]
for title,group in SECTIONS:
    rows=[];row=[];rw=0
    for name,img in group.items():
        cw=max(img.width*S+60,CELLW)
        if rw+cw>W_PREV-PAD*2: rows.append(row);row=[];rw=0
        row.append((name,img,cw)); rw+=cw
    if row: rows.append(row)
    blocks.append((title,rows))
H_PREV=PAD
for title,rows in blocks:
    H_PREV+=44
    for row in rows: H_PREV+=max(i.height for _,i,_ in row)*S+34
    H_PREV+=12
prev=Image.new('RGBA',(W_PREV,H_PREV),rgba('#120d0c')); d=ImageDraw.Draw(prev)
yy=PAD
for title,rows in blocks:
    d.text((PAD,yy),title.upper(),font=f_title,fill=rgba('#ffd27a')); yy+=44
    for row in rows:
        rh=max(i.height for _,i,_ in row)*S; x=PAD
        for name,img,cw in row:
            big=img.resize((img.width*S,img.height*S),Image.NEAREST)
            bx=x+(cw-big.width)//2
            d.rectangle([bx-2,yy-2,bx+big.width+1,yy+big.height+1],fill=rgba('#1d1514'),outline=rgba('#3a2a26'))
            prev.paste(big,(bx,yy),big)
            tw=d.textlength(name,font=f_lab)
            label=name if tw<=cw-4 else name.replace('_','_​')
            d.text((x+cw/2,yy+rh+6),name,font=f_lab,fill=rgba('#a8968a'),anchor='ma')
            x+=cw
        yy+=rh+34
    yy+=12
prev.convert('RGB').save(os.path.join(OUT,'lenda-da-brasa-preview.png'))

# zip com PNGs individuais
with zipfile.ZipFile(os.path.join(OUT,'lenda-da-brasa-sprites.zip'),'w',zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(OUT,'lenda-da-brasa-sprites.png'),'lenda-da-brasa-sprites.png')
    z.write(os.path.join(OUT,'lenda-da-brasa-atlas.json'),'lenda-da-brasa-atlas.json')
    pastas={'Herói — Lume':'heroi','Herói — ataques':'heroi','Inimigos':'inimigos','Chefe':'chefe','Personagens':'personagens','Objetos e itens':'objetos','Cenário — Reino da Brasa':'cenario','Inimigos — Marés':'mares/inimigos','Chefe — Kraken':'mares/chefe','Personagens — Marés':'mares/personagens','Cenário — Reino das Marés':'mares/cenario','Inimigos — Ventos':'ventos/inimigos','Chefe — Grifo':'ventos/chefe','Personagens e espada — Ventos':'ventos/personagens','Cenário — Reino dos Ventos':'ventos/cenario','Santuários — mini-chefes':'santuarios/inimigos','Santuários — cenário':'santuarios/cenario','Masmorras — mecanismos':'masmorras'}
    for title,group in SECTIONS:
        for name,img in group.items():
            b=io.BytesIO(); img.save(b,'PNG'); z.writestr(f'{pastas[title]}/{name}.png',b.getvalue())
print('sprites:',len(atlas),'folha:',sheet.size,'previa:',prev.size)
