# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:31:46 2020

@author: Gaojunfeng1020
"""

import os
from graphviz import Digraph
import cv2 as cv




keyword={'for','while','do','repeat','if','read','root','write','enddo','endwhile','endif','until','else'}

class ASTree:
    def __init__(self):
        self.Node=set()
        self.Edge=[]
    def printTree(self):
        global assign
        dot=Digraph(format='jpg')
        for e in self.Edge:
            e0strip=e[0].strip()
            e1strip=e[1].strip()
            if e0strip in keyword or 'assign ' in e0strip or 'read(' in e0strip:
                dot.node(e[0],e0strip,shape='box')
            else:dot.node(e[0],e0strip)
            if e1strip in keyword or 'assign ' in e1strip or 'read(' in e1strip:
                dot.node(e[1],e1strip,shape='box')
            else:dot.node(e[1],e1strip)
                
            dot.edge(e[0],e[1])
        if not os.path.exists('./image'):
            os.mkdir('./image')
        dot.view(filename='./image/view')
        dot.render(filename='output',directory='./image')

tree=ASTree()           
token_list=[]
token=''
i=0
opi=0
assign={}

#去除注释
def removeTag(code):
    stack=[]
    string=[]
    for s in code:
        if s=='}' and len(stack)!=0:
            stack.pop()
        elif len(stack)>0:
            continue
        elif s!='{':
            string.append(s)
        elif s=='{':
            stack.append('{')
    return ''.join(string)

def get_token(code):
    token_list=[]
    string=str()
    i=-1
    while i <len(code)-1:
        i+=1
        if code[i]==' ' or code[i]=='\n':
            if string!='':
                token_list.append(string)
                string=str()
            continue
        elif (code[i]>='0' and code[i]<='9') or code[i]=='.':
            string+=code[i]
        elif code[i]>='a' and code[i]<='z' or code[i]>='A' and code[i]<='Z':
            string+=code[i]
        elif code[i] in [';','(',')','<','=','>','*','/','%','^','+','-',':']:
            token_list.append(string)
            string=str()
            if code[i]==':':
                if code[i+1]=='=':
                    token_list.append(':=')
                    i+=1
            elif code[i]=='<':
                if code[i+1]=='>':
                    token_list.append('<>')
                    i+=1
                elif code[i+1]=='=':
                    token_list.append('<=')
                    i+=1
                else: token_list.append('<')
            elif code[i]=='+':
                if code[i+1]=='=':
                    token_list.append('+=')
                    i+=1
                else:
                    token_list.append('+')
            else: token_list.append(code[i])
        
            
    return token_list
    
def getToken():
    global i
    global token
    i+=1
    if i<len(token_list):
        token=token_list[i]

def match(parent,expecToken):
    global i
    if expecToken=='identifier':
        if token[0] not in '0123456789':
            getToken()
    elif token==expecToken:
        getToken()
    else:print('Error')

def progrem():
    stmt_sequence('root')

def stmt_sequence(parent):
    statement(parent)
    while token==';':
        match(parent,';')
        global i
        if i<len(token_list):
            stmt_sequence(parent)
    
def statement(parent):
    if token not in keyword and token[0] not in '0123456789;><=()$':
        assign_stmt(parent)
    if token=='read':
        read_stmt(parent)   
    if token=='if':
        if_stmt(parent)
    if token=='repeat':
        repeat_stmt(parent)
    if token=='identifier':
        assign_stmt(parent)
    if token=='while' and parent.strip()!='do':
        while_stmt(parent)
    if token=='do':
        dowhile_stmt(parent)
    if token=='for':
        for_stmt(parent)
    if token=='write':
        write_stmt(parent)
    
        
def if_stmt(parent):
    match(parent,'if')
    #if个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    IF=token_list[i-1]+assign[token_list[i-1]]*' '#第n个if
    
    tree.Edge.append((parent,IF))
    tree.Node.add(parent)
    tree.Node.add(IF)
    match(parent,'(')
    exp(IF)
    match(parent,')')
    stmt_sequence(IF)
    if token=='else':
        match(parent,'else')
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        
        ELSE=token_list[i-1]+assign[token_list[i-1]]*' '
        tree.Edge.append((IF,ELSE))
        tree.Node.add(IF)
        tree.Node.add(ELSE)
        stmt_sequence(ELSE)
    match(IF,'endif')
    

def repeat_stmt(parent):
    match(parent,'repeat')
    #repeat个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    REPEAT=token_list[i-1]+assign[token_list[i-1]]*' '#第n个REPEAT
    
    tree.Edge.append((parent,REPEAT))
    tree.Node.add(parent)
    tree.Node.add(REPEAT)
    stmt_sequence(REPEAT)
    match(parent,'until')
    exp(REPEAT)

def assign_stmt(parent):
    if token in keyword:
        return
    match(parent,'identifier')
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    if token==':=':
        op=token[1]
    else:op=token
    if 'assign '+token_list[i-1]+op not in assign:
        assign['assign '+token_list[i-1]+op]=0
    else:assign['assign '+token_list[i-1]+op]+=1
    
    temp='assign '+token_list[i-1]+op+assign['assign '+token_list[i-1]+op]*' '
    tree.Edge.append((parent,temp))
    tree.Node.add(parent)
    tree.Node.add(temp)
    asop(temp)
    exp(temp)
    

def asop(parent):
    if token==':=':
        match(parent,':=')

    elif token=='+=':
        match(parent,'+=')
        
    
def read_stmt(parent):
    match(parent,'read')
    match(parent,'identifier')
    tree.Edge.append((parent,'read('+token_list[i-1]+')'))
    tree.Node.add(parent)
    tree.Node.add('read('+token_list[i-1]+')')

def write_stmt(parent):
    match(parent,'write')
    #write个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    WRITE=token_list[i-1]+assign[token_list[i-1]]*' '#第n个write
    
    tree.Edge.append((parent,WRITE))
    tree.Node.add(parent)
    tree.Node.add(WRITE)
    exp(WRITE)

def while_stmt(parent):
    match(parent,'while')
    #while个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    WHILE=token_list[i-1]+assign[token_list[i-1]]*' '#第n个while
    
    tree.Edge.append((parent,WHILE))
    tree.Node.add(parent)
    tree.Node.add(WHILE)
    match(parent,'(')
    exp(WHILE)
    match(parent,')')
    stmt_sequence(WHILE)
    match(parent,'endwhile')

def dowhile_stmt(parent):
    match(parent,'do')
    #do个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    DO=token_list[i-1]+assign[token_list[i-1]]*' '#第n个do
    
    tree.Edge.append((parent,DO))
    tree.Node.add(parent)
    tree.Node.add(DO)
    stmt_sequence(DO)
    match(parent,'while')
     #while个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    WHILE=token_list[i-1]+assign[token_list[i-1]]*' '#第n个while
    
    tree.Edge.append((DO,WHILE))
    tree.Node.add(DO)
    tree.Node.add(WHILE)
    match(parent,'(')
    exp(WHILE)
    match(parent,')')

def for_stmt(parent):
    match(parent,'for')
     #for个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    FOR=token_list[i-1]+assign[token_list[i-1]]*' '#第n个for
    tree.Edge.append((parent,FOR))
    tree.Node.add(parent)
    
    #match标识符
    match(parent,'identifier')
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    if token==':=':
        op=token[1]
    else:op=token
    if 'assign '+token_list[i-1]+op not in assign:
        assign['assign '+token_list[i-1]+op]=0
    else:assign['assign '+token_list[i-1]+op]+=1
    
    ASSIGN='assign '+token_list[i-1]+op+assign['assign '+token_list[i-1]+op]*' '
    tree.Edge.append((FOR,ASSIGN))
    tree.Node.add(FOR)
    tree.Node.add(ASSIGN)
    match(parent,':=')
    simple_exp(ASSIGN)
    forop(ASSIGN)
    simple_exp(ASSIGN)
    
    tree.Edge.pop()
    tree.Edge.pop()
    assign[token_list[i-1]]-=1
    assign[token_list[i-3]]-=1
    if token_list[i-2] not in assign:
        assign[token_list[i-2]]=0
    else:assign[token_list[i-2]]+=1
    tree.Edge.append((ASSIGN,token_list[i-2]+assign[token_list[i-2]]*' '))
    
    tree.Node.add(token_list[i-2]+assign[token_list[i-2]]*' ')
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    if token_list[i-3] not in assign:
        assign[token_list[i-3]]=0
    else:assign[token_list[i-3]]+=1
    tree.Node.add(token_list[i-3]+assign[token_list[i-3]]*' ')
    tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')
    tree.Edge.append((token_list[i-2]+assign[token_list[i-2]]*' ',token_list[i-3]+assign[token_list[i-3]]*' '))
    tree.Edge.append((token_list[i-2]+assign[token_list[i-2]]*' ',token_list[i-1]+assign[token_list[i-1]]*' ')) 
    
    match(FOR,'do')
    #do个数加1
    if token_list[i-1] not in assign:
        assign[token_list[i-1]]=0
    else:assign[token_list[i-1]]+=1
    
    DO=token_list[i-1]+assign[token_list[i-1]]*' '#第n个do
    tree.Edge.append((FOR,DO))
    tree.Node.add(FOR)
    tree.Node.add(DO)
    stmt_sequence(DO)
    match(DO,'enddo')

def forop(parent):
    if token=='to':
        match(parent,'to')
    elif token=='downto':
        match(parent,'downto')

def exp(parent):
    global opi
    simple_exp(parent)
    if token=='<' or token=='=' or token=='<=' or token=='<>':
        comparison_op(parent)
        simple_exp(parent)
        
        tree.Edge.pop()
        tree.Edge.pop()
        assign[token_list[i-1]]-=1
        assign[token_list[i-3]]-=1
        
        if token_list[i-2] not in assign:
            assign[token_list[i-2]]=0
        else:assign[token_list[i-2]]+=1
        tree.Edge.append((parent,'op('+token_list[i-2]+')'+assign[token_list[i-2]]*' '))
        
        tree.Node.add('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ')
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        if token_list[i-3] not in assign:
            assign[token_list[i-3]]=0
        else:assign[token_list[i-3]]+=1
        tree.Node.add(token_list[i-3]+assign[token_list[i-3]]*' ')
        tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-3]+assign[token_list[i-3]]*' '))
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-1]+assign[token_list[i-1]]*' ')) 
    

def comparison_op(parent):
    if token=='<':
        match(parent,'<')
                       
    elif token=='=':
        match(parent,'=')
        
    elif token=='<=':
        match(parent,'<=')
        
    elif token=='<>':
        match(parent,'<>')
        

def simple_exp(parent):
    global opi
    term(parent)
    while token=='+' or token=='-':
        addop(parent)
        term(parent)
        
        tree.Edge.pop()
        tree.Edge.pop()
        assign[token_list[i-1]]-=1
        assign[token_list[i-3]]-=1
        
        if token_list[i-2] not in assign:
            assign[token_list[i-2]]=0
        else:assign[token_list[i-2]]+=1
        tree.Edge.append((parent,'op('+token_list[i-2]+')'+assign[token_list[i-2]]*' '))
        
        tree.Node.add('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ')
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        if token_list[i-3] not in assign:
            assign[token_list[i-3]]=0
        else:assign[token_list[i-3]]+=1
        tree.Node.add(token_list[i-3]+assign[token_list[i-3]]*' ')
        tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-3]+assign[token_list[i-3]]*' '))
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-1]+assign[token_list[i-1]]*' ')) 

def addop(parent):
    if token=='+':
        match(parent,'+')
        
    elif token=='-':
        match(parent,'-')
        

def term(parent):
    global opi
    factor(parent)
    while token=='*' or token=='/' or token=='%':
        mulop(parent)
        factor(parent)
        
        tree.Edge.pop()
        tree.Edge.pop()
        assign[token_list[i-1]]-=1
        assign[token_list[i-3]]-=1
        
        if token_list[i-2] not in assign:
            assign[token_list[i-2]]=0
        else:assign[token_list[i-2]]+=1
        tree.Edge.append((parent,'op('+token_list[i-2]+')'+assign[token_list[i-2]]*' '))
        
        tree.Node.add('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ')
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        if token_list[i-3] not in assign:
            assign[token_list[i-3]]=0
        else:assign[token_list[i-3]]+=1
        tree.Node.add(token_list[i-3]+assign[token_list[i-3]]*' ')
        tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-3]+assign[token_list[i-3]]*' '))
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-1]+assign[token_list[i-1]]*' ')) 

def mulop(parent):
    if token=='*':
        match(parent,'*')
          
    elif token=='/':
        match(parent,'/')
            
    elif token=='%':
        match(parent,'%')
            

def factor(parent):
    global opi
    factor1(parent)
    while(token=='^'):
        match(parent,'^')
        factor1(parent)
        
        tree.Edge.pop()
        tree.Edge.pop()
        assign[token_list[i-1]]-=1
        assign[token_list[i-3]]-=1
        
        if token_list[i-2] not in assign:
            assign[token_list[i-2]]=0
        else:assign[token_list[i-2]]+=1
        tree.Edge.append((parent,'op('+token_list[i-2]+')'+assign[token_list[i-2]]*' '))
        
        tree.Node.add('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ')
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        if token_list[i-3] not in assign:
            assign[token_list[i-3]]=0
        else:assign[token_list[i-3]]+=1
        tree.Node.add(token_list[i-3]+assign[token_list[i-3]]*' ')
        tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-3]+assign[token_list[i-3]]*' '))
        tree.Edge.append(('op('+token_list[i-2]+')'+assign[token_list[i-2]]*' ',token_list[i-1]+assign[token_list[i-1]]*' ')) 

def factor1(parent):
    if token=='(':
        match(parent,'(')
        exp(parent)
        match(parent,')')
    elif token.isdigit():  
        match(parent,token)
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        tree.Edge.append((parent,token_list[i-1]))
        tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')
    elif token[0] not in '0123456789':
        match(parent,'identifier')
        if token_list[i-1] not in assign:
            assign[token_list[i-1]]=0
        else:assign[token_list[i-1]]+=1
        tree.Edge.append((parent,token_list[i-1]+assign[token_list[i-1]]*' '))
        tree.Node.add(token_list[i-1]+assign[token_list[i-1]]*' ')

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap,QImage


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("AST生成器")
        MainWindow.resize(1680,960 )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMidLineWidth(0)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.pushButton.raise_()
        self.label_2.raise_()
        self.graphicsView.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.click_start)
        self.retranslateUi(MainWindow)
        self.textEdit.setPlaceholderText("在此输入代码")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "AST生成器"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "在此输入代码"))
        self.pushButton.setText(_translate("MainWindow", "创建AST"))
    
    def click_start(self):
        try:
            global token,token_list,tree,i
            i=0
            tree=ASTree()
            token_list=[]
            code=self.textEdit.toPlainText()
            code=removeTag(code)
            code=code.strip()
            token_list=get_token(code)
            token_list=[s for s in token_list if s!='' and s!=' ']
            token_list.append('$')#加入结束符
            
            token=token_list[0]
            progrem()
            tree.printTree()
            img=cv.imread('./image/output.jpg')
            self.graphicsView.scene_img = QGraphicsScene()
            self.imgShow = QPixmap()
            self.imgShow.load('./image/output.jpg')
            self.imgShowItem = QGraphicsPixmapItem()
            #self.imgShowItem.setPixmap(QPixmap(self.imgShow))
            self.imgShowItem.setPixmap(QPixmap(self.imgShow).scaled(img.shape[1],img.shape[0]))    #自己设定尺寸
            self.graphicsView.scene_img.addItem(self.imgShowItem)
            self.graphicsView.setScene(self.graphicsView.scene_img)
            self.graphicsView.fitInView(QGraphicsPixmapItem(QPixmap(self.imgShow)))    
            
            QtWidgets.QMessageBox.information(self,'提示','生成AST成功!\n原图片存放在路径：./image',QMessageBox.Yes)
        except ValueError:
            QtWidgets.QMessageBox.critical(self,'错误','生成AST失败！请检查代码语法格式！',QMessageBox.Yes)
            
        

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class UsingTest(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(UsingTest, self).__init__(*args, **kwargs)
        self.setupUi(self)  # 初始化ui

if __name__=='__main__':  
    
    app = QApplication(sys.argv)
    win = UsingTest()
    win.show()
    sys.exit(app.exec_())
    """
    code=input("请输入代码：")
    code=removeTag(code)
    code=code.strip()
    token_list=get_token(code)
    token_list=[s for s in token_list if s!='' and s!=' ']
    token_list.append('$')#加入结束符
    tree=Tree()
    token=token_list[0]
    progrem()
    tree.printTree()
    """