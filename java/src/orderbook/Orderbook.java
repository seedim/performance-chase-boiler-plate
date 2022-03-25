package orderbook;

import java.util.ArrayList;

/**
 * An In-memory Orderbook represented by a Singly Linked List.
 *
 * This list is kept sorted by a price-time priority; lowest price orders are kept in the front
 * and if two orders have the same price, the order placed first is kept in front. For example:
 *  list -> (price: 1, time: 3) -> (price: 1, time: 4) -> (price: 2, time: 2) -> (price: 10, time: 1) -> null
 *
 * Author: Seed Labs Team
 */
public class Orderbook {

    // Head of list
    Node head;

    /** Linked list Node, inner class is static so that main() can access it */
    static class Node {
        Order order;
        Node next;
        Node(Order o) {
            order = o;
            next = null;
        }
    }

    /** If sell order, inserts order into the orderbook. If buy order, matches order against sell orders
     * in the orderbook
     * @param order
     */
    public void processOrder(Order order, String operation) {

        if (order == null) return;

        switch (operation) {
            case "cancel":
                deleteOrderById(order.id);
                break;
            case "insert":
                insertSellOrder(order);
                break;
            case "match":
                matchBuyOrder(order);
                break;
        }

        printList(this);
    }

    /** Inserts sell order into orderbook based on price-time priority */
    private void insertSellOrder(Order order) {

        if (order.isBuy()) throw new RuntimeException("Cannot insert buy order into orderbook");

        // Create a new node for the order
        Node newNode = new Node(order);
        newNode.next = null;

        // If the Orderbook Linked List is empty, make the new node the head
        if (head == null) {
            head = newNode;
        } else if (head.order.price > newNode.order.price) {
            // Else if new order price is the cheapest, make the new node the head
            newNode.next = head;
            head = newNode;
        } else {
            // Else traverse the list and insert order based on the price-time priority
            Node currNode = head;
            while (currNode.next != null && currNode.next.order.price <= newNode.order.price) {
                currNode = currNode.next;
            }
            newNode.next = currNode.next;
            currNode.next = newNode;
        }

    }

    /** Deletes order from the orderbook by id */
    private void deleteOrderById(int id) {

        Node prevNode = null;
        Node currNode = head;

        // If the head node itself needs to be deleted, just move head pointer forward
        if (currNode != null && currNode.order.id == id) {
            head = currNode.next;
            return;
        }

        // Search for the order to be deleted
        while (currNode != null && currNode.order.id != id) {
            prevNode = currNode;
            currNode = currNode.next;
        }

        // Do nothing if id not found
        if (currNode == null) return;

        // Remove node from the list
        prevNode.next = currNode.next;
    }

    /** Matches incoming buy order against orders in the book based on price-time priority.
     *
     * All matched orders are returned in an array and deleted from the orderbook. If any order in the book is
     * only partially matched, it is not deleted but has its quantity reduced & is returned as parted of matchedOrders.
     *
     * If the incoming order can not be entirely filled at the specified price and quantity,
     * the incoming order's unfilled quantity is ignored
     * */
    private ArrayList<Order> matchBuyOrder(Order order) {

        if (!order.isBuy()) throw new RuntimeException("Cannot match sell order");

        ArrayList<Order> matchedOrders = new ArrayList<>();

        // If orderbook is empty, return empty list
        if (head == null) return matchedOrders;

        int remainingQty = order.quantity;
        Node currNode = head;

        // Since we keep the orderbook already sorted by price-time priority, we can just iterate
        // the list and delete orders until our incoming order is completely matched
        while (currNode != null && remainingQty > 0 && currNode.order.price <= order.price) {
            Order currOrder =  currNode.order;
            if (currOrder.unfilledQty <= remainingQty) {
                remainingQty -= currOrder.unfilledQty;
                currOrder.unfilledQty = 0;
                matchedOrders.add(currOrder);
                deleteOrderById(currOrder.id);
            } else {
                currOrder.unfilledQty -= remainingQty;
                remainingQty = 0;
                matchedOrders.add(currOrder);
            }
            currNode = currNode.next;
        }

        return matchedOrders;
    }



    /** Prints out the Orderbook */
    public static void printList(Orderbook list)
    {
        Node currNode = list.head;

        System.out.print("Orderbook: ");

        // Traverse through the list & print each order
        while (currNode != null) {
            System.out.print(currNode.order + " -> ");
            currNode = currNode.next;
        }
        System.out.print("null");
        System.out.println();
    }

    public static void main(String[] args) {

        // Start with an empty orderbook
        Orderbook orderbook = new Orderbook();

        // Insert some orders
        orderbook.processOrder(new Order(1, 10, 5, false, 1), "insert");
        orderbook.processOrder(new Order(2, 2, 4, false, 2), "insert");
        orderbook.processOrder(new Order(3, 1, 6, false, 3), "insert");
        orderbook.processOrder(new Order(4, 1, 1, false, 4), "insert");


        // Match an order
        orderbook.processOrder(new Order(7, 3, 10, true, 5), "match");

    }
}