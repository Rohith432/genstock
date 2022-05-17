from flask import Flask, render_template, request,redirect,url_for,session
import cx_Oracle
import random
from datetime import datetime



app=Flask(__name__)
conn=cx_Oracle.connect('rohith/rohith11@//DESKTOP-8ITTR0U:1521/xe') #change username and password of database and your system name#
print(conn.version)
con=conn.cursor()
app.secret_key="hajury&bc*%bnceu"

def tre():
    a = random.randint(0000000000, 9999999999)
    return a
###############################################################################################
########supplier set###########
@app.route('/slogin',methods=['GET','POST'])
def slogin():
    log_check()
    return render_template('slogin.html')
@app.route('/slogcheck',methods=['GET','POST'])
def log_check():
    msg="not found"
    suser = request.form.get('s_user')
    spassword = request.form.get('s_password')
    con.execute('''select password from loginp where type='S' and USER_ID=:suser''' ,[suser])
    print(suser,spassword)
    data=con.fetchone()
    print(data)
    if (data==None):
        pass
    else:
        if (spassword==data[0]):
            session["supplier"] = suser
            return redirect('/supplier')
        else:
            return render_template('slogin.html',msg=msg)
####################
'''@app.route('/logg',methods=['GET','POST'])
def logg():
    msg="not found"
    cuser=request.form.get('s_user')
    cpassword=request.form.get('s_password')
    print(cuser, cpassword)
    con.execute(''' '''select password from loginp where user_id=:cuser''' ''',[cuser])
    print(cuser,cpassword)
    data=con.fetchone()
    print(data)
    if (cpassword==data[0]):

        print(cpassword)
        return supplier()
        #return render_template('lazyrecipe.html')
    else:
        print(cuser)
        return render_template('slogin.html',msg=msg)'''

#################
@app.route('/logout')
def logout():
    session.pop('supplier',None)
    return redirect('/slogin')
##########################
@app.route('/us12')
def te3():
    if "supplier" in session:
        us=session["supplier"]
        print(us)
        return redirect('/supplier')
    else:
        return redirect('/slogin')
@app.route('/add_sup',methods=['GET','POST'])
def add_sup():
    adds()
    con.execute('''delete from supplier where fname IS NULL''')
    conn.commit()
    return render_template('supplier_profile.html')
@app.route('/adds/',methods=['GET','POST'])
def adds():
    global supplier_id1
    con.execute('''select SUPPLIER_ID from supplier ''')
    data=con.fetchall()
    b = tre()
    while True:
        i=0
        if data[i]==b:
            b = tre()
            i=i+1
        else:
            supplier_id1 = b
            break
    first_name=request.form.get('fname')
    middle_name=request.form.get('mname')
    last_name=request.form.get('lname')
    ph_no=request.form.get('pno')
    off_name=request.form.get('oname')
    lice_id=request.form.get('lic_id')
    add_ress=request.form.get('shop_addr')
    aadh_no=request.form.get('aad_no')
    sql10=('''insert into supplier values (:supplier_id1,:first_name ,:middle_name,:last_name,:ph_no,:off_name,:lice_id,:add_ress,:aadh_no)''')
    qr=(supplier_id1,first_name,middle_name,last_name,ph_no,off_name,lice_id,add_ress,aadh_no)
    con.execute(sql10,qr)
    conn.commit()
    return redirect('/')
##########################
@app.route('/supplier')
def supplier():
    if 'supplier' in session:
        sp=session['supplier']
        print(sp)
        con.execute('''select ORDER_ID,MER_ID,p.Pname,o.PRODUCT_ID,QUANTITY,ORDER_TIMEDATE from orders o,product p where o.PRODUCT_ID=p.PRODUCT_ID''')
        data=con.fetchall()
        return render_template('supplier.html',data=data)
    else:
        return redirect('/slogin')
@app.route('/suppprofile')
def supplier_prof():
    if "supplier" in session:
        title = 'profile'
        sp=session["supplier"]
        con.execute('''select * from supplier where SUPPLIER_ID=:sp ''',[sp])
        data = con.fetchall()
        return render_template('sup_profile.html',data=data,title=title)
    else:
        return redirect('/slogin')
@app.route('/sup_update',methods=['GET','POST'])
def sup_update():
    if "supplier" in session:
        sp = session["supplier"]
        con.execute('''select * from supplier where SUPPLIER_ID=:sp ''',[sp])
        data=con.fetchall()
        updatesup()
        return render_template('supplier profile update.html',data=data)
    else:
        return redirect('/slogin')
@app.route('/upsup',methods=['GET','POST'])
def updatesup():
    sup_fname=request.form.get('FName')
    sup_mname=request.form.get('MName')
    sup_lname=request.form.get('LName')
    sup_pnumber=request.form.get('PNumber')
    sup_offname=request.form.get('Office Name')
    sup_lic=request.form.get('License ID')
    sup_addr=request.form.get('Address')
    sup_aadh=request.form.get('Aadhar Number')
    sp = session["supplier"]
    sqlsup=('''update supplier set FNAME=:sup_fname,MINIT=:sup_mname,LNAME=:sup_lname,PHNO=:sup_pnumber,OFFICE_NAME=:sup_offname,LICENSE_ID=:sup_lic,ADDRESS=:sup_addr,AADHAR_NO=:sup_aadh where SUPPLIER_ID=:sp ''',[sp])
    sw=(sup_fname,sup_mname,sup_lname,sup_pnumber,sup_offname,sup_lic,sup_addr,sup_aadh)
    con.execute(sqlsup,sw)
    conn.commit()
    return redirect('/suppprofile')
@app.route('/delsup')
def delsup():
    if "supplier" in session:
        sp = session["supplier"]
        con.execute('''delete from supplier where SUPPLIER_ID=:sp''',[sp])
        conn.commit()
        return '<h1>User deleted sucessfully</h1>'
    else:
        return redirect('/slogin')
@app.route('/stocks',methods=['GET','POST'])
def stocks():
    if "supplier" in session:
        title='stocks'
        sp = session["supplier"]
        con.execute('''select ps.PNAME,p.PRODUCT_ID,p.QUANTITY from provides p ,product ps where SUPPLIER_ID=:sp AND p.PRODUCT_ID=ps.PRODUCT_ID''',[sp])
        data=con.fetchall()
        return render_template('stocks product.html',data=data,title=title)
    else:
        return redirect('/slogin')
@app.route('/stocks_modify',methods=['GET','POST'])
def modifystocks():
    prodid=request.form.get('prdid')
    prod_qn=request.form.get('quant2')
    sqler=('''update provides set QUANTITY=:prod_qn where PRODUCT_ID=:prodid''')
    sdf=(prod_qn,prodid)
    con.execute(sqler,sdf)
    conn.commit()
    return redirect('/stocks')
###############################################################################################
##########merchant set###########
@app.route('/')
def login():
    lcheck()
    return render_template('login.html')
@app.route('/mlogcheck',methods=['GET','POST'])
def lcheck():
    msg="not found"
    muser=request.form.get("muser")
    mpass=request.form.get("mpass")
    con.execute('''select password from loginp where type='M' and USER_ID=:muser''',[muser])
    data=con.fetchone()
    if (data==None):
        pass
    else:
        if(mpass==data[0]):
            session['merchant']=muser
            return redirect('/merchant')
        else:
            return render_template('login.html',msg=msg)
############
@app.route('/addes_mer',methods=['GET','POST'])
def addes_mer():
    addes()
    con.execute('''delete from merchant where fname IS NULL''')
    conn.commit()
    return render_template('merchat_profile.html')
@app.route('/addes/',methods=['GET','POST'])
def addes():
    global merchant_id1
    con.execute('''select MER_ID from merchant ''')
    data=con.fetchall()
    b = tre()
    while True:
        i=0
        if data[i]==b:
            b = tre()
            i=i+1
        else:
            merchant_id1 = b
            break
    fst_name=request.form.get('fstname')
    mid_name=request.form.get('midname')
    lat_name=request.form.get('latname')
    phone_no=request.form.get('phon')
    addr_ess=request.form.get('addrs')
    sql20=('''insert into merchant values (:merchant_id1,:fst_name ,:mid_name,:lat_name,:phone_no,:addr_ess)''')
    qs=(merchant_id1,fst_name,mid_name,lat_name,phone_no,addr_ess)
    con.execute(sql20,qs)
    conn.commit()
    return redirect('/')
################


@app.route('/merchant')
def merchant():
    return render_template('merchant.html')
@app.route('/order')
def order():
    con.execute('''delete from orders where product_id is null''')
    conn.commit()
    con.execute('''select ORDER_ID,MER_ID,p.Pname,o.PRODUCT_ID,QUANTITY,ORDER_TIMEDATE from orders o,product p where o.PRODUCT_ID=p.PRODUCT_ID order by ORDER_TIMEDATE''')
    data = con.fetchall()
    return render_template('orders.html',data=data)
@app.route('/food_grains',methods=['GET','POST'])
def food_grains():
    title='food grains'
    con.execute('''select * from product where CATAGORY='food grains' ''')
    data=con.fetchall()
    ord()
    return render_template('products.html',data=data,title=title)
@app.route('/oils',methods=['GET','POST'])
def oils():
    title='oils'
    con.execute('''select * from product where CATAGORY='oils' ''')
    data=con.fetchall()
    ord()
    return render_template('products.html',data=data,title=title)
@app.route('/masalas_&_spices',methods=['GET','POST'])
def masalas_spices():
    title='masalas & spices'
    con.execute('''select * from product where CATAGORY='masalas & spices' ''')
    data=con.fetchall()
    ord()
    return render_template('products.html',data=data,title=title)
@app.route('/dry_fruits',methods=['GET','POST'])
def dry_fruits():
    title='food grains'
    con.execute('''select * from product where CATAGORY='dry fruits' ''')
    data=con.fetchall()
    ord()
    return render_template('products.html',data=data,title=title)
@app.route('/snacks',methods=['GET','POST'])
def snacks():
    title='snacks'
    con.execute('''select * from product where CATAGORY='snacks' ''')
    data=con.fetchall()
    ord()
    return render_template('products.html',data=data,title=title)
@app.route('/cleaning_&_housing',methods=['GET','POST'])
def cleaning_housing():
    title='cleaning_&_housing'
    con.execute('''select * from product where CATAGORY='cleaning & housing' ''')
    data=con.fetchall()
    ord()
    return render_template('products.html',data=data,title=title)
@app.route('/profile')
def profile():
    if 'merchant' in session:
        me=session['merchant']
        title='profile'
        con.execute('''select * from merchant where mer_id=:me ''',[me])
        data=con.fetchall()
        return render_template('profile.html',data=data,title=title)
    else:
        return redirect('/')
@app.route('/categories')
def categories():
    return render_template('categories.html')
@app.route('/add_product',methods=['GET','POST'])
def add_product():
    add()
    con.execute('''delete from product where pname IS NULL''')
    conn.commit()
    return render_template('add product.html')
@app.route('/add/',methods=['GET','POST'])
def add():
    global product_id
    con.execute('''select PRODUCT_ID from product ''')
    data=con.fetchall()
    b = tre()
    while True:
        i=0
        if data[i]==b:
            b = tre()
            i=i+1
        else:
            product_id = b
            break
    product_name=request.form.get('pname')
    product_cat=request.form.get('cat')
    product_cost=request.form.get('cost')
    product_mgdate=request.form.get('mgdate')
    product_expdate=request.form.get('expdate')
    product_quant=request.form.get('qunt')
    print(product_name)
    sql12=('''insert into product(PRODUCT_ID,PNAME,CATAGORY,COST,MFG_DATE,EXP_DATE) values (:product_id ,:product_name,:product_cat,:product_cost,:product_mgdate,:product_expdate)''')
    qq=(product_id, product_name, product_cat, product_cost, product_mgdate, product_expdate)
    con.execute(sql12,qq)
    sql13=('''insert into provides values (:product_quant,:product_id,3444222134)''')
    con.execute(sql13,(product_quant,product_id))
    conn.commit()
    return redirect('/add_product')
@app.route('/ordpd',methods=['GET','POST'])
def ord():
    if 'merchant' in session:
        me = session['merchant']
        con.execute('''select order_id from orders where mer_id=:me ''',[me])
        data1=con.fetchall()
        b=tre()
        while True:
            if b in data1:
                b=tre()
            else:
                orderid=b
                break
        pt_id=request.form.get('pdid')
        qunt1=request.form.get('quant1')
        now=datetime.now()
        sql34=('''insert into orders values(:orderid,:me,:pt_id,:qunt1,:now)''')
        que=(orderid,me,pt_id,qunt1,now)
        con.execute(sql34,que)
        conn.commit()
        return redirect('/order')

@app.route('/upprofile',methods=['GET','POST'])
def upprofile():
    if 'merchant' in session:
        me = session['merchant']
        con.execute('''select * from merchant where mer_id=:me ''',[me])
        data=con.fetchall()
        updatemer()
        return render_template('merchant profile update.html',data=data)


@app.route('/up',methods=['GET','POST'])
def updatemer():
    if 'merchant' in session:
        me = session['merchant']
        mer_fname=request.form.get('FirstName')
        mer_mname=request.form.get('MiddleName')
        mer_lname=request.form.get('LastName')
        mer_phone=request.form.get('PhoneNumber')
        mer_add=request.form.get('ShopAddress')
        sqlmer=('''update merchant set FNAME=:mer_fname ,MINIT=:mer_mname ,LNAME=:mer_lname,PHNO=:mer_phone,ADDRESS=:mer_add where mer_id=:me''')
        su=(mer_fname,mer_mname,mer_lname,mer_phone,mer_add,me)
        con.execute(sqlmer,su)
        conn.commit()
        return redirect('/profile')
@app.route('/delete')
def delmerchant():
    if 'merchant' in session:
        me = session['merchant']
        con.execute('''delete from merchant where mer_id=:me''',[me])
        conn.commit()
        return '<h1>User deleted sucessfully</h1>'

if __name__ =='__main__':
    app.run(debug=True)