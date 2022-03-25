import os, sys

class Order:
    
    def __init__(self, id, price, quantity, is_buy, time):
        self.id = id
        self.price = price
        self.quantity = quantity
        self.unfilled_quantity = quantity
        self.is_buy = is_buy
        self.time = time

    def get_id(self):
        return self.id

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_unfilled_quantity(self):
        return self.unfilled_quantity
    
    def get_is_buy(self):
        return self.is_buy

    def get_time(self):
        return self.time

    def __str__(self):
        return "Order(id: {}, price: {}, quantity: {}, unfilled_quantity: {}, is_buy: {}, time: {})".format(
                self.id, self.price, self.quantity, self.unfilled_quantity, self.is_buy, self.time
            )


class Node:
    # Constructor to initialize the node object
	def __init__(self, order):
		self.order = order
		self.next = None


class Orderbook:

    # Initialize head
	def __init__(self):
		self.head = None


	# If sell order, inserts order into the orderbook. If buy order, matches order against sell orders
    # in the orderbook
	def process_order(self, order, operation):
		if order == None: return

		if operation == "cancel":
			self.delete_order_by_id(order.id)
		elif operation == "insert":
			self.insert_sell_order(order)
		elif operation == "match":
			self.match_buy_order(order)
		else:
			raise ValueError("Operation {} was not configured correctly.".format(operation)) 


	# Function to insert sell order into orderbook based on price-time priority
	def insert_sell_order(self, order):
		if order.is_buy: raise ValueError("Cannot insert buy order into orderbook")

		# Create a new node for the order
		new_node = Node(order)

		# If the Orderbook Linked List is empty, make the new node the head
		if not self.head:
			self.head = new_node

		# Else if new order price is cheaper, make the new node the head
		elif self.head.order.price > new_node.order.price:
			new_node.next = self.head
			self.head = new_node

		# Else traverse the list and insert order based on the price-time priority
		else:
			curr_node = self.head
			while curr_node.next != None and curr_node.next.order.price <= new_node.order.price:
				curr_node = curr_node.next
			new_node.next = curr_node.next
			curr_node.next = new_node


	# Deletes order from the orderbook by id
	def delete_order_by_id(self, id):
		prev_node = None
		curr_node = self.head

		# If the head node itself needs to be deleted, just move head pointer forward
		if curr_node != None and curr_node.order.id == id:
			self.head = curr_node.next
			return

		# Search for the order to be deleted
		while curr_node != None and curr_node.order.id != id:
			prev_node = curr_node
			curr_node = curr_node.next

		# Do nothing if id not found
		if curr_node == None: return

		# Remove node from the list
		prev_node.next = curr_node.next

	def match_buy_order(self, order):

		if not order.is_buy: raise ValueError("Cannot match sell order")

		matched_orders = []

		# If orderbook is empty, return empty list
		if self.head == None: return matched_orders

		remaining_qty = order.quantity
		curr_node = self.head

		# Since we keep the orderbook already sorted by price-time priority, we can just iterate
        # the list and delete orders until our incoming order is completely matched
		while curr_node != None and remaining_qty > 0 and curr_node.order.price <= order.price:
			curr_order = curr_node.order
			if curr_order.unfilled_quantity <= remaining_qty:
				remaining_qty -= curr_order.unfilled_quantity
				curr_order.unfilled_quantity = 0
				matched_orders.append(curr_order)
				self.delete_order_by_id(curr_order.id)
			else:
				curr_order.unfilled_quantity -= remaining_qty
				remaining_qty = 0
				matched_orders.append(curr_order)
			curr_node = curr_node.next

		return matched_orders


# Prints out the Orderbook
def print_list(orderbook):
	curr_node = orderbook.head

	# Traverse through the list & print each order
	orderbook_str = ""
	while curr_node != None:
		orderbook_str += "{} -> ".format(curr_node.order)
		curr_node = curr_node.next
	orderbook_str += "None"
	print(orderbook_str)
	


# Driver Program
def main():
	# Read in positional arguments

	# Initialize order book
	orderbook = Orderbook()
	num_lines = int(next(sys.stdin))

	while num_lines > 0:
		# print("Num lines:", num_lines)
		line = next(sys.stdin)
		line_args = line.strip().split(" ")
		id = int(line_args[0])
		price = int(line_args[1])
		quantity = int(line_args[2])
		is_buy = line_args[3] == "True"
		time = int(line_args[4])
		operation = line_args[5]

		orderbook.process_order(
			Order(id, price, quantity, is_buy, time), operation
		)

		num_lines = num_lines-1;	

	# Get the final state of the orderbook and print to stdout
	curr_node = orderbook.head
	while curr_node != None:
		order = curr_node.order
		print("{} {} {} {} {} {}".format(
			order.id, order.price, order.quantity, order.unfilled_quantity, order.is_buy, order.time
		))
		curr_node = curr_node.next

main()
