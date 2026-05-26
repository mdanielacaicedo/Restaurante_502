from django import template

register = template.Library()


@register.filter
def precio_colombiano(valor):
   
    if valor is None:
        return "$0"
    
    try:
        
        valor_float = float(valor)
    except (ValueError, TypeError):
        return f"${valor}"
    
  
    partes = f"{valor_float:.2f}".split('.')
    parte_entera = partes[0]
    decimales = partes[1] if len(partes) > 1 else "00"
    

    parte_entera_formateada = ""
    for i, digito in enumerate(reversed(parte_entera)):
        if i > 0 and i % 3 == 0:
            parte_entera_formateada = "." + parte_entera_formateada
        parte_entera_formateada = digito + parte_entera_formateada
    
    if decimales == "00":
        
        return f"${parte_entera_formateada}"
    else:
        
        return f"${parte_entera_formateada},{decimales}"


@register.filter
def precio_simple(valor):
    
    if valor is None:
        return "$0"
    
    try:

        valor_float = float(valor)
        valor_entero = int(valor_float * 1000)
    except (ValueError, TypeError):
        return f"${valor}"
    
    valor_str = str(abs(valor_entero))
    
    valor_str = valor_str.zfill(3)
    
    resultado = ""
    for i, digito in enumerate(reversed(valor_str)):
        if i > 0 and i % 3 == 0:
            resultado = "." + resultado
        resultado = digito + resultado
    
    signo = "-" if valor_entero < 0 else ""
    return f"${signo}{resultado}"
