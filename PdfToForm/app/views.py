from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
import re
import filetype
from .convertforms import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import Matcher
from .skills import *
from .imageprocess import *

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
	text=text.replace(',','\n')

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
	dictionary['marital']="unmarried"
	edu={}
	education=[]
	inter={}
	internship=[]
	pro={}
	project=[]
	skills=[]
	trainings=0
	trainings=[]
	train={}
	skillmode=0
	no=0
	no_edu=0
	for line in lines:
		check_line=line.lower()
		line=re.sub(r"[^a-zA-Z0-9%-.@:\'\"$+/]"," ",line)
		#print('line=',line,flag,count,skillmode)

		if skillmode==1:
			#print(check_line)
			if isskill(check_line)==True:
				line=line.replace("[^a-zA-Z0-9]", " ")
				skills.append(line)

		if check_line.find("github")!=-1:
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

		if 'responsibility' in check_line or 'education' in check_line  or dictionary['Name'] in line or dictionary['Phone'] in line or dictionary['Email'] in line:
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
		if (check_line.find('projects')!=-1) or  bool(re.search(r'\s{0,2}project\s{0,2}$', check_line)) ==True or bool(re.search(r'\s{0,2}projects\s{0,2}$', check_line)) ==True:
			flag=3
			count=0
			skillmode=0
			continue

		if(check_line.find('trainings')!=-1)  or (check_line.find('certifications')!=-1):
			#print(line)
			flag=4
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
				employment_type=find_emp_type(check_line)
				if employment_type !=None:
					inter['EmpType']=employment_type
				if count==3 :
					
					if len(line)>=20:
						if bool(re.search(r'.\s*$', check_line)) ==True:
							if no==0:
								inter['Description']=line
								#print('final')
								#print(line)
							else:
								des+=line
								inter['Description']=des

							no=0
						else:
							if no==0:
								des=""
							no=no+1
							des+=line+" "
							#print(des)
							#inter['Description']=des
							continue
					else:
						inter['Description']=" "

					if 'EmpType' not in inter.keys():
						inter['EmpType']="Internship"
					if 'Date' not in inter.keys():
						inter['Date']="2000-01-01"
					if 'EndDate' not in inter.keys():
						inter['EndDate']="2000-01-01"
					internship.append(inter)
					#obj=Internship(email=email,position=inter['Position'],company=inter['Company'],date=inter['Date'],desc=inter['Description'])
					#obj.save()
					inter={}
					count=0
				elif count==2 :
					if 'Date' not in inter.keys():
						if bool(re.search(r'[0-9]{4}', check_line))==True :
							l=re.findall(r'[0-9]{4}', check_line)
							if len(l)==1:
								start_date=l[0]+"-01-01"
								edu['Date']=start_date
								end_date="2000-01-01"
								edu['EndDate']=end_date
							if len(l)==2:
								start_date=l[0]+"-01-01"
								edu['Date']=start_date
								end_date=l[1]+"-01-01"
								edu['EndDate']=end_date
							count=3
							continue
						else:
							inter['Date']="2000-01-01"
					else:
						count=3
				elif count==1 :
					if bool(re.search(r'\d', check_line)) ==False :
						line=re.sub(r"[^a-zA-Z0-9]"," ",line)
						inter['Company']=line
						count=2
						continue
					else:
						inter['Company']=" "
				elif count==0 :
					if bool(re.search(r'\d', check_line)) ==False and inpositions(line):
						line=re.sub(r"[^a-zA-Z]"," ",line)
						inter['Position']=line
						count=1
						continue

		if flag==3:
				#print('project',count)
				#print(line)
				if count==3 :
					#if bool(re.search(r'\d', check_line)) ==False :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
					else:
						newname=line

					pro['Description']=" "
					if 'Link' not in pro.keys():
						pro['Link']="https://"
					if 'Date' not in pro.keys():
						pro['Date']="2000-01-01"
					if 'EndDate' not in pro.keys():
						pro['EndDate']="2000-01-01"
					project.append(pro)
					pro={}
					pro['Name']=newname
					count=1

					
					#obj=Project(email=email,name=pro['Name'],date=pro['Date'],link=pro['Link'],desc=pro['Description'])
					#obj.save()
					#pro={}
					
				elif count==2 :
					if(line.find("https://")!=-1):
						pro['Link']=line
					else:
						pro['Link']=line
					pro['Description']=""
					project.append(pro)
					pro={}
					count=0
					
				elif count==1 :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
						count=2
					else:
						if(line.find("https://")!=-1):
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=line
							count=3
						else:
							print("here")
							print(line)
							print(pro['Name'])
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=""
							project.append(pro)
							pro={}
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=""
							pro['Name']=line
							project.append(pro)
							pro={}
							count=0

				elif count==0 :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
						count=2
					else:
						if(line.find("https://")!=-1):
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=line
							count=3
						else:
							print(line)
							pro['Name']=line
							count=1
		if flag==4:
			if count==0:
				if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['Title']=line
					count=1

			elif count==1:
				if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['organization']=line
					count=2
				elif bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
					l=re.findall(r'[0-9]{4}', check_line)
					#print(l)
					if len(l)==1:
						start_date=l[0]+"-01-01"
						train['Date']=start_date
						#print(line)
					count=1

			elif count==2:
				if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1 and 'Date' not in train.keys():
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							train['Date']=start_date
						#print(line)
						count=3
				if 'Date' in train.keys():
					count=3
					continue

			elif count==3:
				if len(line)<=50 and bool(re.search(r'\d', check_line)) ==True or  line.find("https://")==-1:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['credentials']=line
					if 'Date' not in train.keys():
						train['Date']="2000-01-01"
					trainings.append(train)
					train={}
					count=0
				elif bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['Title']=line
					train['credentials']="undefined"
					if 'Date' not in train.keys():
						train['Date']="2000-01-01"
					trainings.append(train)
					train={}
					count=0


	if 'degrees' in dictionary.keys():
		degrees=dictionary['degrees']	
	else:
		no_edu=1	
	
	word_tokens = nltk.word_tokenize(text) 
	
	if no_edu ==0:
		for deg in degrees:
			flag=0
			if deg=="x":
				deg+=" "
			edu={}
			for line in lines:
				check_line=line.lower()
				if check_line.find(deg)!=-1 :
					line=re.sub(r"[^a-zA-Z]"," ",line)
					edu['Degree']=line
					field_of_study=find_fields(check_line)
					if field_of_study!=None and 'field_of_study' not in edu:
						edu['field_of_study']=field_of_study
					flag=1
				elif flag==1:
				#print(line)
					if bool(re.search(r'\d', check_line)) ==False and 'Institution' not in edu:
						edu['Institution']=line
					if  bool(re.search(r'[0-9]{4}', check_line))==True and 'Date' not in edu:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							edu['Date']=start_date
							end_date="2000-01-01"
							edu['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							edu['Date']=start_date
							end_date=l[1]+"-01-01"
							edu['EndDate']=end_date
						#edu['Date']=line

					if check_line.find("grade")!=-1 or check_line.find("gpa")!=-1 or check_line.find("cgpa")!=-1 or check_line.find("%")!=-1 and 'Grade' not in edu:
						line=re.sub(r"[^0-9.%]"," ",line)
						edu['Grade']=line
					field_of_study=find_fields(check_line)
					if field_of_study!=None and 'field_of_study' not in edu:
						edu['field_of_study']=field_of_study
			education.append(edu)

	dictionary['Trainings']=trainings
	dictionary["Education"]=education
	dictionary["Internships"]=internship
	dictionary['Projects']=project
	dictionary['Skills']=skills
	#print(skills)
	print(dictionary)
	
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
			email = dictionary['Email']
			return render(request,'Form.html',{'table':dictionary,'email':email})
	else:  
		student = StudentForm()  
		return render(request,"index.html",{'form':student})

def academics(request):
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
	if request.method=="POST":
		name=request.POST.get('Name')
		email=request.POST.get('Email')
		phone=request.POST.get('Phone')
		if email=="abc@gmail.com" or phone=="000000000":
			return HttpResponse("You need to fill correct Phone number and Email id!")
		#add=request.POST.get('Address')
		request.session['email']=email
		dict=request.POST
		github=""
		linkedin=""
		address=""
		gender=""
		dob=""
		hobbies=""
		marital=""
		#print(dict)
		if 'github' in dict.keys():
			github=request.POST.get('github')

		if 'linkedin' in dict.keys():
			linkedin=request.POST.get('linkedin')

		if 'Address' in dict.keys():
			address=request.POST.get('Address')

		if 'gender' in dict.keys():
			gender=request.POST.get('gender')

		if 'DOB' in dict.keys():
			dob=request.POST.get('DOB')

		if 'Hobbies' in dict.keys():
			hobbies=request.POST.get('Hobbies')

		if 'Marital' in dict.keys():
			marital=request.POST.get('Marital')

		obj=social(email = email,dob=dob,gender=gender,martial=marital,hometown=address,hobbies=hobbies,mobile_number=phone,linkedin_profile=linkedin,facebook_profile=github)
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
				field='efield'+str(i)
				if request.POST.get(deg)== None:
					continue
				field_of_study=request.POST.get(field)
				degree=request.POST.get(deg)
				#place for field of study
				count_degree=add_degree.objects.filter(name=degree).count()
				count_field=add_field_of_study.objects.filter(name=field_of_study).count()
				if count_degree==0:
					obj=add_degree(name=degree)
					obj.save()
				if count_field==0:
					obj=add_field_of_study(name=field_of_study)
					obj.save()
				degree_id=add_degree.objects.filter(name=degree).values('id')[0]['id']
				field_of_study_id=add_field_of_study.objects.filter(name=field_of_study).values('id')[0]['id']
				#field_of_study_id=add_field_of_study.objects.filter(name=field_of_study).values('id')
				obj=academic(name=name,email=email,school_or_college=request.POST.get(inst),degree_id=degree_id,field_of_study_id=field_of_study_id,start_date=request.POST.get(date),end_date="2020-01-01",grade=request.POST.get(grade))
				obj.save()
				#academic_obj=academic.objects.filter(email=email).all()

		if 'iPosition1' not in dict.keys():
			return HttpResponse("You need to add atleast one internship field!")
		else:
			total=request.POST.get('intertotal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				pos='iPosition'+ str(i)
				comp='iCompany'+ str(i)
				date='iDate'+ str(i)
				idesc='iDescription'+ str(i)
				checker='icheck'+str(i)
				emptype='EmpType'+str(i)
				iloc='iLocation'+str(i)
				ienddate='iEndDate'+ str(i)
				title=request.POST.get(pos)
				if title==None:
					continue
				emp_type=request.POST.get(emptype)
				company=request.POST.get(comp)
				location=request.POST.get(iloc)
				start_date=request.POST.get(date)
				#end_date=request.POST.get(ienddate)
				desc=request.POST.get(idesc)
				check=request.POST.get(checker)
				if check=='on':
					end_date=datetime.datetime.now()
					check=True
				else:
					end_date=request.POST.get(ienddate)
					check=False

			
				a=professional_pro(name=name,email=email,title=title,
				employment_type=emp_type,company=company,current_company=check,
				location=location,start_date=start_date,end_date=end_date,description=desc)
				a.save()

		if 'pName1' not in dict.keys():
			return HttpResponse("You need to add atleast one project field!")
		else:
			total=request.POST.get('prototal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				pos='pName'+ str(i)
				#comp='i'+ str(i)
				pdate='pDate'+ str(i)
				pdesc='pDescription'+ str(i)
				link='pLink'+str(i)
				penddate='pEndDate'+ str(i)

				name=request.POST.get(pos)
				if name==None:
					continue
				start_date=request.POST.get(date)
				description=request.POST.get(pdesc)
				plink=request.POST.get(link)
				end_date=request.POST.get(penddate)

				a=add_project(email=email,project_name=name,
				start_date=start_date,end_date=end_date,description=description,project_url=plink)
				a.save()

		if 'skill1' not in dict.keys():
			return HttpResponse("You need to add atleast one skill field!")
		else:
			total=request.POST.get('skilltotal')
			total=(int(total))
			#print(total)
			for i in range(1,int(total)+1):
				skillname='skill'+ str(i)
				if skillname==None:
					continue
				if skillname in dict.keys():
					skill=request.POST.get(skillname)
				obj=add_skill(email=email,name=skill)
				obj.save()	

		if 'tTitle1' in dict.keys():
			total=request.POST.get('traintotal')
			#print(total)
			total=(int(total))
			
			for i in range(1,int(total)+1):
				title='tTitle'+ str(i)
				#comp='i'+ str(i)
				organ='tOrga'+ str(i)
				tDate='tDate'+ str(i)
				tcred='tcred'+str(i)
				#penddate='pEndDate'+ str(i)

				ttitle=request.POST.get(title)
				if ttitle==None:
					continue
				start_date=request.POST.get(tDate)
				organization=request.POST.get(organ)
				credentials=request.POST.get(tcred)

				a=add_certifications(email=email,title=ttitle,
				organization=organization,issued_date=start_date,issued_id=credentials)
				a.save()


	return render(request,"success.html",{'email':email})
