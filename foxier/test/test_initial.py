import unittest
from .context import prepare_requestWWF as pRWWF


goodUserName = ''
goodPass = ''


class UserAccessTokenLoginValidation(unittest.TestCase):
    """A bit much, but just setting up Test framework"""
    def test_emailValidationNotDot(self):
        badUserName = u'Not@tryingAtAll'
        password = u'fdfadf'
        self.assertRaises(
            pRWWF.InvalidEmailException,
            pRWWF.accessFactory,
            badUserName, password)

    def test_emailValidationNoAt(self):
        badUserName = u"DidntAt.com"
        password = u'fdfadf'
        self.assertRaises(
            pRWWF.InvalidEmailException,
            pRWWF.accessFactory,
            badUserName, password)

    def test_GoodUserName(self):  # Make AccessToken CLass public
        goodUserName = u'swaggie@dunk.com'
        password = u'fdfadf'
        retriever = pRWWF.accessFactory(goodUserName, password)
        self.assertTrue(
            retriever, "AccessTokenRetriever class failed to be created")
        retriever.driver.quit()

    @unittest.skip("Username and pass must be valid")
    def test_getAccessToken(self):  # Obsolete this just a placeholder
        retriever = pRWWF.accessFactory(goodUserName, goodPass)
        accessCode = retriever.getTokenWWF()
        self.assertIsInstance(accessCode, str)
        accessCode.driver.quit()

    def test_parseSignedRequest(self):
        goodUserName = u'swaggie@dunk.com'
        password = u'fdfadf'
        sampleOuth = 'v3cQGeSBQuMphpwrdxNjt6fL3b-xw9U_u1p4W76DVXE.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImV4cGlyZXMiOjE0Njc1MjIwMDAsImlzc3VlZF9hdCI6MTQ2NzUxNjI1Niwib2F1dGhfdG9rZW4iOiJFQUFDWkFJNVdnTzRRQkFIYlFrREJmbGxvSU5OU0FXdGJMVW9BU2VkTGZ6aEY5UXUwMVZIZ1dDNVVoN3NKRk54cjA0VVpDQU90T25lTkpNcXhQZTcyeDdVcE13dG5NN1pCSUVVN0w1djBhc2JNczVKaW5YOTlaQVFQWkIzbW5OS25iam9MRlpCalE0emxxQ3h6V1RWalIyN2tOcFBWVGVjdzJoZFlqUXQ2NEhQUVpEWkQiLCJ0b2tlbl9mb3JfYnVzaW5lc3MiOiJBYndwY0kwYXRTdk5pVDFtIiwidXNlciI6eyJjb3VudHJ5IjoidXMiLCJsb2NhbGUiOiJlbl9VUyIsImFnZSI6eyJtaW4iOjIxfX0sInVzZXJfaWQiOiIxMDIwMzM4MzU5ODgxMjYwMCJ9'
        retriever = pRWWF.accessFactory(goodUserName, password)
        result = retriever.parseToken(sampleOuth)
        self.assertEqual(result, dict())


class SolverInAction(unittest.TestCase):
    """
    Unit test covering Solver
    """
    pass


if __name__ == '__main__':
    unittest.main()
