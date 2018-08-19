# Forensics 300 Creation

To quickly recreate the forensics 300 problem, run `sh generate.sh` inside this directory (documentation is inside the script). 

The audio file `input.wav` in this directory can't be created by a script as easily, so I will explain how to do the entire process here:

1. Download a copy of Mr. Robot - Main Theme (any audio file will work really, but that is the file I chose for this).
2. Visit [this](http://www.meridianoutpost.com/resources/etools/calculators/calculator-morse-code.php) website, and input the message with the key in the audio file into the textarea (in this case, the message was `FILE KEY IN CAPS IS L0LWEAK`). Choose `5 WPM` as the speed, and `500 Hz` as the frequency (again, these settings are arbitrary). Click "Convert to Morse Code", then click "Click to play audio file", and press Ctrl+S to save it as a file.
3. Open up the first audio file, the music, in Audacity.
    a. Select the track, and from the menu bar, choose "Tracks > Mix > Mix Stereo down to Mono".
    b. Select the whole audio track again, and press Ctrl+C to copy it and Ctrl+V to paste it.
    c. Import the `morsecode.wav` audio file that you generated in step 2 as a track via "File > Import > Audio".
    d. Select the bottom track, the one you just imported, and change the amplification down by 10db or so via "Effect > Amplify".
    e. Select the middle track, and from the dropdown to the left on the track, choose "Make Stereo Track".
    f. Select the stereo track (leave the one mono track at the top out), and from the menubar, choose "Tracks > Mix > Mix Stereo down to Mono".
    g. Now, from the top track's menu to the left of the track, choose "Make Stereo Track"
    h. You're almost done! Choose "File > Export > Export as WAV" from the menubar, and save it to `./input.wav` in this directory.
4. In this directory, execute the script `sh generate.sh`. Your output file will be in `workspace/output.wav`, relative to this directory.

