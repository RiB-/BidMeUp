#****************************************************************************
# Importing packages
#******************************************************************************
from flask import Flask,render_template, request
app = Flask(__name__)

#------------------------------------
# Import user-defined modules
#------------------------------------
from a_Model import ModelIt
from MVP1 import MVP_ShowP, MVP_Result
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
# Applying Tutorial Routes
#******************************************************************************

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = 'Home', user = { 'nickname': 'Miguel' },
        )

@app.route('/db')
def cities_page():
    db = mdb.connect(user="root", host="localhost", passwd="Loki3.14159", db="world",  charset='utf8') 

    with db: 
        cur = db.cursor()
        cur.execute("SELECT Name FROM City LIMIT 15;")
        query_results = cur.fetchall()
    cities = ""
    for result in query_results:
        cities += result[0]
        cities += "<br>"
    return cities

@app.route("/db_fancy")
def cities_page_fancy():
    db = mdb.connect(user="root", host="localhost", passwd="Loki3.14159", db="world",  charset='utf8')
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")
        query_results = cur.fetchall()
    cities = []
    for result in query_results:
    	cities.append(dict(name=result[0], country=result[1], population=result[2]))
    return render_template('cities.html', cities=cities)


#******************************************************************************
# Applying input routes
#******************************************************************************

#------------------------------------
# Tutorial input routes
#------------------------------------
@app.route('/input')
def cities_input():
    return render_template("input.html")

#------------------------------------
# MVP1 input routes
#------------------------------------
@app.route('/MVP_input')
def MVP_input():
    return render_template("MVP_input.html")

#******************************************************************************
# Applying output routes
#******************************************************************************

#------------------------------------
# Tutorial output routes
#------------------------------------

# @app.route('/output')
# def cities_output():
#     return render_template("output.html")

@app.route('/output')
def cities_output():
  #pull 'ID' from input field and store it
  city = request.args.get('ID')
  db = mdb.connect(user="root", host="localhost", passwd="Loki3.14159", db="world",  charset='utf8')
  with db:
    cur = db.cursor()
    #just select the city from the world_innodb that the user inputs
    cur.execute("SELECT Name, CountryCode,  Population FROM City WHERE Name='%s';" % city)
    query_results = cur.fetchall()

  cities = []
  for result in query_results:
    cities.append(dict(name=result[0], country=result[1], population=result[2]))
  # the_result = ''
  # return render_template("output.html", cities = cities, the_result = the_result)
   #call a function from a_Model package. note we are only pulling one result in the query
  pop_input = cities[0]['population']
  the_result = ModelIt(city, pop_input)
  return render_template("output.html", cities = cities, the_result = the_result)

#------------------------------------
# MVP1 output routes
#------------------------------------

@app.route('/MVP_output_01')
def MVP_out_01():
    Product_Name, Brand, Category,Avg_Ret_Price,Min_Sale_Price = MVP_ShowP()
    return render_template("MVP_output_01.html", Product_Name = Product_Name, Brand = Brand, Category = Category, Avg_Ret_Price = Avg_Ret_Price, Min_Sale_Price = Min_Sale_Price)
#end

@app.route('/MVP_output_02')
def MVP_out_02():

    import pickle

    Offer = float(request.args.get('ID'))

    Input_Model_Path = 'model/'
    Input_Path_Man = 'model/'


    with open(Input_Path_Man + 'Savelist.p', 'rb') as f:
        Table_List = pickle.load(f)
    #end

    Proba_out = MVP_Result(User_Offer=Offer)

    return render_template("MVP_output_03.html", Product_Name = Table_List[0], Brand = Table_List[1], Category = Table_List[2], Avg_Ret_Price = Table_List[3], Min_Sale_Price = Table_List[4], User_offer = Offer, Proba_out = Proba_out)
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
# MVP3 Routes
#******************************************************************************

@app.route('/MVP3_input_01', methods=['GET','POST'])
def MVP3_input01():
  Category = 'Photography'
  Subcategory = 'Camera Flashes'
  Brand = 'Canon'
  Product_List = Prod_Info_Unique_DF['Products Name'][Prod_Info_Unique_DF['Brand']==Brand][Prod_Info_Unique_DF['Subcategory']==Subcategory][Prod_Info_Unique_DF['Product Category']==Category].unique().tolist()
  return render_template("MVP3_input_01.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Products = Product_List)
#end

@app.route('/MVP3_input_02', methods=['GET','POST'])
def MVP3_input02():
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

  return render_template("MVP3_input_02.html", Category = Category, Subcategory = Subcategory, Brand = Brand, Product = Product, Avg_Ret_Price = Avg_Ret_Price, Min_Sale_Price = Min_Sale_Price)
#end

@app.route('/MVP3_output', methods=['GET','POST'])
def MVP3_out():

  with open(Input_Path_Man + 'List.p', 'rb') as f:
      Table_List = pickle.load(f)
  #end

  Prod_ID = Table_List[0]  

  Gen_Pred_Prod = Full_CatFeat_SIM_01_DF[Full_CatFeat_SIM_01_DF.Prod_ID==Prod_ID]

  Offer = float(request.args.get('ID'))

  P_Acc, P_CO = MVP2.Predicting(Prediction_Object, Gen_Pred_Prod, Prod_ID, Offer)

  Acc_bar = "width: " + str(int(P_Acc*100)) + "%;"
  CO_bar = "width: " + str(int(P_CO*100)) + "%;"

  return render_template("MVP3_output.html", Category = Table_List[2], Subcategory = Table_List[3], 
                         Brand = Table_List[4], Product = Table_List[1], Avg_Ret_Price = Table_List[5],
                         Min_Sale_Price = Table_List[6], P_Acc = P_Acc, P_CO = P_CO, Acc_bar = Acc_bar,
                         CO_bar = CO_bar, Offer = Offer)
#end

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)


