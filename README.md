# CobWeb — Minimal browser to get the job done

CobWeb is a Python-based minimal/simple web browser, designed originally as a test 
project and may eventually be developed further. This is not a finished product, but
I figure I will keep coming back to it as I like the idea of having a light-weight
Python web browser. It has many of the basic, similar functions you'd expect to see 
on something claimed to be a web browser.

I'd like to make this open source, and see where this goes, despite there being probably 
hundreds of web browsers (never heard pure Python-based though, probably because its hard 
to maintain for mainstream functionality). If you have any ideas maybe contribute?

## Code notes

### TODO:

- Include heavily encrypted traffic, as this is still not very secure, just minimal.
- Add more customizable tweaks/settings for user compatibility. Will probably use a 
  seperate file to read from, config file(?). Add favourites bar/bookmarks etc.?
- Add keyboard shortcuts for quicker use and more flexibility.
- Bundle up an executable to run on systems which may not have Python installed.

### Tabbing

Tab support complicates the internals of the browser a bit, since we now need to
keep track of the currently active browser view, both to update UI elements 
(URL bar, HTTPs icon) to changing state in the currently activewindow, and 
to ensure the UI events are dispatched to the correct web view.

This is achieved by using intermediate slots which filter events, and by
adding signal redirection (using lamba functions to keep it short).

Double click on an empty space next to (or after) the last tab, to open a new one.
Or alternatively, just go to File > New Tab.

## Other licenses

Icons used in the application are by [@flaticon] (https://www.freepik.com/flaticon)
