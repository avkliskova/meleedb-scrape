0. Ensure that your copy of Dolphin is configured as follows:
    - an appropriate Gecko or AR code for accessing the Debug Menu is enabled;
    - no other Gecko or AR codes are enabled (this may be verified by right-clicking on your chosen ROM and selecting *Properties > Gecko Codes* or *Properties > AR Codes*);
    - *Movie > Pause at End of Movie* is checked;
    - no other settings that will interfere with normal emulation are configured;
    - your controller, keyboard, or other controller input device is configured on port 1.
1. Run **autogen.py** [][]
2. Play back **out.dtm** in Dolphin via *Movie > Play Input Recording...* The TAS will automatically select character and stage, exit the debug menu, and pause playback.
3. Unpause and record the animation frames that you wish to extract. **Do not use the C-stick or taunt, as this will affect the position of the camera.** Once you are finished, stop the recording and save the .dtm file, hereafter called **in.dtm**, when prompted.
4. Run **conv.py** [][]. This will
    - generate three copies of **in.dtm** [][];
    - dump their frames;
    - render the animation frame and HUD text separately, on transparent backgrounds;
    - OCR the HUD text, obtaining an action state name and frame number;
    - [][]
