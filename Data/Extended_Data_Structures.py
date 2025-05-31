class MinHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
    
    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root
    
    def empty(self):
        return len(self.heap) == 0
    
    def _heapify_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._heapify_up(parent)
    
    def _heapify_down(self, idx):
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._heapify_down(smallest)

class Queue:
    def __init__(self):
        self.items = []
        self.front = 0
    
    def append(self, item):
        self.items.append(item)
    
    def popleft(self):
        item = self.items[self.front]
        self.front += 1
        if self.front == len(self.items):
            self.items = []
            self.front = 0
        return item
    
    def empty(self):
        return self.front >= len(self.items)
    
class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return 0
