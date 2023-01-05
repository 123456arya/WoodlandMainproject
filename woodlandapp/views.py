import email
from re import S
import re
import MySQLdb
from django import http
from django.shortcuts import render
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
    return render(request,"EmployeePage.html")
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
        try:
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
        except:
             msg="Invalid Username or password"
    return render(request,"login.html",{"msg":msg})
def AdminPage(request):
    return render(request,"AdminPage.html")
def dailyreport(request):
    c.execute("select p.Pname,c.Fname,cr.count,p.price*cr.count,o.date,o.status from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID)")
    data=c.fetchall()
    return render(request,"dailyreport.html",{"data":data})
def datewisereport(request):
    if request.POST:
        frm=request.POST.get("t1")
        to=request.POST.get("t2")
        c.execute("select p.Pname,c.Fname,cr.count,p.price*cr.count,o.date,o.status from products p join orders o on(o.ProductID=p.ProductID) join customer c on (c.CustomerID=o.CustomerID) join cart cr on(cr.CustomerID=c.CustomerID) where o.date between '"+str(frm)+"' and '"+str(to)+"'")
        data=c.fetchall()
        return render(request,"datewisereport.html",{"data":data})
    return render(request,"datewisereport.html")
def AdminAddCategory(request):
    msg=""
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
    return render(request,"AdminAddcategory.html",{"msg":msg,"data":data})
def EmployeeViewOrder(request):
    c.execute("select o.OrderID,p.Pname,c.Fname,p.image1,o.status from orders o join products p on(p.ProductID=o.ProductID) join customer c on(c.CustomerID=o.CustomerID)")
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
    return render(request,"AdminAddsubcategory.html",{"data":data,"data1":data1,"msg":msg})
def AdminAddemployee(request):
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
    return render(request,"AdminAddEmployee.html",{"msg":msg})
def Adminviewemployee(request):
    c.execute("select * from employee")
    data=c.fetchall()
    return render(request,"Adminviewemployee.html",{"data":data})
def Adminviewcustomer(request):
    c.execute("select * from customer")
    data=c.fetchall()   
    return render(request,"Adminviewcustomer.html",{"data":data})
def Adminviewproducts(request):
    c.execute("select * from products")
    data=c.fetchall()   
    return render(request,"Adminviewproducts.html",{"data":data})
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

def Adminviewleave(request):
    # id=request.GET.get("id")
    c.execute("select e.`EmpID`,e.`Fname`,l.`DateofLeave`,l.`NoofDays`,l.`Reason`,l.`Status`,l.LeaveID from employee e join leaves l on(e.`EmpID`=l.`EmpID`) where Status='requested'")
    data=c.fetchall()
    
    return render(request,"Adminviewleave.html",{"data":data})
def Adminapprove(request):
    id=request.GET.get("id")
    c.execute("update leaves set status='Accept' where `LeaveID`='"+str(id)+"'")
    print("update leaves set status='Accept' where `LeaveID`='"+str(id)+"'")
    con.commit()
    
    return HttpResponseRedirect("/Adminviewleave")
def AdminReject(request):
    id=request.GET.get("id")
    c.execute("select e.`EmpID`,e.`Fname`,l.`DateofLeave`,l.`NoofDays`,l.`Reason`,l.`Status`,l.`LeaveID` from employee e join leaves l on(e.`EmpID`=l.`EmpID`) where l.`LeaveID`='"+str(id)+"'" )

    data=c.fetchall()
    if request.POST:
        reason=request.POST.get("t1")
        c.execute("update leaves set status='reject',`RejectReason`='"+str(reason)+"'  where `LeaveID`='"+str(id)+"'")
        con.commit()
        return HttpResponseRedirect("/Adminviewleave")
    return render(request,"AdminReject.html",{"data":data})   
def Adminviewcomplaints(request):
    # id=request.GET.get("id")
    c.execute("select e.`EmpID`,e.`Fname`,c.`title`,c.`Complaint`,c.`Response`,c.`ComplaintID` from employee e join complaint c on(e.`EmpID`=c.`EmpID`) ")
    data=c.fetchall()
    
    return render(request,"Adminviewcomplaints.html",{"data":data})
def Admincomplaintresponse(request):
    msg=""
    id=request.GET.get("id")
    c.execute("select e.`EmpID`,e.`Fname`,c.`title`,c.`Complaint`,c.`ComplaintID` from employee e join complaint c on(e.`EmpID`=c.`EmpID`) where `ComplaintID`='"+str(id)+"' ")
    data=c.fetchall()
    if request.POST:
        response=request.POST.get("t1")
        c.execute("update complaint set `Response`='"+str(response)+"' where  `ComplaintID`='"+str(id)+"' ")
        con.commit()
        msg="Complaint Response Added"   
        return HttpResponseRedirect("/Adminviewcomplaints")     
    return render(request,"Admincomplaintresponse.html",{"data":data,"msg":msg})
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
def EmployeeAddComplaints(request):
    msg=""
    empid=request.session["empid"]
    
    if request.POST:
        title=request.POST.get("t1")
        description=request.POST.get("t2")
        
        empid=request.session["empid"]
        c.execute("insert into complaint (`EmpID`,`title`,`Complaint`) values(%s,%s,%s)",[empid,title, description])
        con.commit()
        msg="Complaint Posted Successfully"
    c.execute("select * from complaint where EmpID='"+str(empid)+"'")
    data=c.fetchall()
    return render(request,"EmployeeAddComplaints.html",{"data":data,"msg":msg})
def EmployeeAddleave(request):
    empid=request.session["empid"]
    msg=""
    
    if request.POST:
        ldate=request.POST.get("t1")
        reason=request.POST.get("t2")
        days=request.POST.get("t3")
        
        status="requested"
        empid=request.session["empid"]
        c.execute("insert into leaves (`EmpID`,`DateofLeave`,`Reason`,`NoofDays`,`Status`) values(%s,%s,%s,%s,%s)",[empid,ldate,reason,days,status])
        con.commit()
        msg="Successfully Requested for Leave"
    c.execute("select * from leaves where EmpID='"+str(empid)+"'")
    data=c.fetchall()
    return render(request,"EmployeeAddleave.html",{"data":data,"msg":msg})
def addeducation(request):
    if request.POST:
        tschool=request.POST.get("t1")
        tpercentage=request.POST.get("t2")
        tcert=request.POST.get("t3")
        if request.FILES.get("t3"):
            myfile=request.FILES.get("t3")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            tcert = fs.url(filename)
        pschool=request.POST.get("t4")
        ppercentage=request.POST.get("t5")
        pcert=request.POST.get("t6")
        if request.FILES.get("t6"):
            myfile=request.FILES.get("t6")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            pcert = fs.url(filename)
        dschool=request.POST.get("t7")
        dpercentage=request.POST.get("t8")
        dcert=request.POST.get("t9")
        if request.FILES.get("t9"):
            myfile=request.FILES.get("t9")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            dcert = fs.url(filename)
        oname=request.POST.get("t13")
        oschool=request.POST.get("t10")
        opercentage=request.POST.get("t11")
        ocert=request.POST.get("t12")
        if request.FILES.get("t12"):
            myfile=request.FILES.get("t12")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            ocert = fs.url(filename)
        empid=request.session["empid"]
        c.execute("select count(*) from education where `EmpID`='"+str(empid)+"'")
        cnt=c.fetchall()
        if(cnt[0]==0):
                
            print("insert into education (`EmpID`,`TenthSchool`,`TenthPercentage`,`TenthCertificate`,`PlustwoSchool`,`PlustwoPercentage`,`PlustwoCertificate`,`DiplomaSchool`,`DiplomaPercentage`,`DiplomaCertificate`,`OtherSchool`,`OtherPercentage`,`OtherCertificate`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[empid,tschool,tpercentage,tcert,pschool,ppercentage,pcert,dschool,dpercentage,dcert,oschool,opercentage,ocert])
            c.execute("insert into education (`EmpID`,`TenthSchool`,`TenthPercentage`,`TenthCertificate`,`PlustwoSchool`,`PlustwoPercentage`,`PlustwoCertificate`,`DiplomaSchool`,`DiplomaPercentage`,`DiplomaCertificate`,`OtherName`,`OtherSchool`,`OtherPercentage`,`OtherCertificate`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[empid,tschool,tpercentage,tcert,pschool,ppercentage,pcert,dschool,dpercentage,dcert,oname,oschool,opercentage,ocert])
        else:
            c.exeecute("update education set `TenthSchool`='"+str(tschool)+"',`TenthPercentage`='"+str(tpercentage)+"',`TenthCertificate`='"+str(tcert)+"',`PlustwoSchool`='"+str(pschool)+"',`PlustwoPercentage`='"+str(ppercentage)+"',`PlustwoCertificate`='"+str(pcert)+"',`DiplomaSchool`='"+str(dschool)+"',`DiplomaPercentage`='"+str(dpercentage)+"',`DiplomaCertificate`='"+str(dcert)+"',`OtherSchool`='"+str(oschool)+"',`OtherPercentage`='"+str(opercentage)+"',`OtherCertificate`='"+str(ocert)+"' where `EmpID`='"+str(empid)+"'")

        con.commit()
        return HttpResponseRedirect("/employeeviewprofile")
    return render(request,"EmployeeAddeducation.html")
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
            
        c.execute("insert into `products` (`Pname`,`SubcategoryID`,`Price`,`Pricenot`,`Description`,`image1`,`image2`,`image3`,`image4`,`image5`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[pname,sname,price,pricenet,description,image1,image2,image3,image4,image5])
        
        con.commit()
        msg="Product Added Successfully"
    return render(request,"EmployeeAddproduct.html",{"data":data,"data1":data1,"msg":msg})