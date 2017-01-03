#******************************************************************************
# Importing packages
#******************************************************************************
from flask import Flask, render_template, request
app = Flask(__name__)

#------------------------------------
# Import user-defined modules
#------------------------------------
import MVP2
import pandas as pd
import pickle
#******************************************************************************
Input_Path_Man = '../model/'
Input_Model_Path = '../model/'

Full_CatFeat_SIM_01_DF = pd.read_pickle(Input_Model_Path + 'Full_CatFeat_SIM_01_DF.pkl')
Prod_Info_Unique_DF = pd.read_csv(Input_Path_Man + 'Prod_Info_Unique_DF.csv')

with open(Input_Model_Path + 'LogReg_3Cat.pkl','r') as f:
    Prediction_Object = pickle.load(f)
#end

#******************************************************************************
# MVP2 Routes
#******************************************************************************

#------------------------------------
# MVP2 input routes
#------------------------------------
@app.route('/MVP2_input_01', methods=['GET','POST'])
def MVP_input01():
  Category_List = MVP2.GetCatList()
  return render_template("MVP2_input_01.html", Categories = Category_List)
#end

@app.route('/MVP2_input_02', methods=['GET','POST'])
def MVP_input02():
  Category = str(request.args.get('Category'))
  Subcategory_List = MVP2.GetSubcatList(Category)
  return render_template("MVP2_input_02.html", Category = Category, Subcategories = Subcategory_List)
#end

@app.route('/MVP2_input_03', methods=['GET','POST'])
def MVP_input03():
  Subcategory = str(request.args.get('Subcategory'))
  Category, Brand_List = MVP2.GetBrandList(Subcategory)
  return render_template("MVP2_input_03.html", Category = Category, Subcategory = Subcategory, Brands = Brand_List)
#end

@app.route('/MVP2_input_04', methods=['GET','POST'])
def MVP_input04():
  Brand = str(request.args.get('Brand'))
  Category, Subcategory, Product_List = MVP2.GetProdList(Brand)
  return render_template("MVP2_input_04.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Products = Product_List)
#end

@app.route('/MVP2_input_05', methods=['GET','POST'])
def MVP_input05():
  import pickle
  Product = str(request.args.get('Product'))
  Category, Subcategory, Brand, Prod_ID = MVP2.GetProdID(Product)
  Avg_Ret_Price, Min_Sale_Price = MVP2.GetPriceInfo(Prod_ID)

  List = [Prod_ID, Product, Category, Subcategory, Brand, Avg_Ret_Price, Min_Sale_Price]
  with open(Input_Path_Man + 'List.p', 'wb') as f:
      pickle.dump(List, f)
  #end

  return render_template("MVP2_input_05.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Product = Product, Avg_Ret_Price = Avg_Ret_Price, Min_Sale_Price = Min_Sale_Price)
#end

@app.route('/MVP2_output', methods=['GET','POST'])
def MVP2_out():
  import pickle
  import pandas as pd

  with open(Input_Path_Man + 'List.p', 'rb') as f:
      Table_List = pickle.load(f)
  #end

  Prod_ID = Table_List[0]  

  Gen_Pred_Prod = Full_CatFeat_SIM_01_DF[Full_CatFeat_SIM_01_DF.Prod_ID==Prod_ID]

  Offer = float(request.args.get('ID'))

  P_Acc, P_CO = MVP2.Predicting(Prediction_Object, Gen_Pred_Prod, Prod_ID, Offer)

  Acc_bar = "width: " + str(int(P_Acc*100)) + "%;"
  CO_bar = "width: " + str(int(P_CO*100)) + "%;"

  return render_template("MVP2_output.html", Category = Table_List[2], Subcategory = Table_List[3], 
                         Brand = Table_List[4], Product = Table_List[1], Avg_Ret_Price = Table_List[5],
                         Min_Sale_Price = Table_List[6], P_Acc = P_Acc, P_CO = P_CO, Acc_bar = Acc_bar,
                         CO_bar = CO_bar, Offer = Offer)
#end

#******************************************************************************
# App Routes
#******************************************************************************

@app.route('/', methods=['GET','POST'])
def App_input():
  Category = 'Photography'
  Subcategory = 'Camera Flashes'
  Brand = 'Canon'
  Product_List = Prod_Info_Unique_DF['Products Name'][Prod_Info_Unique_DF['Brand']==Brand][Prod_Info_Unique_DF['Subcategory']==Subcategory][Prod_Info_Unique_DF['Product Category']==Category].unique().tolist()
  return render_template("App_input.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Products = Product_List)
#end

@app.route('/Insert_Offer', methods=['GET','POST'])
def InsertOffer():
  import pickle

  Product = str(request.args.get('Product'))
  Category = 'Photography'
  Subcategory = 'Camera Flashes'
  Brand = 'Canon'
  Prod_ID = str(Prod_Info_Unique_DF['Prod_ID'][Prod_Info_Unique_DF['Products Name']==Product][Prod_Info_Unique_DF['Brand']==Brand][Prod_Info_Unique_DF['Subcategory']==Subcategory][Prod_Info_Unique_DF['Product Category']==Category].tolist()[0])
  
  Avg_Ret_Price = float("{0:.2f}".format(Full_CatFeat_SIM_01_DF['Avg_Ret_Price'][Full_CatFeat_SIM_01_DF['Prod_ID']==Prod_ID].values[0]))
  Min_Sale_Price = float("{0:.2f}".format(Full_CatFeat_SIM_01_DF['Min_Sale_Price'][Full_CatFeat_SIM_01_DF['Prod_ID']==Prod_ID].values[0]))

  List = [Prod_ID, Product, Category, Subcategory, Brand, Avg_Ret_Price, Min_Sale_Price]
  with open(Input_Path_Man + 'List.p', 'wb') as f:
      pickle.dump(List, f)
  #end

  Avg_Ret_Price = '%.2f' %Avg_Ret_Price
  Min_Sale_Price = '%.2f' %Min_Sale_Price

  return render_template("App_offer_input.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Product = Product, Avg_Ret_Price = Avg_Ret_Price, Min_Sale_Price = Min_Sale_Price)
#end

@app.route('/Output', methods=['GET','POST'])
def App_output():

  with open(Input_Path_Man + 'List.p', 'rb') as f:
      Table_List = pickle.load(f)
  #end

  Prod_ID = Table_List[0]  

  Gen_Pred_Prod = Full_CatFeat_SIM_01_DF[Full_CatFeat_SIM_01_DF.Prod_ID==Prod_ID]

  Offer = float(request.args.get('ID'))

  P_Acc, P_CO = MVP2.Predicting(Prediction_Object, Gen_Pred_Prod, Prod_ID, Offer)
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
# Running directly Views_01.py
#******************************************************************************

if __name__=="__main__":
  app.run(host='0.0.0.0',port=5000)
#end