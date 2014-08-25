import cocos2dx
import string
import weakref
import gl




"
GL_ONE = 1
GL_SRC_COLOR = 0x0300
GL_SRC_ALPHA = 0x0302
GL_ONE_MINUS_SRC_ALPHA = 0x0303
GL_ONE_MINUS_SRC_COLOR = 0x0301

GL_DST_ALPHA = 0x0304
GL_ONE_MINUS_DST_ALPHA = 0x0305
"
def TransformResPath(ResName):
	'转化资源路径，如是合图模式则只取最后的分图路径'
	if len(ResName)<=0:
		return
	index = ResName.rfind('/')
	if index ==-1 and (ResName.endswith(".png") or ResName.endswith('.PNG')):
		return ResName
	elif index !=-1 and (ResName.endswith('.png') or ResName.endswith('.PNG')):
		return ResName[index+1:]
	else:
		print "ERROR::TransformResPath",ResName

class AnimKeyData:
	def __init__(self):
		self.m_keyId = -1
		self.m_keyTime = 0.0
		self.m_bIsChangePic = False
		self.m_picFrameName = ""
		self.m_bIsChangePos = False
		self.m_posX = 0.0
		self.m_posY = 0.0
		self.m_bIsTransPos = False
		self.m_bIsChangeScale = False
		self.m_scaleX = 1.0
		self.m_scaleY = 1.0
		self.m_bIsTransScale = False
		self.m_bIsChangeRotate = False
		self.m_angle = 0.0
		self.m_bIsTransRotate = False
		self.m_bIsChangeOpacity = False
		self.m_opacity = 255
		self.m_bIsTransOpacity = False ＃透明度改变是否过度
		self.m_bIsVisible = True #默认为True
		self.m_bIsStartParticle = False
		self.m_bIsStopParticle = False

class LayerData:
	def __init__(self):
		self.m_layerId = -1
		self.m_layerName = "新Layer"
		self.m_anchorX = 0.5
		self.m_anchorY =0.5
		self.m_bIsParticle = False
		self.m_particlePath = ""
		self.m_bIsBlendAdditive = False
		self.m_bIsGhostNode = False
		self.m_IsDebug = False
		self.m_keyDataList = []
		slef.m_sprite = None

		self.m_origBlendScr = gl.GL_ONE#1
		self.m_origBlendDst = gl.GL_ONE_MINUS_SRC_ALPHA#0x0300

	def getKeyData(self,keyId):
		for animKeyData in self.m_keyDataList:
			if animKeyData.m_keyId == keyId:
				return animKeyData

	def clearLayer(self):
		self.m_sprite = None
		self.m_keyDataList = []

	def clearLayerUnusedata(self):
		self.m_keyDataList = []

	def setupLayerNormal(self,parent):
		keyData0 = self.getKeyData(0)
		if self.m_bIsParticle == True:
			if len(slef.m_particlePath) == 0:
				print "粒子文件路径为空，请设置"
				return
			particle = cocos2dx.CParticleSysmQuad(self.m_particlePath)
			if particle:
				if self.m_bIsBlendAdditive:
					particle.SetBlendAdditive(self.m_bIsBlendAdditive)
				particle.SetAnchorPoint(self.m_anchorX,self.m_anchorY)
				particle.SetPos(keyData0.m_posX,keyData0.m_posY)
				particle.SetScaleX(keyData0.m_scaleX)
				particle.SetScaleY(keyData0.m_scaleY)
				particle.SetRotation(keyData0.m_angle)
				particle.SetVisible(keyData0.m_bIsVisible)
				particle.SetParent(parent)
				particle.SetZ(self.m_layerId)
				particle.StopSystem()
			else:
				print "layer load partilce failed!"
			self.m_sprite = particle
		elif self.m_bIsGhostNode:
			node = cocos2dx.CNode()
			node.SetParent(parent)
			node.SetZ(self.m_layerId)
			slef.m_sprite = None
		else:
			if len(keyData0.m_picFrameName) == 0:
				print "ERROR:: key 0 dose not have the picFrame name"
				return
			layerSprite = cocos2dx.CShaderSprite.CreatewithFile(keyData0.m_picFrameName)
			if layerSprite:
				self.m_origBlendScr,self.m_origBlendDst = layerSprite.getBlendFunc()
				if self.m_bIsBlendAdditive:
					layerSprite.SetBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)
				layerSprite.SetAnchorPoint(self.m_anchorX,self.m_anchorY)
				layerSprite.SetPos(keyData0.m_posX,keyData0.m_posY)
				layerSprite.SetParent(parent)
				layerSprite.SetZ(self.m_layerId)
				layerSprite.SetScaleX(keyData0.m_scaleX)
				layerSprite.SetScaleY(keyData0.m_scaleY)
				layerSprite.SetRotation(keyData0.m_angle)
				if keyData0.m_opacity!=255:
					layerSprite.SetOpacity(keyData0.m_opacity)
				layerSprite.SetVisible(keyData0.m_bIsVisible)
			else:
				print "layer load file failed"
			self.m_sprite = layerSprite

	def setupLayerFrame(self,parent):
		keyData0 = self.getKeyData(0)
		if self.m_bIsParticle == True:
			if len(slef.m_particlePath) == 0:
				print "粒子文件路径为空，请设置"
				return
			particle = cocos2dx.CParticleSysmQuad(self.m_particlePath)
			if particle:
				if self.m_bIsBlendAdditive:
					particle.SetBlendAdditive(self.m_bIsBlendAdditive)
				particle.SetAnchorPoint(self.m_anchorX,self.m_anchorY)
				particle.SetPos(keyData0.m_posX,keyData0.m_posY)
				particle.SetScaleX(keyData0.m_scaleX)
				particle.SetScaleY(keyData0.m_scaleY)
				particle.SetRotation(keyData0.m_angle)
				particle.SetVisible(keyData0.m_bIsVisible)
				particle.SetParent(parent)
				particle.SetZ(self.m_layerId)
				particle.StopSystem()
			else:
				print "layer load partilce failed!"
			self.m_sprite = particle
		elif self.m_bIsGhostNode:
			node = cocos2dx.CNode()
			node.SetParent(parent)
			node.SetZ(self.m_layerId)
			slef.m_sprite = None
		else:
			if len(keyData0.m_picFrameName) == 0:
				print "ERROR:: key 0 dose not have the picFrame name"
				return
			spriteFrameCache = cocos2dx.CSpriteFrameCache.getInstance()
			frame = spriteFrameCache.GetSpriteFrameByName(keyData0.m_picFrameName)
			if frame == None:
				print "ERROR:: frame name not exist!%S"%keyData0.m_picFrameName
				return
			layerSprite = cocos2dx.CShaderSprite.CreatewithFile(frame)
			if layerSprite:
				self.m_origBlendScr,self.m_origBlendDst = layerSprite.getBlendFunc()
				if self.m_bIsBlendAdditive:
					layerSprite.SetBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)
				layerSprite.SetAnchorPoint(self.m_anchorX,self.m_anchorY)
				layerSprite.SetPos(keyData0.m_posX,keyData0.m_posY)
				layerSprite.SetParent(parent)
				layerSprite.SetZ(self.m_layerId)
				layerSprite.SetScaleX(keyData0.m_scaleX)
				layerSprite.SetScaleY(keyData0.m_scaleY)
				layerSprite.SetRotation(keyData0.m_angle)
				if keyData0.m_opacity!=255:
					layerSprite.SetOpacity(keyData0.m_opacity)
				layerSprite.SetVisible(keyData0.m_bIsVisible)
			else:
				print "layer load file failed"
			self.m_sprite = layerSprite

class StateDate:
	def __init__(self):
		self.m_stateId = -1
		self.m_stateName = "新状态"
		self.m_animDura = 0.0
		self.m_bIsLoop = False
		self.m_nLoopNum = 0
		self.m_layerDataList = []

	def getLayerData(self,layerId):
		for layerData in self.m_layerDataList:
			if layerData.m_layerId = layerId:
				return layerData

	def clearState(self):
		for layerData in self.m_layerDataList:
			layerData.clearLayer()
		self.m_layerDataList = []

	def clearStateUnusedata(self):
		resLayerList = []
		for layerDatain self.m_layerDataList:
			if layerData.m_sprite!=None:
				resLayerList.append(layerData)
			else:
				layerData.clearLayer()
		self.m_layerDataList = []
		slef.m_layerDataList = resLayerList

	def setupStateNormal(self,parentNode):
		for layerData in self.m_layerDataList:
			layerData.setupLayerNormal(parentNode)

	def _setupStateNormalWithExtraPath(self,parentNode,extraPath):
		"该函数编辑器使用"
		for layerData in self.m_layerDataList:
			layerData._setupStateNormalWithExtraPath(parentNode,extraPath)

	def setupStateFrame(self,parentNode):
		for layerData in self.m_layerDataList:
			layerData.setupLayerFrame(parentNode)

	def setUpStateBatch(self,setUpStateBatch):
		for layerData in self.m_layerDataList:
			layerData.setupLayerBatch(parentNode)

class LevelData:
	def __init__(self):
		self.m_levelId = -1:
		self.m_levelName = "新Level"
		self.m_selectOriginX  = 0.0
		self.m_selectOriginY = 0.0
		self.m_selectRectW = 40.0
		self.m_selectRectH = 30.0
		self.m_infoTagX = 0.0
		self.m_infoTagY = 0.0
		self.m_stateDataList = []

	def getStateDate(self,stateId):
		for stateData in self.m_stateDataList:
			if stateData.m_stateId = stateId:
				return stateData

	def clearLevel(self):
		for stateDate in self.m_stateDataList:
			stateData.clearState()
		self.m_stateDataList = []

	def clearLevelUnuseData(self,useStateId):
		resStateDate = None
		for stateData in self.m_state.m_stateDataList:
			if stateData.m_stateId == useStateId:
				resStateDate = stateData
			else:
				stateData.clearState()

		self.m_stateDataList = []
		if resStateDate:
			self.m_stateDataList.append(resStateDate)
			resStateDate.clearStateUnusedata()

class AnimBlock:
	def __init__(self,filePath,bReserverStates):
		self.m_node = None
		self.m_bReserverStates = bReserverStates
		self.m_bIsPlistRes = False
		self.m_plistPath = ''
		self.m_bFuncAddPlist = True
		self.m_IsOldEditorData = False
		self.m_curLevelId = -1
		self.m_curStateId = -1
		self.m_filePath = filePath

		#额外信息
		self.m_selectOriginX = 0.0
		self.m_selectOriginY = 0.0
		self.m_selectRectW = 40.0
		self.m_selectRectH = 30.0
		self.m_infoTagY = 0.0
		self.m_infoTagX = 0.0

		self.m_levelDataList = []
		self.m_rowNum = 0
		self.m_colNum = 0

	def __del__(self):
		self._clearAnimBlock()

	def _clearAnimBlock(self):
		for levelData in self.m_levelDataList:
			levelData.clearLevel()
		self.m_levelDataList = []

		self.m_bIsPlistRes = False
		self.m_plistPath = ''
		self.m_rowNum = 0
		self.m_colNum = 0

		self.m_curLevelId = -1
		self.m_curStateId = -1

		#额外信息
		self.m_selectOriginX = 0.0
		self.m_selectOriginY = 0.0
		self.m_selectRectW = 40.0
		self.m_selectRectH = 30.0
		self.m_infoTagY = 0.0
		self.m_infoTagX = 0.0

	def _clearUnuseData(self,useLevelId,useStateData):
		resLevelData = None
		for levleData in self.m_levelDataList:
			if levleData.m_levelId = useLevelId:
				resLevelData = levelData
			else:
				levelData.clearLevel()

		self.m_levelDataList = []
		if resLevelData:
			self.m_levelDataList.append(resLevelData)
			resLevelData.clearLevelUnuseData(useStateData)

	def _loadWithNewNode(self):
		"编辑器接口"
		node = cocos2dx.CNode()
		self.m_node = noder
		return node

	def _loadWithPlist(self,plistPath):
		if len(plistPath) == 0:
			print "plistPath is empty,load failed"
			return None
		batchNode = cocos2dx.CSpriteBatchNode.batchNodeWithPlist(plistPath)
		self.m_node = batchNode
		return batchNode

	def _loadAnimBlockWithFile(self,filePath):
		self._clearAnimBlock()

		xmlDocument = cocos2dx.CXmlDocument()
		loadSuccess  = xmlDocument.LoadFile(filePath)
		if not loadSuccess:
			print "File load failed!!%s"%filePath
			return

		blockElement = xmlDocument.Attribute('block')
		if blockElement == None:
			print "there are no <block> element!"
			return 
		txt = blockElement.Attribute('isPlistRes')
		if string.atoi(txt) == 1:
			self.m_bIsPlistRes = True
		else:
			self.m_bIsPlistRes = False
		self.m_plistPath = blockElement.Attribute('plistPath')
		txt = blockElement.Attribute('rowNum')
		if txt:
			self.m_rowNum = string.atoi(txt)
		txt = blockElement.Attribute('colNum')
		if txt:
			self.m_colNum = string.atoi(txt)
		self.m_IsOldEditorData  = False


		LevelElment = blockElement.FirstChildElement("levelInfo")
		if LevelElment == None:
			self.m_IsOldEditorData = True
			LevelElment = blockElement
			txt = blockElement.Attribute('selectOriginX')
			if txt:
				self.m_selectOriginX = string.atof(txt)
			txt = blockElement.Attribute('selectOriginY')
			if txt:
				self.m_selectOriginY = string.atof(txt)
			txt = blockElement.Attribute('selectRectW')
			if txt:
				self.m_selectRectW = string.atof(txt)
			txt = blockElement.Attribute('selectRectH')
			if txt:
				self.m_selectRectH = string.atof(txt)
			txt = blockElement.Attribute('infoTagX')
			if txt:
				self.m_infoTagX = string.atof(txt)
			txt  = blockElement.Attribute(infoTagY)
			if txt:
				self.m_infoTagY = string.atof(txt)

			LevelElment = blockElement

			while(LevelElment):
				if self.m_IsOldEditorData:
					levelData = LevelData()
					levelData.m_levelId = 1
					levelData.m_selectOriginX = self.m_selectOriginX
					levelData.m_selectOriginY = self.m_selectOriginY
					levelData.m_selectRectW = self.m_selectRectW
					levelData.m_selectRectH = self.m_selectRectH
					levelData.m_infoTagX = self.m_infoTagX
					levelData.m_infoTagY = self.m_infoTagY
				else:
					levelData = LevelData()
					txt = levelElment.Attribute('id')
					levelData.m_levelId = string.atoi(txt)
					levelData.m_levelName= levelElement.Attribute('name')
					txt = levelElement.Attribute('selectOriginX')
					if txt:
						leveldata.m_selectOriginX = string.atof(txt)
					txt = levelElement.Attribute('selectOriginY')
					if txt:
						levelData.m_selectOriginY = string.atof(txt)
					txt = levelElement.Attribute('selectRectW')
					if txt:
						levelData.m_selectRectW = string.atof(txt)
					txt = levelElement.Attribute('selectRectH')
					if txt:
						levelData.m_selectRectH = string.atof(txt)
					txt = levelElement.Attribute('infoTagX')
					if txt:
						levelData.m_infoTagX  = string.atof(txt)
					txt = levelElment.Attribute('infoTagY')
					if txt:
						levelData.m_infoTagY = string.atof(txt)

				stateElement = levelElement.FirstChildElement('stateInfo')
				while(stateElement):
					stateData = StateDate()
					txt = stateElement.Attribute('id')
					stateData.m_stateId =  string.atoi(txt)
					stateData.m_stateName = stateElement.Attribute('name')
					txt = stateElement.Attribute('animDura')
					stateData.m_animDura = string.atof(txt)
					txt = stateElement.Attribute('isLoop')
					if string.atoi(txt) == 1:
						stateData.m_IsLoop = True
					else:
						stateData.m_bIsLoop = False
					txt = stateElement.Attribute('loopNum')
					if txt:
						stateData.m_nloopNum = string.atoi(txt)
					layerElement = stateElement.FirstChildElement('layerInfo')
					while(layerElement):
						layerData = LayerData()
						txt = layerElement.Attribute('id')
						layerData.m_layerId = string.atoi(txt)
						layerData.m_layerName = layerElement.Attribute('name')
						txt = layerElement.Attribute('anchorX')
						if txt:
							layerData.m_anchorX = string.atof(txt)
						txt = layerElement.Attribute('anchorY')
						if txt:
							layerData.m_anchorY = string.atof(txt)
						txt = layerElement.Attribute("isParticle")
						if string.atoi(txt)= 1:
							layerData.m_bIsParticle = True
						else:
							layerData.m_bIsParticle = False
						layerData.m_particlePath = layerElement.Attribute('particlePath')
						txt = layerElement.Attribute('isBlendAddtive')
						if txt and string.atoi(txt) == 1:
							layerData.m_bIsParticle = True
						else:
							layerData.m_bIsParticle = False
						txt = layerElement.Attribute(isGhostNode)
						if txt and string.atoi(txt)==1:
							layerData.m_bIsGhostNode = True
						else:
							layerData.m_bIsGhostNode = False

						keyElement = layerElement.FirstChildElement('keyInfo')
						while(keyElement):
							keyData = AnimKeyData()

							txt = keyElement.Attribute('id')
							keyData.m_keyId = string.atoi(txt)
							txt = keyElement.Attribute('time')
							keyData.m_keyTime = string.atof(txt)
							txt = keyElement.Attribute('changePic')
							if string.atoi(txt) == 1:
								keyData.m_bIsChangePic = True
							else:
								keyData.m_bIsChangePic = False
							keyData.m_picFrameName = keyElement.Attribute('picFrameName')
							txt = keyElement.Attribute(changePos)
							if string.atoi(txt) ==1:
								keyData.m_bIsChangePos = True
							else:
								keyData.m_bIsChangePos = False
							txt = keyElement.Attribute('posX')
							keyData.m_posX = string.atof(txt)
							txt = keyElement.Attribute('posY')
							keyData.m_posY = string.atof(txt)
							txt = keyElement.Attribute("transPos")
							if string.atoi(txt) == 1:
								keyData.m_bIsTransPos = True
							else:
								keyData.m_bIsTransPos = False

							txt = keyElement.Attribute('changeScale')
							if string.atoi(txt):
								keyData.m_bIsChangeScale = True
							else:
								keyData.m_bIsChangeScale = False
							txt = keyElement.Attribute('scaleX')
							if txt:
								keyData.m_scaleX = atof(txt)
							txt keyElement.Attribute('salceY')
							if txt:
								keyData.m_scaleY = atof(txt)
							txt = keyElement.Attribute('transScale')
							if string.atoi(txt) == 1:
								keyData.m_bIsTransScale = True
							else:
								keyData.m_bIsTransScale = False

							txt = keyElement.Attribute('changeRotate')
							if txt:
								if string.atoi(txt) ==1:
									keyData.m_bIsChangeRotate = True
								else:
									keyData.m_bIsChangeRotate = False
							txt = keyElement.Attribute('angle')
							if txt:
								keyData.m_angle = string.atof(txt)
							txt = keyElement.Attribute('transRotate')
							if txt:
								if string.atoi(txt) == 1:
									keyData.m_bIsTransRotate = True
								else:
									keyData.m_bIsTransRotate = False

							txt = keyElement.Attribute('changeOpacity')
							if txt:
								if string.atoi(txt):
									keyData.m_bIsChangeOpacity = True
								else:
									keyData.m_bIsChangeOpacity = False
							txt = keyElement.Attribute('transOpacity')
							if txt:
								if string.atoi(txt) == 1:
									keyData.m_bIsTransOpacity = True
								else:
									keyData.m_bIsTransOpacity = False
							txt = keyElement.Attribute('opacity')
							if txt:
								keyData.m_opacity = string.atoi(txt)

							txt = keyElement.Attribute('isVisible')
							if string.atoi(txt) == 1:
								keyData.m_bIsVisible = True
							else:
								keyData.m_bIsVisible = False

							txt = keyElement.Attribute('isStartParticle')
							if string.atoi(txt)==1:
								keyData.m_bIsStartParticle = True
							else:
								keyData.m_bIsStartParticle = False
							txt = keyElement.Attribute('isStopParticle')
							if string.atoi(txt) == 1:
								keyData.m_bIsStopParticle = True
							else:
								keyData.m_bIsStopParticle = False

							layerData.m_keyDataList.append(keyData)
							keyElement = keyElement.NextSiblingElement('keyInfo')
						stateData.m_layerDataList.append(layerData)
						layerElement = layerElement.NextSiblingElement('layerInfo')

					LevelData.m_stateDataList.append(stateData)
					stateElement = stateElement.NextSiblingElement('stateInfo')
				self.m_levelDataList.append(levelData)
				levelElement = levelElement.NextSiblingElement("levelInfo")

	def _animKeySetTexNormal(self,targetSprite,picName):
		textureCache = cocos2dx.CTextureCache.GetInstance()
		keyTex = textureCache.AddImage(picName)
		if keyTex == None:
			print "load animation key picture failed"
			return
		texW,texH = keyTex.GetContentSize()
		frame = cocos2dx.CSpriteFrame(keyTex,0,0,texW,texW)
		if frame:
			targetSprite.SetSpriteFrame(frame)
			levelData = self.getLevelData(self.m_CurLevelId)
			if levelData == None:
				print "ERROR::there are no level%d existed"%self.m_curLevelId
				return None
			stateData =  levelData.getStateDate(self.m_curStateId)
			if stateData == None:
				print "ERROR::there are no state%d existed"%self.m_curStateId
				return None

			for layerData  in stateData.m_layerDataList:
				if targetSprite == layerData.m_sprite:
					if layerData.m_bIsBlendAdditive:
						layerData.m_sprite.SetBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)
					else:
						layerData.m_sprite.SetBlendFunc(layerData.m_origBlendScr,layerData.m_origBlendDst)
					break

	def _animKeySetTexFrame(self,targetSprite,picName):
		spriteFrameCache = cocos2dx.CSpriteFrameCache.GetInstance()
		frame  = spriteFrameCache.GetSpriteFrameByname(picName)
		if frame:
			targetSprite.SetSpriteFrame(frame)
			levelData = self.getLevelData(self.m_CurLevelId)
			if levelData == None:
				print "ERROR::there are no level%d existed"%self.m_curLevelId
				return None
			stateData =  levelData.getStateDate(self.m_curStateId)
			if stateData == None:
				print "ERROR::there are no state%d existed"%self.m_curStateId
				return None

			for layerData  in stateData.m_layerDataList:
				if targetSprite == layerData.m_sprite:
					if layerData.m_bIsBlendAdditive:
						layerData.m_sprite.SetBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)
					else:
						layerData.m_sprite.SetBlendFunc(layerData.m_origBlendScr,layerData.m_origBlendDst)
					break

	def _animKeySetPos(self,targetSprite,keyData):
		targetSprite.SetPos(keyData.m_posX,keyData.m_posY)

	def _animKeySetScale(self,targetSprite,keyData):
		targetSprite.SetScaleX(keyData.m_scaleX)
		targetSprite.SetScaleY(keyData.m_scaleY)

	def _animKeySetRotation(self,targetSprite,keyData):
		targetSprite.SetRotation(keyData.m_angle)

	def _animKeySetOpacity(self,targetSprite,keyData):
		targetSprite.SetOpacity(keyData.m_opacity)

	def _animKeySetVisible(self,targetSprite,keyData):
		targetSprite.SetVisible(keyData.m_bIsVisible)

	def _animKeyStartPaticle(self,particle):
		particle.ResetSystem()

	def _animKeyStopPaticle(self,particle):
		partilce.StopSystem()

	def _layerAnimEnd(self,target,stateData):
		pass


	def _loadBlockWithState(self,levelId,stateId):
		if self.m_filePath = None or len(self.m_filePath) == 0:
			print "filePath is Empty"
			return None
		self._loadAnimBlockWithFile(self.m_filePath)

		levelData = self.getLevelData(levelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%levelId
			return None
		stateData =  levelData.getStateDate(stateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%stateId
			return None

		self.m_node = self._loadWithNewNode()
		if self.m_bIsPlistRes:
			if self.m_bFuncAddPlist:
				spriteFrameCache = cocos2dx.CSpriteFrameCache.GetInstance()
				spriteFrameCache.AddSpriteFrameWithFile(self.m_plistPath)
				stateData.setupStateFrame(self.m_node)
		else:
			stateData.setupStateNormal(self.m_node)

		if not self.m_bReserverStates:
			slef._clearUnuseData(stateId)
		return self.m_node

	def setState(self,levelId,stateId):
		if self.m_node == None:
			print "ERROR::have Not loaded animblock yet,please load it frist"
			return

		levelData = self.getLevelData(levelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%levelId
			return None
		stateData =  levelData.getStateDate(self.m_curStateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%self.m_curStateId
			return None

		for layerData in stateData.m_layerDataList:
			if layerData.m_sprite:
				self.m_node.RemoveChild(layerData.m_sprite,True)
				layerData.m_sprite = None

		if not self.m_bReserverStates:
			self._loadAnimBlockWithFile(self.m_filePath)

		levelData = self.getLevelData(levelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%levelId
			return None
		stateData =  levelData.getStateDate(stateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%stateId
			return None

		if self.m_bIsPlistRes:
			stateData.setupStateFrame(self.m_node)
		else:
			stateData.setupStateNormal(self.m_node)
		self.m_curLevelId = levelId
		self.m_curStateId = stateId
		if not self.m_bReserverStates:
			self._clearUnuseData(stateId)
		return

	def stopBlockAnim(self,levelId,stateId):
		levelData = self.getLevelData(levelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%levelId
			return None
		stateData =  levelData.getStateDate(stateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%stateId
			return None
		for layerData in stateData.m_layerDataList:
			if layerData.m_sprite:
				if layerData.m_bisDebug:layerData.m_sprite.SetIsBebug(True)
			layerData.m_sprite.StopAllActions()
			if layerData.m_bIsParticle:
				layerData.m_sprite.StopSystem()

	def playBlockAnim(self,levelId,stateId):
		levelData = self.getLevelData(levelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%levelId
			return None
		stateData =  levelData.getStateDate(stateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%stateId
			return None

		for layerData in stateData.m_layerDataList:
			actionInstantList = []
			actionTransPosList = []
			actionTransScaleList = []
			actionsTransRotateList = []
			actionsTransOpacityList = []
			lastKeyData = None
			instantDuraAccu = 0.0
			transPosDuraAccu = 0.0
			transScaleDuraAccu = 0.0
			transRotateDuraAccu = 0.0
			transOpacityDuraAccu = 0.0
			lastInstantKeyTime = 0.0
			layerKeyNum = len(layerData.m_keyDataList)
			bLastIsVisible = True
			bRunAnim = False
			if layerKeyNum > 1:
				bRunAnim = True
			elif layerData.m_bIsParticle and layerData.m_keyDataList:
				targetKeydata = layerData.getKeyData(0)
				if targetKeydata and targetKeydata.m_bIsStartParticle:
					layerData.m_sprite.ResetSystem()
			for keyData in layerData.m_keyDataList:
				lastKeydura = 0.0
				tempInstantList = []
				if lastKeyData:
					#上一帧有关键帧，则添加延迟时间
					lastKeydura = keyData.m_keyTime = lastKeyData.m_keyTime
					＃积累间隔时间
					instantDuraAccu += lastKeydura
					transPosDuraAccu += lastKeydura
					transScaleDuraAccu += lastKeydura
					transRotateDuraAccu += lastKeydura
					transOpacityDuraAccu += lastKeydura
				if keyData.m_bIsChangePic:
					if layerData.m_sprite == None:
						print "layerData.m_sprite is None,you should load it correctly frist"
					elif not keyData.m_picFrameName:
						print "there are no texture name set,play anim failed"
					else:
						if self.m_bIsPlistRes:
							action = cocos2dx.CCallFunc(self._animKeySetTexFrame,layerData.m_sprite,keyData.m_picFrameName)
						else:
							action = cocos2dx.CCallFunc(self._animKeySetTexNormal,layerData.m_sprite,keyData.m_picFrameName)
						tempInstantList.append(action)

				if keyData.m_bIsChangePos:
					if keyData.m_bIsTransPos and lastKeyData:
						action = cocos2dx.CMoveTo(transPosDuraAccu,keyData.m_posX,keyData.m_posY)
						actionTransPosList.append(action)
					else:
						action = cocos2dx.CCallFunc(self._animKeySetPos,layerData.m_sprite,keyData)
						tempInstantList.append(action)

						action = =cocos2dx.CDelayTime(transPosDuraAccu)
						actionTransPosList.append(action)
					transPosDuraAccu = 0.0

				if keyData.m_bIsChangeScale:
					if keyData.m_bIsTransScale and lastKeyData:
						action = cocos2dx.CScale(transPosDuraAccu,keyData.m_sacleX,keyData.m_scaleY)
						actionTransScaleList.append(action)
					else:
						action = cocos2dx.CCallFunc(self._animKeySetScale,layerData.m_sprite,keyData)
						tempInstantList.append(action)

						action = =cocos2dx.CDelayTime(transScaleDuraAccu)
						actionTransScaleList.append(action)
					transScaleDuraAccu = 0.0

				if keyData.m_bIsChangeRotate:
					if keyData.m_bIsTransRotate and lastKeyData:
						action = cocos2dx.CRotationTo(transRotateDuraAccu,keyData.m_angle)
						actionsTransRotateList.append(action)
					else:
						action = cocos2dx.CCallFunc(self._animKeySetRotation,layerData.m_sprite,keyData)
						tempInstantList.append(action)

						action = cocos2dx.CDelayTime(transRotateDuraAccu)
					transRotateDuraAccu = 0.0

				if keyData.m_bIsChangeOpacity:
					if keydata.m_bIsTransOpacity and lastKeyData:
						action  = cocos2dx.FadeTo(transOpacityDuraAccu,keyData.m_opacity)
						tempInstantList.append(action)

						action = cocos2dx.CDelayTime(transOpacityDuraAccu)
						actionsTransOpacityList.append(action)
					transOpacityDuraAccu = 0.0

				if bLastisVisible ! = keyData.m_bIsVisible or lastKeyData == None:
					action = C_objct.CCallFunc(self._animKeySetVisible,layerData.m_sprite,keyData)
					tempInstantList.append(action)
				bLastIsVisible = keyData.m_bIsVisible

				if layerData.m_bIsParticle:
					if keyData.m_bIsStartParticle:
						action = cocos2dx.CCallFunc(self._animKeyStartPaticle,layerData.m_sprite)
						tempInstantList.append(action)
					elif keyData.m_bIsStopParticle:
						action = cocos2dx.CCallFunc(self._animKeyStopPaticle,layerData.m_sprite)
						tempInstantList.append(action)

				if lastKeyData and tempInstantList:#如果该帧有哦instant事件的话，就在动画列表前面加上delaytime
					action = cocos2dx.CDelayTime(instantDuraAccu)
					tempInstantList.insert(0,action)
					instantDuraAccu = 0.0

				#为列表添加该帧的instant动画
				if tempInstantList:
					actionInstantList.extend(tempInstantList)
					lastInstantKeyTime = keyData.m_keyTime

				lastKeyData = keyData#保存上一帧

			seqInstant = None
			seqTransPos = None
			seqTransScale = None
			seqTransRotate = None
			seqTransOpacity = None

			if bRunAnim:
				spawnList = []
				animLeftTime = =stateData.m_animDura - lastInstantKeyTime
				actionLeft = cocos2dx.CDelayTime(animLeftTime)#补全最后的时间
				actionEnd = cocos2dx.CCallFunc(self._layerAnimEnd,stateData)#动画终止要统计完结的动画
				actionInstantList.extend([actionLeft,actionEnd])
				seqInstant = cocos2dx.Csequence(actionInstantList)
				sqawnList.append(seqInstant)
			transPosNum = len(actionTransPosList)
			if transPosNum == 1:
				seqTransPos = actionTransPosList[0]
				spawnList.append(seqTransPos)
			elif transPosNum>1:
				seqTransPos = cocos2dx.Csequence(actionTransPosList)
				spawnList.append(seqTransPos)

			transScaleNum = len(actionTransScaleList)
			if transScaleNum == 1:
				seqTransScale = actionTransScaleList[0]
				spawnList.append(seqTransScale)
			elif transScaleNum>1:
				seqTransScale = cocos2dx.Csequence(actionTransScaleList)
				spawnList.append(seqTransScale)

			transRotateNum = len(actionTransRotateList)
			if transRotateNum == 1:
				seqTransRotate = actionTransRotateList[0]
				spawnList.append(seqTransRotate)
			elif transRotateNum>1:
				seqTransRotate = cocos2dx.Csequence(actionTransRotateList)
				spawnList.append(seqTransRotate)

			transOpacityNum = len(actionTransOpacityList)
			if transOpacityNum == 1:
				seqTransOpacity = actionTransOpacityList[0]
				spawnList.append(seqTransOpacity)
			elif transOpacityNum>1:
				seqTransOpacity = cocos2dx.Csequence(actionTransOpacityList)
				spawnList.append(seqTransOpacity)

			#通过CCSpawn的方式同时进行动画
			spawnlen = len(spawnList)
			spawnAll = None

			if spawnlen == 1:
				spawnAll = spawnList[0]
			elif spawnlen>1:
				spawnAll = cocos2dx.CSpawn(spawnList)
			if spawnAll !=None and layerData.m_sprite:
				if stateData.m_nLoopNum>0:
					spawnAll = cocos2dx.CRepeat(spawnAll,stateData.m_nLoopNum)
				elif stateData.m_bIsLoop:
					spawnAll = cocos2dx.CRepeatForever(spawnAll)
				layerData.m_sprite.StopAllActions()
				layerData.m_sprite.RunAction(spawnAll)

	def setIsFuncAddPlist(self,bFuncAddPlist):
		"设置是否由animblock来加载合图Plist"
		self.m_bFuncAddPlist = bFuncAddPlist

	def getGhostNode(self,layerId = -1):
		levelData = self.getLevelData(self.m_curLevelId)
		stateData = levelData.getStateDate(self.m_curStateId)
		if stateData == None:
			print "ERROR:getGhostNode is failed"
			return None

		for layerData in stateData.m_layerDataList:
			if layerData.m_bIsGhostNode:
				if layerId ==-1 and layerData.m_sprite:
					return layerData.m_sprite
			elif layerData.m_layerid = layerId:
				return layerData.m_sprite
		return None

	def getLevelData(self,levelId):
		for levelData in self.m_levelDataList:
			if levelData.m_levelId == levelId:
				return levelData

	def getSelectRange(self):
		levelData = self.getLevelData(self.m_curLevelId)
		return leveldata.m_selectOriginX,levelData.m_selectOriginY,levelData.m_selectRectW,levelData.m_selectRectH

	def getExtraInfoPos(self):
		levelData = self.getLevel(self.m_curLevelId)
		return levelData.m_infoTagX,levelData.m_infoTagY

	def clearAnimBlock(self):
		self._clearAnimBlock()


	#－－－－－－－－－－－－－－点击效果相关－－－－－－－－－－－－－－

	def runSpriteAction(self):
		levelData = self.getLevelData(self.m_CurLevelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%self.m_curLevelId
			return None
		stateData =  levelData.getStateDate(self.m_curStateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%self.m_curStateId
			return None
		index = 1
		for layerData  in stateData.m_layerDataList:
			if layerData.m_sprite:
				obj = layerData.m_sprite
				keyData0 = layerData.getKeyData(0)
				scaleX,scaleY = keyData0.m_scaleX,keyData0.m_scaleY
				act1 = cocos2dx.CScaleTo(0.1,scaleX*1.2,scaleY*1.3)
				act2 = cocos2dx.CScaleTo(0.1,scaleX,scaleY)
			if index == 1:
				resSetAction = cocos2dx.CCallFunc(self.afterSpring)
				seq = cocos2dx.Csequence.CreateWithTwoActions(cocos2dx.Csequence.Create.CreateWithTwoActions(act1,act2),resSetAction)

			else:
				seq = cocos2dx.Csequence.CreateWithTwoActions(act1,act2)
			index +=1
			obj.RunAction(seq)

	def afterSpring(self):
		pass

	def OnFrameInterVal(self,dt):
		'每帧刷新'
		if self.m_ActionForSelectedFlag !=None:
			self.SetColorForAction()

	def runShadow(self):
		self.stopShadow()
		self.m_ActionForSelectedFlag = -1


	def stopShadow(self):
		self.m_ActionForSelectedFlag = None
		levelData = self.getLevelData(self.m_CurLevelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%self.m_curLevelId
			return None
		stateData =  levelData.getStateDate(self.m_curStateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%self.m_curStateId
			return None

		for layerData  in stateData.m_layerDataList:
			if hasatter(layerData.m_sprite,'SetColor'):
				layerData.m_sprite.SetColor(255,255,255)

	def SetColorForAction(self):
		if self.m_ActionForSelectedFlag == None:
			return 
		levelData = self.getLevelData(self.m_CurLevelId)
		if levelData == None:
			print "ERROR::there are no level%d existed"%self.m_curLevelId
			return None
		stateData =  levelData.getStateDate(self.m_curStateId)
		if stateData == None:
			print "ERROR::there are no state%d existed"%self.m_curStateId
			return None

		for layerData  in stateData.m_layerDataList:
			curSpr = layerData.m_sprite
			if hasatter(curSpr,'SetColor'):
				r,g,b = curSpr.GetColor()
				if r >=255:
					self.m_ActionForSelectedFlag = -1
				elif r<=180:
					self.m_ActionForSelectedFlag = 1
				delColor = 3*self.m_ActionForSelectedFlag
				newR,newG,newB = r+delColor,g+delColor,b+delColor
				newR = 255 if newR > 255 else newR
				newG = 255 if newG > 255 else newG
				newB = 255 if newB > 255 else newB

				newR = 180 if newR < 180 else newR
				newG = 180 if newG < 180 else newG
				newB = 180 if newB < 180 else newB
				curSpr.SetColor(newR,newG,newB)








































