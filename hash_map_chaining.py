# Author: Hassan Chaudhry
# Date: 3/11/2022
# Description: A program which defines two hash functions and a class called HashMap. The HashMap class represents a
#              hash table and is built on top of the DynamicArray and LinkedList classes. The class also makes use of
#              the two hash functions defined. The HashMap class has methods to initialize a hash map with empty linked
#              lists at each index, clear the hash map of its contents, get a value paired with a specific key, put a
#              key/value pair in a hash map through hashing, remove a key from the hash map, check if a key is in the
#              hash map, retrieve the number of empty buckets in the hash map, determine the load factor of the hash
#              map, resize the hash map to a new capacity, and get an array that contains the keys in the hash map. At
#              the bottom of the program there are several tests that test the functionality of the methods in the
#              HashMap class.


from include_file import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Takes no parameters and clears the contents of the hash map.
        The capacity of the hash map remains the same.
        """
        # Set buckets to new DA and append empty linked lists to it
        self.buckets = DynamicArray()
        for i in range(self.capacity):
            self.buckets.append(LinkedList())

        # Size needs to be reset to 0, but capacity remains the same
        self.size = 0

    def get(self, key: str) -> object:
        """
        Takes a key string as a parameter and returns the value paired
        with that key. If no such key exists in the hash map, None is
        returned.
        """
        # Determine index of key and get linked list in hash map at index
        hash = self.hash_function(key)
        index = hash % self.capacity
        linked_list = self.buckets.get_at_index(index)

        # Return None for empty linked list or key not in linked list
        if linked_list.length() == 0 or linked_list.contains(key) is None:
            return None
        # Return value of node that matches key
        else:
            node = linked_list.contains(key)
            return node.value

    def put(self, key: str, value: object) -> None:
        """
        Takes a key string and value object as parameters. If the key already
        exists in the hash map, the value is updated to the new value. If
        the key doesn't exist, the key/value pair is added to the hash map.
        """
        # Determine index of key and get linked list in hash map at index
        hash = self.hash_function(key)
        index = hash % self.capacity
        linked_list = self.buckets.get_at_index(index)

        # Insert node with key/value if empty linked list or key doesn't exist
        if linked_list.length() == 0 or linked_list.contains(key) is None:
            linked_list.insert(key, value)
            self.size += 1
        # Replace value of node if key exists in linked list
        else:
            node = linked_list.contains(key)
            node.value = value

    def remove(self, key: str) -> None:
        """
        Takes a key string as a parameter and removes the key/value pair
        from the hash map. If the key doesn't exist in the hash map, the
        method simply returns without doing anything.
        """
        # Determine index of key and get linked list in hash map at index
        hash = self.hash_function(key)
        index = hash % self.capacity
        linked_list = self.buckets.get_at_index(index)

        # Don't do anything if key doesn't exist
        if linked_list.contains(key) is None:
            return
        # Remove if key exists and decrement size of hash map
        else:
            linked_list.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Takes a key string as a parameter and returns True if the key
        is in the hash map. If the key is not found or the hash map
        is empty, False is returned.
        """
        # Determine index of key and get linked list in hash map at index
        hash = self.hash_function(key)
        index = hash % self.capacity
        linked_list = self.buckets.get_at_index(index)

        # Hash map is empty return False
        if self.empty_buckets() == self.buckets.length():
            return False
        # Key not in linked list return False
        elif linked_list.contains(key) is None:
            return False
        # Key was found return True
        else:
            return True

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns an integer value that equals
        the number of buckets that are empty in the hash table.
        """
        empty_buckets_count = 0

        # Iterate through buckets in hash map and increment count when linked list is empty
        for i in range(self.buckets.length()):
            linked_list = self.buckets.get_at_index(i)
            if linked_list.length() == 0:
                empty_buckets_count += 1

        return empty_buckets_count

    def table_load(self) -> float:
        """
        Takes no parameters and returns a float value that equals the
        load factor of the hash table.
        """
        elements = self.size
        buckets = self.buckets.length()
        table_load = elements / buckets
        return table_load

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer parameter for a new capacity to resize a hash
        table to. All existing key/value pairs remain in the new hash table
        and links are rehashed. The method simply returns if the new capacity
        parameter is less than 1.
        """
        if new_capacity < 1:
            return
        else:
            # Create new hash map
            new_buckets = DynamicArray()
            # Set empty links in the new hash map
            for i in range(new_capacity):
                new_buckets.append(LinkedList())
            # Iterate through buckets in new hash map
            for i in range(self.buckets.length()):
                linked_list = self.buckets.get_at_index(i)
                # If linked list is not empty iterate through it and rehash old keys to new hash map
                if linked_list.length() != 0:
                    for node in linked_list:
                        key = node.key
                        value = node.value
                        hash = self.hash_function(key)
                        index = hash % new_capacity
                        new_linked_list = new_buckets.get_at_index(index)
                        new_linked_list.insert(key, value)
            # Set new hash map as current hash map and capacity to new capacity
            self.buckets = new_buckets
            self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters and returns a DynamicArray that includes all
        the keys from the hash map appended to it.
        """
        keys_da = DynamicArray()

        # Iterate through buckets
        for i in range(self.buckets.length()):
            linked_list = self.buckets.get_at_index(i)
            # If linked list is not empty, iterate through it appending keys to DA
            if linked_list.length() != 0:
                for node in linked_list:
                    keys_da.append(node.key)

        return keys_da


# BASIC TESTING
if __name__ == "__main__":

    print("\nempty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nempty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\ntable_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\ntable_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nclear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nclear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nput example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nput example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\ncontains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\ncontains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nget example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nget example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nremove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nresize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nresize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nget_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
