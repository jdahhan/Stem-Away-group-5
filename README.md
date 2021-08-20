# STEM Away - Learning the Structure of Biomedical Relationships from Unstructured Text

We are now a society not with too little information, but too much information. There are more news articles each day that comes out that humans can ever possibly consume. In a landscape with an overflow of data, humans have a hard time consolidating huge volumes of data. Computers, on the other hand, have the necessary power and even can thrive in an environment with too much data. These scenarios are the places where ML algorithms can thrive. This project sheds light on some of the most powerful techniques available to deal with this gargantuous volume of unstructured text such as distributional semantics and biclustering.

This project replicates and extends the bioinformatic research at Stanford University of Percha and Altman 2015 titled “Learning the Structure of Biomedical Relationships from Unstructured Text.”

Her hypothesis is:

    Distributional techniques can partially or completely replace human curated lexicons and ontologies for normalization in biomedical text mining.
  
Furthermore, these distribtional techniques will enable us to do:
1) `Prediction`: New drug-drug and other bioinformatic interactions
2) `Evaluation`: Against human curated databases
3) `Automation`: Synthesizing new pharmacogenomic pathways from unstructured text and research articles


### Biomedical Data

Medline contains 23 million articles and is growing at a rate of several hundred thousand new articles each year from over 5500 unique journals. We must be able to decipher when two sentences are referring to the same thing. The answer we wish to seek is: can we find themes in the clusters of depedency paths connecting a drug and a gene? If so, there is strong potential to propose novel drug-target relationships for clinicians and health practioners - something that is extremely valuable considering that it costs $3-10 billion to develop a new drug and drug targets with genetically supported targets are twice as likely to lead successful approval.

That is the power of outsourcing complexity to a computer.

## Our Pipeline:

The modularization in this pipeline diagram maps 1-1 to the actual code above. It is our entire pipeline condensed into one diagram. 

![STEM Away - Pipeline Version 3](https://user-images.githubusercontent.com/44710581/129920146-f5107736-62c3-49db-98f8-a0bd2a1830ee.png)

## EBC Scoring

A little deeper dive into how each EBC trial is being scored.

![STEM Away - EBC Scoring Rule-2](https://user-images.githubusercontent.com/44710581/130164649-7176240f-6717-4bf7-9437-6213f764be95.png)

## AUC Scoring

Closer look at the inner workings of how EBC trial is being evaluated (how AUC scoring can be applied to this particular bioinformatic problem).

![STEM Away - AUC-3](https://user-images.githubusercontent.com/44710581/130165695-f97b2edb-8c2e-458d-9459-1cc99443c621.png)
