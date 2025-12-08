import os
from typing import List, Optional, Tuple, Dict

from supabase import create_client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), '.env')


def _cargar_env(path: str = ENV_PATH) -> None:
    """Carga un archivo .env simple si existe y no sobreescribe variables ya definidas."""
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                if key not in os.environ:
                    os.environ[key] = value
    except Exception as e:
        print(f"[DB] No se pudo leer {path}: {e}")


_cargar_env()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL o SUPABASE_KEY no configurados. Define las variables de entorno o un archivo .env"
    )

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print('[DB] Usando Supabase como backend de datos')
except Exception as e:
    raise RuntimeError(f"No se pudo inicializar Supabase: {e}")


def init_db():
    # Supabase ya gestiona el esquema; solo validamos que el cliente exista
    if not supabase_client:
        raise RuntimeError('Supabase no está inicializado')


# ---------- Operaciones de tutores ----------

def insertar_tutor(rol: str, nombres: str, apellidos: str, correo: str, password: str) -> int:
    correo = correo.lower()
    try:
        res = supabase_client.table('tutores').insert({
            'rol': rol,
            'nombres': nombres,
            'apellidos': apellidos,
            'correo': correo,
            'password': password
        }).execute()
        data = res.data or []
        return data[0].get('id_tutor') if data else None
    except Exception as e:
        raise RuntimeError(str(e))


def obtener_tutor_por_correo_password(correo: str, password: str) -> Optional[Tuple]:
    correo = correo.lower()
    try:
        res = supabase_client.table('tutores').select('*').eq('correo', correo).eq('password', password).limit(1).execute()
        data = res.data or []
        if not data:
            return None
        row = data[0]
        return (row['id_tutor'], row['nombres'], row['apellidos'], row['rol'], row['correo'], row['password'])
    except Exception as e:
        raise RuntimeError(str(e))


def obtener_tutor_por_id(tutor_id: int) -> Optional[Dict]:
    try:
        res = supabase_client.table('tutores').select('*').eq('id_tutor', tutor_id).limit(1).execute()
        data = res.data or []
        return data[0] if data else None
    except Exception as e:
        raise RuntimeError(str(e))


def ultimo_tutor_id() -> Optional[int]:
    try:
        res = supabase_client.table('tutores').select('id_tutor').order('id_tutor', desc=True).limit(1).execute()
        data = res.data or []
        return data[0]['id_tutor'] if data else None
    except Exception as e:
        raise RuntimeError(str(e))


# ---------- Operaciones de niños ----------

def insertar_nino(tutor_id: int, genero: str, nombres: str, apellidos: str, password_figuras: str) -> int:
    try:
        res = supabase_client.table('ninos').insert({
            'id_tutor': tutor_id,
            'genero': genero,
            'nombres': nombres,
            'apellidos': apellidos,
            'password_figuras': password_figuras
        }).execute()
        data = res.data or []
        return data[0].get('id_nino') if data else None
    except Exception as e:
        raise RuntimeError(str(e))


def ninos_por_tutor(tutor_id: int) -> List[Dict]:
    try:
        res = supabase_client.table('ninos').select('nombres,apellidos,genero,password_figuras').eq('id_tutor', tutor_id).order('nombres').execute()
        return res.data or []
    except Exception as e:
        raise RuntimeError(str(e))


def obtener_nino_login(nombre: str, apellidos: str, password_figuras: str) -> Optional[Tuple]:
    nombre_l = nombre.lower(); apellidos_l = apellidos.lower()
    try:
        res = supabase_client.table('ninos').select('id_nino,nombres,apellidos,id_tutor,password_figuras').eq('password_figuras', password_figuras).execute()
        for row in res.data or []:
            if row['nombres'].lower() == nombre_l and row['apellidos'].lower() == apellidos_l:
                return (row['id_nino'], row['nombres'], row['apellidos'], row['id_tutor'], row['password_figuras'])
        return None
    except Exception as e:
        raise RuntimeError(str(e))


# ---------- Operaciones de actualización ----------

def actualizar_tutor(tutor_id: int, nombres: str, apellidos: str, correo: str, rol: str, password: str) -> None:
    correo = correo.lower()
    try:
        supabase_client.table('tutores').update({
            'nombres': nombres,
            'apellidos': apellidos,
            'correo': correo,
            'rol': rol,
            'password': password
        }).eq('id_tutor', tutor_id).execute()
    except Exception as e:
        raise RuntimeError(str(e))
