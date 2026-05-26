from django.core.exceptions import ValidationError
import re


def validar_solo_numeros(valor):
  
    if valor:
        if not re.match(r'^[0-9]+$', valor):
            raise ValidationError(
                'Solo se permiten números. Caracteres no válidos: letras, espacios, caracteres especiales.',
                code='solo_numeros'
            )


def validar_nombre(valor):
    
    if valor:
 
        if not re.match(r'^[a-zA-ZáéíóúàèìòùäëïöüÁÉÍÓÚÀÈÌÒÙÄËÏÖÜ\s\-\']+$', valor):
            raise ValidationError(
                'El nombre solo puede contener letras, espacios, guiones y apóstrofes. No se permiten números ni otros caracteres especiales.',
                code='nombre_invalido'
            )


def validar_precio(valor):
   
    if valor:
        if valor < 0:
            raise ValidationError(
                'El precio debe ser un número positivo.',
                code='precio_negativo'
            )


def validar_cantidad(valor):
    
    if valor:
        if valor <= 0:
            raise ValidationError(
                'La cantidad debe ser mayor a 0.',
                code='cantidad_invalida'
            )


def validar_capacidad_mesa(valor):
    
    if valor:
        if valor < 1 or valor > 20:
            raise ValidationError(
                'La capacidad debe estar entre 1 y 20 personas.',
                code='capacidad_invalida'
            )


def validar_numero_mesa(valor):
   
    if valor:
        if valor < 1 or valor > 100:
            raise ValidationError(
                'El número de mesa debe estar entre 1 y 100.',
                code='numero_mesa_invalido'
            )
