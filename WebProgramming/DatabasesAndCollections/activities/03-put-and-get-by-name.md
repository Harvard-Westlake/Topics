# Activity - Put and Get by Name

*Concept: Write one document from your own page and read it back, naming the collection and the document each time.*

![Animated diagram of a put and a get. Firestore on the right holds a collection named tastes with documents games, websites, and wishes, and a collection named scores with a document high-score. First the put: setDoc names tastes and games, the tastes collection lights up, then the games document lights up, a dot carries the data into it, and the page shows saved: tastes/games. Then the get: getDoc names tastes and games, the same collection and document light up, a dot travels back to the page, and the page shows the fields favorite: Wordle and rating: 9. The websites and wishes documents and the whole scores collection are labeled not named, not touched.](../assets/put-get-by-name.svg)

## Task

1. In VS Code, add the Firestore module script from the lesson to your page, with your own `firebaseConfig`, and reload with the Console open. You should see `Connected to Firestore`.
2. Put a document. Inside the module script, add:
   ```javascript
   await setDoc(doc(database, "tastes", "today"), {
     enjoyed: "something you enjoyed on the web today",
     rating: 8
   });
   console.log("Saved tastes/today");
   ```
3. Reload, then find `tastes/today` in the Firebase console. If it is not there, the write did not happen: read the Console error.
4. Get it back. Add:
   ```javascript
   const snapshot = await getDoc(doc(database, "tastes", "today"));
   console.log(snapshot.exists(), snapshot.data());
   ```
5. Change `"today"` in the `getDoc` line to a name that does not exist and reload. Nothing crashes: `exists()` is `false`.
6. Change `"tastes"` in the `setDoc` line to `"taste"` and reload. Look in the Firebase console: a misspelled name quietly created a second collection. Delete it, and fix the name.
