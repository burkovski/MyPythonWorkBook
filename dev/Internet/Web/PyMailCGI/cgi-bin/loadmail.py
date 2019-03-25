import sys
import secret

from mailtools.mailfetcher import SilentMailFetcher, MailFetcherAuthError
from commonhtml import run_silent, error_page


def progress(now, total):
    sys.stderr.write("{} of {}".format(now, total))


def load_mail_headers(host, user, password):
    fetcher = SilentMailFetcher(host)
    fetcher.user = user
    fetcher.password = password
    hdrs, sizes, flg = fetcher.download_all_headers()
    return hdrs
