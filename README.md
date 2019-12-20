# Better Name More Money: Airbnb Analysis

**Project ID:** 201912-16

**Team Members:** 
- Zihe Wang (zw2624@columbia.edu)
- Qianhui Yu (qy2226@columbia.edu)
- Duanyue Yun (dy2400@columbia.edu)

## Overview:

Our project explores the importance of listing name and builds a web application providing visualization tools and prediction tools both for Airbnb hosts and guests. For visualization tools, we provide important words recommendation, market information delivery such as price heat map. For prediction tools, hosts can get estimated popularity of their listings by inputting their listing name and other listing information. We tried with two modeling methods (Random Forest and XGBoost) to predict popularity and compare them to a baseline model. We find that listing names indeed help predict popularity and rank high in terms of variable importance. 


## Repo Structure:
- `airbnb_scrape` contains the Web Crawler App we developed.
- `airbnb_analysis` contains the Django App we developed.
- `exploratory analysis` contains code for exploratory analysis.
- `modeling` contains code for predictive model experiement.

## How to use locally:

1. `pip install -r requirements.txt` to install required packages.

2. For scrapy, run `scrapy crawl airbnb -a min='410' city='New York'` to get the data of your selected city and minimal price.

3. For website, run `python manage.py runserver` to access it on localhost. 

## URL:
hw0-252420.appspot.com

## Individual Contribution
The code developed by Qianhui and Duanyue are marked with UIN. The codes are developed by Zihe otherwise. 

## Reference

[1] R. Martinez, A. Carrington, T. Kuo, L. Tarhuni, and N. Abdel-Motaal. The impact of an airbnb host’s list-ing  description ‘sentiment’ and length on occupancy rates.https://arxiv.org/pdf/1711.09196.pdf

[2] J. Pennington, R. Socher, and C. Manning. Glove: Globalvectors for word representation, 2014

[3] https://towardsdatascience.com/creating-word-clouds-with-python-f2077c8de5cc

[4] https://github.com/kailu3/airbnb-scraper





