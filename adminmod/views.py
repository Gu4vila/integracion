from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required


API_BASE_URL = 'http://localhost:5000'

def adminlogin(request):
    if request.method == 'POST':
        nombre = request.POST.get('username')
        contrasena = request.POST.get('password')

        data = {
            'nombre': nombre,
            'contrasena': contrasena
        }

        try:
            response = requests.post(f'{API_BASE_URL}/login_admin', json=data)
            if response.status_code == 200:
                data = response.json()
                request.session['usuario_id'] = data['usuario_id']
                request.session['usuario_nombre'] = data['nombre']
                messages.success(request, f"Bienvenido, {data['nombre']}!")
                return redirect('panel_admin')  # Redirige al panel de administración
            else:
                error_msg = response.json().get('error', 'Error desconocido.')
                messages.error(request, f"Error al iniciar sesión: {error_msg}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"No se pudo conectar con la API: {e}")
    return render(request, 'adminmod/adminlogin.html')

def admin_logout_view(request):
    request.session.flush() 
    messages.success(request, "Has cerrado sesión correctamente.") 
    return redirect('adminlogin')

# Listar productos
def admin_productos(request):
    try:
        response = requests.get(f'{API_BASE_URL}/productos')
        response.raise_for_status()
        productos = response.json()
    except requests.exceptions.RequestException as e:
        productos = []
        messages.error(request, f"No se pudo obtener la lista de productos: {e}")
    return render(request, 'adminmod/admin_productos.html', {'productos': productos})

# Crear nuevo producto
def admin_producto_crear(request):
    if request.method == 'POST':
        datos = {
            'codigo': request.POST.get('codigo'),
            'nombre': request.POST.get('nombre'),
            'marca': request.POST.get('marca'),
            'precio': request.POST.get('precio'),
            'stock': request.POST.get('stock'),
        }

        imagen = request.FILES.get('imagen')
        files = {'imagen': imagen} if imagen else {}

        try:
            response = requests.post(
                f'{API_BASE_URL}/productos',
                data=datos,         # Form fields
                files=files         # Imagen como archivo
            )
            if response.status_code == 200 or response.status_code == 201:
                messages.success(request, "Producto creado exitosamente.")
                return redirect('admin_productos')
            else:
                messages.error(request, response.json().get('error', 'Error desconocido'))
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error al crear el producto: {e}")

    return render(request, 'adminmod/admin_producto_form.html')

# Editar producto existente
def admin_producto_editar(request, producto_id):    
    if request.method == 'POST':
        datos = {
            'codigo': request.POST.get('codigo'),
            'nombre': request.POST.get('nombre'),
            'marca': request.POST.get('marca'),
            'precio': request.POST.get('precio'),
            'stock': request.POST.get('stock'),
        }
        try:
            response = requests.put(f'{API_BASE_URL}/productos/{producto_id}', json=datos)
            if response.status_code == 200:
                messages.success(request, "Producto actualizado exitosamente.")
                return redirect('admin_productos')
            else:
                messages.error(request, response.json().get('error', 'Error desconocido'))
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error al actualizar el producto: {e}")
    
    else:
        try:
            response = requests.get(f'{API_BASE_URL}/productos/{producto_id}')
            response.raise_for_status()
            producto = response.json()
        except requests.exceptions.RequestException as e:
            messages.error(request, f"No se pudo obtener el producto: {e}")
            return redirect('admin_productos')
        return render(request, 'adminmod/admin_producto_form.html', {'producto': producto})

def admin_producto_eliminar(request, producto_id):
    try:
        response = requests.delete(f'{API_BASE_URL}/productos/{producto_id}')
        if response.status_code == 200:
            messages.success(request, "Producto eliminado exitosamente.")
        else:
            messages.error(request, response.json().get('error', 'Error desconocido'))
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al eliminar el producto: {e}")
    return redirect('admin_productos')

def admin_usuarios(request):
    return render(request, 'adminmod/admin_usuarios.html', {})


def users_basicos(request):
    try:
        response = requests.get(f'{API_BASE_URL}/usuarios')
        response.raise_for_status()
        usuarios = response.json()
        
    except requests.exceptions.RequestException as e:
        usuarios = []
        messages.error(request, f"No se pudo obtener la lista de usuarios: {e}")
    return render(request, 'adminmod/users_basicos.html', {'usuarios': usuarios})

def eliminar_user(request, usuario_id):
    try:
        response = requests.post(f'{API_BASE_URL}/usuarios/{usuario_id}')
        if response.status_code == 200:
            messages.success(request, "Usuario eliminado exitosamente.")
        else:
            messages.error(request, response.json().get('error', 'Error desconocido'))
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al eliminar el usuario: {e}")
    return redirect('users_basicos')






def eliminar_user_admin(request, usuario_id):
    try:
        response = requests.post(f'{API_BASE_URL}/eliminar_usuario_admin/{usuario_id}')
        if response.status_code == 200:
            messages.success(request, "Usuario eliminado exitosamente.")
        else:
            messages.error(request, response.json().get('error', 'Error desconocido'))
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al eliminar el usuario: {e}")
    return redirect('users_admins')


def users_admins(request):
    try:
        response = requests.get(f'{API_BASE_URL}/usuarios_admin')
        response.raise_for_status()
        usuarios = response.json()
        
    except requests.exceptions.RequestException as e:
        usuarios = []
        messages.error(request, f"No se pudo obtener la lista de usuarios: {e}")
    return render(request, 'adminmod/users_admins.html', {'usuarios': usuarios})


def eliminar_user_admin(request, usuario_id):
    try:
        response = requests.post(f'{API_BASE_URL}/eliminar_usuario_admin/{usuario_id}')
        if response.status_code == 200:
            messages.success(request, "Usuario eliminado exitosamente.")
        else:
            messages.error(request, response.json().get('error', 'Error desconocido'))
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al eliminar el usuario: {e}")
    return redirect('users_admins')



def register_user_admin(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        contrasena_confirm = request.POST.get('contrasena_confirm')

        # Validar que las contraseñas coincidan
        if contrasena != contrasena_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'adminmod/register_user_admin.html', {
                'nombre': nombre,
                'email': email,
            })

        data = {
            'nombre': nombre,
            'email': email,
            'contrasena': contrasena
        }

        try:
            response = requests.post(f'{API_BASE_URL}/register_admin', json=data)
            response.raise_for_status()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('users_admins')

        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error al registrar el usuario: {e}')
            return render(request, 'adminmod/user_admin_form.html')

    return render(request, 'adminmod/user_admin_form.html')

def modificar_user_admin(request, usuario_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        contrasena_confirm = request.POST.get('contrasena_confirm')

        if contrasena or contrasena_confirm:
            if contrasena != contrasena_confirm:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'adminmod/user_admin_form.html', {
                    'usuario_id': usuario_id,
                    'nombre': nombre,
                    'email': email,
                    'editar': True
                })
        else:
            contrasena = None  # para que la API no actualice la contraseña

        data = {
            'nombre': nombre,
            'email': email,
            'contrasena': contrasena
        }

        try:
            response = requests.put(f'{API_BASE_URL}/modificar_usuario_admin/{usuario_id}', json=data)
            if response.status_code == 200:
                messages.success(request, 'Usuario modificado correctamente.')
                return redirect('users_admins')
            else:
                messages.error(request, response.json().get('error', 'Error desconocido'))
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error al modificar el usuario: {e}')

        return render(request, 'adminmod/user_admin_form.html', {
            'usuario_id': usuario_id,
            'nombre': nombre,
            'email': email,
            'editar': True
        })

    # GET → Cargar datos del usuario desde la API
    try:
        response = requests.get(f'{API_BASE_URL}/usuarios_admin')
        response.raise_for_status()
        usuarios = response.json()
        usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
        if not usuario:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('users_admins')
        return render(request, 'adminmod/user_admin_form.html', {
            'usuario_id': usuario_id,
            'nombre': usuario['nombre'],
            'email': usuario['email'],
            'editar': True
        })
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error al obtener los datos del usuario: {e}')
        return redirect('users_admins')

def admin_ventas(request):
    return render(request, 'adminmod/admin_ventas.html', {})

def panel_admin(request):
    return render(request, 'adminmod/panel_admin.html', {})
