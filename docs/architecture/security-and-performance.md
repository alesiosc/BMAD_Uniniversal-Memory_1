# Security and Performance

### Security Requirements
The application's primary security principle is **user privacy through local-first data storage**, as mandated by the PRD.

* **Data Security:** No user-generated data (captured conversations, metadata, etc.) will be transmitted to any external server. All data remains on the user's local machine.
* **Frontend Security:** The Tauri application will be configured with a strict Content Security Policy (CSP) to mitigate the risk of cross-site scripting (XSS) attacks within the webview.
* **Backend Security:** The local Python API will only be accessible from the Tauri application itself, preventing unauthorized access from other applications on the user's machine.
* **Dependency Security:** We will use tools to scan both npm and Python dependencies for known vulnerabilities.

### Performance Optimization
The application must feel fast and responsive, adhering to the goals in the PRD and UI/UX Specification.

* **Frontend Performance:**
    * **List Virtualization:** To handle potentially thousands of memories, the UI will only render the items currently visible on the screen, ensuring the feed remains fast.
    * **Debounced Search:** The search input will have a small delay (debounce) to prevent firing off a new search on every single keystroke, improving efficiency.
    * **Code Splitting:** The application will be bundled to load code for different views on demand, ensuring a fast initial startup time.
* **Backend Performance:**
    * **Database Indexing:** The SQLite database will have indexes on frequently queried columns (like `timestamp`) to speed up data retrieval.
    * **Efficient Embeddings:** The choice of a local embedding model will balance search accuracy with the performance impact on the user's CPU.