import distutils, os, sys
from order import Order

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
	test_input_filename = sys.argv[1]
	
	# Generate path to test input file
	tst_dir_name = os.path.dirname(__file__).split("src")[0]
	test_input_file_path = os.path.join(tst_dir_name, "resources/{}".format(test_input_filename))

	# Initialize order book
	orderbook = Orderbook()

	# Read test input file from file path
	test_input_file = open(test_input_file_path, 'r')
	input_lines = test_input_file.readlines()
	num_lines = input_lines.pop(0)

	# Process orders line by line
	for _ in range(int(num_lines)):
		line_args = input_lines.pop(0).strip().split(" ")
		id = int(line_args[0])
		price = int(line_args[1])
		quantity = int(line_args[2])
		is_buy = bool(distutils.util.strtobool(line_args[3]))
		time = int(line_args[4])
		operation = line_args[5]

		orderbook.process_order(
			Order(id, price, quantity, is_buy, time), operation
		)

	# Get the final state of the orderbook and print to stdout
	curr_node = orderbook.head
	while curr_node != None:
		order = curr_node.order
		print("{} {} {} {} {} {}".format(
			order.id, order.price, order.quantity, order.unfilled_quantity, order.is_buy, order.time
		))
		curr_node = curr_node.next

if __name__ == "__main__":
    main()