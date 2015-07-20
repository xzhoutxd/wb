#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(r'../')
import re
import json
import time
import base.Common as Common
import base.Config as Config
from base.MyCrawler import MyCrawler
from db.MysqlAccess import MysqlAccess

import warnings
warnings.filterwarnings("ignore")

import cookielib;
import urllib;
import urllib2;
import optparse;

class Weibo():
    def __init__(self):
        # 抓取设置
        self.crawler     = MyCrawler()

        # db
        self.mysqlAccess  = MysqlAccess() # mysql access

        self.home_url   = 'http://www.weibo.com'
        self.refers     = None
 
    #------------------------------------------------------------------------------
    # check all cookies in cookiesDict is exist in cookieJar or not
    def checkAllCookiesExist(self, cookieNameList, cookieJar) :
        cookiesDict = {};
        for eachCookieName in cookieNameList :
            cookiesDict[eachCookieName] = False;
         
        allCookieFound = True;
        for cookie in cookieJar :
            if(cookie.name in cookiesDict) :
                cookiesDict[cookie.name] = True;
         
        for eachCookie in cookiesDict.keys() :
            if(not cookiesDict[eachCookie]) :
                allCookieFound = False;
                break;
     
        return allCookieFound;
     
    #------------------------------------------------------------------------------
    # just for print delimiter
    def printDelimiter(self):
        print '-'*80;

    #------------------------------------------------------------------------------
    # main function to emulate login weibo
    def emulateLoginWeibo(self):
        #print "Function: Used to demostrate how to use Python code to emulate login baidu main page: http://www.baidu.com/";
        print "Function: Used to demostrate how to use Python code to emulate login weibo main page: http://www.weibo.com/";
        print "Usage: emulate_login_baidu_python.py -u yourBaiduUsername -p yourBaiduPassword";
        self.printDelimiter();
     
        # parse input parameters
        parser = optparse.OptionParser();
        parser.add_option("-u","--username",action="store",type="string",default='',dest="username",help="Your Baidu Username");
        parser.add_option("-p","--password",action="store",type="string",default='',dest="password",help="Your Baidu password");
        (options, args) = parser.parse_args();
        # export all options variables, then later variables can be used
        for i in dir(options):
            exec(i + " = options." + i);
     
        self.printDelimiter();
        print "[preparation] using cookieJar & HTTPCookieProcessor to automatically handle cookies";
        cj = cookielib.CookieJar();
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
        urllib2.install_opener(opener);
     
        self.printDelimiter();
        print "[step1] to get cookie BAIDUID";
        #baiduMainUrl = "http://www.baidu.com/";
        weiboMainUrl = "http://www.weibo.com/";
        resp = urllib2.urlopen(weiboMainUrl);
        ##respInfo = resp.info();
        ##print "respInfo=",respInfo;
        for index, cookie in enumerate(cj):
            print '[',index, ']',cookie;

        #weiboMainUrl = "http://www.weibo.com/";
        #resp = self.crawler.getData(self.home_url, self.refers)
        #print self.crawler.crawl_cookie
        #print self.crawler.use_cookie

        #'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1437328448784'

        #sinaSSOController.preloginCallBack({"retcode":0,"servertime":1437328448,"pcid":"xd-6be37d0294b7df46a80622b0228c20db9a1d","nonce":"B5ZSX8","pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443","rsakv":"1330428213","uid":"1000261474969","exectime":5})
        #sinaSSOController.preloginCallBack({"retcode":0,"servertime":1437329624,"pcid":"xd-6b1ff63f2ceb7afd9521c719c1d9a60d68a3","nonce":"6OM1IT","pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443","rsakv":"1330428213","showpin":0,"exectime":9}) 
     
        """
        self.printDelimiter();
        print "[step2] to get token value";
        getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true";
        getapiResp = urllib2.urlopen(getapiUrl);
        #print "getapiResp=",getapiResp;
        getapiRespHtml = getapiResp.read();
        #print "getapiRespHtml=",getapiRespHtml;
        #bdPass.api.params.login_token='5ab690978812b0e7fbbe1bfc267b90b3';
        foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)';", getapiRespHtml);
        if(foundTokenVal):
            tokenVal = foundTokenVal.group("tokenVal");
            print "tokenVal=",tokenVal;
     
            self.printDelimiter();
            print "[step3] emulate login baidu";
            staticpage = "http://www.baidu.com/cache/user/html/jump.html";
            baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login";
            postDict = {
                #'ppui_logintime': "",
                'charset'       : "utf-8",
                #'codestring'    : "",
                'token'         : tokenVal, #de3dbf1e8596642fa2ddf2921cd6257f
                'isPhone'       : "false",
                'index'         : "0",
                #'u'             : "",
                #'safeflg'       : "0",
                'staticpage'    : staticpage, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
                'loginType'     : "1",
                'tpl'           : "mn",
                'callback'      : "parent.bdPass.api.login._postCallback",
                'username'      : username,
                'password'      : password,
                #'verifycode'    : "",
                'mem_pass'      : "on",
            };
            postData = urllib.urlencode(postDict);
            # here will automatically encode values of parameters
            # such as:
            # encode http://www.baidu.com/cache/user/html/jump.html into http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            #print "postData=",postData;
            req = urllib2.Request(baiduMainLoginUrl, postData);
            # in most case, for do POST request, the content-type, is application/x-www-form-urlencoded
            req.add_header('Content-Type', "application/x-www-form-urlencoded");
            resp = urllib2.urlopen(req);
            #for index, cookie in enumerate(cj):
            #    print '[',index, ']',cookie;
            cookiesToCheck = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID'];
            loginBaiduOK = self.checkAllCookiesExist(cookiesToCheck, cj);
            if(loginBaiduOK):
                print "+++ Emulate login baidu is OK, ^_^";
            else:
                print "--- Failed to emulate login baidu !"
        else:
            print "Fail to extract token value from html=",getapiRespHtml;
        """
 
if __name__=="__main__":
    w = Weibo()
    w.emulateLoginWeibo();
