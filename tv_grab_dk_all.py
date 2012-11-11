#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# $Id$

import os
import codecs
import sys

# R�kkef�lge grabbere skal merges
# Grabberne er sorteret efter hvor mange dages oversigt de leverer, 
# da det giver det mest stabile resultat
mergeorder = ("dr_2012","yousee","swedb")

mergeorderpath = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]),"mergeorder.conf"))
if os.path.isfile(mergeorderpath):
    try:
        print "Found merge order configuration in "+mergeorderpath
        order=()
        pfile = open(mergeorderpath).read()
        for line in pfile.splitlines():
            order+=(line,)
        mergeorder=order
    except:
        print "Can not read mergeorder file. Continuing with default mergeorder"
print "Merge order is "+str(mergeorder)
        
#Standard configfil placering
os.environ["HOME"] = os.path.expanduser("~")
CONFIGDIR = os.environ["HOME"]+os.path.sep+".xmltv"+os.path.sep

#tv_grab_dk_alls ejen configfils placering
CONFIGFILE = CONFIGDIR+"tv_grab_dk_all.conf"

#Grabbere, der ikke bliver hentet af filegrabber
grabbers = {}

#Titlerne på grabberne
grabberNames = {
    "tv_grab_dk_tvtid":"tvtid",
    "tv_grab_dk_yousee.py":"yousee",
    "tv_grab_dk_ahot.py":"ahot",
    "tv_grab_dk_ontv.py":"ontv",
    "tv_grab_dk_jubii.py":"jubii",
    "tv_grab_dk_tvguiden.py":"tvguiden",
    "tv_grab_dk_dr":"dr",
    "tv_grab_se_swedb":"swedb",
    "tv_grab_dk_dr_2009":"dr_2009",
    "tv_grab_dk_dr_2012":"dr_2012"
}

#Hvilke programmer grabbere skal køres med
interpreters = {
    "tvtid":"perl -I perllib/",
    "dr":"perl",
    "yousee":"python",
    "ahot":"python",
    "ontv":"python",
    "jubii":"python",
    "tvguiden":"python",
    "swedb":"perl",
    "dr_2009":"perl",
    "dr_2012":"perl"
} 

#Hvilke options grabbere skal køres med
options = {
    "tvtid":"",
    "dr":"",
    "yousee":"",
    "ahot":"",
    "ontv":"",
    "jubii":"",
    "tvguiden":"",
    "swedb":"",
    "dr_2009":" --days 14",
    "dr_2012":" --days 14"
} 

#Om grabberen skal have splittitle kørt
needSplittitle = {
    "dr":True,
    "dr_2009":True
}

#De efterfoelgende strukturer bestemmer formatet paa grabbernes config filer:

#Navne på forskellige configfiler. 
#Hvis en grabber ikke har et entry i denne liste, vil der ikke blive lavet nogen configfil automatisk. 
#Grabberen skal i det tilf�lde konfigureres s�rskilt.
configFiles = {
    "tvtid":"tv_grab_dk_tvtid.conf",
    "dr":"tv_grab_dk_dr.conf",
    "ahot":"tv_grab_dk_ahot.conf",
    "ontv":"tv_grab_dk_ontv.conf",
    "jubii":"tv_grab_dk_jubii.conf",
    "swedb":"tv_grab_se_swedb.conf",
    "tvguiden":"tv_grab_dk_tvguiden_py.conf",
    "yousee":"tv_grab_dk_yousee.conf",
    "dr_2009":"tv_grab_dk_dr_2009.conf",
    "dr_2012":"tv_grab_dk_dr_2012.conf"
}

#Her kan der defineres linier som placeres i starten af conf filen:
extraConfigLines = {
    "yousee":"firstLang=Original\ncreditsInDesc=Yes\nsplitTitles=Yes",
    "dr_2009":"accept-copyright-disclaimer=accept\ninclude-radio=0\nroot-url=http://www.dr.dk/tjenester/programoversigt/",
    "dr_2012":"accept-copyright-disclaimer=accept\ninclude-radio=0\nroot-url=http://www.dr.dk/tv/oversigt/json/guide/\nepisode-in-subtitle=No"
}

#Særlige funktioner til oversættelse af parsefil -> configfil
configAdaptors = {
    "tvtid": lambda t, a: "channel %s %s" % (t, a),
    "dr":    lambda t, a: "channel %s %s" % (t[:3], a),
    "dr_2009":    lambda t, a: "channel=%s" % (t),
    "dr_2012":    lambda t, a: "channel=%s" % (t),
    "swedb": lambda t, a: "channel=%s" % (t)
}

#Om grabberen bruger "id name" eller bare "id"
needName = {
    "tvtid":True,
    "dr":True,
    "ontv":True,
    "swedb":True,
    "tvguiden":True
}

#     -----     Parser argumenter     -----     #
print "Parsing arguments"
FOLDER = os.path.dirname(__file__)
if not FOLDER: FOLDER = "."
if not FOLDER.endswith(os.path.sep): FOLDER += os.path.sep
FOLDER = os.path.expanduser(FOLDER)
FOLDER = os.path.abspath(FOLDER)

import sys, getopt
cmds = ['config-file=', 'configure', 'noupdate', 'out=']
optlist, args = getopt.getopt(sys.argv[1:], '', cmds)
opts = {}
for k, v in optlist:
    opts[k] = v

for k in [l for l in ("--config-file", "--out") if l in opts]:
    opts[k] = os.path.abspath(opts[k])

if len(args) > 1: FOLDER = args[1]
try: os.makedirs(FOLDER)
except: pass
try: os.chdir(FOLDER)
except: raise TypeError, "Kunne ikke åbne mappen '%s'" % FOLDER

#     -----     Henter filer     -----     #
if not '--noupdate' in opts:
    import urllib2
    import re
    # Find revision:
    svnrevision=0
    try:
        print "Reading revision of sourceforge"
        folderlist=urllib2.urlopen("http://xmltvdk.svn.sourceforge.net/viewvc/xmltvdk/trunk/").read()
        m=re.search('<td>Directory revision:</td>\n*<td><a href="/viewvc/xmltvdk\\?view=revision&amp;revision=([0-9]+)"', folderlist)
        svnrevision=int(m.group(1))
        print "Sourceforge xmltvdk repository is at revision "+str(svnrevision)
    except:
        print "Can not read revision of sourceforge xmltvdk repository"
    localrevision=0
    try:
        file=open("revision","r")
        localrevision=int(file.read())
        file.close()
        print "Local folder at revision "+str(localrevision)
    except:
        print "Can not read local revision file"
    if localrevision<svnrevision:
        try:
            parsefiles = (
                "ahotparsefile",
                "drparsefile",
                "dr_2009parsefile",
                "dr_2012parsefile",
                "jubiiparsefile",
                "ontvparsefile",
                "swedbparsefile",
                "tvguidenparsefile",
                "tvtidparsefile",
                "youseeparsefile")
            for filename in parsefiles:
                print "Copying "+filename+" from sourceforge"
                contents=urllib2.urlopen("http://xmltvdk.svn.sourceforge.net/viewvc/*checkout*/xmltvdk/trunk/channel_ID_parse_filer/"+filename).read()
                file=open(filename,"w")
                file.write(contents)
                file.close()
            if not os.path.isdir("perllib/JSON/PP"):
                os.makedirs("perllib/JSON/PP")
            files = (
                "analyzeformater.py",
                "channelid.py",
                "perllib/JSON.pm",
                "perllib/JSON/PP56.pm",
                "perllib/JSON/PP58.pm",
                "perllib/JSON/PP.pm",
                "perllib/JSON/PP/Boolean.pm",
                "perllib/JSON/PP5005.pm",
                "runall.py",
                "splittitle.py",
                "timefix.py",
                "tv_grab_dk_ahot.py",
                "tv_grab_dk_dr",
                "tv_grab_dk_dr_2009",
                "tv_grab_dk_dr_2012",
                "tv_grab_dk_jubii.py",
                "tv_grab_dk_ontv.py",
                "tv_grab_se_swedb",
                "tv_grab_dk_tvguiden.py",
                "tv_grab_dk_tvtid",
                "tv_grab_dk_yousee.py",
                "xmltvanalyzer.py",
                "xmltvmerger.py")
            for filename in files:
                print "Copying "+filename+" from sourceforge"
                contents=urllib2.urlopen("http://xmltvdk.svn.sourceforge.net/viewvc/*checkout*/xmltvdk/trunk/"+filename).read()
                file=open(filename,"w")
                file.write(contents)
                file.close()
            file=open("revision","w")
            file.write(str(svnrevision))
            file.close()
        except:
            print "Can not copy files from sourceforge. Is the connection down? Tries to continue without"

#     -----     Finder filer     -----     #
#kigger efter tv_grab_dk_dr_2009 grabberen:
if "dr_2009" in mergeorder:
    drpath="./tv_grab_dk_dr_2009"
    if not os.path.isfile(drpath):
        drpath="/usr/bin/tv_grab_dk_dr_2009"
        if not os.path.isfile(drpath):
            drpath=r"C:\Perl\site\lib\xmltv\dk\tv_grab_dk_dr_2009"
            if not os.path.isfile(drpath):
                drpath=r"C:\Perl\site\lib\xmltv\tv_grab_dk_dr_2009"
    if os.path.isfile(drpath):
        grabbers["dr_2009"]=drpath
        print "Using DR_2009 grabber in "+grabbers["dr_2009"]
    else:
        print "Kan ikke finde tv_grab_dk_dr_2009 grabberen. Fortsaetter uden."
#kigger efter tv_grab_se_swedb grabberen:
#if "swedb" in mergeorder: 
#    swedbpath="./tv_grab_se_swedb"
#    if not os.path.isfile(swedbpath):
#        swedbpath="/usr/bin/tv_grab_se_swedb"
#        if not os.path.isfile(swedbpath):
#            swedbpath=r"C:\Perl\site\lib\xmltv\dk\tv_grab_se_swedb"
#            if not os.path.isfile(swedbpath):
#                swedbpath=r"C:\Perl\site\lib\xmltv\tv_grab_se_swedb"
#    if os.path.isfile(swedbpath):
#        grabbers["swedb"]=swedbpath
#        print "Using swedb grabber in "+grabbers["swedb"]
#    else:
#        print "Kan ikke finde tv_grab_se_swedb grabberen. Fortsaetter uden."

parsedicts = {}
for file in os.listdir("."):
    if file in grabberNames:
        if grabberNames[file] in mergeorder:
            grabbers[grabberNames[file]] = file
    elif file.endswith("parsefile"):
        if file[:-9] in mergeorder:
            print "Reading parsefile "+file
            dic = {}
            for line in open(file):
                k, v = [v.strip() for v in line.split("\t",1)]
                dic[v] = k
                print "Adding channel " + v + "=" + k
            parsedicts[file[:-9]] = dic
for grabber in grabbers:
    print "Using "+grabber+" grabber in "+grabbers[grabber]


channel_set = {}
for grabberchannels in parsedicts.values():
    for channel in grabberchannels.keys():
        channel_set[channel] = None
channels = channel_set.keys()
channels.sort()

#     -----     Konfigurerer selv     -----     #

def configure (file, channels):
    folder = os.path.split(file)[0]
    if folder == "": folder = "."
    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(file):
        answer = raw_input("Konfigurationsfilen eksisterer allerede. Vil du overskrive den? (y/N) ").strip()
        if not answer.lower() in ("y","yes"):
            sys.exit()
    file = open(file, "w")
    for id, name in channels:
        answer = raw_input("Tilføj %s (y/N) " % name).strip()
        if answer == "y":
            file.write("%s %s\n" % (id, name))
        else: file.write("#%s %s\n" % (id, name))
    sys.exit()

#     -----     load and save TDC configuration files     -----     #
import traceback
def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

def loadChannels (filename):
    loadLocals = {}
    print "Running "+filename
    #print" with globals="+globals()
    #print " and loadLocals="+loadLocals
    execfile(filename, {}, loadLocals)
    if (not loadLocals.has_key('version')):
        sys.stderr.write("No version found. You should update %s by deleting the old and make a new\n" % filename)
        sys.stderr.write("Sorry for the inconvienence\n")
    else:
        if (loadLocals['version'] == 121):
            sys.stderr.write("Version is wrong. Is "+loadLocals['version']+" but should be "+u'121')
            sys.stderr.write("You should update %s by deleting the old and make a new\n" % filename)
            sys.stderr.write("Sorry for the inconvienence\n")
    return loadLocals['channels']

def saveChannels (channels, filename):
    output = codecs.open(filename, 'w', 'utf-8')
    output.write(u'#!/usr/bin/env python\n')
    output.write(u'# -*- coding: UTF-8 -*-\n')
    output.write(u'\n')
    output.write(u"progname  = u'tv_grab_dk_yousee'\n")
    output.write(u"version   = u'121'\n")
    output.write(u'\n')
    output.write(u'# If you edit this file by hand, only change active and xmltvid columns.\n')
    output.write(u'# (channel, channelUrl, active, xmltvid)\n')
    output.write(u'channels = [\n')
    for ch in channels[:-1]:
        output.write(str(ch) + u',\n')
    output.write(str(channels[-1]) + u']\n')
    output.close()

configfile = "--config-file" in opts and opts["--config-file"] or CONFIGFILE
if "--configure" in opts:
    configure(configfile, [(p,p) for p in channels])

#     -----     Konfigurerer andre     -----     #

if not os.path.isfile(configfile):
    print "Configfilen '%s' kan ikke findes. Kør programmet med '--configure'" % configfile
    sys.exit()

#TODO: De forskellige grabberfiler bør også have #'er, hvis de vil

chosenChannels = [l.strip() for l in open(configfile)]
chosenChannels = [l for l in chosenChannels if not l.startswith("#")]
chosenChannels = [l.split(" ")[0] for l in chosenChannels]
ccset = dict.fromkeys(chosenChannels)
print "Chosen channels: "+str(ccset)
for grabber, parsefile in parsedicts.iteritems():
    if grabber in configFiles:
        try:
            print "Configuring "+grabber+" grabber"
            if grabber=="yousee":
                print "Loading config file:" + configFiles[grabber]
                tdcset={}
                for ch in ccset:
                    if ch in parsedicts[grabber]:
                        tdcset[parsedicts[grabber][ch]]="Yes"
                channelTable=loadChannels(CONFIGDIR+configFiles[grabber])
                for index in range(len(channelTable)):
                    channel, channelUrl, active, xmltvid = channelTable[index]
                    active=xmltvid in tdcset
                    channelTable[index] = (channel, channelUrl, active, xmltvid)
                saveChannels(channelTable, CONFIGDIR+configFiles[grabber])
            else:
                f = open(CONFIGDIR+configFiles[grabber],"w")
                if grabber in extraConfigLines:
                    f.write(extraConfigLines[grabber]+"\n")
                if grabber=="swedb":
                    f.write("root-url=http://tv.swedb.se/xmltv/channels.xml.gz\ncachedir="+CONFIGDIR+"cache\n")
                for channel in [c for c in channels if c in parsedicts[grabber]]:
                    if not channel in ccset:
                        f.write("# ")
                    parsedChannel = parsedicts[grabber][channel]
                    if grabber in configAdaptors:
                        f.write("%s\n" % configAdaptors[grabber](parsedChannel,channel))
                    elif grabber in needName:
                        f.write("%s %s\n" % (parsedChannel,channel))
                    else:
                        f.write("%s\n" % parsedChannel)
                f.close()
        except:
            print "Can not configure "+grabber+" grabber: ", formatExceptionInfo()


df = "data"+os.path.sep
if not os.path.exists(df):
    os.makedirs(df)
else:
    for file in os.listdir(df):
        os.remove(df+file)

#     -----     Grabber     -----     #

import runall
grabcommands = []
for g, command in grabbers.iteritems():
    if g in configFiles:
        grabcommands += ['%s "%s" %s --config-file "%s" > "%s"' % \
            (interpreters[g], command, options[g], CONFIGDIR+configFiles[g], df+g)]
    else:
        grabcommands += ['%s "%s" %s > "%s"' % \
            (interpreters[g], command, options[g], df+g)]
print "Starter grabbere:"
print grabcommands
runall.runEm(grabcommands)

#     -----     Splitter     -----     #

for g in grabbers.keys():
    if g in needSplittitle:
        os.system('python splittitle.py "%s" > "%s_split"' % (df+g,df+g))

#     -----     Channelid     -----     #

for g in grabbers.keys():
    print "ID:",g
    g1 = g
    if g1 in needSplittitle:
        g1 = g1+"_split"
    pre = "python channelid.py "
    try: open(g+"parsefile").read().decode("utf-8")
    except UnicodeDecodeError: pre += "--iso "
    os.system('%s "%sparsefile" "%s" "%s_id"' % (pre, g, df+g1, df+g))

#     -----     Merger     -----     #

for i in range(1,len(mergeorder)):
    print "Merge:"," ".join(mergeorder[:i+1])
    os.system('python xmltvmerger.py "%s_id" "%s_id" "%s_id"' % \
            (df+"".join(mergeorder[:i]), df+mergeorder[i], df+"".join(mergeorder[:i+1])))

#     -----     TimeFix     -----     #

out = "--out" in opts and opts["--out"] or "".join(mergeorder) + "_time"
out = os.path.expanduser(out)
if os.path.isdir(out):
    if out[-1] == os.path.sep:
        out += "".join(mergeorder) + "_time"
    else: out += os.path.sep + "".join(mergeorder) + "_time"
os.system('python timefix.py "%s_id" "%s"' % (df+"".join(mergeorder), out))

