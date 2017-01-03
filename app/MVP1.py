def ModelIt(fromUser  = 'Default', population = 0):
  print 'The population is %i' % population
  result = population/1000000.0
  if fromUser != 'Default':
    return result
  else:
    return 'check your input'


def MVP_ShowP(fromUser  = 'Default'):

	#%%******************************************************************************
	# Importing packages
	#******************************************************************************
	import pandas as pd  #library for advanced data analysis
	import pickle
	#******************************************************************************

	Input_Model_Path = '/media/romano/Data/Data Science/Insight 2015/Insight Project/ML_Results/'
	Input_Path_Man = '/media/romano/Data/Data Science/Insight 2015/Insight Project/Manipulated Data/'
	GT_Feat_LR_SIM_DF = pd.read_pickle(Input_Model_Path + 'GT_Feat_LR_SIM_DF.pkl')	
	Prod_Info_DF = pd.read_pickle(Input_Path_Man + 'Prod_Info_DF.pkl')

	Gen_Pred_Prod = GT_Feat_LR_SIM_DF.sample(n=1)

	Gen_Pred_Prod.to_pickle(Input_Model_Path + 'Gen_Pred_Prod.pkl')

	Gen_Pred_Prod = Gen_Pred_Prod.drop(['Offer_Status'], axis=1)
	Category_Mapping = pickle.load(open(Input_Path_Man + 'Category_Mapping.p', "rb" ) )
	Inv_Category_Mapping = {v: k for k, v in Category_Mapping.items()}
	Show_DF = Gen_Pred_Prod.copy()
	Show_DF['Product_Category'] = Show_DF['Product_Category'].replace(Inv_Category_Mapping)

	Product_Name = Prod_Info_DF['Products Name'].values[0]
	Brand = Prod_Info_DF['Brand'].values[0]
	Category = Show_DF['Product_Category'].values[0]
	Avg_Ret_Price = float("{0:.2f}".format(Show_DF['Avg_Ret_Price'].values[0]))
	Min_Sale_Price = float("{0:.2f}".format(Show_DF['Min_Sale_Price'].values[0]))

	Savelist = [Product_Name, Brand, Category, Avg_Ret_Price, Min_Sale_Price]

	with open(Input_Path_Man + 'Savelist.p', 'wb') as f:
	    pickle.dump(Savelist, f)
	#end

	return Product_Name, Brand, Category, Avg_Ret_Price, Min_Sale_Price
#end

def MVP_Result(fromUser  = 'Default', User_Offer = 0):

	#%%******************************************************************************
	# Importing packages
	#******************************************************************************
	import pandas as pd  #library for advanced data analysis
	import pickle
	#******************************************************************************
	Input_Model_Path = '/media/romano/Data/Data Science/Insight 2015/Insight Project/ML_Results/'
	Input_Path_Man = '/media/romano/Data/Data Science/Insight 2015/Insight Project/Manipulated Data/'

	with open(Input_Model_Path + 'LogReg_obj.pkl','r') as f:
	    LogReg_obj = pickle.load(f)
	#end

	GT_Feat_LR_SIM_DF = pd.read_pickle(Input_Model_Path + 'GT_Feat_LR_SIM_DF.pkl')

	Model_ID = 'Ratio'

	#******************************************************************************
	# Predicting
	#******************************************************************************
	Gen_Pred_Prod =pd.read_pickle(Input_Model_Path + 'Gen_Pred_Prod.pkl')
	Gen_Pred_Prod = Gen_Pred_Prod.drop(['Offer_Status'], axis=1)
	Category_Mapping = pickle.load(open(Input_Path_Man + 'Category_Mapping.p', "rb" ) )
	Inv_Category_Mapping = {v: k for k, v in Category_Mapping.items()}

	if Model_ID=='Simple':
	    Gen_Pred_Prod['Offer_Price'] = User_Offer
	#end
	if Model_ID=='Ratio':
	    Gen_Pred_Prod['Offer_Price'] = 1.0*User_Offer/Gen_Pred_Prod['Avg_Ret_Price']
	#end

	Pred_Array_Imp = Gen_Pred_Prod.values

	Predictions = LogReg_obj.predict(Pred_Array_Imp).astype(int) #make predictions from trained algoritm using the test data
	Pred_Probability = LogReg_obj.predict_proba(Pred_Array_Imp)

	Proba_out = float("{0:.2f}".format(Pred_Probability[0,1]))

	return Proba_out

	# if fromUser != 'Default':
	# 	return Proba_out
	# else:
	# 	return 'Check your Input'
	#end
#end

