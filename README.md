# TINY-code-to-AST
编写递归下降分析程序分析TINY语言文法，生成语法树
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

