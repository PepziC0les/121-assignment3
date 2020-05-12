import re
import nltk
import os
import json
from bs4 import BeautifulSoup
from math import log10
from buildDocCount import buildDocCount

#test
import time


class ContentExtractor:
    def __init__(self, url, jsonLine, globalDict):
        self.jsonLine = jsonLine
        self.globalDict = globalDict
        self.url = url
        self.wordFrequency = dict()
        self.numOfTerms = 0
        


    def extract_content(self):
        content = BeautifulSoup(self.jsonLine, "lxml")
        important_words = []
        for i in content.find_all(["b", "strong", "title", "h1", "h2", "h3"]):
            val = []
            #print(i)
            if (i.name == "title"):
                val.append("t")
            elif (i.name == "h1"):
                val.append("h1")
            elif (i.name == "h2"):
                val.append("h2")
            elif (i.name == "h3"):
                val.append("h3")
            elif (i.name == "b"):
                val.append("b")
            elif (i.name == "strong"):
                val.append("s")
            #print("val1: ", val)
            word = i.getText().rstrip().lstrip()
            #result = word
            val.append(nltk.tokenize.word_tokenize(word))
            #print(val)
            important_words.append(val)
            
        self.compute_frequency(important_words, important=True)
        tokens = nltk.tokenize.word_tokenize(content.get_text())
        self.compute_frequency(tokens)
    
    
    
    def compute_frequency(self, tokens:list, important=False):
        #print(tokens)
        if (not important):
            tokenSet = set()
            text = ''
            for content in tokens:
                #print(content)
                for ch in content:
                    if (ch.isalnum() or ch == "'"):
                        text += ch
                    elif (len(text) >= 2):
                        tokenSet.add(text)
                        text = ''
                    else:
                        text = ''
            for word in tokens:
                if len(word) >= 2 and word.isalnum():
                    self.numOfTerms += 1
                    word = word.lower()
                    if word in self.wordFrequency:
                        self.wordFrequency[word] += 1
                    
                    else:
                        self.wordFrequency[word] = 1
        else:
            value_mode = {
                "t" : 60,
                "h1" : 50,
                "h2" : 50,
                "h3" : 50,
                "b" : 30,
                "s" : 30,
            }
            for mode, content in tokens:
                tokenSet = set()
                text = ''
                for word in content:
                    for ch in word:
                        if (ch.isalnum() or ch == "'"):
                            text += ch
                        elif (len(text) >= 2):
                            tokenSet.add(text)
                            text = ''
                        else:
                            text = ''
                    if (len(text) >= 2):
                        tokenSet.add(text)
                    text = ''
                for word in tokenSet:
                    if len(word) >= 2 and word.isalnum():
                        self.numOfTerms += value_mode[mode]
                        word = word.lower()
                        if word in self.wordFrequency:
                            self.wordFrequency[word] += value_mode[mode]
                        else:
                            self.wordFrequency[word] = value_mode[mode]
                
    
    def write_to_file(self, numFiles, numDir,mode="index"):
        #path = os.getcwd() + f'/TEMP/DIR{numDir}'
        path = os.path.join(os.getcwd(),"TEMP")
        if mode == "wfd": #Default, must change specification. This portion deals with helping make the wordDocFreq.txt which is used to calculate idf. Only need to call this when wordDocFreq.txt is missing.
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + f'/file{numFiles}.txt', mode="w") as file:
                for i in sorted(self.wordFrequency.keys()):
                    try:
                        file.write(f"{i}|")          
                    except:
                        pass
                    
        elif mode == "index":
            #if not os.path.isdir(path):
            #    os.mkdir(path)
            with open(os.path.join(path,f'file{numFiles}.json'), mode="w", buffering=1) as file:
                jsonObj = dict()
                for i,j in self.wordFrequency.items():
                    try:
                        value = self.calculate_tfidf(t=j, 
                                            numOfDwithT= self.globalDict[i], 
                                            numOfTerms=self.numOfTerms, 
                                            numOfD=57381)
                        
                        pair = {"url":self.url, 
                            "tfidf":value}
                        
                        jsonObj[i] = [pair]
                    except:
                        pass
            
                json.dump(jsonObj, file, ensure_ascii=False)                  
                        
                    
    


                        
    
    def get_wordFrequencies(self):
        return self.wordFrequency
    
    
    
    #Cannot use until total number of documents have been counted for, as well as all words.
    def calculate_tfidf(self, t, numOfDwithT, numOfTerms, numOfD):
        numOfTerms = self.numOfTerms
        if(numOfDwithT == 0):
            numOfDwithT = 1
        tf = t/ int(numOfDwithT)
        idf = log10(numOfD/ int(numOfDwithT))
        return tf * idf



if __name__ == "__main__":
    jsonLine = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\n  \n  \n\n\n  <head>\n    <title>\n      cs222-2019-fall-git – Public\n    </title>\n      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n      <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\" />\n    <!--[if IE]><script type=\"text/javascript\">\n      if (/^#__msie303:/.test(window.location.hash))\n        window.location.replace(window.location.hash.replace(/^#__msie303:/, '#'));\n    </script><![endif]-->\n        <link rel=\"search\" href=\"/wiki/public/search\" />\n        <link rel=\"help\" href=\"/wiki/public/wiki/TracGuide\" />\n        <link rel=\"alternate\" href=\"/wiki/public/wiki/cs222-2019-fall-git?version=4&amp;format=txt\" type=\"text/x-trac-wiki\" title=\"Plain Text\" />\n        <link rel=\"up\" href=\"/wiki/public/wiki/cs222-2019-fall-git\" title=\"View latest version\" />\n        <link rel=\"next\" href=\"/wiki/public/wiki/cs222-2019-fall-git?version=5\" title=\"Version 5\" />\n        <link rel=\"start\" href=\"/wiki/public/wiki\" />\n        <link rel=\"stylesheet\" href=\"/wiki/public/chrome/common/css/trac.css\" type=\"text/css\" /><link rel=\"stylesheet\" href=\"/wiki/public/chrome/common/css/wiki.css\" type=\"text/css\" /><link rel=\"stylesheet\" href=\"/wiki/public/chrome/tracwysiwyg/wysiwyg.css\" type=\"text/css\" />\n        <link rel=\"tracwysiwyg.stylesheet\" href=\"/wiki/public/chrome/common/css/trac.css\" /><link rel=\"tracwysiwyg.stylesheet\" href=\"/wiki/public/chrome/tracwysiwyg/editor.css\" />\n        <link rel=\"tracwysiwyg.base\" href=\"/wiki/public\" />\n        <link rel=\"prev\" href=\"/wiki/public/wiki/cs222-2019-fall-git?version=3\" title=\"Version 3\" />\n        <link rel=\"shortcut icon\" href=\"/wiki/public/chrome/site/favicon.ico\" type=\"image/x-icon\" />\n        <link rel=\"icon\" href=\"/wiki/public/chrome/site/favicon.ico\" type=\"image/x-icon\" />\n    <style id=\"trac-noscript\" type=\"text/css\">.trac-noscript { display: none !important }</style>\n    <script type=\"text/javascript\">\n      var _tracwysiwyg={};\n    </script>\n      <script type=\"text/javascript\" charset=\"utf-8\" src=\"/wiki/public/chrome/common/js/jquery.js\"></script>\n      <script type=\"text/javascript\" charset=\"utf-8\" src=\"/wiki/public/chrome/common/js/babel.js\"></script>\n      <script type=\"text/javascript\" charset=\"utf-8\" src=\"/wiki/public/chrome/common/js/trac.js\"></script>\n      <script type=\"text/javascript\" charset=\"utf-8\" src=\"/wiki/public/chrome/common/js/search.js\"></script>\n      <script type=\"text/javascript\" charset=\"utf-8\" src=\"/wiki/public/chrome/common/js/folding.js\"></script>\n      <script type=\"text/javascript\" charset=\"utf-8\" src=\"/wiki/public/chrome/tracwysiwyg/wysiwyg.js\"></script>\n    <script type=\"text/javascript\">\n      jQuery(\"#trac-noscript\").remove();\n      jQuery(document).ready(function($) {\n        $(\".trac-autofocus\").focus();\n        $(\".trac-target-new\").attr(\"target\", \"_blank\");\n        setTimeout(function() { $(\".trac-scroll\").scrollToTop() }, 1);\n        $(\".trac-disable-on-submit\").disableOnSubmit();\n      });\n    </script>\n    <meta name=\"ROBOTS\" content=\"NOINDEX, NOFOLLOW\" />\n    <script type=\"text/javascript\">\n      jQuery(document).ready(function($) {\n        $(\"#content\").find(\"h1,h2,h3,h4,h5,h6\").addAnchor(_(\"Link to this section\"));\n        $(\"#content\").find(\".wikianchor\").each(function() {\n          $(this).addAnchor(babel.format(_(\"Link to #%(id)s\"), {id: $(this).attr('id')}));\n        });\n        $(\".foldable\").enableFolding(true, true);\n      });\n    </script>\n  </head>\n  <body>\n    <div id=\"banner\">\n      <div id=\"header\">\n        <a id=\"logo\" href=\"http://www.ics.uci.edu/\"><img src=\"/wiki/public/chrome/site/ics.jpg\" alt=\"ICS Logo\" height=\"67\" width=\"128\" /></a>\n      </div>\n      <form id=\"search\" action=\"/wiki/public/search\" method=\"get\">\n      </form>\n      <div id=\"metanav\" class=\"nav\">\n    <ul>\n      <li class=\"first\"><a href=\"/wiki/public/login\">Login</a></li><li><a href=\"/wiki/public/prefs\">Preferences</a></li><li class=\"last\"><a href=\"/wiki/public/about\">About Trac</a></li>\n    </ul>\n  </div>\n    </div>\n    <div id=\"mainnav\" class=\"nav\">\n  </div>\n    <div id=\"main\">\n      <div id=\"pagepath\" class=\"noprint\">\n  <a class=\"pathentry first\" title=\"View WikiStart\" href=\"/wiki/public/wiki\">wiki:</a><a class=\"pathentry\" href=\"/wiki/public/wiki/cs222-2019-fall-git\" title=\"View cs222-2019-fall-git\">cs222-2019-fall-git</a>\n</div>\n      <div id=\"ctxtnav\" class=\"nav\">\n        <h2>Context Navigation</h2>\n        <ul>\n          <li class=\"first\"><span>&larr; <a class=\"prev\" href=\"/wiki/public/wiki/cs222-2019-fall-git?version=3\" title=\"Version 3\">Previous Version</a></span></li><li><a href=\"/wiki/public/wiki/cs222-2019-fall-git\" title=\"View latest version\">View Latest Version</a></li><li class=\"last\"><span><a class=\"next\" href=\"/wiki/public/wiki/cs222-2019-fall-git?version=5\" title=\"Version 5\">Next Version</a> &rarr;</span></li>\n        </ul>\n        <hr />\n      </div>\n    <div id=\"content\" class=\"wiki\">\n        <br />\n        <table id=\"info\" summary=\"Revision info\">\n          <tr><th scope=\"row\">Version 4 (modified by yicongh1, <a class=\"timeline\" href=\"/wiki/public/timeline?from=2019-09-25T16%3A10%3A10-07%3A00&amp;precision=second\" title=\"See timeline at Sep 25, 2019 4:10:10 PM\">3 weeks ago</a>)\n             (<a href=\"/wiki/public/wiki/cs222-2019-fall-git?action=diff&amp;version=4\">diff</a>)</th></tr>\n          <tr><td class=\"message\">\n            <p>\n--\n</p>\n\n          </td></tr>\n        </table>\n      <div class=\"wikipage searchable\">\n        \n          <div id=\"wikipage\" class=\"trac-content\"><p>\nSuppose the CS222 team 99 contains 2 members (Bob and Alice). We will see how they use Git to collaborate in the CS222 class.\n</p>\n<h2 id=\"SettingupGit:\">Setting up Git:</h2>\n<ol><li>Each student creates a github account, and shares his/her github username with the CS222 staff on this <a class=\"ext-link\" href=\"https://docs.google.com/spreadsheets/d/1HAtNwwWw3GAqhmvuTKV05uCf3qFpb2KW2WrwQGxiXlc/edit#gid=0\"><span class=\"icon\">​</span>GitHub Username Sheet</a>.\n</li><li>Form a team on this <a class=\"ext-link\" href=\"https://docs.google.com/spreadsheets/d/1HAtNwwWw3GAqhmvuTKV05uCf3qFpb2KW2WrwQGxiXlc/edit#gid=761552949\"><span class=\"icon\">​</span>Team Signup Sheet</a>\n</li><li>Accepts the Assignment with this <a class=\"ext-link\" href=\"https://classroom.github.com/g/.\"><span class=\"icon\">​</span>link</a>\n</li><li>Type in the Team ID with this exactly format <tt>team-#</tt> where # is your team number on the Team Signup Sheet\n</li></ol><p>\n<a style=\"padding:0; border:none\" href=\"/wiki/public/attachment/wiki/cs222-2019-fall-git/accept-assignment.png\"><img width=\"600px\" src=\"/wiki/public/raw-attachment/wiki/cs222-2019-fall-git/accept-assignment.png\" /></a>\n</p>\n<ol start=\"4\"><li>Bob also needs to add the other member Alice to the repository as a collaborator (by following steps given <a class=\"ext-link\" href=\"https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/\"><span class=\"icon\">​</span>here</a>).\n</li></ol><h2 id=\"InitializingGitrepowithourcodebase:\">Initializing Git repo with our codebase:</h2>\n<ol><li>On his local machine, Bob installs a Git client by following the instructions <a class=\"ext-link\" href=\"https://git-scm.com/book/en/v2/Getting-Started-Installing-Git\"><span class=\"icon\">​</span>here</a>.\n</li><li>He then does the following:\n<pre class=\"wiki\">shell&gt; mkdir mycs222-projects\nshell&gt; cd mycs222-projects\nshell&gt; git clone https://&lt;Bob's username&gt;@github.com/UCI-Chenli-teaching/cs222-fall19-team-99.git     - Clone the repository you just created to your local machine\nshell&gt; cd cs222-fall19-team-99/\nshell&gt; git pull https://github.com/UCI-Chenli-teaching/cs222-fall19.git master --allow-unrelated-histories    - Pull our project codebase to your local machine and merge it to your local \"cs222-fall19-team-99\" repository\n</pre></li></ol><p>\nIf you have some commits to your repo before, git will open <tt>vim</tt> automatically for you to edit comments to resolve conflicts.\n</p>\n<pre class=\"wiki\">Just type \":q\" will use default message and complete the merging operation.\n</pre><p>\nOtherwise, simply ignore this step.\n</p>\n<p>\nNow you will see something like this:\n</p>\n<pre class=\"wiki\">From https://github.com/UCI-Chenli-teaching/cs222-fall19\n * branch            master     -&gt; FETCH_HEAD\nMerge made by the 'recursive' strategy.\n .gitignore/.gitignore |  32 ++++++++++++++++++++\n makefile.inc          |   8 +++++\n project1_report.txt   |  23 +++++++++++++++\n rbf/makefile          |  49 +++++++++++++++++++++++++++++++\n rbf/pfm.cc            |  88 +++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/pfm.h             |  52 +++++++++++++++++++++++++++++++++\n rbf/rbfm.cc           |  47 +++++++++++++++++++++++++++++\n rbf/rbfm.h            | 137 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest1.cc       |  50 +++++++++++++++++++++++++++++++\n rbf/rbftest10.cc      | 144 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest11.cc      | 114 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest12.cc      | 116 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest2.cc       |  46 +++++++++++++++++++++++++++++\n rbf/rbftest3.cc       |  62 +++++++++++++++++++++++++++++++++++++++\n rbf/rbftest4.cc       |  92 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest5.cc       |  96 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest6.cc       | 111 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest7.cc       | 144 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest8.cc       | 108 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nrbf/rbftest8b.cc      | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/rbftest9.cc       | 129 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n rbf/test_util.h       | 281 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n readme.txt            |  20 +++++++++++++\n 23 files changed, 2064 insertions(+)\n create mode 100644 .gitignore/.gitignore\n create mode 100644 makefile.inc\n create mode 100644 project1_report.txt\n create mode 100644 rbf/makefile\n create mode 100644 rbf/pfm.cc\n create mode 100644 rbf/pfm.h\n create mode 100644 rbf/rbfm.cc\n create mode 100644 rbf/rbfm.h\n create mode 100644 rbf/rbftest1.cc\n create mode 100644 rbf/rbftest10.cc\n create mode 100644 rbf/rbftest11.cc\n create mode 100644 rbf/rbftest12.cc\n create mode 100644 rbf/rbftest2.cc\n create mode 100644 rbf/rbftest3.cc\n create mode 100644 rbf/rbftest4.cc\n create mode 100644 rbf/rbftest5.cc\n create mode 100644 rbf/rbftest6.cc\n create mode 100644 rbf/rbftest7.cc\n create mode 100644 rbf/rbftest8.cc\n create mode 100644 rbf/rbftest8b.cc\n create mode 100644 rbf/rbftest9.cc\n create mode 100644 rbf/test_util.h\n create mode 100644 readme.txt\n</pre><p>\nNow you already have the whole code base merged to your local repository\n</p>\n<pre class=\"wiki\">shell&gt; git push          - Push the updated local repository to your remote \"cs222-fall19-team-99\" repository\n</pre><p>\nNow you will see something like this:\n</p>\n<pre class=\"wiki\">Counting objects: 31, done.\nDelta compression using up to 4 threads.\nCompressing objects: 100% (29/29), done.\nWriting objects: 100% (31/31), 14.95 KiB | 3.74 MiB/s, done.\nTotal 31 (delta 11), reused 0 (delta 0)\nremote: Resolving deltas: 100% (11/11), done.\nTo https://github.com/UCI-Chenli-teaching/cs222-fall19-team-99.git\n   3e7e4d2..f51d097  master -&gt; master\n</pre><p>\nNow it means your remote \"cs222-fall19-team-99\" repository has all the code in our codebase, and it's ready for you and your partner to work on the project based on that now!\n</p>\n<h2 id=\"UsingGittocollaborateonthisproject:\">Using Git to collaborate on this project:</h2>\n<ol start=\"3\"><li>Bob now wants to start on project 1. He creates a new branch from the master branch for this task.\n</li></ol><pre class=\"wiki\">shell&gt; git branch            - This command is used to check which branch you are on and what branches are there in your repository. master should be highlighted as you are on master branch. \nshell&gt; git checkout -b bob-feature1            - This command creates a new branch and copies all the code from the previous (i.e. master in our case) branch into the new branch. \nshell&gt; mkdir project1 \nshell&gt; cd project1 \nshell&gt; echo \"#include &lt;iostream&gt; using namespace std; int main() { cout &lt;&lt; \"Hello, World!\"; return 0; }\" &gt; hello.cpp \nshell&gt; git add hello.cpp \nshell&gt; git commit -m \"added hello world\"            - commits changes locally to the bob-feature1 branch \nshell&gt; git push --set-upstream origin bob-feature1            - creates a remote tracking branch for the local bob-feature1 branch\n</pre><ol start=\"4\"><li>Alice wants to contribute too. First Bob needs to invite Alice as a contributor to this repository on the Github web site (by following steps given <a class=\"ext-link\" href=\"https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/\"><span class=\"icon\">​</span>here</a>).  Then she can see the repository. She does the following:\n</li></ol><pre class=\"wiki\">shell&gt; mkdir gitclones \nshell&gt; cd gitclones \nshell&gt; git clone https://&lt;Alice's username&gt;@github.com/UCI-Chenli-teaching/cs222-fall19-team-99.git             - brings the repository onto her local machine \nshell&gt; cd cs222-fall19-team-99 \nshell&gt; git checkout bob-feature1             - She is initially on master branch. This statement changes her branch bob-feature1 branch. She can now see project 1 code and does the required changes. \nshell&gt; cd project1\nMODIFY THE FILE hello.cpp\nshell&gt; git add hello.cpp \nshell&gt; git status\nshell&gt; git config  user.email \"alince@alice.com\"\nshell&gt; git config  user.name \"Alice Smith\"\nshell&gt; git commit -m \"minor changes\" \nshell&gt; git push             - pushes the commit to bob-feature1 remote branch\n</pre><ol start=\"5\"><li>Bob wants to continue coding. Before proceeding to modify any files, he needs to do 'git pull' so that the local branch pulls the latest code from the remote branch.  In particular, Bob does:\n</li></ol><pre class=\"wiki\">shell&gt; git branch         - to see which branch he is on. He sees he is on bob-feature1 branch. \nshell&gt; git pull             - pulls the latest code. Bob now sees the changes that Alice pushed.\n</pre><ol start=\"6\"><li>Bob and Alice can also use github to create a pull request from the <tt>bob-feature1</tt> branch to the <tt>master</tt> branch to do code reviews. Check this <a class=\"ext-link\" href=\"https://www.youtube.com/watch?v=oFYyTZwMyAg\"><span class=\"icon\">​</span>video</a> to learn this process.\n</li></ol><p>\nRefer to following tutorials for more information:\n</p>\n<ul><li><a class=\"ext-link\" href=\"https://try.github.io\"><span class=\"icon\">​</span>https://try.github.io</a>\n</li><li><a class=\"ext-link\" href=\"https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners\"><span class=\"icon\">​</span>https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners</a>\n</li></ul></div>\n          \n          \n        \n        \n      </div>\n      \n    <div id=\"attachments\">\n        <h3 class=\"foldable\">Attachments <span class=\"trac-count\">(4)</span></h3>\n        <div>\n          <ul>\n              <li>\n    <a href=\"/wiki/public/attachment/wiki/cs222-2019-fall-git/create-repo-button.png\" title=\"View attachment\">create-repo-button.png</a><a href=\"/wiki/public/raw-attachment/wiki/cs222-2019-fall-git/create-repo-button.png\" class=\"trac-rawlink\" title=\"Download\">​</a>\n       (<span title=\"39282 bytes\">38.4 KB</span>) -\n      added by <em>yicongh1</em> <a class=\"timeline\" href=\"/wiki/public/timeline?from=2019-09-24T11%3A49%3A27-07%3A00&amp;precision=second\" title=\"See timeline at Sep 24, 2019 11:49:27 AM\">3 weeks ago</a>.\n              </li>\n              <li>\n    <a href=\"/wiki/public/attachment/wiki/cs222-2019-fall-git/create-repo-interface.png\" title=\"View attachment\">create-repo-interface.png</a><a href=\"/wiki/public/raw-attachment/wiki/cs222-2019-fall-git/create-repo-interface.png\" class=\"trac-rawlink\" title=\"Download\">​</a>\n       (<span title=\"197808 bytes\">193.2 KB</span>) -\n      added by <em>yicongh1</em> <a class=\"timeline\" href=\"/wiki/public/timeline?from=2019-09-24T11%3A51%3A47-07%3A00&amp;precision=second\" title=\"See timeline at Sep 24, 2019 11:51:47 AM\">3 weeks ago</a>.\n              </li>\n              <li>\n    <a href=\"/wiki/public/attachment/wiki/cs222-2019-fall-git/accept-assignment.png\" title=\"View attachment\">accept-assignment.png</a><a href=\"/wiki/public/raw-attachment/wiki/cs222-2019-fall-git/accept-assignment.png\" class=\"trac-rawlink\" title=\"Download\">​</a>\n       (<span title=\"46240 bytes\">45.2 KB</span>) -\n      added by <em>yicongh1</em> <a class=\"timeline\" href=\"/wiki/public/timeline?from=2019-09-25T16%3A06%3A06-07%3A00&amp;precision=second\" title=\"See timeline at Sep 25, 2019 4:06:06 PM\">3 weeks ago</a>.\n              </li>\n              <li>\n    <a href=\"/wiki/public/attachment/wiki/cs222-2019-fall-git/accept-assignment-second-member.png\" title=\"View attachment\">accept-assignment-second-member.png</a><a href=\"/wiki/public/raw-attachment/wiki/cs222-2019-fall-git/accept-assignment-second-member.png\" class=\"trac-rawlink\" title=\"Download\">​</a>\n       (<span title=\"11234 bytes\">11.0 KB</span>) -\n      added by <em>yicongh1</em> <a class=\"timeline\" href=\"/wiki/public/timeline?from=2019-09-25T16%3A52%3A08-07%3A00&amp;precision=second\" title=\"See timeline at Sep 25, 2019 4:52:08 PM\">3 weeks ago</a>.\n              </li>\n          </ul>\n          <p>\n            Download all attachments as: <a rel=\"nofollow\" href=\"/wiki/public/zip-attachment/wiki/cs222-2019-fall-git/\">.zip</a>\n          </p>\n        </div>\n    </div>\n\n    </div>\n    <div id=\"altlinks\">\n      <h3>Download in other formats:</h3>\n      <ul>\n        <li class=\"last first\">\n          <a rel=\"nofollow\" href=\"/wiki/public/wiki/cs222-2019-fall-git?version=4&amp;format=txt\">Plain Text</a>\n        </li>\n      </ul>\n    </div>\n    </div>\n    <div id=\"footer\" lang=\"en\" xml:lang=\"en\"><hr />\n      <a id=\"tracpowered\" href=\"http://trac.edgewall.org/\"><img src=\"/wiki/public/chrome/common/trac_logo_mini.png\" height=\"30\" width=\"107\" alt=\"Trac Powered\" /></a>\n      <p class=\"left\">Powered by <a href=\"/wiki/public/about\"><strong>Trac 1.0.13</strong></a><br />\n        By <a href=\"http://www.edgewall.org/\">Edgewall Software</a>.</p>\n      <p class=\"right\">Visit the Trac open source project at<br /><a href=\"http://trac.edgewall.org/\">http://trac.edgewall.org/</a></p>\n    </div>\n  </body>\n</html>"
    content = ContentExtractor("https://grape.ics.uci.edu/wiki/public/wiki/cs222-2019-fall-git?version=4", jsonLine, {})
    content.extract_content()
    #print(len(content.get_wordFrequencies()))
    
    path = os.path.join(os.getcwd(), "devTest", "grape_ics_uci_edu")
    start = time.time()
    for i in os.listdir(path):
        #print(f"Working on {i}")
        with open(os.path.join(path, i)) as file:
            data = file.read()
            obj = json.loads(data)
            url = obj["url"]
            webHTML = obj["content"]
            content = ContentExtractor(url=url, jsonLine = webHTML, globalDict = {})
            content.extract_content()
            #print("wordFreq:", content.wordFrequency)
    end = time.time()    
    print(end-start)
    
    #print(content.wordFrequency)
    
    
    
    
    
    
    
    
    
    
    
    