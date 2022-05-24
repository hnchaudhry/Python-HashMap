# Author: Hassan Chaudhry
# Date: 3/11/2022
# Description: A program which defines two classes and two hash functions. The two classes are HashEntry and HashMap.
#              HashMap represents a hash table and HashEntry represents an entry in the hash table with attributes for
#              key, value, and setting it to a tombstone for deletion. The HashMap is created using a DynamicArray for
#              its buckets and the two hash functions to hash entries into the table. The HashMap uses quadratic probing
#              open-addressing scheme to hash entries. It has methods to clear the hash table, get a value which pairs
#              with a given key, put a new key/value pair in the hash map, helper method to resize if put causes the
#              load factor to equal or go over 0.5, remove hash entry with specified key from table, check if a key is
#              in the table, check the number of empty buckets, calculate load factor, resize the table, and retrieve
#              all the keys in the hash map.


from include_file import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Takes no parameters and clears the contents of the hash map by
        setting the buckets to a new DynamicArray and populating it with
        the value None. The size is also reset to 0.
        """
        self.buckets = DynamicArray()
        for i in range(self.capacity):
            self.buckets.append(None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        Takes a key string as a parameter and returns the value object
        that is paired with that key in the hash map. If the key doesn't
        exit, None is returned. Uses quadratic probing open-addressing
        scheme for collisions in the table.
        """
        # Check if key is in table
        if self.contains_key(key) is False:
            return None

        # Find initial index and initial hash entry
        hash = self.hash_function(key)
        index_initial = hash % self.capacity
        hash_entry = self.buckets.get_at_index(index_initial)

        # Use quadratic probing to find hash entry with key
        j = 1
        while hash_entry.key != key:
            index = (index_initial + (j ** 2)) % self.capacity
            j += 1
            hash_entry = self.buckets.get_at_index(index)

        return hash_entry.value

    def put(self, key: str, value: object) -> None:
        """
        Takes a key string and value object as parameters and inserts
        the key/value pair into the hash map. If the key already exists,
        the value of the key is updated to the new value. If the key
        doesn't exist, quadratic probing open-addressing is used to
        find the next open spot to insert the key/value pair at. This
        method will first take into account the load factor of the hash
        map before inserting a new key/value pair. If the load factor is
        greater than or equal to 0.5, the hash map is resized to twice
        its current capacity.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair

        # Resize hash table if needed
        if self.table_load() >= 0.5:
            self.put_resize_helper(2 * self.capacity)

        # Check if the key exists in table using quadratic probing
        hash = self.hash_function(key)
        index_initial = hash % self.capacity
        hash_entry = self.buckets.get_at_index(index_initial)
        j = 1
        while hash_entry is not None:
            if hash_entry.is_tombstone is True:
                index = (index_initial + (j ** 2)) % self.capacity
                j += 1
                hash_entry = self.buckets.get_at_index(index)
            elif hash_entry.key != key:
                index = (index_initial + (j ** 2)) % self.capacity
                j += 1
                hash_entry = self.buckets.get_at_index(index)
            # Key is found so set new value and return
            elif hash_entry.key == key:
                hash_entry.value = value
                return

        # Key doesn't exist so find next open spot using quadratic probing and insert put key/value pair
        hash_entry = self.buckets.get_at_index(index_initial)
        new_hash_entry = HashEntry(key, value)
        index = index_initial
        j = 1
        while hash_entry is not None:
            if hash_entry.is_tombstone is True:
                self.buckets.set_at_index(index, new_hash_entry)
                self.size += 1
                return
            else:
                index = (index_initial + (j ** 2)) % self.capacity
                j += 1
                hash_entry = self.buckets.get_at_index(index)
        self.buckets.set_at_index(index, new_hash_entry)
        self.size += 1

    def put_resize_helper(self, new_capacity: int) -> None:
        """
        Helper method for the put method. Takes a new capacity integer as
        a parameter (should be twice the current capacity of hash map) and
        resizes the hash map to the new capacity. This method is only called
        by the put method if the load factor of the hash map is greater than
        or equal to 0.5. Non-deleted values from the hash map are rehashed
        using quadratic probing open-addressing.
        """
        # Don't resize if new capacity less than 1 or less than current size
        if new_capacity < 1 or new_capacity < self.size:
            return

        # Create new buckets DynamicArray to new capacity and populate with None
        new_buckets = DynamicArray()
        for i in range(new_capacity):
            new_buckets.append(None)

        # Iterate through hash map until a non-deleted value and isn't None is reached
        for i in range(self.buckets.length()):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry is not None:
                if hash_entry.is_tombstone is True:
                    continue
                # Rehash value using quadratic probing and place in new buckets
                else:
                    hash = self.hash_function(hash_entry.key)
                    index_initial = hash % new_capacity
                    some_hash = new_buckets.get_at_index(index_initial)
                    index = index_initial
                    j = 1
                    while some_hash is not None:
                        index = (index_initial + (j ** 2)) % new_capacity
                        j += 1
                        some_hash = new_buckets.get_at_index(index)
                    new_buckets.set_at_index(index, hash_entry)

        # Set current buckets to new buckets and current capacity to new capacity
        self.buckets = new_buckets
        self.capacity = new_capacity

    def remove(self, key: str) -> None:
        """
        Takes a key string as a parameter and "removes" the hash entry
        with the key from the hash map. The physical hash entry is not
        actually removed and instead is set to being a tombstone. This
        represents the location in the hash map as being empty and is
        needed to resolve collisions and searching for keys. If the key
        isn't in the hash map, the method simply returns without doing
        anything. Quadratic probing open-addressing scheme is used to
        remove any key/value pairs from the hash map.
        """
        # Check if key exists in table
        if self.contains_key(key) is False:
            return

        # Find initial key index and retrieve initial hash entry
        hash = self.hash_function(key)
        index_initial = hash % self.capacity
        hash_entry = self.buckets.get_at_index(index_initial)

        # Find hash entry that matches key using quadratic probing
        j = 1
        while hash_entry is not None:
            if hash_entry.is_tombstone is True or hash_entry.key != key:
                index = (index_initial + (j ** 2)) % self.capacity
                j += 1
                hash_entry = self.buckets.get_at_index(index)
            else:
                break

        # Once key is found, set hash entry to tombstone and decrement size
        hash_entry.is_tombstone = True
        self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Takes a key string as a parameter and returns True if the key
        exists in the hash map and False if it doesn't. Quadratic probing
        open-addressing scheme is used to resolve collisions and search
        for the key in the hash map.
        """
        # Check if the hash table is empty
        flag = 0
        for i in range(self.buckets.length()):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry is not None:
                if hash_entry.is_tombstone is True:
                    continue
                else:
                    flag = 1
                    break
        if flag == 0:
            return False

        # Find initial index of key in table and retrieve the hash entry
        hash = self.hash_function(key)
        index_initial = hash % self.capacity
        hash_entry = self.buckets.get_at_index(index_initial)

        # Check if hash entry key matches key, if not go to next hash entry (uses quadratic probing)
        flag = 0
        j = 1
        while hash_entry is not None:
            if hash_entry.is_tombstone is True:
                index = (index_initial + (j ** 2)) % self.capacity
                j += 1
                hash_entry = self.buckets.get_at_index(index)
            else:
                if hash_entry.key == key:
                    flag = 1
                    break
                else:
                    index = (index_initial + (j ** 2)) % self.capacity
                    j += 1
                    hash_entry = self.buckets.get_at_index(index)

        # Flag is set if key was found so return True, otherwise False
        if flag == 1:
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns an integer value that is equal
        to the number of empty buckets in the hash map. A bucket is
        considered empty if the hash entry is None or is a tombstone.
        """
        empty_bucket_count = 0

        # Iterate through hash map and increment count only if value is None or entry is tombstone
        for i in range(self.buckets.length()):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry is None:
                empty_bucket_count += 1
            else:
                if hash_entry.is_tombstone is True:
                    empty_bucket_count += 1

        return empty_bucket_count

    def table_load(self) -> float:
        """
        Takes no parameters and returns a float value that is the load
        factor of the hash map. The equation to calculate the load factor
        is load_factor = total_stored_elements / num_of_buckets.
        """
        elements = self.size
        buckets = self.buckets.length()
        table_load = elements / buckets
        return table_load

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity integer as a parameter and resizes the hash
        map to match the new capacity. Non-deleted values in the hash map
        are rehashed. If the new capacity parameter is less than 1 or less
        than the current size of the hash map, the method simply returns
        without doing anything.
        """
        # remember to rehash non-deleted entries into new table

        # Don't resize if new capacity less than 1 or less than current size
        if new_capacity < 1 or new_capacity < self.size:
            return

        new_hash_map = HashMap(new_capacity, self.hash_function)

        # Iterate through hash map and rehash non-deleted values into new hash map
        for i in range(self.buckets.length()):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry is not None:
                if hash_entry.is_tombstone is True:
                    continue
                else:
                    new_hash_map.put(hash_entry.key, hash_entry.value)

        # Set current hash map buckets and capacity to new hash map buckets and capacity
        self.buckets = new_hash_map.buckets
        self.capacity = new_hash_map.capacity

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters and returns a DynamicArray which includes
        all of the keys from the hash map appended to it.
        """
        keys_da = DynamicArray()

        # Append keys from hash entries that aren't None or tombstones into keys DA
        for i in range(self.buckets.length()):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry is not None and hash_entry.is_tombstone is False:
                keys_da.append(hash_entry.key)

        return keys_da


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
    # this test assumes that put() has already been correctly implemented
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
