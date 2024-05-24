#!/usr/bin/env python
# coding: utf-8

def github() -> str:
    """
    This function returns a link to the GitHub repository containing solutions.

    Returns:
        str: The URL to the GitHub repository.
    """
    return "https://github.com/anasfathul/ECON481/blob/main/ECON481_HW6.py"




# Exercise 1
def std() -> str:
    """
    This function return sql query that outputs a table that has two columns: itemId and std, the standard deviation of bids for that item.
    """
    query = """
    SELECT bids.itemID, SQRT(SUM((bidAmount - avgBid) * (bidAmount - avgBid)) / (COUNT(bidAmount) - 1)) AS std
    FROM bids
    JOIN (
        SELECT itemID, AVG(bidAmount) AS avgBid
        FROM bids
        GROUP BY itemID
        having COUNT(*) > 1
    ) sub ON bids.itemID = sub.itemID
    GROUP BY bids.itemID
    """
    return query

# Exercise 2
def bidder_spend_frac() -> str:
    """
    This function return sql query that outputs a table that has four columns:
    bidderName: the name of the bidder
    total_spend: the amount the bidder spent (that is, the sum of their winning bids)
    total_bids: the amount the bidder bid, regardless of the outcome.
    NB: bidders may submit multiple bids for an item – if this is the case only count their highest bid for an item for this calculation.
    spend_frac: total_spend/total_bids
    """
    query = """
    WITH Winner AS (
        SELECT bidderName, SUM(sub.max_bid) as total_spend
        FROM (
            SELECT itemid, bidderName, MAX(bidAmount) as max_bid
            FROM bids
            GROUP BY itemid
        ) AS sub
        GROUP BY bidderName
    ), 
    HighestBid AS (
        SELECT s.bidderName, SUM(s.max_bid) as total_bids
        FROM (
            SELECT itemid, bidderName, MAX(bidAmount) as max_bid
            FROM bids
            GROUP BY itemid, bidderName
        ) as s
        GROUP BY bidderName
    )
    SELECT h.bidderName,
        IFNULL(w.total_spend, 0) as total_spend,
        IFNULL(h.total_bids, 0) as total_bids,
        IFNULL((w.total_spend / h.total_bids), 0) as spend_frac
    FROM HighestBid h
    LEFT JOIN Winner w ON h.bidderName = w.bidderName
    """
    return query

# Exercise 3
def min_increment_freq() -> str:
    """
    This function return a SQL query that outputs a table that has one column (freq) which represents
    the fraction of bids in the database that are exactly the minimum bid increment (items.bidIncrement)
    above the previous high bid.
    """
    query = """
    WITH itemAlter AS (
        SELECT itemId, bidIncrement 
        FROM items 
        WHERE isBuyNowUsed != 1
    ),
    bidsWithIncrement AS (
        SELECT 
            b.*, 
            i.bidIncrement
        FROM 
            bids b
        LEFT JOIN 
            itemAlter i ON b.itemId = i.itemId
    ),
    bidsLagged AS (
        SELECT 
            itemid,
            itemprice,
            bidAmount,
            bidIncrement,
            LAG(bidAmount) OVER (PARTITION BY itemid ORDER BY bidtime) AS lagged_bidAmount,
            (bidAmount - LAG(bidAmount) OVER (PARTITION BY itemid ORDER BY bidtime)) AS increment
        FROM bidsWithIncrement
    )
    SELECT 
        CAST(SUM(CASE WHEN increment = bidIncrement THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS freq
    FROM 
        bidsLagged
    """
    return query

# Exercise 4
def win_perc_by_timestamp() -> str:
    """
    This function return a SQL query that outputs a table that has two columns:
    timestamp_bin: Using the same methodology as in the slides to normalize the percentage of time remaining in the auction when a bid is placed,
    normalize the bid timestamp and classify it as one of ten bins: 1 corresponds to 0-.1, 2 corresponds to .1-.2, etc.
    win_perc: the frequency with which a bid placed with this timestamp bin won the auction.
    """
    query = """
    WITH partA AS (
        SELECT 
            i.itemid, 
            i.starttime, 
            i.endtime, 
            julianday(i.endtime) - julianday(i.starttime) AS length
        FROM items AS i
    ),
    partitionB AS (
        SELECT 
            b.itemid, 
            b.bidtime, 
            a.starttime, 
            a.endtime,
            CASE 
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.1 THEN 1
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.2 THEN 2
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.3 THEN 3
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.4 THEN 4
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.5 THEN 5
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.6 THEN 6
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.7 THEN 7
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.8 THEN 8
                WHEN (julianday(a.endtime) - julianday(b.bidtime)) / a.length <= 0.9 THEN 9
                ELSE 10
            END AS timestamp_bin,
            MAX(b.bidamount) OVER (PARTITION BY b.itemid) AS max_bid,
            b.bidamount
        FROM bids AS b
        INNER JOIN partA AS a
        ON b.itemid = a.itemid
    ),
    partC AS (
        SELECT 
            timestamp_bin, 
            CASE 
                WHEN bidamount = max_bid THEN 1 
                ELSE 0 
            END AS freq
        FROM partitionB
    )
    SELECT 
        timestamp_bin, 
        SUM(freq) * 1.0 / COUNT(*) AS win_perc
    FROM partC
    GROUP BY timestamp_bin
    """
    
    return query