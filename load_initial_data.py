import requests
import json

portfolio_items = [
    {
        "id": "res_depto_providencia",
        "title": "Departamento Luminoso en Providencia",
        "shortDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
        "fullDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quibusdam, accusamus! Earum ullam harum facere voluptas. Delectus ullam, nulla deleniti amet, porro deserunt expedita aperiam cupiditate ducimus distinctio vel dolorum magni.",
        "imageUrl": "https://i.ytimg.com/vi/z-ARZWQ2ccw/maxresdefault.jpg",
        "category": "Residencial",
        "location": "Providencia, Santiago",
        "year": 2023
    },
    {
        "id": "com_oficina_moderna",
        "title": "Oficina Colaborativa - Centro",
        "shortDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
        "fullDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quibusdam, accusamus! Earum ullam harum facere voluptas. Delectus ullam, nulla deleniti amet, porro deserunt expedita aperiam cupiditate ducimus distinctio vel dolorum magni.",
        "imageUrl": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "category": "Comercial",
        "location": "Santiago Centro, Santiago",
        "year": 2022
    },
    {
        "id": "rem_bano_minimalista",
        "title": "Remodelación Baño Minimalista",
        "shortDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit.",
        "fullDescription": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quibusdam, accusamus! Earum ullam harum facere voluptas. Delectus ullam, nulla deleniti amet, porro deserunt expedita aperiam cupiditate ducimus distinctio vel dolorum magni.",
        "imageUrl": "https://img.freepik.com/fotos-premium/bano-minimalista-moderno-impresionante-ducha-blanca-lujo-resolucion-4k-como-pieza-central_1189966-2709.jpg?w=1380",
        "category": "Remodelación",
        "location": "Vitacura, Santiago",
        "year": 2024
    },
]

backend_url = "http://localhost:5000/api/projects"

print("Iniciando carga de datos iniciales...")

for item in portfolio_items:
    try:
        response = requests.post(backend_url, json=item)
        response.raise_for_status()
        
        print(f"Proyecto '{item['title']}' - Respuesta: {response.status_code} - {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"Error al añadir el proyecto '{item['title']}': {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Respuesta del servidor: {e.response.status_code} - {e.response.json()}")
    except Exception as e:
        print(f"Error inesperado con el proyecto '{item['title']}': {e}")

print("Proceso de carga de datos finalizado.")