def cambio_moneda(cantidad):
    peso_col_a_mx = 145
    return peso_col_a_mx * cantidad

def run():
    print('CALCULADORA')
    print('')
    
    cantidad = float(input('Ingrese cantidad en pesos mx :'))
    
    result = cambio_moneda(cantidad)
    print(result)
    print('${} pesos mexicanos son ${} pesos colombianos'.format(cantidad, result))
if __name__=='__main__':
    run()