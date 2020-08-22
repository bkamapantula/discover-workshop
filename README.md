# discover-workshop
Code search utility using bag of words estimator.

## How it works

<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.6.0/mermaid.min.js"></script>

## Overview

### Fetch data from GitLab

```mermaid
  graph TD;
      Code-files-->Local-Disk;
      Local-Disk--> BoW;
      BoW --> Document-Matrix;
      Document-Matrix --> Vectorizer;
```

BoW refers to Bag of Words model.

### Query against the data

```mermaid
  graph TD;
      User-Query--> BoW;
      BoW-->Cosine-Similarity;
      Cosine-Similarity-->Projects;
      Projects-->Snippets;
```

Cosine Similarity is performed on the input vector (user query) and document matrix.

