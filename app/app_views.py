#******************************************************************************
# Importing packages
#******************************************************************************
from app import App
from flask import render_template, request

#------------------------------------
# Import user-defined modules
#------------------------------------
from scripts import bmu_model
import pandas as pd
import pickle
#******************************************************************************

#******************************************************************************
# Global Variables and Datasets
#******************************************************************************

files_path = './data/'

full_sim_df = pd.read_pickle(files_path + 'Full_CatFeat_SIM_01_DF.pkl')
prod_info_unique_df = pd.read_csv(files_path + 'Prod_Info_Unique_DF.csv')

with open(files_path + 'LogReg_3Cat.pkl','r') as f:
    predictor_object = pickle.load(f)
#end

#******************************************************************************
# Demo App Routes
#******************************************************************************

@App.route('/', methods=['GET','POST'])
@App.route('/index/', methods=['GET','POST'])
def app_input():
    Category = 'Photography'
    Subcategory = 'Camera Flashes'
    Brand = 'Canon'
    Product_List = prod_info_unique_df['Products Name'][prod_info_unique_df['Brand']==Brand]\
                                                       [prod_info_unique_df['Subcategory']==Subcategory]\
                                                       [prod_info_unique_df['Product Category']==Category].unique().tolist()
    return render_template("App_input.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Products = Product_List)
#end

@App.route('/Insert_Offer/', methods=['GET','POST'])
def insert_offer():
    import pickle
    Product = str(request.args.get('Product'))
    Category = 'Photography'
    Subcategory = 'Camera Flashes'
    Brand = 'Canon'
    Prod_ID = str(prod_info_unique_df['Prod_ID'][prod_info_unique_df['Products Name']==Product]\
                                              [prod_info_unique_df['Brand']==Brand]\
                                              [prod_info_unique_df['Subcategory']==Subcategory]\
                                              [prod_info_unique_df['Product Category']==Category].tolist()[0])

    Avg_Ret_Price = float("{0:.2f}".format(full_sim_df['Avg_Ret_Price'][full_sim_df['Prod_ID']==Prod_ID].values[0]))
    Min_Sale_Price = float("{0:.2f}".format(full_sim_df['Min_Sale_Price'][full_sim_df['Prod_ID']==Prod_ID].values[0]))

    List = [Prod_ID, Product, Category, Subcategory, Brand, Avg_Ret_Price, Min_Sale_Price]
    with open(files_path + 'List.p', 'wb') as f:
      pickle.dump(List, f)
    #end

    Avg_Ret_Price = '%.2f' %Avg_Ret_Price
    Min_Sale_Price = '%.2f' %Min_Sale_Price

    return render_template("App_offer_input.html", Category = Category, Subcategory = Subcategory, Brand = Brand, 
                         Product = Product, Avg_Ret_Price = Avg_Ret_Price, Min_Sale_Price = Min_Sale_Price)
#end

@App.route('/Output/', methods=['GET','POST'])
def app_output():

    with open(files_path + 'List.p', 'rb') as f:
      Table_List = pickle.load(f)
    #end

    Prod_ID = Table_List[0]  

    Gen_Pred_Prod = full_sim_df[full_sim_df.Prod_ID==Prod_ID]

    Offer = float(request.args.get('ID'))

    P_Acc, P_CO = bmu_model.Predicting(predictor_object, Gen_Pred_Prod, Prod_ID, Offer)
    P_Exp = 1 - P_Acc - P_CO

    Acc_bar = "width: " + str(int(P_Acc*100)) + "%;"
    CO_bar = "width: " + str(int(P_CO*100)) + "%;"
    Exp_bar = "width: " + str(int(P_Exp*100)) + "%;"

    P_Acc = '%.2f' %P_Acc
    P_CO = '%.2f' %P_CO
    P_Exp = '%.2f' %P_Exp
    Offer = '%.2f' %Offer

    Table_List[5] = '%.2f' %Table_List[5]
    Table_List[6] = '%.2f' %Table_List[6]

    return render_template("App_output.html", Category = Table_List[2], Subcategory = Table_List[3], 
                           Brand = Table_List[4], Product = Table_List[1], Avg_Ret_Price = Table_List[5],
                           Min_Sale_Price = Table_List[6], P_Acc = P_Acc, P_CO = P_CO, P_Exp = P_Exp, Acc_bar = Acc_bar,
                           CO_bar = CO_bar, Exp_bar = Exp_bar, Offer = Offer)
#end

#******************************************************************************
# Additional Routes
#******************************************************************************

@App.route('/MVP2_input_01', methods=['GET','POST'])
def MVP_input01():
    Category_List = bmu_model.GetCatList()
    return render_template("MVP2_input_01.html", Categories = Category_List)
#end

@App.route('/MVP2_input_02', methods=['GET','POST'])
def MVP_input02():
    Category = str(request.args.get('Category'))
    Subcategory_List = bmu_model.GetSubcatList(Category)
    return render_template("MVP2_input_02.html", Category = Category, Subcategories = Subcategory_List)
#end

@App.route('/MVP2_input_03', methods=['GET','POST'])
def MVP_input03():
    Subcategory = str(request.args.get('Subcategory'))
    Category, Brand_List = bmu_model.GetBrandList(Subcategory)
    return render_template("MVP2_input_03.html", Category = Category, Subcategory = Subcategory, 
                           Brands = Brand_List)
#end

@App.route('/MVP2_input_04', methods=['GET','POST'])
def MVP_input04():
    Brand = str(request.args.get('Brand'))
    Category, Subcategory, Product_List = bmu_model.GetProdList(Brand)
    return render_template("MVP2_input_04.html", Category = Category, Subcategory = Subcategory, 
                           Brand = Brand, Products = Product_List)
#end

@App.route('/MVP2_input_05', methods=['GET','POST'])
def MVP_input05():
    Product = str(request.args.get('Product'))
    Category, Subcategory, Brand, Prod_ID = bmu_model.GetProdID(Product)
    Avg_Ret_Price, Min_Sale_Price = bmu_model.GetPriceInfo(Prod_ID)

    List = [Prod_ID, Product, Category, Subcategory, Brand, Avg_Ret_Price, Min_Sale_Price]
    with open(files_path + 'List.p', 'wb') as f:
      pickle.dump(List, f)
    #end

    return render_template("MVP2_input_05.html", Category = Category, Subcategory = Subcategory, 
                           Brand = Brand, Product = Product, Avg_Ret_Price = Avg_Ret_Price, 
                           Min_Sale_Price = Min_Sale_Price)
#end

@App.route('/MVP2_output', methods=['GET','POST'])
def MVP2_out():

    with open(files_path + 'List.p', 'rb') as f:
      Table_List = pickle.load(f)
    #end

    Prod_ID = Table_List[0]  

    Gen_Pred_Prod = full_sim_df[full_sim_df.Prod_ID==Prod_ID]

    Offer = float(request.args.get('ID'))

    P_Acc, P_CO = bmu_model.Predicting(predictor_object, Gen_Pred_Prod, Prod_ID, Offer)
    P_Exp = 1 - P_Acc - P_CO

    Acc_bar = "width: " + str(int(P_Acc*100)) + "%;"
    CO_bar = "width: " + str(int(P_CO*100)) + "%;"
    Exp_bar = "width: " + str(int(P_Exp*100)) + "%;"

    P_Acc = '%.2f' %P_Acc
    P_CO = '%.2f' %P_CO
    P_Exp = '%.2f' %P_Exp
    Offer = '%.2f' %Offer

    Table_List[5] = '%.2f' %Table_List[5]
    Table_List[6] = '%.2f' %Table_List[6]

    return render_template("App_output.html", Category = Table_List[2], Subcategory = Table_List[3], 
                           Brand = Table_List[4], Product = Table_List[1], Avg_Ret_Price = Table_List[5],
                           Min_Sale_Price = Table_List[6], P_Acc = P_Acc, P_CO = P_CO, P_Exp = P_Exp, Acc_bar = Acc_bar,
                           CO_bar = CO_bar, Exp_bar = Exp_bar, Offer = Offer)
#end

#******************************************************************************
# Running directly app_views.py
#******************************************************************************

if __name__=="__main__":
    App.run(host='0.0.0.0',port=5000)
#end
