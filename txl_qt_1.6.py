# coding=utf-8

import sys
from PyQt4 import QtGui, QtCore
import MySQLdb
from xpinyin import Pinyin
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore

reload(sys)
sys.setdefaultencoding('utf-8')  # 解决无法输入中文的情况 http://zsl-oo7.blog.163.com/blog/static/353297032012420105949468/
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(160, 900)
        # 表格布局，用来布局QLabel和QLineEdit及QSpinBox
        grid = QtGui.QGridLayout()
        self.setWindowTitle(u"输入信息")
        grid.addWidget(QtGui.QLabel(u'姓名', parent=self), 0, 0, 1, 1)
        self.nameInputEdit = QtGui.QLineEdit(parent=self)
        self.nameInputEdit.textChanged.connect(self.inputName)
        grid.addWidget(self.nameInputEdit, 0, 1, 1, 1)
        grid.addWidget(QtGui.QLabel(u'电话', parent=self), 1, 0, 1, 1)
        self.passwordInputEdit = QtGui.QLineEdit(parent=self)
        self.passwordInputEdit.textChanged.connect(self.inputPassword)
        grid.addWidget(self.passwordInputEdit, 1, 1, 1, 1)

        # 创建ButtonBox，用户确定和取消
        buttonBox = QtGui.QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)  # 确定和取消两个按钮

        # 连接信号和槽
        buttonBox.accepted.connect(self.clickOkBtn)  # 确定
        buttonBox.rejected.connect(self.clickCancleBtn)  # 取消
        layout = QtGui.QVBoxLayout()

        # 加入前面创建的表格布局
        layout.addLayout(grid)
        # ButtonBox
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def inputName(self, text):
        try:
            self.name = text
        except:
            print "www"

    def inputPassword(self, text):
        try:
            self.password = text
        except:
            print "wawa"

    def clickOkBtn(self):
        self.close()

    def clickCancleBtn(self):
        self.close()

    def insert(self):
        conn = self.init_db()
        cur = conn.cursor()
        sqli = "insert into 35txl values(%s,%s,%s,%s)"  # 35txl为表名
        id = self.auto_id()
        name = self.name
        tel = self.password
        shortname = "hehe"
        cur.execute(sqli, (id, name, tel, shortname))
        cur.close()
        conn.commit()
        conn.close()
        self.insert_shortname()  # 此处是正确的 无需修改

    def auto_id(self):
        conn = self.init_db()
        cur = conn.cursor()
        row = cur.execute("select * from 35txl")
        cur.close()
        conn.commit()
        conn.close()
        z = row + 1
        return z

    def insert_shortname(self):  # 一次性产生全部用户的拼音首字母大写
        conn = self.init_db()
        cur = conn.cursor()
        row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
        x = cur.fetchall()
        p = Pinyin()
        sqli = "update 35txl set shortname=%s where id=%s"  # 35txl为表名
        i = 0
        while (i < row):
            shortname = p.get_initials(x[i][1], u'')
            i = i + 1
            cur.execute(sqli, (shortname, i))
        cur.close()
        conn.commit()
        conn.close()

    def init_db(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            db='test',
            charset="utf8",  # 确保没有乱码
            passwd='root'
        )
        return conn


class LoginBox(QtGui.QWidget):
    def __init__(self):
        super(LoginBox, self).__init__()
        self.initUI()
        # self.resize(399,310)#s设置窗口的大小 可调整大小
        self.setFixedSize(399, 310)  # s设置窗口的大小 不可调整大小

    def initUI(self):
        vBoxLayout = QtGui.QHBoxLayout()
        self.browser = QTextBrowser()
        vBoxLayout.addWidget(self.browser)  # 添加一个显示栏
        self.browser.setFont(QtGui.QFont("lisu", 19))  # 设置字体
        hBoxLayout = QtGui.QGridLayout()
        Btn1 = QtGui.QPushButton(u"1.根据名字查询电话", self)
        Btn2 = QtGui.QPushButton(u"2.根据电话查询名字", self)
        Btn3 = QtGui.QPushButton(u"3.根据名字缩写来查询电话", self)
        Btn4 = QtGui.QPushButton(u"4.显示所有通讯录信息", self)
        Btn5 = QtGui.QPushButton(u"5.添加新的人员通讯信息", self)
        Btn6 = QtGui.QPushButton(u"6.根据id修改电话号码", self)
        Btn7 = QtGui.QPushButton(u"7.根据id修改姓名", self)
        Btn8 = QtGui.QPushButton(u"8.根据id删除数据", self)
        Btn9 = QtGui.QPushButton(u"清屏", self)

        Btn1.clicked.connect(self.find_by_name)
        Btn2.clicked.connect(self.find_by_tel)
        Btn3.clicked.connect(self.find_by_sn)
        Btn4.clicked.connect(self.showall)
        Btn5.clicked.connect(self.add)
        Btn6.clicked.connect(self.update_tel)
        Btn7.clicked.connect(self.update_name)  # 只能修改成英文名字
        Btn8.clicked.connect(self.delete)
        Btn9.clicked.connect(self.clearall)
        # cancleBtn.clicked.connect(self.clickCancleBtn)
        hBoxLayout.addWidget(Btn1)
        hBoxLayout.addWidget(Btn2)
        hBoxLayout.addWidget(Btn3)
        hBoxLayout.addWidget(Btn4)
        hBoxLayout.addWidget(Btn5)
        hBoxLayout.addWidget(Btn6)
        hBoxLayout.addWidget(Btn7)
        hBoxLayout.addWidget(Btn8)
        hBoxLayout.addWidget(Btn9)

        vBoxLayout.addLayout(hBoxLayout)
        self.setLayout(vBoxLayout)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(u"临海中学2006届5班通讯录")
        self.browser.append(u"  公元2016年2月11日，农历丙申年 庚寅月 癸亥日。\n   原临海中学06届5班部分人员相聚在临海某地。留下此通讯录，已纪念过去的时光")

    def add(self):  # 调用函数 弹出个新的窗口
        dialog = Dialog(parent=self)
        if dialog.exec_():
            self.model.appendRow((
                QtGui.QStandardItem(dialog.name()),
                QtGui.QStandardItem(str(dialog.age())),
            ))
        dialog.insert()
        dialog.destroy()

    def about(self):
        QMessageBox.information(self, u"相关信息", self.tr("作者：汤涛 \n2016.02.05"))

    def clearall(self):
        self.browser.clear()

    def auto_resort(self):
        conn = self.init_db()
        cur = conn.cursor()
        row = cur.execute("select name,telephone from 35txl")
        x = cur.fetchall()  # x是个二维数组，存放所有的name和telephone
        cur.execute("delete from 35txl")  # 删除表中的全部数据
        id = 1
        i = 0
        while (id < row + 1):
            sqli = "insert into 35txl values(%s,%s,%s,%s)"  # 35txl为表名
            cur.execute(sqli, (id, x[i][0], x[i][1], "haha"))
            i = i + 1
            id = id + 1
        cur.close()
        conn.commit()
        conn.close()
        self.insert_shortname()

    def update_tel(self):
        self.clearall
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        conn = self.init_db()
        cur = conn.cursor()
        id, ok = QInputDialog.getText(self, self.tr("更新"), self.tr("要更新的id编号"))  # ok的值为true or false
        if (ok):
            if (self.judge_ID(id)):
                if (id == ""):
                    QMessageBox.information(self, u"提示", self.tr("请输入ID"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                else:
                    tel, ok = QInputDialog.getText(self, self.tr("更新"), self.tr("请输入新的电话号码"))  # ok的值为true or false
                    if (ok):
                        if (tel == ""):
                            QMessageBox.information(self, u"提示", self.tr("请输入新的电话号码"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                        else:
                            try:
                                tel = int(tel)
                            except:
                                print u"输如的电话不是数字"
                            NO = int(id)
                            if (self.judge_tel(tel) == 0):
                                QMessageBox.information(self, u"提示", self.tr("请输入正确的电话号码"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                            else:
                                sqli = "update 35txl set telephone=%s where id=%s"  # 35txl为表名
                                row = cur.execute(sqli, (tel, NO))
                                self.insert_shortname()
        cur.close()
        conn.commit()
        conn.close()

    def judge_tel(self, tel):  # 这个是用来判断是否是11位数的
        z = 0
        try:
            changdu = len(str(int(tel)))  # 计算tel的长度，11位为正常
            tel = int(tel)
            if (changdu == 11):
                z = 1
            else:
                z = 0
        except:
            print(u"你输入的tel非法，请重新输入")
        return z

    def update_name(self):
        self.clearall
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        conn = self.init_db()
        cur = conn.cursor()
        id, ok = QInputDialog.getText(self, self.tr("更新"), self.tr("请输入要更新的id"))  # ok的值为true or false
        if (ok):
            if (self.judge_ID(id)):
                if (id == ""):
                    QMessageBox.information(self, u"提示", self.tr("请输入id"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                else:
                    name, ok = QInputDialog.getText(self, self.tr("更新"), self.tr("请输入新的名字"))  # ok的值为true or false
                    if (name == ""):
                        QMessageBox.information(self, u"提示", self.tr("请输入新的名字"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                    else:
                        sqli = "update 35txl set name=%s where id=%s"  # 35txl为表名
                        NO = int(id)
                        row = cur.execute(sqli, (name, NO))
                        self.insert_shortname
        cur.close()
        conn.commit()
        conn.close()

    def init_db(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            db='test',
            charset="utf8",  # 确保没有乱码
            passwd='root'
        )
        return conn

    def find_by_name(self):
        self.browser.clear()
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        name, ok = QInputDialog.getText(self, self.tr("搜索"), self.tr("请输入姓名"))  # ok的值为true or false
        if (ok):
            if (name == ""):
                QMessageBox.information(self, u"提示", self.tr("请输入姓名"))  # 弹出信息框，提示删除成功，此处日后要改成中文
            else:
                conn = self.init_db()
                cur = conn.cursor()
                sqlscript = "select * from 35txl where name like '%%%s%%'" % name
                row = cur.execute(sqlscript)
                x = cur.fetchall()
                if (row == 0):
                    QMessageBox.information(self, u"提示", self.tr("未找到搜索信息"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                else:
                    i = 0
                    while (i < row):
                        No = x[i][0]
                        name = x[i][1]
                        tel = x[i][2]
                        sn = x[i][3]
                        self.browser.append("%s %s %s %s" % (No, name, tel, sn))
                        i = i + 1
                cur.close()
                conn.commit()
                conn.close()

    def find_by_tel(self):
        self.clearall()
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        tel, ok = QInputDialog.getText(self, self.tr("搜索"), self.tr("请输入电话"))  # ok的值为true or false
        if (ok):
            if (tel == ""):
                QMessageBox.information(self, u"提示", self.tr("请输入电话"))  # 弹出信息框，提示删除成功，此处日后要改成中文
            else:
                conn = self.init_db()
                cur = conn.cursor()
                sqlscript = "select * from 35txl where telephone like '%%%s%%'" % tel
                row = cur.execute(sqlscript)
                x = cur.fetchall()
                len_of_txl = len(x)
                if (row == 0):
                    QMessageBox.information(self, u"提示", self.tr("未找到所搜索信息"))  # 弹出信息框，提示删除成功，此处日后要改成中文
                else:
                    i = 0
                    while (i < row):
                        No = x[i][0]
                        name = x[i][1]
                        tel = x[i][2]
                        sn = x[i][3]
                        self.browser.append("%s %s %s %s" % (No, name, tel, sn))
                        i = i + 1
                cur.close()
                conn.commit()
                conn.close()

    def find_by_sn(self):
        self.clearall()
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        sn, ok = QInputDialog.getText(self, self.tr("搜索"), self.tr("请输入名字缩写"))  # ok的值为true or false
        if (ok):
            if (sn == ""):
                QMessageBox.information(self, u"提示", self.tr("请输入名字缩写"))  # 弹出信息框，提示删除成功，此处日后要改成中文
            else:
                conn = self.init_db()
            cur = conn.cursor()
            sqli = "select * from 35txl where shortname=%s"  # 35txl为表名
            row = cur.execute(sqli, (sn))
            x = cur.fetchall()
            len_of_txl = len(x)
            if (row == 0):
                QMessageBox.information(self, u"提示", self.tr("未找到所搜索信息"))  # 弹出信息框，提示删除成功，此处日后要改成中文
            else:
                i = 0
                while (i < row):
                    No = x[i][0]
                    name = x[i][1]
                    tel = x[i][2]
                    sn = x[i][3]
                    self.browser.append("%s %s %s %s" % (No, name, tel, sn))
                    i = i + 1
                cur.close()
                conn.commit()
                conn.close()

    def showall(self):
        self.clearall()
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        self.browser.clear()
        conn = self.init_db()
        cur = conn.cursor()
        row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
        x = cur.fetchall()  # x是个二维数组，里面有全部的数据库信息
        len_of_txl = len(x)
        i = 0
        while (i < row):
            No = x[i][0]
            name = x[i][1]
            tel = x[i][2]
            sn = x[i][3]
            self.browser.append("%s %s %s %s" % (No, name, tel, sn))
            i = i + 1
        cur.close()
        conn.commit()
        conn.close()

    def delete(self):
        self.browser.setFont(QtGui.QFont("Microsoft YaHei", 10))  # 设置字体
        id, ok = QInputDialog.getText(self, self.tr("Delete"), self.tr("ID to del"))  # ok的值为true or false
        if (self.judge_ID(id)):
            if (ok):
                conn = self.init_db()
                cur = conn.cursor()
                row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
                sqlscript = "delete from 35txl where id='%s'" % id
                cur.execute(sqlscript)
                cur.close()
                conn.commit()
                conn.close()
                self.browser.append(u"删除成功")
                QMessageBox.information(self, u"提示", self.tr("恭喜，删除成功"))  # 弹出信息框，提示删除成功，此处日后要改成中文
        self.auto_resort()

    def insert_shortname(self):  # 一次性产生全部用户的拼音首字母大写
        conn = self.init_db()
        cur = conn.cursor()
        row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
        x = cur.fetchall()
        p = Pinyin()
        sqli = "update 35txl set shortname=%s where id=%s"  # 35txl为表名
        i = 0
        while (i < row):
            shortname = p.get_initials(x[i][1], u'')
            i = i + 1
            cur.execute(sqli, (shortname, i))
        cur.close()
        conn.commit()
        conn.close()

    def judge_ID(self, id):  # 判断id是否合法
        conn = self.init_db()
        cur = conn.cursor()
        row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
        cur.close()
        conn.commit()
        conn.close()
        z = 0
        try:
            id = int(id)
            if (0 < id <= row):
                z = 1
            else:
                z = 0
                QMessageBox.information(self, u"提示", self.tr("ID输入非法，请输入正确的ID"))
        except:
            QMessageBox.information(self, u"提示", self.tr("ID输入非法，请输入正确的ID"))
        return z


def main():
    app = QtGui.QApplication(sys.argv)
    t = QtCore.QTranslator()
    # 把Python安装目录\Lib\site-packages\PyQt4\translations\qt_zh_CN.qm复制到当前目录再用
    success = t.load("qt_zh_CN.qm")
    assert success
    app.installTranslator(t)  # http://m.newsmth.net/article/Python/95435 使得按钮变成中文
    lb = LoginBox()
    lb.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
