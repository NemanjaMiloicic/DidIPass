from attr import dataclass
FILE_PATH = "latest_topic.txt"
IMAGE_PATH = "latest_topic.png"
DEFAULT_TIMEOUT = 10
LINK = "https://cs.elfak.ni.ac.rs/nastava/mod/forum/view.php?id=12160"
REPORT_FILE = "reports/report.txt"
@dataclass
class XPaths:
    OPENID = "//a[@title='OpenID Connect']"
    EMAIL = "//input[@type='email']"
    NEXT = "//input[@type='submit' and @value='Next']"
    PASSWORD = "//input[@type='password']"
    SIGN_IN = "//input[@type='submit' and @value='Sign in']"
    NO = "//input[@type='button' and @value='No']"
    DISCUSSION = "(//tr[contains(@class,'discussion') and contains(@class,'subscribed')]//a[@title])[2]"
XPATHS = XPaths()