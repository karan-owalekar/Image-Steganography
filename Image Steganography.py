from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

#Defining the tkinter's root variable
r = Tk()
#Setting up the title
r.title("Image Steganography")
#To show our own icon in the taskbar
r.call('wm', 'iconphoto', r._w, PhotoImage(file='AppImages/Icon.png'))

#Setting up the font for our app
large_font = ('Verdana',15)

def Help():
    #Setting up the function that runs when we press Help button
    messagebox.showinfo("INFO","_.I_M_A_G_E._ _.S_T_E_G_A_N_O_G_R_A_P_H_Y._\n~Karan Owalekar\n\n\n#INSERT Helps to insert the plain text into the image.\n#Entract Helps to extract the message from encoded image.")

def BACK():
    #Function that runs when we press Back button...
    #By pressing this, we remove all the other frames which are on top of main frame
    fInsert.pack_forget()
    fExtract.pack_forget()
    #Removing the previous data...
    IEntry.delete(0,END)
    ITxtEntry.delete(0,END)
    IFileEntry.delete(0,END)
    IKeyEntry.delete(0,END)
    NewTxtEntry.delete(0,END)
    EKeyEntry.delete(0,END)
    EEntry.delete(0,END)
    f.pack()

def Insert():
    #This function unpacks the main frame and puts the Insert frame on place of that...
    f.pack_forget()
    fExtract.pack_forget()
    fInsert.pack()
def Extract():
    #Here we put extract frame in place of main frame
    f.pack_forget()
    fInsert.pack_forget()
    fExtract.pack()

def INSERT_TEXT():
    #With the help of this function, we insert text from textbox into our inserted images...
    #First we get the location of the image...
    Loc = list(IEntry.get())
    #If we just copy the location from file explored we will get "\" in it, so to replace "\" with "/" we run following code...
    for i in range(len(Loc)):
        if Loc[i] == '\\':   #Using "//" because "\" is the special character and to gert "\" we need to use "\" before that hence "\\"
            Loc[i]="/"
    Loc = "".join(Loc)

    try:
        #Opening the image from the given location and converting that to RGB
        image = Image.open(Loc)  
        image = image.convert('RGB')
    except Exception:
        #If we enter wrong location we will get message-box displaying error
        messagebox.showerror("ERROR","Image not found !!!")


    x = v1.get()   #Checking our first radio button
    if x==1:    #If x=1 we take text from the text box...
        plain = ITxtEntry.get()
        if plain == "":    #If there is no text, it will convert that to " " and encrypt it giving us with cyphertext
            plain = " "
    else:    #Here we take text from an text file (whose location is provided)
        temp = list(IFileEntry.get())
        #Using same procedure as above to access file contents...
        for i in range(len(temp)):
            if temp[i] == '\\':
                temp[i]="/"
        temp = "".join(temp)
        ext = temp.split(".")
        if ext[-1] == "txt":
            try:
                with open(temp,"r") as txt_file:
                    plain = txt_file.read()
            except Exception:
                messagebox.showerror("ERROR","File not found !!!")
        else:
            messagebox.showerror("ERROR","File type not supported !")
    try:
        y = list(plain)
        for i in range(len(y)):
            if y[i] == '\n':
                y[i]='\\n'
        plain="".join(y)
    except Exception:
        pass

    #Getting the key to encrypt the image...
    key = IKeyEntry.get()
    if key == "":
        #Necessary to provide a key
        messagebox.showwarning("WARNING","NO KEY USED, Reciever might not be able to view message !")

    try:
        #Now, calling encrypt funv=ction to get encrypted text...
        cipher = ENCRYPT(plain,key)
        #Using insert function to embedd that into our image...
        INSERT(image,cipher)
    except Exception:
        pass 
def INSERT(image,cipher):
    #This function embedds cypher text into image
    plain = ITxtEntry.get()
    #Getting the size of image
    width, height = image.size 
    if len(plain) > ((width*height)/3):
        #As we are encoding each character into 3 pixels we check if number of characters are more than .33pixels in image...
        messagebox.showerror("ERROR","Text too long to be encoded into image !")
    else:
        #Getting the pixel values of the image...
        pix_val = list(image.getdata())
        pix_val = [list(x) for x in pix_val]    #Converting them into list of pixel values...

        step = 0
        #Now taking 3 pixels at a time... 
        #Let [r1, g1, b1], [r2, g2, b2], [r3 ,g3, b3] be our 3 pixels in which and our character is "a" => (65)10 => (01000001)2
        #Here we have 8 bits and 9 pixel values...
        #so deending on our bit we change or not change the pixel value...
        #EG => bit1 = 0, if r1%2 == 0, we dont change else we subtract it by 1 to make r1%2 = 0
        #We do this for all 8 pixels
        # (0, 1, 0, 0, 0, 0, 0, 1) = (r1%2, g1%2, b1%2, r2%2, g2%2, b2%2, r3%2, g3%2)
        #Last pixel value is used to tell if this is our last character or not ...
        #If this is last character then b3%2 == 0.
        #If we get b3%2 == 0, then we stop there... else we continue...
        for i in range(len(cipher)):
            a = ord(cipher[i])
            a = list(format(a,'08b'))
            k=0
            for _ in range(3):
                if str((pix_val[step][0])%2) != a[k]:
                    if pix_val[step][0]!=0:
                        pix_val[step][0]-=1
                    else:
                        pix_val[step][0]+=1
                k+=1

                if str((pix_val[step][1])%2) != a[k]:
                    if pix_val[step][1]!=0:
                        pix_val[step][1]-=1
                    else:
                        pix_val[step][1]+=1
                k+=1

                if k!=8:
                    if str((pix_val[step][2])%2) != a[k]:
                        if pix_val[step][2]!=0:
                            pix_val[step][2]-=1
                        else:
                            pix_val[step][2]+=1
                    k+=1
                else:
                    if i != len(cipher)-1:
                        if (pix_val[step][2])%2 != 0:
                            if pix_val[step][2]!=0:
                                pix_val[step][2]-=1
                            else:
                                pix_val[step][2]+=1
                    else:
                        if (pix_val[step][2])%2 != 1:
                            if pix_val[step][2]!=0:
                                pix_val[step][2]-=1
                            else:
                                pix_val[step][2]+=1

                step+=1
        
        #Once we change the pixel values, we make them permanent and make a new image using them...
        #We save the image to the location provided, if location is not provided, we simply save that in same directory 
        h=0
        w=0
        for i in range((len(cipher))*3):
            if i == width:
                h+=1
                w=0
            else:
                t = []
                t.append(pix_val[i][0])
                t.append(pix_val[i][1])
                t.append(pix_val[i][2])
                t = tuple(t)
                image.putpixel( (w,h) , t )
                w+=1
        #image.show()
        if NewImgEntry.get() == "":
            temp = list(IEntry.get())
            for i in range(len(temp)):
                if temp[i] == '\\':
                    temp[i]="/"
            temp = "".join(temp)
            location = temp.split(".")
            location.insert(1,"(1).")
            location[-1]="png"
            location = "".join(location)
        else:
            try:
                location = NewImgEntry.get()
            except Exception:
                messagebox.showerror("ERROR","INVALID Location !!!")
        try:
            image.save(location)
        except Exception:
            pass
def ENCRYPT(plain,key):
    #The following is my encryption technique...
    key_len = len(key)
    plain_split = []
    cipher=[]
    plain = list(plain)
    if len(plain) % (key_len) != 0:
        a = key_len - (len(plain)%(key_len))
        for i in range(a):
            plain.append(" ")
    for i in range(0,len(plain),key_len):
        temp = []
        for j in range(key_len):
            temp.append(plain[i+j])
        plain_split.append(''.join(temp))
    
    for i in range(len(plain_split)):
        if i == 0:
            cipher.append(GET_CIPHER(plain_split[i],key))
        else:
            cipher.append(GET_CIPHER(plain_split[i],cipher[i-1]))
    return("".join(cipher))
def GET_CIPHER(plain,key):
    ans=[]
    for i in range(len(plain)):
        x = ord(plain[i])
        y = ord(key[i])
        if i%2 == 0:
            for j in range(y):
                x+=1
                if x==127:
                    x=32
        else:
            for j in range(y):
                x-=1
                if x==31:
                    x=126
        ans.append(chr(x))
    return("".join(ans))

def EXTRACT_TEXT():
    #Here we get the image to extract data...
    Loc = list(EEntry.get())
    for i in range(len(Loc)):
        if Loc[i] == '\\':
            Loc[i]="/"
    Loc = "".join(Loc)
    try:
        image = Image.open(Loc)  
        image = image.convert('RGB')
    except Exception:
        messagebox.showerror("ERROR","Image Location NOT Found !!!")

    key = EKeyEntry.get()
    if key == "":
        messagebox.showwarning("WARNING","No key used, Message might be not VALID")

    try:  
        cipher = EXTRACT(image,key)
        DECRYPT(cipher)
    except Exception:
        pass
def EXTRACT(image,key):
    #Again getting the pixel values...
    #We do same process of getting %2 to get character ascii values in binary...
    #We do this process wntill we have b3%2 as 0...
    pix_val = list(image.getdata())
    pix_val = [list(x) for x in pix_val]
    step = 0
    ans = []
    while (True):
        temp = []
        for _ in range(3):
            temp.append(pix_val[step][0]%2)
            temp.append(pix_val[step][1]%2)
            temp.append(pix_val[step][2]%2)
            step+=1
        check = temp[8]
        temp.pop(8)
        temp = [str(i) for i in temp]
        ans.append("".join(temp))
        if check == 1:
            break
    
    for i in range(len(ans)):
        ans[i] = chr(int(ans[i],2))

    #Returning the joint character string...
    return(''.join(ans))
def DECRYPT(cipher):
    key = EKeyEntry.get()
    key_len = len(key)
    cipher_split = []
    plain = []

    temp = list(cipher)
    if len(cipher) % (key_len) != 0:
        a = key_len - (len(cipher)%(key_len))
        for i in range(a):
            temp.append(" ")
        cipher = "".join(temp)
            
    for i in range(0,len(cipher),key_len):
        temp = []
        for j in range(key_len):
            temp.append(cipher[i+j])
        cipher_split.append(''.join(temp))

    for i in range(len(cipher_split)-1,-1,-1):
        if i == 0:
            plain.insert(0,GET_PLAIN(cipher_split[i],key))
        else:
            plain.insert(0,GET_PLAIN(cipher_split[i],cipher_split[i-1]))
    
    y = list("".join(plain))

    for i in range(len(y)):
        j=i+1
        if j>=len(y):
            pass
        else:
            if y[i]=="\\" and y[i+1]=="n":
                y[i]="\n"
                y = y[:i+1] + y[i + 1 + 1:]
    x="".join(y)
    ans = "".join(x)
    if v2.get() == 2:
        temp = list(NewTxtEntry.get())
        for i in range(len(temp)):
            if temp[i] == '\\':
                temp[i]="/"
        temp = "".join(temp)
        location = temp.split(".")
        location[-1]=".txt"
        location = "".join(location)
        try:
            file = open(location,"w")
            file.writelines(ans)
        except Exception:
            messagebox.showerror("ERROR","INALID Location !!!")
    else:
        ans = list(ans)
        for i in range(len(ans)):
            if ans[i]=="\n":
                ans[i]=" "
        tTxtLoc.set("".join(ans))
def GET_PLAIN(cipher,key):
    ans=[]
    for i in range(len(cipher)):
        x = ord(cipher[i])
        y = ord(key[i])
        if i%2 == 0:
            for _ in range(y):
                x-=1
                if x<=31:
                    x=126
        else:
            for _ in range(y):
                x+=1
                if x>=127:
                    x=32
        #print(x)
        ans.append(chr(x))
    return("".join(ans))


#Building the App...

#Main frame
f = Frame(r)
f.configure(bg="White")

ImgBulb  = ImageTk.PhotoImage(Image.open("AppImages/Bulb.png"))
Bulb = Button(f,image = ImgBulb,borderwidth = 0 , bg = "White",command = Help)
Bulb.grid(row=0,column=0)

ImgBulb_  = ImageTk.PhotoImage(Image.open("AppImages/Bulb_.png"))
Bulb_ = Label(f,image = ImgBulb_,borderwidth = 0)
Bulb_.grid(row=0,column=1)


ImgIs  = ImageTk.PhotoImage(Image.open("AppImages/IS.png"))
Lis = Label(f,image = ImgIs,borderwidth = 0)
Lis.grid(row=1,columnspan=2)

ImgInsert  = ImageTk.PhotoImage(Image.open("AppImages/Insert.png"))
Insert = Button(f,image = ImgInsert,borderwidth = 0 , bg = "White",command = Insert)
Insert.grid(row=2,columnspan=2)

ImgExtract  = ImageTk.PhotoImage(Image.open("AppImages/Extract.png"))
Extract = Button(f,image = ImgExtract,borderwidth = 0 , bg = "White",command = Extract)
Extract.grid(row=3,columnspan=2)

f.pack()
#END of main frame

#Insert frame
fInsert = Frame(r)
fInsert.configure(bg="White")

tILoc = StringVar()
tIPlainText = StringVar()
tITextFIle = StringVar()
tIKey = StringVar()
tNewLoc = StringVar()
v1 = IntVar(None,1)

ImgI_back  = ImageTk.PhotoImage(Image.open("AppImages/Insert_Back.png"))
IBack = Button(fInsert,image = ImgI_back,borderwidth = 0 , bg = "White",command = BACK)
IBack.grid(row=0,column=0)

ImgI_back_bulb = ImageTk.PhotoImage(Image.open("AppImages/Insert_Back_Bulb.png"))
IBack_Bulb = Label(fInsert,image = ImgI_back_bulb,borderwidth = 0 , bg = "White")
IBack_Bulb.grid(row=0,column=1,columnspan=2)

ImgI_bulb  = ImageTk.PhotoImage(Image.open("AppImages/Insert_Bulb.png"))
IBulb = Button(fInsert,image = ImgI_bulb,borderwidth = 0 , bg = "White")
IBulb.grid(row=0,column=3)

ImgINSERT = ImageTk.PhotoImage(Image.open("AppImages/Insert_insert.png"))
IInsert = Label(fInsert,image = ImgINSERT,borderwidth = 0 , bg = "White")
IInsert.grid(row=1,columnspan=4,pady=(0,10))

ImgILoc = ImageTk.PhotoImage(Image.open("AppImages/Insert_img_loc.png"))
ILoc = Label(fInsert,image = ImgILoc,borderwidth = 0 , bg = "White")
ILoc.grid(row=2,columnspan=4)

IEntry = Entry(fInsert,textvariable = tILoc,font = large_font,width = 38,fg="gray20",borderwidth=2)
IEntry.grid(row=3,columnspan=4,pady=(0,20))

ImgIPlnTxt = ImageTk.PhotoImage(Image.open("AppImages/Insert_plain_text.png"))
IPlain = Label(fInsert,image = ImgIPlnTxt,borderwidth = 0 , bg = "White")
IPlain.grid(row=4,columnspan=2)

ImgITxtFile = ImageTk.PhotoImage(Image.open("AppImages/Insert_txt_loc.png"))
ITxtLoc = Label(fInsert,image = ImgITxtFile,borderwidth = 0 , bg = "White")
ITxtLoc.grid(row=4,column=2,columnspan=2)

r1 = Radiobutton(fInsert,variable = v1,value = 1,bg="White",text = "                                                              ")
r1.grid(row=5,column=0,columnspan=2)
r2 = Radiobutton(fInsert,variable = v1,value = 2,bg="White",text = "                                                         ")
r2.grid(row=5,column=2,columnspan=2)

ITxtEntry = Entry(fInsert,textvariable = tIPlainText,font = large_font,width = 17,fg="gray20",borderwidth=2)
ITxtEntry.grid(row=6,columnspan=2)

IFileEntry = Entry(fInsert,textvariable = tITextFIle,font = large_font,width = 17,fg="gray20",borderwidth=2)
IFileEntry.grid(row=6,column=2,columnspan=2)

ImgIkey = ImageTk.PhotoImage(Image.open("AppImages/Insert_key.png"))
IKey = Label(fInsert,image = ImgIkey,borderwidth = 0 , bg = "White")
IKey.grid(row=7,columnspan=4,pady= (15,0))

IKeyEntry = Entry(fInsert,textvariable = tIKey,font = large_font,width = 22,fg="gray20",borderwidth=2)
IKeyEntry.grid(row=8,column=1,columnspan=2,pady = (5,10))

ImgNewImg = ImageTk.PhotoImage(Image.open("AppImages/Insert_New_Image.png"))
NewImage = Label(fInsert,image = ImgNewImg,borderwidth = 0 , bg = "White")
NewImage.grid(row=9,columnspan=4)

NewImgEntry = Entry(fInsert,textvariable = tNewLoc,font = large_font,width = 38,fg="gray20",borderwidth=2)
NewImgEntry.grid(row=10,columnspan=4)

ImgIButton = ImageTk.PhotoImage(Image.open("AppImages/Insert_insert-button.png"))
IInsert_Button = Button(fInsert,image=ImgIButton,borderwidth = 0 , bg = "White",command = INSERT_TEXT)
IInsert_Button.grid(row=11,columnspan=4)

#Extract frame
fExtract = Frame(r)
fExtract.configure(bg="White")

tELoc = StringVar()
tEKey = StringVar()
tTxtLoc = StringVar()
v2 = IntVar(None,1)

ImgE_back  = ImageTk.PhotoImage(Image.open("AppImages/Extract_Back.png"))
EBack = Button(fExtract,image = ImgE_back,borderwidth = 0 , bg = "White",command = BACK)
EBack.grid(row=0,column=0)

ImgE_back_bulb = ImageTk.PhotoImage(Image.open("AppImages/Extract_Back_Bulb.png"))
EBack_Bulb = Label(fExtract,image = ImgE_back_bulb,borderwidth = 0 , bg = "White")
EBack_Bulb.grid(row=0,column=1,columnspan=2)

ImgE_bulb  = ImageTk.PhotoImage(Image.open("AppImages/Extract_Bulb.png"))
EBulb = Button(fExtract,image = ImgE_bulb,borderwidth = 0 , bg = "White")
EBulb.grid(row=0,column=3)

ImgEXTRACT = ImageTk.PhotoImage(Image.open("AppImages/Extract_extract.png"))
EExtract = Label(fExtract,image = ImgEXTRACT,borderwidth = 0 , bg = "White")
EExtract.grid(row=1,columnspan=4,pady=(0,10))

ImgELoc = ImageTk.PhotoImage(Image.open("AppImages/Extract_img_loc.png"))
ELoc = Label(fExtract,image = ImgELoc,borderwidth = 0 , bg = "White")
ELoc.grid(row=2,columnspan=4)

EEntry = Entry(fExtract,textvariable = tELoc,font = large_font,width = 38,fg="gray20",borderwidth=2)
EEntry.grid(row=3,columnspan=4,pady=(0,20))

ImgEkey = ImageTk.PhotoImage(Image.open("AppImages/Extract_key.png"))
EKey = Label(fExtract,image = ImgEkey,borderwidth = 0 , bg = "White")
EKey.grid(row=4,columnspan=4,pady= (15,0))

EKeyEntry = Entry(fExtract,textvariable = tEKey,font = large_font,width = 22,fg="gray20",borderwidth=2)
EKeyEntry.grid(row=5,column=1,columnspan=2,pady = (0,40))

s1 = Radiobutton(fExtract,variable = v2,value = 1,bg="White")
s1.grid(row=6,column=0)
s2 = Radiobutton(fExtract,variable = v2,value = 2,bg="White")
s2.grid(row=7,column=0)

ImgOption = ImageTk.PhotoImage(Image.open("AppImages/Extract_Option.png"))
Extract_Option = Label(fExtract,image = ImgOption,borderwidth = 0 , bg = "White")
Extract_Option.grid(row = 6, column = 1, rowspan=2 )

NewTxtEntry = Entry(fExtract,textvariable = tTxtLoc,font = large_font,width = 38,fg="gray20",borderwidth=2)
NewTxtEntry.grid(row=8,columnspan=4,pady=(5,20))

ImgEButton = ImageTk.PhotoImage(Image.open("AppImages/Extract_extract_button.png"))
EExtract_Button = Button(fExtract,image=ImgEButton,borderwidth = 0 , bg = "White",command = EXTRACT_TEXT)
EExtract_Button.grid(row=9,columnspan=4)

r.configure(bg="White")
r.mainloop()