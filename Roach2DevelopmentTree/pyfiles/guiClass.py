import re
import math
import xml.dom.minidom


#execfile('parse.py')
#gretBoard.template-->dgsDigBoard.template
#gretCrystal.template-->dgsCrystal.template



opi_MenuButton = """
  <widget typeId="org.csstudio.opibuilder.widgets.MenuButton" version="1.0">
    <border_alarm_sensitive>false</border_alarm_sensitive>
    <visible>true</visible>
    <actions_from_pv>false</actions_from_pv>
    <wuid>6c71af6e:1396dc2108d:-37de</wuid>
    <scripts />
    <height>_HEIGHT_</height>
    <forecolor_alarm_sensitive>true</forecolor_alarm_sensitive>
    <name>Menu Button_14</name>
    <transparent>false</transparent>
    <pv_name />
    <background_color>
      <color red="255" green="219" blue="160" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="255" />
    </foreground_color>
    <widget_type>Menu Button</widget_type>
    <enabled>true</enabled>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <font>
      <fontdata fontName="Segoe UI" height="16" style="0" />
    </font>
    <width>_WIDTH_</width>
    <border_style>6</border_style>
    <label>_TEXT_</label>
    <rules />
    <pv_value />
    <border_width>1</border_width>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <y>_YYY_</y>
    <actions hook="false" hook_all="false">
    </actions>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>

"""


opi_MenuAction="""
      <action type="OPEN_DISPLAY">
        <path></path>
        <macros>
          <include_parent_macros>true</include_parent_macros>
        </macros>
        <replace>0</replace> 
	<description></description>
      </action>
"""

opi_Macro="""<_MACNAME_>_MACVAL_</_MACNAME_>
"""

opi_bigled="""  <widget typeId="org.csstudio.opibuilder.widgets.LED" version="1.0">
    <border_alarm_sensitive>true</border_alarm_sensitive>
    <visible>true</visible>
    <wuid>6c71af6e:1396dc2108d:-44b4</wuid>
    <scripts />
    <square_led>false</square_led>
    <on_color>
      <color red="0" green="255" blue="0" />
    </on_color>
    <height>_HEIGHT_</height>
    <data_type>0</data_type>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>LED</name>
    <show_boolean_label>false</show_boolean_label>
    <off_color>
      <color red="0" green="100" blue="0" />
    </off_color>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="240" green="240" blue="240" />
    </background_color>
    <foreground_color>
      <color red="192" green="192" blue="192" />
    </foreground_color>
    <off_label>OFF</off_label>
    <widget_type>LED</widget_type>
    <enabled>true</enabled>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <effect_3d>true</effect_3d>
    <rules />
    <pv_value />
    <bit>-1</bit>
    <border_width>1</border_width>
    <on_label>ON</on_label>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <actions hook="false" hook_all="false" />
    <y>_YYY_</y>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>__XXX_</x>
  </widget>
"""


opi_screen = """<?xml version="1.0" encoding="UTF-8"?>
<display typeId="org.csstudio.opibuilder.Display" version="1.0">
  <auto_zoom_to_fit_all>false</auto_zoom_to_fit_all>
  <macros>
    <include_parent_macros>true</include_parent_macros>
  </macros>
  <wuid>788bce97:137bd978550:-7ff9</wuid>
  <boy_version>3.1.0.20120201</boy_version>
  <scripts />
  <show_ruler>true</show_ruler>
  <height>600</height>
  <name />
  <snap_to_geometry>true</snap_to_geometry>
  <show_grid>true</show_grid>
  <background_color>
    <color red="240" green="240" blue="240" />
  </background_color>
  <foreground_color>
    <color red="192" green="192" blue="192" />
  </foreground_color>
  <widget_type>Display</widget_type>
  <show_close_button>true</show_close_button>
  <width>800</width>
  <rules />
  <show_edit_range>true</show_edit_range>
  <grid_space>6</grid_space>
  <actions hook="false" hook_all="false" />
  <y>-1</y>
  <x>-1</x>
  </display>
"""


opi_label="""  <widget typeId="org.csstudio.opibuilder.widgets.Label" version="1.0">
    <visible>true</visible>
    <vertical_alignment>1</vertical_alignment>
    <wuid>788bce97:137bd978550:-7fa0</wuid>
    <auto_size>false</auto_size>
    <scripts />
    <height>_HEIGHT_</height>
    <name>Label_54</name>
    <transparent>false</transparent>
    <show_scrollbar>false</show_scrollbar>
    <background_color>
      <color red="240" green="240" blue="240" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="0" />
    </foreground_color>
    <widget_type>Label</widget_type>
    <enabled>true</enabled>
    <text>_TEXT_</text>
    <font>
      <fontdata fontName="Ubuntu" height="13" style="0" />
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <rules />
    <border_width>1</border_width>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <horizontal_alignment>2</horizontal_alignment>
    <actions hook="false" hook_all="false" />
    <y>_YYY_</y>
    <wrap_words>true</wrap_words>
    <tooltip />
    <x>_XXX_</x>
  </widget>
"""


opi_textinput="""  <widget typeId="org.csstudio.opibuilder.widgets.TextInput" version="1.0">
    <border_alarm_sensitive>false</border_alarm_sensitive>
    <visible>true</visible>
    <minimum>-1.7976931348623157E308</minimum>
    <vertical_alignment>1</vertical_alignment>
    <show_units>true</show_units>
    <multiline_input>false</multiline_input>
    <wuid>788bce97:137bd978550:-7f9f</wuid>
    <auto_size>false</auto_size>
    <rotation_angle>0.0</rotation_angle>
    <scripts />
    <height>_HEIGHT_</height>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>Text Input_1</name>
    <format_type>0</format_type>
    <precision_from_pv>true</precision_from_pv>
    <transparent>false</transparent>
    <selector_type>0</selector_type>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="255" green="255" blue="255" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="0" />
    </foreground_color>
    <widget_type>Text Input</widget_type>
    <enabled>true</enabled>
    <text />
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <precision>0</precision>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>3</border_style>
    <rules />
    <pv_value />
    <border_width>1</border_width>
    <maximum>1.7976931348623157E308</maximum>
    <limits_from_pv>false</limits_from_pv>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <horizontal_alignment>0</horizontal_alignment>
    <actions hook="false" hook_all="false" />
    <y>_YYY_</y>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""

opi_combo="""  <widget typeId="org.csstudio.opibuilder.widgets.combo" version="1.0">
    <border_alarm_sensitive>true</border_alarm_sensitive>
    <visible>true</visible>
    <wuid>788bce97:137bd978550:-7f72</wuid>
    <scripts />
    <height>_HEIGHT_</height>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>Combo Box</name>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="255" green="255" blue="255" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="0" />
    </foreground_color>
    <widget_type>Combo Box</widget_type>
    <enabled>true</enabled>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <rules />
    <pv_value />
    <border_width>1</border_width>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <items_from_pv>true</items_from_pv>
    <actions hook="false" hook_all="false">
      <action type="WRITE_PV">
        <pv_name>$(pv_name)</pv_name>
        <value />
        <timeout>10</timeout>
        <description />
      </action>
    </actions>
    <y>_YYY_</y>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""


opi_textupdate="""  <widget typeId="org.csstudio.opibuilder.widgets.TextUpdate" version="1.0">
    <border_alarm_sensitive>true</border_alarm_sensitive>
    <visible>true</visible>
    <vertical_alignment>1</vertical_alignment>
    <show_units>true</show_units>
    <wuid>788bce97:137bd978550:-7f15</wuid>
    <auto_size>false</auto_size>
    <rotation_angle>0.0</rotation_angle>
    <scripts />
    <height>_HEIGHT_</height>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>Text Update</name>
    <format_type>0</format_type>
    <precision_from_pv>true</precision_from_pv>
    <transparent>false</transparent>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="255" green="255" blue="255" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="0" />
    </foreground_color>
    <widget_type>Text Update</widget_type>
    <enabled>true</enabled>
    <text>######</text>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <precision>0</precision>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <rules />
    <pv_value />
    <border_width>1</border_width>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <horizontal_alignment>0</horizontal_alignment>
    <actions hook="false" hook_all="false" />
    <y>_YYY_</y>
    <wrap_words>false</wrap_words>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""


opi_boolbutton="""  <widget typeId="org.csstudio.opibuilder.widgets.BoolButton" version="1.0">
    <border_alarm_sensitive>true</border_alarm_sensitive>
    <visible>true</visible>
    <wuid>788bce97:137bd978550:-7ebe</wuid>
    <password />
    <scripts />
    <on_color>
      <color red="0" green="255" blue="0" />
    </on_color>
    <height>_HEIGHT_</height>
    <show_led>false</show_led>
    <data_type>0</data_type>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>Boolean Button</name>
    <show_boolean_label>false</show_boolean_label>
    <off_color>
      <color red="0" green="100" blue="0" />
    </off_color>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="240" green="240" blue="240" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="0" />
    </foreground_color>
    <off_label>OFF</off_label>
    <released_action_index>0</released_action_index>
    <widget_type>Boolean Button</widget_type>
    <enabled>true</enabled>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <push_action_index>0</push_action_index>
    <confirm_message>Are your sure you want to do this?</confirm_message>
    <effect_3d>true</effect_3d>
    <rules />
    <pv_value />
    <bit>-1</bit>
    <toggle_button>true</toggle_button>
    <show_confirm_dialog>0</show_confirm_dialog>
    <border_width>1</border_width>
    <on_label>ON</on_label>
    <square_button>true</square_button>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <y>_YYY_</y>
    <actions hook="false" hook_all="false" />
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""






opi_bytemonitor= """ <widget typeId="org.csstudio.opibuilder.widgets.bytemonitor" version="1.0">
    <border_alarm_sensitive>true</border_alarm_sensitive>
    <visible>true</visible>
    <wuid>106c5c4b:1372c975c6b:-7f6b</wuid>
    <bitReverse>false</bitReverse>
    <scripts />
    <square_led>false</square_led>
    <startBit>0</startBit>
    <on_color>
      <color red="0" green="255" blue="0" />
    </on_color>
    <height>_HEIGHT_</height>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>Byte Monitor</name>
    <off_color>
      <color red="0" green="100" blue="0" />
    </off_color>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="240" green="240" blue="240" />
    </background_color>
    <foreground_color>
      <color red="192" green="192" blue="192" />
    </foreground_color>
    <widget_type>Byte Monitor</widget_type>
    <enabled>true</enabled>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <numBits>16</numBits>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <effect_3d>true</effect_3d>
    <rules />
    <pv_value />
    <border_width>1</border_width>
    <horizontal>false</horizontal>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <actions hook="false" hook_all="false" />
    <y>_YYY_</y>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""




opi_actionbutton="""  <widget typeId="org.csstudio.opibuilder.widgets.ActionButton" version="1.0">
    <border_alarm_sensitive>false</border_alarm_sensitive>
    <visible>true</visible>
    <wuid>-35ffa04c:1372e49cdd1:-7ca5</wuid>
    <scripts />
    <height>_HEIGHT_</height>
    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>
    <name>Action Button</name>
    <pv_name>_PVNAME_</pv_name>
    <background_color>
      <color red="255" green="0" blue="0" />
    </background_color>
    <foreground_color>
      <color red="0" green="0" blue="0" />
    </foreground_color>
    <widget_type>Action Button</widget_type>
    <enabled>true</enabled>
    <text>_TEXT_</text>
    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>
    <font>
      <opifont.name>Default</opifont.name>
    </font>
    <width>_WIDTH_</width>
    <border_style>0</border_style>
    <push_action_index>0</push_action_index>
    <image />
    <rules />
    <pv_value />
    <toggle_button>false</toggle_button>
    <border_width>1</border_width>
    <border_color>
      <color red="0" green="128" blue="255" />
    </border_color>
    <y>_YYY_</y>
    <actions hook="false" hook_all="false">
    </actions>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""



opi_setPvAction="""
      <action type="WRITE_PV">
        <pv_name></pv_name>
        <value></value>
        <timeout>10</timeout>
        <description />
      </action>
"""



class cssScreen:
	
	def __init__(self):
		self.name=""
		
		self.dom=xml.dom.minidom.parseString(opi_screen)
		
		
	def addWidget(self,w):
		xmlstr=w.getXML()
		wdom=xml.dom.minidom.parseString(xmlstr)
		w=wdom.getElementsByTagName('widget')[0]
		
		disp=self.dom.getElementsByTagName('display')[0]
		disp.appendChild(w)
		
		
		
	def listWidgets(self):
		disp=self.dom.getElementsByTagName('display')[0]
		wl=disp.getElementsByTagName('widget')
		
		for w in wl:
			c=cssWidget()
			c.setXML(w.toxml())
			c.listFields()
			
	
		
	def findWidgets(self,keyvalue):
		disp=self.dom.getElementsByTagName('display')[0]
		wl=disp.getElementsByTagName('widget')
		
		key=keyvalue[0]
		value=keyvalue[1]
		
		wlist=[]
		for w in wl:
			c=cssWidget()
			c.setXML(w.toxml())
			
			if key=='type':
				if c.getType()==value:
			
					c.listFields()
					wlist.append(c);
			else:
				if c.getField()==value:
			
					c.listFields()
					wlist.append(c);
		return(wlist);
			
	
	def getWidgets(self):
		disp=self.dom.getElementsByTagName('display')[0]
		wl=disp.getElementsByTagName('widget')
		
		wlist=[]
		for w in wl:
			c=cssWidget()
			c.setXML(w.toxml())
			wlist.append(c)
			
		return(wlist)
			
		
		
	def getXML(self):
		
		return(self.dom.toxml())
	
	def setXML(self,xmlstr):
		self.dom=xml.dom.minidom.parseString(xmlstr)
		

	def readXML(self,xmlfile):
		self.dom=xml.dom.minidom.parse(xmlfile)

	def writeXML(self,filename):
		f=open(filename,'w')
		f.write(self.getXML())
		f.close()

		

"""

execfile('guiClass.py')
c=cssWidget()
c.setType('boolbutton')
c.setField('x','100')
c.setField('y','200')
c.setField('width','20')
c.setField('height','20')
c.setField('pv_name','maddog')

c.listFields()



d=cssWidget()
d.setType('combo')
d.setField('x','1000')
d.setField('y','2000')
d.setField('width','200')
d.setField('height','20')
d.setField('pv_name','birddy')

d.listFields()



s=cssScreen()
s.addWidget(c)
s.addWidget(d)
s.listWidgets()


c.setField('AAA','timmadden')
print c.getXML(




"""

class cssWidget:


	
	def __init__(self):
		
		#boolbutton, actionbutton, dispbutton, label, textupdate, textinput, combo
		#bytemonitor, led
		self.type = "NULL"
		
		
		#x,y,text,width, height, pv_name, pvval, display
		#self.fieldlist=dict()
		#when we set displayname we actually create a dict as the entry
		#this disct has macros defined as 'macros': [P:'??', 'R':'dfdf']
		#also we have desc:"fjfjdkfl"
		#
		
		#xml dicument
		dom=None
	
	def setType(self,t):
		self.type=t
		
		if self.type=='boolbutton':
			xmlstr=opi_boolbutton;
		
		elif self.type == 'actionbutton':
			xmlstr=opi_actionbutton;
		
		elif self.type == 'dispbutton':
			xmlstr=opi_MenuButton;
		
		elif self.type == 'label':
			xmlstr=opi_label;
		
		elif self.type == 'textupdate':
			xmlstr=opi_textupdate;
		
		elif self.type == 'textinput':
			xmlstr=opi_textinput;
		
		elif self.type == 'combo':
			xmlstr=opi_combo;
		
		elif self.type == 'bytemonitor':
			xmlstr=opi_bytemonitor;
		
		elif self.type == 'led':
			xmlstr=opi_bigled;
		
		else:
			print "invalid widget type"
			return(None)
		
		
		self.dom=xml.dom.minidom.parseString(xmlstr)
		
		#self.setField('mad_type',t)
		

		
	def getType(self):
		return(self.type);
		
		
	def getXML(self):
		w=self.dom.getElementsByTagName('widget')[0]
		return(self.dom.toxml())
	
	#parses xml str	
	def setXML(self,xmlstr):
		self.dom=xml.dom.minidom.parseString(xmlstr)
		
		t=self.getField('widget_type')
		if (t=='LED'):
			self.type ='led'
		elif (t=='Boolean Button'):
			self.type ='boolbutton'
		elif (t=='Action Button'):
			self.type ='actionbutton'
		elif (t=='Menu Button'):
			self.type ='dispbutton'
		elif (t=='Label'):
			self.type ='label'
		elif (t=='Text Update'):
			self.type ='textupdate'
		elif (t=='Text Input'):
			self.type ='textinput'
		elif (t=='Combo Box'):
			self.type ='combo'
		elif (t=='Byte Monitor'):
			self.type ='bytemonitor'
		
		else:
			self.type =t;
		
		
		#self.type =self.getField('mad_type')
		
		
	def listFields(self):
		print "--------------"
		print "Type :  " + self.getType()
		print "PVName:    " + self.getField('pv_name')
		print "x:    " + self.getField('x')
		print "y:    " + self.getField('y')
		
			
	
		
	def setField(self,fname,fdata):	
		w=self.dom.getElementsByTagName('widget')[0]
		tl=w.getElementsByTagName(fname)
		
		if (len(tl)>0):
			t=tl[0]
		else:	
			print "new element"
			t=self.dom.createElement(fname)
			tnode=self.dom.createTextNode("_NULL_")
			t.appendChild(tnode)

			w.appendChild(t)



		tnode=t.firstChild
		newtnode=self.dom.createTextNode(fdata)
		t.replaceChild(newtnode,tnode)		


	def getField(self,fname):
		w=self.dom.getElementsByTagName('widget')[0]
		tl=w.getElementsByTagName(fname)
		
		if (len(tl)>0):
			t=tl[0]
		else:	
			print "Invalid field"
			return('')
			



		tnode=t.firstChild
		if tnode:
			if (tnode.nodeType==tnode.TEXT_NODE):
				return(tnode.nodeValue)
		
		return('');	
		


#
#opi_MenuAction="""
#      <action type="OPEN_DISPLAY">
#        <path></path>
#        <macros>
#          <include_parent_macros>true</include_parent_macros>
#        </macros>
#        <replace>0</replace>
#        <description>_DESCRIPTION_</description>
#      </action>
#"""

	def addDisp(self,dname,desc,macrodict):
		w=self.dom.getElementsByTagName('widget')[0]
		tl=w.getElementsByTagName("actions")
		
		if (len(tl)>0):
			actions=tl[0]
		else:	
			print "new element"
			actions=self.dom.createElement("actions")
			

			w.appendChild(actions)

		newactiond=xml.dom.minidom.parseString(opi_MenuAction)
		newaction=newactiond.getElementsByTagName('action')[0]

		path=newaction.getElementsByTagName('path')[0]
		path.appendChild(newactiond.createTextNode(dname))
	
		discription=newaction.getElementsByTagName('description')[0]
		discription.appendChild(newactiond.createTextNode(desc))
	
		macros=newaction.getElementsByTagName('macros')[0]
		
		for m in macrodict:
			newmac=newactiond.createElement(m)
			newmac.appendChild(newactiond.createTextNode(macrodict[m]))
			
			macros.appendChild(newmac)
			
		actions.appendChild(newaction)
		
		

	def setFont(self,fname,fsize):
		w=self.dom.getElementsByTagName('widget')[0]
		f=w.getElementsByTagName("font")[0]
		fd=f.getElementsByTagName("fontdata")[0]
		
		fd.setAttribute('fontName',fname)
		fd.setAttribute('height',fsize)
		


#"""
#  
#      <action type="WRITE_PV">
#        <pv_name></pv_name>
#        <value></value>
#        <timeout>10</timeout>
#        <description />
#      </action>
#    </actions>
#"""	
	
	def addPvAction(self,pname,sval):
		w=self.dom.getElementsByTagName('widget')[0]
		tl=w.getElementsByTagName("actions")
		
		if (len(tl)>0):
			actions=tl[0]
		else:	
			print "new element"
			actions=self.dom.createElement("actions")
			

			w.appendChild(actions)

		newactiond=xml.dom.minidom.parseString(opi_setPvAction)
		newaction=newactiond.getElementsByTagName('action')[0]

		pv_name=newaction.getElementsByTagName('pv_name')[0]
		pv_name.appendChild(newactiond.createTextNode(pname))
	
		value=newaction.getElementsByTagName('value')[0]
		value.appendChild(newactiond.createTextNode(sval))
	
		
			
		actions.appendChild(newaction)
		
			
