#!/usr/bin/python
from aptnotes import AptNotes
from argparse import ArgumentParser
import json
import os
import PyPDF2
import re
import socket
import struct
import StringIO
import sys
import tlds

class AptNotes2JaskApi(object):

    @staticmethod
    def makeMask(n):
        # return a mask of n bits as a long integer
        return (2L<<n-1) - 1

    @staticmethod
    def dottedQuadToNum(ip):
        # convert decimal dotted quad string to long integer

        # May be platform dependant, I = x64  (L for x32?)
        return struct.unpack('I',socket.inet_aton(ip))[0]

    @staticmethod
    def networkMask(ip,bits):
        # Convert a network address to a long integer
        return AptNotes2JaskApi.dottedQuadToNum(ip) & makeMask(bits)

    @staticmethod
    def addressInNetwork(ip,net):
       # Is an address in a network
       return ip & net == net

    @staticmethod
    def downloadPdfToFile(AptNotesReport, targetFileName):
        target = open(targetFileName, 'w')
        target.write(AptNotesReport.get_file_content())

    @staticmethod
    def extractTextFromPdf(pdfFilename):
        pdfFileObj = open(pdfFilename, 'rb')
        return AptNotes2JaskApi.extractTextFromPdfStream(pdfFileObj)

    @staticmethod
    def extractTextFromAptNotesPdf(AptNotesReport):
        stream = StringIO.StringIO()
        vprint("Getting file content...")
        stream.write(AptNotesReport.get_file_content())
        return AptNotes2JaskApi.extractTextFromPdfStream(stream)

    @staticmethod
    def extractTextFromPdfStream(stream):
        pdfText = []
        try:
            pypdf2Obj = PyPDF2.PdfFileReader(stream)
            pageCount = pypdf2Obj.numPages
        except (ValueError, PyPDF2.utils.PdfReadError) as ex:
            vprint("Error processing pdf: {}".format(ex))
            return ""
        currentPageNum = 0
        while currentPageNum < pageCount :
            page = pypdf2Obj.getPage(currentPageNum)
            vprint("Extracting text for page {}...".format(currentPageNum + 1))
            pageText = ""
            try:
                pageText = page.extractText()
            except KeyError:
                vprint("Error processing page {}".format(currentPageNum))
            cleanedText = AptNotes2JaskApi.cleanText(pageText)
            pdfText.append(cleanedText)
            currentPageNum += 1
        return "\n".join(pdfText)

    @staticmethod
    def cleanText(textToClean):
        cleanedText = textToClean
        # Since extracted text seems to have eroneous new-lines peppered in,
        # the below regex removes all individual newlines, but leaving in place
        # double new lines (paragraph breaks).
        cleanedText = re.sub(r'([^\n])\n([^\n])', r'\1\2', cleanedText, 0, re.MULTILINE)

        # Exchange strings that look like this:
        #   192.168.xxx.xxx 
        # to this:
        #   192.168.0.0/16
        cleanedText = re.sub(r'(\d{1,3}\.\d{1,3})\.x{1,3}\.x{1,3}', 
                             r'\1.0.0/16', 
                             cleanedText, 
                             0, 
                             re.IGNORECASE | re.MULTILINE)
       
        # same as above but for /24 - 3rd octet networks
        cleanedText = re.sub(r'(\d{1,3}\.\d{1,3}\.\d{1,3})\.x{1,3}', 
                             r'\1.0/24', 
                             cleanedText, 
                             0, 
                             re.IGNORECASE | re.MULTILINE)

        return cleanedText


    @staticmethod
    def isValidIpAddrString(ipString):
        try:
            AptNotes2JaskApi.dottedQuadToNum(ipString)
        except (socket.error, TypeError):
            return False
        return True

    @staticmethod
    def isValidIpCidrString(cidrString):
        try:
            (ip, netmask) =  re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})', cidrString)[0]
            netmask = int(netmask)
            if netmask < 0 or netmask > 32:
                raise Exception("CIDR bits {} out of range, must be lower than 32".format(netmask))
            if AptNotes2JaskApi.isValidIpAddrString(ip) == False:
                return False
        except Exception:
            return False
        return True


    @staticmethod
    def collectIpAddrsFromText(inString):
        # Returns a distinct list of valid ip addresses found in inString.
        # Ignores valid IP's that look like CIDR notation (e.g. won't identify 1.2.3.0/24)
        ipCandidates = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?!\/\d{1,2})', inString, re.MULTILINE)
        ipAddrs = {}
        for candidate in ipCandidates:
            if AptNotes2JaskApi.isValidIpAddrString(candidate):
                ipAddrs[candidate] = 1
        return ipAddrs.keys()

    @staticmethod
    def collectIpCidrsFromText(inString):
        # Returns a distinct list of valid CIDRs found in inString.
        # Ex: collectIpCidrsFromText("The 10.1.0.0/16 brown 192.168.0.0/16 jumped over the 1.2.3.4 dog.")
        #     Returns:  ["10.1.0.0/16", "192.168.0.0/16"]
        cidrCandidates = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})', inString, re.MULTILINE)
        cidrs = {}
        for candidate in cidrCandidates:
            if AptNotes2JaskApi.isValidIpCidrString(candidate):
                cidrs[candidate] = 1
        return cidrs.keys()

    @staticmethod
    def collectHostnamesFromText(inString):
        # Returns a distinct list of valid hostnames found in inString.
        # A valid hostname has this form: hostname.domain.tld
        hostnameCandidates = re.findall(r'.*?([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-]{2,}).*?', inString, re.MULTILINE)
        hostnames = {}
        for hostnameCandidate in hostnameCandidates:
            fields = hostnameCandidate.split('.')
            if tlds.isValidTld(fields[-1]):
                hostnames[hostnameCandidate] = 1
        return hostnames.keys()

    @staticmethod
    def collectEmailAddressesFromText(inString):
        # FIXME Check RFC for valid charachters in an email address name
        emailCandidates = re.findall(r'.*?([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-]{2,}).*?', inString,
                                     re.MULTILINE)
        emailAddresses = {}
        for emailCandidate in emailCandidates:
            (name, domain) = emailCandidate.split("@")
            if len(name) == 0 or len(domain) == 0:
                continue
            domainFields = domain.split('.')
            if tlds.isValidTld(domainFields[-1]) == False:
                continue
            if len(domainFields) < 2:
                continue
            emailAddresses[emailCandidate] = 1
        return emailAddresses.keys()

    @staticmethod
    def collectMd5DigestsFromText(inString):
        # len == 32 chars hex
        md5Candidates = re.findall(r'[^0-9A-Fa-f]([0-9A-Fa-f]{32})[^0-9A-Fa-f]', inString,
                                     re.MULTILINE)
        md5s = {}
        for md5Candidate in md5Candidates:
            # Validation here.  How can you tell if an md5 is valid? Hmmmm...
            md5s[md5Candidate] = 1
        return md5s.keys()

    @staticmethod
    def collectSha1DigestsFromText(inString):
        # len = 40 ad67d0c3ecdd4e61a2baa422508e2215257a8730
        sha1Candidates = re.findall(r'[^0-9A-Fa-f]([0-9A-Fa-f]{40})[^0-9A-Fa-f]', inString,
                                     re.MULTILINE)
        sha1s = {}
        for sha1Candidate in sha1Candidates:
            # Validation here.  How can you tell if a SHA1 is valid? Hmmmm...
            sha1s[sha1Candidate] = 1
        return sha1s.keys()

    @staticmethod
    def collectSha256DigestsFromText(inString):
        # len = 64 bd8b897ceacb5da5e2c4e08f53dec2150a4ec59998d55c43131c07b0bf08c0d8
        sha256Candidates = re.findall(r'[^0-9A-Fa-f]([0-9A-Fa-f]{64})[^0-9A-Fa-f]', inString,
                                     re.MULTILINE)
        sha256s = {}
        for sha256Candidate in sha256Candidates:
            # Validation here.  How can you tell if a SHA256 is valid? Hmmmm...
            sha256s[sha256Candidate] = 1
        return sha256s.keys()

__VERBOSITY__ = 1
def vprint(message):
    if __VERBOSITY__ > 0:
        print >> sys.stderr, message

def crawlAptNotes():
    reportNum = 0
    for report in AptNotes.get_reports():
        reportNum += 1
        print ""
        print "#########################################################################"
        print "Report {}".format(reportNum)
        print "box_file_id {}".format(report.box_file_id)
        print "box_shared_name {}".format(report.box_shared_name)
        print "date {}".format(report.date)
        print "filename {}".format(report.filename)
        print "link {}".format(report.link)
        print "md5 {}".format(report.md5)
        print "sha256 {}".format(report.sha256)
        print "source {}".format(report.source)
        print "title {}".format(report.title)
        print "year {}".format(report.year)
        print "#########################################################################"
        print()
        #ans = raw_input("Process report(P), Save report(W), all other responses will skip: ")
        ans = 'w'
        if ans.lower() == 'p':
            vprint("Extracting text...")
            extractedText  = AptNotes2JaskApi.extractTextFromAptNotesPdf(report)

            ipAddrs        = AptNotes2JaskApi.collectIpAddrsFromText(extractedText)
            ipCidrs        = AptNotes2JaskApi.collectIpCidrsFromText(extractedText)
            hostnames      = AptNotes2JaskApi.collectHostnamesFromText(extractedText)
            emailAddresses = AptNotes2JaskApi.collectEmailAddressesFromText(extractedText)
            md5Digests     = AptNotes2JaskApi.collectMd5DigestsFromText(extractedText)
            sha1Digests    = AptNotes2JaskApi.collectSha1DigestsFromText(extractedText)
            sha256Digests  = AptNotes2JaskApi.collectSha256DigestsFromText(extractedText)
            # FIXME  RFC 1918 and other reserved space ip's (loopback etc.) should NOT be included as threat intel
            print "Extracted IP addresses:\n{}".format("\n".join(ipAddrs))
            print "Extracted CIDRs:\n{}".format("\n".join(ipCidrs))
            print "Extracted hostnames:\n{}".format("\n".join(hostnames))
        elif ans.lower() == 'w':
            AptNotes2JaskApi.downloadPdfToFile(report, "pdfRepo/{}.pdf".format(report.filename))
            metaFile = open("pdfRepo/{}.pdf.meta".format(report.filename), 'w')
            meta = {"jask_report_num": reportNum,
                    "box_file_id": report.box_file_id,
                    "box_shared_name": report.box_shared_name,
                    "date": report.date,
                    "filename": report.filename,
                    "link": report.link,
                    "md5": report.md5,
                    "sha256": report.sha256,
                    "source": report.source,
                    "title": report.title,
                    "year": report.year}
            metaFile.write(json.dumps(meta, indent=4))
        else:
            print "Skipping..."

def crawlDirectory(directory):
    print "filename,ipaddr,ipCidr,hostname,emailAddress,md5,sha1,sha256"
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if re.search(r"\.pdf$", file_name):
                vprint("Processing {}".format(os.path.join(root,file_name)))
                extractedText  = AptNotes2JaskApi.extractTextFromPdf(os.path.join(root,file_name))

                ipAddrs        = AptNotes2JaskApi.collectIpAddrsFromText(extractedText)
                ipCidrs        = AptNotes2JaskApi.collectIpCidrsFromText(extractedText)
                hostnames      = AptNotes2JaskApi.collectHostnamesFromText(extractedText)
                emailAddresses = AptNotes2JaskApi.collectEmailAddressesFromText(extractedText)
                md5Digests     = AptNotes2JaskApi.collectMd5DigestsFromText(extractedText)
                sha1Digests    = AptNotes2JaskApi.collectSha1DigestsFromText(extractedText)
                sha256Digests  = AptNotes2JaskApi.collectSha256DigestsFromText(extractedText)
                for ipAddr in ipAddrs:
                    print "{},{},,,,,,".format(os.path.join(root,file_name), ipAddr)
                for ipCidr in ipCidrs:
                    print "{},,{},,,,,".format(os.path.join(root,file_name), ipCidr)
                for hostname in hostnames:
                    print "{},,,{},,,,".format(os.path.join(root,file_name), hostname)
                for email in emailAddresses:
                    print "{},,,,{},,,".format(os.path.join(root,file_name), email)
                for md5 in md5Digests:
                    print "{},,,,,{},,".format(os.path.join(root,file_name), md5)
                for sha1 in sha1Digests:
                    print "{},,,,,,{},".format(os.path.join(root,file_name), sha1)
                for sha256 in sha1Digests:
                    print "{},,,,,,,{}".format(os.path.join(root,file_name), sha256)

class JaskTridentThreatUpload(object):
    import logging, re, sys
    import requests
    from argparse import ArgumentParser
    from os.path import abspath, basename

    logger = logging.getLogger(__name__)

    BATCH_SIZE = 250
    def __init__(self, username, api_key):
        self.__username__ = username
        self.__api_key__ = api_key
 
    def submit_intel(self, cluster, intel):
        params = {'username': self.__username__, 'api_key': self.__api_key__}
        url = 'https://%s/api/intelligence' % cluster
        response = requests.post(url, json={'objects': intel}, params=params, verify=False)
        response.raise_for_status()

    def threat_intel_from_file(self, cluster, filename, confidence, source):
        intel = []
        with open(abspath(filename), 'r') as f:
          for line in f.readlines():
            intel.append({'value': line.strip(), 'confidence': confidence, 'source': source})
            if len(intel) == BATCH_SIZE:
              submit_intel(cluster, self.__username__, self.__api_key__, intel)
              intel = []
        if intel: submit_intel(cluster, self.__username__, self.__api_key__, intel)    



if __name__ == "__main__":
    parser = ArgumentParser(description='Extract intel from pdfFiles and load into Trident.')
    parser.add_argument('--pdfDirectory', help='Directory to find PDF files to process')
    parser.add_argument('--username', help='username to use when accessing the api')
    parser.add_argument('--api_key', help='password to authenticate with')
    parser.add_argument('--file', help='file from which to import indicators')
    parser.add_argument('--confidence', help='Confidence in the indicator - High/Medium/Low')
    parser.add_argument('--source', help='Source of the indicators, i.e. PhishTank')
    #crawlAptNotes()
    crawlDirectory("pdfRepo")



