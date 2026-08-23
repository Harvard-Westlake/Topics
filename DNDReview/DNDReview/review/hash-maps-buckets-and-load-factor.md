# Review — Hash Maps: Buckets, Collisions, and Load Factor

*Originally covered in [DNDReview](../README.md)*

---

| Concept | Reference |
|---|---|
| Hash function | Deterministic: same key → same bucket index, in O(1) |
| Bucket index | `hash(key) % numberOfBuckets` |
| Collision | Two different keys land in the same bucket — resolved here by chaining |
| Load factor | `stored elements / total buckets`; resize past 0.75 |
| Resize | Double the buckets, then **rehash every key** |

```java
import java.util.ArrayList;

public class MiniHashMap {
    // One chain (ArrayList of entries) per bucket — chaining collision resolution
    private ArrayList<ArrayList<Entry>> buckets = new ArrayList<>();
    private int stored = 0;

    public MiniHashMap() {
        for (int bucketIndex = 0; bucketIndex < 4; bucketIndex++) {
            buckets.add(new ArrayList<Entry>());
        }
    }

    // Hand-checkable hash: the key's length
    private int bucketFor(String key) {
        return key.length() % buckets.size();
    }

    public void put(String key, int value) {
        buckets.get(bucketFor(key)).add(new Entry(key, value));
        stored++;
    }
}

class Entry {
    private String key;
    private int value;

    public Entry(String key, int value) {
        this.key = key;
        this.value = value;
    }

    // Assume proper getters and setters exist for every field:
    // getKey(), getValue(), setValue(int)
}
```

---

## Tasks

1. **Compute the buckets by hand.** With 4 buckets and `bucketFor = key.length() % 4`, place each key: `"pizza"`, `"cola"`, `"soup"`, `"tea"`, `"breadsticks"`. Which keys collide, and in which bucket? Then answer: is a collision an error? What does the chaining ArrayList do about it?

2. **Complete `get`.** A bucket may hold several entries, so finding a value means hashing to the right chain and then checking keys inside it. Fill in the two blanks, then answer: in the worst case (every key in one bucket), what does the O(1) lookup degrade to?

   ```java
   public int get(String key) {
       ArrayList<Entry> chain = buckets.get(________);   // which bucket to search
       for (Entry entry : chain) {
           if (entry.getKey().equals(________)) {        // confirm the exact key
               return entry.getValue();
           }
       }
       return -1;   // not found
   }
   ```

3. **Reason about resizing.** With 4 buckets and the five keys from Task 1 stored, compute the load factor. It exceeds 0.75, so the map doubles to 8 buckets. Recompute `bucketFor("cola")` and `bucketFor("breadsticks")` with the new bucket count — did they move? Explain why every key must be rehashed after a resize, using this line as your evidence:

   ```java
   int before = key.length() % 4;   // bucket in the old table
   int after  = key.length() % 8;   // bucket in the new table
   ```
