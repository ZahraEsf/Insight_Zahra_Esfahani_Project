**PROBLEM STATEMENT**<br>
It is a known fact that the longer the survey is the less engaged the participants are, which leads to a higher drop out rate. Hence optimizing a survey length can not only increase its response rate but also enhances its performance. For example, in our survey to measure employee satisfaction, I could bring down the length of the survey to 1/6th of its original length, without any significant loss of performance. My target audience is every company that is interested in measuring its employee satisfaction and investigating the root causes of its pain points.

**SOLUTION**<br>
I developed an ML-based survey optimizer based on XGboost and Random Forest to develop a shortened survey, where I not only score overall employee satisfaction but also his/her satisfaction in different work domains (such as Management and Salary). I also developed a solution to report the inconsistency score of each participant in his/her responses to the questions. As a deliverable, I have created a web-app dashboard, where each participant can answer the shortened survey and receive the abovementioned suite of scores on the fly.

**PRESENTATION LINK**<br>
https://drive.google.com/file/d/1TV5y_lxyL69PZ5bzVgcsISIvXSfMYSEb/view

**LIVE DEMO**<br>
http://deepneuro.tech:8501/


To run this project you need to at first install the requirements via requirements.txt and then use the Survey_Optimizer notebook in notebooks folder. and to test the model in the streamlit dashboar you need to run the Precise_Survey script in streamlit.
