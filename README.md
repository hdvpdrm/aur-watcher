# aur-watcher
script for filtered search through AUR and official repository of Arch Linux.

# Note
this script requires ```requests``` package.<br>

# Usage
```python aur-watcher p=package_name s=[off|aur] [ o=[pt|ip] ]```

Available options:<br>
p - package name<br>
s - source(AUR or official repository)<br>
o - output mode(plain text or inner pager).<br> 
      Plain text is default mode. To quit page press ```q```. Press ```any key``` to move forward. 
