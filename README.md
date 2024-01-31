# aur-watcher
script for filtered search through AUR.

# Note
this script requires ```requests```, ```keyboard``` packages.<br>

# Usage
```aur-watcher.sh p=micro``` - you will get about 756 found items.<br>
```aur-watcher.sh p=micro d=editor``` you will get about 3 found items, since output is filtered with description that contains ```editor``` substring.<br>
```aur-watcher.sh p=fortune d=``` leave description string empty

You can filter your output with following flags:<br>
```d``` - to filter with description.<br>
```n``` - to filter with name.<br>
```m``` - to filter with maintainer.<br>

### What's new?
Now it's easy to scroll through the output with with left and right key. There is no need for ```less``` anymore.
