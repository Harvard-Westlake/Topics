# Activity — The Path Finder

*Concept: Experiencing the strict difference between absolute and relative paths in code.*

## Task

1. On your Desktop, create a new folder called `path-activity`. Inside it, create three files:
   - `PathFinder.java` (paste the code below into it)
   - `absolute.txt` containing exactly: `I am absolute!`
   - `relative.txt` containing exactly: `I am relative!`
2. Open `PathFinder.java` and update the `absolutePath` string so it matches your own computer's real path to `absolute.txt` (see the comments in the code for examples).
3. Compile and run the program from inside `path-activity`:
   ```bash
   cd path-activity
   javac PathFinder.java
   java PathFinder
   ```
   Both reads should print `SUCCESS`.
4. Now run the program again from *outside* the folder:
   ```bash
   cd ..
   java -cp path-activity PathFinder
   ```
   Watch what happens: the absolute path still succeeds, but the relative path fails — because `relative.txt` is no longer sitting where the terminal's `pwd` is looking.
5. In your own words, write one sentence explaining why the absolute path survived the move but the relative path didn't.

**Code for `PathFinder.java`:**

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class PathFinder {
    public static void main(String[] args) {
        // 1. ABSOLUTE PATH (change this to match your actual computer's path!)
        // Mac/Linux example: "/Users/yourname/Desktop/path-activity/absolute.txt"
        // Windows WSL example: "/mnt/c/Users/yourname/Desktop/path-activity/absolute.txt"
        String absolutePath = "/Users/REPLACE_ME/Desktop/path-activity/absolute.txt";

        System.out.println("--- Reading Absolute Path ---");
        try (BufferedReader br = new BufferedReader(new FileReader(absolutePath))) {
            System.out.println("SUCCESS: " + br.readLine());
        } catch (IOException e) {
            System.out.println("FAIL: Could not find the absolute file. Did you update the path string?");
        }

        // 2. RELATIVE PATH (looks for the file exactly where the terminal is currently sitting)
        String relativePath = "relative.txt";

        System.out.println("\n--- Reading Relative Path ---");
        try (BufferedReader br = new BufferedReader(new FileReader(relativePath))) {
            System.out.println("SUCCESS: " + br.readLine());
        } catch (IOException e) {
            System.out.println("FAIL: Could not find the relative file. Are you in the right folder?");
        }
    }
}
```
