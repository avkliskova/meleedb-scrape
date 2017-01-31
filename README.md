0. Ensure that your copy of Dolphin is configured as follows:
    - an appropriate Gecko or AR code for accessing the Debug Menu is enabled;
    - no other Gecko or AR codes are enabled (this may be verified by right-clicking on your chosen ROM and selecting Properties > Gecko Codes or Properties > AR Codes);
    - Movie > Show Frame Counter and Movie > Show Input Display are enabled;
    - no other settings that will interfere with normal emulation are configured;
    - your controller, keyboard, or other input setup is configured on port 1.
1. Begin a new input recording by selecting your ROM and selecting Movie > Start Input Recording.
2. Navigate to the Debug Menu and configure it as follows:
    - Set DBLEVEL to DEVELOP.
    - ...etc...
3. Record the animation frames that you wish to extract. Do not use the C-stick or taunt, as this will affect the position of the camera. Once you are finished, stop the recording and save the .dtm file, hereafter called **in.dtm**, when prompted.
4. Play **in.dtm** back by selecting Movie > Play Input Recording... When "-----------EXIT" is selected on the Debug Menu, the frame counter will freeze momentarily as the stage is loaded; make a note of the value at which it freezes, hereafter called **frames_to_wait**.
5. Shell stuff.
