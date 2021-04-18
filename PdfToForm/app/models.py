from django.db import models

# Create your models here.
#academic
class add_degree(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class add_field_of_study(models.Model):
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class academic(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	school_or_college=models.CharField(max_length=200)
	degree=models.ForeignKey(add_degree,on_delete=models.CASCADE,null=True,blank=True)
	field_of_study=models.ForeignKey(add_field_of_study,on_delete=models.CASCADE,null=True,blank=True)

	start_date=models.DateField()
	end_date=models.DateField(null=True,blank=True)
	grade=models.CharField(max_length=200,null=True,blank=True)
	def __str__(self):
		return self.name

SALARY_CHOICES = (
	    ('1,50,000','2,00,000'),
	    ('2,00,000','2,50,000'),
	    ('2,50,000','3,00,000'),
	    ('above 3,00,000','>3,00,000'),
	    
	)


#professional
EMP_TYPE_CHOICES = (
	    ('Internship','Internship'),
	    ('Full-time','Full-time'),
	    ('Part-time','Part-time'),
	    ('Self-employed','Self-employed'),
	    ('Freelance','Freelance'),
	    ('Contract','Contract')
	    )


class professional_pro(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	title=models.CharField(max_length=400)
	employment_type=models.CharField(max_length=200, choices=EMP_TYPE_CHOICES,default='Full-time')
	company=models.CharField(max_length=1000)
	current_company=models.BooleanField()
	location=models.CharField(max_length=200)
	start_date=models.DateField()
	end_date=models.DateField()
	description=models.CharField(max_length=500)
	def __str__(self):
		return self.name
class add_project(models.Model):
	email=models.CharField(max_length=200)
	project_name=models.CharField(max_length=200)
	start_date=models.DateField()
	end_date=models.DateField()
	description=models.CharField(max_length=500)
	project_url=models.CharField(max_length=200)
	def __str__(self):
		return self.email
class add_skill(models.Model):
	email=models.CharField(max_length=200)
	name=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class add_certifications(models.Model):
	email=models.CharField(max_length=200)
	title=models.CharField(max_length=200)
	organization=models.CharField(max_length=200)
	issued_date=models.DateField()
	issued_id=models.CharField(max_length=200)
	def __str__(self):
		return self.email



GENDER_CHOICES = (
	    ('MALE','MALE'),
	    ('FEMALE','FEMALE'),
	    
	)
MARITAL_CHOICES = (
	    ('MARRIED','MARRIED'),
	    ('UNMARRIED','UNMARRIED'),
	    
	)

CATEGORY_CHOICES = (
	    ('GENERAL','GENERAL'),
	    ('SC/ST','SC/ST'),
	    ('OBC','OBC')
	    
	)


#social
class social(models.Model):
	#name=models.CharField(max_length=200,null=True,blank=True)
	email=models.CharField(max_length=200)
	dob=models.CharField(max_length=400)
	gender=models.CharField(max_length=1000,choices=GENDER_CHOICES,default='MALE')
	martial=models.CharField(max_length=200, choices=MARITAL_CHOICES,default='MARRIED')
	hometown=models.CharField(max_length=500)
	hobbies=models.CharField(max_length=500)
	mobile_number=models.CharField(max_length=13,null=True,blank=True)
	#category=models.CharField(max_length=500,choices=CATEGORY_CHOICES,default='GENERAL')
	#languages=models.CharField(max_length=500)
	linkedin_profile=models.CharField(max_length=500)
	facebook_profile=models.CharField(max_length=500)
	def __str__(self):
		return self.email