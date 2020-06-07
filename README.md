# FaceTouch
This is a TECO-seminar project.
## Annotation with Anvil
This is a quick guide for annotation (labeling) video with anvil.

### General 

shortcut: f1 to start (green line) and f2 to end (red line) for creating a annotation, f3 to direct edit the annotation.

### Guideline
1. Open the video that should be annotated, change the sepcification in annotation properties to the path of touch-spec-keys.xml
2. Click at the wished start point in timeline and press f1, click at the whished stop point press hotkeys (s=start,l=lefthand,r=righthand,b=bothhands) to create an annotation. Make sure the block is selected(pink shadow).
3. If once changed the spec file, remember to click the 3rd icon to reload the xml and click the 4th icon to refresh the annotation.

### Design of touch-spec-keys.xml
There are overall 3 kinds of tracks.
1. the **_anchor_** track to determinate start point.
2. the **_mouthzone_**, **_eyezone_** and **_nosezone_** track the touch events at the most dangerous zones with mucosa. In each zone 3 or 4 subtracks are defined as follows:
    * the **_touches_** track record all touchs in this zone.
    * the **_lips_**, **_left eye_**, **_right eye_**, **_nostril_** tracks record the direct touchs of the mucosa in each dangerous zones.
    * the **_surroundings_** track record the touchs of surrounding skins in each dangerous zones
3. the **_otherskin_** track the touch events at other facial skins, including forehead, chins, cheeks and ears. There are severl subtracks defined as follows:
    * the **_touches_** track record all touchs in these facial parts.
    * the **_forehead_**, **_left chin_**, **_right chin_**, **_left cheek_**, **_right cheek_**, **_left ear_**, **_right ear_** tracks record the touches in
    regard to each facial part.

* The **_anchor_** track  has a attribute **status** with a value **start**. The corresponidng hotkey is "s", and the block will be colored into green.
* The last 2 types of tracks have a attribute **touchType** with values **lefthand**, 
**righthand** and **bothhands**. The corresponding hotkeys are "l", "r" "b", and the block will be colored into yellow, orange and red.