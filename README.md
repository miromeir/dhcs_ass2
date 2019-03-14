Assignment 2 for Digital Humanities

1.Running the Assignment:
===
For demonstration purposes, the file about [Meir Ariel(מאיר אריאל)](https://en.wikipedia.org/wiki/Meir_Ariel) was chosen.
- I ran Menni Adlers tagger on the file ```untagged_lexicon/156_אריאל_מאיר.txt```. Result is at ```tagged_tagger/meir_ariel.txt```
- Tagged [TEI](https://tei-c.org/) File lcoated at: ```tagged_class/meir_ariel.xml```
- Run the comparison script: 
```
python3 compare_ner_tags.py tagged_tagger/meir_ariel.txt tagged_class/meir_ariel.xml
```
Results will be:

```
I_PERS,אריאל,accurate
I_PERS,מאיר,accurate
I_LOC,פתח,accurate
...
...
...
*****************************************
*************** TOTAL *******************
 - Accurate:69
 - False Positive:36
 - False Negative:21
```
### 1.2.Improving Results:
---
The script searches every token found in tagger output file, in [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page).
For each token 
Then determines if it's a person, or a location, and modify that line with apropriate tag.

Make a copy of the file ```tagged_tagger/meir_ariel.txt```, call it "improve_me.txt"
- Run:
``` python3 improve_results.py improve_me.txt```

- Now compare with TEI file:
```
python3 compare_ner_tags.py improve_me.txt tagged_class/meir_ariel.xml
```
Results will be:
```
I_LOC,Name,false_positive
I_PERS,אריאל,accurate
I_PERS,מאיר,accurate
...
...
...
*****************************************
*************** TOTAL *******************
 - Accurate:76
 - False Positive:246
 - False Negative:14
```
**We can tell there's an increase in 'Accurate', less 'False Negative'**
