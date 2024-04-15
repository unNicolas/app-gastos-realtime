import streamlit as st
import asyncio
from datetime import datetime
from event_hubs import run
import logging  # Importa el módulo logging

# Configura el nivel de registro para depuración
logging.basicConfig(level=logging.DEBUG)
# Configura un controlador de registro para enviar mensajes a la consola
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

async def main():
    # Título del formulario
    st.title('Registro de Gastos')

    # Widgets para ingresar datos
    fecha = st.date_input('Fecha del Gasto', value=None, min_value=None, max_value=None, key=None)
    print(fecha)
    categoria = {
        'Alimentacion': ['Supermercado', 'Verduleria', 'Carniceria', 'Snacks Saludables', 'Comida Chatarra'],
        'Transporte': ['Reparacion Auto', 'Mejoras Auto', 'Combustible', 'Peaje', 'Multas', 'Impuestos', 'Naranjitas'],
        'Entretenimiento': ['Fiestitas', 'Complementos fiestitas', 'Viajes', 'Resto', 'Delivery', 'Bailes', 'Boliches', 'Otros'],
        'Vestimenta': ['Compra Ropa', 'Calzado', 'Reparación'],
        'Hogar': ['Reparaciones', 'Mejoras', 'Mobiliario', 'Limpieza'],
        'Cuidado Personal': ['Proteina', 'Creatina', 'Vitaminas', 'Skin Care', 'Otros Suplementos', 'Atencion Medica'],
        'Otros': [] # Actualmente no hay subcategorías
    }
    
    selected_categoria = st.selectbox('Selecciona una Categoría:', list(categoria.keys()))
    
    # Verificar si es Otros, ya que no tiene subcategoría
    if selected_categoria != 'Otros':
        # En base a la categoría escogida busca las sub disponibles
        subcategoria = categoria[selected_categoria]
        # Crea un selectbox para las subcategorías
        selected_subcategoria = st.selectbox('Selecciona una Subcategoría:', subcategoria)
    else:
        selected_subcategoria = None
    
    max_value = 1000000.00
    importe = st.number_input('Importe del Gasto', min_value=0.0, max_value=max_value, step=0.01)
    if importe is not None and importe > max_value:
        st.error(f'Importe incorrecto. El valor máximo permitido es {max_value}.')
    medio_pago = st.selectbox('Medio de Pago', ['Efectivo', 'Transferencia', 'Tarjeta de Crédito', 'Tarjeta de Débito'])
    
    # Opción para cuotas en caso de elegir Tarjeta de Crédito
    if medio_pago == 'Tarjeta de Crédito':
        tarjeta = st.selectbox('Tarjeta de Crédito', ['Santander Visa', 'Santander Mastercard', 'Galicia Visa', 'Galicia Mastercard'])
        cuotas = st.number_input('Cantidad de Cuotas', min_value=1, max_value=12, step=1)
    
    # Botón para guardar
    if st.button('Guardar Gasto'):
        if fecha is None or importe is None:
            st.error('Falta completar un campo. Por favor, asegúrate de llenar todos los campos antes de guardar.')
        else:
            fecha_carga = datetime.now()
            event_data = {
            "fecha": fecha.isoformat(),
            "importe": importe,
            "categoria": selected_categoria,
            "subcategoria": selected_subcategoria,
            "mediopago": medio_pago,
            "tarjeta": tarjeta if medio_pago == 'Tarjeta de Crédito' else None,
            "cuotas": cuotas if medio_pago == 'Tarjeta de Crédito' else None,
            "fechacarga": fecha_carga.isoformat()  # Convertir a cadena ISO
            }
            #print("Objeto JSON generado:", event_data)
            # Lanzar la función de envío de eventos de forma asíncrona
            # Convertir el objeto de datos a una cadena JSON
            #json_data = json.dumps(event_data)

            # Codificar la cadena JSON en UTF-8
            #encoded_data = json_data.encode('utf-8')

            await run(event_data)


# Ejecutar la función main de forma asíncrona
asyncio.run(main())