import re
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
con=MySQLdb.connect("localhost","root","","woodland")
c=con.cursor()
def usrhome(request):
  uname=request.session["uname"]
  print("#######################################################3")
  print(uname)
  return render(request,"usrhome.html",{"uname":uname})
def cusviewmore(request):

  id=request.GET.get("id")
  c.execute("select * from products where ProductID='"+str(id)+"'")
  data=c.fetchall()
  d=datetime.datetime.now()
  if request.POST:
    cid=request.session["cid"]
    qty=request.POST.get("t1")
    c.execute("insert into cart(`ProductID`,`CustomerID`,`count`,date) values(%s,%s,%s,%s)",[id,cid,qty,d])
    con.commit()
  return render(request,"cusviewmore.html",{"data":data})
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
  # uid=request.session["cid"]
  
  # home="House & Rooms"
  c.execute("select * from subcategory ")
  subcat=c.fetchall()
  s = "select * from  products "
  c.execute(s)
  data = c.fetchall()
  if request.GET:
    id=request.GET.get("id")
    s="select * from products where SubcategoryID='"+str(id)+"' "
    c.execute(s)
    data=c.fetchall()
    print(s)
    return render(request,"usrhommenu.html",{"uid":uid,"uname":uname,"data":data,"subcat":subcat})
  search=request.POST.get("search")
  if request.POST.get("b1"): 
    s="select * from products where Pname like'%"+str(search)+"%'"
    c.execute(s)
    data=c.fetchall()
    print(s)
      
  return render(request,"usrhommenu.html",{"uid":uid,"uname":uname,"data":data,"subcat":subcat})

def deletecart(request):
  cid=request.GET.get("cid")
  c.execute("delete from cart where cartID='"+str(cid)+"'")
  con.commit()
  return HttpResponseRedirect("/viewcart")
def viewcart(request):
  cid=request.session["cid"]
  c.execute("select p.Pname,p.ProductID,p.image1,p.price*c.count as price ,c.cartID,p.Description from products p join cart c on p.ProductID=c.ProductID where c.CustomerID='"+str(cid)+"'")
  data=c.fetchall()
  c.execute("select sum(p.price*c.count) as total  from products p join cart c on p.ProductID=c.ProductID where c.CustomerID='"+str(cid)+"'")
  data2=c.fetchone()
  return render(request,"cart.html",{"data":data,"data2":data2})
def payment1(request):
  
  cid=request.session["cid"]
  paid="paid"
  amount=request.GET.get("amount")
  request.session["pay"]=amount
  dd=datetime.datetime.now()
  c.execute("select * from cart where CustomerID='"+str(cid)+"'")
  dataa=c.fetchall()
  for d in dataa:
    print("######################################")
    print(d[1])
    print("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(dd)+"')")
    c.execute("insert into orders (`ProductID`,`CustomerID`,`Status`,date) values('"+str(d[1])+"','"+str(cid)+"','"+str(paid)+"','"+str(dd)+"')")
    print("######################################")
  con.commit()
  if request.POST:
      card=request.POST.get("test")
      cardno=request.POST.get("cardno")
      request.session["card_no"]=cardno
      pinno=request.POST.get("pinno")
      return HttpResponseRedirect("/payment2")
  
  return render(request,"payment1.html",{"uid":cid})
def payment2(request):
  cno=request.session["card_no"]
  amount=request.session["pay"]
  if request.POST:
      name=request.POST.get("t1")
      request.session["m"]=name
      address=request.POST.get("t2")
      email=request.POST.get("t3")
      phno=request.POST.get("t4")
      # n="insert into delivery values('"+str(cno)+"','"+str(name)+"','"+str(address)+"','"+str(email)+"','"+str(phno)+"','"+str(amount)+"')"
      # print(n)
      # c.execute(n)
      # con.commit()
      return HttpResponseRedirect("/payment3")
  return render(request,"payment2.html",{"cno":cno,"amount":amount})
def payment3(request):
    return render(request,"payment3.html")

def payment4(request):
    return render(request,"payment4.html")

def payment5(request):
    cno=request.session["card_no"]
    today = date.today()
    # n="select * from delivery where card='"+str(cno)+"'"
    # c.execute(n)
    # data=c.fetchall()
    return render(request,"payment5.html")
def vieworder(request):
    cid=request.session["cid"]
    c.execute("select p.Pname,c.Fname,cr.count,p.price*cr.count,o.date,o.status,o.CustomerID from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"'")
    data=c.fetchall()
    return render(request,"vieworder.html",{"data":data})
def Invoice(request):
    cid=request.session["cid"]
    id=request.GET.get("id")
    uname=request.session["uname"]
    c.execute("select p.Pname,c.Fname,cr.count,p.price,p.price*cr.count, o.date,o.status,o.CustomerID from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"' and p.Pname='"+str(id)+"' ")
    data=c.fetchall()
    dat=data[0][5]
    c.execute("select sum(p.price*cr.count) from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.CustomerID='"+str(cid)+"' and p.Pname='"+str(id)+"' ")
    data1=c.fetchall()
    return render(request,"Invoice.html",{"data":data,"uname":uname,"dat":dat,"total":data1[0][0]})
