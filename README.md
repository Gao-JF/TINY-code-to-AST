# TINY-code-to-AST
编写递归下降分析程序分析TINY语言文法，生成语法树  
# 实验要求  
扩充的语法规则有：实现 while、do while、for、if语句、+= 加法赋值运算符号（类似于C语言的+=）、求余%、乘方^、<=(小于等于)、<>(不等于)运算符号，具体文法规则自行构造。  

可参考：云盘中参考书P97及P136的文法规则。  

(1) While-stmt --> while(exp)  stmt-sequence  endwhile   
(2) Dowhile-stmt-->do  stmt-sequence  while(exp);   
(3) for-stmt-->for identifier:=simple-exp  to  simple-exp  do  stmt-sequence enddo    步长递增1  
(4) for-stmt-->for identifier:=simple-exp  downto  simple-exp  do  stmt-sequence enddo    步长递减1  
(5) += 加法赋值运算符号、求余%、乘方^、<=(小于等于)、<>(不等于)运算符号的文法规则请自行组织。  
(6) 把TINY语言原有的if语句书写格式  

    if_stmt-->if exp then stmt-sequence end  |  | if exp then stmt-sequence else stmt-sequence end  

改写为：  

    if_stmt-->if(exp) stmt-sequence else stmt-sequence | if(exp) stmt-sequence  
（7）为了实现以上的扩充或改写功能，还需要对原tiny语言的文法规则做如何的处理？  

# TINY语言文法如下：  
1.	program -> stmt-sequance  
2.	stmt_sequence -> statement{ ; statement}  
3.	statement -> if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt | while-stmt | dowhile-stmt | for-stmt  
4.	if-stmt -> if ( exp ) stmt-sequence [ else stmt-sequence ] endif  
5.	repeat-stmt -> repeat stmt-sequence until exp  
6.	assign-stmt -> identifier asop exp  
7.	asop -> := | +=  
8.	read-stmt -> read identifier  
9.	write-stmt -> write exp  
10.	while-stmt -> while( exp ) stmt-sequence endwhile  
11.	dowhile-stmt -> do stmt-sequence while( exp );  
12.	for-stmt -> for identifier := simple-exp forop simple-exp do stmt-sequence enddo  
13.	forop -> to | downto  
14.	exp -> simple-exp [ comparison-op simple-exp ]  
15.	comparison-op -> < | = | <= | <>  
16.	simple-exp -> term { addop term }  
17.	addop -> + | -  
18.	term -> factor { mulop factor }  
19.	mulop -> * | / | %  
20.	factor -> factor1 {^factor1}  
21.	factor1 -> ( exp ) | number | identifier  

注：为解决if-stmt中statement的归属问题，将文法：  
if-stmt -> if ( exp ) stmt-sequence [ else stmt-sequence ]  
改为  
if-stmt -> if ( exp ) stmt-sequence [ else stmt-sequence ] endif  

# 示例图片  
![图片](https://github.com/Gao-JF/TINY-code-to-AST/blob/main/test.png?raw=true)
