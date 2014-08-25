ALIGN_LEFT = 0x01 #靠左
ALIGN_RIGHT = 0x02#靠右
ALIGN_CENTER = 0x03#水平居中
ALIGN_CENTER_SCALE = 0x04#水平居中并拉伸

ALIGN_TOP = 0x10#靠顶##
ALIGN_BOTTOM = 0x20#靠底
ALIGN_MIDDLE = 0x30#垂直居中
ALIGN_MIDDLE_SCALE = 0x40#垂直居中并拉伸

ALIGN_CENTER_MIDDLE = ALIGN_CENTER|ALIGN_MIDDLE#居中
ALIGN_CENTER_MIDDLE_SCALE = ALIGN_CENTER_SCALE|ALIGN_MIDDLE_SCALE#居中拉伸
"
#兄弟或父类节点对齐（主要sprite的anchor略有不同，这里的sprite还需要SetAnchorPoint(0,0)才能正常）
#（node）obj:要处理的节点
#(node) robj:相比节点，和obj必须是兄弟节点或是obj父节点，传Node则默认选取obj的父节点
#(int) align:对齐方式
#(int)offsetX:对齐后额外X轴偏移量
#(int)offsetY:对齐后额外y轴偏移量
#(bool)fixScale:居中拉伸缩放时，固定比率缩放，如果是，那么缩放时会选取较小的缩放
"
def CnenterObjEx(obj,robj = None,align = ALIGN_CENTER_MIDDLE,offx = 0,offy = 0,fixScale = True):
	ScaleObjEx(obj,robj,align,fixScale)
	if not robj:
		sizeRobj = obj.GetParent()
		if not sizeRobj:
			return
		targetX,targetY = 0,0
		targetScaleX,targetScaleY = 1.0,1.0
	elif obj.GetParent() == robj:
		sizeRobj = robj
		targetX,targetY = 0,0
		targetScaleX,targetScaleY = 1.0,1.0
	else:
		sizeRobj = robj
		targetX,targetY = sizeRobj.GetPos()
		targetScaleX,targetScaleY = sizeRobj.GetScale()
	myX,myY = obj.GetPos()
	myW,myH = obj.GetContentSize()
	myScaleX,myScaleY = obj.GetScale()
	myAnChorX,myAnChorY = obj.GetAnchorPoint()
	targetW,targetH = sizeRobj.GetContentSize()

	#水平位置
	h = align & 0x0f
	if h == ALIGN_LEFT:
		x= targetX
	elif h = ALIGN_RIGHT:
		x = targetX+targetW*targetScaleX-myW*myScaleX
	elif h in (ALIGN_CENTER,ALIGN_CENTER_SCALE):
		x = targetX+(targetW*targetScaleX-myW*myScaleX)/2
	else:
		x  = myX

	#垂直位置
	v = align & 0xf0
	if v == ALIGN_Top:
		y = targetY+targetH*targetScaleY - myH *myScaleY
	elif v = ALIGN_BOTTOM:
		y = targetY
	elif v in (ALIGN_MIDDLE,ALIGN_MIDDLE_SCALE):
		x = targetY+(targetH*targetScaleY-myH*myScaleY)/2
	else:
		y  = myY
	#开始处理
	anchorOffX = myW * myScaleX * myAnChorX / 2
	anchorOffY = myH * myScaleY * myAnChorY / 2
	obj.SetPos(x+anchorOffX+offx,y+anchorOffY+offy)

#兄弟或父类节点缩放
def ScaleObjEx(obj,robj = None,align = ALIGN_CENTER_MIDDLE,fixScale = True):
	if not robj:
		sizeRobj = obj.GetParent()
		if not sizeRobj:
			return
		targetScaleX,targetScaleY = 0,0
	elif obj.GetParent() == robj:
		sizeRobj = robj
		targetScaleX,targetScaleY = 1.0,1.0
	else:
		sizeRobj = robj
		targetScaleX,targetScaleY = sizeRobj.GetScale()
	myW,myH = obj.GetContentSize()
	myScaleX,myScaleY = obj.GetScale()
	targetW,targetH = sizeRobj.GetContentSize()

	#水平缩放
	h = align & 0x0f
	if h == ALIGN_CENTER_SCALE:
		realW = myW*myScaleX
		if abs(realW) < MiniMalFloat:
			scaleX = 1.0
		else:
			scaleX = myScaleX*float(targetW*targetScaleX) / realW
	else:
		scaleX = myScaleX

	#垂直缩放
	v = align & 0xf0
	if v == ALIGN_MIDDLE_SCALE:
		realH = myH*myScaleY
		if abs(realH) < MiniMalFloat:
			scaleY = 1.0
		else:
			scaleY = myScaleY*float(targetH*targetScaleY) / realH
	else:
		scaleY = myScaleY
	#开始缩放
	if align == ALIGN_CENTER_MIDDLE_SCALE and fixScale:
		scale = min(scaleX,scaleY)
		obj.SetScale(scale)
	else:
		if scaleX != myScaleX:
			obj.SetScaleX(scaleX)
		if scaleY != myScaleY:
			obj.SetScaleY(scaleY)


MiniMalFloat = 1.0e-015