# Activity - Lay Out a Collection

*Concept: Decide what your collections, documents, and fields are, then build that layout by hand in the Firebase console.*

![Animated diagram of data being stored. On the left, your page calls setDoc for the collection tastes and the document games with three key and value pairs. One at a time, the pairs favorite: Wordle, why: one puzzle a day, and rating: 9 slide across to Firestore on the right and land as three fields inside the document named games, which sits inside the collection named tastes. Each one is marked saved as it lands. A caption says a document is a JSON object with a name, and the collection is the folder it is filed in.](../assets/fields-into-document.svg)

## Task

1. On paper, lay out a `tastes` collection for yourself: three documents (for example `games`, `websites`, `wishes`) with two or three fields each. Write every field as a key and a value.
2. Open the [Firebase console](https://console.firebase.google.com/), choose your project, and open **Build**, then **Firestore Database**. Create the database if you have not yet (Standard edition, test mode).
3. Click **Start collection**. The collection ID is `tastes`.
4. The console asks for the first document. Give it the **Document ID** `games`, add each field from your paper with its type (string, number, boolean, or array), and save.
5. Use **Add document** for your other two documents. Give each a name you chose, not an Auto-ID.
6. Read the path at the top of the console for one document, such as `tastes/games`. Say it out loud as "collection, then document".
