# Gera os dados dos 3 castelos (mapas, ligações, escadas, baús, armadilhas) para o template.
import json, sys, os

ROOMS = {}   # id -> dict
def room(id, k, fl, gx, gy, name, rows, en=(), **kw):
    assert id not in ROOMS, id
    ROOMS[id] = dict(id=id, k=k, fl=fl, gx=gx, gy=gy, name=name, rows=rows, en=list(en), **kw)

THEME = {'brasa': 'dungeon', 'mares': 'seacastle', 'ventos': 'skycastle'}
CNAME = {'brasa': 'Castelo da Brasa', 'mares': 'Castelo das Marés', 'ventos': 'Castelo dos Ventos'}

# ======================= CASTELO DA BRASA (20 salas) =======================
# Térreo (fl 0) e Subsolo (fl -1). Item: Bastão de Brasa (subsolo, d19).
room('d0','brasa',0,2,3,'Átrio',[
"#######LL#######",
"#VV,,,,KK,,,,VV#",
"#,O,,,,KK,,,,O,#",
"#,,,,,,KK,,,,,,#",
"#,,c,,,KK,,,c,,#",
",,,,,,,KK,,,,,,,",
"#,,c,,,KK,,,c,,#",
"#,,,,,,KK,,,,,,#",
"#,O,,,,KK,,P,O,#",
"#,,,,,,KK,,,,,,#",
"#######XX#######"],[['bat',4,3],['bat',11,7]], exit=True)
room('d2','brasa',0,1,3,'Galeria Oeste',[
"#######,,#######",
"#H,,U,,,,,,U,,,#",
"#,,,,,,,,,,,,,,#",
"#,cc,,cc,,cc,,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,,,,,,,,,,,",
"#,cc,,cc,,cc,,,#",
"#,,,,,,,,,,,,,,#",
"#,,U,,,,,,,U,,V#",
"#,V,,,,,,,,,,VV#",
"################"],[['knight',5,4],['knight',10,7],['slime',8,2]], chests={(1,1):'map'})
room('d11','brasa',0,1,2,'Sala das Colunas',[
"#######,,#######",
"#111,,,22,,,,,,#",
"#1H1,,,,,,,,,,,#",
"#111,,c,,,,c,,,#",
"#,,,,,,,,,,,,,,#",
",,,,,,,,k,,,,,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,c,,,,c,,,#",
"#,V,,,,,,,,,,,V#",
"#,,,,,,,,,,,,,,#",
"#######,,#######"],[['bat',4,6],['bat',12,3],['slime',10,8]], chests={(2,2):'key'})
room('d10','brasa',0,0,2,'Fosso de Lava',[
"#######,,#######",
"#~~~~~~,,~~~~~~#",
"#~Q,,,,,,~~,H~~#",
"#~~,~~~~~~~~~~~#",
"#~~,~~,,,,,,~~~#",
"#~~,~~,~~~~,,,,,",
"#~~,,,,~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"################"],[['spit',8,4],['spit',4,2],['bat',8,8]], chests={(12,2):'piece'})
room('d5','brasa',0,0,1,'Câmara Escura',[
"################",
"#J,,,,,,,,,,,,J#",
"#,X,,oo,,,oo,,,#",
"#,,,,oo,,,oo,,,#",
"#,oo,,,,e,,,,oo#",
"#,oo,,,,,,,,,,,,",
"#,,,,,oo,,oo,,,#",
"#,e,,,oo,,oo,,,#",
"#J,,,,,,,,,,,,J#",
"#,,,,,,,,,,,,,,#",
"#######,,#######"],[['bat',5,4],['bat',10,8],['slime',12,2]], dark=True)
room('d6','brasa',0,1,1,'Corredor das Armaduras',[
"################",
"#U,U,U,U,U,U,U,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,KKKK,,,,,#",
",,,,,,K,,K,,,,,#",
"#,,,,,KKKK,,,,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,,,,,,,,,,#",
"#U,U,U,,,,U,U,U#",
"#######,,#######"],[['knight',4,3],['knight',11,3],['bat',7,7]],
   trap=[[['knight',4,7],['knight',11,7],['slime',3,3],['slime',12,3],['bat',7,2]]], clear=(7,5,'compass'))
room('d3','brasa',0,3,3,'Arsenal',[
"################",
"#,,,,,,,,,,#,H,#",
"#,,,M,,,,,,#,,,#",
"#,,,,,,c,,,##S##",
"#,I,,,,,,,,,,,,#",
",,,,,,,,M,,,,,,#",
"#,,c,,,,,,,,c,,#",
"#,,,,,,M,,,,,,,#",
"#,,,,,,,,,,,I,,#",
"#,V,,,,,,,,,,,V#",
"################"],[['knight',10,6],['slime',5,8]], chests={(13,1):'piece'}, blocks=[(13,3)])
room('d12','brasa',0,2,2,'Salão Central',[
"#######,,#######",
"#U,,,,,KK,,,,,U#",
"#,c,,c,KK,c,,c,#",
"#,,,,,,KK,,,,,,#",
"#,c,,c,KK,c,,c,#",
"#,,,,,,KK,,,,,,Z",
"#,c,,c,KK,c,,c,#",
"#,,,,,,KK,,,,,,#",
"#,c,,c,KK,c,,c,#",
"#V,,,,,KK,,,,,V#",
"#######LL#######"],[['knight',3,3],['knight',12,7],['spit',4,7],['spit',11,3]])
room('d7','brasa',0,2,1,'Antessala do Trono',[
"#######GG#######",
"#F,,,,,KK,,,,,F#",
"#,U,,,,KK,,,,U,#",
"#,,,,,,KK,,,,,,#",
"#,~~~,,KK,,~~~,#",
"#,~~~,,KK,,~~~,,",
"#,,,,,,KK,,,,,,#",
"#,U,,,,KK,,,,U,#",
"#F,,,,,KK,,,P,F#",
"#,,,,,,KK,,,,,,#",
"#######,,#######"],[['spit',4,7],['spit',11,2]])
room('d13','brasa',0,3,2,'Forja',[
"#######LL#######",
"#,,,,,,,,,,,,,,#",
"#,~~~~,,,,~~~~,#",
"#,~~~~,FF,~~~~,#",
"#,,,,,,,,,,,,,,#",
"Z,,,,,,,,,,,,,,Z",
"#,,,,,,,,,,,,,,#",
"#,O,,,c,,c,,,O,#",
"#,,,,,,,,,,,X,,#",
"#,V,,,,,,,,,,,V#",
"################"],[['knight',4,6],['knight',10,4],['slime',8,8]])
room('d14','brasa',0,4,2,'Sala dos Quatro Braseiros',[
"################",
"#J,,~~~~~~~~,,J#",
"#,,,~~~~~~~~,,,#",
"#,,,,,,,,,,,,,,#",
"#~~~,,,,,,,,~~~#",
"Z,,,,,,,,,,,,,,#",
"#~~~,,,,,,,,~~~#",
"#,,,,,,,,,,,,,,#",
"#,,,~~~~~~~~,,,#",
"#J,,~~~~~~~~,,J#",
"################"],[['bat',6,3],['bat',9,7],['spit',12,5]], lit=dict(t=6,chest=(7,5,'key'),msg='UM BAÚ APARECEU!'))
room('d8','brasa',0,3,1,'Biblioteca Queimada',[
"################",
"#J,,,,,,,,,,,,J#",
"#,cccc,,,,cccc,#",
"#,,,,,,,,,,,,,,#",
"#,cccc,,,,cccc,#",
",,,,,,,,,,,,,,,,",
"#,cccc,,,,cccc,#",
"#,,,,,,,,,,,,,,#",
"#,cccc,,,,cccc,#",
"#J,,,,,,,,,,,,J#",
"#######LL#######"],[['spit',7,3],['bat',3,7],['bat',12,3],['knight',8,7]], dark=True)
room('d9','brasa',0,4,1,'Torre Leste',[
"################",
"#,,,#,P,,,#,,,,#",
"#,k,#,,,,,#,,H,#",
"#,,,#,,,,,#,,,,#",
"##2##,,,,,#,,,,#",
",,,,,,,,,,1Z,,,#",
"#,,,,,,,,,#,,,,#",
"#,,,,c,,c,#,,,,#",
"#,,,,,,,,,#,,,,#",
"#V,,,,,,,V#,,,V#",
"################"],[['knight',6,6],['knight',3,8]], chests={(13,2):'master'})
# subsolo
room('d15','brasa',-1,0,1,'Cripta',[
"################",
"#,,,,,,,,,,,,,,#",
"#,%,,e,,,,,e,,,#",
"#,,,,,,,,,,,,,,#",
"#,UU,,UU,,UU,,,#",
"#,,,,,,,,,,,,,,,",
"#,UU,,UU,,UU,,,#",
"#,,e,,,,,,,,e,,#",
"#,,,,,,,,,,,,,,#",
"#,V,,,,,,,,,,,V#",
"#######,,#######"],[['slime',6,3],['slime',10,7],['bat',12,2],['bat',4,8]], dark=True)
room('d18','brasa',-1,0,2,'Poço das Almas',[
"#######,,#######",
"#,,,,,,,,,,,,,,#",
"#,,oo,,,,,,oo,,#",
"#,,oo,,,,,,oo,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,oooo,,,,,#",
"#,,,,,oooo,,,,,#",
"#,,oo,,,,,,oo,,#",
"#,,oo,,,,,,oo,,#",
"#V,,,,,,,,,,,,V#",
"################"],[['slime',4,4],['slime',11,4],['slime',7,8],['bat',7,2]],
   trap=[[['knight',4,4],['knight',11,8],['bat',2,6],['bat',13,6]]], clear=(7,8,'key'))
room('d16','brasa',-1,1,1,'Ossuário',[
"#######zz#######",
"#e,,,,,,,,,,,,e#",
"#,,uu,,,,,,uu,,#",
"#,,uu,,,,,,uu,,#",
"#,,,,,,ee,,,,,,#",
",,,,,,,,,,,,,,,L",
"#,,,,,,ee,,,,,,#",
"#,,uu,,,,,,uu,,#",
"#,,uu,,,,,,uu,,#",
"#e,,,,,,,,,,,,e#",
"################"],[['slime',5,5],['slime',10,5],['knight',8,8]])
room('d20','brasa',-1,1,0,'Câmara Esquecida',[
"################",
"################",
"##F,,,,,,,,,,F##",
"##,,,,,,,,,,,,##",
"##,,V,,,,,,V,,##",
"##,,,,,,H,,,,,##",
"##,,V,,,,,,V,,##",
"##,,,,,,,,,,,,##",
"##F,,,,,,,,,,F##",
"##,,,,,,,,,,,,##",
"#######zz#######"],[], chests={(8,5):'embers50'})
room('d17','brasa',-1,2,1,'Ponte das Chamas',[
"################",
"#~~~~~~~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"#~~~~~~,k,~~~~~#",
"L,,2,,,,,,,,1,,,",
"#~~~~~~,,,~~~~~#",
"#~~~~~~~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"#~~~~~~~~~~~~~~#",
"################"],[['bat',5,2],['bat',10,8],['bat',12,3]])
room('d19','brasa',-1,3,1,'Câmara do Bastão',[
"################",
"#U,,,,#,,#,,,,U#",
"#,,,,,#Y,#,,,,,#",
"#,,,,,#SS#,,,,,#",
"#,,,,,,,,,,,,,,#",
",,,,,,,,,,,,,,,#",
"#,,c,,,,,,,,c,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,,,,,,,,%,#",
"#U,,,,,,,,,,,,U#",
"################"],[['knight',4,6],['knight',11,6],['spit',7,8]],
   trap=[[['knight',3,4],['knight',12,4],['bat',5,8],['bat',10,8],['spit',7,6]]], trapOpen=[(7,3),(8,3)], chests={(7,2):'rod'})

# ======================= CASTELO DAS MARÉS (16 salas) =======================
# '3' água da maré (cheia = água, vazante = chão), '4' plataforma (cheia = flutua, vazante = buraco), 'j' alavanca das comportas
room('c0','mares',0,2,3,'Átrio',[
"#######,,#######",
"#q,,,,3333,,,,q#",
"#,,,,,3333,,,,,#",
"#,,ww,,KK,,ww,,#",
"#,,ww,,KK,,ww,,#",
",,,,,,,KK,,,,,,,",
"#,,,,,,KK,,,,,,#",
"#,U,,,,KK,,,,U,#",
"#,,,,,,KK,,,P,,#",
"#V,,,,,KK,,,,,V#",
"#######XX#######"],[['crab',4,7],['crab',11,6]], exit=True)
room('c1','mares',0,1,3,'Ala Oeste',[
"#######,,#######",
"#,,,,,,,,,,,,,H#",
"#,www,,,,,,www,#",
"#,www,,q,,,www,#",
"#,,,,,,,,,,,,,,#",
"#,,,q,,,,,,q,,,,",
"#,,,,,,,,,,,,,,#",
"#,www,,,,q,www,#",
"#,www,,,,,,www,#",
"#V,,,,,,,,,,,,V#",
"################"],[['crab',6,4],['crab',9,8],['jelly',12,4]], chests={(14,1):'map'})
room('c10','mares',0,1,2,'Grande Poço',[
"################",
"#wwwwwwwwwwwwww#",
"#ww,H,44444wwww#",
"#ww,,,wwww4wwww#",
"#wwwwwwwww4wwww#",
",,,,,,,,,,,,,,,#",
"#,,q,,,,,,,,q,,#",
"#,,,,,,,,,,,,,,#",
"#,,,,,ww,,,,,,,#",
"#V,,,,ww,,,,,,V#",
"#######,,#######"],[['crab',4,7],['crab',11,8],['jelly',7,3]], chests={(4,2):'key'})
room('c9','mares',0,0,2,'Comportas',[
"#######LL#######",
"#,,,,,,,,,,,,,,#",
"#,,j,,,,,,,,,,,#",
"#,,,,3333333,,,#",
"#,,,,3333333,,,#",
"#,,,,,,,,,,,,,,,",
"#,,,,,,,,,,,,,,#",
"#,U,,,,,,,,,,U,#",
"#,,,,,,,P,,,,,,#",
"#V,,,,,,,,,,,,V#",
"################"],[['coral',12,2],['crab',6,7]])
room('c5','mares',0,0,1,'Aquário',[
"################",
"#q,,,,,,,,,,,,q#",
"#,33333,,,,,,,,#",
"#,33X33,,ww,,,,#",
"#,33333,,ww,,,,#",
"#,,,,,,,,ww,,,,,",
"#,,,,,,,,ww,,,,#",
"#,,q,,,,,,,,q,,#",
"#,,,,,,,,,,,,,,#",
"#V,,,,,,,,,,,,V#",
"#######LL#######"],[['jelly',7,3],['jelly',12,7],['crab',5,8]])
room('c6','mares',0,1,1,'Galeria das Conchas',[
"################",
"#q,,,,,,,,,,,,q#",
"#,,ww,,,,,,ww,,#",
"#,,ww,,,,,,ww,,#",
"#,,,,,,,,,,,,,,#",
",,,,,,,,,,,,,,,#",
"#,,,,,,,,,,,,,,#",
"#,,ww,,,,,,ww,,#",
"#,,ww,,,,,,ww,,#",
"#q,,,,,,,,,,,,q#",
"################"],[['crab',5,4],['crab',10,6],['jelly',7,2]],
   trap=[[['coral',5,6],['coral',10,4],['crab',7,8],['jelly',3,5],['jelly',12,5]]], clear=(7,5,'compass'))
room('c11','mares',0,2,2,'Ponte da Maré',[
"#######,,#######",
"#,,,,,,,,,,,,,,#",
"#33333344333333#",
"#33333344333333#",
"#,,,,,,,,,,,,,,#",
"#,,q,,,,,,,,q,,,",
"#,,,,,,,,,,,,,,#",
"#ww,,,,,,,,,,ww#",
"#ww,,,,,,,,,,ww#",
"#,,,,,,,,,,,,,,#",
"#######,,#######"],[['jelly',4,1],['jelly',11,8],['crab',7,6]])
room('c7','mares',0,2,1,'Antessala do Trono',[
"#######GG#######",
"#q,,,,,KK,,,,,q#",
"#,U,,,,KK,,,,U,#",
"#,,ww,,KK,,ww,,#",
"#,,ww,,KK,,ww,,#",
"#,,,,,,KK,,,,,,#",
"#,,ww,,KK,,ww,,#",
"#,,ww,,KK,,ww,,#",
"#,U,,,,KK,,,,U,#",
"#q,,,,,KK,,P,,q#",
"#######,,#######"],[['coral',4,5],['coral',11,5],['jelly',7,3]])
room('c12','mares',0,3,2,'Docas',[
"#######LL#######",
"#,,Q,,,,,,,,,H,#",
"#,,,,,,,,,,,,,,#",
"#wwwwwwwwwwwwww#",
"#wwwwwwwwwwwwww#",
",,,,,,,,,,,,,,,#",
"#,,,,,,,,,,,Q,,#",
"#,,q,,,,,,,,,,,#",
"#,,,,,,,,,,,X,,#",
"#V,,,,,,,,,,,,V#",
"#######,,#######"],[['crab',5,6],['crab',9,8],['jelly',8,4]], chests={(13,1):'embers'})
room('c3','mares',0,3,3,'Ala Leste',[
"#######,,#######",
"#,,,,,,,,,#,H,,#",
"#,,M,,,,,,#,,,,#",
"#,,,,,ww,,##S###",
"#,,,,,ww,,,,,,,#",
",,,,,,,,,,,M,,,#",
"#,,I,,,,,,,,,,,#",
"#,,,,,ww,,,,I,,#",
"#,,,M,ww,,,,,,,#",
"#V,,,,,,,,,,,,V#",
"################"],[['crab',8,5],['coral',13,8]], chests={(12,1):'piece'}, blocks=[(12,3)])
room('c8','mares',0,3,1,'Torre do Farol',[
"################",
"#,,,wwwwwwwwwww#",
"#,H,wwwwwwwwwww#",
"#,,,wwwwwQwwwww#",
"#Q,,wwwww,,wwww#",
"#wwwwwwww,,wwww#",
"#wwwwwwwwwwwwww#",
"#wwwwwwwwwwwwww#",
"#,,,,,,,,,,,,,,#",
"#,Q,,,,,,,,,,,,#",
"#######LL#######"],[['jelly',6,6],['jelly',12,2],['coral',12,8]], chests={(2,2):'master'})
# subsolo (cisterna)
room('c13','mares',-1,1,2,'Cisterna',[
"################",
"#,,,,,,,,,,,,,,#",
"#,%,,,,,,,,,,,,#",
"#,,,,333333,,,,#",
"#,,,,3wwww3,,,,#",
"z,,,,3wwww3,,,,,",
"#,,,,333333,,,,#",
"#,,,,,,,,,,,,,,#",
"#,e,,,,,,,,,,e,#",
"#V,,,,,,,,,,,,V#",
"################"],[['crab',3,6],['crab',12,4],['jelly',8,8]])
room('c17','mares',-1,0,2,'Gruta Escondida',[
"################",
"################",
"##q,,,,,,,,,,q##",
"##,,V,,,,,,V,,##",
"##,,,,,,,,,,,,##",
"##,,,,,,H,,,,,,z",
"##,,,,,,,,,,,,##",
"##,,V,,,,,,V,,##",
"##q,,,,,,,,,,q##",
"################",
"################"],[], chests={(8,5):'embers50'})
room('c14','mares',-1,2,2,'Galeria Submersa',[
"################",
"#,,,,,,,,,,,,ww#",
"#,j,,,,,,,,,,ww#",
"#,,,,,,,,,,,,ww#",
"#,,,,,,,,,,,www#",
",,,,,,,,,,,4444,",
"#,,,,,,,,,,,www#",
"#,,,,,,,,,,,,ww#",
"#,,,,,,,,,,,,ww#",
"#V,,,,,,,,,,,ww#",
"################"],[['crab',5,3],['crab',8,7],['jelly',10,5]],
   trap=[[['coral',4,7],['coral',9,3],['crab',6,5],['jelly',3,3]]], clear=(6,5,'key'))
room('c15','mares',-1,3,2,'Câmara do Gancho',[
"################",
"#wwwwwwwwwwww,%#",
"#ww,,Y,wwwwww,,#",
"#ww,,,,wwwwww,Q#",
"#wwww4wwwwwwwww#",
",,,,,4wwwwwwwww#",
"#,,,,,wwwwwwwww#",
"#,,q,,wwwwwwwww#",
"#,,,,,wwwwwwwww#",
"#V,,,,wwwwwwwww#",
"################"],[['jelly',8,6],['jelly',10,3]], chests={(5,2):'hook'})

# ======================= CASTELO DOS VENTOS (16 salas) =======================
# 'r' piso rachado (desaba), 'o' abismo, setas = correntes de vento. Térreo, 1º andar e torre.
room('e0','ventos',0,2,3,'Átrio',[
"#######LL#######",
"#VV,,,,KK,,,,VV#",
"#,U,,,,KK,,,,U,#",
"#,,,,,,KK,,,,,,#",
"#,,oo,,KK,,oo,,#",
",,,oo,,KK,,oo,,,",
"#,,,,,,KK,,,,,,#",
"#,U,,,,KK,,,,U,#",
"#,,,,,,KK,,P,,,#",
"#,,,,,,KK,,,,,,#",
"#######XX#######"],[['harpy',4,2],['harpy',11,7]], exit=True)
room('e1','ventos',0,1,3,'Ala Oeste',[
"#######,,#######",
"#,,,,,,,,,,,,,H#",
"#,oooo,,,,oooo,#",
"#,oooo,,,,oooo,#",
"#,,,,,,,,,,,,,,#",
"z,,,,,,,,,,,,,,,",
"#,,,,,,,,,,,,,,#",
"#,oooo,,,,oooo,#",
"#,oooo,,,,oooo,#",
"#V,,,,,,,,,,,,V#",
"################"],[['harpy',7,3],['archer',7,8],['harpy',12,6]], chests={(14,1):'map'})
room('e2','ventos',0,0,3,'Sala Secreta',[
"################",
"################",
"##,,,,,,,,,,,,##",
"##,V,,,,,,,,V,##",
"##,,,,,,,,,,,,##",
"##,,,,,,H,,,,,,z",
"##,,,,,,,,,,,,##",
"##,V,,,,,,,,V,##",
"##,,,,,,,,,,,,##",
"################",
"################"],[], chests={(8,5):'piece'})
room('e6','ventos',0,1,2,'Jardim Suspenso',[
"################",
"#ooooooooo,,,,,#",
"#ooooooooo,,,H,#",
"#oooo,,,rr,,,,,#",
"#oooo,,,oooorro#",
",,,,oorroooorro#",
"#,,,oorroooorro#",
"#,,,oorroooorro#",
"#,,,oorroooorro#",
"#,,,,,,,,,,,,,,#",
"#######,,#######"],[['harpy',6,4],['harpy',12,1]], chests={(13,2):'key'})
room('e7','ventos',0,0,2,'Torre Oeste',[
"################",
"#,,,,,#,,,,#,,,#",
"#,%,,,#,,,,#,,,#",
"#,,,,,#,,,,#,,,#",
"#,,,,,1,,k,2,,k#",
"#,,,,,1,,,,2,,,,",
"#,,,,,1,,,,2,,,#",
"#,,,,,#,,,,#,,,#",
"#V,,,,#,,,,#,,V#",
"#,,,,,#,,,,#,,,#",
"################"],[['harpy',8,7],['golem',3,7]])
room('e3','ventos',0,3,3,'Ala Leste',[
"#######,,#######",
"#,,,,,,,,,,,,,,#",
"#,U,,,,,,,,,,U,#",
"#,,,,oo,,oo,,,,#",
"#,,,,oo,,oo,,,,#",
",,,,,,,,,,,,,,,#",
"#,,,,oo,,oo,,,,#",
"#,,,,oo,,oo,,,,#",
"#,U,,,,,,,,,,U,#",
"#V,,,,,,,,,,,,V#",
"################"],[['harpy',4,2],['harpy',11,8],['golem',8,5]],
   trap=[[['golem',3,5],['golem',12,5],['harpy',7,2],['harpy',7,8]]], clear=(7,5,'key'))
room('e8','ventos',0,3,2,'Salão das Correntes',[
"################",
"#,,,,,,H,,,,,,,#",
"#oo<<<<<<<<<<<,#",
"#oo<<<<<<<<<<<,#",
"#,,,,,,,,,,,,,,#",
"#,>>>>>>>>>>>oo#",
"#,>>>>>>>>>>>oo#",
"#,,,,,,,,,,,,,,#",
"#oo<<<<<<<<<<<,#",
"#,,,,,,,,,,,,,,#",
"#######,,#######"],[['archer',1,4],['archer',14,7],['harpy',7,4]], chests={(7,1):'compass'})
room('e5','ventos',0,2,2,'Salão dos Ventos',[
"################",
"#U,,,,,,,,,,,,U#",
"#,,,,,,,,,,,,,,#",
"#,,,,,,%,,,,,,,#",
"#,,rr,,,,,,rr,,#",
"#,,rr,,,,,,rr,,#",
"#,,,,,,,,,,,,,,#",
"#,U,,,,KK,,,,U,#",
"#,,,,,,KK,,,,,,#",
"#V,,,,,KK,,,,,V#",
"#######LL#######"],[['whirl',4,7],['harpy',10,2],['harpy',4,2]])
# 1º andar
room('e10','ventos',1,0,2,'Varanda dos Ventos',[
"################",
"#,,,,vvvvvvv,,,#",
"#,X,,vvvvvvv,,,#",
"#,,,,vvvvvvv,,,#",
"#,,,,vvvvvvv,,,#",
"#,,,,vvvvvvv,,,L",
"#,,,,vvvvvvv,,,#",
"#,,,,ooooooo,,,#",
"#,,,,ooooooo,,,#",
"#V,,,ooooooo,,V#",
"################"],[['harpy',8,3],['archer',13,8]])
room('e11','ventos',1,1,2,'Salão do Golem',[
"################",
"#,,,,,,,,,,,,,,#",
"#,U,,,,,,,,,,U,#",
"#,,,oo,,,,oo,,,#",
"#,,,oo,,,,oo,,,#",
"L,,,,,,,,,,,,,,,",
"#,,,oo,,,,oo,,,#",
"#,,,oo,,,,oo,,,#",
"#,U,,,,,,,,,,U,#",
"#,,,,,,,,,,,,,,#",
"################"],[['golem',8,3],['harpy',4,8]],
   trap=[[['golem',4,5],['golem',11,5],['harpy',7,1],['harpy',7,9]]])
room('e12','ventos',1,2,2,'Câmara da Pena',[
"################",
"#U,,,,,,,,,,,o,#",
"#,,,,,111,,,,o,#",
"#,,,,,1Y1,,,,o,#",
"#,,,,,,1,,,,,o,#",
",,,k,,,,,,,,,o,,",
"#,,,,,,2,,,,,o,#",
"#,,,,,2,2,,,,o,#",
"#,,,,,2X2,,,,o,#",
"#U,,,,,2,,,,,o,#",
"################"],[['harpy',10,2],['harpy',10,8]], chests={(7,3):'feather'})
room('e13','ventos',1,3,2,'Ponte Partida',[
"################",
"#,,,,o,<<<o,,%,#",
"#,,,,o,<<<o,,,,#",
"#,,,,o,<<<o,,,,#",
"#,,,,o,<<<o,,,,#",
",,,,,o,<<<o,,,,#",
"#,,,,o,<<<o,,,,#",
"#,,,,o,<<<o,,,,#",
"#,,,,o,<<<o,,H,#",
"#V,,,o,<<<o,,,V#",
"################"],[['harpy',3,3],['harpy',12,6]], chests={(13,8):'key'})
# torre (2º andar)
room('e16','ventos',2,3,1,'Corredor Quebradiço',[
"################",
"#oooooooooooo,,#",
"#ooooooooooooX,#",
"#,rrrrrrrrrrr,,#",
"#,ooooooooooooo#",
"L,ooooooooooooo#",
"#oooooooooooooo#",
"#oooooooooooooo#",
"#oooooooooooooo#",
"#oooooooooooooo#",
"################"],[['harpy',7,6],['harpy',4,1]])
room('e14','ventos',2,2,1,'Antessala do Ninho',[
"#######GG#######",
"#,,,,,,KK,,,,,,#",
"#,U,,,,KK,,,,U,#",
"#,,oo,,KK,,oo,,#",
"#,,oo,,KK,,oo,,#",
",,,,,,,KK,,,,,,L",
"#,,oo,,KK,,oo,,#",
"#,,oo,,KK,,oo,,#",
"#,U,,,,KK,,,,U,#",
"#,,,,,,KK,,,P,,#",
"################"],[['golem',4,8],['harpy',11,2]])
room('e15','ventos',2,1,1,'Mirante do Vendaval',[
"################",
"#,,,o>>>,,,,,,,#",
"#,H,o>>>,,,,,,,#",
"#,,,o>>>,,,,,,,#",
"#oooo,,,,,,,,,,#",
"#,,,,,,,,,,,,,,,",
"#,,,,,,,,,,,,,,#",
"#,,U,,,,,,,,U,,#",
"#,,,,,,,,,,,,,,#",
"#V,,,,,,,,,,,,V#",
"################"],[['golem',8,6],['harpy',11,2],['archer',13,8]], chests={(2,2):'master'})

# escadas: pares (sala, x, y) <-> (sala, x, y)
STAIRS = [
 (('d5',2,2),('d15',2,2)), (('d13',12,8),('d19',13,8)),
 (('c5',4,3),('c13',2,2)), (('c12',12,8),('c15',14,1)),
 (('e7',2,2),('e10',2,2)), (('e5',7,3),('e12',7,8)), (('e13',13,1),('e16',13,2)),
]
BOSS = {'brasa':('d1',2,-1+0,0), 'mares':('c4',2,0), 'ventos':('e4',2,0)}
BOSS_FL = {'d1':0,'c4':0,'e4':2}
BOSS_POS = {'d1':(2,0),'c4':(2,0),'e4':(2,0)}

SIGNS = {
 'd0:11,8':['CASTELO DA BRASA. Chaves pequenas abrem portas comuns, e cada chave serve só neste castelo.','Dizem que no SUBSOLO, abaixo da Câmara Escura, repousa o BASTÃO DE BRASA.'],
 'd7:12,8':['ANTESSALA DO TRONO. A porta grande só se abre com a CHAVE MESTRA, guardada na Torre Leste.'],
 'd9:6,1':['A chama alcança o que a mão não alcança.'],
 'c0:12,8':['CASTELO DAS MARÉS. As águas do castelo obedecem às COMPORTAS, a oeste.','Maré cheia: as plataformas flutuam. Maré vazante: os canais secam.'],
 'c9:8,8':['COMPORTAS. Puxe a alavanca para baixar ou subir as águas de TODO o castelo.'],
 'c7:11,9':['ANTESSALA DO TRONO. O Kraken dorme além da porta grande. A CHAVE MESTRA está na Torre do Farol.'],
 'e0:11,8':['CASTELO DOS VENTOS. Suba a torre. Pisos rachados desabam sob seus pés: não pare em cima deles!'],
 'e14:12,9':['ANTESSALA DO NINHO. O Grifo espera além da porta grande.'],
}

# ---------------- validação e geração ----------------
OPEN = set(",KLGSZzX")
errs = []
for r in ROOMS.values():
    rows = r['rows']
    if len(rows) != 11: errs.append(f"{r['id']}: {len(rows)} linhas")
    for i, row in enumerate(rows):
        if len(row) != 16: errs.append(f"{r['id']} linha {i}: {len(row)} col '{row}'")
if errs:
    print('\n'.join(errs)); sys.exit(1)

grid = {}
for r in ROOMS.values(): grid[(r['k'], r['fl'], r['gx'], r['gy'])] = r['id']
for k, (bid, gx, gy, *_) in [('brasa',('d1',2,0)),('mares',('c4',2,0)),('ventos',('e4',2,0))]:
    grid[(k, BOSS_FL[bid], gx, gy)] = bid

def side_tiles(rows, side):
    if side == 'n': return [rows[0][7], rows[0][8]]
    if side == 's': return [rows[10][7], rows[10][8]]
    if side == 'w': return [rows[5][0]]
    if side == 'e': return [rows[5][15]]
D = {'n': (0,-1), 's': (0,1), 'w': (-1,0), 'e': (1,0)}
OPP = {'n':'s','s':'n','w':'e','e':'w'}
LINKS = {}
BOSS_SOUTH = {'d1': ',', 'c4': ',', 'e4': ','}
for r in ROOMS.values():
    L = {}
    for side, (dx, dy) in D.items():
        t = side_tiles(r['rows'], side)
        if all(c == '#' for c in t): continue
        if side == 's' and r.get('exit'):
            assert t == ['X','X'], r['id']; continue
        nb = grid.get((r['k'], r['fl'], r['gx']+dx, r['gy']+dy))
        if not nb: errs.append(f"{r['id']}: abertura {side} sem vizinho"); continue
        if nb in BOSS_SOUTH:
            assert side == 'n' and t == ['G','G'], (r['id'], t)
            L[side] = nb; continue
        t2 = side_tiles(ROOMS[nb]['rows'], OPP[side])
        if t != t2: errs.append(f"{r['id']}<->{nb}: porta {side} {t} != {t2}")
        L[side] = nb
    # vizinhos com abertura para cá mas sem retorno
    LINKS[r['id']] = L
for a, L in LINKS.items():
    for s, b in L.items():
        if b in BOSS_SOUTH: continue
        if LINKS.get(b, {}).get(OPP[s]) != a: errs.append(f"link quebrado {a}-{s}->{b}")

# escadas
STAIR_JS = {}
def arrival(rid, x, y):
    rows = ROOMS[rid]['rows']
    for dx, dy, d in ((0,1,'down'),(1,0,'right'),(-1,0,'left'),(0,-1,'up')):
        c = rows[y+dy][x+dx]
        if c in ",KerI3": return [rid, (x+dx)*16, (y+dy)*16-4, d]
    errs.append(f'escada sem saída {rid} {x},{y}')
for (a, b) in STAIRS:
    for (r1, x1, y1), (r2, x2, y2) in ((a, b), (b, a)):
        ch = ROOMS[r1]['rows'][y1][x1]
        if ch not in 'X%': errs.append(f'{r1} {x1},{y1} não é escada ({ch})')
        STAIR_JS[f'{r1}:{x1},{y1}'] = arrival(r2, x2, y2)
for r in ROOMS.values():
    for y, row in enumerate(r['rows']):
        for x, ch in enumerate(row):
            if ch in 'X%' and not (r.get('exit') and y == 10) and f"{r['id']}:{x},{y}" not in STAIR_JS:
                errs.append(f"escada solta {r['id']} {x},{y}")
# baús
CHESTS = {}; CLEAR = {}; LIT = {}; BLOCKS = {}; TRAPS = {}; DARK = []
for r in ROOMS.values():
    for (x, y), what in r.get('chests', {}).items():
        if r['rows'][y][x] not in 'HY': errs.append(f"{r['id']} baú {x},{y} = {r['rows'][y][x]}")
        CHESTS[f"{r['id']}:{x},{y}"] = what
    for y, row in enumerate(r['rows']):
        for x, ch in enumerate(row):
            if ch in 'HY' and (x, y) not in r.get('chests', {}): errs.append(f"{r['id']} baú sem conteúdo {x},{y}")
    if 'clear' in r:
        x, y, what = r['clear']; CLEAR[r['id']] = {'x': x, 'y': y, 'f': 'cc_'+r['id']}; CHESTS[f"{r['id']}:{x},{y}"] = what
    if 'lit' in r:
        l = r['lit']; x, y, what = l['chest']
        LIT[r['id']] = {'t': l['t'], 'open': [], 'chest': [x, y], 'f': 'lit_'+r['id'], 'msg': l['msg']}; CHESTS[f"{r['id']}:{x},{y}"] = what
    if 'blocks' in r: BLOCKS[r['id']] = {'open': [list(p) for p in r['blocks']], 'f': 'bl_'+r['id']}
    if 'trap' in r: TRAPS[r['id']] = {'waves': r['trap'], 'open': [list(p) for p in r.get('trapOpen', [])], 'f': 'tr_'+r['id']}
    if r.get('dark'): DARK.append(r['id'])
if errs:
    print('\n'.join(errs)); sys.exit(1)

def js(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':'))
out = []
out.append('// ==== CASTELOS (gerado por castelos.py) ====')
out.append('const CASTLE_MAPS=' + js({r['id']: r['rows'] for r in ROOMS.values()}) + ';')
defs = {}
for r in ROOMS.values():
    d = {'theme': THEME[r['k']], 'k': r['k'], 'name': CNAME[r['k']] + ' · ' + r['name'], 'en': r['en']}
    if r.get('dark'): d['dark'] = True
    defs[r['id']] = d
out.append('const CASTLE_DEF=' + js(defs) + ';')
out.append('const CASTLE_LINKS=' + js(LINKS) + ';')
out.append('const STAIRS=' + js(STAIR_JS) + ';')
out.append('const CASTLE_CHESTS=' + js(CHESTS) + ';')
out.append('const CASTLE_CLEAR=' + js(CLEAR) + ';')
out.append('const CASTLE_LIT=' + js(LIT) + ';')
out.append('const CASTLE_BLOCKS=' + js(BLOCKS) + ';')
out.append('const TRAPS=' + js(TRAPS) + ';')
dg = {r['id']: [r['k'], r['fl'], r['gx'], r['gy']] for r in ROOMS.values()}
dg.update({'d1': ['brasa', 0, 2, 0], 'c4': ['mares', 0, 2, 0], 'e4': ['ventos', 2, 2, 0]})
out.append('const DGRID=' + js(dg) + ';')
out.append('const CASTLE_SIGNS=' + js(SIGNS) + ';')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'castelos.js'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
n = {}
for r in ROOMS.values(): n[r['k']] = n.get(r['k'], 0) + 1
print('ok', {k: v+1 for k, v in n.items()}, 'escadas', len(STAIR_JS), 'baús', len(CHESTS))
