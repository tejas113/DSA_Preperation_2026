# 355. Design Twitter

**LC 355** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Min-heap merge of `k` sorted lists (each followed user's tweets)

---

## 1. Intuition

A user's news feed is the 10 most recent tweets among everyone they follow, themselves included. Each person's own tweets are already in time order, because we only ever append. So the feed is a merge of several sorted lists, and we only need the first 10 results. We never need to sort all the tweets.

* `self.count` is a global timestamp that goes **down** (`0, -1, -2, ...`). `heapq` is a min-heap, so the most recent tweet (the most negative number) comes out first. This is the "negate for a max-heap" trick, applied to time.
* `self.tweet_map[userId]` holds `[count, tweetId]` pairs in the order posted, so the last item is the newest.
* In `getNewsFeed`, the heap starts with only the **newest** tweet of each followed user: `[count, tweetId, followeeId, index - 1]`. The last field is the position of that user's next-older tweet.
* `while min_heap and len(res) < 10` pops the newest tweet overall, adds it to `res`, then pushes that same user's next-older tweet (`index >= 0`). Only one tweet per user is in the heap at a time.
* `self.follow_map[userId].add(userId)` makes every user follow themselves, so their own tweets appear in their feed.

**Recall:** global timestamp counting down; heap holds each followed user's newest tweet; pop, then push that user's next-older one; stop at 10.

---

## 2. Approach

* **Idea:** Store tweets per user in posting order. To build a feed, do a k-way merge: put the newest tweet of every followed user in a min-heap, then repeat 10 times: pop the newest, push the next-older tweet of the same user.
* **Data structure / pointers:**
  * `self.count`: a global timestamp that decreases by 1 per tweet, so a smaller value means a newer tweet.
  * `self.tweet_map`: `userId` to a list of `[count, tweetId]`, oldest first.
  * `self.follow_map`: `userId` to a set of followee ids.
  * `min_heap`: a **min-heap** of `[count, tweetId, followeeId, next_index]` lists. It has no size cap, but it never holds more than one entry per followed user. Root is the newest tweet among those entries. Since `count` is a negative-going timestamp, the smallest `count` is the newest tweet.
  * Tie-breaker: lists compare left to right. `count` is unique for every tweet, so the comparison is always decided by the first field, and the later fields are never compared.
  * `index`: position of that user's next-older tweet in their list. `-1` means there is none.
* **Invariant:** The heap holds, for each followed user, their newest tweet that has not been added to `res` yet. So the root is always the newest remaining tweet in the whole feed.
* **Edge cases:**
  * A user who follows nobody and has not tweeted: `getNewsFeed` returns `[]`.
  * Users with no tweets: the `if followeeId in self.tweet_map and self.tweet_map[followeeId]` check keeps empty lists out of the heap. (Using `in` first also avoids creating empty entries in the `defaultdict`.)
  * Fewer than 10 tweets in total: the loop stops when the heap is empty.
  * More than 10 tweets: the loop stops at 10, even if tweets remain.
  * Unfollowing yourself does nothing, because of `followerId != followeeId`. Unfollowing someone you don't follow is safe too.
  * Following yourself, or following someone twice, changes nothing, since `follow_map` stores sets.

---

## 3. Code

```python
from collections import defaultdict
import heapq


class Twitter:

    def __init__(self):
        self.count = 0  # Global timestamp counter (decremented for max-heap behavior)
        self.tweet_map = defaultdict(list)  # userId -> list of [count, tweetId]
        self.follow_map = defaultdict(set)  # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweet_map[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> list[int]:
        res = []
        min_heap = []

        # Ensure user follows themselves to see their own tweets
        self.follow_map[userId].add(userId)

        # Push the most recent tweet of each followee into the heap
        for followeeId in self.follow_map[userId]:
            if followeeId in self.tweet_map and self.tweet_map[followeeId]:
                index = len(self.tweet_map[followeeId]) - 1
                count, tweetId = self.tweet_map[followeeId][index]
                # Heap stores: [count, tweetId, followeeId, next_index_in_list]
                min_heap.append([count, tweetId, followeeId, index - 1])

        heapq.heapify(min_heap)

        # Pull top 10 most recent tweets across all followed users
        while min_heap and len(res) < 10:
            count, tweetId, followeeId, index = heapq.heappop(min_heap)
            res.append(tweetId)

            # If the user has older tweets, push the next recent one into the heap
            if index >= 0:
                count, tweetId = self.tweet_map[followeeId][index]
                heapq.heappush(
                    min_heap, [count, tweetId, followeeId, index - 1]
                )

        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follow_map[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.follow_map[followerId] and followerId != followeeId:
            self.follow_map[followerId].remove(followeeId)


if __name__ == "__main__":
    twitter = Twitter()
    twitter.postTweet(1, 5)
    assert twitter.getNewsFeed(1) == [5]
    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    assert twitter.getNewsFeed(1) == [6, 5]
    twitter.unfollow(1, 2)
    assert twitter.getNewsFeed(1) == [5]

    assert Twitter().getNewsFeed(7) == []

    many = Twitter()
    for tweet_id in range(1, 16):
        many.postTweet(1, tweet_id)
    assert many.getNewsFeed(1) == list(range(15, 5, -1))

    many.unfollow(1, 1)
    assert many.getNewsFeed(1) == list(range(15, 5, -1))
    print("All tests passed")
```

---

## 4. Dry Run

LeetCode example 1. `count` starts at `0`. The heap entries are `[count, tweetId, followeeId, next_index]`.

| Operation | State | `min_heap` at its start (after `heapify`) | Result |
| --- | --- | --- | --- |
| `postTweet(1, 5)` | `tweet_map[1] = [[0, 5]]`, `count = -1` | - | - |
| `getNewsFeed(1)` | user 1 follows self | `[[0, 5, 1, -1]]` | pop gives `5`, no older tweet, so `[5]` |
| `follow(1, 2)` | `follow_map[1] = {1, 2}` | - | - |
| `postTweet(2, 6)` | `tweet_map[2] = [[-1, 6]]`, `count = -2` | - | - |
| `getNewsFeed(1)` | user 1 has `[[0, 5]]`, user 2 has `[[-1, 6]]` | `[[-1, 6, 2, -1], [0, 5, 1, -1]]` | pop `-1` (tweet 6), then pop `0` (tweet 5), so `[6, 5]` |
| `unfollow(1, 2)` | `follow_map[1] = {1}` | - | - |
| `getNewsFeed(1)` | only user 1 | `[[0, 5, 1, -1]]` | `[5]` |

`-1` is smaller than `0`, so tweet 6 (newer) is on top of the heap.

---

## 5. Complexity

* **`postTweet`:** O(1). One list append and one subtraction.
* **`follow` and `unfollow`:** O(1). A set add or remove.
* **`getNewsFeed`:** O(F + 10 log F), where `F` is the number of users the user follows (including themselves). Building and heapifying the starting heap is O(F), then at most 10 pops and 10 pushes on a heap of at most `F` items.
* **Space:** O(U + T), where `U` counts follow relationships and `T` counts all tweets ever posted. The heap inside `getNewsFeed` is O(F).

---

## 6. Recall (30 seconds)

* Global `count` that goes down means the newest tweet has the smallest number, so a min-heap yields newest first.
* `getNewsFeed`: heapify the newest tweet of each followed user (including yourself), then pop up to 10, pushing each popped user's next-older tweet (`index - 1`).
* `unfollow` ignores yourself, and a followee with no tweets is skipped.
