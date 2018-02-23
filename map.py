#!/usr/bin/python
#-*- coding: utf-8 -*-
import json
import os
import sys
import re
import readline


com = ""
currento = {}
#path =  os.path.dirname(os.path.abspath(sys.argv[0]))
path = os.path.dirname(os.path.realpath(__file__))
chartdata = {u"maxid":0,u"label":u"",u"id": u"0", u"data":[]}
ttyrows, ttycols = os.popen('stty size', 'r').read().split()
ttycols = int(ttycols)
ttyrows = int(ttyrows)
chartname = sys.argv[1]
if not os.path.exists(path+"/history"):
    os.makedirs(path+"/history")
if not os.path.exists(path+"/data"):
    os.makedirs(path+"/data")

def parsecommand(rawcommand):
  comargv = ""
  argv = rawcommand.split(" ")
  command = argv[0]
  return command, " ".join(argv[1:])

def display():
  print "label: "+currento[u'label']
  print "id: "+currento[u'id']
  try:
    print "pid: "+currento[u'pid']
  except: pass
  print "childs: "+str(len(currento[u'data']))

def add(strg):
  global currento
  newobject =  {u"label":u"",u"id": 0, u"data":[], u"pid":u"0"}
  id = __getnewid()
  newobject[u"label"] = unicode(strg, "utf-8")
  newobject[u"id"] = unicode(id, "utf-8")
  newobject[u"pid"] = currento[u"id"]
  currento[u"data"].append(newobject)

def printch(obj={},pre="", reng="",rec=True):
  global currento,com
  if not obj:
    obj = currento
  lens = len(pre+obj[u"id"]) + 3
  lenst = len(obj[u"label"])
  count = 1
  while count < 4 :  
    isok = lens+lenst/count
    if isok < ttycols:
      break
    else:
      count += 1 
  if count == 4:
    print pre+"("+obj[u"id"]+") "
  else:
    arrays = __splitstr(obj[u"label"], count)
    print pre+reng+"("+obj[u"id"]+") "+arrays[0]
    if(reng == u"├"):
      reng = u"│"
    else:
      reng = " "
    for arr in arrays[1:]:
      print pre+reng+"   "+" "*len(obj[u"id"])+arrays[0]
    pre = pre+reng+"   "+" "*len(obj[u"id"])
    if com == "ls":
      if len(obj[u"data"] )> 0:
        print pre + u"│"
      else:
        print pre
    _co = 0
    _sate = True if com == "ls" else False
    if rec:
      while _co < len(obj[u"data"]):
        if (_co+1)< len(obj[u"data"]):
          reng = u"├"
        else:
          reng = u"└"
        printch(obj[u"data"][_co],pre,reng,_sate)
        _co += 1

def delete(ids):
  #get id to print
  global currento
  if not ids:
    ids = currento[u'id']
  ids = ids.split(" ")
  for id in ids:
    if id != u"0" and re.match("[0-9]*",id):
      obj = __findid(id)
      pobj = __findid(obj[u"pid"])
      if id == currento[u'id']:
        currento = pobj
      _co = 0
      _er = False
      while _co < len(pobj[u"data"]):
        if pobj[u"data"][_co][u"id"] == id:
          _er = True
          break
        _co += 1
      if _er:
        pobj[u"data"].pop(_co)

def deletebr():
  #get id to print
  global currento
  currento[u"data"] = []

def deletech():
  #get id to print
  global currento
  _co = 0
  while _co < len(currento[u'data']):
    if not currento[u"data"][_co][u"data"]:
      currento[u"data"].pop(_co)
    _co += 1

def mod(strg):
  currento[u"label"] = strg

def mv(ids):
  global currento
  ids = ids.split(" ") 
  if len(ids) == 1:
    ids.append(currento[u"id"])
  if len(ids) > 1:
    tobj = __findid(ids[0])
    for id in ids[1:]:
      if id != "0":
        obj = __findid(id)
        pobj = __findid(obj[u"pid"])
        _co = 0
        _er = False
        while _co < len(pobj[u"data"]):
          if pobj[u"data"][_co][u"id"] == obj[u"id"]:
            _er = True
            break
          _co += 1
        if _er:
          obj[u'pid'] = ids[0]
          tobj[u"data"].append(obj)
          pobj[u"data"].pop(_co)

def copy(ids):
  global currento
  ids = ids.split(" ")
  tobj = __findid(ids[0])
  obj = json.loads(json.dumps(currento))
  obj[u'pid']=ids[0]
  obj = __copyid(obj)
  tobj[u'data'].append(obj)

def copybr(ids):
  global currento
  ids = ids.split(" ")
  tobj = __findid(ids[0])
  for obje in currento[u'data']:
    obj = json.loads(json.dumps(obje))
    obj[u'pid']=ids[0]
    obj = __copyid(obj)
    tobj[u'data'].append(obj)

def copych(ids):
  global currento
  ids = ids.split(" ")
  tobj = __findid(ids[0])
  for obje in currento[u'data']:
    if not obje[u'data']:
      obj = json.loads(json.dumps(obje))
      obj[u'pid']=ids[0]
      obj = __copyid(obj)
      tobj[u'data'].append(obj)

def cplabel(ids):
  global currento
  ids = ids.split(" ")
  tobj = __findid(ids[0])
  obj = json.loads(json.dumps(currento))
  obj[u'pid']=ids[0]
  obj[u'id']=__getnewid()
  obj[u'data']=[]
  tobj[u'data'].append(obj)

def cplabelch(ids):
  global currento
  ids = ids.split(" ")
  tobj = __findid(ids[0])
  for obje in currento[u'data']:
    obj = json.loads(json.dumps(obje))
    obj[u'pid']=ids[0]
    obj[u'id']=__getnewid()
    obj[u'data']=[]
    tobj[u'data'].append(obj)

def mvbr(ids):
  global currento
  ids = ids.split(" ") 
  _co = 0
  tobj = __findid(ids[0])
  while _co < len(currento[u'data']):
    obj = currento[u'data'][_co]
    obj[u"pid"] = ids[0]
    tobj[u"data"].append(obj)
    currento[u"data"].pop(_co)
    _co += 1

def mvch(ids):
  global currento
  ids = ids.split(" ") 
  _co = 0
  tobj = __findid(ids[0])
  while _co < len(currento[u'data']):
    if not currento[u'data'][_co][u'data']:
      obj = currento[u'data'][_co]
      obj[u"pid"] = ids[0]
      tobj[u"data"].append(obj)
      currento[u"data"].pop(_co)
    _co += 1

def move(id):
  global currento
  obj =  __findid(id)
  if obj:
    print "move on: "+id
    currento = obj
  else:
    print "id not found!"

def find(strg,obj={}):
  global chartdata,com
  if not obj:
    obj = chartdata
  try: 
    if com == "ifind" or com == "ifindbr":
      if re.match(unicode(strg, "utf-8"),obj[u"label"],re.IGNORECASE) :
        print "("+obj[u"id"]+") "+obj[u"label"]
    else:
      if re.match(unicode(strg, "utf-8"),obj[u"label"]) :
        print "("+obj[u"id"]+") "+obj[u"label"]
  except: pass
  for data in obj[u"data"]:
    find(strg,data)

def pwd():
  global currento
  array = ["("+currento['id']+") "+currento["label"]]
  obj = currento
  while obj[u'id'] != "0":
    array.append("   "+" "*len(obj['id'])+"|")
    obj = __findid(obj[u'pid'])
    array.append("("+obj['id']+") "+obj["label"])
  for line in array[::-1]:
    print line

def bye():
  global chartname
  with open(path+"/data/"+chartname,"w") as f:
    f.write(json.dumps(chartdata))
  readline.write_history_file(path+"/history/"+chartname)
  sys.exit()

def save():
  global chartname
  with open(path+"/data/"+chartname,"w") as f:
    f.write(json.dumps(chartdata))
  readline.write_history_file(path+"/history/"+chartname)

def __copyid(obj):
  obj[u'id'] = __getnewid()
  for data in obj[u'data']:
    data['pid'] = obj[u'id']
    __copyid(data)
  return obj

def __getnewid():
  chartdata[u"maxid"] += 1
  return str(chartdata[u"maxid"])

def __findid(id,obj={}):
  obj = chartdata if (not obj) else obj
  objr = {}
  if obj[u"id"] == id :
    objr =  obj
  else:
    for data in obj[u"data"]:
      objr1 =  __findid(id,data)
      if ( objr1 ):
        objr = objr1
  return objr
def help():
  print "ls                   map-tree the branch"
  print "find <REGEX>         find in the database all the label that match <REGEX>"
  print "findbr <REGEX>       find in the current branch all the label that match <REGEX>"
  print "ifind <REGEX>        find in the database all the label that match <REGEX> without Sensitive Case"
  print "ifindbr <REGEX>      find in the current branch all the label that match <REGEX> without Sensitive Case"
  print "cd <ID>              change the current selected branch to <ID>"
  print "add <LABEL>          add child to the current brach with label <LABEL>"
  print "lsch                 list only the direct child of the current brach"
  print "mod <LABEL>          modify the current label selected"
  print "rm <IDs>             remove one or more branch"
  print "rmbr                 remove all the child branch"
  print "rmch                 remove all the terminal child"
  print "save                 save all changes"        
  print "mv <DEST> <IDs>      move all IDs to DEST"
  print "mvbr <DEST>          move all child to DEST" 
  print "mvch <DEST>          move all terminal child to DEST" 
  print "disaplay             displays metadata of current selection"
  print "cp <DEST>            copy selected object to dest"
  print "cpbr <DEST>          copy all child to dest"
  print "cpch <DEST>          copy all terminal child to dest"
  print "cplabel <DEST>       copy only label of current selection to DEST"
  print "cplabelch <DEST>     copy only label of all child to DEST"
  print "pwd                  return path from ID 0 to current"

def __complete(text, state):
  options = sorted(["ls","find","findbr","cd","add","lsch","mod","rm","rmbr","rmch","save","mv","mvbr","mvch","display",
                    "cp","cpch","cpbr","cplabel","cplabelch","pwd","help","ifind","ifindbr"])
  matches = []
  if text:
    matches = [s for s in options if s and s.startswith(text)]
  else: 
    matches = options
  return matches[state]
try:
  readline.read_history_file(path+"/history/"+chartname)
except:
  pass
#readline.read_init_file("./inputrc")
readline.parse_and_bind("tab: complete")
readline.set_completer(__complete)

def __splitstr(strg, pices):
  count = 0
  add = len(strg)/pices
  arrays = []
  while count < len(strg):
    if count+add < len(strg):
      arrays.append(strg[count:(count+add)])
    else:
      arrays.append(strg[count:])
    count=count+add
  return arrays

def init():
  global currento,com,ttycols,chartname
  inputmax = ttycols
  while True:
    rawcommand = raw_input("<: "+chartname+" "+currento[u'id']+":> ") 
    if rawcommand != "":
      com, argv = parsecommand(rawcommand)
      if com == "ls":
        printch()
      elif (com == "find") and (len(argv) > 0):
        find(argv)
      elif (com == "findbr") and (len(argv) > 0):
        find(argv,currento)
      elif (com == "cd") and (len(argv) > 0):
        move(argv)
      elif (com == "add") and (len(argv) > 0) and (len(argv) < inputmax ):
        add(argv)
      elif (com == "lsch"):
        printch()
      elif (com == "mod") and (len(argv) > 0) and (len(argv) < inputmax ):
        mod( argv )
      elif (com == "rm") and (len(argv) > 0):
        delete(argv)
      elif (com == "rmbr"):
        deletebr()
      elif (com == "rmch"):
        deletech()
      elif (com == "bye"):
        bye()
      elif (com == "mv") and (len(argv) > 0):
        mv(argv)
      elif (com == "mvbr") and (len(argv) > 0):
        mvbr(argv)
      elif (com == "mvch") and (len(argv) > 0):
        mvch(argv)
      elif (com == "save") :
        save()
      elif (com == "display" ):
        display()
      elif (com == "cp") and (len(argv) > 0):
        copy(argv)
      elif (com == "cpbr") and (len(argv) > 0):
        copybr(argv)
      elif (com == "cpch") and (len(argv) > 0):
        copych(argv)
      elif (com == "cplabel") and (len(argv) > 0):
        cplabel(argv)
      elif (com == "cplabelch") and (len(argv) > 0):
        cplabelch(argv)
      elif (com == "pwd"):
        pwd()
      elif com == "help":
        help()
      elif com == "ifind":
        find(argv)
      elif com == "ifindbr":
        find(argv,currento)
      else:
        print "command not found or invalid arguments"

def load():
  global currento, chartdata
  try:
    with open(path+"/data/"+chartname,"r") as f:
      chartdata = json.loads(f.read())
  except Exception as e:
    strg = raw_input("insert root label :> ")
    chartdata["label"] = strg
  currento = chartdata

try:
  load()
  init()
except:
  print
  #raise e

#init()

