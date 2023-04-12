import re
from django.forms import BaseModelForm
from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseRedirect
import MySQLdb
import random
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
import smtplib 
import urllib.request
import webbrowser
from django.contrib import messages
from datetime import date
from datetime import datetime
import datetime
import csv
import os
import time
import razorpay
con=MySQLdb.connect("localhost","root","","woodland")
c=con.cursor()
def usrhome(request):
  c.execute("select * from products join rateview on(products.ProductID=rateview.ProductID) order by rateview.`sum(rate)/count(rate)` desc")
  data = c.fetchall()
  if request.POST:
    name=request.POST["attribute"]
    s = "select * from products join rateview on(products.ProductID=rateview.ProductID) order by rateview.`sum(rate)/count(rate)` desc where products.Pname like '%"+str(name)+"%'" 
    c.execute(s)
    data = c.fetchall()
    return HttpResponseRedirect('/usrhomemenu?name='+name)
  uname=request.session["uname"]
  print("#######################################################3")
  print(uname)
  return render(request,"usrhome.html",{"uname":uname})
def cusviewmore(request):
  uname=request.session["uname"]
  id=request.GET.get("id")
  c.execute("select * from products where ProductID='"+str(id)+"'")
  data=c.fetchall()
  d=datetime.datetime.now()
  uid=request.session["cid"]
  c.execute("select sum(rate),count(rate) from rate where  usrid='"+str(uid)+"'")
  ratdata=c.fetchone()
  rating=float(ratdata[0])/float(ratdata[1])
  if "submit" in request.POST:
    print("**********************************************************")
    feedback=request.POST["feedback"]
    rat=request.POST["rating"]
    
    dat=d
    print("insert into rate (`usrid`,`date`,`rate`,`message`) values('"+str(uid)+"','"+str(dat)+"','"+str(rat)+"','"+str(feedback)+"')")
    c.execute("insert into rate (`ProductID`,`usrid`,`date`,`rate`,`message`) values('"+str(id) +"','"+str(uid)+"','"+str(dat)+"','"+str(rat)+"','"+str(feedback)+"')")
    con.commit()
  if "sub" in request.POST:
    print("============================Am SUB")
    cid=request.session["cid"]
    qty=request.POST.get("qty")
    tqty=data[0][6]
  
    c.execute("select count from cart where ProductID='"+str(id)+"' and status<>'paid' and CustomerID='"+str(cid)+"' ")
    print("select count from cart where ProductID='"+str(id)+"' and CustomerID='"+str(cid)+"' ")
    cnnt=c.fetchone()
    print(cnnt)
    ccount=0
    if cnnt:
      ccount=cnnt[0]
    if(int(ccount)< int(tqty)):
      print("********************************************************")
      c.execute("insert into cart(`ProductID`,`CustomerID`,`count`,date) values(%s,%s,%s,%s)",[id,cid,qty,d])
      con.commit()
    
    qty=int(tqty)-int(qty)
    # c.execute("update products set qty='"+str(qty)+"' where ProductID='"+str(id)+"' ")
    # con.commit()
  cn=0
  return render(request,"cusviewmore.html",{"data":data,"cn":cn,"ratdata":rating,"uname":uname})
def myaccount(request):
  msg=""
  uname=request.session["uname"]
  c.execute("select * from customer where username='"+str(uname)+"'")
  data=c.fetchall()
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
    c.execute("update customer set Fname='"+str(fname)+"',Lname='"+str(lname)+"',Housename='"+str(hname)+"',Street='"+str(street)+"',District='"+str(district)+"',State='"+str(state)+"',PinCode='"+str(pin)+"',Email='"+str(email)+"',password='"+str(password)+"',Mobno1='"+str(mob1)+"',Mobno2='"+str(mob2)+"' where username='"+str(uname)+"'")
    c.execute("update login set Password='"+str(password)+"' where Username='"+str(uname)+"'")

    con.commit()
    msg="Profile Updated Successfully"
    c.execute("select * from customer where username='"+str(uname)+"'")
    data=c.fetchall()    
  return render(request,"myaccount.html",{"data":data})
def usrhommenu(request):
  uname=request.session["uname"]
  print("##########################################")
  print(uname)
  uid=""
  
  c.execute("select * from subcategory ")
  subcat=c.fetchall()
  s = "select * from  products "
  c.execute(s)
  data = c.fetchall()
  print("***************************************************************************")
  cid=request.session["cid"]
  dd=datetime.datetime.now()
  paid="paid"
  c.execute("select * from cart where CustomerID='"+str(cid)+"' and status<>'paid'")
  dataa=c.fetchall()
  print("######################################################")
  print(dataa)
  # c.execute("update cart set status='Paid' where  CustomerID='"+str(cid)+"'")
  # con.commit()
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
      tod=datetime.datetime.today()
      print("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(tod)+"')")
      c.execute("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(tod)+"')")
      # c.execute("update products set qty=qty-"+int(d[3])+" where ProductID='"+str(d[1])+"'")
      print("######################################")  
      con.commit()
      
  print("**************************************************************************")
  if request.POST:
    name=request.POST["attribute"]
    s = "select * from  products where Pname like '%"+str(name)+"%'" 
    c.execute(s)
    data = c.fetchall()
  if request.GET:
    print("#######################################################*************")
    name=request.GET.get("name")
    s="select * from products where Pname='%"+str(name)+"%' "
    c.execute(s)
    data=c.fetchall()
    print(s)
    return render(request,"usrhommenu.html",{"uid":uid,"uname":uname,"data":data,"subcat":subcat})
  # search=request.POST.get("search")
  # if request.POST.get("b1"): 
  #   s="select * from products where Pname like'%"+str(search)+"%'"
  #   c.execute(s)
  #   data=c.fetchall()
  #   print(s)
      
  return render(request,"usrhommenu.html",{"uid":uid,"uname":uname,"data":data,"subcat":subcat})

def deletecart(request):
  cid=request.GET.get("cid")
  c.execute("delete from cart where cartID='"+str(cid)+"'")
  print("delete from cart where cartID='"+str(cid)+"'")
  con.commit()
  return HttpResponseRedirect("/viewcart")

from django.conf import settings

def viewcart(request):
  uname=request.session["uname"]
  cid=request.session["cid"]
  c.execute("select p.Pname,p.ProductID,p.image1,p.price*c.count as price ,c.cartID,p.Description,c.count,p.price from products p join cart c on p.ProductID=c.ProductID where c.CustomerID='"+str(cid)+"' and c.status='notpaid'")
  data=c.fetchall()
  c.execute("select sum(p.price*c.count) as total  from products p join cart c on p.ProductID=c.ProductID where c.CustomerID='"+str(cid)+"' and c.status='notpaid'")
  data2=c.fetchone()
  
  print("select sum(p.price*c.count) as total  from products p join cart c on p.ProductID=c.ProductID where c.CustomerID='"+str(cid)+"' and c.status='notpaid'")
 
  if request.POST:
    amt=data2[0]
    c.execute("select * from cart where CustomerID='"+str(cid)+"' and status<>'paid'")
    
    dataa=c.fetchall()
    c.execute("update cart set status='Paid' where  CustomerID='"+str(cid)+"'")
    con.commit()
    paid="paid"
    
    print("######################################################")
    print(dataa)
    # c.execute("update cart set status='Paid' where  CustomerID='"+str(cid)+"'")
    # con.commit()
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
        tod=datetime.datetime.today()
        print("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(tod)+"')")
        c.execute("insert into orders (`ProductID`,`CustomerID`,`Status`,date,qty) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(tod)+"','"+str(d[3])+"')")
        # c.execute("update products set qty=qty-"+int(d[3])+" where ProductID='"+str(d[1])+"'")
        print("######################################")  
        con.commit()
    
    
    return HttpResponseRedirect("http://localhost/payment/pay.php?amount="+str(amt))
  

  # context={'cart':total, 'payment':payment }
  return render(request,"shop-shopping-cart.html",{"data":data,"data2":data2})
def payments(request):
  amt=request.GET["amount"]
  print(amt)
  return render(request,"payment.html",{"amt":amt}) 
# def Cart(request):
#   user=()
#   is_paid=()
   
# def get_cart_total(self):
#   cart_items=self.cart_items.all()
#   price=[]
#   for cart_item in cart_items:
#     price.append(cart_item.product_price)
#     if cart_item.color_variant:
#       color_varient_price=cart_item.color_varient.price
#       price.append(color_varient_price)
#     if cart_item.size_varient:
#       size_varient_price=cart_item.size_varient.price
#       price.append(size_varient_price)
#       return sum(price)

def vieworder(request):
    uname=request.session["uname"]
    cid=request.session["cid"]
    c.execute("select p.Pname,c.Fname,cr.count,p.price*cr.count,o.date,o.status,o.CustomerID ,o.OrderID from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"' group by o.ProductID")
    data=c.fetchall()
    return render(request,"vieworder.html",{"data":data,"uname":uname})
def Invoice(request):
    cid=request.session["cid"]
    id=request.GET.get("id")
    uname=request.session["uname"]
    oid=request.GET.get('oid')
    
    date=datetime.datetime.today()
    
    c.execute("SELECT o.OrderID, p.Pname, p.price, o.qty,o.qty*p.price as total,date FROM orders o JOIN products p ON ( o.ProductID = p.ProductID ) where o.OrderID ='"+str(oid)+"'")
    data=c.fetchall()
    print("select p.Pname,c.Fname,cr.count,p.price,p.price*cr.count, o.date,o.status,o.qty,o.CustomerID from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"'and o.OrderID='"+str(oid)+"' and c.Fname='"+str(id)+"' ")
    c.execute("select c.Fname,c.Housename,c.Street,c.District,c.State,c.PinCode,c.Email,c.Mobno1 from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"'and o.OrderID='"+str(oid)+"' and c.Fname='"+str(id)+"' ")
    data2=c.fetchall()
    if data:
     dat=data[0][4]
    else:
      dat=0
    c.execute("select sum(p.price*cr.count) from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"' and p.Pname='"+str(id)+"' ")
    data1=c.fetchall()
    return render(request,"Invoice.html",{"data":data,"uname":uname,"dat":dat,"total":data1[0][0],"date":date,"data2":data2})

def Recommendedproduct(request):
   uname=request.session["uname"]
   c.execute("select products.*,rateview.*,ROUND(rateview.`sum(rate)/count(rate)`,1) from products join rateview on(products.ProductID=rateview.ProductID) order by rateview.`sum(rate)/count(rate)` desc")
   data1=c.fetchall()
   return render(request,"Recommendedproduct.html",{"data":data1,"uname":uname})
   

def productrating(request):
  uname=request.session["uname"]
  c.execute("select * from products join rateview on(products.ProductID=rateview.ProductID)  group by rateview.ProductID")
  data1=c.fetchall()
  x=[1,2]
  y=[3,4]
  for d in data1:
    x.append(d[1])
    y.append(int(d[17]))
  print(y)
  import matplotlib.pyplot as pp
  pp.plot(x,y)
  pp.show()
  return HttpResponseRedirect("/AdminPage")


def orderrating(request):
  uname=request.session["uname"]
  c.execute("select * from orders join products on(orders.OrderID=products.ProductID)  group by orders.ProductID")
  data1=c.fetchall()
  x=[1,2]
  y=[3,4]
  for d in data1:
    x.append(d[1])
    y.append((d[22]))
  print(y)
  import matplotlib.pyplot as pp
  pp.plot(x,y)
  pp.show()
  return HttpResponseRedirect("/AdminPage")