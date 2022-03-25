package orderbook;

import java.util.Date;

public class Order {
    final int id;
    final double price;
    final int quantity;
    int unfilledQty;
    final boolean isBuy;
    final long time;


    public Order(int id, double price, int quantity, boolean isBuy, long time) {
        this.id = id;
        this.price = price;
        this.quantity = quantity;
        this.unfilledQty = quantity;
        this.isBuy = isBuy;
        this.time = time;
    }

    public int getId() {
        return id;
    }

    public double getPrice() {
        return price;
    }

    public int getQuantity() {
        return quantity;
    }

    public long getTime() {
        return time;
    }

    public int getUnfilledQty() {
        return unfilledQty;
    }

    public boolean isBuy() {
        return isBuy;
    }

    @Override
    public String toString() {
        return "Order(" + "id: " + id + ", price: " + price + ", qty: " + quantity + ", isBuy: " + isBuy + ", time: " + time + ")";
    }
}
