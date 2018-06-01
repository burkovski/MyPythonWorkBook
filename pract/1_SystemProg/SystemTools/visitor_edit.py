"""
Порядок использования: 'python ...\Tools\visitor_edit.py string rootdir?'.
Добавляет подкласс класса SearchVisitor, который автоматически запускает
текстовый редактор. В процессе обхода автоматически открывает в текстовом
редакторе файлы, содержащие искомую строку; в Windows можно также использовать
editor='edit' или 'notepad'; чтобы воспользоваться текстовым редактором,
реализация которого будет представлена далее в книге, попробуйте r'python Gui\
TextEditor\textEditor.py'; при работе с некоторыми редакторами можно было бы
передать команду перехода к первому совпадению с искомой строкой;
"""

import os
import sys
from visitor import SearchVisitor


class EditVisor(SearchVisitor):
    """
    открывает для редактирования файлы, содержащие искомую строку и
    находящиеся в каталоге startDir и ниже
    """
    editor = r"C:\Program Files (x86)\Sublime Text 3\sublime_text.exe"

    def visit_match(self, fpath, text):
        os.system('"{}" {}'.format(self.editor, fpath))


if __name__ == '__main__':
    visitor = EditVisor(sys.argv[1])
    visitor.run('.' if len(sys.argv) < 3 else sys.argv[2])
    print("Edited {} files, visited {}".format(
        visitor.scount,
        visitor.fcount
    ))
