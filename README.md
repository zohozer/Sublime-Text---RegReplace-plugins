# Sublime-Text---RegReplace-plugins
Some useful plugins for the [Sublime Text](https://www.sublimetext.com) and his [RegReplace](https://github.com/facelessuser/RegReplace) package.

I do created two plugins, each plugin with two variants: One called (standalone) for Sublime Text and another version that do the same thing but integrated into RegReplace package.

1. Summarize Tools used in Gcode.
- This plugin will write in the header of the Gcode file the Tools used into the file like a summary of used tools
- Here is a samplle of what it does. In the bellow G-code file will insert the "; Tools: 0, 102, 103;" after the line ";Part#-123" because it detect that on the entire file that are the tools used, so basically creates a quick summary of the used tools in the G-code file:

```
H DX=10.5 DY=6.5 -A C=0 T=0 R=99 *IN /"DEF" BX=-.25 BY=-.25 BZ=0 ;PGM:ARCHCUT
;Part -ABC
;Part#-123
; TimeNowHere
;
;#60-052 DOWN SPRIAL 1/2" CHIPBREAKER
XG0 X=-.25 Y=-1 Z=.1 E=0 V=100 S=10000 D=0 T=102 F=1 C=0
G1 X=-.25 Y=-1 Z=-.05 E=0 V=200
G1 X=-.25 Y=1.5 E=0 V=200
G1 X=-.25 Y=4.5 E=0 V=200
G1 X=-.25 Y=7 E=0 V=200
;
;#60-052 DOWN SPRIAL 1/2" CHIPBREAKER
XG0 X=10.25 Y=7 Z=.1 E=0 V=100 S=10000 D=0 T=102 F=1 C=0
G1 X=10.25 Y=7 Z=-.05 E=0 V=300
G1 X=10.25 Y=-1 E=0 V=300
;
;#60-052 DOWN SPRIAL 1/2" CHIPBREAKER
XG0 X=-1 Y=6.25 Z=.1 E=0 V=100 S=10000 D=0 T=103 F=1 C=0
G1 X=-1 Y=6.25 Z=-.05 E=0 V=200
G1 X=11 Y=6.25 E=0 V=200
;
;#60-052 DOWN SPRIAL 1/2" CHIPBREAKER
XG0 X=11 Y=-.25 Z=.1 E=0 V=100 S=10000 D=0 T=102 F=1 C=0
G1 X=11 Y=-.25 Z=-.05 E=0 V=200
G1 X=-1 Y=-.25 E=0 V=200
;
;#60-052 DOWN SPRIAL 1/2" CHIPBREAKER
XG0 X=-1.0176 Y=1.75 Z=.1 E=0 V=100 S=10000 D=0 T=102 F=1 C=0
G1 X=-1.0176 Y=1.75 Z=-.05 E=0 V=200
G1 X=0 Y=1.75 E=0 V=200
G3 X=1.25 Y=3 I=0. J=3. E=0 V=200
G3 X=0 Y=4.25 I=0. J=3. E=0 V=200
G1 X=-1.0176 Y=4.25 E=0 V=200
N X=0 Y=0 V=100000
```

2. Replace the TimeNowHere occurencies with the actual date and Time of the computer.
- Finds all occurencies of the "TimeNowHere" in the file
- Replaces them with the actual Date/Time in this form: Saturday 2025/04/12 (09:42:27)

After using this tools the file should look like this:

```
H DX=10.5 DY=6.5 -A C=0 T=0 R=99 *IN /"DEF" BX=-.25 BY=-.25 BZ=0 ;PGM:ARCHCUT
;Part -ABC
;Part#-123
; Tools: 0, 102, 103;
; Saturday 2025/04/12 (09:42:27)
;
;#60-052 DOWN SPRIAL 1/2" CHIPBREAKER
XG0 X=-.25 Y=-1 Z=.1 E=0 V=100 S=10000 D=0 T=102 F=1 C=0
 . . . . . . . . . .
etc.
```
