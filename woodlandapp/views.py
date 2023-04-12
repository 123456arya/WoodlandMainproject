import email
import pickle
from re import S
import re
import MySQLdb
from django import http
from django.shortcuts import render,redirect
from datetime import date

from datetime import datetime
import datetime
from django.http import HttpResponse, HttpResponseRedirect
import MySQLdb
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import re
from nltk.corpus import stopwords
import pyttsx3
import matplotlib.pyplot as plt

nltk.download('stopwords')
set(stopwords.words('english'))
from django.core.files.storage import FileSystemStorage
con=MySQLdb.connect("localhost","root","","woodland")
c=con.cursor()


# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")
def EmployeePage(request):
    sid=request.session["empid"]
    c.execute("select * from products where qty=0 and sid='"+str(sid)+"'")
    data=c.fetchall()
    return render(request,"EmployeePage.html",{"data":data})
def customerreg(request):
    msg=""
    if request.POST:
        fname=request.POST.get("t1")
        lname=request.POST.get("t2")
        hname=request.POST.get("t3")
        street=request.POST.get("t4")
        district=request.POST.get("t5")
        state=request.POST.get("t6")
        pin=request.POST.get("t7")
        email=request.POST.get("t8")
        mob1=request.POST.get("t9")
        mob2=request.POST.get("t10")
        uname=request.POST.get("t11")
        password=request.POST.get("t12")
        c.execute("insert into customer (`Fname`,`Lname`,`Housename`,`Street`,`District`,`State`,`PinCode`,`Email`,`Mobno1`,`Mobno2`,`username`,`password`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[fname,lname,hname,street,district,state,pin,email,mob1,mob2,uname,password])
        c.execute("insert into login (`Username`,`Password`,`Usertype`) values(%s,%s,%s)",[uname,password,'Customer'])
        con.commit()
        msg="Registered Successfully"
    return render(request,"customerreg.html",{"msg":msg})
def furniture(request):
    return render(request,"furniture.html")
def shop(request):
    return render(request,"shop.html")
def login(request):
    msg=""
    if request.POST:
        uname=request.POST.get("t11")
        password=request.POST.get("t12")
        request.session["uname"]=uname
        c.execute("select Usertype from login where Username='"+str(uname)+"' and password='"+str(password)+"'")
        data=c.fetchone()
        print(data[0])
        # try:
        if data:
            if(data[0]=="admin"):
                return HttpResponseRedirect("/AdminPage")
            elif(data[0]=="Customer"):
                c.execute("select CustomerID from customer where username='"+str(uname)+"'")
                cid=c.fetchone()
                request.session["cid"]=cid[0]
                return HttpResponseRedirect("/customerhome/")
            elif(data[0]=="Employee"):
                c.execute("select 	EmpID from employee where username='"+str(uname)+"'")
                cid=c.fetchone()
                request.session["empid"]=cid[0]
                return HttpResponseRedirect("/EmployePage")
        else:
            msg="Invalid Username or password"
        # except:
        #      msg="Invalid Username or password"
    return render(request,"login.html",{"msg":msg})
def AdminPage(request):
    
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from products")
    data=c.fetchall()   
    return render(request,"Adminpage.html",{"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})



def AdminAddCategory(request):
    msg=""
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from category")
    data=c.fetchall()

    
    if request.GET:
        try:
            cid=request.GET.get("id")
            c.execute("delete from category where categoryID='"+str(cid)+"'")
            con.commit()
            msg="deleted successfully"
        except:
            msg="Can't delete"
    if request.POST:
        cat=request.POST.get("t1")
        c.execute("insert into `category` (`category`) values(%s)",[cat])
        con.commit()
        msg="Category Added Successfully"
    c.execute("select * from category")
    data=c.fetchall()
    st="Active"
    return render(request,"AdminAddcategory.html",{"msg":msg,"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0],"st":st})
def EmployeeViewOrder(request):
    # cid=request.session["cid"]
    sid=request.session["empid"]
    c.execute("select o.OrderID,p.Pname,c.Fname,p.image1,o.status from orders o join products p on(p.ProductID=o.ProductID) join customer c on(c.CustomerID=o.CustomerID) where p.sid='"+str(sid)+"'")
    data=c.fetchall()

    return render(request,"EmployeeViewOrder.html",{"data":data})
import csv

# def EmployeeViewOrder(request):
#     sid=request.session["empid"]
#     c.execute("select o.OrderID,p.Pname,c.Fname,p.image1,o.status from orders o join products p on(p.ProductID=o.ProductID) join customer c on(c.CustomerID=o.CustomerID) where p.sid='"+str(sid)+"'")
#     data=c.fetchall()
#     return render(request, 'EmployeeViewOrder.html', {'data': data})

import csv
from datetime import datetime

def ExportEmployeeOrdersToCSV(request):
    sid=request.session["empid"]
    c.execute("select p.Pname,o.qty,o.p_price,o.date from orders o join products p on(p.ProductID=o.ProductID) join customer c on(c.CustomerID=o.CustomerID) where p.sid='"+str(sid)+"'")
    data=c.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_orders.csv"'

    writer = csv.writer(response)
    writer.writerow([ 'Product Name', 'qty', 'month','price'])

    for row in data:
        order_date_str = row[3].strftime('%Y-%m-%d')
        order_date = datetime.strptime(order_date_str, '%Y-%m-%d')
        month_name = order_date.strftime('%B')
        writer.writerow([row[0], row[1], month_name, row[2]])

    return response





def acceptorder(request):
    oid=request.GET.get("id")
    c.execute("update orders set status='Accepted' where OrderID='"+str(oid)+"'")
    con.commit()
    return HttpResponseRedirect('/order')
def deleveredorder(request):
    oid=request.GET.get("id")
    c.execute("update orders set status='Delivered' where OrderID='"+str(oid)+"'")
    con.commit()
    return HttpResponseRedirect('/order')
def deletecategory(request):
    
    return HttpResponseRedirect('/AdminAddCategory')
def deletesubcat(request):
    
    return HttpResponseRedirect('/AdminAddsubcategory')
def AdminAddsubcategory(request):
    st="Active"
    msg=""
    c.execute("select * from `category`")
    data=c.fetchall()
    c.execute("select * from subcategory")
    data1=c.fetchall()
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from category")
    data=c.fetchall()
    if request.GET:
        try:
            cid=request.GET.get("id")
            c.execute("delete from subcategory where SubID='"+str(cid)+"'")
            con.commit()
            msg="Subcategory Deleted Successfully"
        except:
            msg="Can't Delete"
    if request.POST:
        cat=request.POST.get("t1")
        subcat=request.POST.get("t2")
        c.execute("insert into `subcategory` (`categoryID`,`subcategory`) values(%s,%s)",[cat,subcat])
        con.commit()
        msg="Subcategory Added Successfully"
    c.execute("select * from subcategory")
    data1=c.fetchall()
    return render(request,"AdminAddsubcategory.html",{"data":data,"data1":data1,"msg":msg,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0],"st":st})
def AdminAddemployee(request):
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from category")
    data=c.fetchall()
    msg=""
    if request.POST:
        fname=request.POST.get("t1")
        lname=request.POST.get("t2")
        hname=request.POST.get("t3")
        street=request.POST.get("t4")
        district=request.POST.get("t5")
        state=request.POST.get("t6")
        pin=request.POST.get("t7")
        Email=request.POST.get("t8")
        mob1=request.POST.get("t9")
        mob2=request.POST.get("t10")
        desig=request.POST.get("t12")
        salary=request.POST.get("t11")
        uname=request.POST.get("t13")
        password=request.POST.get("t14")
        c.execute("select max(EmpID) from employee")
        data=c.fetchone()
        print("###################################################")
        print(data[0])
        empid=0
        if data[0] :

            empid=int(data[0])+1
        else:
            empid=1   
        c.execute("insert into `employee` (EmpID,`Fname`,`Lname`,`Housename`,`Street`,`District`,`State`,`PinCode`,`Email`,`Mob1`,`Mob2`,`Salary`,`Designation`,`username`,`password`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[empid,fname,lname,hname,street,district,state,pin,Email,mob1,mob2,salary,desig,uname,password])
        c.execute("insert into login (`Username`,`Password`,`Usertype`) values(%s,%s,%s)",[uname,password,'Employee'])
        con.commit()
        msg="Employee Added Successfully"
    return render(request,"AdminAddEmployee.html",{"msg":msg,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
def Adminviewemployee(request):
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from category")
    data=c.fetchall()
    c.execute("select * from employee")
    data=c.fetchall()
    return render(request,"Adminviewemployee.html",{"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
def Adminviewcustomer(request):
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from customer")
    data=c.fetchall()   
    return render(request,"Adminviewcustomer.html",{"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
def Adminviewproducts(request):
    st="Active"
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from products")
    data=c.fetchall()   
    return render(request,"Adminviewproducts.html",{"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0],"st":st})
def viewproduct(request):

    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from products")
    data=c.fetchall()   
    # return render(request,"viewproduct.html",{"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
    id=request.GET.get("id")
    c.execute("select * from products where ProductID='"+str(id)+"'")
    data=c.fetchall()  
    if "b1" in request.POST:
          id=request.POST.get("t1")
          name=request.POST.get("t2")
          pnot=request.POST.get("t3")
          price=request.POST.get("t4")
          desc=request.POST.get("t5")
          mat=request.POST.get("t16")
          brand=request.POST.get("t17")
          dimension=request.POST.get("t18")
          c.execute("update products set Pname='"+str(name)+"',Pricenot='"+str(pnot)+"',Price='"+str(price)+"',Description='"+str(desc)+"',Material='"+str(mat)+"',Brand='"+str(brand)+"',dimension='"+str(dimension)+"' where ProductID='"+str(id)+"'")
          con.commit()
          c.execute("select * from products where ProductID='"+str(id)+"'")

          data=c.fetchall() 
    return render(request,"viewproduct.html",{"data":data})
def deleteproduct(request):
    id=request.GET.get("id")
    c.execute("delete  from cart where ProductID='"+str(id)+"'")
    c.execute("delete  from orders where ProductID='"+str(id)+"'")
    c.execute("delete  from products where ProductID='"+str(id)+"'")
    print("delete  from products where ProductID='"+str(id)+"'")
    con.commit()
    return HttpResponseRedirect("/Adminviewproducts")
def updateproduct(request):
    id=request.GET.get("id")
    
    con.commit()
    return HttpResponseRedirect("/Adminviewproducts")
def Viewemploye(request):

    id=request.GET.get("id")
    msg=""
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from products")
    data=c.fetchall()   
   
    c.execute("select * from employee where EmpId='"+str(id)+"'")
    data1=c.fetchone()
    c.execute("select * from education where EmpID='"+str(id)+"'")
    data2=c.fetchone()
    c.execute("select * from experiance where EmpID='"+str(id)+"'")
    data3=c.fetchone()
    if request.POST:
        fname=request.POST.get("t1")
        lname=request.POST.get("t2")
        hname=request.POST.get("t3")
        street=request.POST.get("t4")
        district=request.POST.get("t5")
        state=request.POST.get("t6")
        pin=request.POST.get("t7")
        email=request.POST.get("t8")
        mobile1=request.POST.get("t9")
        mobile2=request.POST.get("t10")
        salary=request.POST.get("t11")
        desig=request.POST.get("t12")
        uname=request.POST.get("t13")
        psw=request.POST.get("t14")
        c.execute("update employee set Fname='"+str(fname)+"',Lname='"+str(lname)+"',Housename='"+str(hname)+"',Street='"+str(street)+"',District='"+str(district)+"',State='"+str(state)+"',PinCode='"+str(pin)+"',salary='"+str(salary)+"',Designation='"+str(desig)+"',Mob2='"+str(mobile2)+"' where `EmpId`='"+str(id)+"'")
        con.commit()
        msg="Updated Successfully"

    return render(request,"Viewemploye.html",{"data1":data1,"data2":data2,"data3":data3,"msg":msg})
    
    # return render(request,"Viewemploye.html",{"data":data})
def Deleteemploye(request):
    
    id=request.GET.get("id")
    c.execute("delete from login where Username in(select username from employee where EmpId='"+str(id)+"' ) ")
    c.execute("delete from experiance where EmpID='"+str(id)+"'")
    c.execute("delete from education where EmpID='"+str(id)+"'")
    c.execute("delete from leaves where EmpId='"+str(id)+"'")
    c.execute("delete from complaint where EmpId='"+str(id)+"'")
    c.execute("delete from employee where EmpId='"+str(id)+"'")   
    con.commit()
    return HttpResponseRedirect("/Adminviewemployee")
 
def Viewcustomer(request):
    id=request.GET.get("id")   
    c.execute("select * from customer where CustomerID='"+str(id)+"'")   
    data=c.fetchall()
    return render(request,"Viewcustomer.html",{"data":data})

def employeeviewprofile(request):
    uname=request.session["uname"]
    c.execute("select * from employee where username='"+str(uname)+"'")
    data1=c.fetchone()
    c.execute("select * from education where EmpID='"+str(data1[0])+"'")
    data2=c.fetchone()
    c.execute("select * from experiance where EmpID='"+str(data1[0])+"'")
    data3=c.fetchone()
    return render(request,"employeeviewprofile.html",{"data1":data1,"data2":data2,"data3":data3})

def EmployeeAddproduct(request):
    msg=""
    image1=""
    image2=""
    image3=""
    image4=""
    image5=""
    c.execute("select * from category")
    data=c.fetchall()
    c.execute("select * from subcategory")
    data1=c.fetchall()
    if "b1" in request.POST:
        pname=request.POST.get("t1")
        cname=request.POST.get("t2")
        sname=request.POST.get("t3")
        price=request.POST.get("t4")
        pricenet=request.POST.get("t5")
        qty=request.POST.get("t15")
        description=request.POST.get("t8")
        fs=FileSystemStorage()
        if request.FILES.get("t9"):
            myfile=request.FILES.get("t9")
            
            filename=fs.save(myfile.name , myfile)
            image1 = fs.url(filename)
        if request.FILES.get("t10"):
            myfile=request.FILES.get("t10")
            
            filename=fs.save(myfile.name , myfile)
            image2 = fs.url(filename)
        if request.FILES.get("t11"):
            myfile=request.FILES.get("t11")
            
            filename=fs.save(myfile.name , myfile)
            image3 = fs.url(filename)
        
        if request.FILES.get("t12"):
            myfile=request.FILES.get("t12")
            
            filename=fs.save(myfile.name , myfile)
            image4 = fs.url(filename)
        if request.FILES.get("t13"):
            myfile=request.FILES.get("t13")
            
            filename=fs.save(myfile.name , myfile)
            image5 = fs.url(filename)
            
        c.execute("insert into `products` (`Pname`,`SubcategoryID`,`Price`,`Pricenot`,`Description`,`image1`,`image2`,`image3`,`image4`,`image5`,`qty`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[pname,sname,price,pricenet,description,image1,image2,image3,image4,image5,qty])
        
        con.commit()
        msg="Product Added Successfully"
    return render(request,"EmployeeAddproduct.html",{"data":data,"data1":data1,"msg":msg})
def Employeeviewproduct(request):
    sid=request.session["empid"]
    c.execute("select * from `products` where sid='"+str(sid)+"'")
    data=c.fetchall()
    return render(request,"Employeeviewproduct.html",{"data":data})
def Employeeeditproduct(request):
    id=request.GET["id"]
    c.execute("select * from `products` where ProductID='"+str(id)+"'")
    data=c.fetchall()
    if request.POST:
        qty=request.POST["t1"]
        c.execute("update  `products` set `qty`='"+str(qty)+"' where ProductID='"+str(id)+"'")
        con.commit()
    return render(request,"Employeeeditproduct.html",{"data":data})
def AdminUpdateProduct(request):
    pid = request.GET.get('id')
    c.execute("select * from products where pid = '"+str(pid)+"'")
    data = c.fetchall()
    cdate=date.today()
    if request.POST:
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            uploaded_file_url="static"+uploaded_file_url
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update products set pamount = '"+str(price)+"', qty = '"+str(qty)+"',pimage='"+str(uploaded_file_url)+"' where pid = '"+str(pid)+"'")
            c.commit()
            return HttpResponseRedirect("/AdminViewProduct/")
        else:
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update products set pamount = '"+str(price)+"', qty = '"+str(qty)+"', date='"+str(cdate)+"' where pid = '"+str(pid)+"'")
            c.commit()
            return HttpResponseRedirect("/AdminViewProduct/")
    return render(request,"AdminUpdateProduct.html",{"data":data,"cdate":cdate})

def payment1(request):
     amount=request.GET.get("amount")
     msg=""
     if request.POST:
        request.session["pay"]=amount
        card=request.POST.get("test")
        request.session["card"]=card
        cardno=request.POST.get("cardno")
        request.session["card_no"]=cardno
        pinno=request.POST.get("pinno")
        request.session["pinno"]=pinno
        cid=request.session["cid"]
        dd=datetime.datetime.now()
        paid="paid"
        c.execute("select * from cart where CustomerID='"+str(cid)+"' and status<>'paid'")
        dataa=c.fetchall()
        c.execute("update cart set status='Paid' where  CustomerID='"+str(cid)+"'")
        con.commit()
        qty=0

        for d in dataa:
            print("######################################")
            print(d[1])
            ss="select qty from products where ProductID='"+str(d[1])+"'"
            c.execute(ss)
            dd=c.fetchall()
            qty=int(dd[0][0])-int(d[3])

            u="update products set qty='"+str(qty)+"' where ProductID='"+str(d[1])+"'"
            print(u)
            c.execute(u)
            con.commit()
            print("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(dd)+"')")
            c.execute("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(dd)+"')")
            # c.execute("update products set qty=qty-"+int(d[3])+" where ProductID='"+str(d[1])+"'")
            print("######################################")  
            con.commit()
        cno=request.session["card_no"]
        today = date.today()
        name =  request.session['uname'] 
        amount = request.session["pay"]
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        cid=request.session["cid"]
       
       
        # for d in dataa:
            
        cid=request.session["cid"]
        c.execute("update cart set status='paid' where CustomerID='"+str(cid)+"'")
        con.commit()
        msg="success"
     return render(request,"payment1.html",{"amount":amount,"msg":msg})

def AdminDeleteProduct(request):
    id=request.GET["id"]
    c.execute("update products set status='deactivate' where ProductID='"+str(id)+"'")
    c.commit()
    return HttpResponseRedirect("/Adminviewproducts")

def AdminRestoreProduct(request):
    print("###########################################################")
    id=request.GET["id"]
    status=""
    c.execute("select status from products where ProductID='"+str(id)+"'")
    data=c.fetchall()
    print("select status from products where ProductID='"+str(id)+"'")
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update products set status='"+str(status)+"' where ProductID='"+str(id)+"'")
    print("***************************************")
    print("update products set status='"+str(status)+"' where ProductID='"+str(id)+"'")
    con.commit()
    return HttpResponseRedirect("/Adminviewproducts")

def AdminRestorecategory(request):
    print("###########################################################")
    id=request.GET["id"]
    status=""
    c.execute("select status from category where categoryID='"+str(id)+"'")
    data=c.fetchall()
    print("select status from category where categoryID='"+str(id)+"'")
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update category set status='"+str(status)+"' where categoryID='"+str(id)+"'")
    print("***************************************")
    print("update category set status='"+str(status)+"' where categoryID='"+str(id)+"'")
    con.commit()
    return HttpResponseRedirect("/AdminAddCategory")

def AdminRestoresubcategory(request):
    print("###########################################################")
    id=request.GET["id"]
    status=""
    c.execute("select status from subcategory where SubID='"+str(id)+"'")
    data=c.fetchall()
    print("select status from subcategory where SubID='"+str(id)+"'")
    if (data[0][0]=='Active'):  
        status="deactivate"
    else:
        status="Active"
    c.execute("update subcategory set status='"+str(status)+"' where SubID='"+str(id)+"'")
    print("***************************************")
    print("update subcategory set status='"+str(status)+"' where SubID='"+str(id)+"'")
    con.commit()
    return HttpResponseRedirect("/AdminAddsubcategory")

def Adminviewproductreport(request):

    if request.POST:
        da1=request.POST["d1"]
        da2=request.POST["d2"]
        c.execute("select p.Pname,p.Description,sum(o.qty) as qty,sum(o.p_price) as total from orders o join products p on(o.ProductID=p.ProductID) where o.date between '"+str(da1)+"' and '"+str(da2)+"'  group by p.ProductID order by sum(o.p_price) desc")
        print("select p.Pname,p.Description,sum(o.qty) as qty,sum(o.p_price) as total from orders o join products p on(o.ProductID=p.ProductID) where o.date between '"+str(da1)+"' and '"+str(da2)+"'  group by p.ProductID order by sum(o.p_price) desc")
        data=c.fetchall()
        return render(request,"Adminviewproductreport.html",{"data":data,"da1":da1,"da2":da2})

    return render(request,"Adminviewproductreport.html")





def datewisereport(request):

    if request.POST:
        da1=request.POST["d1"]
       
        c.execute("select p.Pname,p.Description,sum(o.qty) as qty,sum(o.p_price) as total from orders o join products p on(o.ProductID=p.ProductID) where o.date='"+str(da1)+"' group by p.ProductID order by sum(o.p_price) desc")
        print("select p.Pname,p.Description,sum(o.qty) as qty,sum(o.p_price) as total from orders o join products p on(o.ProductID=p.ProductID) where o.date='"+str(da1)+"'  group by p.ProductID order by sum(o.p_price) desc")
        data=c.fetchall()
        return render(request,"datewisereport.html",{"data":data,"da1":da1})

    return render(request,"datewisereport.html")

# def my_form(request):
#     engine = pyttsx3.init()
#     engine.say('Hello, Welcome to the feedback section.')
#     engine.runAndWait()
#     return render(request,'form.html')
 
# def my_post(request):
#         if request.method == 'POST':
#                 stop_words = stopwords.words('english')
#                 # my contribution
#                 stop_words.remove('very')
#                 stop_words.remove('not')
                
#                 #convert to lowercase
#                 text1 = request.POST['text1'].lower()
                
#                 # my contribution
#                 text_final = ''.join(i for i in text1 if not i.isdigit())
#                 net_txt=re.sub('[^a-zA-Z0-9\n]', ' ',text_final)
                
                #remove stopwords    
                # processed_doc1 = ' '.join([i for i in net_txt.split() if i not in stop_words])

                # sa = SentimentIntensityAnalyzer()
                # dd = sa.polarity_scores(text=processed_doc1)
                # compound = round((1 + dd['compound'])/2, 2)
                # final=compound*100
                
                # if "enough" in text1 or "sufficient" in text1 or "ample" in text1 or "abudant" in text1:
                #    engine = pyttsx3.init()
                #    engine.say('You liked us by'+str(final)+'% Thank you for your valuable response')
                #    engine.runAndWait()
                #    feeds = feedback(feedback=text1)
                #    feeds.save()
                #    return render(request,'form.html',{'final': final,'text1':net_txt})
                   
                # elif final == 50:
                #    engine = pyttsx3.init()
                #    engine.say('Please enter an adequate resposnse, Thank You')
                #    engine.runAndWait()
                #    return render(request,'form.html',{'final': final,'text1':net_txt})
                # else:
                #    engine = pyttsx3.init()
                #    engine.say('You liked us by'+str(final)+'% Thank you for your valuable response')
                #    engine.runAndWait()
                #    if final > 50:
                    #   feeds = feedback(feedback=text1)
                    #   feeds.save()
                #       return render(request,'form.html',{'final': final,'text1':net_txt})
                #    elif final < 50:
                      #feeds = feedback(feedback=text1)
                    #   feeds.save()
                #       return render(request,'form.html',{'final': final,'text1':net_txt})
                #    else:
                    #    feeds = feedback(feedback=text1)
                    #    feeds.save()
        #                return render(request,'form.html',{'final': final,'text1':net_txt})
        # else:
        #    return redirect('my_form')
            
def RateProduct(request):
     return render(request,"rating.html")

def AdminSellerReport(request):
    c.execute("SELECT * FROM `employee`")
    data1=c.fetchall() 
    c.execute("select p.Pname,sum(co.p_price)as totalprice,sum(co.qty),ct.category,sc.subcategory,sr.Fname from products p join category ct on(p.SubcategoryID=ct.categoryID) join subcategory sc on(ct.categoryID=sc.categoryID) join employee sr on(sr.EmpID =p.sid) join orders co on(co.ProductID=p.ProductID) group by co.ProductID")
    data=c.fetchall() 
    if request.GET:
        sid=request.GET["sid"]
        c.execute("SELECT p.Pname, SUM(co.p_price) AS totalprice, SUM(co.qty), ct.category, sc.subcategory, sr.Fname FROM products p JOIN category ct ON p.SubcategoryID = ct.categoryID JOIN subcategory sc ON ct.categoryID = sc.categoryID JOIN employee sr ON sr.EmpID = p.sid JOIN orders co ON co.ProductID = p.ProductID WHERE p.sid = '"+str(sid)+"' GROUP BY co.ProductID")

        data=c.fetchall() 
        print(data)
    return render (request,"AdminSellerReport.html",{"data1":data1,"data":data})

def AdminviewreviewReport(request):
    data = ""
    c.execute("select p.Pname from products p join rate r on(p.SubcategoryID=r.message)  group by r.ProductID")
    data=c.fetchall() 
    print(data)
    return render (request,"AdminviewreviewReport.html",{"data":data})



def SellerproductReport(request):

    if request.POST:
        da1=request.POST["d1"]
        da2=request.POST["d2"]
        c.execute("select p.Pname,p.Description,sum(o.qty) as qty,sum(o.p_price) as total from orders o join products p on(o.ProductID=p.ProductID) where o.date between '"+str(da1)+"' and '"+str(da2)+"'  group by p.ProductID order by sum(o.p_price) desc")
        print("select p.Pname,p.Description,sum(o.qty) as qty,sum(o.p_price) as total from orders o join products p on(o.ProductID=p.ProductID) where o.date between '"+str(da1)+"' and '"+str(da2)+"'  group by p.ProductID order by sum(o.p_price) desc")
        data=c.fetchall()
        return render(request,"SellerproductReport.html",{"data":data,"da1":da1,"da2":da2})

    return render(request,"SellerproductReport.html")

def AdminCategoryReport(request):
    data = ""
    c.execute("select c.category,sum(co.qty),sum(co.p_price) as totalprice from orders co inner join products p on co.ProductID=p.ProductID inner join category c on p.SubcategoryID=c.categoryID group by p.ProductID")
    data=c.fetchall() 
    print(data)
    return render (request,"AdminCategoryReport.html",{"data":data})

def customerhome(request):
    name=request.session['uname']
    t="select * from category"
    c.execute(t)
    data1=c.fetchall()
    if request.GET:
        print("*****************************************************************")
        catid=request.GET["id"]
        t="select * from subcategory where categoryID='"+str(catid)+"'"
        c.execute(t)
        data2=c.fetchall()
        print(data2)
        return render(request,'customerhome.html',{"uname":name,"data1":data1,"data2":data2})
    return render(request,'customerhome.html',{"uname":name,"data1":data1})
    
def MyProfile(request):
    uname=request.session['username']   
    if request.POST:
        cname = request.POST.get("uname")
        address = request.POST.get("uaddress")
        cntry = request.POST.get("udistrict")
        state = request.POST.get("uloc")
        fon = request.POST.get("umob")
        email = request.POST.get("uemail")
        password = request.POST.get("upass")
        type= "Customer"
        qry1="update customer set cname='"+str(cname)+"', address = '"+str(address)+"', district = '"+str(cntry)+"', location ='"+str(state)+"' , mobile = '"+str(fon)+"' , password='"+str(password)+"' where email='"+str(email)+"' "
        c.execute(qry1)
        con.commit()
    qry="select * from customer where email='"+str(email)+"' "
    c.execute(qry)
    data=c.fetchone()
    return render(request,'MyProfile.html',{"data":data})
def ar(request):
    return render (request,"ar.html")


# import pandas as pd
# from django.shortcuts import render
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.model_selection import train_test_split
# from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# def encode_product_name(product):
    
#     if product not in product_map:
#         return None
import numpy as np
import pickle
from django.http import HttpResponse
from django.shortcuts import render

def predict_sales(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        product = request.POST.get('product')
        with open('sale.pkl', 'rb') as f:
            model = pickle.load(f)
        if month == 'January':
            month_int = 1
        elif month == 'February':
            month_int = 2
        elif month == 'March':
            month_int = 3
        elif month == 'April':
            month_int = 4
        elif month == 'May':
            month_int = 5
        elif month == 'June':
            month_int = 6
        elif month == 'July':
            month_int = 7
        elif month == 'August':
            month_int = 8
        elif month == 'September':
            month_int = 9
        elif month == 'October':
            month_int = 10
        elif month == 'November':
            month_int = 11
        elif month == 'December':
            month_int = 12
        else:
            return HttpResponse('Invalid month name')
        if product == 'Chair':
            product_int = 1
        elif product == 'Table':
            product_int = 2
        elif product == 'Sofa':
            product_int = 3
        else:
            valid_products = ['Chair', 'Table', 'Sofa']
            return HttpResponse(f'Invalid product name. Valid products: {", ".join(valid_products)}')
        input_data = np.zeros(22)  # create an array of zeros with 22 elements
        input_data[month_int - 1] = 1  # set the value at the month index to 1
        input_data[product_int + 11] = 1  # set the value at the product index to 1
        prediction = model.predict(input_data.reshape(1, -1))[0]  # extract the prediction value
        prediction_percent = round(prediction * 100)
        context = {
            'prediction_percent': prediction_percent
        }
        print(context)
        return render(request,'predict.html',context)
    return render(request, 'index.html')





def predict(request):
    return render(request,'predict.html')



from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('TkAgg')



def visual(request):
    # Load employee orders data
    df = pd.read_csv('employee_orders .csv')

    # Preprocess data
    month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    df['month'] = df['month'].apply(lambda x: month_map[x])
    grouped_data = df.groupby('month')[['qty', 'price']].sum()

    # Split data into training and testing sets
    train_size = int(0.8 * len(grouped_data))
    train_data = grouped_data.iloc[:train_size]
    test_data = grouped_data.iloc[train_size:]

    # Train linear regression model on training data
    model = LinearRegression()
    model.fit(train_data.index.values.reshape(-1, 1), train_data['qty'])

    # Make predictions on testing data and calculate mean squared error
    test_preds = model.predict(test_data.index.values.reshape(-1, 1))
    mse = mean_squared_error(test_data['qty'], test_preds)

    # Generate predictions for next four months and plot bar chart
    future_months = pd.DataFrame({'month': [9, 10, 11, 12]})
    future_sales = model.predict(future_months)

    plt.bar(future_months['month'], future_sales)
    plt.xticks(future_months['month'], [month for month in month_map.keys() if month_map[month] in future_months['month']] + [''], rotation=45)

    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.title('Monthly Sales Predictions')

    # Convert plot to PNG image and return as HTTP response
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    return render(request, 'visual.html', {'image': image, 'future_sales': future_sales})



import dateutil
print(dateutil.__version__)

def customization(request):
    return render(request, 'customization.html', {})



def deletecart(request):
  cid=request.GET.get("cid")
  c.execute("delete from cart where cusid='"+str(cid)+"'")
  print("delete from cart where cusid='"+str(cid)+"'")
  con.commit()
  return HttpResponseRedirect("/cartcustom")





def customization(request):
    uname=request.session["uname"]
    msg=""
    if request.POST:
        productname=request.POST.get("c1")
        image=request.POST.get("c2")
        fs=FileSystemStorage()
        myfile=request.FILES.get("c2")
        filename=fs.save(myfile.name , myfile)
        image = fs.url(filename)
        quantity=request.POST.get("c3")
        length=request.POST.get("c4")
        width=request.POST.get("c5")
        height=request.POST.get("c6")
        color=request.POST.get("c7")
        import datetime
        date=datetime.datetime.today()
        status="requested"
        cid=request.session["cid"]
        wood=request.POST.get("c10")
        x=[productname,image,quantity,length,width,height,color,date,status,cid,wood]
        print(x)
        print("insert into customization (`productname`,`image`,`quantity`,`length`,`width`,`height`,`color`,`date`,`status`,`CustomerID`,`wood`) values('"+str(productname)+"','"+str(image)+"','"+str(quantity)+"','"+str(length)+"','"+str(width)+"','"+str(height)+"','"+str(color)+"','"+str(date)+"','"+str(status)+"','"+str(cid)+"','"+str(wood)+"')")
        c.execute("insert into customization (`productname`,`image`,`quantity`,`length`,`width`,`height`,`color`,`date`,`status`,`CustomerID`,`wood`) values('"+str(productname)+"','"+str(image)+"','"+str(quantity)+"','"+str(length)+"','"+str(width)+"','"+str(height)+"','"+str(color)+"','"+str(date)+"','"+str(status)+"','"+str(cid)+"','"+str(wood)+"')")    
        con.commit()
    return render(request,"customization.html",{"msg":msg,"uname":uname})
def customizeorders(request):
  
    if request.GET:
        id=request.GET["id"]
        c.execute("update customization set status='accept' where custid='"+str(id)+"'")
        print("update customization set status='accept' where custid='"+str(id)+"'")
    c.execute("select * from customization")

    data=c.fetchall()
    con.commit()
    return render(request,"customizeorders.html",{"data":data})