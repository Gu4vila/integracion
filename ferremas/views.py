import requests
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse

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
def limpiar_carrito(request, carrito_id):
    url = f"{API_BASE_URL}/carrito/{carrito_id}/limpiar"

    try:
        response = requests.post(url)  # <- usar POST porque así lo define la API
        response.raise_for_status()
        messages.success(request, "Carrito limpiado exitosamente.")
    except requests.exceptions.HTTPError as e:
        try:
            error = e.response.json().get('error', 'Error al limpiar carrito')
        except Exception:
            error = 'Error al limpiar carrito'
        messages.error(request, error)
    except Exception as e:
        messages.error(request, f'Error al conectar con la API: {str(e)}')

    return redirect('carrito', carrito_id=carrito_id)

def eliminar_producto_del_carrito(request, carrito_id, producto_id):
    url = f"{API_BASE_URL}/carrito/{carrito_id}/eliminar/{producto_id}"

    try:
        response = requests.delete(url)  # <- usar DELETE porque así lo define la API
        response.raise_for_status()
        messages.success(request, "Producto eliminado del carrito.")
    except requests.exceptions.HTTPError as e:
        try:
            error = e.response.json().get('error', 'Error al eliminar producto')
        except Exception:
            error = 'Error al eliminar producto'
        messages.error(request, error)
    except Exception as e:
        messages.error(request, f'Error al conectar con la API: {str(e)}')

    return redirect('carrito', carrito_id=carrito_id)

def finalizar_compra(request, carrito_id):
    if request.method == 'POST':
        verificar_url = f"{API_BASE_URL}/carrito/{carrito_id}"
        try:
            verificar_response = requests.get(verificar_url)
            verificar_response.raise_for_status()
            data = verificar_response.json()
            if not data:  # Si la lista está vacía
                messages.warning(request, "El carrito está vacío. Agrega productos antes de finalizar la compra.")
                return redirect('carrito', carrito_id=carrito_id)
        except requests.exceptions.RequestException:
            messages.error(request, "No se pudo verificar el carrito.")
            return redirect('carrito', carrito_id=carrito_id)

        url = f"{API_BASE_URL}/carrito/{carrito_id}/finalizar"
        try:
            response = requests.post(url)
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
def formulario_registro(request):
    return render(request, 'ferremas/formulario_registro.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        # Enviar los datos a la API Flask
        api_url = f"{API_BASE_URL}/usuarios"
        data = {
            'nombre': username,
            'email': email,
            'contrasena': password1
        }

        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 201:
                messages.success(request, "Usuario registrado exitosamente.")
                return redirect('inicio')
            else:
                error_msg = response.json().get('error', 'Error desconocido.')
                messages.error(request, f"Error al registrar usuario: {error_msg}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"No se pudo conectar con el servidor: {e}")

    return render(request, 'ferremas/formulario_registro.html')

def login_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('username')
        contrasena = request.POST.get('password')

        data = {
            'nombre': nombre,
            'contrasena': contrasena
        }

        try:
            response = requests.post(f'{API_BASE_URL}/login', json=data)
            if response.status_code == 200:
                data = response.json()
                request.session['usuario_id'] = data['usuario_id']
                request.session['usuario_nombre'] = data['nombre']
                messages.success(request, f"Bienvenido, {data['nombre']}!")
                return redirect('inicio')
            else:
                error_msg = response.json().get('error', 'Error desconocido.')
                messages.error(request, f"Error al iniciar sesión: {error_msg}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'ferremas/login.html')
def logout_view(request):
    try:
        del request.session['usuario_id']
        del request.session['usuario_nombre']
        messages.success(request, "Has cerrado sesión exitosamente.")
    except KeyError:
        messages.error(request, "No estabas logueado.")

    return redirect('inicio')

@require_POST
def agregar_carrito_ajax(request):
    producto_id = request.POST.get('producto_id')
    cantidad = request.POST.get('cantidad', 1)

    url = f"{API_BASE_URL}/carrito/{CARRITO_ID}/agregar"
    payload = {
        "producto_id": producto_id,
        "cantidad": int(cantidad)
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return JsonResponse({'ok': True, 'mensaje': 'Producto agregado'})
        else:
            error = response.json().get('error', 'Error al agregar producto')
            return JsonResponse({'ok': False, 'error': error})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

def api_carrito(request, carrito_id):
    url = f"{API_BASE_URL}/carrito/{carrito_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        carrito = response.json()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse(carrito, safe=False)