import email
from re import S
import re
import MySQLdb
from django import http
from django.shortcuts import render
from datetime import date

from datetime import datetime
import datetime
from django.http import HttpResponseRedirect
import MySQLdb
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
                return HttpResponseRedirect("/usrhommenu/")
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
    
    print(pcnt)
    return render(request,"AdminPage.html",{"pcnt":pcnt[0]})

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
    return render(request,"AdminAddcategory.html",{"msg":msg,"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
def EmployeeViewOrder(request):
    cid=request.session["cid"]
    sid=request.session["empid"]
    c.execute("select o.OrderID,p.Pname,c.Fname,p.image1,o.status from orders o join products p on(p.ProductID=o.ProductID) join customer c on(c.CustomerID=o.CustomerID) where p.sid='"+str(sid)+"'")
    data=c.fetchall()

    return render(request,"EmployeeViewOrder.html",{"data":data})
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
    return render(request,"AdminAddsubcategory.html",{"data":data,"data1":data1,"msg":msg,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
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
    c.execute("select count(*) from products ")
    pcnt=c.fetchone()
    c.execute("select count(*) from category ")
    ccnt=c.fetchone()
    c.execute("select count(*) from customer ")
    cucnt=c.fetchone()
    c.execute("select * from products")
    data=c.fetchall()   
    return render(request,"Adminviewproducts.html",{"data":data,"pcnt":pcnt[0],"ccnt":ccnt[0],"cucnt":cucnt[0]})
def viewproduct(request):
    id=request.GET.get("id")
    
    c.execute("select * from products where ProductID='"+str(id)+"'")
    data=c.fetchall()  
    if "b1" in request.POST:
          id=request.POST.get("t1")
          name=request.POST.get("t2")
          pnot=request.POST.get("t3")
          price=request.POST.get("t4")
          desc=request.POST.get("t5")
          c.execute("update products set Pname='"+str(name)+"',Pricenot='"+str(pnot)+"',Price='"+str(price)+"',Description='"+str(desc)+"' where ProductID='"+str(id)+"'")
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
def addexperiance(request):
    if request.POST:
        cname=request.POST.get("t1")
        eoe=request.POST.get("t2")
        post=request.POST.get("t3")
        empid=request.session["empid"]
        c.execute("insert into experiance (`EmpID`,`CompanyName`,`YearsofExperiance`,`Post`) values(%s,%s,%s,%s)",[empid,cname, eoe,post])
        con.commit()
        return HttpResponseRedirect("/employeeviewprofile")
    return render(request,"EmployeeAddExp.html")


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
            db.commit()
            return HttpResponseRedirect("/AdminViewProduct/")
        else:
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update products set pamount = '"+str(price)+"', qty = '"+str(qty)+"', date='"+str(cdate)+"' where pid = '"+str(pid)+"'")
            db.commit()
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
        c.execute("select * from cart where CustomerID='"+str(cid)+"'")
        dataa=c.fetchall()
        c.execute("update cart set status='Paid' where  CustomerID='"+str(cid)+"'")
        con.commit()
        for d in dataa:
            print("######################################")
            print(d[1])
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
        d="select * from cart where CustomerID='"+str(cid)+"' and status='notpaid'"
        c.execute(d)
        data=c.fetchall()
        print(d)
        qty=0
        for d in data:
            ss="select qty from products where ProductID='"+str(d[1])+"'"
            c.execute(ss)
            dd=c.fetchall()
            qty=int(dd[0][0])-int(d[3])

        u="update products set qty='"+str(qty)+"' where ProductID='"+str(d[1])+"'"
        print(u)
        c.execute(u)
        con.commit()
        cid=request.session["cid"]
        c.execute("update cart set status='paid' where CustomerID='"+str(cid)+"'")
        con.commit()
        msg="success"
     return render(request,"payment1.html",{"amount":amount,"msg":msg})

#def payment2(request):
   #=request.session["card_no"]
    #amount=request.session["pay"]
    #if request.POST:
    #    return HttpResponseRedirect("/payment3")
    #return render(request,"payment2.html",{"cno":cno,"amount":amount})

#def payment3(request):
  #  return render(request,"payment3.html")

#def payment4(request):
   # return render(request,"payment4.html")
