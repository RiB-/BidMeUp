#******************************************************************************
# Importing packages
#******************************************************************************
from app import BidMeApp
from flask import render_template, request

#------------------------------------
# Import user-defined modules
#------------------------------------
import bmu_model
import pandas as pd
import pickle
import base64
#******************************************************************************

#******************************************************************************
# Global Variables and Datasets
#******************************************************************************

files_path = './data/'

full_sim_df = pd.read_pickle(files_path + 'Full_CatFeat_SIM_01_DF.pkl')
prod_info_unique_df = pd.read_csv(files_path + 'Prod_Info_Unique_DF.csv')

with open(files_path + 'LogReg_3Cat.pkl', 'r') as f:
    predictor_object = pickle.load(f)
#end


#******************************************************************************
# App Home
#******************************************************************************
@BidMeApp.route('/home/', methods=['GET', 'POST'])
@BidMeApp.route('/', methods=['GET', 'POST'])
@BidMeApp.route('/index/', methods=['GET', 'POST'])
def app_home():
    return render_template("./home.html")
#end


#******************************************************************************
# Demo App Routes
#******************************************************************************
@BidMeApp.route('/demo_bidmeapp/', methods=['GET', 'POST'])
def app_input():
    Category = 'Photography'
    Subcategory = 'Camera Flashes'
    Brand = 'Canon'
    Product_List = prod_info_unique_df['Products Name'][prod_info_unique_df['Brand']==Brand]\
                                                       [prod_info_unique_df['Subcategory']==Subcategory]\
                                                       [prod_info_unique_df['Product Category']==Category].unique().tolist()
    return render_template("./demo_input_product.html", Category=Category, Subcategory=Subcategory,
                           Brand=Brand, Products=Product_List)
#end


@BidMeApp.route('/demo_input_offer/', methods=['GET', 'POST'])
def demo_input_offer():
    import pickle
    Product = str(request.args.get('Product'))
    Category = 'Photography'
    Subcategory = 'Camera Flashes'
    Brand = 'Canon'
    Prod_ID = str(prod_info_unique_df['Prod_ID'][prod_info_unique_df['Products Name']==Product]\
                                              [prod_info_unique_df['Brand']==Brand]\
                                              [prod_info_unique_df['Subcategory']==Subcategory]\
                                              [prod_info_unique_df['Product Category']==Category].tolist()[0])

    Avg_Ret_Price = float("{0:.2f}".format(full_sim_df['Avg_Ret_Price'][full_sim_df['Prod_ID'] == Prod_ID].values[0]))
    Min_Sale_Price = float("{0:.2f}".format(full_sim_df['Min_Sale_Price'][full_sim_df['Prod_ID'] == Prod_ID].values[0]))

    List = [Prod_ID, Product, Category, Subcategory, Brand, Avg_Ret_Price, Min_Sale_Price]
    with open(files_path + 'List.p', 'wb') as f:
        pickle.dump(List, f)
    #end

    Avg_Ret_Price = '%.2f' %Avg_Ret_Price
    Min_Sale_Price = '%.2f' %Min_Sale_Price

    return render_template("./demo_input_offer.html", Category=Category, Subcategory=Subcategory,
                           Brand=Brand, Product=Product, Avg_Ret_Price=Avg_Ret_Price,
                           Min_Sale_Price=Min_Sale_Price)
#end


@BidMeApp.route('/demo_output/', methods=['GET', 'POST'])
def app_output():

    with open(files_path + 'List.p', 'rb') as f:
        Table_List = pickle.load(f)
    #end

    Prod_ID = Table_List[0]

    Gen_Pred_Prod = full_sim_df[full_sim_df.Prod_ID == Prod_ID]

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

    return render_template("./demo_output.html", Category=Table_List[2], Subcategory=Table_List[3],
                           Brand=Table_List[4], Product=Table_List[1], Avg_Ret_Price=Table_List[5],
                           Min_Sale_Price=Table_List[6], P_Acc=P_Acc, P_CO=P_CO, P_Exp=P_Exp,
                           Acc_bar=Acc_bar, CO_bar=CO_bar, Exp_bar=Exp_bar, Offer=Offer)
#end


#******************************************************************************
# Additional Routes
#******************************************************************************
@BidMeApp.route('/full_login/', methods=['GET', 'POST'])
def full_login():
    return render_template("./full_login.html")
#end


@BidMeApp.route('/full_login_error/', methods=['GET', 'POST'])
def full_login_error():
    return render_template("./full_login_error.html",
                           login_error="Password incorrect: retry or use the demo version.")
#end


@BidMeApp.route('/full_logged_bidmeapp/', methods=['GET', 'POST'])
def full_logged_bidmeapp():
    passw = str(request.args.get('passw'))
    check_pssw = (passw == base64.b64decode('QmlkTWVBcHBGdWxsQWNjZXNz'))
    if check_pssw:
        Category_List = bmu_model.GetCatList()
        return render_template("./full_input_category.html", Categories=Category_List)
    else:
        return render_template("./full_login_error.html")
    #end


@BidMeApp.route('/full_bidmeapp/', methods=['GET', 'POST'])
def full_input_category():
    Category_List = bmu_model.GetCatList()
    return render_template("./full_input_category.html", Categories=Category_List)
#end


@BidMeApp.route('/full_input_subcategory/', methods=['GET', 'POST'])
def full_input_subcategory():
    Category = str(request.args.get('Category'))
    Subcategory_List = bmu_model.GetSubcatList(Category)
    return render_template("./full_input_subcategory.html", Category=Category, Subcategories=Subcategory_List)
#end


@BidMeApp.route('/full_input_brand/', methods=['GET', 'POST'])
def full_input_brand():
    Subcategory = str(request.args.get('Subcategory'))
    Category, Brand_List = bmu_model.GetBrandList(Subcategory)
    return render_template("./full_input_brand.html", Category=Category, Subcategory=Subcategory,
                           Brands=Brand_List)
#end


@BidMeApp.route('/full_input_product/', methods=['GET', 'POST'])
def full_input_product():
    Brand = str(request.args.get('Brand'))
    Category, Subcategory, Product_List = bmu_model.GetProdList(Brand)
    return render_template("./full_input_product.html", Category=Category, Subcategory=Subcategory,
                           Brand=Brand, Products=Product_List)
#end


@BidMeApp.route('/full_input_offer/', methods=['GET', 'POST'])
def full_input_offer():
    Product = str(request.args.get('Product'))
    Category, Subcategory, Brand, Prod_ID = bmu_model.GetProdID(Product)
    Avg_Ret_Price, Min_Sale_Price = bmu_model.GetPriceInfo(Prod_ID)

    List = [Prod_ID, Product, Category, Subcategory, Brand, Avg_Ret_Price, Min_Sale_Price]
    with open(files_path + 'List.p', 'wb') as f:
        pickle.dump(List, f)
    #end

    return render_template("./full_input_offer.html", Category=Category, Subcategory=Subcategory,
                           Brand=Brand, Product=Product, Avg_Ret_Price=Avg_Ret_Price,
                           Min_Sale_Price=Min_Sale_Price)
#end


@BidMeApp.route('/full_output/', methods=['GET', 'POST'])
def full_output():

    with open(files_path + 'List.p', 'rb') as f:
        Table_List = pickle.load(f)
    #end

    Prod_ID = Table_List[0]

    Gen_Pred_Prod = full_sim_df[full_sim_df.Prod_ID == Prod_ID]

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

    return render_template("./full_output.html", Category=Table_List[2], Subcategory=Table_List[3],
                           Brand=Table_List[4], Product=Table_List[1], Avg_Ret_Price=Table_List[5],
                           Min_Sale_Price=Table_List[6], P_Acc=P_Acc, P_CO=P_CO, P_Exp=P_Exp,
                           Acc_bar=Acc_bar, CO_bar=CO_bar, Exp_bar=Exp_bar, Offer=Offer)
#end


#******************************************************************************
# Running directly app_views.py
#******************************************************************************

if __name__=="__main__":
    BidMeApp.run(host='0.0.0.0',port=5000)
#end
