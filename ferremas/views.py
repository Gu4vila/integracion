import requests
from django.shortcuts import redirect, render
from django.contrib import messages

API_BASE_URL = 'http://localhost:5000'  # o la URL donde corre tu API Flask
CARRITO_ID = 1  # Aquí podrías gestionar usuarios y carritos reales, pero para prueba dejamos fijo.
def inicio(request):
    return render(request, 'ferremas/inicio.html')

def productos(request):
    nombre = request.GET.get('nombre', '')  # obtiene el parámetro de búsqueda o cadena vacía
    
    try:
        if nombre:
            # Si hay nombre, llama al endpoint de búsqueda con filtro
            response = requests.get(f'{API_BASE_URL}/productos/buscar', params={'nombre': nombre})
        else:
            # Si no hay filtro, obtiene todos los productos
            response = requests.get(f'{API_BASE_URL}/productos')
        
        response.raise_for_status()
        productos = response.json()
    except requests.exceptions.RequestException as e:
        productos = []
        messages.error(request, f"No se pudo obtener la lista de productos: {e}")

    return render(request, 'ferremas/productos.html', {'productos': productos, 'nombre': nombre})

def buscar_productos(request):
    nombre = request.GET.get('nombre', '').strip()
    resultados = []

    if nombre:
        url = f"{API_BASE_URL}/productos/buscar"
        params = {"nombre": nombre}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            resultados = response.json()
        except requests.exceptions.RequestException:
            messages.error(request, "Error al buscar productos.")

    return render(request, 'ferremas/buscar_productos.html', {
        'resultados': resultados,
        'nombre': nombre
    })

def carrito(request, carrito_id):
    url = f"{API_BASE_URL}/carrito/{carrito_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        carrito = response.json()  # Aquí es una lista, no usar .get()
    except Exception as e:
        messages.error(request, f"No se pudo obtener el carrito: {str(e)}")
        carrito = []

    return render(request, 'ferremas/carrito.html', {
        'carrito': carrito,
        'carrito_id': carrito_id
    })

def agregar_carrito(request, producto_id):
    cantidad = 1  # O podrías obtenerla de request.POST si quieres que el usuario elija cantidad

    url = f"{API_BASE_URL}/carrito/{CARRITO_ID}/agregar"
    payload = {
        "producto_id": producto_id,
        "cantidad": cantidad
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            messages.success(request, 'Producto agregado al carrito')
        else:
            error = response.json().get('error', 'Error al agregar producto')
            messages.error(request, error)
    except Exception as e:
        messages.error(request, f'Error en la conexión con la API: {str(e)}')

    return redirect('productos')  
def actualizar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        try:
            nueva_cantidad = int(request.POST.get('cantidad', 1))
            if nueva_cantidad < 1:
                messages.error(request, "La cantidad debe ser al menos 1.")
                return redirect('carrito', carrito_id=CARRITO_ID)
        except ValueError:
            messages.error(request, "Cantidad inválida.")
            return redirect('carrito', carrito_id=CARRITO_ID)

        url = f"{API_BASE_URL}/carrito/{CARRITO_ID}/actualizar"
        payload = {
            "producto_id": producto_id,
            "cantidad": nueva_cantidad
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            messages.success(request, "Cantidad actualizada correctamente.")
        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get('error', 'Error al actualizar cantidad')
            except Exception:
                error = 'Error al actualizar cantidad'
            messages.error(request, error)
        except Exception as e:
            messages.error(request, f'Error al conectar con la API: {str(e)}')

    return redirect('carrito', carrito_id=CARRITO_ID)

def finalizar_compra(request, carrito_id):
    if request.method == 'POST':
        # Verificar si el carrito tiene productos
        verificar_url = f"{API_BASE_URL}/carrito/{carrito_id}"
        try:
            verificar_response = requests.get(verificar_url)
            verificar_response.raise_for_status()
            data = verificar_response.json()
            if not data.get('carrito'):  # lista vacía
                messages.warning(request, "El carrito está vacío. Agrega productos antes de finalizar la compra.")
                return redirect('carrito', carrito_id=carrito_id)
        except:
            messages.error(request, "No se pudo verificar el carrito.")
            return redirect('carrito', carrito_id=carrito_id)

        # Si hay productos, se finaliza la compra
        url = f"{API_BASE_URL}/carrito/{carrito_id}/finalizar"
        try:
            response = requests.post(url, json={})  # JSON vacío
            response.raise_for_status()
            messages.success(request, "Compra finalizada exitosamente.")
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                messages.error(request, f"Error al finalizar compra: {e.response.text}")
            else:
                messages.error(request, f"Error al finalizar compra: {str(e)}")
    return redirect('carrito', carrito_id=carrito_id)

def ventas_resumen(request):
    return render(request, 'ferremas/ventas_resumen.html')
def usuarios(request):
    return render(request, 'ferremas/usuarios.html')

