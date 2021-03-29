Mempy3 Readme
=============


Project structure
-----------------

The project 

* config.py
    * Stores project wide variables and data paths.
* preprocess
    * Contains all tools related to preprocessing.
    * This includes extraction from source files and all the cleaning steps. 
    * Also handles the generation of corpusframes, which are DataFrames representing different aspects of the corpus.
* analysis
    * analysis algos, work from preprocessed docs.
    * Contains all analysis tools (topic modeling, clustering, etc.).
    * Works from DocModels / corpusframes data.
    * Everything should be reusable on other corpora as long as the data is structured in the same way.
* results
    * Tools to format data for visualization or publication.
* utils
    * Various tools or util functions used around the project.
* viewer
    * Dash visualization app.
    * **Deprecated, is now it's own project.**
    * See [Memviz](https://github.com/PolycarpeLeGrand/Memviz) 

