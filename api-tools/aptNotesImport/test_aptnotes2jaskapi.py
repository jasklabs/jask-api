from aptnotes2jaskapi import AptNotes2JaskApi
import unittest

class TestAptNotes2JaskApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_isValidIpAddrString(self):
        assert AptNotes2JaskApi.isValidIpAddrString("192.168.1.1") is True
        assert AptNotes2JaskApi.isValidIpAddrString("256.0.0.0") is False
        assert AptNotes2JaskApi.isValidIpAddrString("Foo") is False
        assert AptNotes2JaskApi.isValidIpAddrString(123) is False

    def test_isValidIpCidrString(self):
        self.assertTrue(AptNotes2JaskApi.isValidIpCidrString("192.168.0.0/16"))
        self.assertFalse(AptNotes2JaskApi.isValidIpCidrString("258.168.0.0/16"))
        self.assertFalse(AptNotes2JaskApi.isValidIpCidrString("258.168.0.0/60"))
        self.assertFalse(AptNotes2JaskApi.isValidIpCidrString("foo/bar"))

    def test_collectIpCidrsFromText(self):
        testString1 = "The 10.0.0.0/8 network does not contain 192.168.1.10."
        self.assertListEqual(AptNotes2JaskApi.collectIpCidrsFromText(testString1),
                             ['10.0.0.0/8'])
        testString2 = "The 10.0.0.0/8 CIDR is technically invalid."
        self.assertListEqual(AptNotes2JaskApi.collectIpCidrsFromText(testString2),
                             ['10.0.0.0/8'])

    def test_collectIpAddrsFromText(self):
        testString1 = "This is a string with an IP address 10.45.128.99 in it."
        self.assertListEqual(AptNotes2JaskApi.collectIpAddrsFromText(testString1),
                             ['10.45.128.99'])

        testString2 = "This is a string with an invalid IP address 10.455.128.99 in it."
        self.assertListEqual(AptNotes2JaskApi.collectIpAddrsFromText(testString2),
                             [])

    def test_collectHostnamesFromText(self):
        testString1 = "Here's a couple hostnames for you www.google.com, www.jask.io. Yeah?"
        self.assertListEqual(AptNotes2JaskApi.collectHostnamesFromText(testString1),
                             ['www.jask.io', 'www.google.com'])

    def test_collectEmailAddressesFromText(self):
        testString1 = "You should send an email to: lovetests@yougotthatright.com."
        self.assertListEqual(AptNotes2JaskApi.collectEmailAddressesFromText(testString1),
                             ['lovetests@yougotthatright.com'])
        testString2 = "You should send an email to: lovetests@invalidtld.123abcfake."
        self.assertListEqual(AptNotes2JaskApi.collectEmailAddressesFromText(testString2),
                             [])

    def test_collectMd5DigestsFromText(self):
        testString1 = "Here's a hash: 3c2364fc0b6133508d20e9336EB7b6e7.  What up?"
        self.assertListEqual(AptNotes2JaskApi.collectMd5DigestsFromText(testString1),
                             ['3c2364fc0b6133508d20e9336EB7b6e7'])

        testString2 = "Here's almost a hash: FFF3c2364fc0b6133508d20e9336eb7b6e7.  What up?"
        self.assertListEqual(AptNotes2JaskApi.collectMd5DigestsFromText(testString2),
                             [])

    def test_collectSha1DigestsFromText(self):
        testString1 = "Sha1?  sure: ad67d0c3ecdd4e61a2BAA422508e2215257a8730.  Sup?"
        self.assertListEqual(AptNotes2JaskApi.collectSha1DigestsFromText(testString1),
                             ['ad67d0c3ecdd4e61a2BAA422508e2215257a8730'])

        testString2 = "Here's almost a hash: FFFad67d0c3ecdd4e61a2BAA422508e2215257a8730 done"
        self.assertListEqual(AptNotes2JaskApi.collectMd5DigestsFromText(testString2),
                             [])

    def test_collectSha256DigestsFromText(self):
        testString1 = "Sha256?  sure: bd8b897ceacb5da5e2c4e08f53dec2150a4ec59998d55c43131c07b0bf08c0d8 lol."
        self.assertListEqual(AptNotes2JaskApi.collectSha256DigestsFromText(testString1),
                             ['bd8b897ceacb5da5e2c4e08f53dec2150a4ec59998d55c43131c07b0bf08c0d8'])

        testString2 = "Here's almost a hash: FFFbd8b897ceacb5da5e2c4e08f53dec2150a4ec59998d55c43131c07b0bf08c0d8 done"
        self.assertListEqual(AptNotes2JaskApi.collectMd5DigestsFromText(testString2),
                             [])




























