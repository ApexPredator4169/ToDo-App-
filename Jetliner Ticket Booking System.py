from email.message import EmailMessage
import mysql.connector
import datetime
import random
import smtplib
import os
fldb=mysql.connector.connect(host='localhost',\
                             user='root',\
                             passwd=os.environ.get('SQL_PASSWORD'),\
                             database='flight')
flcursor=fldb.cursor()
def booktkt() :
    flcursor.execute("select * from domesticfares order by DESTINATION")
    domerecords=flcursor.fetchall()
    flcursor.execute("select * from internationalfares order by DESTINATION")
    intlrecords=flcursor.fetchall()
    print("\nWhere We Fly")
    print("\nDomestic Destinations/Airports\n")
    for x in domerecords :
        print(x[0],end=',    ')
    print("\n\nInternational Destinations/Airports\n")
    for x in intlrecords :
        print(x[0],end=',    ')
    print("\n\nNOTE : All connection flights are through Kochi International Airport\n")
    for i in range(int(input("Enter the no. of passengers : "))) : 
        print("\n\nNOTE : Fields marked * are mandatory. Data has to be given for any one field marked ^.")
        while True :
            print("\n\n\nSTEP 1 : Enter General Details\n")
            nam=input("Enter Name in BLOCK LETTERS* : ")
            nam=nam.upper()
            ppn=input("Enter Passport No.^(For International Flights) : ")
            adn=input("Enter Aadhar Card No.^(For Domestic Flights) : ")
            age=input("Enter Age* : ")
            if nam=='' or age=='' or (ppn=='' and adn=='') :
                print("Error!!! Data not given for mandatory fields")
                continue
            else :
                break
        while True :
            datr='NULL'
            print("\n\n\nSTEP 2 : Enter Travel Details\n")
            trp=input("Enter Trip Type (One Way or Round Trip) : ")
            if trp.lower()!='one way' and trp.lower()!='round trip' :
                print("Invalid Choice")
                continue
            if trp.lower()=='one way' :
                trp='One Way'
            if trp.lower()=='round trip' :
                trp='Round Trip'
            dat=input("Enter Date of Departure (YYYY-MM-DD)* : ")
            datr='NULL'
            y=datetime.datetime(int(dat[:4]),int(dat[5:7]),int(dat[8:]))
            if y<datetime.datetime.now() :
                print("Error!!! Given Date has Already Passed")
                continue
            if trp=='Round Trip' :
                datr=input("Enter Date of Return (YYYY-MM-DD)* : ")
                y=datetime.datetime(int(datr[:4]),int(datr[5:7]),int(datr[8:]))
                if y<datetime.datetime.now() :
                    print("Error!!! Given Date has Already Passed")
                    continue
                if datr<dat :
                    print("Error!!! Cannot Return Before Departing")
                    continue
                if datr=='' :
                    print("Error!!! Cannot Proceed Without Date of Return")
                    continue
            flag=False
            dep=input("Enter Departure Airport* : ")
            for i in domerecords :
                if dep.upper() in i[0] :
                    dep=i[0]
                    flag=True
            for i in intlrecords :
                if dep.upper() in i[0] :
                    dep=i[0]
                    flag=True
            if flag==False :
                print("Error!!! We Don't Operate Flights From That Destination")
                continue
            flag=False
            arr=input("Enter Destination Airport* : ")
            for i in domerecords :
                if arr.upper() in i[0] :
                    arr=i[0]
                    flag=True
            for i in intlrecords :
                if arr.upper() in i[0] :
                    arr=i[0]
                    flag=True
            if flag==False :
                print("Error!!! We Don't Operate Flights to That Destination")
                continue
            if dep==arr :
                print("Error!!! Cannot Depart and Arrive at the Same Airport")
                continue
            if dep!='KOCHI INTERNATIONAL' and arr!='KOCHI INTERNATIONAL' :
                print("Your Flight Will Include a Halt at Kochi International Airport")
            cls=input("Enter Your Class (Economy/Business/First)* : ")
            clschk=False
            if cls.lower()=='economy' :
                cls,clschk='Economy',True
            elif cls.lower()=='business' :
                cls,clschk='Business',True
            elif cls.lower()=='first' :
                cls,clschk='First',True
            if clschk==False :
                print("Error!!! Invalid Class Selected")
                continue
            if dat=='' or dep=='' or arr=='' or cls=='' :
                print("Error!!! Data not Given for Mandatory Fields")
                continue
            else :
                break
        while True :
            print("\n\n\nSTEP 3 : Enter Contact Details\n")
            hos=input("Enter Home Phone No.* : ")
            mob1=input("Enter Primary Mobile No.* : ")
            mob2=input("Enter Secondary Mobile No. : ")
            if mob2=='' :
                mob2='NULL'
            ema=input("Enter E-mail Address* : ")
            if '@' not in ema and '.' not in ema :
                print("Invalid E-mail ID")
                continue
            if hos=='' or mob1=='' or ema=='' :
                print("Error!!! Data not Given for Mandatory Fields")
                continue
            else :
                break
        for i in intlrecords :
            if i[0]==dep :
                diat,dffr,dhfr=i[1],i[2],i[3]
            if i[0]==arr :
                aiat,affr,ahfr=i[1],i[2],i[3]
        for i in domerecords :
            if i[0]==dep :
                diat,dffr,dhfr=i[1],i[2],i[3]
            if i[0]==arr :
                aiat,affr,ahfr=i[1],i[2],i[3]
        fare=0
        if cls=='Economy' :
            fare=dffr+affr
        elif cls=='Business' :
            fare=dffr+dhfr+ahfr+affr
        elif cls=='First' :
            fare=(dffr+affr)*2
        if trp=='Round Trip' :
            fare*=2
        if int(age)<2 :
            fare=0
        elif int(age)<12 or int(age)>65 :
            fare/=2
        cont=''
        tno=str(datetime.datetime.now())
        print("\n\n\n--------------------------------------------------------------------------------\nTICKET GENERATED\n")
        print("Ticket No. :",tno)
        print("Name of Passenger :",nam)
        print("Age :",age)
        if adn=='' :
            print("Passport No. :",ppn)
            cont+='Ticket No. : '+tno+'\nName of Passenger : '+nam+'\nAge : '+age+'\nPassport No. : '+ppn+'\n'
        else :
            print("Aadhar No. :",adn)
            cont+='Ticket No. : '+tno+'\nName of Passenger : '+nam+'\nAge : '+age+'\nAadhar No. : '+adn+'\n'
        print("Trip Type :",trp)
        print("Class :",cls)
        print("Ticket Fare : ₹",fare)
        print("-----DEPARTURE DETAILS-----")
        print("Departure Airport :",dep,'(',diat,')')
        print("Destination Airport :",arr,'(',aiat,')')
        print("Date of Departure :",dat)
        h=random.randint(00,23)
        if h<10 :
            h+=9
        m=random.randint(00,59)
        if m<10 :
            m+=9
        print("Time of Departure :",h,':',m,'GMT')
        cont+='Trip Type : '+trp+'\nClass : '+cls+'\nTicket Fare : ₹ '+str(fare)+'\n-----DEPARTURE DETAILS-----\nDeparture Airport : '+dep+'('+diat+')\nDestination Airport : '\
               +arr+'('+aiat+')\nDate of Departure : '+dat+'\nTime of Departure : '+str(h)+':'+str(m)+' GMT\n'
        if trp=='Round Trip' :
            print("-----RETURN DETAILS-----")
            print("Departure Airport :",arr,'(',aiat,')')
            print("Destination Airport :",dep,'(',diat,')')
            print("Date of Return :",datr)
            h=random.randint(00,23)
            if h<10 :
                h+=9
            m=random.randint(00,59)
            if m<10 :
                m+=9
            print("Time of Departure :",h,':',m,'GMT')
            cont+='-----RETURN DETAILS-----\nDeparture Airport : '+arr+'('+aiat+')\nDestination Airport : '+dep+'('+diat+')\nDate of Return : '+datr+'\nTime of Departure : '\
                   +str(h)+':'+str(m)+' GMT\n'
        cont+='Please Pay the Fare by Using Our Dedicated Payment Site https://www.payments.jetliner.com or Pay on Check-in\nIf You Have Any Queries Please Feel Free to Send \
an E-mail to our Dedicated Customer Service E-mail : jetlinertm@gmail.com\nThank You for Choosing Jetliner™\nHave a Safe and Wonderful Journey\n                      Flying \
Safe..............For You'
        print("--------------------------------------------------------------------------------")
        user=os.environ.get('MAIL_USER')
        password=os.environ.get('MAIL_PASSWORD')
        email=EmailMessage()
        email['Subject']='Jetliner™ Flight Ticket'
        email['From']=user
        email['To']=ema
        email.set_content(cont)
        with smtplib.SMTP_SSL('smtp.gmail.com','465') as smtp :
            smtp.login(user,password)
            smtp.send_message(email)
        print("A Copy of the Flight Details Have Been Sent to the Given Email-ID")
        print("Please Pay the Fare by Using Our Dedicated Payment Site https://www.payments.jetliner.com or Pay on Check-in")
        print("If You Have Any Queries Please Feel Free to Send an E-mail to our Dedicated Customer Service E-mail : jetlinertm@gmail.com")
        if adn=='' :
            adn='NULL'
        if ppn=='' :
            ppn='NULL'
        if datr=='NULL' :
            flcursor.execute("insert into passengerdata values('"+tno+"','"+nam+"',"+age+",'"+ppn+"',"+adn+",'"+trp+"','"+dat+"',"+datr+",'"+dep+"','"+arr+"','"+cls+"',\
"+str(fare)+",'"+ema+"','"+hos+"','"+mob1+"','"+mob2+"')")
        else :
            flcursor.execute("insert into passengerdata values('"+tno+"','"+nam+"',"+age+",'"+ppn+"',"+adn+",'"+trp+"','"+dat+"','"+datr+"','"+dep+"','"+arr+"','"+cls+"',\
"+str(fare)+",'"+ema+"','"+hos+"','"+mob1+"','"+mob2+"')")
        fldb.commit()
def viewtkt() :
    tno=input("Enter Your Ticket No. : ")
    flcursor.execute("select * from passengerdata")
    data=flcursor.fetchall()
    cont=''
    f=False
    for i in data :
        if i[0]==tno :
            ema=i[12]
            f=True
            cont="Hey There,\nWe Just Detected A Sign-In Using Your Ticket No.\nIf This Wasn't You, Please Contact Our Customer Service Manager : jetlinertm@gmail.com\nJetliner™                      Flying Safe..............For You"
            print("Date of Departure :",i[6])
            if i[5]=='Round Trip' :
                print("Date of Return :",i[7])
    if f==False :
        print("Ticket No. Not Found")
    else :
        user=os.environ.get('MAIL_USER')
        password=os.environ.get('MAIL_PASSWORD')
        email=EmailMessage()
        email['Subject']='Jetliner™ Flight Ticket'
        email['From']=user
        email['To']=ema
        email.set_content(cont)
        with smtplib.SMTP_SSL('smtp.gmail.com','465') as smtp :
            smtp.login(user,password)
            smtp.send_message(email)
def modtkt() :
    tno=input("Enter Your Ticket No. : ")
    flcursor.execute("select * from passengerdata")
    data=flcursor.fetchall()
    f=False
    for i in data :
        if i[0]==tno :
            f=True
            flag=True
            ema=i[12]
            cont="Your Travel Details Have Been Changed"
            if i[5]=='Round Trip' :
                print("\nMENU\n 1. Edit Date of Departure\n2. Edit Date of Return\n3. Edit Both Date of Departure and Return\n4. Exit\n")
                c=int(input("Enter Your Choice : "))
                if c==1 :
                    dat=input("Enter New Date of Departure (YYYY-MM-DD) : ")
                    y=datetime.datetime(int(dat[:4]),int(dat[5:7]),int(dat[8:]))
                    if y<datetime.datetime.now() :
                        print("Error!!! New Date of Departure has Already Passed")
                        flag=False
                        break
                    if dat>str(i[7]) :
                        print("Error!!! Date of Departure Cannot be Later Than Date of Return")
                        flag=False
                        break
                    cont+="New Date of Departure : "+dat
                    flcursor.execute("update passengerdata set DATE_OF_DEPARTURE='"+dat+"'where TICKET_NO='"+tno+"'")
                    fldb.commit()
                    print("Date of Departure Updated")
                elif c==2 :
                    datr=input("Enter New Date of Return (YYYY-MM-DD) : ")
                    y=datetime.datetime(int(datr[:4]),int(datr[5:7]),int(datr[8:]))
                    if y<datetime.datetime.now() :
                        print("Error!!! New Date of Return has Already Passed")
                        flag=False
                        break
                    if datr<str(i[6]) :
                        print("Error!!! Date of Return Cannot be Earlier Than Date of Departure")
                        flag=False
                        break
                    cont+="New Date of Return : "+datr
                    flcursor.execute("update passengerdata set DATE_OF_RETURN='"+datr+"'where TICKET_NO='"+tno+"'")
                    fldb.commit()
                    print("Date of Return Updated")
                elif c==3 :
                    dat=input("Enter New Date of Departure (YYYY-MM-DD) : ")
                    y=datetime.datetime(int(dat[:4]),int(dat[5:7]),int(dat[8:]))
                    if y<datetime.datetime.now() :
                        print("Error!!! New Date of Departure has Already Passed")
                        flag=False
                        break
                    datr=input("Enter New Date of Return (YYYY-MM-DD) : ")
                    z=datetime.datetime(int(datr[:4]),int(datr[5:7]),int(datr[8:]))
                    if z<datetime.datetime.now() :
                        print("Error!!! New Date of Return has Already Passed")
                        flag=False
                        break
                    if dat>datr :
                        print("Error!!! Date of Departure is Later Than Date of Return")
                        flag=False
                        break
                    cont+="New Date of Departure : "+dat+"\nNew Date of Return : "+datr
                    flcursor.execute("update passengerdata set DATE_OF_DEPARTURE='"+dat+"'where TICKET_NO='"+tno+"'")
                    fldb.commit()
                    f=True
                    flcursor.execute("update passengerdata set DATE_OF_RETURN='"+datr+"'where TICKET_NO='"+tno+"'")
                    fldb.commit()
                    print("Date of Departure and Date of Return Updated")
                elif c==4 :
                    break
                else :
                    print("Invalid Input")
                    break
            else :
                print("\nMENU\n 1. Edit Date of Departure\n2. Exit\n")
                c=int(input("Enter Your Choice : "))
                if c==1 :
                    dat=input("Enter New Date of Departure (YYYY-MM-DD) : ")
                    y=datetime.datetime(int(dat[:4]),int(dat[5:7]),int(dat[8:]))
                    if y<datetime.datetime.now() :
                        print("Error!!! New Date of Departure has Already Passed")
                        flag=False
                        break
                    cont+="New Date of Departure : "+dat
                    flcursor.execute("update passengerdata set DATE_OF_DEPARTURE='"+dat+"'where TICKET_NO='"+tno+"'")
                    fldb.commit()
                    print("Date of Departure Updated")
                elif c==2 :
                    break
                else :
                    print("Invalid Input")
                    break
    cont+="\nIf You Have Any Queries Please Feel Free to Send an E-mail to our Dedicated Customer Service E-mail : jetlinertm@gmail.com\nThank You for Choosing Jetliner™\n\
Have a Safe and Wonderful Journey\n                      Flying Safe..............For You"
    if f==False :
        print("Ticket No. Not Found")
    else :
        if flag==False :
            pass
        else :
            user=os.environ.get('MAIL_USER')
            password=os.environ.get('MAIL_PASSWORD')
            email=EmailMessage()
            email['Subject']='Jetliner™ Flight Ticket'
            email['From']=user
            email['To']=ema
            email.set_content(cont) 
            with smtplib.SMTP_SSL('smtp.gmail.com','465') as smtp :
                smtp.login(user,password)
                smtp.send_message(email)
def deltkt() :
    tno=input("Enter Ticket No. : ")
    flcursor.execute("select * from passengerdata")
    f=False
    cont=''
    data=flcursor.fetchall()
    for i in data :
        if i[0]==tno :
            ema=i[12]
            flcursor.execute("delete from passengerdata where TICKET_NO='"+tno+"'")
            fldb.commit()
            print("Your Ticket Has Been Deleted\nYour Fare Amount of ₹",i[11],"Will be Refunded Within 2 Working Days\nWe Hope You Will Join Us in the Skies Again")
            cont+="Your Ticket Has Been Deleted\nYour Fare Amount of ₹ "+str(i[11])+" Will be Refunded Within 2 Working Days\n"
            f=True
    cont+="If You Have Any Queries Please Feel Free to Send an E-mail to our Dedicated Customer Service E-mail : jetlinertm@gmail.com\nWe Hope You Will Join Us in the \
Skies Again\nJetliner™                      Flying Safe..............For You"
    if f==False :
        print("Ticket No. Not Found")
    else :
        user=os.environ.get('MAIL_USER')
        password=os.environ.get('MAIL_PASSWORD')
        email=EmailMessage()
        email['Subject']='Jetliner™ Flight Ticket'
        email['From']=user
        email['To']=ema
        email.set_content(cont)
        with smtplib.SMTP_SSL('smtp.gmail.com','465') as smtp :
            smtp.login(user,password)
            smtp.send_message(email)
while True :
    print("\n_____-----JETLINER™ AIR TICKET BOOKING SYSTEM-----_____\n")
    print("NOTE : Due to the Current COVID-19 Pandemic Restrictions, We are Operating to 283 Destinations Only\nIf any Airspace is Closed and Your Ticket is for That Destination, We Will Refund Your Ticket Amount Within 2 Working Days\n")
    print("MENU\n1. Book a Ticket\n2. View Your Departure (and Return) Date(s)\n3. Modify Your Ticket\n4. Cancel Your Ticket\n5. Exit\n")
    ch=int(input("Enter Your Choice : "))
    if ch==1 :
        booktkt()
    elif ch==2 :
        viewtkt()
    elif ch==3 :
        modtkt()
    elif ch==4 :
        deltkt()
    elif ch==5 :
        break
    else :
        print("Invalid Input")
flcursor.close()
fldb.close()
print("Thank You for Choosing Jetliner™")
print("Have a Safe and Wonderful Journey!")
print("Flying Safe............For You")
