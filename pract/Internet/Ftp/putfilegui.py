"""
############################################################################
запускает функцию FTP putfile из многократно используемого класса формы
графического интерфейса; см. примечания в getfilegui: справедливыми
остаются большинство тех же предупреждений; формы для получения
и отправки выделены в единый класс, чтобы производить изменения
лишь в одном месте;
############################################################################
"""

from tkinter import Tk
import getfilegui
import putfile


class FtpPutFileForm(getfilegui.FtpForm):
    title = "FtpPutFileGui"
    mode = "Upload"
    def do_transfer(self, file_name, server_name, remote_dir, user_info):
        putfile.putfile(file_name, server_name, remote_dir, user_info,
                        verbose=False)


if __name__ == "__main__":
    root = Tk()
    FtpPutFileForm(root)
    root.mainloop()
