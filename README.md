kipadcheck.py
Original Author: Greg Smith, June-August 2017

Naming conventions (from PEP8):
Short python naming guide (from PEP8):

ClassName
function_name
function_parameter
parameter_disambiguation_
variable_name
_nonpublic_function
_nonpublic_global_variable
CONSTANT_VALUE_NAME

This is beta. Not thoroughly tested.

Inputs and outputs are in varying non-changable units (mils, inches, mm, nm)
Only tested on KiCAD 4.06, Windows 7.

Install: In Windows, place file in 
C:\Program Files\KiCad\share\kicad\scripting\plugins\kipadcheck.py
In pcbnew, open scripting console (Tools > Scripting Console)
Type "import kipadcheck".

ABOUT:
   This python script provides additional basic DRC checks to KiCAD
   and lists to make tweaking pads for stencil creation easier.
   It adds a menu item to "Tools" called kipadcheck.

THERE ARE BUGS:

Preliminary support is included for more than 2 layers.
Pads are not verified for shape, currently assumes rectangle bounding box.
Assumes all pads are on the front.
Does not mix via drill and pad drill checks.
Does not check annular ring size.

TODO list, aside from fixing the BUGS above.
  Support all layers for all checks. Currently SilkInfo does check layers
     appropriately: F.Cu vs. F.SilkS and B.Cu vs. B.SilkS
	Support more than just through drills (i.e. buried/blind self._vias).
  Label units and make consistent.
  Mask Info: Check solder mask dam sizes.
  Silk Info: Check silk screen character sizes.
  Check Annular Rings.
  Update progress bar when doing SilkInfo

Pad Info: Produces two lists: 
  1) detailed list of pads by footprint reference with paste/mask properties
  2) quantity of pads by size
Drill Info: Generates multiple lists:
  1) Hole quantity by specified pad drill sizes
  2) Quantity by closest larger standard drill size
     (future option will be to pick among defined drill sets)     
  3) Drill list
  4) Distance from each via to next closest via
  5) Checks via drill to via drill clearance
  6) Checks via drill to track clearance
Stencil Info:
  1) Lists quantity of apertures by aperture size
  2) Summary of aperture ratios by stencil thickness
  3) Checks AspectRatio and AreaRatio against a variety 
     of stencil thicknesses (2 mil-7 mil, all currently hardcoded)
  4) Lists solder paste sizes for calculating appropriate.
SilkInfo has several options:
  1) Fast check of silkscreen bounding boxes and line segments.
  2) Slower check includes line thicknesses.

EXAMPLES:

Pad Info: Produces two lists: 
  1) detailed list of pads by footprint reference with paste/mask properties
     Number of pads: 293

     ***** Pads By Footprint Reference, Alphabetical *****
     # 4	(BT1.) X=113.665086 Y=147.423648 P=CIRC (2.64, 2.64) D=CIRC
     (2.64, 2.64) Layers=F.Cu,B.Cu,B.Mask,F.Mask lc=0.0000 c=0.1530
     Paste: spm=0.0000,0.0000 lspm=0.0000 lspmr=0.0000
     | Mask : smm=0.0000 lsmm=0.0000
     ...
  2) quantity of pads by size
     ***** Quantity of Pads By Size *****
     Size: 0.900 0.900, Quantity 4
     Size: 0.875 1.250, Quantity 2
     Size: 0.800 1.200, Quantity 2
     Size: 0.900 1.700, Quantity 1
     Size: 0.300 0.800, Quantity 24
     ...

Drill Info: Generates multiple lists:
  1) Hole quantity by specified pad drill sizes
     ***** Quantity of Pads By Specified Drill Size *****
     Size: 1.020mm, Quantity 2
     Size: 4.826mm, Quantity 6
     Size: 1.000mm, Quantity 54
     Size: 2.640mm, Quantity 2
     Size: 1.097mm, Quantity 8

  2) Hole quantity by closest larger standard drill size
     (future option will be to pick among defined drill sets)     
     ***** Quantity of Pads By Standard Drill Size *****
     Size: 1.020mm (25.908in), Drill: 0.041 (59), Quantity 2
     Size: 4.826mm (122.580in), Drill: 0.191 (11), Quantity 6
     Size: 1.000mm (25.400in), Drill: 0.04 (60), Quantity 54
     Size: 2.640mm (67.056in), Drill: 0.104 (37), Quantity 2
     Size: 1.097mm (27.871in), Drill: 0.0465 (56), Quantity 8

  3) Drill list
     ***** Drill Holes List
    (pad #, position (nm), Type, Drill, Drill Value, Via Width) *****
     0 (152661291, 138048648) 3 294000 294000 600000
     1 (113725000, 140800000) 3 294000 294000 600000
     ...

  4) Distance from each via to next closest via
     ***** Distance to next closest via  *****
     (looking only *forward* through the list)

     Minimum Via to Via = 20.000 mils (0.508 mm)
     0 3.692 mm
     1 1.205 mm
     ...

  5) Checks via drill to via drill clearance
     ***** Vias too close to another via *****
     29
     44
     ...

  6) Checks via drill to track clearance
     ***** Vias too close to track *****
     31 Via (/IOC_RB6) at (125934690, 138137006) is 306005 away from track
	(/IOC_RB5)
	((126280790, 137531001) ; (125660499, 137531001)). Shoud be 508000
     23 Via (/GND) at (150540086, 141423648) is 307472 away from track (/RE2)
	((149487558, 140816176) ; (152110941, 140816176)). Shoud be 508000
     ...


Stencil Info:
  1) Lists quantity of apertures by aperture size:
     (Aperture in mm, triplets of:
      stencil mil thickness, area ratio, aspect ratio)
     (qty 24)	Aperture=0.225,0.725 (2.0 1.69 4.43) (3.0 1.13 2.95)
	(4.0 0.85 2.21) (5.0 0.68 1.77) (6.0 0.56 1.48) (7.0 0.48 1.27)
	      Pads: [20, 45, 80, 98, 99, 100, 101, 109, 113, 121, 125, 140,
	143, 165, 205, 208, 209, 210, 233, 234, 238, 239, 241, 244]
	From: CONN_01X24
     ...

  2) Summary of aperture ratios by stencil thickness
      ***** Aperture Ratio Ranges *****
      2.0 mil Aspect: 4.429 14.764	 Area  : 1.471 4.318
      3.0 mil Aspect: 2.953 9.843	 Area  : 0.981 2.879
      4.0 mil Aspect: 2.215 7.382	 Area  : 0.735 2.159
      5.0 mil Aspect: 1.772 5.906	 Area  : 0.588 1.727
      6.0 mil Aspect: 1.476 4.921	 Area  : 0.490 1.439
      7.0 mil Aspect: 1.265 4.218	 Area  : 0.420 1.234

  3) Checks AspectRatio and AreaRatio against a variety 
     of stencil thicknesses (2 mil-7 mil, all currently hardcoded):
      ***** Failed Aperture Test *****
      Failed 5.0 mil thickness:
	Failed Area  : 0.445 0.225
	Failed Area  : 0.300 0.350
      Failed 6.0 mil thickness:
	Failed Area  : 0.555 0.245
	Failed Area  : 0.445 0.225
	Failed Area  : 0.300 0.350
	Failed Area  : 0.225 0.725
	Failed Aspect: 0.445 0.225
	Failed Aspect: 0.225 0.725
      Failed 7.0 mil thickness:
	Failed Area  : 0.555 0.245
	Failed Area  : 0.325 0.725
	Failed Area  : 0.445 0.225
	Failed Area  : 0.300 0.350
	Failed Area  : 0.225 0.725
	Failed Aspect: 0.555 0.245
	Failed Aspect: 0.445 0.225
	Failed Aspect: 0.225 0.725


Nevertheless, there are some examples of using python code to interact
with KiCAD:
   Install Tools menu, replace if already existing
      (allows reloading python file after changes)
   Iterate over tracks, identify self._vias, get sizes of
   via and pad copper, mask, and paste
   Identify which layers a pad is on.
   Generate basic interactive window.
   Display  multi-threaded wx.Gauge (self._progress bar).
   Get Paste (stencil) Aperture size calculated from pad properties.
