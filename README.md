# AI-1-expense-8-puzzle
-> Name : Jay Shah

-> UTA ID : 1002070971

-> Programming language used : Python 3.10.7

-> Structure of my code: 
   My entire code is in a single File named expense_8_puzzle.py
   and no other support files are needed except for the start and goal nodes.
   My code has library import commands in the first part.
   Than I have lines reading commands from terminal/cmd.
   After that I have declared my dump file as false and then
   following the dump variable are my 3 functions which are needed
   further in my code. 

   Now I have defined 7 functions each for a search method in
   a new function and than as per the command line arguements 
   it will call the search method accordingly.

   Underneath my 7 search functions I have wrote the logic
   to call functions as per the command line arguements.

-> How to run my code:
	My (.py) file is in zip folder so You need to extract it. Now wherever you extract it
	make sure, that while running the file in CMD pr any terminal the path is set to the location
	where the .py file is. Now that you have the .py file, you will also need 2 .txt files wherein
	you need to define start state and the goal state. You can name the file however you would like but
	make sure to put following phrase in the 4 th line of your text file - "End of file". DFS 
	
	Now that all the files are ready with you, you can call my function using the filename :- expense_8_puzzle.py
	followed by name of the file having start state and then the filename having goal state.
	Please note: - if no method will be passed than default method would be A* search.
	commands for each search are as followed.
	
	search name    <command> 
	   BFS            bfs
	   UCS            ucs
	   DFS            dfs
	   IDS            ids
	   DLS            dls
	   GREEDY         greedy
	   ASTAR           a*
	
	Command for the dump file is set to false by default. And will only become true if, declared in the command line
	arguement using the "true" command. Also, the dump file will always be in the same path which is having the .py file. 
	Please make sure to only pass one search command and one dump flag value other than the python filename
	and names of start file and goal file, at max in command line. Because in all the other conditions it will return an error.

	So format of command line arguement for my code is as follow
	
	expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>


Thank you!
