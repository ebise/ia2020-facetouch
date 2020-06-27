# FaceTouch
This is a TECO-seminar project.
## Annotation with Anvil
This is a quick guide for annotating (labeling) videos with the anvil tool.
(https://www.anvil-software.org/)

### General 

shortcut: f1 to start (green line) and f2 to end (red line) for creating an annotation, f3 to directly edit the annotation.

### Guideline
1. Open the video that should be annotated, change the sepcification in annotation properties to the path of touch-spec-keys.xml
2. Click at the wished start point in timeline and press f1, click at the whished stop point press hotkeys (q=begin,w=stop,a=lefthand,s=righthand,d=bothhands) to create an annotation. Make sure the block is selected(pink shadow).
3. If the spec file was changed, remember to click the 3rd icon to reload the xml and click the 4th icon to refresh the annotation.

### Design of touch-spec-keys.xml
There are overall 4 kinds of tracks.
1. the **_anchor_** track determines start and end periods.
2. the **_trl_** track records face touch in general.
3. the **_mouthzone_**, **_eyezone_** and **_nosezone_** tracks record the touch events at the most dangerous zones with mucosa. In each zone 3 to 5 subtracks are defined as follows:
    * the **_touches_** track records all touches in this zone.
    * the **_oralcavity_**, **_eyes_**, **_nostril_** tracks record the direct touchs of the mucosa in each dangerous zone.
    * the **_left eye_**, **_right eye_** tracks record the direct touches of the eyes mucosa in detail.
    * the **_surroundings_** track records the touches of surrounding skins in each dangerous zones
4. the **_otherskin_** track the touch events at other facial skins, including forehead, jaws, cheeks and ears. There are several subtracks defined as follows:
    * the **_touches_** track records all touches in these facial parts.
    * the **_forehead_**, **_jaws_**, **_cheeks_**, **_ears_** tracks record the touches in regard to each facial part
    * the **_left jaw_**, **_right jaw_**, **_left cheek_**, **_right cheek_**, **_left ear_**, **_right ear_** track the corresponding touches in detail.

* The **_anchor_** track  has a attribute **status** with value **begin** and **stop**. The corresponding hotkeys are "q"and "w", and the block will be colored either green or red.
* The last 2 types of tracks have an attribute **touchType** with values **lefthand**, 
**righthand** and **bothhands**. The corresponding hotkeys are "a", "s" "d", and the block will be colored yellow, orange and olive.
* the **_trl_** track is the only primary track except the **_anchor_** track. That means once the blocks in **_trl_** track are annotated, annotation in following tracks could be easily remarked with double klicks and hotkeys for touchType (left-, right-, bothhands). Thus, the annoattion in **_trl_** tracks should include all the breakpoints in every below detail track.
* the **_touches_** tracks reference driectly to **_trl_**, the facial parts of this zone reference to **_touches_** in its groups(**_eyes_** reference to **_eyezone.touches_**, **_jaws_** reference to **_otherskin.touches_**), the detail destinguishment of left and right reference to its corresponding facial parts(**_left eye_** reference to **_eyezone.eyes_**, **_left jaw_** reference to **_otherskin.jaws_**).
