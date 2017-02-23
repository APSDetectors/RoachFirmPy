import re
import math
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
    _ACTION_LIST_
    </actions>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>

"""


opi_MenuAction="""
      <action type="OPEN_DISPLAY">
        <path>_DISPLAYNAME_</path>
        <macros>
          <include_parent_macros>true</include_parent_macros>
          _MACROLIST_
        </macros>
        <replace>0</replace>
        <description>_DESCRIPTION_</description>
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


opi_start = """<?xml version="1.0" encoding="UTF-8"?>
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
"""

opi_end="""
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
    <pv_name />
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
      <action type="WRITE_PV">
        <pv_name>_PVNAME_</pv_name>
        <value>_PVVALUE_</value>
        <timeout>10</timeout>
        <description />
      </action>
    </actions>
    <tooltip>$(pv_name)
$(pv_value)</tooltip>
    <x>_XXX_</x>
  </widget>
"""





def epics2opi(filein, fileout, s_dtype,excludetype, excludename, is_make_rbv) :
	f = open(filein)
	f2=open(fileout,"w+")
	f3=open("opilogfile.txt","w+")
	f2.write(opi_start);

	try:
		x=50;
		y=50;
		height_s=20
		width_s=300
		
		for line in f:
			record=re.search('(?<=record).*',line)
			dtyp=re.search('(?<=field\(DTYP).*',line)
			endrec=re.search('}',line);
			
			
			
			if endrec!=None:
					
				if excludetype in rectype.group(0) :
					is_found=None;

				if excludename in pvname.group(0) :
					is_found=None;

				#write label with pv name
				if is_found!=None:
					widget = opi_label;
					widget = widget.replace('_TEXT_',pvname.group(0))
					widget = widget.replace('_XXX_','%d'%(x))
					widget = widget.replace('_YYY_','%d'%(y))
					widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
					widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

					f2.write(widget);
					f3.write('wrote opi Label at %d, %d\n' %(x,y));

					if 'ao'in rectype.group(0):
						widget = opi_textinput;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_YYY_','%d'%(y))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Textinput at %d, %d\n' %(x,y));

					elif 'ai'in rectype.group(0):
						widget = opi_textupdate;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_YYY_','%d'%(y))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi TextUpdate at %d, %d\n' %(x,y));

					elif 'longout'in rectype.group(0):
						widget = opi_textinput;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_YYY_','%d'%(y))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Textinput at %d, %d\n' %(x,y));

						if (is_make_rbv==1):
							rbvname = pvname.group(0) + '_RBV'
							widget = opi_textupdate;
							widget = widget.replace('_PVNAME_',rbvname)
							widget = widget.replace('_XXX_','%d'%(x+410))
							widget = widget.replace('_YYY_','%d'%(y))
							widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
							widget = widget.replace('_WIDTH_','%d'%(int(width_s)))


							f2.write(widget);
							f3.write('wrote opi TextUpdate at %d, %d\n' %(x,y));


					elif 'longin'in rectype.group(0):
						widget = opi_textupdate;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_YYY_','%d'%(y))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi TextUpdate at %d, %d\n' %(x,y));



					elif 'waveform'in rectype.group(0):
						widget = opi_textupdate;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_YYY_','%d'%(y))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi TextUpdate at %d, %d\n' %(x,y));


					elif 'mbbi'in rectype.group(0):
						widget = opi_textupdate;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(y))

						f2.write(widget);
						f3.write('wrote opi TextUpdate at %d, %d\n' %(x,y));

					elif 'mbbo'in rectype.group(0):
						widget = opi_combo;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(y))

						f2.write(widget);
						f3.write('wrote opi Combo at %d, %d\n' %(x,y));
					elif 'bi'in rectype.group(0):
						widget = opi_textupdate;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(y))

						f2.write(widget);
						f3.write('wrote opi TextUpdate at %d, %d\n' %(x,y));


					elif 'bo'in rectype.group(0):
						widget = opi_boolbutton;
						widget = widget.replace('_PVNAME_',pvname.group(0))
						widget = widget.replace('_XXX_','%d'%(x+205))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(y))

						f2.write(widget);
						f3.write('wrote opi Boolean Button at %d, %d\n' %(x,y));


				
					y=y+30;
					if y>550 :
						x=x+145+3*width
						y=30; 
						if (is_make_rbv):
							x=x+width+10
				
				
				
			elif record!=None:
				
				is_found = None;
				if s_dtype=='all':
					is_found='true'
			
				rectype=re.search('(?<=\()\w*',record.group(0))
				pvname=re.search('(?<=\")[$()\w]*',record.group(0))
				
			
				if pvname==None :
					pvname=re.search('(?<=, )[\w]*',record.group(0))

				
				if pvname!= None and rectype!=None :
					f3.write( '\n\n**************************************\n')
					f3.write( 'PV= %s  Type= %s\n' % (pvname.group(0),rectype.group(0)))
					print 'PV= %s  Type= %s\n' % (pvname.group(0),rectype.group(0))
				else:
					f3.write( '\n\n**************************************\n')
					f3.write( "NO PV or TYPE\n") 
					print "NO PV or TYPE\n"
					is_found = None;
			elif dtyp!=None :
				f3.write('found dtype %s\n' %line);
				is_found=re.search(s_dtype,dtyp.group(0));
				if is_found!=None:
					f3.write("Found %s\n"%(s_dtype))
					
					
			
	finally:
		f3.write("\n\n-------------END PARSE---------------\n")
		f.close()
		f2.write(opi_end);
		f2.close()
    







	


def edm2opi(filein, fileout) :
	f = open(filein)
	f2=open(fileout,"w+")
	f3=open("opilogfile.txt","w+")
	f2.write(opi_start);

	try:
		x=50;
		y=50;
		in_value = 0
		in_symbols=0
		in_menuLabel=0
		in_displayName=0
		
		text_string = ' '
		
		for line in f:
			object=re.search('(?<=^object\s).*',line)
			xpos=re.search('(?<=^x\s).*',line)
			ypos=re.search('(?<=^y\s).*',line)
			endrec=re.search('endObjectProperties',line);

			height=re.search('(?<=^h\s).*',line)
			width=re.search('(?<=^w\s).*',line)

			buttonLabel=re.search('(?<=^buttonLabel\s")[\s\w./_$()=,]*',line)
			
			pressvalue=re.search('(?<=^pressValue\s).*',line)
			pvname=re.search('(?<=^controlPv\s).*',line)
			isValue = re.search('(?<=^value\s).*',line)
			endValue = re.search('^}',line)
			
			displayName=re.search('^displayFileName',line);
			menuLabel=re.search('^menuLabel',line);
			symbols=re.search('^symbols',line);
			
			if in_value==1:
				text_string= re.search('(?<=")[\s\w./_$()=,]*',line).group(0)
				in_value = 0;
				f3.write( 'Value = %s\n'%(text_string))
			



			if endrec!=None:

			

				#write label with pv name
				if is_found!=None:
					



					if 'relatedDisplayClass'in rectype:
						widget = opi_MenuButton;
						widget = widget.replace('_TEXT_',buttonLabel_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
	

						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))


						#Add in the actions and replace the Action List
						actionlist = ""
						for index in range(len(displayName_list)):
							action=opi_MenuAction;
							displayName_list[index]=displayName_list[index].replace('.edl','.opi')
							action = action.replace('_DISPLAYNAME_',displayName_list[index])
							action = action.replace('_DESCRIPTION_',menuLabel_list[index])
							
							f3.write("Create Action %s %s\n"%(displayName_list[index],menuLabel_list[index]))
							
							#HERE WE FOR OVER THE MACROS
							macrolist = ""
							macro_l=symbols_list[index].split(',')
							f3.write("N synbols %d \n"%(len(macro_l)))
							for mindex in range(len(macro_l)):
								name_val=macro_l[mindex].split('=')
								f3.write("Macro %s %s\n"%(name_val[0],name_val[1]))
								macxml=opi_Macro;
								macxml=macxml.replace('_MACNAME_',name_val[0]);
								macxml = macxml.replace('_MACVAL_',name_val[1]);
								macrolist+=macxml
								
								
							
							f3.write(macrolist);
							action = action.replace('_MACROLIST_',macrolist);
							
							actionlist += action
							actionlist +='\n'
						
						widget = widget.replace('_ACTION_LIST_',actionlist)	
							
						f2.write(widget);
						f3.write('wrote opi Related Disp at %d, %d\n' %(int(xpos_s),int(ypos_s)));



					if 'activeXTextClass'in rectype:
						widget = opi_label;
						widget = widget.replace('_TEXT_',text_string)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
	

						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Label at %d, %d\n' %(int(xpos_s),int(ypos_s)));



					elif 'activeCircleClass'in rectype:
						widget = opi_bigled
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))

						f2.write(widget);
						f3.write('wrote opi big led at %d, %d\n' %(int(xpos_s),int(ypos_s)));


					elif 'activeXTextDspClass:noedit'in rectype:
						widget = opi_textupdate;
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))

						f2.write(widget);
						f3.write('wrote opi TextUpdate at %d, %d\n' %(int(xpos_s),int(ypos_s)));



					elif 'activeXTextDspClass'in rectype:
						widget = opi_textinput;
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))

						f2.write(widget);
						f3.write('wrote opi Textinput at %d, %d\n' %(int(xpos_s),int(ypos_s)));

					elif 'TextupdateClass'in rectype:
						widget = opi_textinput;
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))

						f2.write(widget);
						f3.write('wrote opi Textinput at %d, %d\n' %(int(xpos_s),int(ypos_s)));

					

					elif 'ByteClass'in rectype:
						widget = opi_bytemonitor
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Byte Monitor at %d, %d\n' %(int(xpos_s),int(ypos_s)));





					elif 'activeMenuButtonClass'in rectype:
						widget = opi_combo;
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Combo Box at %d, %d\n' %(int(xpos_s),int(ypos_s)));
	
					elif 'activeChoiceButtonClass'in rectype:
						widget = opi_combo;
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Combo Box at %d, %d\n' %(int(xpos_s),int(ypos_s)));

					elif 'activeButtonClass'in rectype:
						widget = opi_boolbutton;
						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Boolean Button at %d, %d\n' %(int(xpos_s),int(ypos_s)));


					elif 'activeMessageButtonClass'in rectype:
						widget = opi_actionbutton
						widget = widget.replace('_TEXT_'," ")

						widget = widget.replace('_PVNAME_',pvname_s)
						widget = widget.replace('_PVVALUE_',pressvalue_s)
						widget = widget.replace('_XXX_','%d'%(int(xpos_s)))
						widget = widget.replace('_YYY_','%d'%(int(ypos_s)))
						widget = widget.replace('_HEIGHT_','%d'%(int(height_s)))
						widget = widget.replace('_WIDTH_','%d'%(int(width_s)))

						f2.write(widget);
						f3.write('wrote opi Action Button at %d, %d\n' %(int(xpos_s),int(ypos_s)));

				
				
				
				
				
			elif object!=None:
				
				is_found = 'true'
				xpos=None
				ypos=None
				endrec=None
				pvname = None
				height = None
				width = None
				pressvalue=None
				isValue = None
				endBrace = None
				buttonLabel=None
				rectype=object.group(0)
				in_value=0
				text_string = ' '
				
				displayName=None
				menuLabel=None
				symbols=None
		
				in_symbols=0
				in_menuLabel=0
				in_displayName=0
				
				symbols_list = list();
				menuLabel_list = list();
				displayName_list = list();


				f3.write( '\n\n**************************************\n')
				f3.write( 'rec Type= %s  \n' % (rectype))
				
			
			elif isValue !=None:
				in_value = 1
				f3.write( 'Found a Value\n')
				
				

			elif displayName !=None:
				in_displayName = 1
				f3.write( 'Found displayName\n')
				
			elif menuLabel !=None:
				in_menuLabel = 1
				f3.write( 'Found a menuLabel\n')
			
			elif symbols !=None:
				in_symbols = 1
				f3.write( 'Found a symbols\n')


			elif endValue !=None:
				in_value = 0
				in_symbols=0
				in_menuLabel=0
				in_displayName=0
				f3.write( 'End Value\n')
				
				
			elif pvname!=None:
						
				pvname_s=re.search('(?<=")[\s\w$():._]*',pvname.group(0)).group(0)

				f3.write( 'pvname= %s  \n' % (pvname_s))

			elif pressvalue!=None:
						
				pressvalue_s=re.search('(?<=")[\s\w$():._]*',pressvalue.group(0)).group(0)

				f3.write( 'pressvalue= %s  \n' % (pressvalue_s))

			

			elif width!=None:
						
				width_s=width.group(0)

				f3.write( 'width= %s \n ' % (width_s))


			elif height!=None:
						
				height_s=height.group(0)

				f3.write( 'height= %s \n ' % (height_s))

					
			elif xpos!=None:
						
				xpos_s=xpos.group(0)

				f3.write( 'xpos= %s \n ' % (xpos_s))
				
			elif ypos!=None:
						
				ypos_s=ypos.group(0)

				f3.write( 'ypos= %s  \n' % (ypos_s))
				

			elif buttonLabel!=None:
						
				buttonLabel_s=buttonLabel.group(0)

				f3.write( 'buttonLabel= %s  \n' % (buttonLabel_s))
				
				
				
				
				
			elif in_symbols==1:
				text_string= re.search('(?<=")[\s\w./_$()=,]*',line).group(0)
				symbols_list.append(text_string);
				f3.write( 'symbol = %s\n'%(text_string))

			elif in_menuLabel==1:
				text_string= re.search('(?<=")[\s\w./_$()=,]*',line).group(0)
				menuLabel_list.append(text_string);
				f3.write( 'menuLabel = %s\n'%(text_string))


			elif in_displayName==1:
				
				text_string= re.search('(?<=")[\s\w./_$()]*',line).group(0)
				displayName_list.append(text_string);
				f3.write( 'displayName = %s\n'%(text_string))



					
			
	finally:
		f3.write("\n\n-------------END PARSE---------------\n")
		f.close()
		f2.write(opi_end);
		f2.close()
    







	













				
    
#read line


#if field dtype, we will change, else write the line.

#re.search('(?<=field\(DTYP).*','  field(DTYP,asyn$(TIMER)1)').group(0)

