make:
	gcc -o pagerank-executable 03_pagerank.cpp mr/mapreduce.c mr/mr_functions.c mr/mapreduce.h -Wall -Werror -pthread -g
object:
	gcc -c 03_pagerank.cpp mr/mapreduce.c mr/mr_functions.c mr/mapreduce.h -Wall -Werror -pthread
clean:
	rm -f pagerank-executable
