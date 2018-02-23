# TMaps
Simply Python terminal mind mapping tool

## installation:
```
[admin@test ~]$ mkdir -p ~/.local/bin ~/.local/app/lib/
[admin@test ~]$ cd ~/.local/app/lib/
[admin@test TMaps]$ git clone https://github.com/SLusenti/TMaps.git
[admin@test TMaps]$ ln -s ~/.local/app/lib/TMaps/map.py ~/.local/bin/tmaps
```

check PATH variable:
```
[admin@slusenti ~]$ echo $PATH
/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/home/admin/.local/bin
```
if you don't found "~/.local/bin"
update PATH and .bash_profile
```
[admin@test ~]$ PATH=${PATH}:$HOME/.local/bin
[admin@test ~]$ export PATH
[admin@test ~]$ echo $PATH
/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/home/admin/.local/bin
[admin@test ~]$ sed "/^PATH/ s/PATH.*/PATH\=$(echo $PATH | sed -e "s;\/;\\\/;g")/" .bash_profile 
```
## usage:
```
[admin@test ~]$ #create new map
[admin@test ~]$ tmaps <MAP-NAME>
```

examples and help
```
insert root label :> test
<: test 0:> ls
(0) test
     
<: test 0:> add test1
<: test 0:> ls
(0) test
     │
     └(1) test1
          
<: test 0:> help
ls                   map-tree the branch
find <REGEX>         find in the database all the label that match <REGEX>
findbr <REGEX>       find in the current branch all the label that match <REGEX>
ifind <REGEX>        find in the database all the label that match <REGEX> without Sensitive Case
ifindbr <REGEX>      find in the current branch all the label that match <REGEX> without Sensitive Case
cd <ID>              change the current selected branch to <ID>
add <LABEL>          add child to the current brach with label <LABEL>
lsch                 list only the direct child of the current brach
mod <LABEL>          modify the current label selected
rm <IDs>             remove one or more branch
rmbr                 remove all the child branch
rmch                 remove all the terminal child
save                 save all changes
mv <DEST> <IDs>      move all IDs to DEST
mvbr <DEST>          move all child to DEST
mvch <DEST>          move all terminal child to DEST
disaplay             displays metadata of current selection
cp <DEST>            copy selected object to dest
cpbr <DEST>          copy all child to dest
cpch <DEST>          copy all terminal child to dest
cplabel <DEST>       copy only label of current selection to DEST
cplabelch <DEST>     copy only label of all child to DEST
pwd                  return path from ID 0 to current
```

