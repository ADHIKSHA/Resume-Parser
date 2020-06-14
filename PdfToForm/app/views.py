from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import *
import re
import filetype
from app.convertforms import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import Matcher
from app.skills import *
from app.imageprocess import *

def inpositions(text):
	positions=["Representative","Designer","Engineer","Technician","Developer","Mentor","Assistant","Counselor","Secretary","Manager","Leader"]
	for p in positions:
		if text.find(p)!=-1:
			return True
	return False

def MakeForm(text):
	length=len(text)
	dictionary={}
	flag=0
	count=0
	lines=text.splitlines()
	lines = [x for x in lines if x != '' and x != ' ' and x!='• '] 

	#print(lines)
	dictionary=basicdetails(lines,text)
	dictionary['Address']=" "
	email=dictionary['Email']
	if dictionary['Phone']==None:
		dictionary['Phone']="000000000"
	if dictionary['Email']==None:
		dictionary['Email']="abc@gmail.com"
	if dictionary['Name']==None:
		dictionary['Name']="xyz"
	edu={}
	education=[]
	inter={}
	internship=[]
	pro={}
	project=[]
	skills=[]
	skillmode=0
	no=0
	no_edu=0
	for line in lines:
		check_line=line.lower()
		print('line=',line,flag,count,skillmode)

		if skillmode==1:
			#print(check_line)
			if isskill(check_line)==True:
				line.replace("[^a-zA-Z0-9]", " ")
				skills.append(line)

		if check_line.find("github")!=-1:
			liner=line.find('https://')
			leng=len(line)
			line=line[liner:leng]
			dictionary["github"]=line
			continue
		if check_line.find("linkedin")!=-1:
			dictionary["linkedin"]=line
			continue

		if  bool(re.search(r'\s{0,2}skills\s{0,2}$', check_line)) ==True or line.find("Skills")!=-1 or line.find("SKILLS")!=-1:
			skillmode=1
			flag=0
			count=0
			continue

		if 'trainings' in check_line or 'responsibility' in check_line or 'education' in check_line or 'courses' in check_line or dictionary['Name'] in line or dictionary['Phone'] in line or dictionary['Email'] in line:
			continue
		
		if line =="  ":
			flag=0
			count=0
		if(check_line.find('internships')!=-1) or bool(re.search(r'\s{0,2}experience\s{0,2}$', check_line)) ==True or (check_line.find('employment history')!=-1):
			#print(line)
			flag=2
			count=0
			skillmode=0
			continue
		if bool(re.search(r'\s{0,2}Projects\s{0,2}', line)) ==True or  bool(re.search(r'\s{0,2}project\s{0,2}$', check_line)) ==True or bool(re.search(r'\s{0,2}projects\s{0,2}$', check_line)) ==True:
			flag=3
			count=0
			skillmode=0
			continue

		if flag==2:
				#print('intern',count)
				if bool(re.search(r'[0-9]{4}', check_line))==True and count==0:
						inter['Date']=line
						count=0
						continue

				#print(line)
				
				if count==3 :
					if len(line)>=20:
						if bool(re.search(r'.\s*$', check_line)) ==True:
							if no==0:
								inter['Description']=line
								print('final')
								print(line)
							else:
								des+=line
								inter['Description']=des

							no=0
						else:
							if no==0:
								des=""
							no=no+1
							des+=line+" "
							print(des)
							#inter['Description']=des
							continue
					else:
						inter['Description']=" "

					internship.append(inter)
					#obj=Internship(email=email,position=inter['Position'],company=inter['Company'],date=inter['Date'],desc=inter['Description'])
					#obj.save()
					inter={}
					count=0
				elif count==2 :
					if 'Date' not in inter.keys():
						if bool(re.search(r'[0-9]{4}\s', check_line))==True :
							inter['Date']=line
							count=3
							continue
						else:
							inter['Date']=" "
					else:
						count=3
				elif count==1 :
					if bool(re.search(r'\d', check_line)) ==False :
						line.replace("[^a-zA-Z0-9]", " ")
						inter['Company']=line
						count=2
						continue
					else:
						inter['Company']=" "
				elif count==0 :
					if bool(re.search(r'\d', check_line)) ==False and inpositions(line):
						line.replace("[^a-zA-Z0-9]", " ")
						inter['Position']=line
						count=1
						continue

		if flag==3:
				#print('project',count)
				#print(line)
				if count==3 :
					#if bool(re.search(r'\d', check_line)) ==False :
					if len(line)>=30:
						pro['Description']=line
						count=0
						project.append(pro)
						pro={}
					else:
						if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
							pro['Description']=" "
							project.append(pro)
							pro={}
							pro['Name']=line
							count=1

					
					#obj=Project(email=email,name=pro['Name'],date=pro['Date'],link=pro['Link'],desc=pro['Description'])
					#obj.save()
					#pro={}
					
				elif count==2 :
					if(line.find("https://")!=-1):
						pro['Link']=line
						count=3
					
				elif count==1 :
					if bool(re.search(r'[0-9]{4}\s', check_line))==True and  line.find("https://")==-1:
						pro['Date']=line
						#print(line)
						count=2
					else:
						if(line.find("https://")!=-1):
							pro['Date']=" "
							pro['Link']=line
							count=3
				elif count==0 :
					if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
						line.replace("[^a-zA-Z0-9]", " ")
						pro['Name']=line
						count=1
		

	if 'degrees' in dictionary.keys():
		degrees=dictionary['degrees']	
	else:
		no_edu=1	
	
	word_tokens = word_tokenize(text) 
	
	if no_edu ==0:
		for deg in degrees:
			flag=0
			if deg=="x":
				deg+=" "
			edu={}
			for line in lines:
				check_line=line.lower()
				if check_line.find(deg)!=-1 :
					edu['Degree']=line
					flag=1
				elif flag==1:
				#print(line)
					if bool(re.search(r'\d', check_line)) ==False and 'Institution' not in edu:
						edu['Institution']=line
					if  bool(re.search(r'[0-9]{4}\s', check_line))==True and 'Date' not in edu:
						edu['Date']=line
					if check_line.find("cgpa")!=-1 or check_line.find("%")!=-1 and 'Grade' not in edu:
						edu['Grade']=line
			education.append(edu)


	dictionary["Education"]=education
	dictionary["Internships"]=internship
	dictionary['Projects']=project
	dictionary['Skills']=skills
	#print(skills)
	#print(dictionary)
	return dictionary

def handlefile(myfile):
	kind = filetype.guess('app/static/upload/'+myfile.name)
	if kind is None:
		print('Cannot guess file type!')

	print('File extension: %s' % kind.extension)
	print('File MIME type: %s' % kind.mime)

	if(kind.extension=="pdf"):
		from pdfminer3.layout import LAParams, LTTextBox
		from pdfminer3.pdfpage import PDFPage
		from pdfminer3.layout import LAParams, LTTextBox
		from pdfminer3.pdfpage import PDFPage
		from pdfminer3.pdfinterp import PDFResourceManager
		from pdfminer3.pdfinterp import PDFPageInterpreter
		from pdfminer3.converter import PDFPageAggregator
		from pdfminer3.converter import TextConverter
		import io

		resource_manager = PDFResourceManager()
		fake_file_handle = io.StringIO()
		codec='utf-8'
		converter = TextConverter(resource_manager, fake_file_handle,codec=codec, laparams=LAParams())
		page_interpreter = PDFPageInterpreter(resource_manager, converter)

		with open('app/static/upload/'+myfile.name, 'rb') as fh:

			for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
				
				page_interpreter.process_page(page)
				text = fake_file_handle.getvalue()

		converter.close()
		fake_file_handle.close()
		print(text)

	if(kind.extension=="png" or kind.extension=="jpg" or kind.extension=="webp"):
		from PIL import Image, ImageFilter, ImageChops
		import pytesseract
		from pytesseract import image_to_string
		import cv2
		filename='app/static/upload/'+myfile.name
		imgcv = cv2.imread(filename, 0)
		imp = Image.open(filename)
		text=image_to_string(imp)
		#text = main_fun(imgcv,imp,kind.extension)
		#text=main_fun(im)
		print(text)
		

	dictionary=MakeForm(text)
	#dictionary.replace('"', "'")
	#print(dictionary)
	return dictionary

def handle_uploaded_file(f):  
    with open('app/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

def start(request):
	if request.method == 'POST':
		student = StudentForm(request.POST, request.FILES)  
		if student.is_valid():  
			handle_uploaded_file(request.FILES['file'])  
			dictionary=handlefile(request.FILES['file'])
			return render(request,'Form.html',{'table':dictionary})
	else:  
		student = StudentForm()  
		return render(request,"index.html",{'form':student})

def academic(request):
	email=request.session['email']
	edus = Education.objects.filter(email=email)
	dic={}
	lt=[]
	for elt in edus:
		if elt.degree !=None:
			dic={'degree':elt.degree,
				'date':elt.date,
				'inst':elt.inst,
				'grade':elt.grade,}
			lt.append(dic)
	return render(request,"academic.html",{'table':lt})

def professional(request):
	email=request.session['email']
	edus = Internship.objects.filter(email=email)
	prs=Project.objects.filter(email=email)
	sks=Skills.objects.filter(email=email)
	final={}
	dic={}
	lt=[]
	for elt in edus:
		if elt.position !=None:
			dic={'position':elt.position,
				'company':elt.company,
				'date':elt.date,
				'desc':elt.desc,}
			lt.append(dic)
	final['IN']=lt
	dic={}
	lt=[]
	for elt in prs:
		if elt.name !=None:
			dic={'name':elt.name,
				'date':elt.date,
				'link':elt.link,
				'desc':elt.desc,}
			lt.append(dic)
	final['PR']=lt
	
	for elt in sks:
		stringsk=elt.skilllist

	lt=list(stringsk.split(";"))
	final['SK']=lt
	return render(request,"professional.html",{'table':final})

@csrf_exempt
def save(request):
	if request.method == 'POST':
		name=request.POST.get('Name')
		email=request.POST.get('Email')
		phone=request.POST.get('Phone')
		if email=="abc@gmail.com" or phone=="000000000":
			return HttpResponse("You need to fill correct Phone number and Email id!")
		add=request.POST.get('Address')
		request.session['email']=email
		dict=request.POST
		#print(dict)
		if 'github' in dict.keys():
			github=request.POST.get('github')

		if 'linkedin' in dict.keys():
			linkedin=request.POST.get('linkedin')

		obj=General(name=name,email=email,phone=phone,address=add)
		obj.save()
		if 'eDegree1' not in dict.keys():
			return HttpResponse("You need to add atleast one education field!")
		else:
			total=request.POST.get('edutotal')
			#print(total)
			total=(int(total))
			for i in range(1,total+1):
				deg='eDegree'+ str(i)
				date='eDate'+str(i)
				inst='eInstitution'+str(i)
				grade='eGrade'+str(i)
				obj=Education(email=email,degree=request.POST.get(deg),date=request.POST.get(date),inst=request.POST.get(inst),grade=request.POST.get(grade))
				obj.save()


		if 'iPosition1' not in dict.keys():
			return HttpResponse("You need to add atleast one internship/experience field!")
		else:
			total=request.POST.get('intertotal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				pos='iPosition'+ str(i)
				comp='iCompany'+ str(i)
				date='iDate'+ str(i)
				desc='iDescription'+ str(i)
				obj=Internship(email=email,position=request.POST.get(pos),company=request.POST.get(comp),date=request.POST.get(date),desc=request.POST.get(desc))
				obj.save()

		if 'pName1' not in dict.keys():
			return HttpResponse("You need to add atleast one project field!")
		else:
			total=request.POST.get('prototal')
			total=(int(total))
			#print(total)
			for i in range(1,int(total)+1):
				name='pName'+ str(i)
				date='pDate'+ str(i)
				link='pLink'+ str(i)
				desc='pDescription'+ str(i)
				obj=Project(email=email,name=request.POST.get(name),date=request.POST.get(date),link=request.POST.get(link),desc=request.POST.get(desc))
				obj.save()

		if 'skill1' not in dict.keys():
			return HttpResponse("You need to add atleast one project field!")
		else:
			total=request.POST.get('skilltotal')
			total=(int(total))
			#print(total)
			skill=""
			for i in range(1,int(total)+1):
				skillname='skill'+ str(i)
				if skillname in dict.keys():
					skill+=request.POST.get(skillname)
					skill+=";"
			obj=Skills(email=email,skilllist=skill)
			obj.save()	

	return render(request,"success.html",{'email':email})
