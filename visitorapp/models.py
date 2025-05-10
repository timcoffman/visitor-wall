from django.db import models

class Wall(models.Model):
	name = models.CharField(max_length=200)
	banner = models.CharField(max_length=200)
	description_html = models.CharField(max_length=2000)
	created_date = models.DateTimeField( "date created" )

	def __str__(self):
		return self.name

class Visitor(models.Model):
	cookie = models.CharField(max_length=4000)
	
	def __str__(self):
		return self.cookie

class Inscription(models.Model):
	wall = models.ForeignKey(Wall,on_delete=models.CASCADE)
	visitor = models.ForeignKey(Visitor,on_delete=models.CASCADE)
	text = models.CharField(max_length=2000)

	def __str__(self):
		return self.text

