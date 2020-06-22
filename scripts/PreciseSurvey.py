import streamlit as st
import random
import numpy as np
import pickle
import pandas as pd
# import xgboost as xgb
# import altair as alt
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go
st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.image('../images/Logo.png')


#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# def remote_css(url):
#     st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

# def icon(icon_name):
#     st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

# local_css("style.css")
# remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

# icon("search")
# selected = st.text_input("", "Search...")
# button_clicked = st.button("OK")
st.title("Hello!")
st.title("We DO care about your work place satisfaction and also your time!")
st.write("You are participating a survey, which is optimized with atrificial inteligence!")
st.selectbox('Please choose your company name',['...','Insight Data Science','Boston University','Facebook','Microsoft'])
# iq = random.sample(range(10),10)
# iq = range(10)
data_location = '../data/pickles/'
data_file = 'New_dataframe_Questions.pkl'
sheet1 = 'Question List w Categories'
dfq = pickle.load(open(data_location+data_file, 'rb'))
qcategories = dfq['Categories'].unique()
np.random.seed(2345)
directory_name='../data/pickles/'
pickle_name = 'Important_questions.pkl'
dfq1 = pickle.load(open(directory_name+pickle_name, 'rb'))
q = dfq['Text'][:10].values
# np.random.shuffle(q)

x = np.zeros([10,6])
# st.cache()






for i,qq in enumerate(q):
	resp = st.radio(
	qq,
	['N/A','Poor','Bad','Neutral', 'Good', 'Excellent'])
	if (resp == 'Poor'):
		x[i,1] = 1
	elif (resp == 'Bad'):
		x[i,2] = 1
	elif (resp == 'Neutral'):
		x[i,3] = 1
	elif (resp == 'Good'):
		x[i,4] = 1
	elif (resp == 'Excellent'):
		x[i,5] = 1
	else:
		x[i,0] = 1			
x=x.reshape(1,-1)
xu = np.zeros([10,6])
xu[:,5] = 1
xu = xu.T.reshape(1,-1)
result = np.zeros(10)
aa =0
if st.button('Submit'):
	# iq = random.sample(range(10),10)
	# q = q[iq]
	if aa==1:#(x==np.zeros([10*4]))|(x==xu):
		st.spinner("Please answer questions!")
	else:			
		pickle_name = 'ML_overall_score.pkl'
		loaded_model_overall = pickle.load(open(directory_name+pickle_name, 'rb'))
		a = loaded_model_overall.best_estimator_.feature_names
		# st.write(x)
		# st.write(a)
		dfx = pd.DataFrame(x,columns=a)
		result[0] = loaded_model_overall.best_estimator_.predict(dfx)

		for i,cat in enumerate(qcategories):
			pickle_name = 'ML_Category'+str(i)+'.pkl'
			# st.write(directory_name+pickle_name)
			loaded_model = pickle.load(open(directory_name+pickle_name, 'rb'))
			dummy_aQs = loaded_model.best_estimator_.feature_names
			dfx = pd.DataFrame(x,columns=dummy_aQs)
			result[i+1] = loaded_model.best_estimator_.predict(dfx)
		dfr = pd.DataFrame(data=np.round(result*100,1),index=np.insert(qcategories,0,'Overall')).reset_index()
		dfr.columns=['Categories','percentage']
		dfr1 = dfr[dfr['Categories']!='Overall'].sort_values(by='percentage')
		dfr1 = dfr1.append(dfr[dfr['Categories']=='Overall'])
		resultm = np.zeros(12)
		for i in range(12):
			print(i)
			pickle_name = 'ML_Rand_'+str(i)+'.pkl'
			loaded_model = pickle.load(open(directory_name+pickle_name, 'rb'))
			dummy_aQs_5 = loaded_model.best_estimator_.feature_names
			dfx = pd.DataFrame(x,columns=dummy_aQs)
			resultm[i] = loaded_model.best_estimator_.predict(dfx.loc[:,dummy_aQs_5])
		# resultm = 2*resultm
		# resultm = 2*(1-result)
		dfr2 = pd.DataFrame([['Inconsistency/Malingering',1/(1+np.exp(-(resultm.max()-resultm.min()-0.3)*20))*100]],columns=['Categories','percentage'])
		# dfr2 = pd.DataFrame([['Inconsistency/Malingering',(resultm.max()-resultm.min())*100]],columns=['Categories','percentage'])
		dfr1 = pd.concat([dfr2,dfr1])
		import plotly.express as px
		# st.write(x)
		zz = (dfr1['percentage']//10).astype(int).tolist()
		zz[0] = 10-zz[0]
		colorz = px.colors.diverging.RdYlGn
		colorz = np.array(colorz)[zz]
		colorz =[str(i) for i in colorz]

		fig = px.bar(x=dfr1['percentage'],y=dfr1['Categories'],orientation='h')
		fig = go.Figure(fig)

		fig.update_traces(marker_color=colorz)
		fig.update_layout(
			title=".                                Predicted Scores",
			xaxis_title="Score(%)",
			yaxis_title="Categories",
			font=dict(
				size=14,
				color="#7f7f7f"
			),
		xaxis_showgrid=True, yaxis_showgrid=True
		)
		fig.update_xaxes(range=[0, 100], row=1, col=1,nticks=11,tickangle=-45)
		annotationsList = [dict(
                x=xi+6,
                y=yi,
                text=str(xi)+'%',
                showarrow=False,
            ) for xi, yi in zip((dfr1['percentage']//1).astype(int),range(len(dfr1['Categories'])))]
		fig.update_layout(annotations=annotationsList)

		# fig.update_layout(
		# 	title="Malingering score = {:.0f}%".format((1-resultm.max()+resultm.min())*100))
		st.plotly_chart(fig)
		st.write('Thank you! Your responses are so valuable for us to increase your work place quality!')
		np.random.shuffle(q)

