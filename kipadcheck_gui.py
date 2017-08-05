# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 28 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class kipadcheck_gui
###########################################################################

class kipadcheck_gui ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 656,531 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button1 = wx.Button( self.m_panel3, wx.ID_ANY, u"Run Pad", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self.m_panel3, wx.ID_ANY, u"Run Stencil", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self.m_panel3, wx.ID_ANY, u"Run Drill", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel3, wx.ID_ANY, u"Run Silk", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		self.m_panel3.SetSizer( bSizer21 )
		self.m_panel3.Layout()
		bSizer21.Fit( self.m_panel3 )
		bSizer2.Add( self.m_panel3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL, wx.DefaultValidator, u"progress" )
		self.m_gauge1.SetValue( 0 ) 
		bSizer2.Add( self.m_gauge1, 0, wx.EXPAND, 5 )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel8 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.VERTICAL )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		self.m_staticText11 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Via to Via spacing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gbSizer1.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText112 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"(mils)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText112.Wrap( -1 )
		gbSizer1.Add( self.m_staticText112, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText1121 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"(mils)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1121.Wrap( -1 )
		gbSizer1.Add( self.m_staticText1121, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText11211 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"(mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11211.Wrap( -1 )
		gbSizer1.Add( self.m_staticText11211, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_textCtrl21 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"vv" )
		gbSizer1.Add( self.m_textCtrl21, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText1 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Via to Track spacing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gbSizer1.Add( self.m_staticText1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"vt" )
		gbSizer1.Add( self.m_textCtrl2, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText111 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Drill to Edge spacing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		gbSizer1.Add( self.m_staticText111, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl211 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"dtoe" )
		gbSizer1.Add( self.m_textCtrl211, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		self.m_panel8.SetSizer( gbSizer1 )
		self.m_panel8.Layout()
		gbSizer1.Fit( self.m_panel8 )
		self.m_notebook1.AddPage( self.m_panel8, u"Drill Parameters", False )
		self.m_panel9 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText18 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Silk to Pad minimum spacing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		gbSizer3.Add( self.m_staticText18, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_textCtrl10 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"sp" )
		gbSizer3.Add( self.m_textCtrl10, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"(mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gbSizer3.Add( self.m_staticText19, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Silk minimum thickness (aka \"width\")", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		gbSizer3.Add( self.m_staticText21, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"smw" )
		gbSizer3.Add( self.m_textCtrl11, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText22 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"(mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		gbSizer3.Add( self.m_staticText22, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText23 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Text minimum height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		gbSizer3.Add( self.m_staticText23, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_textCtrl12 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"tmh" )
		gbSizer3.Add( self.m_textCtrl12, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"(mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		gbSizer3.Add( self.m_staticText24, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText241 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"(mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText241.Wrap( -1 )
		gbSizer3.Add( self.m_staticText241, wx.GBPosition( 8, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText25 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Text minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		gbSizer3.Add( self.m_staticText25, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText27 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Thickness / Height = 1 /", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		gbSizer3.Add( self.m_staticText27, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_textCtrl13 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"wtoh" )
		gbSizer3.Add( self.m_textCtrl13, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText26 = wx.StaticText( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		gbSizer3.Add( self.m_staticText26, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText29 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Silk Slow Check (off=check boundaries only)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		gbSizer3.Add( self.m_staticText29, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_checkBox1 = wx.CheckBox( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"sc" )
		gbSizer3.Add( self.m_checkBox1, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText30 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Draw All Outlines (writes to Debug Layer)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		gbSizer3.Add( self.m_staticText30, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Outline Thickness (non-0 writes to Debug Layer)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		gbSizer3.Add( self.m_staticText32, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_textCtrl14 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"ot" )
		gbSizer3.Add( self.m_textCtrl14, wx.GBPosition( 8, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_checkBox2 = wx.CheckBox( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"dao" )
		gbSizer3.Add( self.m_checkBox2, wx.GBPosition( 9, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText242 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Debug Options", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText242.Wrap( -1 )
		gbSizer3.Add( self.m_staticText242, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 3 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText211 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Eco2.User", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )
		gbSizer3.Add( self.m_staticText211, wx.GBPosition( 7, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText231 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Debug Layer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText231.Wrap( -1 )
		gbSizer3.Add( self.m_staticText231, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		
		self.m_panel9.SetSizer( gbSizer3 )
		self.m_panel9.Layout()
		gbSizer3.Fit( self.m_panel9 )
		self.m_notebook1.AddPage( self.m_panel9, u"Silk Parameters", True )
		
		bSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.Pad )
		self.m_button2.Bind( wx.EVT_BUTTON, self.Stencil )
		self.m_button3.Bind( wx.EVT_BUTTON, self.Drill )
		self.m_button4.Bind( wx.EVT_BUTTON, self.Silk )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Pad( self, event ):
		event.Skip()
	
	def Stencil( self, event ):
		event.Skip()
	
	def Drill( self, event ):
		event.Skip()
	
	def Silk( self, event ):
		event.Skip()
	

