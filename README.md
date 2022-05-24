# Python-HashMap
This is a project that I completed as part of a data structures course in my undergraduate CS degree. It implements a hash table through object-oriented programming in Python and uses two different methods for collision resolution. The first collision resolution method is chaining and the second is open addressing.

### hash_map_chaining.py
This py file makes use of chaining for collision resolution. The hash table is stored in a dynamic array with each key/value pair being stored within a node of singly linked list. 

![Chaining](https://user-images.githubusercontent.com/13329400/170104841-ad2d3198-7a2d-494a-8e61-f612d37b4896.jpg)

### hash_map_open_addressing.py
This py file makes use of opening addressing for collision resolution. The hash table is again stored in a dynamic array, but now, instead of storing key/value pairs in the nodes of a singly linked list, the key/value pairs are stored in the array itself using quadratic probing.

Quadratic probing: &nbsp; i = i<sub>initial</sub> + j<sup>2</sup> &nbsp; (where j = 1, 2, 3, …)

![open addressing](https://user-images.githubusercontent.com/13329400/170104957-914031b1-7e90-4b77-acfb-f244a61f5886.jpg)

### Testing
The methods of the HashMap class in each file are tested using built-in tests at the bottom of each file and will execute when the file is run. The output of running the test on each method is printed out to the user.  
