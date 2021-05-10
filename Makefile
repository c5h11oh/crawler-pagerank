make:
	g++ -o pagerank-executable mapreduce.c 03_pagerank.cpp -Wall -Werror -pthread -g
object:
	g++ -c mapreduce.c 03_pagerank.cpp -Wall -Werror -pthread
clean:
	rm -f pagerank-executable
