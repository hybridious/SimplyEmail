#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import configparser
from BeautifulSoup import BeautifulSoup
from Helpers import Parser
from Helpers import helpers
import time

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue


# https://gist.github.com/search?utf8=✓&q=%40enron.com&ref=searchresults

class ClassName:

    def __init__(self, domain):
        self.name = "Searching GitHubGist Code"
        self.description = "Search GitHubGist code for emails using a large pool of code searches"
        self.domain = domain
        config = configparser.ConfigParser()
        self.Html = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.Depth = int(config['GitHubGistSearch']['PageDepth'])
            self.Counter = int(config['GitHubGistSearch']['QueryStart'])
        except:
            print helpers.color("[*] Major Settings for GitHubGistSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput = self.get_emails()
        return FinalOutput

    def process(self):
        # Get all the USER code Repos
        # https://github.com/search?p=2&q=enron.com+&ref=searchresults&type=Code&utf8=✓
        UrlList = []
        while self.Counter <= self.Depth:
            try:
                # search?p=2&q=%40enron.com&ref=searchresults&utf8=✓
                url = "https://gist.github.com/search?p=" + str(self.Counter) + "&q=%40" + \
                    str(self.domain) + "+&ref=searchresults&utf8=✓"
                r = requests.get(url, timeout=5)
                if r.status_code != 200:
                    break
            except Exception as e:
                error = "[!] Major isself.Counter += 1sue with GitHubGist Search:" + str(e)
                print helpers.color(error, warning=True)
            RawHtml = r.content
            # Parse the results for our URLS)
            soup = BeautifulSoup(RawHtml)
            for a in soup.findAll('a', href=True):
                a = a['href']
                if a.startswith('/'):
                    UrlList.append(a)
            self.Counter += 1
        # Now take all gathered URL's and gather the HTML content needed
        for Url in UrlList:
            try:
                Url = "https://gist.github.com" + Url
                html = requests.get(Url, timeout=2)
                self.Html += html.content
            except Exception as e:
                error = "[!] Connection Timed out on GithubGist Search:" + str(e)
                print helpers.color(error, warning=True)

    def get_emails(self):
    	Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        return FinalOutput
