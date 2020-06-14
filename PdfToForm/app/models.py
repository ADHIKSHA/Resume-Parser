from django.db import models

# Create your models here.
class General(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100,primary_key=True)
	phone=models.CharField(max_length=50)
	address=models.CharField(max_length=200)
	github=models.CharField(max_length=100,blank=True)
	linkedin=models.CharField(max_length=100,blank=True)
	class Meta:
		db_table="General"
		
class Education(models.Model):
	email=models.CharField(max_length=100)
	degree=models.CharField(max_length=100,blank=True,null=True)
	date=models.CharField(max_length=100,blank=True,null=True)
	inst=models.CharField(max_length=50,blank=True,null=True)
	grade=models.CharField(max_length=50,blank=True,null=True)
	class Meta:
		db_table="Education"

class Internship(models.Model):
	email=models.CharField(max_length=100)
	position=models.CharField(max_length=100,blank=True,null=True)
	company=models.CharField(max_length=100,blank=True,null=True)
	date=models.CharField(max_length=50,blank=True,null=True)
	desc=models.CharField(max_length=200,blank=True,null=True)
	class Meta:
		db_table="Internship"

class Project(models.Model):
	email=models.CharField(max_length=100)
	name=models.CharField(max_length=100,blank=True,null=True)
	date=models.CharField(max_length=100,blank=True,null=True)
	link=models.CharField(max_length=50,blank=True,null=True)
	desc=models.CharField(max_length=200,blank=True,null=True)
	class Meta:
		db_table="Project"

class Skills(models.Model):
	email=models.CharField(max_length=100)
	skilllist=models.CharField(max_length=500,blank=True)