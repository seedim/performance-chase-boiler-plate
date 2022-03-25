# Performance Chase Challenge

# Introduction

Welcome to Performance Chase! This challenge will test your data structures & algorithms knowledge to use in designing an extremely efficient in-memory Orderbook - a service that facilitates fast trade matching in exchanges! All performant exchanges design this service in memory to achieve ultra fast speeds, often able to process a few hundred thousand orders in a second. Building a fully functioning service like this though takes some time, so we’ll be focusing on optimizing a much simpler version that already implements the major functionality. 

## The Challenge

The Seed Labs team has been building an in-memory Orderbook to serve all incoming users on their exchange; however, they’ve been facing several performance bottlenecks. The Orderbook is fully functional and passes all unit tests ensuring its reliability, but its implementation suffers from a naive choice of data-structures 😟 Your team has been invited to come take a look at the codebase and strategize a better choice of data-structures and algorithms to help improve the Orderbook’s performance. Your refactor of the service should improve the performance of the operations made against the Orderbook while maintaining its correctness.

## A Simplified Orderbook

The Orderbook implementation being shared is an in-memory service the only has a Sell Orderbook. This means all Sell Orders submitted to the orderbook are kept in an open state in-memory waiting to be matched. Buy orders on the other hand are never kept in open state, they are immediately matched against the Open Sell Orders.

Let’s understand some of these terms more:

- **Order**: An order, as found in the `Order` class, is how a hypothetical user submits the `price` and `quantity` of an asset they’d like to purchase or sell.
- **Open Order:** An order is in an open state if it’s sitting in the orderbook’s data store waiting to be matched.

Operations allowed against the Orderbook:

- **Insert:** Inserts a Sell Order into the orderbook as it waits to be matched
- **Cancel:** Deletes a Sell Order from the orderbook if it has not yet been matched
- **Match:** Matches an incoming Buy Order against the Open Sell Orders, outputs an array of the matched Sell Order IDs and deletes them from the orderbook. The returned IDs are sorted in the order in which there were matched.
    1. For a Buy Order to match a Sell Order, the Buy Order’s `price` must be `<=` to the Sell Order’s `price`. The Buy Order must keep getting matched until its entire specified `quantity` has been filled.
    2. If there isn’t enough Open Sell Orders in the orderbook to match the entire Buy order’s quantity, the remaining portion of the Buy Order `quantity` can be ignored.
    3. Matching must follow “Price-Time” priority; a Buy Order should match the cheapest available Sell Order first. If there are multiple Sell Orders at the same price, the Sell Order placed first should get matched first.
    
    Let’s see some examples:
    
    ```jsx
    **Example 1: Basic**
    Orderbook: Order(id: 1, time: 1, price: 4, qty: 6, side: sell),
    					 Order(id: 2, time: 2, price: 7, qty: 8, side: sell)
    Incoming Buy Order: Order(id: 3, time: 3, price: 4, qty: 6, side: buy)
    // Result
    Matched Order Ids: [1]
    Orderbook After:  Order(id: 2, time: 2, price: 7, qty: 8, side: sell)
    
    **Example 2: Basic**
    Orderbook: Order(id: 1, time: 1, price: 4, qty: 6, side: sell),
    					 Order(id: 2, time: 2, price: 7, qty: 8, side: sell),
    					 Order(id: 3, time: 3, price: 12, qty: 4, side: sell)
    Incoming Buy Order: Order(id: 4, time: 4, price: 9, qty: 10, side: buy)
    // Result
    Matched Order Ids: [1, 2]
    																								 // Qty reduced
    Orderbook After:  Order(id: 2, time: 2, price: 7, qty: 4, side: sell)
    									Order(id: 3, time: 3, price: 12, qty: 4, side: sell)
    
    **Example 3: No Match**
    Orderbook: Order(id: 1, time: 1, price: 4, qty: 6, side: sell),
    					 Order(id: 2, time: 2, price: 7, qty: 8, side: sell)
    Incoming Buy Order: Order(id: 3, time: 3, price: 2, qty: 4, side: buy)
    // Result
    Matched Order Ids: [] // No match found at the specified price
    Orderbook After: Order(id: 1, time: 1, price: 4, qty: 6, side: sell),
    								 Order(id: 2, time: 2, price: 7, qty: 8, side: sell)
    
    **Example 4: Not Enough Open Orders**
    Orderbook: Order(id: 1, time: 1, price: 4, qty: 6, side: sell),
    					 Order(id: 2, time: 2, price: 7, qty: 8, side: sell)
    Incoming Buy Order: Order(id: 3, time: 3, price: 10, qty: 100, side: buy)
    // Result
    Matched Order Ids: [1, 2] // Matched as many orders as possible 
    Orderbook After: empty
    
    **Example 5: Price Time Priority**
    Orderbook: Order(id: 3, time: 3, price: 5, qty: 6, side: sell),
    					 Order(id: 4, time: 4, price: 5, qty: 2, side: sell),
    					 Order(id: 2, time: 2, price: 10, qty: 8, side: sell)
    					 Order(id: 1, time: 1, price: 11, qty: 4, side: sell)
    Incoming Buy Order: Order(id: 5, time: 5, price: 9, qty: 10, side: buy)
    // Result
    Matched Order Ids: [3, 4, 2]
    Orderbook After: Order(id: 2, time: 2, price: 10, qty: 6, side: sell)
    								 Order(id: 1, time: 1, price: 11, qty: 4, side: sell)
    ```
    

## Goals

- Understand the current implementation of the three possible operations: insert orders, cancel orders, and match orders based on price-time priority
- Strategize optimizations for each of the three operations that will increase their respective performance. Optimizations will range from simple improvements in the algorithms carrying out of these operations to entire overhauls in the choice of data-structures representing the Orderbook. As you strategize possible changes, make sure to consider trade-offs on the other operations; for example, achieving O(1) complexity in one operation at the consequence of O(n^3) complexity in another is not optimal. You may assume unlimited memory; i.e, optimize for latency not memory.
- Implement your optimizations. Changes to the operations and data structures **must continue to pass all functionality tests to count as a valid submission**. *Tip: Validate your changes against the provided tests often so that you’re not going down long incorrect tangents that may be hard to recover from. Start with small optimizations for easy points incase you run out of time doing a larger design changes later.*

## Technical Details

### Sample Input/Output(s):

The testing code reads from stdin and output the state of the orderbook on console using stdout once a test is exhausted. A test script reads in the stdin in the following order: 

1. Number N on its first line, this N indicates the number of order requests to process. 
2. The next N lines will each contain an order’s information in the following sequence: 
    1. **id:** the id of the order
    2. **price**: price at which user wishes to BUY or SELL
    3. **quantity**: the amount of asset user wishes to BUY or SELL
    4. **isBuy**: True is the user wishes to buy, false other wise
    5. **timestamp**: unix timestamp at which order was placed
    6. **Operation**: operation to be performed on order, will be one of the three `insert`, `match`, and `cancel`

*Sample_Input_01.txt*

```jsx
5
1 10 5 False 1 insert
2 2 4 False 2 insert
3 1 6 False 3 insert
4 1 1 False 4 insert
5 3 10 True 5 match
```

After processing the entire input case, print the state of orderbook on console in the format provided in *Sample_Output_01.txt*. On each line print 1 order. For each order things to be printed are: id, price, quantity, unfilled_quantity, is_buy, time.

*Sample_Output_01.txt*

```jsx
2 2 4 1 False 2
1 10 5 5 False 1
```

### Groundwork

You can clone our simple implementation of the Orderbook written in Python or Java from our repo over [here](https://github.com/seedim/performance-chase-boiler-plate).  The implementation passes all functional tests but fails on time evaluation tests. The codebase does the following:

- Reads in a test case file path as input.
- Parses the test cases line by line.
- Forwards the parsed order request to `process_order` function.
- Once all orders are processed, outputs the state of orderbook to console.

The codebase can be used to serve as foundation for your implementation and can also be used to evaluate your implementation as the boiler plate is guaranteed to generate the correct output on input test cases.

## Evaluation Criteria

The goal of the competition is to submit an optimized version of the in-memory orderbook that improves the speed of inserting, matching and cancelling an order. The winning team of the competition will be the one whose implementation:

- Passes all unit/functional tests
- Takes the least amount of time to execute all cases

DomJudge will auto grade all submissions - the implementation will be considered `WRONG` if it fails any of the functional tests and inefficient if it takes time > time threshold (`TIMELIMIT`). 

Submissions can be made here: [http://13.214.166.24:12345/jury/problems](http://13.214.166.24:12345/jury/problems) 

There is no limitation on number of submissions and submitting invalid/incorrect implementation does not have any effect on the outcome of competition. We will consider your fastest valid submission.

The choice of language may play a small role in getting a lower execution time. However, the competition is language agnostic - we care about your understanding and application of data structures not choice of languages. So it is possible that team A and B both implement the same solution but since A is using a lower level language, their execution time is < B’s. To normalize such a scenario, the final submission will be manually reviewed by the Seed Labs team.
