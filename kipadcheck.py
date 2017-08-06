# kipadcheck.py
#
# KiPadCheck
# https://github.com/HiGregSmith/KiPadCheck
# Original Author: Greg Smith, June-August 2017
#
# THERE ARE NO GUARANTEES THAT THE Design Rule Checks ARE 
# COMPLETE OR THOROUGH. USE AT YOUR OWN RISK.
#
# ABOUT
#
# KiPadCheck provides additional basic DRC checks to KiCAD and proviedes lists
# to make tweaking pads easier for drill compliance, silk compliance, and
# stencil creation. It adds a menu item to "Tools" called KiPadCheck which
# brings up a dialog for control. Functions include pad list, drill list,
# drill to drill spacing check, drill to track spacing check, stencil
# aperture check vs. stencil thicknesses, stencil aperture width vs.
# paste type, silk overlap of copper, text width/height/ratio, silk width.
#
#   
# INSTALLATION
#
# In Windows, place file in 
# C:\Program Files\KiCad\share\kicad\scripting\plugins\kipadcheck.py
# C:\Program Files\KiCad\share\kicad\scripting\plugins\kipadcheck_gui.py
# In pcbnew, open scripting console (Tools > Scripting Console)
# Type "import kipadcheck".
#
# If installed in the scripting/plugins folder, installation should occur
# with Tools > External Plugins > Refresh Plugins.
# Otherwise, type "import kipadcheck" in the Scripting Console.
# This installs a menu item in Tools > External Plugins > KiPadCheck.
# There's a little bit of weirdness that happens during development and
# repeated loads and imports. There's an inconsistency between the menu items
# Tools > KiPadCheck and Tools > External Plugins > KiPadCheck
# Both should work.
#
# USE
#
# Selecting the KiPadCheck menu item brings up the Dialog for control of the
# checks.
#
# Fill out the dimension information supplied by your PCB manufacturer to
# check your layout against. You can enter the units along with the number and
# KiPadCheck will recognize the units appropriately.
#
# The following entry items are used in the respective checks.
#
# Pad Info: Produces output on the KiCad console, no dialog entries used.
# Stencil Info: Produces output on the KiCad console, no dialog entries used.
# Drill Info: Produces output on the KiCad console, the following entries are used.
#       Via to Via Spacing
#       Via to Track spacing
#       Drill to Edge spacing
#       Drill Minimum
#       Drill Maximum
#       Drill Set
# Silk Info:  Produces output on the KiCad console, the following entries are used.
#       Silk to Pad spacing:
#           Spacing between items on silk layers and pad copper.
#       Silk Slow Check:
#           Enables non-zero silk-to-pad check, and text stroke check.
#           If disabled, will only check silk overlap of pad against
#           bounding boxes of text.
#           Note that text strokes are only checked if the text bounding box
#           is close enough to require further checking.
#       Silk Minimum Width:
#           The minimum line thickness on the silk layer for text and
#           graphical items.
#       Text Minimum Height:
#           The minimum height of text on the silk layer.
#       Minimum Text W/H:
#           The ratio of text thickness divided by text height must be
#           greater than 1 divided by the value in this entry.
#           A typical value entered here would be "5" which would represent
#           a W/H ratio of 1/5, or 0.2.
#       DEBUG OPTIONS
#       Outline Thickness:
#           Will draw outlines on Eco2 layer of pads and text that are checked.
#           Note that text strokes are only checked if the text bounding box
#           is close enough to require further checking.
#       Draw All Outlines:
#           Will draw all outlines of pads and text strokes with the specified
#           Outline Thickness.
#
# TODO
#   Support layers appropriately for all checks. Currently SilkInfo does
#      check layers appropriately: F.Cu vs. F.SilkS and B.Cu vs. B.SilkS.
#      Other checks may only support 2 layers or may incorrectly check all
#      layers, including those that don't make sense (e.g. F.SilkS vs. B.Cu).
#   Support non-rectangular pads. Currently checks only rectangle bounding box.
#   Handle pad drill vs. via drill appropriately.
#   Check annular ring size.
#   Outputs are in varying non-changable units (mils, inches, mm, nm)
#   Label output units and make consistent.
#	Support more than just through drills (i.e. buried/blind self._vias).
#   Mask Info: Check solder mask dam sizes (i.e. "Mask spacing.")
#   Check Annular Rings.
#   Allow reading/writing from dru file, then:
#       Consider adapting translation for descriptions:
#       https://ctrlq.org/code/19909-google-translate-api
#
# COMPLETE
#
# DONE Allow changing drill sets
# DONE Allow changing Debug Layer
# DONE Allow changing input units
# DONE Update progress bar when doing SilkInfo
# DONE Silk Info: Check silk screen character sizes:
#           Minimum Character Width(Legend)	0.15mm	Characters of less than 0.15mm wide will be too narrow to be identifiable.
#           Minimum Character Height (Legend)	0.8mm	Characters of less than 0.8mm high will be too small to be recognizable.
#           Character Width to Height Ratio (Legend)	1:5
# DONE Check drill to Edge.Cut clearance.
#
#
# Pad Info: Produces two lists: 
#   1) detailed list of pads by footprint reference with paste/mask properties
#   2) quantity of pads by size
# Drill Info: Generates multiple lists:
#   1) Hole quantity by specified pad drill sizes
#   2) Quantity by closest larger standard drill size
#      (future option will be to pick among defined drill sets)     
#   3) Drill list
#   4) Distance from each via to next closest via
#   5) Checks via drill to via drill clearance
#   6) Checks via drill to track clearance
# Stencil Info:
#   1) Lists quantity of apertures by aperture size
#   2) Summary of aperture ratios by stencil thickness
#   3) Checks AspectRatio and AreaRatio against a variety 
#      of stencil thicknesses (2 mil-7 mil, all currently hardcoded)
#   4) Lists solder paste sizes for calculating appropriate.
# SilkInfo has several options:
#   1) Fast check of silkscreen bounding boxes and line segments.
#   2) Slower check includes line thicknesses.
#
# EXAMPLES:
#
# Pad Info: Produces two lists: 
#   1) detailed list of pads by footprint reference with paste/mask properties
#      Number of pads: 293
#      
#      ***** Pads By Footprint Reference, Alphabetical *****
#      # 4	(BT1.) X=113.665086 Y=147.423648 P=CIRC (2.64, 2.64) D=CIRC
#      (2.64, 2.64) Layers=F.Cu,B.Cu,B.Mask,F.Mask lc=0.0000 c=0.1530
#      Paste: spm=0.0000,0.0000 lspm=0.0000 lspmr=0.0000
#      | Mask : smm=0.0000 lsmm=0.0000
#      ...
#   2) quantity of pads by size
#      ***** Quantity of Pads By Size *****
#      Size: 0.900 0.900, Quantity 4
#      Size: 0.875 1.250, Quantity 2
#      Size: 0.800 1.200, Quantity 2
#      Size: 0.900 1.700, Quantity 1
#      Size: 0.300 0.800, Quantity 24
#      ...
#
# Drill Info: Generates multiple lists:
#   1) Hole quantity by specified pad drill sizes
#      ***** Quantity of Pads By Specified Drill Size *****
#      Size: 1.020mm, Quantity 2
#      Size: 4.826mm, Quantity 6
#      Size: 1.000mm, Quantity 54
#      Size: 2.640mm, Quantity 2
#      Size: 1.097mm, Quantity 8
#      
#   2) Hole quantity by closest larger standard drill size
#      (future option will be to pick among defined drill sets)     
#      ***** Quantity of Pads By Standard Drill Size *****
#      Size: 1.020mm (25.908in), Drill: 0.041 (59), Quantity 2
#      Size: 4.826mm (122.580in), Drill: 0.191 (11), Quantity 6
#      Size: 1.000mm (25.400in), Drill: 0.04 (60), Quantity 54
#      Size: 2.640mm (67.056in), Drill: 0.104 (37), Quantity 2
#      Size: 1.097mm (27.871in), Drill: 0.0465 (56), Quantity 8
#
#   3) Drill list
#      ***** Drill Holes List
#     (pad #, position (nm), Type, Drill, Drill Value, Via Width) *****
#      0 (152661291, 138048648) 3 294000 294000 600000
#      1 (113725000, 140800000) 3 294000 294000 600000
#      ...
#
#   4) Distance from each via to next closest via
#      ***** Distance to next closest via  *****
#      (looking only *forward* through the list)
#      
#      Minimum Via to Via = 20.000 mils (0.508 mm)
#      0 3.692 mm
#      1 1.205 mm
#      ...
#
#   5) Checks via drill to via drill clearance
#      ***** Vias too close to another via *****
#      29
#      44
#      ...
#
#   6) Checks via drill to track clearance
#      ***** Vias too close to track *****
#      31 Via (/IOC_RB6) at (125934690, 138137006) is 306005 away from track
#         (/IOC_RB5)
#         ((126280790, 137531001) ; (125660499, 137531001)). Shoud be 508000
#      23 Via (/GND) at (150540086, 141423648) is 307472 away from track (/RE2)
#         ((149487558, 140816176) ; (152110941, 140816176)). Shoud be 508000
#      ...
#      
# 
# Stencil Info:
#   1) Lists quantity of apertures by aperture size:
#      (Aperture in mm, triplets of:
#       stencil mil thickness, area ratio, aspect ratio)
#      (qty 24)	Aperture=0.225,0.725 (2.0 1.69 4.43) (3.0 1.13 2.95)
#         (4.0 0.85 2.21) (5.0 0.68 1.77) (6.0 0.56 1.48) (7.0 0.48 1.27)
#	      Pads: [20, 45, 80, 98, 99, 100, 101, 109, 113, 121, 125, 140,
#         143, 165, 205, 208, 209, 210, 233, 234, 238, 239, 241, 244]
#         From: CONN_01X24
#      ...
#
#   2) Summary of aperture ratios by stencil thickness
#       ***** Aperture Ratio Ranges *****
#       2.0 mil Aspect: 4.429 14.764	 Area  : 1.471 4.318
#       3.0 mil Aspect: 2.953 9.843	 Area  : 0.981 2.879
#       4.0 mil Aspect: 2.215 7.382	 Area  : 0.735 2.159
#       5.0 mil Aspect: 1.772 5.906	 Area  : 0.588 1.727
#       6.0 mil Aspect: 1.476 4.921	 Area  : 0.490 1.439
#       7.0 mil Aspect: 1.265 4.218	 Area  : 0.420 1.234
#
#   3) Checks AspectRatio and AreaRatio against a variety 
#      of stencil thicknesses (2 mil-7 mil, all currently hardcoded):
#       ***** Failed Aperture Test *****
#       Failed 5.0 mil thickness:
#       	Failed Area  : 0.445 0.225
#       	Failed Area  : 0.300 0.350
#       Failed 6.0 mil thickness:
#       	Failed Area  : 0.555 0.245
#       	Failed Area  : 0.445 0.225
#       	Failed Area  : 0.300 0.350
#       	Failed Area  : 0.225 0.725
#       	Failed Aspect: 0.445 0.225
#       	Failed Aspect: 0.225 0.725
#       Failed 7.0 mil thickness:
#       	Failed Area  : 0.555 0.245
#       	Failed Area  : 0.325 0.725
#       	Failed Area  : 0.445 0.225
#       	Failed Area  : 0.300 0.350
#       	Failed Area  : 0.225 0.725
#       	Failed Aspect: 0.555 0.245
#       	Failed Aspect: 0.445 0.225
#       	Failed Aspect: 0.225 0.725
#
# HISTORY
#
# Hopefully fixed nightly compatibility and some other improvements.
# Removed references to pcbnew colors.
# Disabled non-functional buttons on GUI.
# Removed unused GeomPoint class.
# Modified SilkInfo to work with progress bar.
# Fixed the 'Silk Slow Check' to incorporate text thickness and graphical item width
# One step closer to working with nightly re: LAYER_ID_COUNT => PCB_LAYER_ID_COUNT
#
# Eliminate dependance on class variable _board.
# Pad and drill lists not already ordered by number are ordered by area
#
# PROGRAMMING NOTES
#
# Naming conventions (from PEP8):
#       Short python naming guide (from PEP8):

#       ClassName
#       function_name
#       function_parameter
#       parameter_disambiguation_
#       variable_name
#       _nonpublic_function
#       _nonpublic_global_variable
#       CONSTANT_VALUE_NAME
#
# pcbnew.Iu2Mils and pcbnew.Iu2DMils do not seem to work on Windows/ KiCad 4.06
# Here, we use pcbnew.IU_PER_MILS and IU_PER_MM (not used: IU_PER_DECIMILS)
# I cannot seem to figure out LSET structure. Workarounds are applied in code.
#
# There are some examples of using python code to interact
# with KiCAD:
#    Install Tools menu, replace if already existing
#       (allows reloading python file after changes)
#    Iterate over tracks, identify self._vias, get sizes of
#    via and pad copper, mask, and paste
#    Identify which layers a pad is on.
#    Generate basic interactive window.
#    Display  multi-threaded wx.Gauge (self._progress bar).
#    Get Paste (stencil) Aperture size calculated from pad properties.
#


import time
import threading
import Queue
from operator import itemgetter
import math
import itertools

import wx
import pcbnew
import random # for testing
import kipadcheck_gui

# Action Plugin information here:
# https://forum.kicad.info/t/
# howto-register-a-python-plugin-inside-pcbnew-tools-menu/
# 5540/22

# Perhaps this site can lead to some rule of thumb checks for vias:
# https://www.eeweb.com/blog/eeweb/pcb-reliability-via-design1

 
    # ds = board.GetDesignSettings() 
    # ugly. exposes a public member not via an accessor method
    # nc = ds.m_NetClasses
    # foo = pcbnew.NETCLASSPTR("foo")
    # nc.Add(foo)

    # References for stencil information
    # BEST:
    # http://prod.semicontaiwan.org/zh/sites/semicontaiwan.org
    # /files/data15/docs/7_5_semicon_taiwan_2015_ppt_senju_akita.pdf
    
    # http://www.circuitnet.com/experts/56418.html
    
    
    # https://www.linkedin.com/pulse/
    #     how-choose-correct-stencil-suits-your-smt-requirement-lisa-chu
    # http://www.photostencil.com/pdf/choosing_a_stencil.pdf
    # https://www.smta.org/chapters/files/
    #     SMTA_India_05_SMTA_Presentation_Workshop_on_SMT_Stencil(R1).pdf
    # https://ise.lehigh.edu/sites/ise.lehigh.edu/files/99t_005.pdf
    
    # Minimum Aspect Ratio based on stencil production method:
    # 1.5; 
    # 1.8: chemical etched;
    # 1.2 Electropolished laser-cut or electroformed
    #    
    # http://www.indium.com/blog/
    #     stencil-coach-calculates-optimal-solder-paste-printing-aperture-
    #     parameters-now-available-online.php
    # 
    
class gui (kipadcheck_gui.kipadcheck_gui):
    kpc = None
    def __init__(self, kpc, parent,
        layer_names=None,
        drillset_names=None,
        *args, **kw):
        
        super(gui,self).__init__(parent, *args, **kw)
        kpc=kpc
        
        # fill any list box named *_layers with the layer names
        #print ', '.join([w.GetName() for w in windows])
        # First, get all the windows within gui
        if layer_names is not None:
            windows = [w for w in self.GetChildren()]
            i = 0
            while ( i < len(windows) ):
                try:
                    windows.extend([w for w in windows[i].GetChildren()])
                except:
                    pass
                i += 1
            # Get all windows that end in '_layers'
            layer_windows = filter(lambda x: x.GetName().endswith('_layers'),windows)
            # setitems of all *_layers windows with the layer names
            for window in layer_windows:
                try:
                    window.SetItems(layer_names)
                    
                    # right now, just force the selection to be Eco2.
                    # we can organize this later to allow different defaults
                    # for different controls (i.e. dict value by window name)
                    window.SetSelection(layer_names.index('Eco2.User'))
                except:
                    pass
        # Initialize Drill Set
        if drillset_names is not None:
            drillsetcontrol = filter(lambda x: x.GetName() == 'drillset' ,windows)[0]
            drillsetcontrol.SetItems(drillset_names)
            drillsetcontrol.SetSelection(0)
        
    def Pad(self,e):
        kpc.PadInfo(e)
    def Silk(self,e):
        kpc.SilkInfo(e)
    def Stencil(self,e):
        kpc.StencilInfo(e)
    def Drill(self,e):
        kpc.DrillInfo(e)

    def get_value_float(self,name):
        # parse the entered value for value and units.
        input_string = self.FindWindowByName(name).GetValue()
        if input_string is None \
           or not isinstance(input_string,basestring) \
           or input_string == '':
            value = 0.0
            units = ''
        else:
            #print "input %s"%(input_string)
            value,units = parse_measurement(input_string)
            #print "Value %f; Units %s"%(value,units)
             
        
        if units is None or units.strip() == '':
            # if no units were specified, use the units specified in label.
            #print "Units Label: %s"%(name+'_units')
            units = self.FindWindowByName(name+'_units').GetLabel()
        else:
            # if units were specified, set the label to those units.
            units = units.strip()
            self.set_units(name,units)
        
        if value is None:
            return 0.0
            
        mult = conversion.get(units,1) #or 1/default_units
       

        # value = None
        # try:
            # value = float(self.FindWindowByName(name).GetValue())
        # except ValueError:
            # pass
        return value * mult
        
    def set_units(self,name,label):
        units_name = name+'_units'
        value = None
        control = self.FindWindowByName(units_name)
        if control is not None:
            print "Setting %s to %s"%(units_name,label)
            control.SetLabel(label)
            return True
        return False
        
class wxPointUtil:
    """A variety of utilities and geometric calculations for
       operating on wxPoint objects. Will work on other objects with
       x,y attributes"""
       
    atts=('x','y','z')
    d=[]
    # 
    # Possible functions to implement for point class: 
    # __add__(), __radd__(), __iadd__(), __mul__(), __rmul__() and __imul__()
    # 
        
    @staticmethod
    def dot(v,w):
        """return the dot product of point and w"""
        return v.x*w.x + v.y*w.y	
    @staticmethod
    def distance2(v,w):
        """return the distance squared between point and w"""
        #sub=w-v
        wvx = w.x - v.x
        wvy = w.y - v.y
        return wvx*wvx+wvy*wvy #abs(wxPointUtil.dot(sub,sub))
    @staticmethod
    def distance(v,w):
        """return the distance between point and w"""
        p = v - w
        return (p.x*p.x+p.y*p.y)**(1/2.0)
    @staticmethod
    def scale(w,factor):
        """ scale (multiply) the point x and y by a specific factor"""
        # self.x *= factor
        # self.y *= factor
        return w.__class__(float(w.x)*factor,float(w.y)*factor)

    @staticmethod
    def projection_axis(v, axis):
        """Project the point onto axis specified by w.
           w must be a vector on the unit circle (for example: (1,0) or (0,1)
           to project on the x axis or y axis, respectively)"""
           
        # Consider the line extending the segment,
        # parameterized as v + t (w - v).
        # We find projection of point p onto the line. 
        # It falls where t = [(p-v) . (w-v)] / |w-v|^2
        t = wxPointUtil.dot(v,axis);
        return t
        
    # v,w are points defining the line segment
    @staticmethod
    def projection_line(p, v, w):
        """project point onto the line segment v,w"""
        # Return minimum distance between line segment vw and point p
        # Consider the line extending the segment,
        # parameterized as v + t (w - v).
        # We find projection of point p onto the line. 
        # It falls where t = [(p-v) . (w-v)] / |w-v|^2
        # We clamp t from [0,1] to handle points outside the segment vw.
        # if w.x == v.x and w.y == v.y:
            # return self.distance(w);   # v == w case

        #print "divisor=",w.distance(v)
        wv=w-v
        wvx = w.x - v.x
        wvy = w.y - v.y
        pvx = p.x - v.x
        pvy = p.y - v.y
        #t=0.5
        t = max(0, min(1, abs(pvx*wvx+pvy*wvy) / float(wvx*wvx+wvy*wvy)));
        #t = max(0, min(1, wxPointUtil.dot(p - v,wv) / float(wxPointUtil.distance2(w,v))));
        projection = v + wxPointUtil.scale(wv,t);  # Projection falls on the segment
        return projection
    
    @staticmethod
    def normal(v, w):
        """NOT FINISHED
           get normals of line formed with point w 
           This is the left normal if w is clockwise of self 
           This is the right normal if w is counter-clockwise of self"""
        w.x - v.x, 
        w.y - v.y
    
    # var normals:Vector.<Vector2d> = new Vector.<Vector2d>
    # for (var i:int = 1; i < dots.length-1; i++) 
    # {
        # var currentNormal:Vector2d = new Vector2d(
            # dots[i + 1].x - dots[i].x, 
            # dots[i + 1].y - dots[i].y
        # ).normL //left normals
        # normals.push(currentNormal);
    # }
    # normals.push(
        # new Vector2d(
            # dots[1].x - dots[dots.length-1].x, 
            # dots[1].y - dots[dots.length-1].y
        # ).normL
    # )
    # return normals;

    @staticmethod
    def mindistance2(u, v, w):
        """Return minimum distance squared between point and line segment v,w.
           Perhaps obviously, this is faster than mindistance because sqrt()
           is not called."""
        #L2 = wxPointUtil.distance2(v,w)
        if w.x == v.x and w.y == v.y:
        #if L2 == 0.0:
            return wxPointUtil.distance2(u,w);   # v == w case
        return wxPointUtil.distance2(u,wxPointUtil.projection_line(u,v,w))        
        
    @staticmethod
    def mindistance(u, v, w):
        """return minimum distance squared between point and line segment v,w"""
        L2 = wxPointUtil.distance2(w,v)
        #if w.x == v.x and w.y == v.y:
        if L2 == 0.0:
            return wxPointUtil.distance(u,w);   # v == w case
        return wxPointUtil.distance(u,wxPointUtil.projection_line(u,v,w))
        
        # L2 = v.distance2(w);  # i.e. |w-v|^2 -  avoid a sqrt
        # if (L2 == 0.0):
            # return p.distance(w);   # v == w case
        # return p.distance(self.projection_line(v,w));
        
        # p = self
        # # Return minimum distance between line segment vw and point p
        # L2 = self.distance2(v, w);  # i.e. |w-v|^2 -  avoid a sqrt
        # if (L2 == 0.0):
            # return p.distance(v);   # v == w case
        # # Consider the line extending the segment,
        # # parameterized as v + t (w - v).
        # # We find projection of point p onto the line. 
        # # It falls where t = [(p-v) . (w-v)] / |w-v|^2
        # # We clamp t from [0,1] to handle points outside the segment vw.
        # t = max(0, min(1, (p - v).dot(w - v) / float(L2)));
        # # SavePrint = "L2 %d; t %.3f"%(L2,t)
        
        # #t = max(0, min(1, (v - p).dot(v - w) / float(L2)));
        # projection = v + (w-v).scale(t);  # Projection falls on the segment
        # return p.distance(projection);
                
    #https://stackoverflow.com/questions/2272179/a-simple-algorithm-for-polygon-intersection
    # NB: The algorithm only works for convex polygons, specified in either clockwise, or counterclockwise order.

    # 1)For each edge in both polygons, check if it can be used as a separating line. If so, you are done: No intersection.
    # 2) If no separation line was found, you have an intersection

    @staticmethod
    def check_polygons_intersecting(poly_a, poly_b,closed=True):
        """Returns boolean indicating whether the indicated polygons are intersecting.
           closed=True indicates the last point is equal to the first point.
           if closed=False, the first and last point are checked as if they represent
           the last polygon edge."""
        for polygon in (poly_a, poly_b):
            #print "\nPolygon",

            # This loop is assuming last point is not the repeated first point:
            # for i1 in range(len(polygon)):
                # i2 = (i1 + 1) % len(polygon)
                
            # This loop assumes the last point is the repeated first point to form closed polygon:
            # for i1 in range(len(polygon)-1):
                # i2 = (i1 + 1)
                
            # This loop combines both loops above:
            for i1 in range(len(polygon)-1*closed):
                i2 = (i1 + 1) % len(polygon)
                
                #print("i1={} i2={}".format(polygon[i1], i2))
                p1 = polygon[i1]
                p2 = polygon[i2]

                normal = pcbnew.wxPoint(p2.y - p1.y, p1.x - p2.x)

                minA, maxA, minB, maxB = (None,) * 4

                for p in poly_a:
                    projected = normal.x * p.x + normal.y * p.y

                    if not minA or projected < minA:
                        minA = projected
                    if not maxA or projected > maxA:
                        maxA = projected

                for p in poly_b:
                    projected = normal.x * p.x + normal.y * p.y

                    if not minB or projected < minB:
                        minB = projected
                    if not maxB or projected > maxB:
                        maxB = projected

                #print("maxA={} minB={} -- maxB={} minA={}".format(maxA, minB, maxB, minA))
                if maxA < minB or maxB < minA:
                    return False
                #print(" Nope\n")

        return True
        
    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are colinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise
    # sign = lambda x: x and (1, -1)[x < 0]
    
    # Get leftmost point
    # i, value = min(enumerate(vector), key=attrgetter('x'))
    # nextpoint = vector[(i+1)%len(vector)]
    # @staticmethod
    # def orientation(p, q, r)
    # {
        # int val = (q.y - p.y) * (r.x - q.x) -
                  # (q.x - p.x) * (r.y - q.y);
     
        # if (val == 0) return 0;  // colinear
        # return (val > 0)? 1: 2; // clock or counterclock wise
    # }
    
    @staticmethod
    def convex_hull(self,line,vector):
        """NOT IMPLEMENTED.
           Currently returns bounding box, best used on orthogonal.
           Return the convex hull of point list vector
           A fast algorithm using Jarvis's Algorithm (aka Wrapping)."""
        minx = vector[0].x
        miny = vector[0].y
        maxx = minx
        maxy = miny
        for v in vector:
            minx = min(minx,v.x)
            maxx = max(minx,v.x)
            miny = min(miny,v.y)
            maxy = max(miny,v.y)           
        return (
            pcbnew.wxPoint(minx,maxy), # upper left
            pcbnew.wxPoint(maxx,maxy), # upper right
            pcbnew.wxPoint(maxx,miny), # lower right
            pcbnew.wxPoint(minx,miny)) # lower left

            
    # ds = board.GetDesignSettings() 
    # ugly. exposes a public member not via an accessor method
    # nc = ds.m_NetClasses
    # foo = pcbnew.NETCLASSPTR("foo")
    # nc.Add(foo)

    # References for stencil information
    # BEST:
    # http://prod.semicontaiwan.org/zh/sites/semicontaiwan.org
    # /files/data15/docs/7_5_semicon_taiwan_2015_ppt_senju_akita.pdf
    
    # http://www.circuitnet.com/experts/56418.html
    
    
    # https://www.linkedin.com/pulse/
    #     how-choose-correct-stencil-suits-your-smt-requirement-lisa-chu
    # http://www.photostencil.com/pdf/choosing_a_stencil.pdf
    # https://www.smta.org/chapters/files/
    #     SMTA_India_05_SMTA_Presentation_Workshop_on_SMT_Stencil(R1).pdf
    # https://ise.lehigh.edu/sites/ise.lehigh.edu/files/99t_005.pdf
    
    # Minimum Aspect Ratio based on stencil production method:
    # 1.5; 
    # 1.8: chemical etched;
    # 1.2 Electropolished laser-cut or electroformed
    #    
    # http://www.indium.com/blog/
    #     stencil-coach-calculates-optimal-solder-paste-printing-aperture-
    #     parameters-now-available-online.php
    # 
    
####################################################################
############                           #############################
############      UNIT CONVERSION      #############################
############                           #############################
####################################################################

import re
# import pcbnew

# Regular expression to parse floating point followed by units.
# The first group (the scanf() tokens for a number any which way) is
# lifted directly from the python docs for the re module.

SCANF_MEASUREMENT = re.compile(
    r'''(                      # group match like scanf() token %e, %E, %f, %g
    [-+]?                      # +/- or nothing for positive
    (\d+(\.\d*)?|\.\d+)        # match numbers: 1, 1., 1.1, .1
    ([eE][-+]?\d+)?            # scientific notation: e(+/-)2 (*10^2)
    )
    (\s*)                      # separator: white space or nothing
    (                          # unit of measure: like GB. also works for no units
    \S*)''',    re.VERBOSE)
'''
:var SCANF_MEASUREMENT:
    regular expression object that will match a measurement

    **measurement** is the value of a quantity of something. most complicated example::

        -666.6e-100 units
'''

def parse_measurement(value_sep_units):
    value = None
    units = None
    measurement = re.match(SCANF_MEASUREMENT, value_sep_units)
    if measurement:
        #print measurement.groups()
        try:
            value = float(measurement.groups()[0])
        except ValueError:
            pass
            #print "doesn't start with a number", value_sep_units
        units = measurement.groups()[5]
    # else:
        # print "No match!"

    return value, units


conversion = {
    '':1,
    'nm':1,
    'nanometer':1,
    'nanometers':1,
    'um':pcbnew.IU_PER_MM/1000.0,
    'micron':pcbnew.IU_PER_MM/1000.0,
    'microns':pcbnew.IU_PER_MM/1000.0,
    'micrometer':pcbnew.IU_PER_MM/1000.0,
    'micrometers':pcbnew.IU_PER_MM/1000.0,
    'decimicron':pcbnew.IU_PER_MM/10000.0,
    'decimicrons':pcbnew.IU_PER_MM/10000.0,
    'du':pcbnew.IU_PER_MM/10000.0,
    'dus':pcbnew.IU_PER_MM/10000.0,
    'dum':pcbnew.IU_PER_MM/10000.0,
    'dums':pcbnew.IU_PER_MM/10000.0,
    'mm':pcbnew.IU_PER_MM,
    'millimeter':pcbnew.IU_PER_MM,
    'millimeters':pcbnew.IU_PER_MM,
    'm':pcbnew.IU_PER_MM*1000,
    'meter':pcbnew.IU_PER_MM*1000,
    'meters':pcbnew.IU_PER_MM*1000,
    'km':pcbnew.IU_PER_MM*1000000,
    'kilometer':pcbnew.IU_PER_MM*1000000,
    'kilometers':pcbnew.IU_PER_MM*1000000,
    'thou':pcbnew.IU_PER_MILS,
    'mil':pcbnew.IU_PER_MILS,
    'mils':pcbnew.IU_PER_MILS,
    'dmil':pcbnew.IU_PER_MILS/10.0,
    'dmils':pcbnew.IU_PER_MILS/10.0,
    'decimil':pcbnew.IU_PER_MILS/10.0,
    'decimils':pcbnew.IU_PER_MILS/10.0,
    'cmil':pcbnew.IU_PER_MILS/100.0,
    'cmils':pcbnew.IU_PER_MILS/100.0,
    'centimil':pcbnew.IU_PER_MILS/100.0,
    'centimils':pcbnew.IU_PER_MILS/100.0,
    'cm':pcbnew.IU_PER_MM*10,
    'centimeter':pcbnew.IU_PER_MM*10,
    'centimeters':pcbnew.IU_PER_MM*10,
    'in':pcbnew.IU_PER_MILS*1000.0,
    'inch':pcbnew.IU_PER_MILS*1000.0,
    'inches':pcbnew.IU_PER_MILS*1000.0,
    '"':pcbnew.IU_PER_MILS*1000.0, # inches
    "'":pcbnew.IU_PER_MILS*1000.0*12, # feet
    'feet':pcbnew.IU_PER_MILS*1000.0*12,
    'foot':pcbnew.IU_PER_MILS*1000.0*12,
}
# squared versions of measurements (three types: 2, **2, ^2)
for unit in conversion.keys():
    value = conversion[unit]
    conversion[unit+'2']=value**2
    conversion[unit+'^2']=value**2
    conversion[unit+'**2']=value**2
    
def convert_to_iu(value_units_string,default_units='',assume_squared=False):
    """default_units specified as a valid suffix or a multiplier for
       converting to nanometers."""
    value, units = parse_measurement(value_units_string)
    if value is None:
        return None
    mult = conversion.get(units,conversion.get(default_units)) or 1/default_units
    
    # if assume_squared:
        # mult = mult*mult

    return value*mult

####################################################################
############                               #########################
############      END UNIT CONVERSION      #########################
############                               #########################
####################################################################




class KiPadCheck( pcbnew.ActionPlugin ):
    """Contains user interface and calculations for a variety
       of KiCad layers and objects. Includes information and checks on:
       Pads, Silk, Stencil Apertures (Paste), and Drills."""

# LAYERCOUNT = 0
# while (0 <= pcbnew.GetBoard().GetLayerID(pcbnew.GetBoard().GetLayerName(LAYERCOUNT)) <= 254):
    # LAYERCOUNT += 1

# num = 0
# while (0 <= pcbnew.GetBoard().GetLayerID(pcbnew.GetBoard().GetLayerName(num)) <= 254):
    # num += 1
# num
  
    try:
        LAYERCOUNT = pcbnew.PCB_LAYER_ID_COUNT # nightlies, post 4.0.6
    except:
        LAYERCOUNT = pcbnew.LAYER_ID_COUNT # KiCad 4.0.6 stable
        

    # Some threading support for self._progress bar (wx.Gauge)

    # This allows stopping the thread from outside the thread.
    _progress_stop = False
    """Allows stopping the progress thread from outside the thread."""
    
    # These provide communication from inside the thread to the main GUI thread:
    _progress_value_queue = Queue.Queue()
    """Place values in the queue to set the progress value, which is set
       in the main GUI thread."""
    _console_text_queue = Queue.Queue()
    """Place values in the queue to write as console text in the pcbnew window,
       which is written in the main GUI thread."""

    def defaults( self ):
        """Support for ActionPlugins, though it doesn't work in 4.0.6 stable"""
        self.name = "KiPadCheck"
        self.category = "Check PCB"
        self.description = "Check pads, holes, stencil apertures, mask, and silkscreen"


    def progress_thread_function(self,WorkerThread):
        value = self._progress.GetValue()
        while(WorkerThread.is_alive()):
        
            # take stuff from queue here
            # take all you can, then call update_progress()
            while (not self._progress_value_queue.empty()):
                value = self._progress_value_queue.get()
            self.update_progress(value)
            while (not self._console_text_queue.empty()):
                self._consoleText.AppendText(self._console_text_queue.get())
            time.sleep(0.25)
        # process any remaining from the queues.
        while (not self._progress_value_queue.empty()):
            value = self._progress_value_queue.get()
        self.update_progress(value)
        while (not self._console_text_queue.empty()):
            self._consoleText.AppendText(self._console_text_queue.get())

    # def GraphThreadFunction():
        # while(not GraphStop):
            # # put stuff in queue here
            # DataQueue.put("1")
            # sleep(1)
    #from scipy import reshape, sqrt, identity
    #import numpy
    _consoleText = None
    _pcbnewWindow = None
    _frame = None
    _progress = None
    """The index within StandardDrill to use in DrillInfo() checks."""
    
    _StandardDrill = []
    """Tables of standard drill sets. Each member of the list is itself a list
       of tuples (float Size, string Name)."""
    _StandardDrillInfo = []
    """Information about the standard drill array member.
       Description, Scale, Source (link)
       Scale is multiplied by Size to get the drill size in nanameters."""

    # self._StandardDrillInfo is a list of tuples (Drill Set Name, scale factor)
    # scale factor is used to convert to nm (which are currently nm).
    # self._StandardDrillInfo is in parallel order with self._StandardDrill
    # self._StandardDrill is a list of lists of tuples. Each tuple is
    # (Size in scale units, printable name)

    #http://www.engineersedge.com/drill_sizes.htm
    _StandardDrillInfo.append(
        ("Fractional per ANSI/ASME B94.11M-1993",
        pcbnew.IU_PER_MILS*1000,
        "http://www.engineersedge.com/drill_sizes.htm"))
    _StandardDrill.append([
    (.0135,"80"),
    (.0145,"79"),
    (.0156,"1/64"),
    (.0160,"78"),
    (.0180,"77"),
    (.0200,"76"),
    (.0210,"75"),
    (.0225,"74"),
    (.0240,"73"),
    (.0250,"72"),
    (.0260,"71"),
    (.0280,"70"),
    (.0292,"69"),
    (.0310,"68"),
    (.0313,"1/32"),
    (.0320,"67"),
    (.0330,"66"),
    (.0350,"65"),
    (.0360,"64"),
    (.0370,"63"),
    (.0380,"62"),
    (.0390,"61"),
    (.0400,"60"),
    (.0410,"59"),
    (.0420,"58"),
    (.0430,"57"),
    (.0465,"56"),
    (.0469,"3/64"),
    (.0520,"55"),
    (.0550,"54"),
    (.0595,"53"),
    (.0625,"1/16"),
    (.0635,"52"),
    (.0670,"51"),
    (.0700,"50"),
    (.0730,"49"),
    (.0760,"48"),
    (.0781,"5/64"),
    (.0785,"47"),
    (.0810,"46"),
    (.0820,"45"),
    (.0860,"44"),
    (.0890,"43"),
    (.0935,"42"),
    (.0937,"3/32"),
    (.0960,"41"),
    (.0980,"40"),
    (.0995,"39"),
    (.1015,"38"),
    (.1040,"37"),
    (.1065,"36"),
    (.1093,"7/64"),
    (.1100,"35"),
    (.1110,"34"),
    (.1130,"33"),
    (.1160,"32"),
    (.1200,"31"),
    (.1250,"1/8"),
    (.1285,"30"),
    (.1360,"29"),
    (.1405,"28"),
    (.1406,"9/64"),
    (.1440,"27"),
    (.1470,"26"),
    (.1495,"25"),
    (.1520,"24"),
    (.1540,"23"),
    (.1562,"5/32"),
    (.1570,"22"),
    (.1590,"21"),
    (.1610,"20"),
    (.1660,"19"),
    (.1695,"18"),
    (.1719,"11/64"),
    (.1730,"17"),
    (.1770,"16"),
    (.1800,"15"),
    (.1820,"14"),
    (.1850,"13"),
    (.1875,"3/16"),
    (.1890,"12"),
    (.1910,"11"),
    (.1935,"10"),
    (.1960,"9"),
    (.1990,"8"),
    (.2010,"7"),
    (.2031,"13/64"),
    (.2040,"6"),
    (.2055,"5"),
    (.2090,"4"),
    (.2130,"3"),
    (.2187,"7/32"),
    (.2210,"2"),
    (.2280,"1"),
    (.2340,"A"),
    (.2344,"15/64"),
    (.2380,"B"),
    (.2420,"C"),
    (.2460,"D"),
    (.2500,"E"),
    (.2500,"1/4"),
    (.2570,"F"),
    (.2610,"G"),
    (.2656,"17/64"),
    (.2660,"H"),
    (.2720,"I"),
    (.2770,"J"),
    (.2811,"K"),
    (.2812,"9/32"),
    (.2900,"L"),
    (.2950,"M"),
    (.2968,"19/64"),
    (.3020,"N"),
    (.3125,"5/16"),
    (.3160,"O"),
    (.3230,"P"),
    (.3281,"21/64"),
    (.3320,"Q"),
    (.3390,"R"),
    (.3437,"11/32"),
    (.3480,"S"),
    (.3580,"T"),
    (.3594,"23/64"),
    (.3680,"U"),
    (.3750,"3/8"),
    (.3770,"V"),
    (.3860,"W"),
    (.3906,"25/64"),
    (.3970,"X"),
    (.4040,"Y"),
    (.4062,"13/32"),
    (.4130,"Z"),
    (.4219,"27/64"),
    (.4375,"7/16"),
    (.4531,"29/64"),
    (.4687,"15/32"),
    (.4844,"31/64"),
    (.5000,"1/2"),
    (.5156,"33/64"),
    (.5312,"17/32"),
    (.5469,"35/64"),
    (.5625,"9/16"),
    (.5781,"37/64"),
    (.5937,"19/32"),
    (.6094,"39/64"),
    (.6250,"5/8"),
    (.6406,"41/64"),
    (.6562,"21/32"),
    (.6719,"43/64"),
    (.6875,"11/16"),
    (.7031,"45/64"),
    (.7187,"23/32"),
    (.7344,"47/64"),
    (.7500,"3/4"),
    (.7656,"49/64"),
    (.7812,"25/32"),
    (.7969,"51/64"),
    (.8125,"13/16"),
    (.8281,"53/64"),
    (.8437,"27/32"),
    (.8594,"55/64"),
    (.8750,"7/8"),
    (.8906,"57/64"),
    (.9062,"29/32"),
    (.9219,"59/64"),
    (.9375,"15/16"),
    (.9531,"61/64"),
    (.9687,"31/32"),
    (.9844,"63/64"),
    (1.000,"1")])
    _StandardDrillInfo.append(
        ("ISO Metric per ANSI/ASME B94.11M-1993 (preconverted to mils)",
        pcbnew.IU_PER_MILS*1000,
        "http://www.engineersedge.com/drill_sizes.htm"))
    _StandardDrill.append([
    (.0138,".35"),
    (.0157,".4"),
    (.0177,".45"),
    (.0197,".5"),
    (.0217,".55"),
    (.0236,".6"),
    (.0256,".65"),
    (.0276,".7"),
    (.0295,".75"),
    (.0315,".8"),
    (.0335,".85"),
    (.0355,".9"),
    (.0374,".95"),
    (.0394,"1.0"),
    (.0413,"1.05"),
    (.0433,"1.1"),
    (.0453,"1.15"),
    (.0472,"1.2"),
    (.0492,"1.25"),
    (.0512,"1.3"),
    (.0531,"1.35"),
    (.0551,"1.4"),
    (.0571,"1.45"),
    (.0591,"1.5"),
    (.0610,"1.55"),
    (.0629,"1.6"),
    (.0650,"1.65"),
    (.0669,"1.7"),
    (.0689,"1.75"),
    (.0709,"1.8"),
    (.0728,"1.85"),
    (.0748,"1.9"),
    (.0768,"1.95"),
    (.0787,"2.0"),
    (.0807,"2.05"),
    (.0827,"2.1"),
    (.0846,"2.15"),
    (.0866,"2.2"),
    (.0886,"2.25"),
    (.0905,"2.3"),
    (.0925,"2.35"),
    (.0945,"2.4"),
    (.0965,"2.45"),
    (.0984,"2.5"),
    (.1004,"2.55"),
    (.1024,"2.6"),
    (.1043,"2.65"),
    (.1063,"2.7"),
    (.1083,"2.75"),
    (.1102,"2.8"),
    (.1142,"2.9"),
    (.1181,"3.0"),
    (.1220,"3.1"),
    (.1260,"3.2"),
    (.1280,"3.25"),
    (.1299,"3.3"),
    (.1339,"3.4"),
    (.1378,"3.5"),
    (.1417,"3.6"),
    (.1457,"3.7"),
    (.1477,"3.75"),
    (.1496,"3.8"),
    (.1535,"3.9"),
    (.1575,"4.0"),
    (.1614,"4.1"),
    (.1654,"4.2"),
    (.1674,"4.25"),
    (.1693,"4.3"),
    (.1732,"4.4"),
    (.1771,"4.5"),
    (.1811,"4.6"),
    (.1850,"4.7"),
    (.1870,"4.75"),
    (.1890,"4.8"),
    (.1929,"4.9"),
    (.1968,"5.0"),
    (.2008,"5.1"),
    (.2047,"5.2"),
    (.2067,"5.25"),
    (.2087,"5.3"),
    (.2126,"5.4"),
    (.2165,"5.5"),
    (.2205,"5.6"),
    (.2244,"5.7"),
    (.2264,"5.75"),
    (.2283,"5.8"),
    (.2323,"5.9"),
    (.2362,"6.0"),
    (.2401,"6.1"),
    (.2441,"6.2"),
    (.2461,"6.25"),
    (.2480,"6.3"),
    (.2520,"6.4"),
    (.2559,"6.5"),
    (.2598,"6.6"),
    (.2638,"6.7"),
    (.2658,"6.75"),
    (.2677,"6.8"),
    (.2716,"6.9"),
    (.2756,"7.0"),
    (.2795,"7.1"),
    (.2835,"7.2"),
    (.2855,"7.25"),
    (.2874,"7.3"),
    (.2913,"7.4"),
    (.2953,"7.5"),
    (.2990,"7.6"),
    (.3031,"7.7"),
    (.3051,"7.75"),
    (.3071,"7.8"),
    (.3110,"7.9"),
    (.3150,"8.0"),
    (.3189,"8.1"),
    (.3228,"8.2"),
    (.3248,"8.25"),
    (.3267,"8.3"),
    (.3307,"8.4"),
    (.3346,"8.5"),
    (.3386,"8.6"),
    (.3425,"8.7"),
    (.3445,"8.75"),
    (.3465,"8.8"),
    (.3504,"8.9"),
    (.3543,"9.0"),
    (.3583,"9.1"),
    (.3622,"9.2"),
    (.3642,"9.25"),
    (.3661,"9.35"),
    (.3701,"9.4"),
    (.3740,"9.5"),
    (.3780,"9.6"),
    (.3819,"9.7"),
    (.3839,"9.75"),
    (.3858,"9.8"),
    (.3898,"9.9"),
    (.3937,"10.0"),
    (.4133,"10.5"),
    (.4331,"11.0"),
    (.4528,"11.5"),
    (.4724,"12.0"),
    (.4921,"12.5"),
    (.5118,"13.0"),
    (.5315,"13.5"),
    (.5512,"14.0"),
    (.5708,"14.5"),
    (.5906,"15.0"),
    (.6102,"15.5"),
    (.6300,"16.0"),
    (.6496,"16.5"),
    (.6693,"17.0"),
    (.6889,"17.5"),
    (.7087,"18.0"),
    (.7283,"18.5"),
    (.7480,"19.0"),
    (.7677,"19.5"),
    (.7874,"20.0"),
    (.8071,"20.5"),
    (.8268,"21.0"),
    (.8465,"21.5"),
    (.8661,"22.0"),
    (.8858,"22.5"),
    (.9055,"23.0"),
    (.9252,"23.5"),
    (.9449,"24.0"),
    (.9646,"24.5"),
    (.9843,"25.0")
    ])
    # http://www.pcbwizards.com/Drillchart.htm
    _StandardDrillInfo.append(("Standard PCB drill sizes",
        pcbnew.IU_PER_MILS*1000,
        "http://www.pcbwizards.com/Drillchart.htm"))
    _StandardDrill.append([
    (0.011,"85"),
    (0.0115,"84"),
    (0.012,"83"),
    (0.0125,"82"),
    (0.013,"81"),
    (0.0135,"80"),
    (0.0145,"79"),
    (0.015625,"1/64"),
    (0.016,"78"),
    (0.018,"77"),
    (0.02,"76"),
    (0.021,"75"),
    (0.0225,"74"),
    (0.024,"73"),
    (0.025,"72"),
    (0.026,"71"),
    (0.028,"70"),
    (0.0292,"69"),
    (0.031,"68"),
    (0.03125,"1/32"),
    (0.032,"67"),
    (0.033,"66"),
    (0.035,"65"),
    (0.036,"64"),
    (0.037,"63"),
    (0.038,"62"),
    (0.039,"61"),
    (0.04,"60"),
    (0.041,"59"),
    (0.042,"58"),
    (0.043,"57"),
    (0.0465,"56"),
    (0.046875,"3/64"),
    (0.052,"55"),
    (0.055,"54"),
    (0.0595,"53"),
    (0.0625,"1/16"),
    (0.0635,"52"),
    (0.067,"51"),
    (0.07,"50"),
    (0.073,"49"),
    (0.076,"48"),
    (0.078125,"5/64"),
    (0.0785,"47"),
    (0.081,"46"),
    (0.082,"45"),
    (0.086,"44"),
    (0.089,"43"),
    (0.0935,"42"),
    (0.09375,"3/32"),
    (0.096,"41"),
    (0.098,"40"),
    (0.0995,"39"),
    (0.1015,"38"),
    (0.104,"37"),
    (0.1065,"36"),
    (0.109375,"7/64"),
    (0.11,"35"),
    (0.111,"34"),
    (0.113,"33"),
    (0.116,"32"),
    (0.12,"31"),
    (0.125,"1/8"),
    (0.1285,"30"),
    (0.136,"29"),
    (0.1405,"28"),
    (0.140625,"9/64"),
    (0.144,"27"),
    (0.147,"26"),
    (0.1495,"25"),
    (0.152,"24"),
    (0.154,"23"),
    (0.15625,"5/32"),
    (0.157,"22"),
    (0.159,"21"),
    (0.161,"20"),
    (0.166,"19"),
    (0.1695,"18"),
    (0.171875,"11/64"),
    (0.173,"17"),
    (0.177,"16"),
    (0.18,"15"),
    (0.182,"14"),
    (0.185,"13"),
    (0.1875,"3/16"),
    (0.189,"12"),
    (0.191,"11"),
    (0.1935,"10"),
    (0.196,"09"),
    (0.199,"08"),
    (0.201,"07"),
    (0.203125,"13/64"),
    (0.204,"06"),
    (0.2055,"05"),
    (0.209,"04"),
    (0.213,"03"),
    (0.21875,"7/32"),
    (0.221,"02"),
    (0.228,"01")
    ])
    #size_iu = size*scale
    _StandardDrillInfo.append(
        ("ISO Metric per ANSI/ASME B94.11M-1993",
        pcbnew.IU_PER_MM,
        "http://www.pcbwizards.com/Drillchart.htm"))

    _StandardDrill.append([
    (.35,".35"),
    (.4,".4"),
    (.45,".45"),
    (.5,".5"),
    (.55,".55"),
    (.6,".6"),
    (.65,".65"),
    (.7,".7"),
    (.75,".75"),
    (.8,".8"),
    (.85,".85"),
    (.9,".9"),
    (.95,".95"),
    (1.0,"1.0"),
    (1.05,"1.05"),
    (1.1,"1.1"),
    (1.15,"1.15"),
    (1.2,"1.2"),
    (1.25,"1.25"),
    (1.3,"1.3"),
    (1.35,"1.35"),
    (1.4,"1.4"),
    (1.45,"1.45"),
    (1.5,"1.5"),
    (1.55,"1.55"),
    (1.6,"1.6"),
    (1.65,"1.65"),
    (1.7,"1.7"),
    (1.75,"1.75"),
    (1.8,"1.8"),
    (1.85,"1.85"),
    (1.9,"1.9"),
    (1.95,"1.95"),
    (2.0,"2.0"),
    (2.05,"2.05"),
    (2.1,"2.1"),
    (2.15,"2.15"),
    (2.2,"2.2"),
    (2.25,"2.25"),
    (2.3,"2.3"),
    (2.35,"2.35"),
    (2.4,"2.4"),
    (2.45,"2.45"),
    (2.5,"2.5"),
    (2.55,"2.55"),
    (2.6,"2.6"),
    (2.65,"2.65"),
    (2.7,"2.7"),
    (2.75,"2.75"),
    (2.8,"2.8"),
    (2.9,"2.9"),
    (3.0,"3.0"),
    (3.1,"3.1"),
    (3.2,"3.2"),
    (3.25,"3.25"),
    (3.3,"3.3"),
    (3.4,"3.4"),
    (3.5,"3.5"),
    (3.6,"3.6"),
    (3.7,"3.7"),
    (3.75,"3.75"),
    (3.8,"3.8"),
    (3.9,"3.9"),
    (4.0,"4.0"),
    (4.1,"4.1"),
    (4.2,"4.2"),
    (4.25,"4.25"),
    (4.3,"4.3"),
    (4.4,"4.4"),
    (4.5,"4.5"),
    (4.6,"4.6"),
    (4.7,"4.7"),
    (4.75,"4.75"),
    (4.8,"4.8"),
    (4.9,"4.9"),
    (5.0,"5.0"),
    (5.1,"5.1"),
    (5.2,"5.2"),
    (5.25,"5.25"),
    (5.3,"5.3"),
    (5.4,"5.4"),
    (5.5,"5.5"),
    (5.6,"5.6"),
    (5.7,"5.7"),
    (5.75,"5.75"),
    (5.8,"5.8"),
    (5.9,"5.9"),
    (6.0,"6.0"),
    (6.1,"6.1"),
    (6.2,"6.2"),
    (6.25,"6.25"),
    (6.3,"6.3"),
    (6.4,"6.4"),
    (6.5,"6.5"),
    (6.6,"6.6"),
    (6.7,"6.7"),
    (6.75,"6.75"),
    (6.8,"6.8"),
    (6.9,"6.9"),
    (7.0,"7.0"),
    (7.1,"7.1"),
    (7.2,"7.2"),
    (7.25,"7.25"),
    (7.3,"7.3"),
    (7.4,"7.4"),
    (7.5,"7.5"),
    (7.6,"7.6"),
    (7.7,"7.7"),
    (7.75,"7.75"),
    (7.8,"7.8"),
    (7.9,"7.9"),
    (8.0,"8.0"),
    (8.1,"8.1"),
    (8.2,"8.2"),
    (8.25,"8.25"),
    (8.3,"8.3"),
    (8.4,"8.4"),
    (8.5,"8.5"),
    (8.6,"8.6"),
    (8.7,"8.7"),
    (8.75,"8.75"),
    (8.8,"8.8"),
    (8.9,"8.9"),
    (9.0,"9.0"),
    (9.1,"9.1"),
    (9.2,"9.2"),
    (9.25,"9.25"),
    (9.35,"9.35"),
    (9.4,"9.4"),
    (9.5,"9.5"),
    (9.6,"9.6"),
    (9.7,"9.7"),
    (9.75,"9.75"),
    (9.8,"9.8"),
    (9.9,"9.9"),
    (10.0,"10.0"),
    (10.5,"10.5"),
    (11.0,"11.0"),
    (11.5,"11.5"),
    (12.0,"12.0"),
    (12.5,"12.5"),
    (13.0,"13.0"),
    (13.5,"13.5"),
    (14.0,"14.0"),
    (14.5,"14.5"),
    (15.0,"15.0"),
    (15.5,"15.5"),
    (16.0,"16.0"),
    (16.5,"16.5"),
    (17.0,"17.0"),
    (17.5,"17.5"),
    (18.0,"18.0"),
    (18.5,"18.5"),
    (19.0,"19.0"),
    (19.5,"19.5"),
    (20.0,"20.0"),
    (20.5,"20.5"),
    (21.0,"21.0"),
    (21.5,"21.5"),
    (22.0,"22.0"),
    (22.5,"22.5"),
    (23.0,"23.0"),
    (23.5,"23.5"),
    (24.0,"24.0"),
    (24.5,"24.5"),
    (25.0,"25.0")])

    _StandardDrillInfo.append(
        ("Reduced set PCB drill sizes",
        pcbnew.IU_PER_MM,
        ("https://electronics.stackexchange.com/"
        "questions/85292/"
        "what-pad-hole-drill-size-is-appropriate-for-a-given-"
        "a-given-through-hole-lead-diameter")))

    _StandardDrill.append([
    (.020,"76"),
    (.025,"72"),
    (.029,".029in"),
    (.035,"65"),
    (.040,"60"),
    (.046,".046in"),
    (.052,"55"),
    (.061,".061in"),
    (.067,"51"),
    (.079,".079in"),
    (.093,".093in"),
    (.110,"35"),
    (.125,"1/8in")
    ])

    # https://en.wikipedia.org/wiki/Solder_paste#By_size
    # IPC J-STD 005 80% minimum between
    PowderSizeRangeByType_um = {
    1:(75,150),
    2:(45,75),
    3:(25,45), # Avg 35 -> Apt 0.175mm (7mil)
    4:(20,38), # Avg 29 -> Apt 0.145mm (6mil)
    5:(10,25), # Avg 17.5 -> Apt 0.0875mm (3.5mil)
    6:(5,15),
    7:(2,11),
    8:(2,8)
    }
    """Dictionary of IEC Solder Powder Type related to the min/max powder size in microns."""
    # rules of thumb 
    # http://www.circuitnet.com/experts/56418.html
    # minimum of 4-5 solder particles should span the width of the stencil
    # aperture. Type 3 powder is used for (a) 20 mil pitch CSPs & above 16 mil
    # pitch QFPs & above; Type 4 is typically used for anything smaller
    #
    # The breaking point for Type 3 solder paste in printing applications
    # is generally considered to be in the range of a 9-mil stencil aperture
    # width for most pastes.

    # Type 3 paste will generally work well down to an aperture with an
    # opening of 9 mils or greater. For apertures that are narrower than
    # 9 mils in width, the user is best off using Type 4 paste
    # This rule says that you need to be able to fit five of the largest
    # powder particles across the narrowest aperture in order to achieve
    # good stencil release.

    # 16mil pitch, and micro BGAs from 10mil and below and as a cut-off point
    # for type-3 powder.
    #
    # Some of the new Fine Grain foils allow for paste release down to
    # a .45 surface area ratio.
    #
    # Type 3 solder paste has an average solder sphere of 36 microns,
    # So any aperture smaller than 180 microns (7 mils) should use type 4
    # solder paste.
    # Solder sphere for type 4 is 30 microns, So any aperture smaller than
    # 150 microns (6mils) should use type 5 paste

    # Future categorization:
    # http://www.indium.com/blog/solder-powder-types-3-4-5-6-7.php


        
    padshapes = {
        pcbnew.PAD_SHAPE_CIRCLE: "CIRC",
        pcbnew.PAD_SHAPE_OVAL: "OVAL",
        pcbnew.PAD_SHAPE_RECT: "RECT",
        pcbnew.PAD_SHAPE_TRAPEZOID: "TPZD" 
    }
    """A simple dictionary for retreiving pad shape name from enumeration value."""
    # new in the most recent kicad code
    if hasattr(pcbnew, 'PAD_SHAPE_ROUNDRECT'):
        padshapes[pcbnew.PAD_SHAPE_ROUNDRECT] = "RREC"
     

    shapes = {
        pcbnew.S_ARC:"Arc",
        pcbnew.S_CIRCLE:"Circle",
        pcbnew.S_CURVE:"Curve",
        pcbnew.S_LAST:"Last",
        pcbnew.S_POLYGON:"Polygon",
        pcbnew.S_RECT:"Rect",
        pcbnew.S_SEGMENT:"Segment"
    }
    """A simple dictionary for retreiving (segment?) shape name from enumeration value."""

    _layernums = []
    """Layers on this board, specifically excluding inner copper layers
       that don't exist as indicated by GetBoard().GetCopperLayerCount()"""
    _layer_num_by_name = {}
    """Dicationary of layer numbers indicated by the given name."""
    # _board = None
    # """The current board loaded into KiCad (shortcut for pcbnew.GetBoard())"""        

    def CreateLabeledEntry(self,parent,label="",name="",value=0.0):
        """Create a wx Double Spin Control with label for the GUI."""
        #p = wx.Panel(parent,wx.ID_ANY)
        p = wx.StaticBox(parent,label=label)#,size=wx.Size(300,100))
        #sb1 = wx.StaticBox(panelbottom,label="mils1",size=wx.Size(300,300))

        sbs = wx.BoxSizer(wx.HORIZONTAL)
        #p.SetSizer(sbs)
        #sl = wx.SpinCtrlDouble(p,wx.ID_ANY,name=name,value=str(value), initial=value)
        #sbs.Add(sl)
        #sbs.Add(wx.StaticText(p, wx.ID_ANY,label=label))
        #sbs.Layout()
        
        # aurabindo contrib:
        sl = wx.SpinCtrlDouble(p,wx.ID_ANY,name=name,value=str(value), initial=value)
        sl.SetSize(wx.Size(96, 47))
        sbs.Add(sl, 0, wx.ALL | wx. EXPAND, 5)
        sbs.Add(wx.StaticText(p, wx.ID_ANY,label=label), 0, wx.ALL | wx.EXPAND, 5)
        sbs.AutoSize = True
        sbs.Fit()
        sbs.Layout()
        p.SetSizer(sbs)

        return p
    def CreateLabeledCheckBox(self,parent,label="",name="",initial=False):
        """Create a CheckBox Control with label."""
        #p = wx.Panel(parent,wx.ID_ANY)
        p = wx.StaticBox(parent,label=label)#,size=wx.Size(300,100))
        #sb1 = wx.StaticBox(panelbottom,label="mils1",size=wx.Size(300,300))

        sbs = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(sbs)
        #sbs = wx.StaticBoxSizer(p,wx.HORIZONTAL)
        sl = wx.CheckBox(p,wx.ID_ANY,name=name)
        sl.SetValue(initial)
        sbs.Add(sl)#(sbs.GetStaticBox(),wx.ID_ANY))
        sbs.Add(wx.StaticText(p, wx.ID_ANY,label=label))
        #sl.SetLabel="12.0"
        return p

    def create_panel(self):
        p = wx.Panel(self._frame)
        wx.GridBagSizer()
    def MenuItemPadInfo(self,e):
        """The main function called when the menu item is selected.
           This function displays the Dialog for providing parameters and executing
           functions."""
        board = pcbnew.GetBoard()
        self._consoleText.AppendText("Starting MenuItemPadInfo()...\n")

##################################################
######   Get Layers Used   #######################
##################################################
        #self._layernums = [num for num in range(self.LAYERCOUNT) if not board.GetLayerName(num).startswith("In")]
        copperLayers = filter(
            (lambda x: pcbnew.IsCopperLayer(x)),
            range(self.LAYERCOUNT))
        nonCopperLayers = filter(
            (lambda x: pcbnew.IsNonCopperLayer(x)),
            range(self.LAYERCOUNT))
        self._layernums = copperLayers[0:board.GetCopperLayerCount()] \
            + nonCopperLayers
        #self._layernums = copperLayers + nonCopperLayers
        self._layernums = [copperLayers[0]] \
            + [copperLayers[-1]] \
            + copperLayers[1:board.GetCopperLayerCount()-1] \
            + nonCopperLayers

        self._layer_num_by_name = {}
        for num in range(self.LAYERCOUNT):
            self._layer_num_by_name[board.GetLayerName(num)] = num
        layer_names = sorted(self._layer_num_by_name.keys(), key=lambda x: self._layer_num_by_name[x])
        
##################################################
#########   End Layers Used   ####################
##################################################

        windowName = 'KiPadCheck'

        padsWindow = wx.FindWindowByLabel(windowName,parent=self._pcbnewWindow)
        if padsWindow is not None:
            #padsWindow.Close()
            padsWindow.Iconize(False); # restore if minimized
            padsWindow.Raise() # raise to the top
            self._frame = padsWindow
            self._progress = self._frame.FindWindowByName('progress')

        else:
            # this will tie the 'Pads' window to pcbnew window
            names = [pcbnew.GetBoard().GetLayerName(num) for num in self._layernums]
            drillsets = map(lambda x:x[0],self._StandardDrillInfo)

            self._frame = gui(self,parent=self._pcbnewWindow,
                layer_names=names,
                drillset_names=drillsets
            )
            self._progress = self._frame.FindWindowByName('progress')
            #self._frame = wx.Frame(self._pcbnewWindow, size=wx.Size(50,50),title=windowName) #, size=wx.Size(400,400))
            # paneltop = wx.Panel(self._frame)
            # panelbottom = wx.Panel(self._frame)
            # #sb1 = wx.StaticBox(panelbottom,label="mils1",size=wx.Size(300,300))
            # #sb2 = wx.StaticBox(panelbottom,label="mils2",size=wx.Size(300,300))
            # sizertop = wx.BoxSizer(wx.HORIZONTAL)
            # sizerbottom = wx.BoxSizer(wx.VERTICAL)
            # sizerpanels = wx.BoxSizer(wx.VERTICAL)
            # sizerpanels.Add(paneltop)
            # sizerpanels.Add(panelbottom)

            # self._frame.SetSizer(sizerpanels)
            # paneltop.SetSizer(sizertop)
            # panelbottom.SetSizer(sizerbottom)
            # panelbottom.AutoSize = True

            # self._progress = wx.Gauge(panelbottom,name="progress")
            # #sizerbottom.Add(self._progress)
            # # aurabindo contrib:
            # sizerbottom.Add(self._progress, 0, wx.ALL | wx.EXPAND, 0)
            
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"(mil) Via to Via spacing","vv",12.0))
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"(mil) Via to Track spacing","vt",12.0))
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"(mm) Drill to Edge spacing","dtoe",3.0))
            # sp = self.CreateLabeledEntry(panelbottom,"(mm) Silk to Pad spacing","sp",0.0)
            # #sp.Disable()
            # sizerbottom.Add(sp)
            # cb = self.CreateLabeledCheckBox(panelbottom,"Silk Slow Check (off = check boundaries only)","sc")
            # sizerbottom.Add(cb)
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"(mm) Outline Thickness (for debug, non-0 writes to Eco2)","ot",0.00))
            # cb = self.CreateLabeledCheckBox(panelbottom,"Draw All Outlines (debug, writes to Eco2)","dao")
            # sizerbottom.Add(cb)
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"(mm) USER_silk_minimum_width","smw",0.15))
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"(mm) USER_text_minimum_height","tmh",0.8))
            # sizerbottom.Add(self.CreateLabeledEntry(panelbottom,"Minimum Text W/H = 1/[this value]","wtoh",5.0))
            
            # #cb.Disable()
            # #wx.CheckBox(panelbottom,wx.ID_ANY,name='oo', pos=wx.Point(300,300), initial=True,label="hello")
            # #sizerbottom.Add(sl)
            
            # self._frame.SetSizer(sizerpanels)
            # #    self.paneltop.SetSizer(sizer)
            # #self._frame.SetAutoLayout(True)
            # b_padlist = wx.Button(paneltop,label="Pad List")
            # b_padlist.Bind(wx.EVT_BUTTON, self.PadInfo)
            
            # b_drillinfo = wx.Button(
                # paneltop, label="Drill Info", pos=wx.Point(50,50))
            # b_drillinfo.Bind(wx.EVT_BUTTON, self.DrillInfo)
            
            # b_stencilinfo = wx.Button(
                # paneltop, label="Stencil Info", pos=wx.Point(100,100))
            # b_stencilinfo.Bind(wx.EVT_BUTTON, self.StencilInfo)

            # b_silkinfo = wx.Button(
                # paneltop, label="Silk Info")	
            # b_silkinfo.Bind(wx.EVT_BUTTON, self.SilkInfo)

            # sizertop.Add(b_padlist)
            # sizertop.Add(b_drillinfo)
            # sizertop.Add(b_stencilinfo)
            # sizertop.Add(b_silkinfo)
            # panelbottom.Hide()
            # panelbottom.Show()
            # panelbottom.Update()
            # panelbottom.Refresh()
            # self._frame.Layout()
            # self._frame.GetSizer().Layout()
            # panelbottom.Layout()
            # self._frame.Fit()
            # panelbottom.Fit()

        self._consoleText.AppendText("Finished MenuItemPadInfo()\n")
        self._frame.Show(True)
        self._frame.Update()
        self._frame.Refresh()
        wx.Yield()
        
    #	PadLayerNames, PadLayers = GetPadLayerNameNum()
    def get_vias(self):
        """Get vias by filtering from _board.GetTracks()."""
        return filter(lambda x: isinstance(x,pcbnew.VIA), pcbnew.GetBoard().GetTracks())
        
    def GetViaLayerNameNum(self,vias=None):
        """Get the layer numbers that each via is on.
           Return as a list in the same order as vias
           (or get_vias(), if vias is not supplied)"""
        return map(
            lambda v: tuple(layer for layer in range(self.LAYERCOUNT) \
            if layer in _layernums \
            #not board.GetLayerName(layer).startswith("In") \
                and v.IsOnLayer(layer)), vias or get_vias())

    def GetPads(self):
        """Get all the pads in a list ordered by pad number."""
        board = pcbnew.GetBoard()
        return [board.GetPad(n) for n in range(board.GetPadCount())]
        
    def get_drill_size(self,object):
        """Gets the value of the drill from pad or via."""
        if hasattr(object,'GetDrillSize'):
            d = object.GetDrillSize()
        else:
            d = object.GetDrillValue()
            d = pcbnew.wxPoint(d,d)
        return d


    def get_pad_holes_and_vias(self):
        board = pcbnew.GetBoard()
        holes = [board.GetPad(n) for n in range(board.GetPadCount()) if board.GetPad(n).GetDrillSize().x != 0 and board.GetPad(n).GetDrillSize().y != 0]
        holes.extend(self.get_vias())
        return holes
    def objects_by_layer(self, objects):
        returnval = {}
        for layernum in self._layernums:
            hs = filter ( lambda x: x.IsOnLayer(layernum), objects )
            if len(hs):
                returnval[layernum] = hs 
        return returnval

    def get_holes_by_layer(self):
        """Get all the pads in a list ordered by layer."""
        return self.objects_by_layer(self.get_pad_holes_and_vias())

    def GetAllHolesByLayer(self):
        """DEPRECATED
           Returns a dictionary with layer number as key, and a list of
           all drill holes (those from vias and pads)."""
        # self._layernums = [num for num in range(self.LAYERCOUNT) if not board.GetLayerName(num).startswith("In")]
        # self._layernums = range(self.LAYERCOUNT)
        allholes = self.GetPads()
        allholes.extend(self.get_vias())
        
        #print self._layernums
        layersByHole = []
        for h in allholes:
            layersByHole.append(
                tuple([layer for layer in self._layernums if h.IsOnLayer(layer)]))

    #	layersByHole = map(lambda h: tuple(layer for layer in self._layernums if h.IsOnLayer(layer)), allholes)

        holesByLayer = {}

        for index,layers in enumerate(layersByHole):
            for layer in layers:
                holesByLayer.setdefault(layer,[]).append(allholes[index])
        return holesByLayer
        

    def GetPadLayerNameNum(self):
        """Returns two structures: PadLayerNames is a list of layer names
        on which the pad lies, and PadLayers is a list of layer numbers.
        Each list is ordered by pad number."""
        board = pcbnew.GetBoard()
        PadLayers = {}
        PadLayerNames = {}
        for padnum in range(board.GetPadCount()):
            pad = board.GetPad(padnum)
            #_consoleText.AppendText("%s "%padnum)
            for layernum in self._layernums:
                if pad.IsOnLayer(layernum):
                    PadLayers.setdefault(padnum,[]).append(layernum)
                    PadLayerNames.setdefault(padnum,[]). \
                        append(board.GetLayerName(layernum))
            #_consoleText.AppendText("%s\n"%(" ".join(PadLayerNames[padnum])))
        # _consoleText.AppendText("************** PadLayerNames*************\n")

        # for padnum, names in PadLayerNames.iteritems():
            # _consoleText.AppendText("%s %s\n"%(str(padnum),','.join(names)))
        return PadLayerNames, PadLayers

    def GetPadSizes(self,padnums=None):
        """Returns a dictionary with key of pad size, and value of the list
           of pad numbers with that size."""
        board = pcbnew.GetBoard()
        padsizes = {}
        if padnums==None:
            padnums = range(board.GetPadCount())
        for padnum in padnums:
            pad = board.GetPad(padnum)
            key = pad.GetSize()
            key = (int(key[0]),int(key[1]))
            padsizes.setdefault(key,[]).append(pad)
        return padsizes
        
    def GetStencilSizes(self,padnums=None):
        """Returns a dictionary with key of Paste (stencil aperture) size,
           and value of the list of pad numbers with that size."""
        board = pcbnew.GetBoard()
        stencilsizes = {}
        if padnums==None:
            padnums = range(board.GetPadCount())
        for padnum in padnums:
            pad = board.GetPad(padnum)
            key = self.GetApertureSize(pad)
            key = (int(key[0]),int(key[1]))
            stencilsizes.setdefault(key,[]).append(padnum)
        return stencilsizes
        
    def GetPadHoles(self,padnums=None):
        """Returns a dictionary with key of Drill Hole size,
           and value of the list of pad numbers with that size."""
        board = pcbnew.GetBoard()
           
        self.padHolesBySize = {}
        # if padnums==None:
            # padnums = range(board.GetPadCount())
        for padnum in padnums or range(board.GetPadCount()):
            pad = board.GetPad(padnum)
            dsize = pad.GetDrillSize()
            self.padHolesBySize.setdefault( \
                (int(dsize[0]),int(dsize[1])),[]).append(pad)
        return self.padHolesBySize
        
    def BoundingBoxIntersect(self,element1,element2,growby):
        """Returns whether the (orthogonal) Bounding Boxes of the given
           elements are closer than "growby" from each other."""
        rect1 = element1.GetBoundingBox().GetWxRect()
        rect2 = element2.GetBoundingBox().GetWxRect()
        return RectangleNear(rect1,rect2,growby)
        
    def RectangleIntersect(self,rect1,rect2,grow1by):
        """Returns whether the (orthogonal) Rectangles of the given
           elements are closer than "growby" from each other.
           Rectangles are defined by index x=[0]; y=[1]; w=[2]; h=[3]."""
        #defined by indexed x=[0]; y=[1]; w=[2]; h=[3]
        hr1 = (rect1[2]+grow1by)/2.0
        vr1 = (rect1[3]+grow1by)/2.0
        hr2 = (rect2[2])/2.0
        vr2 = (rect2[3])/2.0
        # l1x = rect1[0] - hr1 ; l1y = rect1[1] - vr1 
        # r1x = rect1[0] + hr1 ; r1y = rect1[1] + vr1 
        # l2x = rect2[0] - hr2 ; l2y = rect2[1] - vr2 
        # r2x = rect2[0] + hr2 ; r2y = rect2[1] + vr2 
        l1x = rect1[0] - hr1 ; l1y = rect1[1] + vr1 
        r1x = rect1[0] + hr1 ; r1y = rect1[1] - vr1 
        l2x = rect2[0] - hr2 ; l2y = rect2[1] + vr2 
        r2x = rect2[0] + hr2 ; r2y = rect2[1] - vr2 
        #print l1x,r1x,l2x,r2x
        #print l1y,r1y,l2y,r2y
        
        #wxRect(118071999, 139321999, 856003, 2206003)
        #x
        
        # l1: Top Left coordinate of first rectangle.
        # r1: Bottom Right coordinate of first rectangle.
        # l2: Top Left coordinate of second rectangle.
        # r2: Bottom Right coordinate of second rectangle.
        # // If one rectangle is on left side of other
        # if (l1.x > r2.x || l2.x > r1.x)
            # return false;
     
        # // If one rectangle is above other
        # if (l1.y < r2.y || l2.y < r1.y)
            # return false;
        if (l1x > r2x) or (l2x > r1x):
            return False;
     
        # If one rectangle is above other
        if (l1y < r2y) or (l2y < r1y):
            return False;

        return True
        
    def PadInfo(self,e):
        """Main function for getting information about the pads in the current board."""
        board = pcbnew.GetBoard()
        self._consoleText.AppendText("Number of pads: %s\n"%(board.GetPadCount()))
        #_consoleText.AppendText("All Layers: %s\n"%(str(self._layernums)))
        
        self._consoleText.AppendText(
            "\n  ***** Pads By Footprint Reference, Alphabetical *****\n")	
                    
        
            
        # pad = pcbnew.GetBoard().GetPad(0)
        # modules  = pcbnew.GetBoard().GetModules()
        # for module in modules:
        # module.GetPads()
        self.PadsByReferenceAndName = {}
        PadLayerNames, PadLayers = self.GetPadLayerNameNum()
        for padnum in range(board.GetPadCount()):
            pad = board.GetPad(padnum)
            self.PadsByReferenceAndName.setdefault(
                str(pad.GetParent().GetReference()),{}). \
                setdefault(str(pad.GetPadName()),[]).append(padnum)
        
        sortedpads = []
        for ref in sorted(self.PadsByReferenceAndName.keys()):
            for padname in sorted(self.PadsByReferenceAndName[ref]):
                sortedpads.extend(self.PadsByReferenceAndName[ref][padname])
                
        for padnum in sortedpads: #range(board.GetPadCount()):
            pad = board.GetPad(padnum)
            psize = pad.GetSize()
            psize = (psize[0]/pcbnew.IU_PER_MM,psize[1]/pcbnew.IU_PER_MM)
            dsize = pad.GetDrillSize()
            dsize = (dsize[0]/pcbnew.IU_PER_MM,dsize[1]/pcbnew.IU_PER_MM)
            self._consoleText.AppendText(
                "#%5s\t(%s) X=%s Y=%s P=%s %s D=%s %s "
                "Layers=%s lc=%.4f c=%.4f\n\t"
                "Paste: spm=%.4f,%.4f lspm=%.4f lspmr=%.4f | "
                "Mask : smm=%.4f lsmm=%.4f\n"%(
                    padnum,
                    pad.GetParent().GetReference()+'.'+pad.GetPadName(),
                    pad.GetCenter()[0]/pcbnew.IU_PER_MM,
                    pad.GetCenter()[1]/pcbnew.IU_PER_MM,
                    self.padshapes[pad.GetShape()],
                    psize,
                    self.padshapes[pad.GetDrillShape()],
                    dsize,
                    ",".join(PadLayerNames[padnum]),
                    pad.GetLocalClearance()/pcbnew.IU_PER_MM,
                    pad.GetClearance()/pcbnew.IU_PER_MM,
                    pad.GetSolderPasteMargin()[0]/pcbnew.IU_PER_MM,
                    pad.GetSolderPasteMargin()[1]/pcbnew.IU_PER_MM,
                    pad.GetLocalSolderPasteMargin()/pcbnew.IU_PER_MM,
                    pad.GetLocalSolderPasteMargin()/pcbnew.IU_PER_MM,
                    pad.GetSolderMaskMargin()/pcbnew.IU_PER_MM,
                    pad.GetLocalSolderMaskMargin()/pcbnew.IU_PER_MM
                    ))
        self._consoleText.AppendText("\n***** Quantity of Pads By Size, ordered by Area *****\n")
        # sort pad sizes by area
        psizes = self.GetPadSizes()
        sizes = psizes.keys()
        sizes.sort(key=(lambda x: x[0]*x[1]))
        for padsize in sizes:
            padlist = psizes[padsize]
            self._consoleText.AppendText(
                "Size: %.3f %.3f, "
                "Quantity %s\n"%(
                padsize[0]/pcbnew.IU_PER_MM,
                padsize[1]/pcbnew.IU_PER_MM,
                len(padlist)))
        self._consoleText.AppendText("\n  ***** DONE *****\n")	
        
        
            #_consoleText.AppendText(str(key))
            # pad.GetAttribute
            # pad.GetBoard
            # pad.GetBoundingRadius
            # pad.GetBoundBox
            # pad.GetCenter
            # pad.GetClass
            # pad.GetClearance
            # pad.GetDelta
            # pad.GetDrillShape
            # pad.GetDrillSize
            # pad.GetFlags
            # pad.GetLayer
            # pad.GetLayerName
            # pad.GetLayerSet
            # pad.GetList
            # pad.GetLocalClearance
            # pad.GetLocalSolderMaskMargin
            # pad.GetLocalSolderPasteMargin
            # pad.GetLocalSolderPasteMarginRatio
            # pad.GetMenuImage
            # pad.GetMsgPanelInfo
            # pad.GetOblongDrillGeometry
            # pad.GetOffset
            # pad.GetOrientation
            # pad.GetPackedPadName
            # pad.GetPadName
            # pad.GetPadToDieLength
            # pad.GetParent
            # pad.GetPos0
            # pad.GetPosition
            # pad.GetSelectMenuText
            # pad.GetShape
            # pad.GetShortNetname
            # pad.GetSize
            # pad.GetSolderMaskMargin
            # pad.GetSolderPasteMargin
            # pad.GetState
            # pad.GetStatus
            # pad.GetSubNet
            # pad.GetThermalGap
            # pad.GetThermalWidth
            # pad.GetTimeStamp
            # pad.GetZoneConnection
            # pad.GetZoneSubNet
            # pad.UnplatedHoleMask
            # pad.ViewGetLayers
            # pad.ViewGetLOD

    def get_position_and_size(self,object):
        """Return GetPosition() and GetSize() in a tuple (x,y,w,h)."""
        p=object.GetPosition()
        s=object.GetSize()
        #p0=object.GetPos0()
        return (p[0],p[1],s[0],s[1])#,p0[0],p0[1])
    def get_corners_rotated_text(self,object):
        """Return the non-orthogonal corner points of TEXTE_ object (either PCB or MODULE),
           taking text object orientation and parent (if any) orientation."""
        # Box is given by
        if isinstance(object,pcbnew.TEXTE_MODULE):
            orientation = \
            object.GetDrawRotation()#\            
            #-object.GetTextAngle()
        else:
            orientation = object.GetTextAngle()
        
        # try:
            # m=object.GetParent().Cast()
            # parentorientation = m.GetOrientation()
        # except:
            # parentorientation = 0.0
        # orientation = parentorientation+object.GetTextAngleDegrees()*10
        
        return self.get_corners_rotated_rect(
            object.GetTextBox().getWxRect(),
            object.GetCenter(),
            orientation)
            
    def get_corners_rotated_pad(self,object):
        """NEED TO REVIEW IMPLIMENTATION! uses GetBoundingBox(),
           should use GetSize and GetPosition instead!
           Return the non-orthogonal corner points of pad object,
           taking object orientation and parent (if any) orientation."""
        # Box is given by
        # Upper Left, width, height
        size = object.GetSize()
        upperleft = pcbnew.wxPoint(object.GetCenter().x-size.x/2.0,object.GetCenter().y-size.y/2.0)
        return self.get_corners_rotated_rect(
            pcbnew.wxRect(upperleft,size),
            #object.GetBoundingBox().getWxRect(),
            object.GetCenter(),
            object.GetOrientation())#object.GetOrientation())
    def remove_drawings(self,layer):
        """Removes all drawings on specified layer from pcbnew.GetBoard()."""
        ds = pcbnew.GetBoard().GetDrawings()
        for d in ds:
            if d.IsOnLayer(layer):
                d.Remove()
    def get_rotated_vector(self,vector,center,orientation):
        """Returns new vector by rotating all points within given vector
           using center and orientation (in tenths of a degree)."""
        if len(vector) == 0:
            return vector
        # the center is the rotation point
        ox,oy = center
        orientation = -orientation/10.0
        cos= math.cos(math.radians(orientation))
        sin= math.sin(math.radians(orientation))
        
        rpoints = pcbnew.wxPoint_Vector(0)
        #initial points
        #print type(vector)
        #print "length of vector = ",len(vector)
        for v in vector:
            px=v[0]; py=v[1]
            # rotate point around center
            pox = px-ox
            poy = py-oy
            
            nx = cos * (pox) - sin * (poy) + ox
            ny = sin * (pox) + cos * (poy) + oy
            
            rpoints.append(pcbnew.wxPoint(int(nx),int(ny)))

        # add the start point to form a closed polygon
        rpoints.append(rpoints[0]) 
        
        return rpoints
    def get_corners_rotated_rect(self,rect,center,orientation):
        """Returns new list of wxPoints by rotating all points in the given
           rectangle using center and orientation (in tenths of a degree).
           Note: input is indexable (orthongonal) rectangle (x,y,w,h),
           while the return value is a list of corner points."""
        # rect is entered as a KiCAD boundingbox in wxRect format (indexable)
        # rect format is (upper left x, upper left y, width, height)
        # orientation for this algorithm is -(kicad orientation).
        # This is because algorithm orientation is in the opposite direction
        # of kicad orientation.
        # (note that orientation is returned as tenths of a degree,
        #  so this also converts to floating point degrees)
        orientation = -orientation/10.0
        
        # the center is the rotation point
        ox,oy = center
        
        rpoints = []
        #initial points
        for px,py in (
            (rect[0]        ,rect[1]),
            (rect[0]+rect[2],rect[1]),
            (rect[0]+rect[2],rect[1]+rect[3]),
            (rect[0]        ,rect[1]+rect[3]),
            ):
            
            # rotate point around center
            cos= math.cos(math.radians(orientation))
            sin= math.sin(math.radians(orientation))
            pox = px-ox
            poy = py-oy
            
            nx = cos * (pox) - sin * (poy) + ox
            ny = sin * (pox) + cos * (poy) + oy
            
            rpoints.append(pcbnew.wxPoint(int(nx),int(ny)))

        # add the start point to form a closed polygon
        rpoints.append(rpoints[0]) 
        
        return rpoints
    # def check_polygons_intersecting(polygon1,polygon2):
        # return True
        # # uses SAT algorithm. Does not generate the resulting intersection.
        # # only determines if they are disjoint.
    def test(self):
        """Testing wxPointUtil projection_axis.
        Printing values to Python console."""
        points=[]
        for i in range(1000):
            points.append(pcbnew.wxPoint(random.randrange(1000),random.randrange(1000)))
        
        xa = pcbnew.wxPoint(1,0)
        ya = pcbnew.wxPoint(0,1)
        for p in points:
            print p, p.projection_axis(xa),p.projection_axis(ya)
            
        # the shortest of the distance between point A and line segment CD, B and CD, C and AB or D and AB. So it's a fairly simple "distance between 

        p1 = (pcbnew.wxPoint(0.235, 0.305), pcbnew.wxPoint(0.485, 0.305), pcbnew.wxPoint(0.235, 0.495), pcbnew.wxPoint(0.485, 0.495))
        p2 = (pcbnew.wxPoint(-0.125, 0.405), pcbnew.wxPoint(0.125, 0.405), pcbnew.wxPoint(-0.125, 0.595), pcbnew.wxPoint(0.125, 0.595))
        r = wxPointUtil.check_polygons_intersecting(p1, p2)
        print(r)
        p1 = [pcbnew.wxPoint(0, 0), pcbnew.wxPoint(1,0), pcbnew.wxPoint(1, -1), pcbnew.wxPoint(0,-1), pcbnew.wxPoint(0,0)]
        p2 = [pcbnew.wxPoint(100,100), pcbnew.wxPoint(200,100), pcbnew.wxPoint(200, 50), pcbnew.wxPoint(100,50), pcbnew.wxPoint(100,100)]
        r = wxPointUtil.check_polygons_intersecting(p1, p2)
        print(r)
        p2 = [pcbnew.wxPoint(.5,.5), pcbnew.wxPoint(1.5,.5), pcbnew.wxPoint(1.5,-.5), pcbnew.wxPoint(.5,-.5), pcbnew.wxPoint(.5,.5)]
        r = wxPointUtil.check_polygons_intersecting(p1, p2)
        print(r)

    def draw_vector(self,vector,layer=pcbnew.Eco2_User,thickness=0.015*pcbnew.IU_PER_MM):
        """Draws the vector (wxPoint_vector of line segments) on the given
           layer and with the given thickness."""
        #print type(vector)
        for i in range(0,len(vector)-1,2):
            self.draw_segment(
                vector[i][0],
                vector[i][1],
                vector[i+1][0],
                vector[i+1][1],
                layer=layer,
                thickness=thickness)
    def draw_polygon(self,polygon,layer=pcbnew.Eco2_User,thickness=0.015*pcbnew.IU_PER_MM,close=False):
        """Draws the vector (wxPoint_vector of polygon vertices) on the given
           layer and with the given thickness.
           close indicates whether the polygon needs to be closed
           (close=False means the last point is equal to the first point).
           The drawing will use this input to draw a closed polygon."""
        #print type(vector)
        for i in range(len(polygon)-1):
            self.draw_segment(
                polygon[i][0],
                polygon[i][1],
                polygon[i+1][0],
                polygon[i+1][1],
                layer=layer,
                thickness=thickness)
        if close:
            self.draw_segment(
                polygon[0][0],
                polygon[0][1],
                polygon[-1][0],
                polygon[-1][1],
                layer=layer,
                thickness=thickness)
        
    def draw_segment(self,x1,y1,x2,y2,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
        """Draws the line segment indicated by the x,y values
        on the given layer and with the given thickness."""
        board = pcbnew.GetBoard()
        ds=pcbnew.DRAWSEGMENT(board)
        board.Add(ds)
        ds.SetStart(pcbnew.wxPoint(x1,y1))
        ds.SetEnd(pcbnew.wxPoint(x2,y2))
        ds.SetLayer(layer)
        #print thickness, thickness*pcbnew.IU_PER_MM, int(thickness*pcbnew.IU_PER_MM)
        ds.SetWidth(max(1,int(thickness*pcbnew.IU_PER_MM)))

    def SilkInfo(self,e):
    
        # Set up the thread, check if it is already running.
        # If so, return.
        self._progress_stop = False
        if self.WorkerThread is not None and self.WorkerThread.is_alive():
            self.progress_thread_function(self.WorkerThreadself)
            print self._progress
            self._progress.SetValue(0)
            return

        # Set up specifically for this worker thread.
        # only enough to set the max value of the progress bar.
        
        # Total number of checks is:
        # For each layer pair of padrects[i]*textrects[i]
        # + padrects[i]*graphicalitems_to_check[i]
        # Alternatively, just count each pad (sum of padrects[i]).
        
        pad_layer_list = (pcbnew.F_Cu,pcbnew.B_Cu)

        # Get items to check that are pads on the layers in pad_layer_list
        pads = self.GetPads()
        pads_to_check = []
        for layernum in pad_layer_list:
            pads_to_check.append(filter(lambda x:x.IsOnLayer(layernum),pads))
        
        done=sum([len(p) for p in pads_to_check])
        self._consoleText.AppendText("progress bar set to %d\n"%done)
        # initialize progress bar
        print self._progress
        self._progress.SetRange(done)

        # Start up the worker thread
        self.WorkerThread = threading.Thread(
            target=self.SilkInfo_Worker, 
            name="WT", 
            args=(), 
            kwargs={})#, daemon=False)#, *, daemon=None)
        self.WorkerThread.start()
        # Start the progress thread that updates the progress bar
        # and console text
        self.progress_thread_function(self.WorkerThread)
        
        # Finalize by making sure the worker thread is complete,
        # Then reset the progress bar.
        self.WorkerThread.join()
        self._progress.SetValue(0)

       
    def SilkInfo_Worker(self):
        """Main function for getting information about the Silk Layers on the current board.
           And executes basic silk-related DRC checks."""
           
                   # Fast check:
        # mindist2=max
        # intersecting? pad, text
           # yes, mindist2=0

        # if mindist2 <= minsilk^2:
           # mindist2=max
           # if thickness: draw
           # for each stroke
              # if intersecting stroke, pad
                 # mindist2=0
                 # break


        # Slow check:

        # mindist2=max
        # if intersecting pad, text
           # yes, mindist2=0
        # else: (slow)
           # mindist2=mindist2(pad,text)

        # if mindist2 <= minsilk^2:
           # mindist2=max
           # if thickness: draw
           # for each stroke
              # if intersecting stroke, pad
                 # mindist2=0
                 # break
              # else:
                 
        # self._progress_value_queue.put(count)
        # self._console_text_queue.put(text)
        board = pcbnew.GetBoard()
        
        Texts = self.get_text_objects()
        GraphicalItems = self.get_all_drawings_and_graphic_items_by_layer()
        
        # Texts = filter(lambda x:x.GetText()=='Elegant Computer Design',Texts)
        # Texts = filter(lambda x:x.GetText()=='I',Texts)

# reload(kipadcheck); kpc=kipadcheck.KiPadCheck(); kpc.Run(); kpc.MenuItemPadInfo(); kpc.SilkInfo(None)


        # Strokes need to be associated with the text so text width
        # can be retrieved
        # line to line intersection: http://paulbourke.net/geometry/pointlineplane/Helpers.cs

        # strokes_to_check is aligned with texts_to_check so
        # the text width can be retrieved during DRC

        #layer lists whould be in parallel, the same indexes are compared
        # on texts vs pad
        silk_layer_list = (pcbnew.F_SilkS,pcbnew.B_SilkS)
        pad_layer_list = (pcbnew.F_Cu,pcbnew.B_Cu)
        # other options:
        # pad_layer_list = (pcbnew.F_Mask,pcbnew.B_Mask)

        # Get items to check that are pads on the copper layers
        pads = self.GetPads()
        pads_to_check = []
        for layernum in pad_layer_list:
            pads_to_check.append(filter(lambda x:x.IsOnLayer(layernum),pads))
          
        padrect_to_check = []
        for layerindex,layernum in enumerate(pad_layer_list):
            padrect_to_check.append([])
            for i,pad in enumerate(pads_to_check[layerindex]):
                padrect_to_check[-1].append(self.get_corners_rotated_pad(pad))

        
        # Get items to check on the silk layer: graphical items and text
        texts_to_check = []
        strokes_to_check = []
        textrect_to_check = []
        graphicalitems_to_check = []
        for layernum in silk_layer_list:
            graphicalitems_to_check.append(GraphicalItems.get(layernum,[]))
            texts_to_check.append(filter(lambda x:x.IsOnLayer(layernum),Texts))
            strokes_to_check.append([])
            for t in texts_to_check[-1]:
                strokes_to_check[-1].append(pcbnew.wxPoint_Vector(0))
                t.TransformTextShapeToSegmentList(strokes_to_check[-1][-1])
                # orient TEXTE_MODULE strokes to the board
                # TEXTE_MODULE: oddly, the combination of draw rotation and 
                # orientation is what's needed to determine the correct
                # segments transformation only for TEXTE_MODULE object.

                # orientation is specified ccw (leftward) from positive x-axis
                if isinstance(t,pcbnew.TEXTE_MODULE):
                    orientation = t.GetDrawRotation()\
                                 -t.GetTextAngle() 
                                  
                    #print t.GetText(), orientation
                    strokes_to_check[-1][-1] = self.get_rotated_vector(strokes_to_check[-1][-1],t.GetCenter(),orientation)
                    
            textrect_to_check.append([])
            for text in texts_to_check[-1]:
                # if isinstance(text,pcbnew.TEXTE_MODULE):
                    # self._console_text_queue.put("%s %d %d %d\n"%(text.GetShownText(),text.GetDrawRotation(),t.GetTextAngle(),t.GetParent().Cast().GetOrientation()))
                # else:
                    # self._console_text_queue.put("%s %d\n"%(text.GetShownText(),t.GetTextAngle()))
                textrect_to_check[-1].append(self.get_corners_rotated_text(text))
            # for text in strokes_to_check[-1]:
                # wxPointUtil.convex_hull(strokes)
                
        # Draw all outlines writes to Eco2:
        # pad rectangles, text rectangles, text strokes with
        # thickness specified by Outline Thickness
        
        USER_minsilkpadspacing = (self._frame.get_value_float('sp') or 0.0)
        USER_slow_check        = self._frame.FindWindowByName('sc').GetValue()

        USER_draw_outlines_thickness = (self._frame.get_value_float('ot') or 0.0) 
        USER_silk_minimum_width = (self._frame.get_value_float('smw') or 0.0)
        USER_text_minimum_height = (self._frame.get_value_float('tmh') or 0.0)
        # expressed as W/H > 1/minW2H, or W*minW2H > H
        
        try:
            USER_text_minimum_WtoH = float(self._frame.FindWindowByName('dao').GetValue())
        except ValueError:
            USER_text_minimum_WtoH = 1.0
        USER_draw_stroke_thickness   = USER_draw_outlines_thickness
        USER_draw_all_outlines = self._frame.FindWindowByName('dao').GetValue()
        
        try:
            control = self._frame.FindWindowByName('dl_layers')
            USER_draw_outlines_layer = self._layer_num_by_name[control.GetString(control.GetSelection())]
        except:
            USER_draw_outlines_layer = pcbnew.Eco2_User
        print pcbnew.GetBoard().GetLayerName(USER_draw_outlines_layer)
        
        

        if USER_draw_all_outlines:
            for rects_to_check in (padrect_to_check, textrect_to_check):
                for rects in rects_to_check:
                    for vertices in rects:
                        for i in range(len(vertices)-1):
                            self.draw_segment(
                                vertices[i][0],
                                vertices[i][1],
                                vertices[i+1][0],
                                vertices[i+1][1],
                                layer=USER_draw_outlines_layer,
                                thickness=USER_draw_outlines_thickness)
                                

            for layerindex,strokes in enumerate(strokes_to_check):
                for vindex, vector in enumerate(strokes):

                    object=texts_to_check[layerindex][vindex]
                    center = object.GetCenter()
                    
                    # Creates line
                    # segments ('DRAWSEGMENT') from the individual strokes of text.
                    #
                    # 'object' here is a text object of type TEXTE_MODULE or TEXTE_PCB
                    #
                        
                    self.draw_vector(vector,
                        layer=USER_draw_outlines_layer,
                        thickness=USER_draw_stroke_thickness)

        # We are basically testing objects in padrects to objects in textrects
        # if there is a collision on a specific object, then we test that
        # object in padrects to the corresponding object in strokes.
        
        # the outer loop include the parallel objects to check
        # These are the objects on F.Cu -> F.Silk and B.Cu -> B.Silk in all
        # combinations.

        # Check text height, thickness, and aspect ratio
        for items in texts_to_check:
            for item in items:
                w = item.GetThickness()
                h = item.GetTextHeight()
                fail = False
                if w < USER_silk_minimum_width:
                    self._console_text_queue.put("Text at %s too narrow\n"%(str(item.GetCenter())))
                    fail = True
                if h < USER_text_minimum_height:
                    self._console_text_queue.put("Text at %s too short\n"%(str(item.GetCenter())))
                    fail = True
                # check w/h < 1/min
                # expressed as fail if W/H < 1/minW2H, or W*minW2H < H
                if (w * USER_text_minimum_WtoH) < h:
                    self._console_text_queue.put("Text at %s too tall for specified width\n"%(str(item.GetCenter())))
                    self._console_text_queue.put("Actual aspect = 1:%.2f (w*min)=%.1f; h=%d\n"%(float(h)/w,w*USER_text_minimum_WtoH,h))
                    
                    fail = True
                if fail:
                    item.SetSelected()
                    fail = False
        for items in graphicalitems_to_check:
            for item in items:
                try:
                    w = item.GetWidth()
                    #self._console_text_queue.put("Fail if  %s < %s\n"%(str(w),str(USER_silk_minimum_width)))
                    if w < USER_silk_minimum_width:
                        self._console_text_queue.put("Item at %s too narrow\n"%(str(item.GetCenter())))
                        item.SetSelected()
                except:
                    # self._console_text_queue.put("GetWidth failed for %s\n"%(str(item)))
                    pass
            
        # Check graphical item width
        
        failed=0
        checked=0
        #print "Back",len(pads_to_check[pcbnew.B_SilkS]),len(texts_to_check[pcbnew.B_SilkS])
        #BTextRect=[]
        layerindex = -1
        progress_count = 0
        # loop through the layer pairs
        for padrects, textrects in itertools.izip(padrect_to_check, textrect_to_check):
            layerindex += 1 # keep track of which layers (by index) are being compared

            self._console_text_queue.put( "Comparing layers: %s and %s\n"%(
                board.GetLayerName(silk_layer_list[layerindex]),
                board.GetLayerName(pad_layer_list[layerindex])))
            self._console_text_queue.put( "Pads: %d; Text Objects: %d\n"%(len(padrects),len(textrects)))
            for ipad,pad in enumerate(padrects):
                progress_count+=1
                self._progress_value_queue.put(progress_count)
                #self._console_text_queue.put("Progress = %d\n"%progress_count)

                for itext,text in enumerate(textrects):
                    checked+=1
                    flow = 'start '
                    # mindist = self.mindistance_polygon_polygon(text,pad)
                    # continue
                    #print str(pad),str(text)
                    #if self.RectangleIntersect(pad,text,0):
                    # Here, we proceed through four checks.
                    # 1) Do the bounding boxes intersect. If so, dist = 0
                    # 2) If not, dist = dist from bounding box to polygon pad
                    # 3) if dist < minimum, do any segments intersect? If so, dist=0
                    # 4) If not, find minimum distance of all segments to polygon pad.
                    mindist2 = 1000000000*1000000000 # 1m
                    if wxPointUtil.check_polygons_intersecting(pad,text):
                        # self.draw_polygon(pad)
                        # self.draw_polygon(text)
                        mindist2=0.0 # temporary value until we find segment distances
                        flow += '-> intersecting'
                    elif USER_slow_check:
                        mindist2 = (self.mindistance_polygon_polygon(text,pad) - texts_to_check[layerindex][itext].GetThickness()/2.0)**2.0
                        flow += '-> mindist2_pp'
                            
                    # if polygons are within mindistance, check all strokes for that text
                    #print mindist2, USER_minsilkpadspacing*USER_minsilkpadspacing
                    if mindist2 <= USER_minsilkpadspacing*USER_minsilkpadspacing: # and USER_slow_check:
                        mindist2 = 1000000000*1000000000 # 1m
                        flow += '-> mindist2 le minsilk'
                        #print "Checking strokes for ", itext,ipad
                        vectors = strokes_to_check[layerindex][itext]
                        intersect=False
                        #print len(vectors)
                        if USER_draw_outlines_thickness > 0:
                            self.draw_vector(vectors,layer=USER_draw_outlines_layer,thickness=USER_draw_outlines_thickness)
                            self.draw_polygon(pad,layer=USER_draw_outlines_layer,thickness=USER_draw_outlines_thickness)
                        for vindex in range(0,len(vectors)-1,2):                            
                            # does this stroke (vector[vindex]) intersect pad?
                            if wxPointUtil.check_polygons_intersecting((vectors[vindex],vectors[vindex+1]),pad,closed=False):
                                mindist2 = 0.0
                                flow += '-> stroke intersect'
                                break
                        
                        if USER_slow_check and mindist2 > USER_minsilkpadspacing*USER_minsilkpadspacing:
                            for vindex in range(0,len(vectors)-1,2):
                                #print vectors[vindex],vectors[vindex+1],pad
                                mindist2 = (self.mindistance_line_polygon((vectors[vindex],vectors[vindex+1]),pad) - texts_to_check[layerindex][itext].GetThickness()/2)**2.0
                                if mindist2 <= USER_minsilkpadspacing*USER_minsilkpadspacing:
                                    flow += '-> stroke dist<=min'
                                    break
                    if mindist2 <= USER_minsilkpadspacing*USER_minsilkpadspacing:
                        #self._console_text_queue.put("%d %d\n"%(mindist2,USER_minsilkpadspacing*USER_minsilkpadspacing))
                        pads_to_check[layerindex][ipad].SetSelected()
                        texts_to_check[layerindex][itext].SetSelected()
                        failed+=1
                        #print("%.3f %.3f %s %s %s"%(pad[0]/pcbnew.IU_PER_MM,pad[1]/pcbnew.IU_PER_MM,texts_to_check[pcbnew.B_SilkS][itext].GetText(),str(pads_by_layernum[pcbnew.B_SilkS][ipad].GetPosition()),str(pads_by_layernum[pcbnew.B_SilkS][ipad].GetBoundingBox().getWxRect())))
                    #self._console_text_queue.put('%s\n'%flow)
            # Check the drawings against this padrect
            #print graphicalitems_to_check[layerindex]
            for gi in graphicalitems_to_check[layerindex]:
                if not hasattr(gi,'GetShapeStr'):
                    continue
                if gi.GetShapeStr() != "Line":
                    self._console_text_queue.put("Shape '%s' at %s not checked.\n"%(gi.GetShapeStr(),str(gi.GetCenter())))
                    continue
                #self.draw_segment(gi.GetStart().x,gi.GetStart().y,gi.GetEnd().x,gi.GetEnd().y,layer=pcbnew.Eco2_User, thickness=0.02)
                #self._console_text_queue.put("width=%.3f mm\n"%(gi.GetWidth()/pcbnew.IU_PER_MM))
                for ipad,pad in enumerate(padrects):
                    # does this stroke (vector[vindex]) intersect pad?
                    mindist2 = (1000 * pcbnew.IU_PER_MM)*(1000 * pcbnew.IU_PER_MM)
                    #print gi
                    if not hasattr(gi,'GetShapeStr'):
                        continue
                    if gi.GetShapeStr() == "Line":
                        
                        try:
                            orientation = gi.GetDrawRotation() \
                                  - gi.GetOrientation()
                        except:
                            orientation = 0.0

                        #print gi.GetCenter(), orientation
                        #self.draw_segment(gi.GetStart().x,gi.GetStart().y,gi.GetEnd().x,gi.GetEnd().y,layer=pcbnew.Cmts_User, thickness=0.02*pcbnew.IU_PER_MM)

                        if wxPointUtil.check_polygons_intersecting(
                           (gi.GetStart(),gi.GetEnd()),pad,closed=False):
                            mindist2 = 0.0
                            # break
                            
                        elif USER_slow_check:
                            #for vindex in range(0,len(vectors)-1,2):
                            #print vectors[vindex],vectors[vindex+1],pad
                            # Width is the diameter, but we need to subtract the radius
                            mindist2 = (self.mindistance_line_polygon((gi.GetStart(),gi.GetEnd()),pad) - gi.GetWidth()/2.0)**2.0
                            #self._console_text_queue.put("%d %d\n"%(mindist2,gi.GetWidth()))
                            # if mindist2<= USER_minsilkpadspacing*USER_minsilkpadspacing:
                                # break
                    else:
                        self._console_text_queue.put("SHAPE '%s' at %s not checked.\n"%(gi.GetShapeStr(),str(gi.GetCenter())))
                        continue
                    #print gi.GetCenter(), mindist2
                    if mindist2 <= USER_minsilkpadspacing*USER_minsilkpadspacing:
                        pads_to_check[layerindex][ipad].SetSelected()
                        gi.SetSelected()
                        failed+=1

        self._console_text_queue.put("Checked: %d; Failed: %d\n"%(checked,failed))
        if failed > 0:
            self._console_text_queue.put("Objects failing check have been selected.\n")
            self._console_text_queue.put("You may need to switch views (F9, F11, F12) to see the newly-selected objects.\n")

        return

    def is_on_any_layer(self,object,layerlist):
        """returns true if object is on any layer in the iterable layerlist"""
        for layer in layerlist:
            if object.IsOnLayer(layer):
                return True
        return False
        
    def get_all_drawings_and_graphic_items(self,layerlist=None):
        items = [d for d in pcbnew.GetBoard().GetDrawings()]
        for m in pcbnew.GetBoard().GetModules():
            items.extend([g for g in m.GraphicalItems()])
        
        if layerlist is not None:
            items = filter(lambda x:self.is_on_any_layer(x,layerlist),items)

        return items
        
    def get_all_drawings_and_graphic_items_by_layer(self):
        return self.objects_by_layer(self.get_all_drawings_and_graphic_items())
        
    def GetAllDrawingsAndGraphicItemsByLayer(self):
        """DEPRECATED - Use get_all_drawings_and_graph_items_by_layer"""
        items = [d for d in pcbnew.GetBoard().GetDrawings()]
        for m in pcbnew.GetBoard().GetModules():
            items.extend([g for g in m.GraphicalItems()])
            
        itemsByLayer={}
        for i in items:
            for layernum in range(self.LAYERCOUNT):
                if i.IsOnLayer(layernum):
                    itemsByLayer.setdefault(layernum,[]).append(i)
        return itemsByLayer

    def draw_all_graphic_items(self):
        itemsByLayer = self.get_all_drawings_and_graphic_items_by_layer()
        silkdrawsegments = filter(lambda x: isinstance(x,pcbnew.DRAWSEGMENT),itemsByLayer[pcbnew.F_SilkS])
        for i in silkdrawsegments:
            self.draw_segment(i.GetStart().x,i.GetStart().y,i.GetEnd().x,i.GetEnd().y,layer=pcbnew.Eco1_User)
        #self.draw_segment(0,0,pcbnew.IU_PER_MM*100,pcbnew.IU_PER_MM*100,layer=pcbnew.Eco1_User)
        print [(pcbnew.GetBoard().GetLayerName(layer),len(itemsByLayer[layer])) for layer in itemsByLayer.keys()]
        print [i.GetShapeStr() for i in silkdrawsegments]

    def get_text_objects(self,layer=None):
        """Gets all the text objects, those on the main board and those within
           modules. If specified, the text objects are filtered to return only
           those text objects on the indicated layer."""
            
        Texts = []
        for drawing in pcbnew.GetBoard().GetDrawings():
            if isinstance(drawing,pcbnew.TEXTE_PCB):
                Texts.append(drawing)
        for module in pcbnew.GetBoard().GetModules():
            Texts.append(module.Value())
            Texts.append(module.Reference()) 
            for gi in module.GraphicalItems():
                if isinstance(gi,pcbnew.TEXTE_MODULE):
                    Texts.append(gi) 
        if layer is not None:
            Texts = filter(lambda x:x.IsOnLayer(layer),Texts)
        return Texts
        
    def text_stroke(self):
        """Draw all text object strokes on layer Eco2_User with thickness 0.075."""
        tobjects = self.get_text_objects()
        vectors = pcbnew.wxPoint_Vector(0)
        for t in tobjects:
            t.TransformTextShapeToSegmentList(vectors)
            for vindex in range(0,len(vectors)-1,2):
                # if vectors[vindex] == vectors[vindex+1]:
                    # vindex+=1
                    # continue
                self.draw_segment(vectors[vindex][0],vectors[vindex][1],
                    vectors[vindex+1][0],vectors[vindex+1][1],layer=pcbnew.Eco2_User,thicknessmm=0.075*pcbnew.IU_PER_MM)
            vectors.clear()
           

    def update_progress(self,count):
        """Updated the GUI progress bar to the indicated value.
        (Sleep an arbitrary amount of time (100ms) to allow GUI update."""
        self._progress.SetValue(count)
        # self._progress.Refresh()
        # self._progress.Update()
        wx.Yield()
        time.sleep(.1)
        return

    padHolesBySize = None
    WorkerThread = None
    def DrillInfo(self,e):
        """Main function for getting information about Drill Holes on the current board.
           And executes basic hole-related DRC checks.
           This is the parent function that instantiates and installs a separated
           workor thread (DrillInfo_Worker())"""
    # TODO: Clean up _progress_stop: change to CancelDrillWorker, provide for cancel.
        board = pcbnew.GetBoard()
        self._progress_stop = False
        if self.WorkerThread is not None and self.WorkerThread.is_alive():
            self.progress_thread_function(self.WorkerThreadself)
            self._progress.SetValue(0)
            return

        for t in board.GetTracks():
            t.ClearSelected()
            t.ClearHighlighted()
            t.ClearBrightened()
        
        self.padHolesBySize = self.GetPadHoles(); 
        self._vias = self.get_vias()
        
        self._progress.SetRange(2*len(self.padHolesBySize)+2*len(self._vias))

        self.WorkerThread = threading.Thread(
            target=self.DrillInfo_Worker, 
            name="WT", 
            args=(), 
            kwargs={})#, daemon=False)#, *, daemon=None)
        self.WorkerThread.start()
        self.progress_thread_function(self.WorkerThread)
        self.WorkerThread.join()
        self._progress.SetValue(0)
        
    def DrillInfo_Worker(self):
        """Function that does all the work of Drill Hole DRC as a background thread."""
        # this is run in a thread
        # use _console_text_queue and _progress_value_queue
        # to update the GUI
        
        board = pcbnew.GetBoard()

        MinimumViaVia = (self._frame.get_value_float('vv') or 0.0)
        MinimumViaTrack = (self._frame.get_value_float('vt') or 0.0)
                
        self._console_text_queue.put(
            "\n\n***** Quantity of holes by layer and size *****\n")
        self._console_text_queue.put("Layers: %s\n"%(str(self.get_holes_by_layer().keys())))
        
        self._console_text_queue.put("Testing holes near edge (only straight line edge cuts are checked!)\n")
        allholes = self.get_pad_holes_and_vias()
        edgecut_items = self.get_all_drawings_and_graphic_items(layerlist=(pcbnew.Edge_Cuts,))

        USER_drill_to_edge = (self._frame.get_value_float('dtoe') or 0.0)
        
        edgefail = 0
        
        for item in edgecut_items:
            if not isinstance(item,pcbnew.DRAWSEGMENT):
                continue
            if item.GetShapeStr() != "Line":
                self._console_text_queue.put("Shape '%s' at %s not checked.\n"%(item.GetShapeStr(),str(item.GetCenter())))

            for hole in allholes:
                try:
                    d = hole.GetDrillSize()
                except:
                    d = hole.GetDrillValue()
                    d = (d,d)
                if d[0] == 0.0 or d[1] == 0.0:
                    continue
                c = hole.GetCenter()
                dist = wxPointUtil.mindistance(c,item.GetStart(),item.GetEnd())
                if (dist - d[0]) <  USER_drill_to_edge:
                    self._console_text_queue.put("Hole at %s too close to edge\n"%(str(hole.GetCenter())))
                    hole.SetSelected()
                    item.SetSelected()
                    edgefail += 1

        if edgefail > 0:
            self._console_text_queue.put("Objects failing check have been selected.\n")
            self._console_text_queue.put("You may need to switch views (F9, F11, F12) to see the newly-selected objects.\n")

        allHolesByLayer = self.objects_by_layer(allholes)
        for layer, holelist in allHolesByLayer.iteritems():
            IsOrIsNot = []
            if pcbnew.IsCopperLayer(layer):
                IsOrIsNot.append("Copper")
            else:
                IsOrIsNot.append("not Copper")
            if pcbnew.IsNonCopperLayer(layer):
                IsOrIsNot.append("NonCopper")
            else:
                IsOrIsNot.append("not NonCopper")
            if pcbnew.IsUserLayer(layer):
                IsOrIsNot.append("User")
            else:
                IsOrIsNot.append("not User")
            if pcbnew.IsValidLayer(layer):
                IsOrIsNot.append("Valid")
            else:
                IsOrIsNot.append("not Valid")
            if pcbnew.IsPcbLayer(layer):
                IsOrIsNot.append("Pcb")
            else:
                IsOrIsNot.append("not Pcb")

            self._console_text_queue.put(
                "Layer %s (%s):\n"%(
                board.GetLayerName(layer),
                ', '.join(IsOrIsNot)))
            bysize = {}
            for hole in holelist:
                try:
                    d = hole.GetDrillSize()
                    #d = getattr(
                    #   hole,
                    #   "GetDrillSize",
                    #   getattr(hole,"GetDrillValue"))
                except:
                    d = hole.GetDrillValue()
                    d = (d,d)
                if d[0] == 0.0 or d[1] == 0.0:
                    continue
                bysize.setdefault((d[0],d[1]),[]).append(hole)
                
            areaorder = sorted(bysize.keys(),key=lambda x: x[0]*x[1])
            for size in areaorder:
                holelist = bysize[size]
                self._console_text_queue.put(
                    "Size %.3f,%.3f; "
                    "Quantity %d\n"%(
                    size[0]/pcbnew.IU_PER_MM,
                    size[1]/pcbnew.IU_PER_MM,
                    len(holelist)))
        self._console_text_queue.put("\n\n***** Check hole separation by layer *****\n")
        mindist = 1000*pcbnew.IU_PER_MM
        
        totalfails = 0
        for layer, holelist in self.get_holes_by_layer().iteritems():
            fails = 0
            for i in range(len(holelist)-2):
                sizei = self.get_drill_size(holelist[i])
                for j in range(i+1,len(holelist)-1):
                    sizej = self.get_drill_size(holelist[j])
                    dist2 = wxPointUtil.distance2(holelist[i].GetCenter(),holelist[j].GetCenter())
                    mindist = min(mindist,math.sqrt(dist2) - (max(sizei.x,sizei.y) + max(sizej.x,sizej.y))/2.0)
                    if mindist <= MinimumViaVia:
                        holelist[i].SetSelected()
                        holelist[j].SetSelected()
                        fails += 1
            totalfails += fails
            self._console_text_queue.put("Layer %s => %d errors:\n"%(board.GetLayerName(layer),fails))
            if fails > 0:
                self._console_text_queue.put("Objects failing check have been selected.\n")
                self._console_text_queue.put("You may need to switch views (F9, F11, F12) to see the newly-selected objects.\n")
                     
            
        count = 0
        self._progress_value_queue.put(count)
        #_console_text_queue.put("\n%s\n"%(str(count)))
        self._console_text_queue.put(
            "\n\n***** Quantity of Pads By Specified Drill Size, ordered by area *****\n")
        areaorder = sorted(self.padHolesBySize.keys(),key=lambda x:x[0]*x[1])
        for padsize in areaorder:
            padlist = self.padHolesBySize[padsize]
            count += 1
            self._progress_value_queue.put(count)
            #_console_text_queue.put(str(count))
            # time.sleep(1)
            # self._progress.Refresh()
            if padsize[0]==0 and padsize[1]==0:
                continue
            self._console_text_queue.put(
                "Size: %.3fmm, Quantity %s\n"%(
                padsize[0]/pcbnew.IU_PER_MM,len(padlist)))
        self._console_text_queue.put(
            "\n\n***** Quantity of Pads By Standard Drill Size, ordered by area *****\n")
        drillset = 0
        setname, scale, source = self._StandardDrillInfo[drillset]
        self._console_text_queue.put("%s from:\n%s\n\n"%(setname,source))
        drillmin = (self._frame.get_value_float('drillmin') or 0.0)
        drillmax = (self._frame.get_value_float('drillmax') or 1000*pcbnew.IU_PER_MM)
        areaorder = sorted(self.padHolesBySize.keys(),key=lambda x:x[0]*x[1])
        for padsize in areaorder:
            padlist = self.padHolesBySize[padsize]
            count += 1
            self._progress_value_queue.put(count)
            if padsize[0]==0 and padsize[1]==0:
                continue
            for dindex,dsize in enumerate(self._StandardDrill[drillset]):
                # drill sizes * scale are internal units
                standarddrillsize = dsize[0]*scale
                if standarddrillsize >= padsize[0]:
                    if not ( drillmin <= standarddrillsize <= drillmax ):
                        self._console_text_queue.put(
                        "Drill exceeds limits (%.3f mm<-> %.3f mm):\n"%(drillmin/pcbnew.IU_PER_MM,drillmax/pcbnew.IU_PER_MM) )
                    self._console_text_queue.put(
                       'Size: %.3fmm (%.1f mils), '
                       'Drill "%s": %.3fmm  (%.1f mils), '
                       'Quantity %s\n'%(
                       padsize[0]/pcbnew.IU_PER_MM,
                       padsize[0]/pcbnew.IU_PER_MILS,
                       self._StandardDrill[drillset][dindex][1],
                       standarddrillsize/pcbnew.IU_PER_MM,
                       standarddrillsize/pcbnew.IU_PER_MILS,
                       len(padlist)))
                    # padsize[0]*25.4/1000000.0
                    break

        # for via in self._vias:
            # via.SetDrill(int(0.294*1000000.0))
            
        self._console_text_queue.put(
            "\n\n***** Via Holes List "
            "(pad #, position (nm), "
            "Type, Drill, Drill Value, Via Width) *****\n")
        vias_details = []
        for index,v in enumerate(self._vias):
            count += 1
            self._progress_value_queue.put(count)
            p=v.GetPosition()
            t=v.GetViaType()
            d=v.GetDrill()
            dv=v.GetDrillValue()
            w=v.GetWidth()
            self._console_text_queue.put(
                "%d (Type %d) Pos=%.3f mm, "
                "%.3f mm; Drill=%.3f mm; "
                "DrillValue=%.3f mm; "
                "Pad Width=%.3f mm\n"%
                (index,t,p[0]/pcbnew.IU_PER_MM,p[1]/pcbnew.IU_PER_MM,
                d/pcbnew.IU_PER_MM,dv/pcbnew.IU_PER_MM,w/pcbnew.IU_PER_MM))
            vias_details.append((p[0],p[1],dv,w))
        num = len(vias_details)
        distmin = num*[1000000000]
        for i in range(num):
            for j in range(i+1,num):
                dist2 = (
                    ((vias_details[i][0]-vias_details[j][0])*
                    (vias_details[i][0]-vias_details[j][0]))+
                    ((vias_details[i][1]-vias_details[j][1])
                    *(vias_details[i][1]-vias_details[j][1]))
                    )
                dist = (dist2**(1/2.0)) \
                    - vias_details[i][2]/2.0 \
                    - vias_details[j][2]/2.0
                if dist < distmin[i]:
                    distmin[i] = dist
        FailedVias = []
        FailedViaTracks = set()
        FailedTracks = set()
        self._console_text_queue.put(
            "\n\n***** Distance to next closest via  ***** "
            "(looking only *forward* through the list)\n")
        self._console_text_queue.put(
            "Minimum Via to Via = %.3f mils (%.3f mm)\n\n"
            %(MinimumViaVia/pcbnew.IU_PER_MILS,MinimumViaVia/pcbnew.IU_PER_MM))
        for i,dist in enumerate(distmin):
            self._console_text_queue.put("%d %.3f mm\n"%(i,dist/1000000.0))
            if dist<MinimumViaVia:
                FailedVias.append(i)
                self._vias[i].SetHighlighted()
        if len(FailedVias) > 0:
            self._console_text_queue.put(
                "\n\n***** Vias too close to another via *****\n")
        for via in FailedVias:
            self._console_text_queue.put("%d\n"%via)
        
        # test for self._vias proximity to track segments
        for vindex,via in enumerate(self._vias):
            count += 1
            self._progress_value_queue.put(count)
            for track in board.GetTracks():
                if isinstance(track,pcbnew.VIA): # is a via, skip
                    continue
                # Check if via and track are the same net. If so, skip
                if via.GetNetname() == track.GetNetname():
                    continue
                v = via.GetPosition()
                d = via.GetDrillValue()
                # if RectangleIntersect(
                #     (v[0],v[1],d,d),
                #     track.GetBoundingBox().getWxRect(),0):
                #     continue
                s = track.GetStart()
                e = track.GetEnd()
                #v = via.GetPosition()
                s = pcbnew.wxPoint(s[0],s[1])
                e = pcbnew.wxPoint(e[0],e[1])
                v = pcbnew.wxPoint(v[0],v[1])
                #print "point=",v,'start=', s,'end=',e,'length=',e.distance(s)
                dist = wxPointUtil.mindistance(v,s,e)
                if dist == 0.0:
                    continue
                DIST = dist
                dist = dist - (track.GetWidth() + d)/2.0
                DISTREDUCED = dist
                if (abs(dist) > 1000) and (dist < MinimumViaTrack):
                    if dist < 0:
                        track.SetSelected()
                        via.SetSelected()
                        #print v,s,e
                        #print "dist %d; reduced dist %d\n" \
                        #    %(DIST,DISTREDUCED),SavePrint
                    FailedViaTracks.add(
                        (vindex,
                            "Via (%s) at %s is %d away from track (%s) (%s ; %s)."
                            "Shoud be %d"%
                            (via.GetNetname(),
                            str(v),
                            dist,
                            track.GetNetname(),
                            str(s),
                            str(e),
                            MinimumViaTrack)))
                    FailedTracks.add(track)
        for track in FailedTracks:
            track.SetSelected()
        if len(FailedViaTracks) > 0:
            self._console_text_queue.put("\n\n***** Vias too close to track *****\n")
        for via,message in FailedViaTracks:
            self._console_text_queue.put("%d %s\n"%(via,message))
            
        if (len(FailedViaTracks) > 0) or (len(FailedTracks) > 0) or (len(FailedVias) > 0):
            self._console_text_queue.put("Objects failing check have been selected.\n")
            self._console_text_queue.put("You may need to switch views (F9, F11, F12) to see the newly-selected objects.\n")

        self._console_text_queue.put("\n  ***** DONE *****\n")	
        self._progress_stop = True


    def GetApertureSize(self,pad):
        """Return the aperture (Paste) size of the given pad object as a tuple (w,h)."""
        Size = pad.GetSize()
        margin = pad.GetSolderPasteMargin()
        sizex = Size[0] + margin[0]
        sizey = Size[1] + margin[1]
        return (sizex,sizey)
        
    def GetMaskSize(self,pad):
        """Return the (solder) Mask size of the given pad object as a tuple (w,h)."""
        Size = pad.GetSize()
        margin = pad.GetSolderMaskMargin()
        sizex = Size[0] + margin
        sizey = Size[1] + margin
        return (sizex,sizey)

        
    def StencilInfo(self,e):
        """Main function for getting information about Paste Layers on the current board.
           And calculates parameters useful for creating stencils including:
           (aperture ratio, area ratio, solder paste type/size)."""
        board = pcbnew.GetBoard()
           
        FailedAreaRatio = {}
        FailedAspectRatio = {}
        PadLayerNames, PadLayers = self.GetPadLayerNameNum()
        # get only pads on F.Paste layer
        padnums = [padnum for padnum in range(board.GetPadCount()) \
            if board.GetPad(padnum).IsOnLayer(self._layer_num_by_name["F.Paste"])]
        AreaRange = {}
        AspectRange = {}
        AperturesBySize = {}
        stencilSizes = self.GetStencilSizes(padnums)
        AreaRatio = {}
        AspectRatio = {}
        for Size,padlist in stencilSizes.iteritems():
            #_consoleText.AppendText("Size: %s, Number %s\n"%(padsize,len(padlist)))
            #_consoleText.AppendText("Size = %s\n"%str(Size))
            W=min(Size[0],Size[1])
            L=max(Size[0],Size[1])
            Tlist = (2,3,4,5,6,7)
            # aspect 1.5
            # area .66
            for Tmil in Tlist:
                T=(1000000/1000)*25.4*Tmil # 0.12 = 4.7mil or 0.15 = 6 mil
                AreaRatio.setdefault(Size,[]).append((L*W)/(2.0*(L+W)*T))
                AspectRatio.setdefault(Size,[]).append(float(W)/T)
                AreaRange.setdefault(Tmil,[1000000,0]) 
                AspectRange.setdefault(Tmil,[1000000,0]) 
                AreaRange[Tmil][0] = min(AreaRange[Tmil][0],AreaRatio[Size][-1])
                AreaRange[Tmil][1] = max(AreaRange[Tmil][1],AreaRatio[Size][-1])
                AspectRange[Tmil][0] = min(AspectRange[Tmil][0],
                                           AspectRatio[Size][-1])
                AspectRange[Tmil][1] = max(AspectRange[Tmil][1],
                                           AspectRatio[Size][-1])
                #_consoleText.AppendText("%s\n"%str(AreaRange))
                if (AreaRatio[Size][-1] < 0.66):
                    FailedAreaRatio.setdefault(Tmil,[]).append(Size)
                if (AspectRatio[Size][-1] < 1.5):
                    FailedAspectRatio.setdefault(Tmil,[]).append(Size)
                # AspectRatio W is always lower than AspectRatioL
                # AspectRatioL = float(L)/T
            AperturesBySize[Size] = (AreaRatio[Size][-1],AspectRatio[Size][-1],W,L)
            # Desired: AreaRatio > 0.66 and AspectRatio > 1.5
            #if (AreaRatio < 0.66) or (AspectRatio<1.5):
            # _consoleText.AppendText("(qty %d)\tP=%.3f,%.3f;"
            #     "A=%.3f,%.3f"%(
            #     len(padlist),Size[0],Size[1],W/1000000.0,L/1000000.0))
            # for index, Tmil in enumerate(Tlist):
                # _consoleText.AppendText(" (%.1f %.2f %.2f)"%(
                    # Tmil,AreaRatio[Size][index],AspectRatio[Size][index]))
            # _consoleText.AppendText("\n")
        self._consoleText.AppendText(
            "\n***** Pads by Stencil Aperture (Paste Aperture) Ratio *****\n")
        for Size in sorted(AperturesBySize, key=lambda k: AperturesBySize[k][0]):
        #_consoleText.AppendText("AR=%s; AS=%s\n"%(str(AreaRatio),str(AspectRatio)))
        #for Size in sorted(AperturesBySize, key=itemgetter(1)):
            #_consoleText.AppendText("AR=%s; AS=%s\n"%(str(AreaRatio[Size]),str(AspectRatio[Size])))
            padlist = stencilSizes[Size]
            W = AperturesBySize[Size][2]
            L = AperturesBySize[Size][3]
            self._consoleText.AppendText("(qty %d)\tAperture=%.3f,%.3f"%(len(padlist),#Size[0]/1000000.0,Size[1]/1000000.0,
            W/1000000.0,L/1000000.0))
            for index, Tmil in enumerate(Tlist):
                self._consoleText.AppendText(" (%.1f %.2f %.2f)"%(
                    Tmil,AreaRatio[Size][index],AspectRatio[Size][index]))
            self._consoleText.AppendText("\n")
            footprints = set()
            for padnum in padlist:
                p = board.GetPad(padnum)
                footprints.add(p.GetParent().GetValue())
            self._consoleText.AppendText("\tPads: %s\n"%str(padlist))
            self._consoleText.AppendText("\tFrom: %s\n"%','.join(footprints))
            
        self._consoleText.AppendText("\n***** Aperture Ratio Ranges *****\n")
        for Tmil in sorted(AspectRange.keys()):
            text = "%.1f mil Aspect: %.3f %.3f\t Area  : %.3f %.3f\n"%(
                   Tmil,AspectRange[Tmil][0],AspectRange[Tmil][1],
                   AreaRange[Tmil][0],AreaRange[Tmil][1])
            self._consoleText.AppendText(text)
        
        FailedMil = set([Tmil for Tmil in FailedAreaRatio.keys()])
        FailedMil.update([Tmil for Tmil in FailedAspectRatio.keys()])
        if len(FailedMil) > 0:
            self._consoleText.AppendText("\n***** Failed Aperture Test *****\n")
        #_consoleText.AppendText(
        #    "%s\n%s\n"%(str(FailedAreaRatio),str(FailedAspectRatio)))
        for Tmil in sorted(FailedMil):
            self._consoleText.AppendText("Failed %.1f mil thickness:\n"%Tmil)
            for Size in FailedAreaRatio.get(Tmil,[]):
                self._consoleText.AppendText(
                    "\tFailed Area  : %.3f %.3f\n"%
                    (Size[0]/1000000.0,Size[1]/1000000.0))
            for Size in FailedAspectRatio.get(Tmil,[]):
                self._consoleText.AppendText(
                    "\tFailed Aspect: %.3f %.3f\n"%
                    (Size[0]/1000000.0,Size[1]/1000000.0))
        #_consoleText.AppendText("%s\n"%str(AperturesBySize))
        
        mu = unichr(0x03BC)
        self._consoleText.AppendText(
            "\n***** Max aperture size (%cm) by Solder Powder Size *****\n"%mu)
        for type,sizerange in self.PowderSizeRangeByType_um.iteritems():
            self._consoleText.AppendText(
                "Type %.1f; Range (%cm): %d %d; "
                "Min Aperture: %d %cm (%.3f mil)\n"%
                (type,mu,sizerange[0],sizerange[1],sizerange[1]*5,
                mu,(sizerange[1]*5)/25.4))
        self._consoleText.AppendText("\n  ***** DONE *****\n")	
        
    #@deprecated
    def StencilInfo_old(self):
        """DEPRECATED"""
        board = pcbnew.GetBoard()
        PadsByLayer = {}
        for padnum, layers in PadLayers.iteritems():
            for layer in layers:
                PadsByLayer.setdefault(layer,[]).append(padnum)
        # http://www.circuitinsight.com/programs/50456.html
        # We have converted IPC 7525 for stencil thickness determination into a
        # regression equation. Stencil Thickness = 2.64 + 0.0831 * pitch of
        # component. 
        # Take average of all stencil thickness derived for all components,
        # if min. to max. difference is more than 2mil, consider a
        # step-up/step-down stencil in selective locations. 

        # https://git.launchpad.net/kicad/tree/pcbnew/class_pad_draw_functions.cpp
        # Mask Margin effect per shape:
        # Circle => radius = (sise/2)-margin.x
        # Oval => 
                # seg_width = BuildSegmentFromOvalShape(segStart, segEnd, angle,
                # aDrawInfo.m_Mask_margin);
                # segStart += shape_pos;
                # segEnd += shape_pos;

                # if( aDrawInfo.m_ShowPadFilled )
                # {
                # GRFillCSegm( aClipBox, aDC,
                #     segStart.x, segStart.y, segEnd.x, segEnd.y,
                #     seg_width, aDrawInfo.m_Color );
        # RECTANGLE or TRAPEZOID =>
        # BuildPadPolygon( coord, aDrawInfo.m_Mask_margin, angle );
        # ROUNDED_RECT =>
        # size += aDrawInfo.m_Mask_margin * 2;
        # int corner_radius = GetRoundRectCornerRadius( size );

        # Margin Handling is also in:
        #    https://git.launchpad.net/kicad/tree/pcbnew/class_pad.cpp
        # Logic from source code 6/16/2017
        # get the final margin number (if local=0, get parent, etc.)
        # pad.GetSolderPasteMargin() 
        # margin.x = margin + (size.x * ratio)
        # margin.y = margin + (size.y * ratio)
        
        _consoleText.AppendText("W,L,AreaRatio,AspectRatioW,AspectRatioL\n")
        for padnum in PadsByLayer[self._layer_num_by_name["F.Paste"]]:
            pad = board.GetPad(padnum)
            Size = pad.GetSize()
            # get the final margin number (if local=0, get parent, etc.)
            #pad.GetSolderPasteMargin()
            # margin.x = margin + (size.x * ratio)
            # margin.y = margin + (size.y * ratio)
            margin = pad.GetSolderPasteMargin()
            sizex = Size[0] + margin[0]
            sizey = Size[1] + margin[1]
            W=min(sizex,sizey)
            L=max(sizex,sizey)
            T=25.4*4/1000.0 # 0.12 = 4.7mil or 0.15 = 6 mil
            AreaRatio = (L*W)/(2.0*(L+W)*T)
            AspectRatioW = float(W)/T
            AspectRatioL = float(L)/T
            # Desired: AreaRatio > 0.66 and AspectRatio > 1.5
            #if (AreaRatio < 0.66) or (AspectRatioW<1.5):
            self._consoleText.AppendText(
                "%d %d %f %f %f\n"%(W,L,AreaRatio,AspectRatioW,AspectRatioL))
            #print("%d %d %f %f %f\n"%(W,L,AreaRatio,AspectRatioW,AspectRatioL))

        
    def FindWindowByTitle(self,title,startwindow=None):
        """UI convenience function to find the GUI window by its title.
           If startwindow is unspecified, search from the top level windows."""
        if startwindow is None:
            startwindow = wx.GetTopLevelWindows()
        window = filter(lambda w: w.GetTitle().startswith(title), startwindow)
        if len(window) != 1:
            raise Exception("Cannot find %s window from title."%title)        
        return window[0]

    def FindWindowByName(self,name,startwindow=None):
        """UI convenience function to find the GUI window by its name.
           If startwindow is unspecified, search from the top level windows."""
        if startwindow is None:
            startwindow = wx.GetTopLevelWindows()
        window = filter(lambda w: w.Name.startswith(name), startwindow)
        if len(window) != 1:
            raise Exception("Cannot find %s window from name."%name)
        return window[0]

        #point and line" calculation (if the distances are all the same, then the lines are parallel).

    def mindistance_line_polygon(self,line,polygon):
        """Return the minimum distance between the specified line and polygon.
           Polygon is a list of wxPoint vertices"""
        return math.sqrt(self.mindistance2_line_polygon(line,polygon))

    def mindistance2_line_polygon(self,line,polygon):
        """Return the minimum distance between the specified line and polygon.
           Polygon is a list of wxPoint vertices"""
        # loop through each polygon edge
        #for i in range(0,len(polygon)-1,2):

        # last polygon vertex to line
        min2 = wxPointUtil.mindistance2(polygon[-1],line[0],line[1])
        #print min2, line[0], line[1]
        for i in range(len(polygon)-1):
            # loop through each end point to opposite line
            
            # first line point to polygon edge
            min2 = min(min2,wxPointUtil.mindistance2(line[0],polygon[i],polygon[i+1]))
            #print min2, wxPointUtil.mindistance2(line[0],polygon[i],polygon[i+1])
            # second line point to polygon edge
            min2 = min(min2,wxPointUtil.mindistance2(line[1],polygon[i],polygon[i+1]))
            #print min2, wxPointUtil.mindistance2(line[1],polygon[i],polygon[i+1])
            # first polygon vertex to line (second one will be next loop)
            min2 = min(min2,wxPointUtil.mindistance2(polygon[i],line[0],line[1]))
            #print min2, wxPointUtil.mindistance2(polygon[i],line[0],line[1])
        return min2
        
    def mindistance_polygon_polygon(self,polygon1,polygon2):
        """Return the minimum distance between the specified polygons.
           Each polygon is a list of wxPoint vertices"""
        return math.sqrt(self.mindistance2_polygon_polygon(polygon1,polygon2))

    def mindistance2_polygon_polygon(self,polygon1,polygon2):
        """Return the minimum distance between the specified polygons.
           Each polygon is a list of wxPoint vertices"""
        # This doesn't consider the case where polygon is contained in another
        # loop through each polygon1 edge
        min2=wxPointUtil.mindistance2(polygon1[0], polygon2[0], polygon2[1])
        for i in range(len(polygon1)):
            p1a = polygon1[i]
            p1b = polygon1[(i+1)%len(polygon1)]
            #polygon1_edge = (polygon1[i], polygon1[(i+1)%len(polygon1)])
            for j in range(len(polygon2)):
                p2a = polygon2[j]
                p2b = polygon2[(j+1)%len(polygon2)]
                #polygon2_edge = (polygon2[j], polygon2[(j+1)%len(polygon2)])
                
                # loop through each end point to opposite line
                min2 = min(min2,wxPointUtil.mindistance2(p1a,p2a,p2b))
                min2 = min(min2,wxPointUtil.mindistance2(p1b,p2a,p2b))
                min2 = min(min2,wxPointUtil.mindistance2(p2a,p1a,p1b))
                min2 = min(min2,wxPointUtil.mindistance2(p2b,p1a,p1b))
        return min2

# The following code is by Randolph Franklin, it returns 1 for interior points and 0 for exterior points.

    # int pnpoly(int npol, float *xp, float *yp, float x, float y)
    # {
      # int i, j, c = 0;
      # for (i = 0, j = npol-1; i < npol; j = i++) {
        # if ((((yp[i] <= y) && (y < yp[j])) ||
             # ((yp[j] <= y) && (y < yp[i]))) &&
            # (x < (xp[j] - xp[i]) * (y - yp[i]) / (yp[j] - yp[i]) + xp[i]))
          # c = !c;
      # }
      # return c;
    # }

    
kpc=None
def Run():
    """The main function to run when imported. Creates the menu
       and a variety of variables pointing to the graphic windows needed
       later in the code."""
    global kpc
    kpc = KiPadCheck()
    MenuItemName = "KiPadCheck"
    kpc._pcbnewWindow = kpc.FindWindowByTitle("Pcbnew")
    kpc._consoleText = kpc.FindWindowByName("text",
        startwindow=kpc.FindWindowByName("KicadFrame").GetChildren())
    kpc._consoleText.AppendText("Starting Run()...\n")
    
    menuBar = kpc._pcbnewWindow.MenuBar
    # add the menu item under Tools menu
    toolsMenu = menuBar.GetMenu(menuBar.FindMenu("Tools"))
    #existingItem = menuBar.FindMenuItem("Tools",MenuItemName)
    existingItem = toolsMenu.FindItem(MenuItemName)
    if existingItem != -1:
        kpc._consoleText.AppendText("Deleting existing menuitem.\n")
        toolsMenu.Delete(existingItem)
    MenuItem = toolsMenu.Append(wx.ID_ANY, MenuItemName)
    kpc._pcbnewWindow.Bind(wx.EVT_MENU, kpc.MenuItemPadInfo, MenuItem)
    # _id = wx.NewId()
    # subMenuObject.Append(_id, title, statustext)
    # wx.EVT_MENU(self, _id, action)
    kpc._consoleText.AppendText("Finished Run()\n")

# invoke only when run as a script, not as import
if __name__ == "__main__":
    Run()
else:
    # The above should work (currently untested) with Action Menu
    # (KiCAD compiled with KICAD_SCRIPTING_ACTION_MENU)
    # However, in KiCAD builds without ACTION_MENU enabled, the following
    # is a workaround that allows "import kipadcheck" to enable the menu item.
    Run()

# register through Action Script when imported
kpc.register()