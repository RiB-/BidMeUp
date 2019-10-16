
"""
  **************************************
  Created by Romano Foti - rfoti
  On Thu, Sept 24th, 2015
  **************************************
"""
#******************************************************************************
# Importing packages
#******************************************************************************
#-----------------------------
# Standard libraries
#-----------------------------
import pandas as pd
import pickle
#******************************************************************************

#******************************************************************************
# Global Variables and Datasets
#******************************************************************************
files_path = './data/'

#******************************************************************************


def MVP_ShowP():

    GT_Feat_LR_SIM_DF = pd.read_pickle(files_path + 'GT_Feat_LR_SIM_DF.pkl')
    Prod_Info_DF = pd.read_pickle(files_path + 'Prod_Info_DF.pkl')

    Gen_Pred_Prod = GT_Feat_LR_SIM_DF.sample(n=1)

    Gen_Pred_Prod.to_pickle(files_path + 'Gen_Pred_Prod.pkl')

    Gen_Pred_Prod = Gen_Pred_Prod.drop(['Offer_Status'], axis=1)
    Category_Mapping = pickle.load(open(files_path + 'Category_Mapping.p', "rb"))
    Inv_Category_Mapping = {v: k for k, v in Category_Mapping.items()}
    Show_DF = Gen_Pred_Prod.copy()
    Show_DF['Product_Category'] = Show_DF['Product_Category'].replace(Inv_Category_Mapping)

    Product_Name = Prod_Info_DF['Products Name'].values[0]
    Brand = Prod_Info_DF['Brand'].values[0]
    Category = Show_DF['Product_Category'].values[0]
    Avg_Ret_Price = float("{0:.2f}".format(Show_DF['Avg_Ret_Price'].values[0]))
    Min_Sale_Price = float("{0:.2f}".format(Show_DF['Min_Sale_Price'].values[0]))

    Savelist = [Product_Name, Brand, Category, Avg_Ret_Price, Min_Sale_Price]

    with open(files_path + 'Savelist.p', 'wb') as f:
        pickle.dump(Savelist, f)
    #end

    return Product_Name, Brand, Category, Avg_Ret_Price, Min_Sale_Price
#end


def MVP_Result(User_Offer=0):

    with open(files_path + 'LogReg_obj.pkl', 'r') as f:
        LogReg_obj = pickle.load(f)
    #end

    Model_ID = 'Ratio'

    #******************************************************************************
    # Predicting
    #******************************************************************************
    Gen_Pred_Prod = pd.read_pickle(files_path + 'Gen_Pred_Prod.pkl')
    Gen_Pred_Prod = Gen_Pred_Prod.drop(['Offer_Status'], axis=1)

    if Model_ID == 'Simple':
        Gen_Pred_Prod['Offer_Price'] = User_Offer
    #end
    if Model_ID == 'Ratio':
        Gen_Pred_Prod['Offer_Price'] = 1.0 * User_Offer / Gen_Pred_Prod['Avg_Ret_Price']
    #end

    Pred_Array_Imp = Gen_Pred_Prod.values
    Pred_Probability = LogReg_obj.predict_proba(Pred_Array_Imp)

    Proba_out = float("{0:.2f}".format(Pred_Probability[0, 1]))

    return Proba_out

#end


def GetCatList():

    Prod_Info_Unique_DF = pd.read_pickle(files_path + 'Prod_Info_Unique_DF.pkl')
    Category_List = Prod_Info_Unique_DF['Product Category'].unique().tolist()
    return Category_List

#end


def GetSubcatList(Category):

    Prod_Info_Unique_DF = pd.read_pickle(files_path + 'Prod_Info_Unique_DF.pkl')

    with open(files_path + 'Category.p', 'wb') as f:
        pickle.dump(Category, f)
    #end

    Subcategory_List = Prod_Info_Unique_DF['Subcategory'][Prod_Info_Unique_DF['Product Category'] == Category].unique().tolist()  # noqa
    return Subcategory_List

#end


def GetBrandList(Subcategory):

    Prod_Info_Unique_DF = pd.read_pickle(files_path + 'Prod_Info_Unique_DF.pkl')

    with open(files_path + 'Category.p', 'r') as f:
        Category = str(pickle.load(f))
    #end

    with open(files_path + 'Subcategory.p', 'wb') as f:
        pickle.dump(Subcategory, f)
    #end

    Brand_List = Prod_Info_Unique_DF['Brand'][Prod_Info_Unique_DF['Subcategory'] == Subcategory][Prod_Info_Unique_DF['Product Category'] == Category].unique().tolist()  # noqa
    return Category, Brand_List

#end


def GetProdList(Brand):

    Prod_Info_Unique_DF = pd.read_pickle(files_path + 'Prod_Info_Unique_DF.pkl')

    with open(files_path + 'Category.p', 'r') as f:
        Category = str(pickle.load(f))
    #end
    with open(files_path + 'Subcategory.p', 'r') as f:
        Subcategory = str(pickle.load(f))
    #end

    with open(files_path + 'Brand.p', 'wb') as f:
        pickle.dump(Brand, f)
    #end

    Prod_List = Prod_Info_Unique_DF['Products Name'][Prod_Info_Unique_DF['Brand'] == Brand][Prod_Info_Unique_DF['Subcategory'] == Subcategory][Prod_Info_Unique_DF['Product Category'] == Category].unique().tolist()  # noqa
    return Category, Subcategory, Prod_List

#end


def GetProdID(Product):

    Prod_Info_Unique_DF = pd.read_pickle(files_path + 'Prod_Info_Unique_DF.pkl')

    with open(files_path + 'Category.p', 'r') as f:
        Category = str(pickle.load(f))
    #end
    with open(files_path + 'Subcategory.p', 'r') as f:
        Subcategory = str(pickle.load(f))
    #end
    with open(files_path + 'Brand.p', 'r') as f:
        Brand = str(pickle.load(f))
    #end

    Prod_ID = str(Prod_Info_Unique_DF['Prod_ID'][Prod_Info_Unique_DF['Products Name'] == Product][Prod_Info_Unique_DF['Brand'] == Brand][Prod_Info_Unique_DF['Subcategory'] == Subcategory][Prod_Info_Unique_DF['Product Category'] == Category].tolist()[0])  # noqa

    return Category, Subcategory, Brand, Prod_ID

#end


def GetPriceInfo(Prod_ID):

    Full_CatFeat_SIM_01_DF = pd.read_pickle(files_path + 'Full_CatFeat_SIM_01_DF.pkl')

    Avg_Ret_Price = float("{0:.2f}".format(Full_CatFeat_SIM_01_DF['Avg_Ret_Price'][Full_CatFeat_SIM_01_DF['Prod_ID'] == Prod_ID].values[0]))  # noqa
    Min_Sale_Price = float("{0:.2f}".format(Full_CatFeat_SIM_01_DF['Min_Sale_Price'][Full_CatFeat_SIM_01_DF['Prod_ID'] == Prod_ID].values[0]))  # noqa

    return Avg_Ret_Price, Min_Sale_Price

#end


def Predicting(Pred_Obj, Feat_DF, Prod_ID, User_Offer, Drop_Feat='None', Model_ID='Ratio'):

    if Drop_Feat == 'None':
        Drop_Feat = ['Prod_ID', 'Offer_Status']
    #end

    Feat_DF = Feat_DF.drop(Drop_Feat, axis=1)

    if Model_ID == 'Simple':
        Feat_DF['Offer_Price'] = User_Offer
    #end
    if Model_ID == 'Ratio':
        Feat_DF['Offer_Price'] = 1.0 * User_Offer / Feat_DF['Min_Sale_Price']
    #end

    if User_Offer >= Feat_DF['Avg_Ret_Price'].values[0]:
        Pred_Probability = [[0.01, 0.98, 0.01]]
    else:
        Pred_Array_Imp = Feat_DF.values
        Pred_Probability = Pred_Obj.predict_proba(Pred_Array_Imp)
        #end

    #end

    return float("{0:.2f}".format(Pred_Probability[0][1])), float("{0:.2f}".format(Pred_Probability[0][2]))  # noqa

#end
