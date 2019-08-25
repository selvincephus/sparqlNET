# sparqlNET
This work is part of my master thesis @ Chalmers University of Technology, Sweden.
This code is a byproduct of the research conducted during the thesis.

The train.py script is used to train an encoder-decoder RNN to learn features of 
english-SPARQL language pairs avaliable in data/eng-sparql.txt.

The translator.py script is an example application that uses the pytorch model output from train.py.

The trained model is available in encoder_decoder/..  

The tutorial below provided a good starting point for this project.
https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html
