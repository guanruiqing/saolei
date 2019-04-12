#!/usr/bin/python
# -*- coding:utf-8 -*-

def menu():
	print('''	1.简单 9x9
	2.中等 16x16
	3.困难 30x16
	4.自定义
	5.帮助
	0.退出''')
	while True:
		menulevel=input('请选择游戏等级:')
		if menulevel in ['1','2','3','4','5','0']:
			menulevel=int(menulevel)
			break
		else:
			print('请输入对应的游戏等级')
	return menulevel

def mapnum(maplength=0,mapwidth=0,mapboom=0):
	if maplength==0 or mapwidth==0 or mapboom==0:
		print('有地图参数为0，请重新输入参数')
		maplength=input('请输入自定义地图长度:')
		mapwidth=input('请输入自定义地图宽度:')
		mapboom=input('请输入自定义地雷数量:')
	while True:
		if maplength.isdigit() is False:
			maplength=input('请重新输入自定义地图长度:')
		elif mapwidth.isdigit() is False:
			mapwidth=input('请重新输入自定义地图宽度:')
		elif mapboom.isdigit() is False:
			mapboom=input('请重新输入自定义地雷数量:')
		else:
			maplength,mapwidth,mapboom=int(maplength),int(mapwidth),int(mapboom)
			break
	return maplength,mapwidth,mapboom

def mapgenerate():
	mapsystem={}
	mapplayer={}
	for i1 in range(maplength):
		for i2 in range(mapwidth):
			mapsystem[str(i1)+'x'+str(i2)]=0
			mapplayer[str(i1)+'x'+str(i2)]='□'
	mapboomposition=set()
	while len(mapboomposition)<mapboom:
		mapboomposition.add(str(random.randint(0,maplength-1))+'x'+str(random.randint(0,mapwidth-1)))
	for i in mapboomposition:
		mapsystem[i]='B'
	for i1 in range(maplength):
		for i2 in range(mapwidth):
			if mapsystem[str(i1)+'x'+str(i2)]=='B':
				#for i11 in i1-1,i1,i1+1:
				#	for i22 in i2-1,i2,i2+1:
				#		if i11>=0 and i11<=maplength-1 and i22>=0 and i22<=mapwidth-1 and mapsystem[str(i11)+'x'+str(i22)]!='B':
				#			mapsystem[str(i11)+'x'+str(i22)]+=1
				for i in [str(i11)+'x'+str(i22) for i11 in [i1-1,i1,i1+1] for i22 in [i2-1,i2,i2+1]]:
					if i in mapsystem and  mapsystem[i]!='B':
						mapsystem[i]+=1
	return mapsystem,mapplayer

def mapprint(maptype):
	print('  ',end='')
	for i in range(maplength):
		if i <10:
			print('',i,end='')
		else:
			print(i,end='')
	print()
	for i1 in sorted(list(range(mapwidth)),reverse=True):
		if i1<10:
			print('',i1,end='')
		else:
			print(i1,end='')
		for i2 in range(maplength):
			print('',maptype[str(i2)+'x'+str(i1)],end='')
		if i1<10:
			print('',i1)
		else:
			print(i1)
	print('  ',end='')
	for i in range(maplength):
		if i <10:
			print('',i,end='')
		else:
			print(i,end='')
	print()
	
def gameplay():
	gameplayerinput=input('请输入下一步指令：')
	if gameplayerinput is '':
		return 'e'
	elif gameplayerinput in cachemapplayer:
		if cachemapplayer[gameplayerinput]=='□':
			cachemapplayer[gameplayerinput]=cachemapsystem[gameplayerinput]
		if cachemapplayer[gameplayerinput]==0:
			cacheset=set()
			cacheset.add(gameplayerinput)
			cacheset1=set()
			num=0
			while True:
				cacheset2=copy.copy(cacheset)
				for cacheinput in cacheset2:
					n,i1,i2=0,'',''
					for i in range(len(cacheinput)):
						if cacheinput[i]=='x':
							n=1
						elif n==0:
							i1=i1+cacheinput[i]
						elif n==1:
							i2=i2+cacheinput[i]
					i1=int(i1)
					i2=int(i2)
					for i in [str(i11)+'x'+str(i22) for i11 in [i1-1,i1,i1+1] for i22 in [i2-1,i2,i2+1]]:
						if i in cachemapsystem and cachemapsystem[str(i1)+'x'+str(i2)]==0:
							cacheset.add(i)
				if len(cacheset)==num:
					break
				num=len(cacheset)
			for i in cacheset: 
				cachemapplayer[i]=cachemapsystem[i]
		if cachemapplayer[gameplayerinput]=='B':
			return 0
	elif gameplayerinput[0]=='x':
		if gameplayerinput[len(gameplayerinput)-1]=='e':
			return 'e'
		cacheinput=''
		for i in range(1,len(gameplayerinput)):
			cacheinput=cacheinput+gameplayerinput[i]
		if cachemapplayer[cacheinput]=='□':
			cachemapplayer[cacheinput]='X'
		elif cachemapplayer[cacheinput]=='X':
			cachemapplayer[cacheinput]='□'
	elif gameplayerinput[0]=='?':
		if gameplayerinput[len(gameplayerinput)-1]=='e':
			return 'e'
		cacheinput=''
		for i in range(1,len(gameplayerinput)):
			cacheinput=cacheinput+gameplayerinput[i]
		if cachemapplayer[cacheinput]=='□':
			cachemapplayer[cacheinput]='?'
		elif cachemapplayer[cacheinput]=='?':
			cachemapplayer[cacheinput]='□'
	elif gameplayerinput=='q':
		return 'q'
	else:
		return 'e'
	global blank
	blank=maplength*mapwidth
	for i in cachemapplayer:
		if cachemapplayer[i]!='□' and cachemapplayer[i]!='X' and cachemapplayer[i]!='?':
			blank-=1
	if blank==mapboom:
		return 1

def gamehelp():
	print('''1.请按'x轴+x+y轴'的方式输入点击坐标，比如5x7
2.请按'x+x轴+x+y轴'的方式输入地雷坐标，比如x5x7，取消请重复此操作
3.请按'?+x轴+x+y轴'的方式输入不确定坐标，比如?5x7，取消请重复此操作
4.当您输入'x++'或'?++'时，如果遇到输入失误，请在最后添加字符e，否则程序会出错
5.游戏途中，可以按q退出
6.当地图上仅剩地雷坐标没有被点开时，游戏判定为胜利
''')

import copy,random

menulevel=1
while menulevel:
	menulevel=menu()
	print('~'*20)
	if menulevel==1:
		maplength,mapwidth,mapboom=9,9,10
		mapsystem,mapplayer=mapgenerate()
		cachemapsystem=copy.copy(mapsystem)
		cachemapplayer=copy.copy(mapplayer)
		while True:
			mapprint(cachemapplayer)
			x=gameplay()
			print('~'*20)
			if x==0:
				mapprint(cachemapsystem)
				print('\tgameover\n'+'~'*20)
				break
			elif x==1:
				mapprint(cachemapplayer)
				print('\tyou win\n'+'~'*20)
				break
			elif x=='e':
				print('您的输入有误\n'+'~'*20)
			elif x=='q':
				break
	elif menulevel==2:
		maplength,mapwidth,mapboom=16,16,40
		mapsystem,mapplayer=mapgenerate()
		cachemapsystem=copy.copy(mapsystem)
		cachemapplayer=copy.copy(mapplayer)
		while True:
			mapprint(cachemapplayer)
			x=gameplay()
			print('~'*20)
			if x==0:
				mapprint(cachemapsystem)
				print('\tgameover\n'+'~'*20)
				break
			elif x==1:
				print('\tyou win\n'+'~'*20)
				break
			elif x=='e':
				print('您的输入有误\n'+'~'*20)
			elif x=='q':
				break
	elif menulevel==3:
		maplength,mapwidth,mapboom=30,16,99
		mapsystem,mapplayer=mapgenerate()
		cachemapsystem=copy.copy(mapsystem)
		cachemapplayer=copy.copy(mapplayer)
		while True:
			mapprint(cachemapplayer)
			x=gameplay()
			print('~'*20)
			if x==0:
				mapprint(cachemapsystem)
				print('\tgameover\n'+'~'*20)
				break
			elif x==1:
				print('\tyou win\n'+'~'*20)
				break
			elif x=='e':
				print('您的输入有误\n'+'~'*20)
			elif x=='q':
				break
	elif menulevel==4:
		maplength,mapwidth,mapboom=mapnum()
		mapsystem,mapplayer=mapgenerate()
		cachemapsystem=copy.copy(mapsystem)
		cachemapplayer=copy.copy(mapplayer)
		while True:
			mapprint(cachemapplayer)
			x=gameplay()
			print('~'*20)
			if x==0:
				mapprint(cachemapsystem)
				print('\tgameover\n'+'~'*20)
				break
			elif x==1:
				print('\tyou win\n'+'~'*20)
				break
			elif x=='e':
				print('您的输入有误\n'+'~'*20)
			elif x=='q':
				break
	elif menulevel==5:
		gamehelp()
		print('~'*20)
