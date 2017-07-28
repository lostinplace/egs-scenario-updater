# Empyrion Scenario Updater

## Summary

This is a script that I created to meet the needs of my play group.

This script reads a scenario, and writes out a copy with the following modifications:

* All Pentaxid (Resources and Crystals) are removed
* All Resource deposits have been dramatically shrunk, but the number of deposits is much higher
* A Faction Mission has been generated for every planet with randomly generated POIs
  * There is a task for each POI randomly generated type that can be found on the planet
  * Placing a core block on 1 of each type rewards the faction with 5 pentaxid
  * Conquering 1 of each POI type completes the mission and rewards the faction with 100 Gold coins


## Instructions
To run the script from the command line:

```
~ git clone git@github.com:lostinplace/egs-scenario-updater.git
~ cd egs-scenario-updater
~ pip install -r requirements.txt
~ ./updater.py --basepath=<PATH TO CONTENT FOLDER> <NAME OF SOURCE SCENARIO> <NAME OF OUTPUT SCENARIO>
```

You can also see usage by running:

```
~ ./updater.py -h
```

If you's like, you can place the basepath in a file called `.updater-config`  it will traverse to root looking for it, and it will use the file contents as a basepath

I ran every thing on WSL (bash for windows) I haven't tried it on the windows command line

## Feedback

I created this as the precursor to a framework for programatically generating scenarios, let me know if you have any questions
