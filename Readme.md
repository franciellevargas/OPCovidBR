![SSC-logo-300x171](https://user-images.githubusercontent.com/19657817/63529693-77e6b100-c4db-11e9-9385-7d9b109427a2.png) 

# OPCovid-BR : Aspect-Based Sentiment Analysis on Covid-19 Twitter Data in Brazilian Portuguese

<p align="justify"> The OPCovid-Br is the first dataset of twitter data annotated with fine-grained opinions and sentiment polarity in Brazilian Portuguese. We extracted 1.800 twitters during the COVID-19 pandemic and annotated the fine-grained opinions for each twitter, as well as the binary document polarity (positive or negative). </p>


<div align="center">
<table> 
  <tr><th>Polarity Classification</th><th>Fine-grained opinion groups</th></tr>
<tr><td>

|class|label|total|
|--|--|--|  
|positive|1|900| 
|negative|0|900| 

</td><td>

|class|label|total|
|--|--|--|
||||
||||
||||
||||
  
</td><td>

</td></tr></table>

<p align="justify"> We also provide machine learning-based classifiers for fine-grained opinion and polarity classification tasks using OPcovid-BR dataset. For polarity classification, we tested a cross-domain strategy in order to measure the performance of the classifiers among different domains. For fine-grained opinion identification, we created a taxonomy of aspects and employed them in conjunction with machine learning methods. Based on the obtained results, we found that the cross-domain method improved the results for polarity classification task. However, the use of a domain taxonomy presented competitive results for fine-grained opinion identification in Portuguese Language. </p>

Link for the paper: https://link.springer.com/chapter/10.1007/978-3-030-61377-8_35

CITING

<p align="justify"> Vargas, F.A.,Santos, R.S.S. and Rocha, P.R. (2020). Identifying fine-grained opinion and classifying polarity of twitter data on coronavirus pandemic. Proceedings of the 9th Brazilian Conference on Intelligent Systems (BRACIS 2020), Rio Grande, RS, Brazil. </p>


BIBTEX

@inproceedings{VargasEtAll2020,
  author    = {Francielle Alves Vargas and
               Rodolfo Sanches Saraiva Dos Santos and
               Pedro Regattieri Rocha},
  title     = {Identifying fine-grained opinion and classifying polarity of twitter data on coronavirus pandemic},
  booktitle = {Proceedings of the 9th Brazilian Conference on Intelligent Systems (BRACIS 2020)},
  pages     = {01-10},
  year      = {2020},
  address   = {Rio Grande, RS, Brazil},
  crossref  = {http://bracis2020.c3.furg.br/acceptedPapers.html},
}



