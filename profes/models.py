# -*- encoding: utf-8 -*-
from django.db import models


class Profesor(models.Model):
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    pais = models.CharField(max_length=200,default='Spain')
    provincia = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    email = models.CharField(max_length=250)
    edad = models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return self.nombre + ' ' +  self.apellidos


class Telefono(models.Model):
    numero = models.CharField(max_length=30)
    profesor = models.ForeignKey(Profesor,related_name='telefonos')

    def __unicode__(self):
        return unicode.encode(self.numero)



TIPOS_CURSOS = (
    ('online', 'Online'),
    ('presencial', 'Presencial'),
    ('semipresencial', 'Semipresencial'),
    ('subvencionado', 'Subvencionado'),
)

class Categoria(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=140)

    def __unicode__(self):
        return self.codigo + ' - ' + self.nombre


class Curso(models.Model):
    numero = models.CharField(max_length=20)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    posibilidades = models.ManyToManyField(Profesor,through='Posibilidad')
    tipo = models.CharField(max_length=100,choices=TIPOS_CURSOS)
    categoria = models.ForeignKey(Categoria,related_name='cursos')

    def __unicode__(self):
        return self.titulo


class Tarea(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField()
    profesor = models.ForeignKey(Profesor)

    def __unicode__(self):
        return str(self.created_at)



class Posibilidad(models.Model):
    modified_at = models.DateTimeField(auto_now=True)
    alumnos_minimos = models.PositiveIntegerField()
    profesor = models.ForeignKey(Profesor,)
    curso = models.ForeignKey(Curso)

    def __unicode__(self):
        return self.curso.titulo + ' -------- ' + self.profesor.nombre + ' ' + self.profesor.apellidos


class Edicion(models.Model):
    numero =  models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    calificacion = models.IntegerField(default=0)
    profesor = models.ForeignKey(Profesor,related_name='ediciones')
    curso = models.ForeignKey(Curso,related_name='ediciones')

    def __unicode__(self):
        return self.numero + ' - ' + self.curso.titulo

    def codigo(self):
        return self.curso.numero+'-'+self.numero

    def alumnos_minimos(self):
        return Posibilidad.objects.get(profesor_id = self.profesor_id,curso_id = self.curso_id).alumnos_minimos