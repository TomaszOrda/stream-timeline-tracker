# stream-timeline-tracker

A purely functional piece of code. One file command line application designed to be lightweight and rudimentary.

Goal of this program is to give a simple interface which will allow quickly saving timestamps in real time. Mostly as a help for creating timelines while watching streams. Though it can certainly be used under different circumstances.

Generally, using it one would run the application, add offset such that it aligns with the stream or is a few seconds behind. The results are being written into text file, and json file in the same directory, named with current date and a short random string to avoid collisions.

It uses textualize library to create a TUI (text-based user interface). It seems such a library was an overkill. Yet it gets the job done. I might want to create a different version of this program using a different interface — basic python with no library, curses for pascal-like console manipulation or javascript web application.
